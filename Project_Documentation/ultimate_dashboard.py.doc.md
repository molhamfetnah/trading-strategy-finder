File: ultimate_dashboard.py
Relative path: ultimate_dashboard.py
One-line purpose:
- Produce the Ultimate Trading Dashboard: compute indicators, filter signals with ML, run contract-sized backtests, and generate JSON + HTML reports for evaluation and interview demos.

Summary (3–5 bullets):
- Pipeline: load 1-min data → time filter → resample to 15-min → compute indicators → generate rule-based signals → train/apply ML filter → apply RSI-entry filters → run per-contract backtest → compute metrics → produce dashboard.
- Backtest measures P/L in dollars per-contract (points_moved * point_value - fees) for NQ ($2/point) to reflect futures economics.
- ML uses a RandomForest to filter weak signals (not to predict exact exit), improving realized win rate.
- Dashboard includes trade-level analysis, logs, insights and a playbook section describing rules and parameters.

API / Key functions (what they do):
- get_indicator_at_idx(df, idx): extract human-friendly snapshot of indicators at a row.
- analyze_trade(df, trade, trade_num): produce per-trade narrative (entry/exit indicators, what went right/wrong).
- get_timestamp_str(df, idx): format row Date/Time into human timestamp.
- generate_logs(trades, df, metrics): produce sequential ENTRY/EXIT/METRICS log events for UI.
- generate_insights(trades, metrics): high-level observations and recommendations derived from metrics.
- prepare_chart_data(df, trades): assemble arrays used by Plotly HTML (prices, EMAs, RSI, volumes, markers).
- prepare_data(df, rsi_period=5): convenience wrapper that computes RSI, EMAs, volume spike and signals.
- add_ml_features(df): feature engineering used by ML filter (price changes, volatility, ema diff, etc.).
- train_ml(df_train, rsi_thresh=25): trains RandomForest on next-candle direction only on rows with signals.
- apply_ml_filter(df, ml_data): uses trained model to zero-out weak signals (keeps signal semantics).
- apply_rsi_entry_filters(signals, rsi_values, oversold=25, overbought=75): enforces symmetric RSI logic for long/short entries.
- resample_15min(df): resample 1-min to 15-min OHLCV preserving Date/Time columns.
- run_backtest_15min(...): simulate trades using signals and per-contract P/L; returns trade list and final capital.
- generate_html(data): create the interactive HTML dashboard and write docs/ultimate_trading_dashboard.html.

Section-by-section (detailed, with rationale):

1) Data loading & resample
- load_data('1min.csv') → filter_2025 → split_train_test: keeps experiments focused to 2025 window.
- Resample: convert 1-min to 15-min using resample_15min. Note the code reverses input ([::-1]) to ensure chronological order when input CSVs are newest-first.
- Rationale: 15-min is chosen to balance noise vs frequency for scalping on NQ; reproducing results requires exact resample logic and timezone handling.

2) Indicator calculations (prepare_data)
- RSI (period=5): short-window momentum to detect oversold/overbought micro-conditions.
- EMA 5 / EMA 15: fast/slow trend filters — crossovers and price vs EMA used for entry direction.
- Volume spike: flag when volume exceeds threshold (1.0 × average) to confirm liquidity-driven moves.
- Pattern: functions return a copy (copy-before-mutate) to avoid in-place surprises in pipelines.

3) Rule-based signals
- generate_scalping_signals produces {-1,0,1} signals based on RSI/EMA/volume rules. Signals are intentionally permissive; downstream ML filter reduces false positives.
- Key invariant: signal column values represent requested entries; backtest assumes immediate entry at next row price.

4) ML filter (train_ml / apply_ml_filter)
- Features: rsi_5, short-term returns, volume ratios, ema_diff, volatility, rsi delta.
- Target: next candle up/down (binary). Training restricts to rows where a rule-based signal existed to teach the model to accept/reject rule signals.
- Model: RandomForest (n_estimators=100, max_depth=10). Chosen for robustness, interpretability (feature importance) and quick training.
- Apply: model predicts probability/direction; conflicting model vs rule signals cause the rule signal to be zeroed (filtering).
- Caveats: training on next-candle direction is a simple proxy — it may introduce lookahead if features include post-entry values. The code mitigates by shifting target and dropping NaNs.

5) RSI entry filter (apply_rsi_entry_filters)
- Symmetric enforcement: longs only if RSI < oversold (default 25), shorts only if RSI > overbought (default 75).
- Reason: initial bug was asymmetrical filtering that suppressed shorts. This restores intended symmetric behavior for both directions.

6) Backtest: run_backtest_15min
- Position lifecycle: enter when signals != 0 and not in position; exit when pnl_pct <= -stop_loss or >= take_profit.
- PnL calculation: uses per-contract math: points_moved * point_value - fee_per_trade. This reflects futures (NQ $2/pt) economics and decouples P/L from capital.
- Capital update: capital += pnl_dollars; trades store capital_after and fees_paid for auditing.
- Assumptions: entries/exits executed at observed candle 'Close' prices; no partial fills; slippage only implicitly via target thresholds.
- Limitations: market gaps (overnight) are not explicitly modelled; spread/slippage beyond fee_per_trade not modelled.

7) Reporting & Dashboard (generate_html)
- Metrics formatting: computes displays with fallbacks (Sharpe N/A if too few trades) and safe stringification.
- Trade analysis: per-trade narratives and classification (what_went_right/wrong) assist interview storytelling.
- Playbook section: documents long/short/exit rules, ML role, parameter table and best-setup notes.

Mathematical / academic appendix (short):
- RSI(5): relative strength index = 100 - 100/(1 + RS) where RS = avg_gain/avg_loss over period. Short periods increase sensitivity; cite: Welles Wilder (1978).
- EMA: exponential moving average with smoothing alpha = 2/(N+1). Faster EMA responds quicker, useful for short-term trend detection.
- ATR/Volatility: std or ATR used to measure dispersion — here volatility = rolling std / rolling mean * 100 to normalize.
- P/L for futures: pnl_dollars = points_moved * point_value - fees. For NQ E-mini, point_value = $2. This is per-contract profit.
- Risk metrics: Sharpe uses daily-equivalent returns; here computed conservatively with minimum trades check.

Testing and reproducibility notes:
- Tests reference indicator defaults and backtest behavior (see tests/test_ultimate_dashboard.py).
- To reproduce: pip install -r requirements.txt; python3 ultimate_dashboard.py (writes docs/dashboard_data.json and docs/ultimate_trading_dashboard.html).
- Use seed (RandomForest random_state=42) for deterministic training results.

Interview talking points (3–6 bullets to memorize):
- Problem: build a repeatable pipeline to evaluate scalping strategies on NQ with realistic per-contract economics.
- Approach: combine human-readable rule-based signals + ML filter to reduce false positives; use contract-sized backtest for economic realism.
- Key fix: corrected asymmetric RSI filter and changed PnL calc to points*point_value for futures — explain why percent-of-capital is misleading for per-contract instruments.
- Results: X trades, Net Profit $Y, Win Rate Z% (point to dashboard numbers and trade examples).
- Limitations & next steps: add slippage model, multi-contract sizing, walk-forward optimization, and live paper-trading integration.

Common interview Q&A (short answers):
- Q: Why use RF instead of logistic regression? A: RF handles nonlinearities, is robust to feature scaling, and gives feature importances for quick analysis.
- Q: Why measure P/L per contract? A: Futures P/L is per-tick/point and independent of capital; percent-of-capital distorts per-contract economics.
- Q: How to avoid overfitting on parameters? A: Use out-of-sample test split, cross-validation, and walk-forward tests; prefer conservative parameter choices.

Cross-references and next reading order:
- src/indicators/scalping.py (indicator math)
- src/signals/ml_filter.py (ML filter code and train/apply patterns)
- src/backtest/engine.py (reference implementation and integration differences)
- tests/test_ultimate_dashboard.py (regressions used to fix bugs)

References / further reading:
- Welles Wilder, 'New Concepts in Technical Trading Systems' (RSI)
- Alexander Elder, 'Trading for a Living' (volume & trend filters)
- Fabozzi et al., 'Quantitative Investment Analysis' (backtest/metrics definitions)

Notes / TODOs:
- Expand per-line commentary for generate_html (large template) on demand.
- Add explicit slippage model and multi-contract sizing helper.

Talking snippets for the demo:
- "This dashboard runs a controlled experiment: the same code computes indicators, filters signals and simulates P/L with per-contract economics — enabling reproducible decisions for live integration."

Tests referencing this file:
- tests/test_ultimate_dashboard.py

Edited-by: Assistant
