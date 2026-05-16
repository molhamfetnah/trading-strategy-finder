File: src/backtest/engine.py
Relative path: src/backtest/engine.py
High-level overview:
- Core backtest engine: simulates trades given signals, handles position sizing, stop-loss/take-profit, fees and slippage.
Purpose:
- Turn signals into executed trades and compute per-trade P/L and portfolio evolution.
Key functions/sections:
- run_backtest(...): main simulation loop
- trade execution and exit logic
- position sizing helpers
Inputs/outputs:
- Inputs: DataFrame with OHLCV and signal column; Outputs: list of trade dicts, equity curve
Technical notes:
- Supports both percent-of-capital and per-contract (point-value) PnL models in different contexts. NQ fixed point_value=2.0 assumed in dashboard flows.
Related files:
- src/backtest/metrics.py, ultimate_dashboard.py, src/signals/ml_filter.py
Tests referencing this file:
- tests/test_backtest.py
Academic appendix:
- Explain slippage/fees model, path-dependency, and assumptions on execution (mid-bar vs next-bar fills).
