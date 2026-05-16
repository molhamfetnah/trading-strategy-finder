File: tests/test_indicators.py
Relative path: tests/test_indicators.py
High-level overview:
- Unit tests for indicator calculations (RSI, EMA defaults). Updated to match rsi_5 and ema_15 defaults.
Purpose:
- Ensure indicator implementations produce expected column names and sample values.
Related files:
- src/indicators/scalping.py
Notes:
- Contains small numeric assertions; ensure deterministic environment (numpy/pandas versions).
