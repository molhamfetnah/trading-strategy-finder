# Live Trading Dashboard Demo

## Overview

This folder contains the complete output from running the live trading simulation demo on historical NASDAQ data (July - September 2025).

## Files

| File | Description |
|------|-------------|
| `README.md` | This file - demo documentation |
| `console-output.txt` | Complete terminal output from simulation |
| `trades-summary.json` | Machine-readable trade data |
| `strategy-comparison.json` | Strategy comparison results |
| `live_trading_dashboard.html` | Interactive candlestick chart with trades |
| `equity_curve_dashboard.html` | Equity curve visualization |

## Quick Start

### Run Live Demo
```bash
cd /mnt/data/projects/trading
python3 live_dashboard.py
```

### View Visual Dashboard
Open `live_trading_dashboard.html` in your browser to see:
- Candlestick chart with trade markers
- Entry/Exit points highlighted
- RSI indicator
- Volume bars

## Demo Results Summary

| Metric | Value |
|--------|-------|
| Test Period | July - September 2025 |
| Initial Capital | $10,000 |
| Final Capital | $10,107.66 |
| Total Profit | +$107.66 (1.08%) |
| Total Trades | 17 |
| Win Rate | 29.4% |
| Profit Factor | 1.17 |
| Best Strategy | Scalping (1min) |

## Trade History (17 Trades)

| # | Direction | Entry | Exit | P/L % | P/L $ | Exit Reason |
|---|-----------|-------|------|-------|-------|-------------|
| 1 | SHORT | 24746.75 | 24885.00 | -0.56% | -$55.87 | STOP LOSS |
| 2 | LONG | 24720.50 | 24593.75 | -0.51% | -$50.99 | STOP LOSS |
| 3 | LONG | 24489.25 | 24353.00 | -0.56% | -$55.04 | STOP LOSS |
| 4 | SHORT | 23535.00 | 23653.00 | -0.50% | -$49.33 | STOP LOSS |
| 5 | LONG | 23607.50 | 23483.25 | -0.53% | -$51.52 | STOP LOSS |
| 6 | SHORT | 23579.50 | 23210.50 | +1.56% | +$148.38 | TAKE PROFIT |
| 7 | LONG | 23471.50 | 23823.75 | +1.50% | +$148.42 | TAKE PROFIT |
| 8 | SHORT | 23793.50 | 23913.00 | -0.50% | -$50.41 | STOP LOSS |
| 9 | LONG | 23885.25 | 23758.00 | -0.53% | -$53.21 | STOP LOSS |
| 10 | LONG | 23627.50 | 23509.00 | -0.50% | -$49.82 | STOP LOSS |
| 11 | LONG | 23408.00 | 23284.50 | -0.53% | -$52.15 | STOP LOSS |
| 12 | LONG | 22875.00 | 23220.75 | +1.51% | +$148.62 | TAKE PROFIT |
| 13 | LONG | 23666.50 | 23492.50 | -0.74% | -$73.38 | STOP LOSS |
| 14 | LONG | 23452.25 | 23332.50 | -0.51% | -$50.59 | STOP LOSS |
| 15 | SHORT | 23394.25 | 23043.00 | +1.50% | +$148.00 | TAKE PROFIT |
| 16 | SHORT | 23061.00 | 23176.75 | -0.50% | -$50.22 | STOP LOSS |
| 17 | SHORT | 23033.50 | 22680.00 | +1.53% | +$152.78 | TAKE PROFIT |

## Strategy Comparison

| Strategy | Trades | Profit | Win Rate | PF | Sharpe | Drawdown |
|----------|--------|--------|----------|-----|--------|----------|
| 🏆 Scalping | 17 | +$107.66 | 29.4% | 1.17 | 0.07 | 2.6% |
| Day Trading | 23 | -$719.55 | 26.1% | 0.62 | -0.23 | 11.2% |
| Intraday | 0 | $0.00 | 0% | 0 | 0 | 0% |

## Key Insights

1. **Scalping Strategy** - Only profitable strategy
   - 5 winning trades, 12 losing trades
   - Win rate 29.4% (low but profitable due to favorable R:R)
   - All winners were TAKE PROFIT exits (+1.5-1.56%)
   - All losers were STOP LOSS exits (-0.5-0.74%)

2. **Day Trading Strategy** - Lost money
   - More trades (23) but negative returns
   - MACD/VWAP combination not effective for 15min timeframe

3. **Intraday Strategy** - No signals generated
   - Supertrend thresholds too strict
   - ADX > 25 rarely met in test period

## Next Steps for Live Trading

1. **Connect to live data** - WebSocket/API integration
2. **Broker integration** - Interactive Brokers, Alpaca, etc.
3. **Parameter tuning** - Adjust RSI, volume thresholds
4. **Add market regime detection** - Trend vs range filtering
5. **Improve ML model** - More features, better classifiers

---
**Demo Date:** 2025-05-13  
**Repository:** git@github.com:molhamfetnah/trading-strategy-finder.git