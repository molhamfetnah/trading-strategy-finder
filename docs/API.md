# API Documentation

## Trading Strategy Finder - Code Reference

---

## Table of Contents
1. [Data Module](#data-module)
2. [Indicators Module](#indicators-module)
3. [Signals Module](#signals-module)
4. [Backtest Module](#backtest-module)
5. [Dashboard Module](#dashboard-module)

---

## Data Module

### `src/data/loader.py`

```python
from src.data.loader import load_data

def load_data(filepath: str) -> pd.DataFrame
```

**Description:** Load CSV data and normalize column names to Title Case.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| filepath | str | Path to CSV file |

**Returns:** DataFrame with normalized columns (Open, High, Low, Close, Volume, Date, Time, etc.)

**Raises:** FileNotFoundError, Exception

**Example:**
```python
df = load_data('1min.csv')
print(df.columns)  # ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
```

---

### `src/data/splitter.py`

```python
from src.data.splitter import filter_2025, split_train_test

def filter_2025(df: pd.DataFrame) -> pd.DataFrame
def split_train_test(df: pd.DataFrame, split_date: str = '2025-06-30') -> tuple
```

**filter_2025:** Filter DataFrame to 2025 data only (Jan 1 - Sep 30).

**split_train_test:** Split data into training and test sets.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| df | pd.DataFrame | Data with Date/timestamps column |
| split_date | str | Split date (YYYY-MM-DD) |

**Returns:** Tuple of (train_df, test_df)

**Example:**
```python
df = load_data('1min.csv')
df_2025 = filter_2025(df)
train, test = split_train_test(df_2025, '2025-06-30')
# Train: Jan 1 - Jun 30, 2025
# Test: Jul 1 - Sep 30, 2025
```

---

### `src/data/resampler.py`

```python
from src.data.resampler import resample_to_timeframe

def resample_to_timeframe(df: pd.DataFrame, timeframe: str) -> pd.DataFrame
```

**Description:** Resample 1-minute data to different timeframes.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| df | pd.DataFrame | 1-minute data with Date/Time columns |
| timeframe | str | Target timeframe ('5min', '15min', '1h', '4h', '1d') |

**Returns:** Resampled DataFrame with OHLCV data

**Example:**
```python
df = load_data('1min.csv')
df_5min = resample_to_timeframe(df, '5min')
df_15min = resample_to_timeframe(df, '15min')
```

---

## Indicators Module

### Scalping Indicators (`src/indicators/scalping.py`)

```python
from src.indicators.scalping import (
    calculate_rsi,
    calculate_ema,
    calculate_volume_spike,
    calculate_scalping_indicators
)
```

| Function | Description |
|----------|-------------|
| `calculate_rsi(df, period=7)` | Calculate RSI with given period |
| `calculate_ema(df, periods=[5,20])` | Calculate EMA for given periods |
| `calculate_volume_spike(df, threshold=2.0)` | Detect volume spikes (2x MA) |
| `calculate_scalping_indicators(df)` | Calculate all scalping indicators |

**Output Columns:** rsi_7, ema_5, ema_20, volume_ma, volume_spike

**Example:**
```python
df = calculate_scalping_indicators(df)
print(df[['Close', 'rsi_7', 'ema_5', 'volume_spike']].tail())
```

---

### Day Trading Indicators (`src/indicators/day_trading.py`)

```python
from src.indicators.day_trading import (
    calculate_macd,
    calculate_vwap,
    calculate_atr,
    calculate_day_trading_indicators
)
```

| Function | Description |
|----------|-------------|
| `calculate_macd(df, fast=12, slow=26, signal=9)` | MACD with histogram |
| `calculate_vwap(df)` | Volume Weighted Average Price |
| `calculate_atr(df, period=14)` | Average True Range |
| `calculate_day_trading_indicators(df)` | Calculate all day trading indicators |

**Output Columns:** macd, macd_signal, macd_hist, vwap, atr

**Example:**
```python
df = calculate_day_trading_indicators(df)
print(df[['Close', 'macd', 'vwap', 'atr']].tail())
```

---

### Intraday Indicators (`src/indicators/intraday.py`)

```python
from src.indicators.intraday import (
    calculate_supertrend,
    calculate_adx,
    calculate_stochastic,
    calculate_intraday_indicators
)
```

| Function | Description |
|----------|-------------|
| `calculate_supertrend(df, period=10, multiplier=3.0)` | Supertrend with direction |
| `calculate_adx(df, period=14)` | Average Directional Index |
| `calculate_stochastic(df, k=14, d=3)` | Stochastic oscillator |
| `calculate_intraday_indicators(df)` | Calculate all intraday indicators |

**Output Columns:** supertrend, supertrend_direction, adx, adx_plus, adx_minus, stoch_k, stoch_d

**Example:**
```python
df = calculate_intraday_indicators(df)
print(df[['Close', 'supertrend_direction', 'adx', 'stoch_k']].tail())
```

---

## Signals Module

### Base Signals (`src/signals/base_signals.py`)

```python
from src.signals.base_signals import (
    generate_scalping_signals,
    generate_day_trading_signals,
    generate_intraday_signals
)
```

**Signal Values:** 0 (no signal), 1 (long), -1 (short)

| Function | Strategy | Entry Conditions |
|----------|----------|-----------------|
| `generate_scalping_signals(df)` | Scalping | Price + RSI + Volume |
| `generate_day_trading_signals(df)` | Day Trading | MACD + RSI + VWAP |
| `generate_intraday_signals(df)` | Intraday | Supertrend + ADX + Stoch |

**Example:**
```python
df = calculate_scalping_indicators(df)
df = generate_scalping_signals(df)
signals = df[df['signal'] != 0]
print(f"Generated {len(signals)} signals")
```

---

### ML Filter (`src/signals/ml_filter.py`)

```python
from src.signals.ml_filter import (
    add_ml_features,
    train_ml_filter,
    apply_ml_filter
)

def train_ml_filter(df, n_estimators=100, max_depth=10) -> dict
def apply_ml_filter(df, ml_data) -> pd.DataFrame
```

**train_ml_filter:** Train Random Forest classifier on historical data.

**apply_ml_filter:** Apply ML filter to remove conflicting signals.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| df | pd.DataFrame | Data with features and signals |
| ml_data | dict | Trained model with feature columns |
| n_estimators | int | Number of trees (default 100) |
| max_depth | int | Maximum tree depth (default 10) |

**Returns:** ml_data dict with 'model' and 'feature_cols' keys

**Example:**
```python
# Train on historical data
train_data = add_ml_features(train_df)
ml_data = train_ml_filter(train_data)

# Apply to new data
df = apply_ml_filter(test_df, ml_data)
# New column: ml_signal (filtered version of signal)
```

---

## Backtest Module

### Engine (`src/backtest/engine.py`)

```python
from src.backtest.engine import run_backtest

def run_backtest(
    df,
    initial_capital=10000,
    stop_loss=1.0,
    take_profit=1.5,
    max_daily_trades=10
) -> Tuple[List[Dict], float]
```

**Description:** Simulate trading with entry/exit signals.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| df | pd.DataFrame | - | Data with Close and signal/ml_signal |
| initial_capital | float | 10000 | Starting capital |
| stop_loss | float | 1.0 | Stop loss % (0.5 = 0.5%) |
| take_profit | float | 1.5 | Take profit % (1.5 = 1.5%) |
| max_daily_trades | int | 10 | Max trades per day |

**Returns:** Tuple of (trades_list, final_capital)

**Trade Dict:**
```python
{
    'entry_idx': int,
    'exit_idx': int,
    'entry_price': float,
    'exit_price': float,
    'direction': 'long' or 'short',
    'profit_pct': float,
    'profit_dollars': float,
    'capital_after': float
}
```

**Example:**
```python
trades, final_capital = run_backtest(
    df,
    initial_capital=10000,
    stop_loss=0.5,
    take_profit=1.5
)
print(f"Final capital: ${final_capital:.2f}")
print(f"Total trades: {len(trades)}")
```

---

### Metrics (`src/backtest/metrics.py`)

```python
from src.backtest.metrics import calculate_metrics

def calculate_metrics(trades: List[Dict], initial_capital: float = 10000) -> Dict
```

**Description:** Calculate comprehensive performance metrics.

**Returns:**
```python
{
    'total_profit': float,      # Net profit/loss
    'profit_factor': float,     # Gross profit / Gross loss
    'win_rate': float,          # % of winning trades
    'sharpe_ratio': float,      # Risk-adjusted return
    'max_drawdown': float,      # Maximum drawdown %
    'total_trades': int,        # Total number of trades
    'avg_profit': float,        # Average winning trade
    'avg_loss': float,          # Average losing trade
    'final_capital': float      # Final account balance
}
```

**Example:**
```python
metrics = calculate_metrics(trades, 10000)
print(f"Profit: ${metrics['total_profit']:.2f}")
print(f"Win Rate: {metrics['win_rate']:.1f}%")
print(f"Sharpe: {metrics['sharpe_ratio']:.2f}")
```

---

## Dashboard Module

### Report (`src/dashboard/report.py`)

```python
from src.dashboard.report import (
    generate_comparison_report,
    generate_error_analysis,
    format_metrics_for_display
)
```

**generate_comparison_report:** Compare all strategies and find best.

**generate_error_analysis:** Analyze losing trades and error rate.

**format_metrics_for_display:** Format metrics for human-readable output.

**Example:**
```python
results = {
    'scalping': metrics_scalping,
    'day_trading': metrics_day,
    'intraday': metrics_intra
}

report = generate_comparison_report(results)
print(f"Best: {report['best_strategy']}")
print(f"Confidence: {report['confidence']}")

error = generate_error_analysis(trades)
print(f"Error Rate: {error['error_rate']:.1f}%")
```

---

### Visualizer (`src/dashboard/visualizer.py`)

```python
from src.dashboard.visualizer import (
    create_trade_chart,
    create_equity_curve,
    calculate_trade_statistics
)
```

**create_trade_chart:** Generate chart data with trade markers.

**create_equity_curve:** Create equity curve from trade history.

**calculate_trade_statistics:** Calculate detailed trade statistics.

**Example:**
```python
chart = create_trade_chart(df, trades, 'scalping')
equity = create_equity_curve(trades, 10000)
stats = calculate_trade_statistics(trades)
```

---

## Usage Example

Complete pipeline from data loading to results:

```python
from src.data.loader import load_data
from src.data.splitter import filter_2025, split_train_test
from src.indicators.scalping import calculate_scalping_indicators
from src.signals.base_signals import generate_scalping_signals
from src.signals.ml_filter import train_ml_filter, apply_ml_filter, add_ml_features
from src.backtest.engine import run_backtest
from src.backtest.metrics import calculate_metrics
from src.dashboard.report import generate_comparison_report

# Load and prepare data
df = load_data('1min.csv')
df_2025 = filter_2025(df)
train, test = split_train_test(df_2025, '2025-06-30')

# Calculate indicators
train = calculate_scalping_indicators(train)
test = calculate_scalping_indicators(test)

# Generate signals
train = generate_scalping_signals(train)
test = generate_scalping_signals(test)

# Train ML filter
train = add_ml_features(train)
ml_data = train_ml_filter(train)

# Apply ML filter
test = apply_ml_filter(test, ml_data)

# Run backtest
trades, capital = run_backtest(test, stop_loss=0.5, take_profit=1.5)

# Calculate metrics
metrics = calculate_metrics(trades, 10000)

# Print results
print(f"Profit: ${metrics['total_profit']:.2f}")
print(f"Win Rate: {metrics['win_rate']:.1f}%")
```

---

## Error Handling

All modules include error handling:

```python
try:
    df = load_data('data.csv')
except FileNotFoundError:
    print("Data file not found")
except Exception as e:
    print(f"Error: {e}")
```

---

## Constants Reference

| Constant | Value | Usage |
|----------|-------|-------|
| RSI_OVERSOLD | 30 | Scalping long signal |
| RSI_OVERBOUGHT | 70 | Scalping short signal |
| EMA_FAST | 5 | Fast EMA period |
| EMA_SLOW | 20 | Slow EMA period |
| VOLUME_THRESHOLD | 2.0 | Volume spike multiplier |
| MACD_FAST | 12 | MACD fast period |
| MACD_SLOW | 26 | MACD slow period |
| MACD_SIGNAL | 9 | MACD signal period |
| ATR_PERIOD | 14 | ATR calculation period |
| ADX_THRESHOLD | 25 | Trend strength threshold |
| STOCH_K | 14 | Stochastic %K period |
| STOCH_D | 3 | Stochastic %D period |

---

*Document Version: 1.0 | Generated: 2025-05-13*