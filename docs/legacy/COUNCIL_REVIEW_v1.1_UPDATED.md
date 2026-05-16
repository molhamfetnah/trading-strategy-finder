# Trading Dashboard v1.1 — Updated Intensive Council Review

Generated: 2026-05-15T14:39:59.410+03:00  
Scope: post-fix re-audit (tests + multi-specialist review)

## Executive verdict

**Status: improved, but still not release-safe.**  
The developer fixed major chart-indicator corruption from the prior review, but **financial truth/reporting inconsistencies and core code regressions remain blocking**.

---

## 1) Intensive automated testing

Test suite run: `pytest tests -v`  
Result: **27 passed, 2 failed**

### Failing regression A (High)
- Test: `tests/test_backtest.py::test_calculate_all_metrics`
- Root cause: `calculate_metrics()` returns `net_profit` but not `total_profit`, while tests and runtime paths expect `total_profit`.
- Evidence:
  - `tests/test_backtest.py:48,53`
  - `src/backtest/metrics.py:56-70`
  - `main.py:63,97,130,186`
  - `live_dashboard.py:193-198,302`

### Failing regression B (High)
- Test: `tests/test_signals.py::test_scalping_signals`
- Root cause: default mismatch between indicators and signal generator (`rsi_7` produced vs `rsi_5` consumed by default).
- Evidence:
  - `src/indicators/scalping.py:51` (RSI 7)
  - `src/signals/base_signals.py:5,10,14,20` (expects `rsi_5` by default)
  - `tests/test_signals.py:23-24`

---

## 2) Specialist council scores (post-update)

| Specialist domain | Score | Verdict |
|---|---:|---|
| Strategy logic | 6.4/10 | Trade/log structure improved, but SL realism breaches and long-only validation gap remain. |
| Financial integrity | 4.5/10 | Core arithmetic still mislabeled/misrepresented around fee-adjusted net results. |
| Technical charts/indicators | 7.8/10 | Prior RSI/EMA corruption appears fixed; chart framework now mostly coherent. |
| UX & operations risk | 5.9/10 | Usable layout, but still has misleading narrative and operational clarity gaps. |
| Code health / regression stability | 4.0/10 | Two high-impact test regressions in core metrics/signals pipeline. |

---

## 3) What improved since previous report

1. **Indicator integrity improved significantly**
   - RSI is no longer flatlined; values span proper range.
   - EMA(5) and EMA(15) are no longer identical series.
2. **Trade/log consistency remains strong**
   - Trades, logs, and key chart mappings are largely coherent.
3. **General dashboard structure stayed stable**
   - Header/panels/tabs continue to present the system clearly.

---

## 4) Remaining blockers (must-fix)

1. **Financial truth mismatch (Critical)**
   - Trade sum = **$350.8387**, fees = **$70.00**, true net-after-fees = **$280.8387**.
   - Yet JSON/UI still report `net_profit` and final capital on pre-fee basis:
     - `docs/dashboard_data.json` (`metrics.net_profit=350.8387`, `metrics.final_capital=10350.8387`)
     - `docs/ultimate_trading_dashboard.html:341-347,816` (“Net profit after fees: $350.84”)

2. **Backtest/reporting contract break (High)**
   - `total_profit` key expected broadly but missing from `calculate_metrics` output.

3. **Signal pipeline contract break (High)**
   - RSI period default mismatch causes runtime KeyError in default path.

4. **Strategy execution realism gap (High)**
   - Stated SL `-0.6%` but realized SL exits exceed this materially (e.g., `-1.14%`).
   - Evidence: `docs/ultimate_trading_dashboard.html:640,711,729,765,783`

5. **Evidence-claim mismatch for ML/filter narrative (Medium)**
   - Claims on ML benefit and filtering quality are not backed with transparent per-trade evidence fields.

---

## 5) Priority fix plan

1. Restore API compatibility in metrics:
   - Return both `net_profit` and `total_profit` consistently.
2. Align scalping signal defaults:
   - Use RSI-7 by default or dynamically resolve available RSI column.
3. Correct fee-adjusted reporting:
   - Separate and clearly label gross vs net-after-fees across metrics, header, and insights.
4. Clarify SL model:
   - Either enforce hard SL or explicitly show slippage/gap model.
5. Re-run full test suite and publish only when all pass.

---

## Updated council conclusion

**Dashboard v1.1 is materially better than the previous audited state, especially in indicator/chart data quality, but still fails release readiness due to financial-reporting truth issues and two core code regressions.**
