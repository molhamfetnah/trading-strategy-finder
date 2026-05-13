# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-05-13

### Added
- Initial implementation of NASDAQ Trading Strategy Finder
- Hybrid ML-powered strategy comparison system

### Data Pipeline
- CSV data loader with column normalization (`src/data/loader.py`)
- 2025 data filter and train/test split (`src/data/splitter.py`)
- Timeframe resampling (`src/data/resampler.py`)

### Indicators
- Scalping indicators: RSI(7), EMA(5,20), Volume spike (`src/indicators/scalping.py`)
- Day trading indicators: MACD, VWAP, ATR (`src/indicators/day_trading.py`)
- Intraday indicators: Supertrend, ADX, Stochastic (`src/indicators/intraday.py`)

### Signals
- Rule-based signal generation for all strategies (`src/signals/base_signals.py`)
- ML signal filter using Random Forest (`src/signals/ml_filter.py`)

### Backtest Engine
- Trade simulation with stop loss/take profit (`src/backtest/engine.py`)
- Comprehensive performance metrics (`src/backtest/metrics.py`)

### Dashboard
- Trade visualization (`src/dashboard/visualizer.py`)
- Comparison reports and error analysis (`src/dashboard/report.py`)

### Testing
- 29 passing unit tests covering all modules

### Documentation
- README.md - Project overview and quick start
- PLAYBOOK.md - Comprehensive trading guide
- API.md - Code reference documentation

### Strategy Results (Test Period: Jul-Sep 2025)

| Strategy | Profit | Win Rate | Profit Factor | Status |
|----------|--------|----------|---------------|--------|
| Scalping | $107.66 | 29.4% | 1.17 | Best |
| Day Trading | -$719.55 | 26.1% | 0.62 | Failed |
| Intraday | $0.00 | 0% | 0 | No signals |

---

## [Unreleased]

### Known Issues
- Win rates lower than target (>50%)
- Limited trading frequency
- Intraday strategy not generating signals

### Planned Improvements
- Parameter tuning for signal sensitivity
- Additional ML features and model optimization
- Market regime detection
- Enhanced risk management