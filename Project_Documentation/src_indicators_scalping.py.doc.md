File: src/indicators/scalping.py
Relative path: src/indicators/scalping.py
High-level overview:
- Indicator implementations used by scalping strategy: RSI short windows, EMAs, ATR-based filters.
Purpose:
- Compute feature columns consumed by rule-based signals and ML filters.
Key functions/sections:
- calculate_scalping_indicators(df, rsi_window=5, ema_window=15)
Notes:
- Function returns a copy of df with new columns (copy-before-mutate pattern)
Academic appendix:
- RSI formula, EMA smoothing math, ATR computation and why chosen for scalping.
Related files:
- src/signals/base_signals.py, tests/test_indicators.py
