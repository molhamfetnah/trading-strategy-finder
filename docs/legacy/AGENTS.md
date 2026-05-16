# AGENTS.md - Trading Strategy Finder

## Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run main strategy comparison
python3 main.py

# Generate dashboard (outputs to docs/)
python3 ultimate_dashboard.py

# Run all tests
pytest tests/ -v

# Run one test file
pytest tests/test_indicators.py -v

# Run single test
pytest tests/test_indicators.py::test_calculate_rsi -v
```

## Architecture

Pipeline flow: `src/data/loader.py` → `src/data/splitter.py` → `src/indicators/*` → `src/signals/base_signals.py` → `src/signals/ml_filter.py` → `src/backtest/engine.py` → `src/dashboard/*`

- `main.py`: Multi-strategy comparison (scalping, day trading, intraday)
- `ultimate_dashboard.py`: Rich dashboard with HTML output to `docs/`

## Key Conventions

- **Canonical dataframe schema**: Uses normalized OHLCV columns (`Open`, `High`, `Low`, `Close`, `Volume`, plus `Date`/`Time` or `timestamps`). Always use `load_data()` from `src/data/loader.py` for new ingestion paths.
- **Copy-before-mutate**: Indicator/signal functions return new DataFrames, don't mutate in-place.
- **Signal values**: `-1` (short), `0` (hold), `1` (long).
- **Trade dict keys**: `entry_idx`, `exit_idx`, `direction`, `profit_dollars`, `capital_after`, `exit_reason`, `fees_paid`.
- **Date-window**: Tuned for 2025 data with train/test split around `2025-06-30`.
- **Chronological order matters**: Scalping path reverses descending CSV data to ascending order before backtest (see `main.py:42`).

## Testing

- Tests run from repo root with relative CSV paths (`1min.csv`, `NQ_15min_processed.csv`).
- No lint/typecheck tooling configured.

## Important Gotchas

- ML filter: When applying ML output, ensure the DataFrame passed to backtest uses the **filtered signal column** as the active signal source, not the raw rule-based signal.
- Data loading: 1min.csv loads in descending order (newest first) — must reverse for backtest.
- Output artifacts go to `docs/` directory (dashboard HTML, JSON data).