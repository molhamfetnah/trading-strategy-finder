File: src/data/splitter.py
Relative path: src/data/splitter.py
High-level overview:
- Time-window filtering and train/test splitting helpers.
Purpose:
- Constrain experiments to 2025 windows and split historical data for ML training vs evaluation.
Key functions/sections:
- train_test_split_by_date(df, split_date)
Related files:
- src/data/loader.py, src/signals/ml_filter.py
Academic notes:
- Discuss leakage prevention, stationarity assumptions, and recommended split strategies.
