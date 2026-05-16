File: live_dashboard.py
Relative path: live_dashboard.py
High-level overview:
- Creates a live/near-real-time dashboard artifact for streaming or demo data.
Purpose:
- Visualize ongoing trades and equity curves for manual or simulated live trading.
Key functions/sections:
- Data ingestion for demo/live streams and HTML generation
Inputs/outputs:
- Inputs: demo JSONs under demo/live-demo/ and CSVs; Outputs: live_trading_dashboard.html
Related files:
- demo/live-demo/*, docs/live_trading_dashboard.html
Notes:
- TODO: document refresh cadence and data format expectations.
Academic notes:
- Discuss visualization choices and latency implications.
