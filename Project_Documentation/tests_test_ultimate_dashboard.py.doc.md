File: tests/test_ultimate_dashboard.py
Relative path: tests/test_ultimate_dashboard.py
High-level overview:
- Regression tests validating: RSI filtering behavior, duplicate metric removal, and NQ point-value PnL correctness.
Purpose:
- Prevent regressions for fixes described in COUNCIL_REPORT-round3.md and report-revision4.md
Key asserts:
- Filtered signals behave symmetrically for long/short
- Dashboard HTML contains a single 'Total Fees' box
- PnL dollars for a simple trade equals points_moved * point_value - fees
Related files:
- ultimate_dashboard.py, src/backtest/engine.py, src/signals/ml_filter.py
Notes:
- Tests are run with pytest from repo root.
