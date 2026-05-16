File: src/data/loader.py
Relative path: src/data/loader.py
High-level overview:
- Data ingestion and normalization utilities. Loads CSVs and normalizes column names to canonical OHLCV schema.
Purpose:
- Ensure downstream modules can rely on consistent DataFrame schema.
Key functions/sections:
- load_data(path, tz=None): returns DataFrame with columns Date, Open, High, Low, Close, Volume
Notes:
- Some CSVs arrive in descending order; scalping path reverses to ascending before backtest.
Related files:
- src/data/splitter.py, ultimate_dashboard.py
Academic notes:
- Describe timestamp handling, timezone assumptions, and resampling rationale.
