File: src/signals/ml_filter.py
Relative path: src/signals/ml_filter.py
High-level overview:
- ML-based filter that trains a RandomForest to predict which rule-based signals to keep.
Purpose:
- Reduce low-quality signals by filtering using ML confidence; improves realized performance in backtests.
Key functions/sections:
- train_ml_filter(X_train, y_train)
- apply_ml_filter(model, df_features)
Notes:
- Uses RandomForest; ensure train/test split prevents leakage
Related files:
- src/signals/base_signals.py, src/data/splitter.py, tests/test_ultimate_dashboard.py
Academic appendix:
- Rationale for RandomForest, feature importance interpretation, and cross-validation strategy.
