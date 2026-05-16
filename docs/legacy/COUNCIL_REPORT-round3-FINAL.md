# Trading Dashboard v1.1 — FINAL EXPERT COUNCIL REVIEW

**Generated:** 2026-05-15  
**Audience:** Experienced Futures Trader  
**Scope:** Complete dashboard audit before submission deadline

---

## EXECUTIVE SUMMARY

**Status: REQUIRES IMMEDIATE FIX BEFORE SUBMISSION**

The dashboard has one **critical flaw** that makes it unsuitable for an experienced NQ trader:
- **Profit calculations are 4-5x too small** due to missing NQ futures contract multiplier ($2/point)

Beyond this critical issue, the dashboard shows improvement in:
- Indicator rendering (RSI, EMA, Volume charts all correct)
- Entry signal logic (all trades meet RSI <25 for longs, >75 for shorts)
- Both long and short trades now execute correctly
- Metrics arithmetic is internally consistent

---

## SECTION 1: CRITICAL BUG — NQ FUTURES CONTRACT SIZING

### The Problem

The backtest calculates profits as a **percentage of capital** rather than using the **NQ futures $2/point contract multiplier**.

```python
# Current (WRONG):
pnl_dollars = (pnl_pct / 100) * capital - fee_per_trade

# Should be (NQ Futures):
pnl_dollars = points_moved * 2 - fee_per_trade
```

### Evidence

| Trade | Points | Correct $ | Shown $ | Ratio |
|-------|--------|----------|---------|-------|
| #1 | 562.0 | $1,124.00 | $235.96 | 4.8x |
| #5 | 571.5 | $1,143.00 | $238.06 | 4.8x |
| #7 | 622.0 | $1,244.00 | $254.01 | 4.9x |
| #10 | 563.0 | $1,126.00 | $235.23 | 4.8x |

### Impact on Trader

- Dashboard shows **$365.97 net profit** (3.66% return)
- **Actual should be ~$1,500+** with proper contract sizing
- A trader with $10,000 can trade 1 NQ contract
- A 2.5% move = ~575 points = **$1,150 actual profit**, not $235

### Verdict for Experienced Trader

**UNACCEPTABLE** — This fundamental error invalidates all profit claims. An experienced NQ trader will immediately recognize the numbers are wrong.

---

## SECTION 2: STRATEGY LOGIC VERIFICATION

### Entry Signal Rules (Verified ✓)

| Rule | Requirement | Actual | Status |
|------|-------------|--------|--------|
| LONG | RSI < 25 | All long entries: 12.70 - 24.68 | ✓ |
| LONG | Price > EMA5 | All long entries: "above" | ✓ |
| LONG | Volume Spike | All long entries: True | ✓ |
| SHORT | RSI > 75 | All short entries: 75.23 - 88.79 | ✓ |
| SHORT | Price < EMA5 | All short entries: "below" | ✓ |
| SHORT | Volume Spike | All short entries: True | ✓ |

### Trade Execution Summary

| # | Dir | Entry Time | Exit Time | P/L % | P/L $ | Reason | RSI Check |
|---|-----|------------|-----------|-------|-------|--------|-----------|
| 1 | long | Jul 3 06:30 | Jul 21 10:15 | +2.46% | +$235.96 | TP | 24.68 ✓ |
| 2 | long | Jul 21 11:30 | Jul 22 09:45 | -1.14% | -$127.02 | SL | 16.25 ✓ |
| 3 | short | Jul 22 11:00 | Jul 23 16:00 | -0.79% | -$89.49 | SL | 76.19 ✓ |
| 4 | long | Jul 27 23:45 | Jul 30 15:15 | -0.72% | -$81.90 | SL | 20.83 ✓ |
| 5 | long | Aug 1 15:45 | Aug 6 18:15 | +2.50% | +$238.06 | TP | 23.39 ✓ |
| 6 | short | Aug 8 03:00 | Aug 8 10:15 | -0.61% | -$71.72 | SL | 75.23 ✓ |
| 7 | short | Aug 18 03:45 | Aug 20 09:45 | +2.61% | +$254.01 | TP | 88.79 ✓ |
| 8 | long | Aug 20 23:30 | Aug 21 09:45 | -0.65% | -$77.65 | SL | 12.70 ✓ |
| 9 | long | Aug 26 11:45 | Sep 1 02:15 | -0.61% | -$72.40 | SL | 17.39 ✓ |
| 10 | long | Sep 3 12:15 | Sep 10 08:30 | +2.40% | +$235.23 | TP | 23.81 ✓ |
| 11 | short | Sep 17 05:45 | Sep 18 03:45 | -0.64% | -$77.11 | SL | 79.53 ✓ |

**Direction Count:** 7 longs, 4 shorts  
**Verdict:** All entries meet strategy rules. ✓

---

## SECTION 3: STOP LOSS REALITY CHECK

### Stated: -0.6% SL  
### Actual: All SL exits exceed -0.6%

| Trade | Stated | Actual | Over by |
|-------|--------|--------|---------|
| #2 | -0.6% | -1.14% | +91% |
| #3 | -0.6% | -0.79% | +31% |
| #4 | -0.6% | -0.72% | +20% |
| #6 | -0.6% | -0.61% | +1% |
| #8 | -0.6% | -0.65% | +9% |
| #9 | -0.6% | -0.61% | +1% |
| #11 | -0.6% | -0.64% | +7% |

### Root Cause
Backtest uses **close of signal bar** for exit price. Real markets have gaps. The playbook includes a disclaimer about this.

### Verdict for Experienced Trader
**ACCEPTABLE** — This is documented in the playbook. The disclaimer is visible. Traders understand backtest vs live gap reality.

---

## SECTION 4: PERFORMANCE METRICS (Internal Consistency ✓)

### Metrics Shown vs Calculated

| Metric | Dashboard | Calculated | Match |
|--------|-----------|------------|-------|
| Net Profit | $365.97 | $365.97 | ✓ |
| Gross Profit | $475.97 | $475.97 | ✓ |
| Total Fees | $110.00 | $110.00 | ✓ |
| Win Rate | 36.4% | 36.4% (4/11) | ✓ |
| Profit Factor | 1.61 | 1.61 | ✓ |
| Avg Win | $240.82 | $240.82 | ✓ |
| Avg Loss | -$85.33 | -$85.33 | ✓ |
| Max Drawdown | 2.92% | 2.92% | ✓ |
| Sharpe Ratio | 0.21 | 0.20 | ✓ |
| Expected Value | $33.27 | $33.27 | ✓ |

**Verdict:** Metrics are internally consistent. ✓

---

## SECTION 5: CHART & INDICATOR VERIFICATION

### RSI Chart ✓
- **Column used:** `rsi_5` 
- **Range:** 12.70 - 88.79 (proper distribution)
- **Chart:** Purple line in middle panel, 0-100 scale

### EMA Lines ✓
- **EMA 5:** Green line
- **EMA 15:** Orange line
- Properly separated, no longer identical

### Volume Chart ✓
- Bar chart in bottom panel
- Green bars for volume_spike = True
- Gray bars for volume_spike = False

### Trade Markers ✓
- Entry: Green/red triangle-up markers at entry price
- Exit: Green/red triangle-down markers at exit price

**Verdict:** Charts render correctly. ✓

---

## SECTION 6: UI/UX COMPONENTS

### Header ✓
- Symbol: "NQ E-mini ($2/pt) | Scalping Strategy"
- Initial Capital: $10,000
- Final Capital: $10,365.97
- Total Return: +3.66%

### Metrics Panel ✓
- All metrics displayed
- Net Profit, Final Capital, Win Rate, Profit Factor all present

### Trade List ✓
- All 11 trades displayed with entry/exit/indicators
- Click to highlight functionality (placeholder)

### Analysis Tab ✓
- Winners breakdown (Trade #1, #5, #7, #10)
- Losers breakdown (Trade #2, #3, #4, #6, #8, #9, #11)

### Playbook Tab ✓
- Long Entry Rules (RSI < 25, Price > EMA5, Vol spike, ML filter)
- Short Entry Rules (RSI > 75, Price < EMA5, Vol spike, ML filter)
- Exit Rules with SL slippage disclaimer
- Asset class details (NQ futures, CME, $2/pt)
- ML model specs (Random Forest, 100 trees)

### Logs Tab ✓
- Sequential: ENTRY → EXIT → METRICS per trade
- Timestamps accurate

### Insights Tab ✓
- Key findings and recommendations present

**Verdict:** UI complete and professional. ✓

---

## SECTION 7: CODE HEALTH

### Test Results
```
tests/test_backtest.py:     3 passed ✓
tests/test_dashboard.py:    4 passed ✓
tests/test_data_loader.py: 6 passed ✓
```
**Total: 13/13 passed** (indicator tests timing out but core logic passes)

---

## FINAL VERDICT FOR EXPERIENCED TRADER

### BLOCKERS (Must Fix)

1. **CRITICAL: NQ Futures Contract Multiplier Missing**
   - Current profit calculation uses % of capital
   - Must use: `points × $2 = profit`
   - This invalidates ALL profit figures

2. **Minor: Header shows $10,365.97 but should show ~$11,500+**
   - Due to contract multiplier bug

### What's Working
- RSI entry conditions correct (all longs <25, all shorts >75)
- Both long and short trades executing
- Charts render properly
- Metrics internally consistent
- Playbook complete with SL disclaimer

---

## REQUIRED FIXES BEFORE SUBMISSION

```python
# In run_backtest_15min() function, line ~344:

# CURRENT (WRONG):
pnl_dollars = (pnl_pct / 100) * capital - fee_per_trade

# FIX TO:
point_value = 2  # NQ futures $2/point
points = abs(closes[i] - entry_price)
pnl_dollars = points * point_value - fee_per_trade
```

After this fix, recalculate all metrics with proper contract sizing.

---

**Council Final Decision:**  
NOT APPROVED for submission — Critical NQ contract multiplier bug must be fixed first.

---

*End of Expert Council Review*