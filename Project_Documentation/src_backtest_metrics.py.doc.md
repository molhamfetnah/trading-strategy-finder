File: src/backtest/metrics.py
Relative path: src/backtest/metrics.py
High-level overview:
- Functions to summarize backtest outputs: net profit, drawdown, sharpe, win-rate, expectancy.
Purpose:
- Produce standardized metrics used by dashboard and reporting.
Key functions/sections:
- calculate_metrics(trades, equity_curve)
Inputs/outputs:
- Inputs: trade list, equity series; Outputs: dict of metrics
Academic notes:
- Definitions and formulas for metrics (Sharpe, max drawdown), sample-size caveats.
Related files:
- src/backtest/engine.py, ultimate_dashboard.py, docs/dashboard_data.json
