# NASDAQ Trading Algorithm Finder - Design Specification

## Project Overview

**Purpose:** Build a hybrid trading algorithm that finds the most profitable strategy (scalping/day trading/intraday) using NASDAQ historical data for production use.

**Data Sources:**
- 1min.csv: ~2M rows, 2020-01-01 to 2025-09-26
- NQ_15min_processed.csv: ~135K rows, same date range

## Data Split

- **Training:** Jan 2025 - June 2025 (6 months)
- **Test:** July 2025 - Sep 2025 (3 months)
- **Target Asset:** NASDAQ futures (NQ)

## Approach: Hybrid (C)

Combines classical technical indicators as base signals with ML classifiers to filter/enhance signals.

### Why Hybrid for Production:
- Interpretable base rules (you can understand why a trade was taken)
- ML can capture complex patterns classical indicators miss
- Better risk control than pure ML
- You can override/audit signals

## Strategy Types to Test

### 1. Scalping (1-5 min)
- **Timeframe:** 1-minute candles
- **Indicators:** RSI(7), EMA(5,20), Volume spike
- **Entry:** Price crosses EMA + RSI oversold/overbought + volume confirmation
- **Exit:** Quick profit target or stop loss

### 2. Day Trading (15min-1hr)
- **Timeframe:** 15-minute candles
- **Indicators:** MACD, RSI(14), VWAP, ATR
- **Entry:** MACD crossover + RSI zone + price above/below VWAP
- **Exit:** ATR-based profit target or end-of-day close

### 3. Intraday/Swing (4hr-daily)
- **Timeframe:** 15min or 4hr candles
- **Indicators:** Supertrend, ADX, Stochastic
- **Entry:** Supertrend breakout + ADX > 25 + Stochastic crossover
- **Exit:** Trend reversal or stop loss

## Risk Parameters (Conservative)

| Parameter | Value |
|-----------|-------|
| Stop Loss | 0.5% - 1% |
| Take Profit | 1.5% - 2% (RRR 1:1.5+) |
| Position Sizing | Fixed 2-5% of capital |
| Max Daily Trades | 10-15 |
| Max Concurrent Positions | 2 |

## Technical Implementation

### Phase 1: Data Pipeline
- Load and clean CSV files
- Filter 2025 data only (Jan-Sep)
- Split into train (Jan-Jun) / test (Jul-Sep)
- Resample to required timeframes

### Phase 2: Indicator Calculation
- Calculate all indicators for each strategy
- Generate base signals from indicator rules

### Phase 3: ML Enhancement
- Feature engineering: price patterns, indicators, volume, time features
- Train classifier (Random Forest or XGBoost) to predict direction
- Use ML predictions to filter/weight indicator signals

### Phase 4: Backtesting Engine
- Simulate trades with realistic conditions
- Apply conservative risk parameters
- Calculate all metrics

### Phase 5: Analysis & Dashboard
- Compare strategies across all metrics
- Generate visualization dashboard
- Error rate analysis

## Success Metrics

| Metric | Target |
|--------|--------|
| Total Profit | Positive |
| Profit Factor | > 1.5 |
| Sharpe Ratio | > 1.0 |
| Win Rate | > 50% |
| Max Drawdown | < 10% |

## Deliverables

1. **Strategy Comparison Report** - Best performing timeframe
2. **Production Playbook** - Exact entry/exit rules
3. **Trade Dashboard** - Visual trade log with P&L
4. **Error Analysis** - False signal rate
5. **Confidence Score** - How confident to be in results

## Key Decisions for Production

- Use 1min data for scalping
- Use 15min data for day trading and intraday
- Focus on long (buy) and short (sell) signals
- Include transaction costs simulation

---

*Design approved for implementation*