File: ultimate_dashboard.py
Relative path: ultimate_dashboard.py
High-level overview:
- Orchestrates data loading, resampling, indicator calculation, ML filtering, backtests, and HTML dashboard generation.
Purpose:
- Produce the final dashboard artifacts (docs/dashboard_data.json and docs/ultimate_trading_dashboard.html) and run experiments across multiple strategies.
Key functions/sections:
- run_backtest_15min(...): backtest runner for 15-min strategies (contract-sized PnL support)
- apply_rsi_entry_filters(...): symmetric RSI-based entry filtering helper
- HTML template & generate_html(): builds dashboard HTML and writes to docs/
Inputs/outputs:
- Inputs: CSV data files (e.g., NQ_15min_processed.csv), config params
- Outputs: docs/dashboard_data.json, docs/ultimate_trading_dashboard.html
Notes / TODOs:
- TODO: add line-by-line explanation and academic rationale for indicator choices.
Related files:
- src/data/loader.py, src/indicators/scalping.py, src/signals/ml_filter.py, src/backtest/engine.py
Tests referencing this file:
- tests/test_ultimate_dashboard.py
Academic/technical appendix:
- TODO: describe RSI theory, contract PnL math, ML-filter rationale, and sampling assumptions.
