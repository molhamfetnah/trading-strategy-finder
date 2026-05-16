File: parameter_optimizer.py
Relative path: parameter_optimizer.py
High-level overview:
- Script for parameter search and optimization across strategy hyperparameters.
Purpose:
- Find performant parameter sets for indicators and backtest rules via grid/random search.
Key functions/sections:
- Parameter search loops, evaluation metric aggregation, config export to best_config.txt
Inputs/outputs:
- Inputs: strategy config ranges; Outputs: best_config.txt, performance summaries
Related files:
- fast_optimizer.py, src/backtest/engine.py
Notes:
- TODO: document algorithm (grid vs random vs Bayesian) and reproducibility seeds.
Academic notes:
- Describe overfitting risks, walk-forward validation, and metric selection.
