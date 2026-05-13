# NASDAQ Trading Strategy Finder

A hybrid ML-powered trading algorithm finder that compares scalping, day trading, and intraday strategies to identify the most profitable approach for NASDAQ futures trading.

## Overview

This project implements a proof-of-concept trading strategy finder that:
- Analyzes historical NASDAQ data (2025)
- Tests three different trading timeframes: scalping (1min), day trading (15min), intraday/swing (15min)
- Uses a hybrid approach combining classical technical indicators with ML signal filtering
- Compares strategies across all key performance metrics

## Project Structure

```
trading/
├── src/
│   ├── data/
│   │   ├── loader.py           # CSV data loading with column normalization
│   │   ├── splitter.py         # 2025 data filter and train/test split
│   │   └── resampler.py         # Timeframe resampling (1min to 5min, 15min, etc.)
│   ├── indicators/
│   │   ├── scalping.py         # RSI(7), EMA(5,20), Volume spike detection
│   │   ├── day_trading.py      # MACD, VWAP, ATR indicators
│   │   └── intraday.py         # Supertrend, ADX, Stochastic indicators
│   ├── signals/
│   │   ├── base_signals.py     # Rule-based entry/exit signals
│   │   └── ml_filter.py        # Random Forest signal enhancement
│   ├── backtest/
│   │   ├── engine.py            # Trade simulation with stop loss/take profit
│   │   └── metrics.py           # Performance metrics calculation
│   └── dashboard/
│       ├── visualizer.py        # Trade chart and equity curve generation
│       └── report.py            # Comparison reports and error analysis
├── tests/                       # 29 passing unit tests
├── docs/
│   ├── specs/                   # Design specifications
│   └── plans/                  # Implementation plans
├── main.py                      # Main execution script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the strategy finder
python3 main.py
```

## Data Requirements

- **1min.csv**: 1-minute NASDAQ futures data (Date, Time, Open, High, Low, Close, Volume)
- **NQ_15min_processed.csv**: 15-minute NASDAQ futures data (timestamps, open, high, low, close, volume)

Data should cover January 2025 - September 2025 for proper train/test split.

## How It Works

### 1. Data Pipeline
- Loads and normalizes CSV data
- Filters to 2025 data only
- Splits: Training (Jan-Jun 2025) | Test (Jul-Sep 2025)

### 2. Strategy Types

| Strategy | Timeframe | Indicators | Stop Loss | Take Profit |
|----------|-----------|------------|-----------|-------------|
| Scalping | 1 min | RSI(7), EMA(5,20), Volume | 0.5% | 1.5% |
| Day Trading | 15 min | MACD, VWAP, ATR | 1.0% | 2.0% |
| Intraday | 15 min | Supertrend, ADX, Stochastic | 1.0% | 2.0% |

### 3. Hybrid Approach
- **Classical Indicators**: Rule-based signals from technical indicators
- **ML Enhancement**: Random Forest classifier filters signals using price/volume patterns

### 4. Signal Generation

**Scalping:**
- Long: Price > EMA5 + RSI < 30 + Volume spike
- Short: Price < EMA5 + RSI > 70 + Volume spike

**Day Trading:**
- Long: MACD > Signal + RSI < 70 + Price > VWAP
- Short: MACD < Signal + RSI > 30 + Price < VWAP

**Intraday:**
- Long: Supertrend bullish + ADX > 25 + Stochastic oversold
- Short: Supertrend bearish + ADX > 25 + Stochastic overbought

## Performance Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Total Profit | Net profit/loss | Positive |
| Profit Factor | Gross profit / Gross loss | > 1.5 |
| Win Rate | % of profitable trades | > 50% |
| Sharpe Ratio | Risk-adjusted returns | > 1.0 |
| Max Drawdown | Maximum peak-to-trough decline | < 10% |

## Backtest Results

Test period: July - September 2025 (3 months)
Initial capital: $10,000

### Strategy Comparison

| Strategy | Total Profit | Win Rate | Profit Factor | Sharpe | Max DD |
|----------|--------------|----------|---------------|--------|--------|
| **Scalping** | $107.66 | 29.4% | 1.17 | 0.07 | 2.63% |
| Day Trading | -$719.55 | 26.1% | 0.62 | -0.23 | 11.21% |
| Intraday | $0.00 | - | - | - | - |

### Key Observations

1. **Scalping** was the only profitable strategy during the test period
2. **Day trading** had significant losses with high drawdown
3. **Intraday** generated no signals (indicator thresholds not met)
4. Win rates are low across all strategies (~26-30%)
5. Profit factors are marginal (1.17 for scalping)

## Recommendations for Production

### Parameter Tuning Needed

1. **Increase signal sensitivity**
   - RSI thresholds: 30/70 → 35/65
   - ADX threshold: 25 → 20

2. **Adjust risk parameters**
   - Consider wider stop loss (1.0%) with larger take profit (2.5%)
   - Increase max daily trades

3. **Improve ML model**
   - Add more features (candle patterns, time-based features)
   - Try different classifiers (XGBoost, LightGBM)
   - Tune hyperparameters

4. **Add market regime detection**
   - Trend vs range market filtering
   - Volume profile analysis

## Development

```bash
# Run tests
pytest tests/ -v

# Run with specific test
pytest tests/test_indicators.py -v

# Run main script
python3 main.py
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      MAIN.PY                                 │
│              Strategy Comparison Engine                      │
└─────────────────┬───────────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┬──────────────────┐
    ▼             ▼             ▼                  ▼
┌────────┐  ┌──────────┐  ┌──────────┐       ┌──────────────┐
│ Scalping│  │Day Trading│ │ Intraday  │       │Comparison    │
│ (1min)  │  │ (15min)   │ │ (15min)   │       │Report        │
└────┬────┘  └─────┬────┘  └─────┬────┘       └──────────────┘
     │             │             │
     ▼             ▼             ▼
┌────────────────────────────────────────────────────────────┐
│              BACKTEST ENGINE                               │
│  - Entry/Exit signals   - Stop loss/Take profit           │
│  - Position tracking    - Daily trade limits              │
└─────────────────────────────┬────────────────────────────┘
                              ▼
┌────────────────────────────────────────────────────────────┐
│              PERFORMANCE METRICS                           │
│  - Total profit    - Win rate     - Sharpe ratio          │
│  - Profit factor   - Max drawdown                        │
└────────────────────────────────────────────────────────────┘
```

## Dependencies

- pandas
- numpy
- scikit-learn
- plotly
- pytest

## License

MIT License

## Authors

Trading Strategy Finder - Proof of Concept

---

**Disclaimer**: This is a proof-of-concept implementation. Past performance does not guarantee future results. Always use proper risk management and consult with financial advisors before making trading decisions.