# NASDAQ Trading Strategy Playbook

## Comprehensive Trading Guide

---

## Executive Summary

This playbook documents the findings from backtesting three trading strategies on NASDAQ futures (NQ) data from January-September 2025.

**Test Period:** July - September 2025 (3 months)  
**Initial Capital:** $10,000  
**Data Split:** Training (Jan-Jun) | Testing (Jul-Sep)

### Results Summary

| Strategy | Profit | Win Rate | Profit Factor | Sharpe | Drawdown |
|----------|--------|----------|---------------|--------|----------|
| **Scalping** | +$107.66 | 29.4% | 1.17 | 0.07 | 2.63% |
| Day Trading | -$719.55 | 26.1% | 0.62 | -0.23 | 11.21% |
| Intraday | $0 | 0% | 0 | 0 | 0% |

**Recommendation:** Scalping strategy shows marginal profitability. Requires parameter tuning before production use.

---

## 1. Strategy Definitions

### 1.1 Scalping Strategy

**Purpose:** Quick trades capturing small price movements  
**Timeframe:** 1-minute candles  
**Risk Profile:** Conservative  

#### Entry Rules (Long)
- Price crosses above EMA(5)
- RSI(7) below 30 (oversold)
- Volume spike (>2x 20-period average)

#### Entry Rules (Short)
- Price crosses below EMA(5)
- RSI(7) above 70 (overbought)
- Volume spike (>2x 20-period average)

#### Exit Rules
- Stop Loss: 0.5% from entry
- Take Profit: 1.5% from entry
- Max holding time: 15 minutes

#### Position Sizing
- Max 2% of capital per trade
- Max 10 trades per day

---

### 1.2 Day Trading Strategy

**Purpose:** Capture intraday trends  
**Timeframe:** 15-minute candles  
**Risk Profile:** Moderate  

#### Entry Rules (Long)
- MACD crosses above signal line
- RSI(14) below 70 (not overbought)
- Price above VWAP

#### Entry Rules (Short)
- MACD crosses below signal line
- RSI(14) above 30 (not oversold)
- Price below VWAP

#### Exit Rules
- Stop Loss: 1.0% from entry
- Take Profit: 2.0% from entry
- Close all positions by 16:00 EST

#### Position Sizing
- Max 3% of capital per trade
- Max 5 trades per day

---

### 1.3 Intraday/Swing Strategy

**Purpose:** Capture multi-hour trends  
**Timeframe:** 15-minute candles  
**Risk Profile:** Moderate-Aggressive  

#### Entry Rules (Long)
- Supertrend changes to bullish
- ADX > 25 (trending market)
- Stochastic(14,3) below 20 (oversold bounce)

#### Entry Rules (Short)
- Supertrend changes to bearish
- ADX > 25 (trending market)
- Stochastic(14,3) above 80 (overbought)

#### Exit Rules
- Stop Loss: 1.0% from entry
- Take Profit: 2.0% from entry
- Or trend reversal signal

#### Position Sizing
- Max 5% of capital per trade
- Max 3 trades per day

---

## 2. Performance Analysis

### 2.1 Scalping Performance (Best)

```
Total Trades: 17
Winning Trades: 5
Losing Trades: 12
Win Rate: 29.4%
Profit Factor: 1.17
Sharpe Ratio: 0.07
Max Drawdown: 2.63%
```

**Strengths:**
- Only profitable strategy
- Low drawdown (2.63%)
- Quick trade execution
- Clear entry signals

**Weaknesses:**
- Low win rate (29.4%)
- Only 17 trades in 3 months
- Profit factor barely above 1.0

---

### 2.2 Day Trading Performance (Failed)

```
Total Trades: 23
Winning Trades: 6
Losing Trades: 17
Win Rate: 26.1%
Profit Factor: 0.62
Sharpe Ratio: -0.23
Max Drawdown: 11.21%
```

**Issues:**
- Profit factor < 1.0 (losing money)
- High drawdown (11.21%)
- MACD signals too slow for 15min timeframe
- VWAP causes false signals in ranging markets

---

### 2.3 Intraday Performance (No Signals)

```
Total Trades: 0
Signals Generated: 0
```

**Issues:**
- ADX threshold too strict (>25)
- Supertrend needs strong trends to trigger
- NASDAQ often trades in ranges
- Stochastic thresholds too restrictive

---

## 3. Key Findings

### 3.1 Market Conditions (Jul-Sep 2025)

- High volatility periods alternating with low volatility
- Ranging markets more common than trending
- Volume spikes frequent but not always directional
- End-of-day momentum often reverses

### 3.2 Strategy Effectiveness

| Condition | Scalping | Day Trading | Intraday |
|-----------|----------|-------------|----------|
| Trending Market | Good | Poor | Good |
| Ranging Market | Poor | Poor | None |
| High Volatility | Good | Moderate | None |
| Low Volatility | None | None | None |
| High Volume | Good | Good | None |

### 3.3 Signal Quality

| Signal Type | Accuracy | Frequency |
|-------------|----------|-----------|
| Scalping Long | 35% | Low |
| Scalping Short | 25% | Low |
| Day Trading Long | 30% | Moderate |
| Day Trading Short | 23% | Moderate |
| Intraday Long | N/A | None |
| Intraday Short | N/A | None |

---

## 4. Recommended Improvements

### 4.1 Parameter Adjustments

#### Scalping (Current Best)
```
RSI(7): 30/70 → 35/65
Volume threshold: 2.0x → 1.5x
Stop Loss: 0.5% → 0.75%
Take Profit: 1.5% → 2.0%
Max Trades: 10 → 15
```

#### Day Trading
```
MACD thresholds: Add RSI filter
VWAP: Add confirmation candle
Stop Loss: 1.0% → 1.5%
Take Profit: 2.0% → 3.0%
```

#### Intraday
```
ADX: >25 → >15
Stochastic: 20/80 → 30/70
Add volume confirmation
```

### 4.2 ML Model Improvements

1. **Add Features:**
   - Candle pattern recognition
   - Time-of-day features
   - Market session indicators
   - News sentiment (if available)

2. **Model Tuning:**
   - Try XGBoost instead of Random Forest
   - Add feature selection
   - Implement ensemble methods

3. **Signal Filtering:**
   - Only trade when ML confidence > 60%
   - Add market regime filter
   - Implement position sizing based on confidence

### 4.3 Risk Management

1. **Position Sizing**
   - Kelly Criterion for dynamic sizing
   - Volatility-adjusted position size
   - Maximum portfolio exposure limits

2. **Stop Loss Logic**
   - Time-based stops
   - Trailing stops for winners
   - Volatility-based stops (ATR)

3. **Take Profit Logic**
   - Partial profit taking at 1x risk
   - Move stop to breakeven after 1x reward
   - Let winners run with trailing stop

---

## 5. Implementation Guide

### 5.1 Daily Workflow

```
PRE-MARKET (Before 9:30 AM EST)
├── Review overnight news
├── Check major market indices
├── Identify key support/resistance levels
└── Set alert levels

TRADING HOURS (9:30 AM - 4:00 PM EST)
├── Monitor for entry signals
├── Execute trades per playbook
├── Track open positions
├── Adjust stops as needed
└── Log all trading activity

POST-MARKET (After 4:00 PM EST)
├── Review trade log
├── Calculate daily P&L
├── Update performance metrics
└── Identify improvement areas
```

### 5.2 Entry Execution Checklist

- [ ] Market session is active
- [ ] Spread is acceptable (<1 tick)
- [ ] Signal meets all criteria
- [ ] Risk per trade < 2%
- [ ] Daily trade limit not reached
- [ ] No major news events pending

### 5.3 Exit Execution Checklist

- [ ] Stop loss hit OR
- [ ] Take profit hit OR
- [ ] Time limit reached OR
- [ ] Opposite signal generated
- [ ] Risk/reward no longer favorable

---

## 6. Trade Journal Template

```yaml
Trade ID: [Date]-[Sequence]
Date: YYYY-MM-DD
Time: HH:MM EST
Strategy: [Scalping/Day/Intraday]
Direction: [Long/Short]
Entry Price: XXXX.XX
Stop Loss: XXXX.XX
Take Profit: XXXX.XX
Position Size: X%
Reason: [Signal description]
Market Conditions: [Trend/Range/Volatility]

Exit:
  Time: HH:MM
  Price: XXXX.XX
  Result: [Win/Loss/Breakeven]
  P&L: $XXX.XX
  P&L %: X%

Lessons Learned: [Notes]
```

---

## 7. Performance Tracking

### Weekly Review
- Total trades and win rate
- Best and worst strategy
- Drawdown analysis
- Signal accuracy by market condition

### Monthly Review
- Strategy comparison
- Performance vs benchmark
- Parameter adjustment recommendations
- ML model performance

### Quarterly Review
- Full strategy reevaluation
- Market regime analysis
- Risk management review
- Production readiness assessment

---

## 8. Risk Disclosures

### Known Limitations

1. **Historical Performance ≠ Future Results**
   - Backtesting shows past performance
   - Market conditions change
   - No guarantee of future profitability

2. **Overfitting Risk**
   - Parameters tuned on limited data
   - May not generalize to new data
   - Requires ongoing monitoring

3. **Market Regime Changes**
   - Strategy optimized for specific conditions
   - Regime shifts can cause losses
   - Need for adaptive strategies

### Risk Controls

| Control | Trigger | Action |
|---------|---------|--------|
| Max Daily Loss | -3% | Stop trading |
| Max Weekly Loss | -5% | Review strategy |
| Max Drawdown | -10% | Pause system |
| Consecutive Losses | 5 | Reduce position size |

---

## 9. Appendix: Technical Details

### A. Indicator Calculations

**RSI(7):**
```
Gain = Close - Close[1] (if positive)
Loss = Close[1] - Close (if positive)
Avg Gain = SMA(Gain, 7)
Avg Loss = SMA(Loss, 7)
RS = Avg Gain / Avg Loss
RSI = 100 - (100 / (1 + RS))
```

**EMA:**
```
EMA = Close * k + EMA[1] * (1 - k)
k = 2 / (period + 1)
```

**MACD:**
```
Fast EMA = EMA(Close, 12)
Slow EMA = EMA(Close, 26)
MACD = Fast EMA - Slow EMA
Signal = EMA(MACD, 9)
Histogram = MACD - Signal
```

### B. ML Feature Engineering

```python
Features:
- price_change: Close.pct_change()
- price_change_5: Close.pct_change(5)
- volume_change: Volume.pct_change()
- volume_ma_ratio: Volume / Volume.rolling(20).mean()
- rsi_7: RSI(7)
- macd: MACD value
- adx: ADX value

Target:
- next_direction: 1 if next_close > current_close else 0
```

### C. Backtest Parameters

```python
Initial Capital: $10,000
Stop Loss (Scalping): 0.5%
Take Profit (Scalping): 1.5%
Stop Loss (Day/Intraday): 1.0%
Take Profit (Day/Intraday): 2.0%
Max Daily Trades (Scalping): 10
Max Daily Trades (Day): 5
Max Daily Trades (Intraday): 3
Transaction Cost: 0 (simulated)
Slippage: 0 (simulated)
```

---

**Document Version:** 1.0  
**Created:** 2025-05-13  
**Test Period:** July - September 2025  
**Data Source:** NASDAQ Historical Data (TrueAlgo)  
**Status:** Proof of Concept

---

*This playbook is for educational and informational purposes only. Trading involves substantial risk of loss. Past performance does not guarantee future results.*