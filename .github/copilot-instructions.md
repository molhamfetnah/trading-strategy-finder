# Copilot Instructions for `trading-strategy-finder`

## Build, test, and lint

This repository is Python-based and does not define a dedicated build step.

```bash
# Install dependencies
pip install -r requirements.txt

# Run main strategy comparison
python3 main.py

# Generate the dashboard artifacts (docs/dashboard_data.json + HTML output)
python3 ultimate_dashboard.py

# Run full test suite
pytest tests/ -v

# Run one test module
pytest tests/test_indicators.py -v

# Run a single test
pytest tests/test_indicators.py::test_calculate_rsi -v
```

No project-specific lint command (ruff/flake8/black/mypy) is currently configured in the repo.

## High-level architecture

The core pipeline is:

1. **Data ingestion and normalization** (`src/data/loader.py`)  
   CSV columns are normalized so downstream modules can rely on standard OHLCV names.
2. **Time filtering and split** (`src/data/splitter.py`)  
   Data is constrained to 2025 and split into train/test sets.
3. **Indicators** (`src/indicators/*`)  
   Strategy-specific technical indicators are added to DataFrames.
4. **Signal generation** (`src/signals/base_signals.py`)  
   Rule-based signals are produced using `1` (long), `-1` (short), `0` (hold).
5. **ML filtering** (`src/signals/ml_filter.py`)  
   RandomForest is trained and used to suppress weak rule-based signals.
6. **Backtesting and metrics** (`src/backtest/engine.py`, `src/backtest/metrics.py`)  
   Trades are simulated with stop-loss/take-profit, slippage, fees, then summarized.
7. **Reporting/dashboard output** (`src/dashboard/*`, `main.py`, `ultimate_dashboard.py`)  
   Strategy comparison reports and dashboard data/HTML are generated for analysis.

`main.py` is the multi-strategy comparison entrypoint. `ultimate_dashboard.py` is the richer dashboard workflow and writes outputs into `docs/`.

## Key codebase conventions

- **Canonical dataframe schema:** downstream logic expects normalized names (`Open`, `High`, `Low`, `Close`, `Volume`, plus `Date`/`Time` or `timestamps`). Reuse `load_data()` for any new ingestion path.
- **Copy-before-mutate pattern:** indicator/signal/data functions typically call `df.copy()` and return a new DataFrame instead of mutating caller state in-place.
- **Signal/trade contracts are stable across modules:** signals use `{-1, 0, 1}` and backtest trade dicts use keys like `entry_idx`, `exit_idx`, `direction`, `profit_dollars`, `capital_after`, `exit_reason`, `fees_paid`.
- **Chronological ordering matters for backtests:** workflows that start from descending CSV data reverse to ascending order before simulation (see scalping path in `main.py`).
- **Date-window assumptions are baked in:** helpers and scripts are tuned to 2025 data with train/test split around `2025-06-30`; preserve that unless intentionally changing experiment scope.
- **ML-filter execution detail:** `run_backtest()` reads `signal` first; when applying ML output, ensure the DataFrame passed to backtest uses the filtered signal column as the active signal source.
- **Tests rely on repo-root execution context:** tests use relative CSV paths (`1min.csv`, `NQ_15min_processed.csv`) and `sys.path` injection, so run pytest from the repository root.
