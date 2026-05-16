File: fast_optimizer.py
Relative path: fast_optimizer.py
High-level overview:
- Performance-optimized parameter search for quick iteration and testing.
Purpose:
- Faster but potentially less exhaustive search than parameter_optimizer.py
Key functions/sections:
- Parallel evaluation helpers, caching of results, lightweight scoring
Inputs/outputs:
- Inputs: parameter ranges; Outputs: best parameter candidates
Related files:
- parameter_optimizer.py, src/backtest/engine.py
Academic notes:
- Notes on parallelism, sampling bias, and reproducibility.
