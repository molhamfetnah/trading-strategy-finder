# NASDAQ Trading Strategy Finder - Complete Documentation

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [Data Pipeline](#3-data-pipeline)
4. [Indicators Module](#4-indicators-module)
5. [Signals Module](#5-signals-module)
6. [ML Filter](#6-ml-filter)
7. [Backtest Engine](#7-backtest-engine)
8. [Performance Metrics](#8-performance-metrics)
9. [Dashboard & Reports](#9-dashboard--reports)
10. [Strategies](#10-strategies)
11. [Demo Results](#11-demo-results)
12. [Setup & Usage](#12-setup--usage)
13. [File Reference](#13-file-reference)
14. [Glossary](#14-glossary)

---

## 1. Project Overview

### What This Project Does

A hybrid ML-powered trading algorithm that:
1. Loads historical NASDAQ futures data (1min and 15min candles)
2. Calculates technical indicators (RSI, EMA, MACD, etc.)
3. Generates buy/sell signals based on indicator rules
4. Enhances signals using a Random Forest ML classifier
5. Simulates trades with realistic stop loss/take profit
6. Compares three trading strategies: Scalping, Day Trading, Intraday
7. Outputs performance metrics and visual dashboards

### Why It Was Built

- Proof of concept for automated trading strategy selection
- To find the most profitable timeframe/strategy for NASDAQ futures
- To demonstrate hybrid approach (rules + ML) for signal generation
- To create a production-ready codebase for live trading integration

### Test Period

- **Training Data:** January 1 - June 30, 2025 (6 months)
- **Test Data:** July 1 - September 26, 2025 (3 months)
- **Total Candles:** 87,243 (test set)
- **Initial Capital:** $10,000
- **Final Capital:** $10,107.66 (Scalping best result)

---

## 2. Architecture

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         MAIN.PY                                  │
│                    Entry Point                                   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┬─────────────────┐
        ▼                 ▼                 ▼                 ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│    Scalping    │  │  Day Trading   │  │   Intraday     │  │   Reports      │
│    (1min)      │  │    (15min)     │  │    (15min)     │  │                │
└───────┬────────┘  └───────┬────────┘  └───────┬────────┘  └───────┬───────┘
        │                   │                   │                   │
        ▼                   ▼                   ▼                   │
┌─────────────────────────────────────────────────────────────────┐
│                      BACKTEST ENGINE                             │
│  - Tracks positions    - Entry/Exit logic    - Capital tracking │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PERFORMANCE METRICS                           │
│  - Total profit      - Win rate          - Sharpe ratio        │
│  - Profit factor     - Max drawdown      - Trade count          │
└─────────────────────────────────────────────────────────────────┘
```

### Module Dependencies

```
main.py
├── src.data.loader              (loads CSV)
├── src.data.splitter            (filters 2025, splits train/test)
├── src.indicators.scalping      (RSI, EMA, Volume for 1min)
├── src.indicators.day_trading   (MACD, VWAP, ATR for 15min)
├── src.indicators.intraday      (Supertrend, ADX, Stochastic)
├── src.signals.base_signals     (generates BUY/SELL/HOLD)
├── src.signals.ml_filter       (Random Forest enhancement)
├── src.backtest.engine          (simulates trades)
├── src.backtest.metrics         (calculates performance)
└── src.dashboard.report         (comparison, error analysis)
```

---

## 3. Data Pipeline

### 3.1 Data Loader (`src/data/loader.py`)

**Purpose:** Load CSV files and normalize column names to Title Case.

**Function: `load_data(filepath: str) -> pd.DataFrame`**

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| filepath | str | Path to CSV file |

**Returns:** DataFrame with normalized columns (Open, High, Low, Close, Volume, Date, Time)

**How it works:**
1. Read CSV with pandas
2. Strip whitespace from column names
3. Normalize column names to Title Case (open → Open)
4. Return clean DataFrame

**Example:**
```python
df = load_data('1min.csv')
print(df.columns)  # ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
```

**Source Data Formats:**

| File | Columns | Format |
|------|---------|--------|
| 1min.csv | Date, Time, Inc Vol, Volume, Open, High, Low, Close | YYYY-MM-DD, HH:MM:SS |
| NQ_15min_processed.csv | timestamps, open, high, low, close, volume | YYYY-MM-DD HH:MM:SS |

---

### 3.2 Data Splitter (`src/data/splitter.py`)

**Function: `filter_2025(df: pd.DataFrame) -> pd.DataFrame`**

**Purpose:** Filter DataFrame to only include 2025 data (Jan 1 - Sep 30).

**Logic:**
1. Check if 'Date' or 'timestamps' column exists
2. Convert to datetime
3. Filter rows where date >= 2025-01-01 AND date <= 2025-09-30
4. Return filtered DataFrame

---

**Function: `split_train_test(df: pd.DataFrame, split_date: str = '2025-06-30') -> tuple`**

**Purpose:** Split data into training and test sets.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| df | pd.DataFrame | - | Data with Date column |
| split_date | str | '2025-06-30' | Date to split on |

**Logic:**
1. Convert split_date to Timestamp
2. Train = rows where Date <= split_date (Jan-Jun 2025)
3. Test = rows where Date > split_date (Jul-Sep 2025)
4. Return (train_df, test_df)

**Returns:** Tuple of (train_df, test_df)

---

### 3.3 Data Resampler (`src/data/resampler.py`)

**Function: `resample_to_timeframe(df: pd.DataFrame, timeframe: str) -> pd.DataFrame`**

**Purpose:** Resample 1-minute data to longer timeframes.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| df | pd.DataFrame | Data with Date/Time columns |
| timeframe | str | Target timeframe ('5min', '15min', '1h', '4h', '1d') |

**OHLCV Aggregation:**
| Column | Aggregation |
|--------|------------|
| Open | first |
| High | max |
| Low | min |
| Close | last |
| Volume | sum |

**Example:**
```python
df_1min = load_data('1min.csv')
df_5min = resample_to_timeframe(df_1min, '5min')
df_15min = resample_to_timeframe(df_1min, '15min')
```

---

## 4. Indicators Module

### 4.1 Scalping Indicators (`src/indicators/scalping.py`)

**Used for:** 1-minute scalping strategy

**Timeframe:** 1 minute candles

#### RSI (Relative Strength Index)

**Function:** `calculate_rsi(df: pd.DataFrame, period: int = 7) -> pd.DataFrame`

**Purpose:** Measure momentum - if price moved up or down more than usual.

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| period | 7 | Number of periods for calculation |

**Calculation:**
```
gain = Close - Close[1]  (if positive, else 0)
loss = Close[1] - Close   (if positive, else 0)
avg_gain = SMA(gain, 7)
avg_loss = SMA(loss, 7)
RS = avg_gain / avg_loss
RSI = 100 - (100 / (1 + RS))
```

**Output column:** `rsi_7`

**Signal interpretation:**
| Value | Meaning |
|-------|---------|
| < 30 | Oversold (potential buy) |
| > 70 | Overbought (potential sell) |
| 30-70 | Neutral |

---

#### EMA (Exponential Moving Average)

**Function:** `calculate_ema(df: pd.DataFrame, periods: list = [5, 20]) -> pd.DataFrame`

**Purpose:** Show the "average" price with more weight on recent data.

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| periods | [5, 20] | EMA periods to calculate |

**Calculation:**
```
k = 2 / (period + 1)
EMA = Close * k + EMA[1] * (1 - k)
```

**Output columns:** `ema_5`, `ema_20`

**Signal interpretation:**
| Condition | Signal |
|-----------|--------|
| Close > EMA5 | Short-term bullish |
| Close < EMA5 | Short-term bearish |
| EMA5 > EMA20 | Uptrend |
| EMA5 < EMA20 | Downtrend |

---

#### Volume Spike Detection

**Function:** `calculate_volume_spike(df: pd.DataFrame, threshold: float = 2.0) -> pd.DataFrame`

**Purpose:** Detect unusually high trading volume.

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| threshold | 2.0 | Multiplier of 20-period average |

**Calculation:**
```
volume_ma = SMA(Volume, 20)
volume_spike = Volume > (volume_ma * 2.0)
```

**Output columns:** `volume_ma`, `volume_spike` (True/False)

**Signal interpretation:**
- `volume_spike = True` → High activity, confirmation signal

---

### 4.2 Day Trading Indicators (`src/indicators/day_trading.py`)

**Used for:** 15-minute day trading strategy

**Timeframe:** 15 minute candles

#### MACD (Moving Average Convergence Divergence)

**Function:** `calculate_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame`

**Purpose:** Show when a trend is changing direction.

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| fast | 12 | Fast EMA period |
| slow | 26 | Slow EMA period |
| signal | 9 | Signal line period |

**Calculation:**
```
fast_ema = EMA(Close, 12)
slow_ema = EMA(Close, 26)
macd = fast_ema - slow_ema
macd_signal = EMA(macd, 9)
macd_hist = macd - macd_signal
```

**Output columns:** `macd`, `macd_signal`, `macd_hist`

**Signal interpretation:**
| Condition | Signal |
|-----------|--------|
| MACD > Signal | Bullish |
| MACD < Signal | Bearish |
| MACD crosses above | Buy signal |
| MACD crosses below | Sell signal |
| Histogram positive | Momentum up |
| Histogram negative | Momentum down |

---

#### VWAP (Volume Weighted Average Price)

**Function:** `calculate_vwap(df: pd.DataFrame) -> pd.DataFrame`

**Purpose:** Show the average price weighted by volume.

**Calculation:**
```
typical_price = (High + Low + Close) / 3
vwap = cumulative(typical_price * Volume) / cumulative(Volume)
```

**Output column:** `vwap`

**Signal interpretation:**
| Condition | Signal |
|-----------|--------|
| Price > VWAP | Bullish |
| Price < VWAP | Bearish |

---

#### ATR (Average True Range)

**Function:** `calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame`

**Purpose:** Measure volatility - how much the price moves.

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| period | 14 | Number of periods |

**Calculation:**
```
tr1 = High - Low
tr2 = abs(High - Close[1])
tr3 = abs(Low - Close[1])
true_range = max(tr1, tr2, tr3)
atr = SMA(true_range, 14)
```

**Output column:** `atr`

**Usage:** Used for stop loss and take profit sizing.

---

### 4.3 Intraday Indicators (`src/indicators/intraday.py`)

**Used for:** 15-minute intraday/swing strategy

**Timeframe:** 15 minute candles

#### Supertrend

**Function:** `calculate_supertrend(df: pd.DataFrame, period: int = 10, multiplier: float = 3.0) -> pd.DataFrame`

**Purpose:** Identify trend direction with dynamic support/resistance.

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| period | 10 | ATR period |
| multiplier | 3.0 | ATR multiplier for bands |

**Calculation:**
```
hl2 = (High + Low) / 2
atr = ATR(period)
upper_band = hl2 + (multiplier * atr)
lower_band = hl2 - (multiplier * atr)
supertrend_direction:
  - If Close > upper_band → 1 (uptrend)
  - If Close < lower_band → -1 (downtrend)
  - Otherwise → keep previous direction
```

**Output columns:** `supertrend`, `supertrend_direction` (1, -1, or 0)

**Signal interpretation:**
| Direction | Meaning |
|-----------|---------|
| 1 | Bullish trend |
| -1 | Bearish trend |
| 0 | No trend |

---

#### ADX (Average Directional Index)

**Function:** `calculate_adx(df: pd.DataFrame, period: int = 14) -> pd.DataFrame`

**Purpose:** Measure trend strength (not direction).

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| period | 14 | Number of periods |

**Output columns:** `adx`, `adx_plus` (DI+), `adx_minus` (DI-)

**Signal interpretation:**
| ADX Value | Trend Strength |
|-----------|----------------|
| < 20 | Weak/None |
| 20-25 | Weak |
| 25-50 | Strong |
| 50-75 | Very Strong |
| > 75 | Extremely Strong |

**Rule:** Only trade when ADX > 25 (strong trend)

---

#### Stochastic Oscillator

**Function:** `calculate_stochastic(df: pd.DataFrame, k: int = 14, d: int = 3) -> pd.DataFrame`

**Purpose:** Show where the close is relative to the range.

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| k | 14 | %K period |
| d | 3 | %D period |

**Calculation:**
```
lowest_low = min(Low, k periods)
highest_high = max(High, k periods)
stoch_k = 100 * (Close - lowest_low) / (highest_high - lowest_low)
stoch_d = SMA(stoch_k, d)
```

**Output columns:** `stoch_k`, `stoch_d`

**Signal interpretation:**
| Value | Meaning |
|-------|---------|
| < 20 | Oversold (potential buy) |
| > 80 | Overbought (potential sell) |

---

## 5. Signals Module

### 5.1 Base Signal Generation (`src/signals/base_signals.py`)

**Purpose:** Convert indicator values into BUY (1), SELL (-1), or HOLD (0) signals.

---

#### Scalping Signals

**Function:** `generate_scalping_signals(df: pd.DataFrame) -> pd.DataFrame`

**Entry Rules (Long):**
```python
long_condition = (
    df['Close'] > df['ema_5'] AND      # Price above fast EMA
    df['rsi_7'] < 30 AND              # RSI oversold
    df['volume_spike'] == True         # Volume confirmation
)
```

**Entry Rules (Short):**
```python
short_condition = (
    df['Close'] < df['ema_5'] AND      # Price below fast EMA
    df['rsi_7'] > 70 AND              # RSI overbought
    df['volume_spike'] == True         # Volume confirmation
)
```

**Output:** `signal` column (1, -1, or 0)

---

#### Day Trading Signals

**Function:** `generate_day_trading_signals(df: pd.DataFrame) -> pd.DataFrame`

**Entry Rules (Long):**
```python
long_condition = (
    df['macd'] > df['macd_signal'] AND  # MACD bullish crossover
    df['rsi'] < 70 AND                 # Not overbought
    df['Close'] > df['vwap']           # Above VWAP
)
```

**Entry Rules (Short):**
```python
short_condition = (
    df['macd'] < df['macd_signal'] AND  # MACD bearish crossover
    df['rsi'] > 30 AND                 # Not oversold
    df['Close'] < df['vwap']           # Below VWAP
)
```

**Output:** `signal` column (1, -1, or 0)

---

#### Intraday Signals

**Function:** `generate_intraday_signals(df: pd.DataFrame) -> pd.DataFrame`

**Entry Rules (Long):**
```python
long_condition = (
    df['supertrend_direction'] == 1 AND   # Supertrend bullish
    df['adx'] > 25 AND                     # Strong trend
    df['stoch_k'] < 20                     # Stochastic oversold
)
```

**Entry Rules (Short):**
```python
short_condition = (
    df['supertrend_direction'] == -1 AND   # Supertrend bearish
    df['adx'] > 25 AND                     # Strong trend
    df['stoch_k'] > 80                     # Stochastic overbought
)
```

**Output:** `signal` column (1, -1, or 0)

---

## 6. ML Filter

### 6.1 ML Signal Enhancement (`src/signals/ml_filter.py`)

**Purpose:** Use machine learning to filter out bad signals.

**Algorithm:** Random Forest Classifier

---

#### Feature Engineering

**Function:** `add_ml_features(df: pd.DataFrame) -> pd.DataFrame`

**Features created:**
| Feature | Description | Formula |
|---------|-------------|---------|
| `price_change` | 1-period return | Close.pct_change() |
| `price_change_5` | 5-period return | Close.pct_change(5) |
| `volume_change` | Volume momentum | Volume.pct_change() |
| `volume_ma_ratio` | Volume vs average | Volume / Volume.rolling(20).mean() |
| `next_direction` | Target variable | 1 if next_close > current_close, else 0 |

**Optional features (if available):**
- `rsi_7`
- `macd`
- `macd_hist`
- `adx`
- `supertrend`

---

#### Model Training

**Function:** `train_ml_filter(df: pd.DataFrame, n_estimators: int = 100, max_depth: int = 10) -> dict`

**Purpose:** Train Random Forest to predict next candle direction.

**Parameters:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| n_estimators | 100 | Number of trees |
| max_depth | 10 | Maximum tree depth |

**Training data:** Cleaned DataFrame (no NaN values)

**Output:** dict with `model` and `feature_cols`

---

#### Signal Filtering

**Function:** `apply_ml_filter(df: pd.DataFrame, ml_data: dict) -> pd.DataFrame`

**Purpose:** Remove signals that ML predicts will fail.

**Logic:**
```python
for each signal != 0:
    features = row[feature_cols]
    prediction = model.predict(features)
    
    if prediction == 0 AND signal == 1:   # ML says price will go down
        ml_signal = 0                   # Remove buy signal
    
    if prediction == 1 AND signal == -1:  # ML says price will go up
        ml_signal = 0                     # Remove sell signal
```

**Output:** `ml_signal` column (filtered version of `signal`)

---

## 7. Backtest Engine

### 7.1 Trade Simulation (`src/backtest/engine.py`)

**Function:** `run_backtest(df: pd.DataFrame, initial_capital: float = 10000, stop_loss: float = 1.0, take_profit: float = 1.5, max_daily_trades: int = 10) -> Tuple[List[Dict], float]`

**Purpose:** Simulate trading with realistic entry/exit logic.

---

#### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| initial_capital | 10000 | Starting capital |
| stop_loss | 1.0 | Stop loss % (0.5 = 0.5%) |
| take_profit | 1.5 | Take profit % (1.5 = 1.5%) |
| max_daily_trades | 10 | Maximum trades per day |

---

#### Trade Logic

**Entry:**
```python
if position is None AND signal != 0 AND daily_trades < max_daily_trades:
    position = signal          # 1 = long, -1 = short
    entry_price = Close
    daily_trades += 1
```

**Exit (Long):**
```python
if position == 1:
    price_change = (current_price - entry_price) / entry_price * 100
    
    if price_change <= -stop_loss:       # -0.5% or worse
        EXIT with loss
    if price_change >= take_profit:      # +1.5% or more
        EXIT with profit
```

**Exit (Short):**
```python
if position == -1:
    price_change = -(current_price - entry_price) / entry_price * 100
    
    if price_change <= -stop_loss:       # -0.5% or worse
        EXIT with loss
    if price_change >= take_profit:       # +1.5% or more
        EXIT with profit
```

---

#### Trade Record Format

```python
{
    'entry_idx': 10,           # Candle index of entry
    'exit_idx': 20,             # Candle index of exit
    'entry_price': 24746.75,    # Entry price
    'exit_price': 24885.00,     # Exit price
    'direction': 'LONG',       # 'LONG' or 'SHORT'
    'profit_pct': -0.56,       # Percentage gain/loss
    'profit_dollars': -55.87,  # Dollar gain/loss
    'capital_after': 9944.13,  # Capital after trade
    'exit_reason': 'STOP LOSS' # 'STOP LOSS' or 'TAKE PROFIT'
}
```

---

## 8. Performance Metrics

### 8.1 Metrics Calculation (`src/backtest/metrics.py`)

**Function:** `calculate_metrics(trades: List[Dict], initial_capital: float = 10000) -> Dict`

---

#### Metrics Calculated

| Metric | Formula | Target |
|--------|---------|--------|
| `total_profit` | sum(profit_dollars) | > 0 |
| `profit_factor` | gross_profit / gross_loss | > 1.5 |
| `win_rate` | winning_trades / total_trades * 100 | > 50% |
| `sharpe_ratio` | mean(returns) / std(returns) | > 1.0 |
| `max_drawdown` | max(peak - capital) / peak * 100 | < 10% |
| `total_trades` | count of trades | - |
| `avg_profit` | mean(winning_trades) | - |
| `avg_loss` | mean(losing_trades) | - |
| `final_capital` | last trade capital_after | - |

---

#### Profit Factor Calculation

```python
gross_profit = sum(profit_dollars for trades where profit > 0)
gross_loss = abs(sum(profit_dollars for trades where profit <= 0))
profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
```

**Interpretation:**
| PF Value | Meaning |
|---------|---------|
| < 1.0 | Losing system |
| 1.0 - 1.5 | Marginal |
| 1.5 - 2.0 | Good |
| > 2.0 | Excellent |

---

#### Max Drawdown Calculation

```python
capital_curve = [initial_capital] + [t['capital_after'] for t in trades]
peak = initial_capital
max_dd = 0

for capital in capital_curve:
    if capital > peak:
        peak = capital
    dd = (peak - capital) / peak * 100
    if dd > max_dd:
        max_dd = dd
```

---

## 9. Dashboard & Reports

### 9.1 Report Generation (`src/dashboard/report.py`)

#### Strategy Comparison

**Function:** `generate_comparison_report(results: Dict[str, Dict]) -> Dict`

**Purpose:** Compare all strategies and find the best.

**Output:**
```python
{
    'best_strategy': 'scalping',
    'best_profit': 107.66,
    'all_results': {...},
    'recommendation': 'Use scalping strategy for production trading.',
    'confidence': 'Low'  # or 'Medium' or 'High'
}
```

**Confidence Calculation:**
```python
advantage = (best_profit - avg_other_profits) / avg_other_profits * 100

if advantage > 50: confidence = 'High'
elif advantage > 20: confidence = 'Medium'
else: confidence = 'Low'
```

---

#### Error Analysis

**Function:** `generate_error_analysis(trades: List[Dict]) -> Dict`

**Output:**
```python
{
    'error_rate': 70.6,        # % of losing trades
    'total_trades': 17,
    'losing_trades': 12,
    'avg_loss': 54.22,
    'analysis': '70.6% of trades resulted in loss'
}
```

---

## 10. Strategies

### 10.1 Scalping Strategy

| Parameter | Value |
|-----------|-------|
| Timeframe | 1 minute |
| Indicators | RSI(7), EMA(5,20), Volume spike |
| Stop Loss | 0.5% |
| Take Profit | 1.5% |
| Max Daily Trades | 10 |
| Signal Requirements | All 3 conditions must match |

**Pros:**
- Quick trades, fast feedback
- Lower exposure to overnight risk
- Can capture small price movements

**Cons:**
- High transaction costs
- Requires precise timing
- More affected by spread

---

### 10.2 Day Trading Strategy

| Parameter | Value |
|-----------|-------|
| Timeframe | 15 minute |
| Indicators | MACD(12,26,9), RSI(14), VWAP, ATR(14) |
| Stop Loss | 1.0% |
| Take Profit | 2.0% |
| Max Daily Trades | 5 |
| Signal Requirements | MACD cross + RSI + VWAP |

**Pros:**
- Clearer signals than scalping
- Less noise than 1min charts
- Can hold positions for hours

**Cons:**
- Requires more patience
- Overnight risk (if holding)
- MACD can be slow

---

### 10.3 Intraday/Swing Strategy

| Parameter | Value |
|-----------|-------|
| Timeframe | 15 minute |
| Indicators | Supertrend(10,3), ADX(14), Stochastic(14,3) |
| Stop Loss | 1.0% |
| Take Profit | 2.0% |
| Max Daily Trades | 3 |
| Signal Requirements | Supertrend + ADX > 25 + Stochastic |

**Pros:**
- Catches larger trends
- Clear entry points
- Good risk:reward

**Cons:**
- Fewer signals
- ADX threshold too strict
- May miss choppy markets

---

## 11. Demo Results

### Test Period: July - September 2025

### Scalping (Best)

| Metric | Value |
|--------|-------|
| Initial Capital | $10,000.00 |
| Final Capital | $10,107.66 |
| Total Profit | +$107.66 (1.08%) |
| Total Trades | 17 |
| Winning Trades | 5 (29.4%) |
| Losing Trades | 12 (70.6%) |
| Profit Factor | 1.17 |
| Sharpe Ratio | 0.07 |
| Max Drawdown | 2.6% |
| Avg Win | $149.24 |
| Avg Loss | -$54.22 |

### Why Low Win Rate But Profitable?

- Winners: +1.5% to +1.56% (avg $149.24)
- Losers: -0.5% to -0.74% (avg -$54.22)
- Risk:Reward ratio: 3:1
- Even with 29% win rate, profit factor > 1.0

---

## 12. Setup & Usage

### Installation

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
pandas
numpy
scikit-learn
plotly
pytest
```

### Running the Demo

```bash
# Full simulation with console output + HTML dashboards
python3 live_dashboard.py

# Basic strategy comparison
python3 main.py
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific module
pytest tests/test_indicators.py -v

# Single test
pytest tests/test_indicators.py::test_calculate_rsi -v
```

---

## 13. File Reference

### Source Files

| File | Lines | Purpose |
|------|-------|---------|
| `src/data/loader.py` | 26 | CSV loading |
| `src/data/splitter.py` | 35 | 2025 filter, train/test split |
| `src/data/resampler.py` | 50 | Timeframe resampling |
| `src/indicators/scalping.py` | 38 | RSI, EMA, Volume |
| `src/indicators/day_trading.py` | 44 | MACD, VWAP, ATR |
| `src/indicators/intraday.py` | 70 | Supertrend, ADX, Stochastic |
| `src/signals/base_signals.py` | 68 | Signal generation |
| `src/signals/ml_filter.py` | 100 | ML filtering |
| `src/backtest/engine.py` | 90 | Trade simulation |
| `src/backtest/metrics.py` | 80 | Performance metrics |
| `src/dashboard/visualizer.py` | 60 | Chart generation |
| `src/dashboard/report.py` | 120 | Reports |
| `main.py` | 234 | Main execution |
| `live_dashboard.py` | 180 | Demo script |

### Test Files

| File | Tests | Coverage |
|------|-------|----------|
| `tests/test_data_loader.py` | 6 | Data loading, filtering, resampling |
| `tests/test_indicators.py` | 12 | All indicators |
| `tests/test_signals.py` | 4 | Signal generation, ML filter |
| `tests/test_backtest.py` | 3 | Backtest, metrics |
| `tests/test_dashboard.py` | 4 | Reports, visualization |

**Total: 29 tests**

---

## 14. Glossary

| Term | Definition |
|------|------------|
| **Candle** | A single time period showing OHLCV data |
| **Long** | Buying (expect price to go up) |
| **Short** | Selling (expect price to go down) |
| **Stop Loss** | Exit point to limit losses |
| **Take Profit** | Exit point to lock gains |
| **Drawdown** | Peak-to-trough decline |
| **Profit Factor** | Gross profit / Gross loss |
| **Sharpe Ratio** | Risk-adjusted return measure |
| **Win Rate** | % of profitable trades |
| **RSI** | Relative Strength Index (momentum) |
| **EMA** | Exponential Moving Average |
| **MACD** | Moving Average Convergence Divergence |
| **VWAP** | Volume Weighted Average Price |
| **ATR** | Average True Range (volatility) |
| **ADX** | Average Directional Index (trend strength) |
| **Scalping** | Very short-term trading (1-5 min) |
| **Day Trading** | Intraday trading (15min-1hr) |
| **Intraday/Swing** | Multi-hour trading |

---

**Document Version:** 1.0  
**Last Updated:** 2025-05-13  
**Repository:** [GitHub](https://github.com/molhamfetnah/trading-strategy-finder)