File: src/data/resampler.py
Relative path: src/data/resampler.py
High-level overview:
- Utilities to resample tick/1-min data to higher timeframes (e.g., 15-min) and aggregate OHLCV.
Purpose:
- Provide consistent timeframe inputs for strategy indicators and backtests.
Key functions/sections:
- resample_to_interval(df, interval)
Notes:
- Preserve volume aggregation and timestamp alignment (label by period end vs start)
Academic notes:
- Explain effects of resampling on indicator signals and lookahead risk.
Related files:
- src/indicators/*, ultimate_dashboard.py
