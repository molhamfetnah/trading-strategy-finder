# TradingView-Style Dashboard - Design Spec

**Date:** 2025-05-13  
**Status:** Approved

## Overview

A comprehensive TradingView-style dashboard that visualizes the scalping strategy backtest results over the full test period (July-September 2025, 87,243 candles). The dashboard will feature live-style scrolling, trade annotations, and detailed analysis panels.

## Sections

### 1. Header Bar
- Strategy name: "NASDAQ Scalping Strategy"
- Test period: "Jul 1 - Sep 26, 2025"
- Initial Capital: $10,000
- Final Capital: $10,807.29
- Total Return: +8.07%
- Real-time clock showing current simulation position

### 2. Main Chart (TradingView-style)
- **Candlestick chart** with full 87,243 candles
- **Zoom controls**: Scroll to zoom, drag to pan
- **Time range selector**: 1D, 1W, 1M, 3M buttons
- **Overlays:**
  - EMA 5 (blue)
  - EMA 15 (orange)
  - Entry markers (green triangles up)
  - Exit markers (red/green triangles down)
- **Indicator panels:**
  - RSI (7) with 30/70 lines
  - Volume bars with spike highlights
- **Trade tooltips:** Hover on markers to see trade details

### 3. Trade Log Panel (Right Sidebar)
- Scrollable trade list
- Each trade shows:
  - Trade #, Direction (LONG/SHORT)
  - Entry time, Entry price
  - Exit time, Exit price
  - Profit % and Profit $
  - Exit reason (STOP LOSS / TAKE PROFIT)
  - Indicators at entry: RSI, EMA position, Volume spike
- Color coding: Green for wins, Red for losses
- Click to highlight trade on chart

### 4. Performance Metrics Panel (Top Right)
- Total Profit: $807.29
- Profit Factor: 3.56
- Win Rate: 54.5%
- Sharpe Ratio: 0.59
- Max Drawdown: 1.24%
- Total Trades: 11
- Avg Win: $176.29
- Avg Loss: -$49.55

### 5. Trade Breakdown Analysis
- Right Moves section (winners):
  - Trade #, entry conditions, exit conditions, profit
  - What indicators said at entry/exit
- Wrong Moves section (losers):
  - Trade #, entry conditions, exit conditions, loss
  - What went wrong (indicator readings)

### 6. Playbook Panel
- Entry Rules:
  - RSI(5) < 30 (oversold)
  - Price > EMA 5
  - Volume spike > 2.0x average
  - ML filter confirmed
- Exit Rules:
  - Take Profit: +1.8% (TP1.8)
  - Stop Loss: -0.6% (SL0.6)
- Best Setup: "RSI oversold + Volume spike + Price above EMA"
- Worst Setup: "Late signals, missed moves"

### 7. Logs Panel
- Timestamp, Event type, Details
- Event types: SIGNAL, ENTRY, EXIT, METRICS_UPDATE
- Filter by event type
- Search functionality

### 8. Insights Panel
- Key findings:
  - "Win rate of 54.5% is acceptable with 3:1 reward:risk"
  - "All winners hit take profit, all losers hit stop loss"
  - "ML filter improved profit factor from 2.1 to 3.56"
  - "11 trades over 3 months = ~1 trade per week"
- Recommendations:
  - "Consider tightening stop loss to 0.4% for more trades"
  - "Volume spike threshold of 2.0x works well"
  - "EMA crossover at 5/15 is optimal"

### 9. Equity Curve (Mini Chart)
- Bottom of main chart
- Shows capital progression over time
- Annotations for trades

## Technical Approach

- **Framework:** Single HTML file with Plotly.js for charts
- **Data:** Pre-computed in Python, serialized to JSON, embedded in HTML
- **Interactivity:** Plotly's built-in zoom/pan, custom JavaScript for trade highlighting
- **Performance:** Virtual scrolling for trade list, lazy-load candle data

## File Output
- `docs/ultimate_trading_dashboard.html` - Main dashboard file
- `docs/trading_dashboard.html` - Existing, will be enhanced