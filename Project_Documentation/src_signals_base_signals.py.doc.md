File: src/signals/base_signals.py
Relative path: src/signals/base_signals.py
High-level overview:
- Rule-based signal generation: converts indicator columns into {-1,0,1} signals using business rules.
Purpose:
- Provide deterministic strategy entry/exit rules used in backtests and ML labeling.
Key functions/sections:
- generate_scalping_signals(df)
- signal post-processing helpers (e.g., cooldowns, signal holding rules)
Related files:
- src/indicators/scalping.py, src/signals/ml_filter.py
Academic notes:
- Explain labeling choices, class imbalance issues, and how rules map to trade execution.
