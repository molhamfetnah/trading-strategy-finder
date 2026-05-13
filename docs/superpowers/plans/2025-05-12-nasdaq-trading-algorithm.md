# NASDAQ Trading Algorithm Finder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a hybrid trading algorithm that compares scalping, day trading, and intraday strategies to find the most profitable approach for NASDAQ futures.

**Architecture:** Hybrid approach combining classical technical indicators (RSI, MACD, EMA, Supertrend) as base signals with ML classifiers (Random Forest) to filter/enhance trading signals. Backtest using 2025 data (train: Jan-Jun, test: Jul-Sep).

**Tech Stack:** Python 3.10+, pandas, numpy, pandas-ta, scikit-learn, matplotlib, plotly

---

## File Structure

```
trading/
├── src/
│   ├── data/
│   │   ├── loader.py          # Load and clean CSV files
│   │   ├── splitter.py        # Split into train/test (2025)
│   │   └── resampler.py       # Resample to different timeframes
│   ├── indicators/
│   │   ├── scalping.py        # RSI, EMA, Volume indicators
│   │   ├── day_trading.py     # MACD, VWAP, ATR indicators
│   │   └── intraday.py        # Supertrend, ADX, Stochastic
│   ├── signals/
│   │   ├── base_signals.py    # Generate indicator-based signals
│   │   └── ml_filter.py       # ML classifier for signal filtering
│   ├── backtest/
│   │   ├── engine.py          # Trade simulation engine
│   │   └── metrics.py         # Calculate performance metrics
│   └── dashboard/
│       ├── visualizer.py      # Create trading charts
│       └── report.py          # Generate reports
├── data/
│   ├── 2025_train.csv         # Training data (Jan-Jun 2025)
│   └── 2025_test.csv          # Test data (Jul-Sep 2025)
├── tests/
│   ├── test_data_loader.py
│   ├── test_indicators.py
│   ├── test_signals.py
│   └── test_backtest.py
├── main.py                    # Main execution script
├── requirements.txt           # Dependencies
└── README.md                  # Usage instructions
```

---

## Phase 1: Data Pipeline

### Task 1: Data Loader

**Files:**
- Create: `src/data/loader.py`
- Test: `tests/test_data_loader.py`

- [ ] **Step 1: Write the failing test**

```python
import pandas as pd

def test_load_1min_data():
    df = load_data('1min.csv')
    assert 'Date' in df.columns
    assert 'Open' in df.columns
    assert len(df) > 0

def test_load_15min_data():
    df = load_data('NQ_15min_processed.csv')
    assert 'open' in df.columns
    assert 'high' in df.columns
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_data_loader.py::test_load_1min_data -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
import pandas as pd

def load_data(filepath):
    df = pd.read_csv(filepath)
    return df
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_data_loader.py::test_load_1min_data -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/data/loader.py tests/test_data_loader.py
git commit -m "feat: add data loader module"
```

---

### Task 2: Data Splitter (Filter 2025 Data)

**Files:**
- Modify: `src/data/loader.py`
- Create: `src/data/splitter.py`
- Test: `tests/test_data_loader.py`

- [ ] **Step 1: Write the failing test**

```python
def test_filter_2025_data():
    df = load_data('1min.csv')
    df_2025 = filter_2025(df)
    assert df_2025['Date'].min() >= '2025-01-01'
    assert df_2025['Date'].max() <= '2025-09-30'

def test_split_train_test():
    df = load_data('1min.csv')
    df_2025 = filter_2025(df)
    train, test = split_train_test(df_2025, '2025-06-30')
    assert train['Date'].max() <= '2025-06-30'
    assert test['Date'].min() >= '2025-07-01'
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_data_loader.py::test_filter_2025_data -v`
Expected: FAIL

- [ ] **Step 3: Write implementation**

```python
def filter_2025(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df_2025 = df[(df['Date'] >= '2025-01-01') & (df['Date'] <= '2025-09-30')]
    return df_2025

def split_train_test(df, split_date='2025-06-30'):
    train = df[df['Date'] < split_date]
    test = df[df['Date'] >= split_date]
    return train, test
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_data_loader.py::test_filter_2025_data -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/data/loader.py src/data/splitter.py
git commit -m "feat: add 2025 data filter and train/test split"
```

---

### Task 3: Data Resampler

**Files:**
- Create: `src/data/resampler.py`
- Test: `tests/test_data_loader.py`

- [ ] **Step 1: Write the failing test**

```python
def test_resample_1min_to_5min():
    df = load_data('1min.csv')
    df_2025 = filter_2025(df)
    df_5min = resample_to timeframe(df_2025, '5min')
    assert len(df_5min) < len(df_2025)
    assert 'open' in df_5min.columns

def test_resample_1min_to_15min():
    df = load_data('1min.csv')
    df_2025 = filter_2025(df)
    df_15min = resample_to timeframe(df_2025, '15min')
    assert len(df_15min) < len(df_2025)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_data_loader.py::test_resample_1min_to_5min -v`
Expected: FAIL

- [ ] **Step 3: Write implementation**

```python
def resample_to_timeframe(df, timeframe):
    df = df.copy()
    df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df = df.set_index('datetime')
    
    ohlc = {
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    }
    
    df_resampled = df.resample(timeframe).agg(ohlc).dropna()
    df_resampled = df_resampled.reset_index()
    return df_resampled
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_data_loader.py::test_resample_1min_to_5min -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/data/resampler.py
git commit -m "feat: add data resampler for different timeframes"
```

---

## Phase 2: Indicator Calculation

### Task 4: Scalping Indicators (1min)

**Files:**
- Create: `src/indicators/scalping.py`
- Test: `tests/test_indicators.py`

- [ ] **Step 1: Write the failing test**

```python
def test_calculate_rsi():
    df = load_data('1min.csv')
    df = calculate_rsi(df, period=7)
    assert 'rsi_7' in df.columns

def test_calculate_ema():
    df = load_data('1min.csv')
    df = calculate_ema(df, periods=[5, 20])
    assert 'ema_5' in df.columns
    assert 'ema_20' in df.columns

def test_volume_spike():
    df = load_data('1min.csv')
    df = calculate_volume_spike(df)
    assert 'volume_spike' in df.columns
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_indicators.py::test_calculate_rsi -v`
Expected: FAIL

- [ ] **Step 3: Write implementation**

```python
import pandas_ta as ta

def calculate_rsi(df, period=7):
    df['rsi_7'] = ta.rsi(df['close'], length=period)
    return df

def calculate_ema(df, periods=[5, 20]):
    for period in periods:
        df[f'ema_{period}'] = ta.ema(df['close'], length=period)
    return df

def calculate_volume_spike(df, threshold=2.0):
    df['volume_ma'] = df['volume'].rolling(20).mean()
    df['volume_spike'] = df['volume'] > (df['volume_ma'] * threshold)
    return df

def calculate_scalping_indicators(df):
    df = calculate_rsi(df, 7)
    df = calculate_ema(df, [5, 20])
    df = calculate_volume_spike(df)
    return df
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_indicators.py::test_calculate_rsi -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/indicators/scalping.py
git commit -m "feat: add scalping indicators (RSI, EMA, Volume)"
```

---

### Task 5: Day Trading Indicators (15min)

**Files:**
- Create: `src/indicators/day_trading.py`
- Test: `tests/test_indicators.py`

- [ ] **Step 1: Write the failing test**

```python
def test_calculate_macd():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_macd(df)
    assert 'macd' in df.columns
    assert 'macd_signal' in df.columns

def test_calculate_vwap():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_vwap(df)
    assert 'vwap' in df.columns

def test_calculate_atr():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_atr(df)
    assert 'atr' in df.columns
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_indicators.py::test_calculate_macd -v`
Expected: FAIL

- [ ] **Step 3: Write implementation**

```python
import pandas_ta as ta

def calculate_macd(df, fast=12, slow=26, signal=9):
    df['macd'] = ta.macd(df['close'], fast=fast, slow=slow, signal=signal)['MACD_12_26_9']
    df['macd_signal'] = ta.macd(df['close'], fast=fast, slow=slow, signal=signal)['MACDs_12_26_9']
    df['macd_hist'] = ta.macd(df['close'], fast=fast, slow=slow, signal=signal)['MACDh_12_26_9']
    return df

def calculate_vwap(df):
    df['vwap'] = ta.vwap(df['high'], df['low'], df['close'], df['volume'])
    return df

def calculate_atr(df, period=14):
    df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=period)
    return df

def calculate_day_trading_indicators(df):
    df = calculate_macd(df)
    df = calculate_vwap(df)
    df = calculate_atr(df)
    return df
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_indicators.py::test_calculate_macd -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/indicators/day_trading.py
git commit -m "feat: add day trading indicators (MACD, VWAP, ATR)"
```

---

### Task 6: Intraday/Swing Indicators

**Files:**
- Create: `src/indicators/intraday.py`
- Test: `tests/test_indicators.py`

- [ ] **Step 1: Write the failing test**

```python
def test_calculate_supertrend():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_supertrend(df)
    assert 'supertrend' in df.columns
    assert 'supertrend_direction' in df.columns

def test_calculate_adx():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_adx(df)
    assert 'adx' in df.columns

def test_calculate_stochastic():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_stochastic(df)
    assert 'stoch_k' in df.columns
    assert 'stoch_d' in df.columns
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_indicators.py::test_calculate_supertrend -v`
Expected: FAIL

- [ ] **Step 3: Write implementation**

```python
import pandas_ta as ta

def calculate_supertrend(df, period=10, multiplier=3.0):
    result = ta.supertrend(df['high'], df['low'], df['close'], period=period, multiplier=multiplier)
    df['supertrend'] = result[f'SUPERT_{period}_{multiplier}']
    df['supertrend_direction'] = result[f'SUPERTd_{period}_{multiplier}']
    return df

def calculate_adx(df, period=14):
    result = ta.adx(df['high'], df['low'], df['close'], length=period)
    df['adx'] = result[f'ADX_{period}']
    df['adx_plus'] = result[f'DMP_{period}']
    df['adx_minus'] = result[f'DMN_{period}']
    return df

def calculate_stochastic(df, k=14, d=3):
    result = ta.stoch(df['high'], df['low'], df['close'], k=k, d=d)
    df['stoch_k'] = result[f'STOCHk_{k}_{d}']
    df['stoch_d'] = result[f'STOCHd_{k}_{d}']
    return df

def calculate_intraday_indicators(df):
    df = calculate_supertrend(df)
    df = calculate_adx(df)
    df = calculate_stochastic(df)
    return df
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_indicators.py::test_calculate_supertrend -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/indicators/intraday.py
git commit -m "feat: add intraday indicators (Supertrend, ADX, Stochastic)"
```

---

## Phase 3: Signal Generation & ML Enhancement

### Task 7: Base Signal Generation

**Files:**
- Create: `src/signals/base_signals.py`
- Test: `tests/test_signals.py`

- [ ] **Step 1: Write the failing test**

```python
def test_scalping_signals():
    df = load_data('1min.csv')
    df = calculate_scalping_indicators(df)
    df = generate_scalping_signals(df)
    assert 'signal' in df.columns
    assert df['signal'].isin([0, 1, -1]).all()

def test_day_trading_signals():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_day_trading_indicators(df)
    df = generate_day_trading_signals(df)
    assert 'signal' in df.columns

def test_intraday_signals():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_intraday_indicators(df)
    df = generate_intraday_signals(df)
    assert 'signal' in df.columns
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_signals.py::test_scalping_signals -v`
Expected: FAIL

- [ ] **Step 3: Write implementation**

```python
import numpy as np

def generate_scalping_signals(df):
    df = df.copy()
    df['signal'] = 0
    
    # Long signal: price above EMA5, RSI < 30, volume spike
    long_condition = (
        (df['close'] > df['ema_5']) &
        (df['rsi_7'] < 30) &
        (df['volume_spike'] == True)
    )
    
    # Short signal: price below EMA5, RSI > 70, volume spike
    short_condition = (
        (df['close'] < df['ema_5']) &
        (df['rsi_7'] > 70) &
        (df['volume_spike'] == True)
    )
    
    df.loc[long_condition, 'signal'] = 1
    df.loc[short_condition, 'signal'] = -1
    
    return df

def generate_day_trading_signals(df):
    df = df.copy()
    df['signal'] = 0
    
    # Long: MACD crosses above signal, RSI < 70, price above VWAP
    long_condition = (
        (df['macd'] > df['macd_signal']) &
        (df['rsi'] < 70) &
        (df['close'] > df['vwap'])
    )
    
    # Short: MACD crosses below signal, RSI > 30, price below VWAP
    short_condition = (
        (df['macd'] < df['macd_signal']) &
        (df['rsi'] > 30) &
        (df['close'] < df['vwap'])
    )
    
    df.loc[long_condition, 'signal'] = 1
    df.loc[short_condition, 'signal'] = -1
    
    return df

def generate_intraday_signals(df):
    df = df.copy()
    df['signal'] = 0
    
    # Long: Supertrend direction changes to bullish, ADX > 25, Stochastic oversold
    long_condition = (
        (df['supertrend_direction'] == 1) &
        (df['adx'] > 25) &
        (df['stoch_k'] < 20)
    )
    
    # Short: Supertrend direction changes to bearish, ADX > 25, Stochastic overbought
    short_condition = (
        (df['supertrend_direction'] == -1) &
        (df['adx'] > 25) &
        (df['stoch_k'] > 80)
    )
    
    df.loc[long_condition, 'signal'] = 1
    df.loc[short_condition, 'signal'] = -1
    
    return df
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_signals.py::test_scalping_signals -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/signals/base_signals.py
git commit -m "feat: add base signal generation for all strategies"
```

---

### Task 8: ML Signal Filter

**Files:**
- Create: `src/signals/ml_filter.py`
- Test: `tests/test_signals.py`

- [ ] **Step 1: Write the failing test**

```python
def test_ml_signal_filter():
    df = load_data('1min.csv')
    df = calculate_scalping_indicators(df)
    df = generate_scalping_signals(df)
    df = add_ml_features(df)
    trained_model = train_ml_filter(df)
    df_test = apply_ml_filter(df, trained_model)
    assert 'ml_signal' in df_test.columns
    assert df_test['ml_signal'].isin([0, 1, -1]).all()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_signals.py::test_ml_signal_filter -v`
Expected: FAIL

- [ ] **Step 3: Write implementation**

```python
from sklearn.ensemble import RandomForestClassifier
import numpy as np

def add_ml_features(df):
    df = df.copy()
    
    # Price-based features
    df['price_change'] = df['close'].pct_change()
    df['price_change_5'] = df['close'].pct_change(5)
    
    # Volume features
    df['volume_change'] = df['volume'].pct_change()
    df['volume_ma_ratio'] = df['volume'] / df['volume'].rolling(20).mean()
    
    # Time-based features
    df['hour'] = pd.to_datetime(df.get('datetime', df.get('Date', '2025-01-01'))).dt.hour
    df['day_of_week'] = pd.to_datetime(df.get('datetime', df.get('Date', '2025-01-01'))).dt.dayofweek
    
    # Target: next candle direction
    df['next_direction'] = np.where(df['close'].shift(-1) > df['close'], 1, 0)
    
    return df

def train_ml_filter(df):
    feature_cols = ['price_change', 'price_change_5', 'volume_change', 'volume_ma_ratio']
    
    # Add indicator features if they exist
    for col in ['rsi_7', 'macd', 'adx', 'supertrend']:
        if col in df.columns:
            feature_cols.append(col)
    
    # Drop rows with NaN
    df_clean = df.dropna(subset=feature_cols + ['next_direction'])
    
    X = df_clean[feature_cols]
    y = df_clean['next_direction']
    
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X, y)
    
    return model

def apply_ml_filter(df, model):
    df = df.copy()
    df['ml_signal'] = df['signal']
    
    feature_cols = ['price_change', 'price_change_5', 'volume_change', 'volume_ma_ratio']
    for col in ['rsi_7', 'macd', 'adx', 'supertrend']:
        if col in df.columns:
            feature_cols.append(col)
    
    df_with_features = add_ml_features(df)
    
    # Predict only where we have valid signals
    signal_mask = df['signal'] != 0
    
    for idx in df[signal_mask].index:
        row_features = df_with_features.loc[idx, feature_cols].values.reshape(1, -1)
        if not np.isnan(row_features).any():
            prediction = model.predict(row_features)[0]
            # Only keep signal if ML agrees with direction
            if prediction == 1 and df.loc[idx, 'signal'] == -1:
                df.loc[idx, 'ml_signal'] = 0
            elif prediction == 0 and df.loc[idx, 'signal'] == 1:
                df.loc[idx, 'ml_signal'] = 0
    
    return df
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_signals.py::test_ml_signal_filter -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/signals/ml_filter.py
git commit -m "feat: add ML signal filter using Random Forest"
```

---

## Phase 4: Backtesting Engine

### Task 9: Backtest Engine

**Files:**
- Create: `src/backtest/engine.py`
- Test: `tests/test_backtest.py`

- [ ] **Step 1: Write the failing test**

```python
def test_backtest_single_trade():
    df = load_data('1min.csv')
    df['signal'] = [0] * len(df)
    df.loc[10, 'signal'] = 1  # Buy signal
    df.loc[20, 'signal'] = 0  # Close position
    
    trades = run_backtest(df, initial_capital=10000, stop_loss=1.0, take_profit=1.5)
    assert len(trades) > 0
    assert 'profit' in trades[0]

def test_stop_loss_trigger():
    df = load_data('1min.csv')
    df['signal'] = [0] * len(df)
    df.loc[10, 'signal'] = 1
    
    trades = run_backtest(df, initial_capital=10000, stop_loss=0.5, take_profit=2.0)
    # Should trigger stop loss
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_backtest.py::test_backtest_single_trade -v`
Expected: FAIL

- [ ] **Step 3: Write implementation**

```python
import numpy as np

def run_backtest(df, initial_capital=10000, stop_loss=1.0, take_profit=1.5, max_daily_trades=10):
    trades = []
    capital = initial_capital
    position = None
    entry_price = 0
    entry_idx = 0
    
    daily_trade_count = 0
    last_date = None
    
    for idx, row in df.iterrows():
        current_date = row.get('Date', row.get('datetime'))
        
        # Reset daily counter
        if last_date and str(current_date) != str(last_date):
            daily_trade_count = 0
        last_date = current_date
        
        # Check for entry signal
        if position is None and row['signal'] != 0 and daily_trade_count < max_daily_trades:
            position = row['signal']
            entry_price = row['close']
            entry_idx = idx
            daily_trade_count += 1
            
        # Check for exit
        elif position is not None:
            current_price = row['close']
            price_change_pct = (current_price - entry_price) / entry_price * 100
            
            # Apply direction
            if position == -1:  # Short
                price_change_pct = -price_change_pct
            
            # Stop loss or take profit hit
            if price_change_pct <= -stop_loss or price_change_pct >= take_profit:
                profit = capital * (price_change_pct / 100)
                capital += profit
                
                trades.append({
                    'entry_idx': entry_idx,
                    'exit_idx': idx,
                    'entry_price': entry_price,
                    'exit_price': current_price,
                    'direction': 'long' if position == 1 else 'short',
                    'profit_pct': price_change_pct,
                    'profit_dollars': profit,
                    'capital_after': capital
                })
                
                position = None
    
    return trades, capital

def calculate_max_drawdown(trades, initial_capital):
    capital_curve = [initial_capital]
    for trade in trades:
        capital_curve.append(trade['capital_after'])
    
    peak = capital_curve[0]
    max_dd = 0
    
    for capital in capital_curve:
        if capital > peak:
            peak = capital
        dd = (peak - capital) / peak * 100
        if dd > max_dd:
            max_dd = dd
    
    return max_dd
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_backtest.py::test_backtest_single_trade -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/backtest/engine.py
git commit -m "feat: add backtest engine with stop loss/take profit"
```

---

### Task 10: Performance Metrics

**Files:**
- Create: `src/backtest/metrics.py`
- Test: `tests/test_backtest.py`

- [ ] **Step 1: Write the failing test**

```python
def test_calculate_all_metrics():
    trades = [
        {'profit_pct': 1.5, 'profit_dollars': 150},
        {'profit_pct': -0.5, 'profit_dollars': -50},
        {'profit_pct': 2.0, 'profit_dollars': 200},
    ]
    initial_capital = 10000
    
    metrics = calculate_metrics(trades, initial_capital)
    
    assert 'total_profit' in metrics
    assert 'profit_factor' in metrics
    assert 'win_rate' in metrics
    assert 'sharpe_ratio' in metrics
    assert 'max_drawdown' in metrics
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_backtest.py::test_calculate_all_metrics -v`
Expected: FAIL

- [ ] **Step 3: Write implementation**

```python
import numpy as np

def calculate_metrics(trades, initial_capital):
    if not trades:
        return {
            'total_profit': 0,
            'profit_factor': 0,
            'win_rate': 0,
            'sharpe_ratio': 0,
            'max_drawdown': 0,
            'total_trades': 0,
            'avg_profit': 0,
            'avg_loss': 0
        }
    
    profits = [t['profit_dollars'] for t in trades]
    winning_trades = [p for p in profits if p > 0]
    losing_trades = [p for p in profits if p <= 0]
    
    total_profit = sum(profits)
    gross_profit = sum(winning_trades) if winning_trades else 0
    gross_loss = abs(sum(losing_trades)) if losing_trades else 1
    
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
    win_rate = len(winning_trades) / len(trades) * 100 if trades else 0
    
    # Sharpe ratio (simplified)
    returns = [p / initial_capital * 100 for p in profits]
    sharpe_ratio = (np.mean(returns) / np.std(returns)) if np.std(returns) > 0 else 0
    
    # Max drawdown
    max_dd = calculate_max_drawdown_from_trades(trades, initial_capital)
    
    return {
        'total_profit': total_profit,
        'profit_factor': profit_factor,
        'win_rate': win_rate,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_dd,
        'total_trades': len(trades),
        'avg_profit': np.mean(winning_trades) if winning_trades else 0,
        'avg_loss': np.mean(losing_trades) if losing_trades else 0,
        'final_capital': trades[-1]['capital_after'] if trades else initial_capital
    }

def calculate_max_drawdown_from_trades(trades, initial_capital):
    capital_curve = [initial_capital]
    for trade in trades:
        capital_curve.append(trade['capital_after'])
    
    peak = capital_curve[0]
    max_dd = 0
    
    for capital in capital_curve:
        if capital > peak:
            peak = capital
        dd = (peak - capital) / peak * 100
        if dd > max_dd:
            max_dd = dd
    
    return max_dd
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_backtest.py::test_calculate_all_metrics -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/backtest/metrics.py
git commit -m "feat: add performance metrics calculation"
```

---

## Phase 5: Dashboard & Analysis

### Task 11: Visualization Dashboard

**Files:**
- Create: `src/dashboard/visualizer.py`
- Test: `tests/test_dashboard.py`

- [ ] **Step 1: Write the failing test**

```python
def test_create_trade_chart():
    df = load_data('1min.csv')
    trades = [{'entry_idx': 10, 'exit_idx': 20, 'profit_dollars': 100}]
    
    chart = create_trade_chart(df, trades, 'scalping')
    assert chart is not None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_dashboard.py::test_create_trade_chart -v`
Expected: FAIL

- [ ] **Step 3: Write implementation**

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_trade_chart(df, trades, strategy_name):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.05, 
                        subplot_titles=('Price Chart', 'Volume'))
    
    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='Price'
    ), row=1, col=1)
    
    # Add trade markers
    for trade in trades:
        color = 'green' if trade['profit_dollars'] > 0 else 'red'
        fig.add_trace(go.Scatter(
            x=[trade['entry_idx']],
            y=[df.iloc[trade['entry_idx']]['low']],
            mode='markers',
            marker=dict(symbol='triangle-up', size=10, color='green'),
            name='Entry'
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=[trade['exit_idx']],
            y=[df.iloc[trade['exit_idx']]['high']],
            mode='markers',
            marker=dict(symbol='triangle-down', size=10, color=color),
            name='Exit'
        ), row=1, col=1)
    
    # Volume
    fig.add_trace(go.Bar(
        x=df.index,
        y=df['volume'],
        name='Volume'
    ), row=2, col=1)
    
    fig.update_layout(
        title=f'{strategy_name} Trading Results',
        height=600
    )
    
    return fig

def save_dashboard(df, trades, metrics, strategy_name):
    fig = create_trade_chart(df, trades, strategy_name)
    fig.write_html(f'dashboard_{strategy_name}.html')
    return fig
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_dashboard.py::test_create_trade_chart -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dashboard/visualizer.py
git commit -m "feat: add trade visualization dashboard"
```

---

### Task 12: Report Generation

**Files:**
- Create: `src/dashboard/report.py`
- Test: `tests/test_dashboard.py`

- [ ] **Step 1: Write the failing test**

```python
def test_generate_comparison_report():
    results = {
        'scalping': {'total_profit': 1000, 'win_rate': 60},
        'day_trading': {'total_profit': 1500, 'win_rate': 55},
        'intraday': {'total_profit': 800, 'win_rate': 50}
    }
    
    report = generate_comparison_report(results)
    assert 'best_strategy' in report
    assert 'recommendation' in report
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_dashboard.py::test_generate_comparison_report -v`
Expected: FAIL

- [ ] **Step 3: Write implementation**

```python
def generate_comparison_report(results):
    # Find best strategy by total profit
    best_strategy = max(results.items(), key=lambda x: x[1]['total_profit'])
    
    report = {
        'best_strategy': best_strategy[0],
        'best_profit': best_strategy[1]['total_profit'],
        'all_results': results,
        'recommendation': f"Use {best_strategy[0]} strategy for production trading.",
        'confidence': calculate_confidence(results, best_strategy[0])
    }
    
    return report

def calculate_confidence(results, best_strategy):
    best = results[best_strategy]
    others = [r['total_profit'] for k, r in results.items() if k != best_strategy]
    
    if not others:
        return 'High'
    
    avg_others = sum(others) / len(others)
    advantage = (best['total_profit'] - avg_others) / avg_others * 100 if avg_others > 0 else 0
    
    if advantage > 50:
        return 'High'
    elif advantage > 20:
        return 'Medium'
    else:
        return 'Low'

def generate_error_analysis(trades):
    total_trades = len(trades)
    if total_trades == 0:
        return {'error_rate': 0, 'analysis': 'No trades to analyze'}
    
    losing_trades = [t for t in trades if t['profit_dollars'] <= 0]
    error_rate = len(losing_trades) / total_trades * 100
    
    avg_loss = sum([t['profit_dollars'] for t in losing_trades]) / len(losing_trades) if losing_trades else 0
    
    return {
        'error_rate': error_rate,
        'total_trades': total_trades,
        'losing_trades': len(losing_trades),
        'avg_loss': abs(avg_loss),
        'analysis': f'{error_rate:.1f}% of trades resulted in loss'
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_dashboard.py::test_generate_comparison_report -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/dashboard/report.py
git commit -m "feat: add comparison report and error analysis"
```

---

## Phase 6: Main Execution & Integration

### Task 13: Main Script

**Files:**
- Create: `main.py`
- Create: `requirements.txt`

- [ ] **Step 1: Write main.py**

```python
from src.data.loader import load_data, filter_2025
from src.data.splitter import split_train_test
from src.data.resampler import resample_to_timeframe
from src.indicators.scalping import calculate_scalping_indicators
from src.indicators.day_trading import calculate_day_trading_indicators
from src.indicators.intraday import calculate_intraday_indicators
from src.signals.base_signals import generate_scalping_signals, generate_day_trading_signals, generate_intraday_signals
from src.signals.ml_filter import train_ml_filter, apply_ml_filter, add_ml_features
from src.backtest.engine import run_backtest
from src.backtest.metrics import calculate_metrics
from src.dashboard.visualizer import save_dashboard
from src.dashboard.report import generate_comparison_report, generate_error_analysis
import pandas as pd

def main():
    print("Loading data...")
    
    # Load 1min data
    df_1min = load_data('1min.csv')
    df_1min_2025 = filter_2025(df_1min)
    train_1min, test_1min = split_train_test(df_1min_2025, '2025-06-30')
    
    # Load 15min data
    df_15min = load_data('NQ_15min_processed.csv')
    df_15min_2025 = filter_2025(df_15min)
    train_15min, test_15min = split_train_test(df_15min_2025, '2025-06-30')
    
    results = {}
    
    # ========== SCALPING ==========
    print("\n--- Testing Scalping Strategy ---")
    scalping_train = calculate_scalping_indicators(train_1min.copy())
    scalping_train = generate_scalping_signals(scalping_train)
    scalping_train = add_ml_features(scalping_train)
    ml_model = train_ml_filter(scalping_train)
    
    scalping_test = calculate_scalping_indicators(test_1min.copy())
    scalping_test = generate_scalping_signals(scalping_test)
    scalping_test = apply_ml_filter(scalping_test, ml_model)
    
    trades, final_capital = run_backtest(scalping_test, initial_capital=10000, 
                                         stop_loss=0.5, take_profit=1.5)
    metrics = calculate_metrics(trades, 10000)
    results['scalping'] = metrics
    
    print(f"Scalping: Profit=${metrics['total_profit']:.2f}, Win Rate={metrics['win_rate']:.1f}%")
    
    # ========== DAY TRADING ==========
    print("\n--- Testing Day Trading Strategy ---")
    daytrain = calculate_day_trading_indicators(train_15min.copy())
    daytrain = generate_day_trading_signals(daytrain)
    daytrain = add_ml_features(daytrain)
    ml_model_dt = train_ml_filter(daytrain)
    
    daytest = calculate_day_trading_indicators(test_15min.copy())
    daytest = generate_day_trading_signals(daytest)
    daytest = apply_ml_filter(daytest, ml_model_dt)
    
    trades_dt, final_capital_dt = run_backtest(daytest, initial_capital=10000,
                                               stop_loss=1.0, take_profit=2.0)
    metrics_dt = calculate_metrics(trades_dt, 10000)
    results['day_trading'] = metrics_dt
    
    print(f"Day Trading: Profit=${metrics_dt['total_profit']:.2f}, Win Rate={metrics_dt['win_rate']:.1f}%")
    
    # ========== INTRADAY ==========
    print("\n--- Testing Intraday Strategy ---")
    intraday_train = calculate_intraday_indicators(train_15min.copy())
    intraday_train = generate_intraday_signals(intraday_train)
    intraday_train = add_ml_features(intraday_train)
    ml_model_intra = train_ml_filter(intraday_train)
    
    intraday_test = calculate_intraday_indicators(test_15min.copy())
    intraday_test = generate_intraday_signals(intraday_test)
    intraday_test = apply_ml_filter(intraday_test, ml_model_intra)
    
    trades_intra, final_capital_intra = run_backtest(intraday_test, initial_capital=10000,
                                                      stop_loss=1.0, take_profit=2.0)
    metrics_intra = calculate_metrics(trades_intra, 10000)
    results['intraday'] = metrics_intra
    
    print(f"Intraday: Profit=${metrics_intra['total_profit']:.2f}, Win Rate={metrics_intra['win_rate']:.1f}%")
    
    # ========== COMPARISON ==========
    print("\n" + "="*50)
    print("COMPARISON RESULTS")
    print("="*50)
    
    for strategy, metrics in results.items():
        print(f"\n{strategy.upper()}:")
        print(f"  Total Profit: ${metrics['total_profit']:.2f}")
        print(f"  Profit Factor: {metrics['profit_factor']:.2f}")
        print(f"  Win Rate: {metrics['win_rate']:.1f}%")
        print(f"  Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
        print(f"  Max Drawdown: {metrics['max_drawdown']:.2f}%")
        print(f"  Total Trades: {metrics['total_trades']}")
    
    # Generate report
    report = generate_comparison_report(results)
    print(f"\nBEST STRATEGY: {report['best_strategy']}")
    print(f"RECOMMENDATION: {report['recommendation']}")
    print(f"CONFIDENCE: {report['confidence']}")
    
    # Error analysis
    print("\n--- Error Analysis ---")
    for strategy, metrics in results.items():
        error_analysis = generate_error_analysis(trades if strategy == 'scalping' else 
                                                 trades_dt if strategy == 'day_trading' else trades_intra)
        print(f"{strategy}: {error_analysis['analysis']}")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Write requirements.txt**

```
pandas
numpy
pandas-ta
scikit-learn
plotly
pytest
```

- [ ] **Step 3: Commit**

```bash
git add main.py requirements.txt
git commit -m "feat: add main execution script and requirements"
```

---

## Phase 7: Validation & Testing

### Task 14: Integration Test

**Files:**
- Modify: `tests/` (create full integration test)

- [ ] **Step 1: Run full pipeline**

```bash
cd /mnt/data/projects/trading
pip install -r requirements.txt
python main.py
```

- [ ] **Step 2: Verify output**

Expected: All three strategies run, metrics calculated, comparison report generated

- [ ] **Step 3: Check for errors**

Run: `pytest tests/ -v`
Expected: All tests pass

- [ ] **Step 4: Commit**

```bash
git add tests/
git commit -m "test: add integration tests"
```

---

## Summary

This plan creates a complete trading algorithm finder with:

1. **Data pipeline** - Load, filter 2025 data, split train/test
2. **Indicators** - RSI, EMA, MACD, VWAP, ATR, Supertrend, ADX, Stochastic
3. **Signals** - Rule-based entry/exit with ML enhancement
4. **Backtesting** - Realistic simulation with stop loss/take profit
5. **Metrics** - Profit, profit factor, Sharpe, win rate, drawdown
6. **Dashboard** - Visual charts and comparison report

The output will show which strategy (scalping/day trading/intraday) is most profitable on the test data (Jul-Sep 2025).

---

**Plan complete and saved to `docs/superpowers/plans/2025-05-12-nasdaq-trading-algorithm.md`**

Two execution options:

1. **Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?