# Trading Dashboard v1.1 — Council Review (Exported)

Exported at: 2026-05-15T14:30:39.043+03:00

Overall verdict: **Not trader-safe yet** due to technical-indicator corruption and financial-labeling inconsistencies.

| Aspect | Score | Deep finding |
|---|---:|---|
| **Header** | 4/10 | Instrument spec mismatch: labeled **NQ E-mini** while showing **$2/point** contract size, which can mislead risk sizing. |
| **Strategy logic** | 6.3/10 | Entry logic is internally consistent for shown longs, but SL rule (-0.6%) is breached on multiple trades (e.g., -1.14%, -0.72%). Short rules exist but zero short executions. |
| **Shapes / visual encoding** | 5/10 | Color semantics are mixed (entry color = direction, exit color = P/L), and TP/SL reason text uses same orange style, reducing interpretation quality. |
| **Results summary** | 5/10 | Core displayed totals are internally coherent, but narrative claims (“after fees”) conflict with actual arithmetic basis. |
| **Financial sense** | 4.5/10 | Strong base metric math (win rate, PF, avg win/loss) but labeling/meaning errors around gross vs net and fee treatment. |
| **Profitability trueness** | 4/10 | Displayed “Net Profit” **$350.84** is pre-fee; true after-fee net is **$280.84**. Final capital should be **$10,280.84**, not **$10,350.84**. |
| **Price chart** | 4/10 | Main panel is line+EMA, not candlestick/OHLC; markers plotted at candle open instead of exact entry/exit prices (misplacement risk). |
| **RSI chart** | 1/10 | RSI series is effectively broken: constant 50 across dataset, so oscillator provides no real signal validation. |
| **Volume chart** | 6/10 | Rendering is structurally fine; “volume spike” thresholding appears too lenient in playbook context. |
| **Performance matrix** | 2/10 | No clear dedicated performance-matrix module found in v1.1 asset, so matrix-level validation cannot be fully performed. |
| **Trades panel** | 7/10 | Trade list, reasons, and timestamps mostly align with logs/data; outcome styling is clear; execution-rule adherence remains the issue. |
| **Analysis tab** | 6/10 | Useful KPIs present, but duplicated “Total Fees” and missing explicit fee-adjusted variants for key metrics reduce trust. |
| **Playbook** | 5/10 | Good structure, but includes unvalidated short-side guidance and ambiguous “realized R/R vs target” framing; contract-spec inconsistency is critical. |
| **Logs** | 6/10 | Chronology and trade linkage are good; missing timezone context and no explicit slippage/gap annotation when SL is overshot. |
| **Insights** | 4/10 | Most misleading section: “net profit after fees: $350.84,” which contradicts trade+fee arithmetic. |

## Collective consolidated diagnosis

1. **Critical technical integrity break:** RSI and EMA inputs are corrupted/non-informative, invalidating indicator confidence.
2. **Critical financial truth issue:** “Net after fees” and final-capital messaging are overstated by **$70**.
3. **Execution realism gap:** SL overshoots are present without clear slippage/gap handling model.
4. **Operational risk communication gap:** instrument specification inconsistency can cause wrong position sizing.

## Blocking fixes before trusting v1.1

1. Recompute and repopulate **RSI(5), EMA(5), EMA(15)** from price closes.
2. Correct fee-adjusted metrics/labels: net PnL, final capital, return %, EV (after fees).
3. Fix instrument metadata (NQ vs MNQ contract economics) and reflect it consistently in playbook/header.
4. Plot trade markers at true **entry_price/exit_price**, add SL/TP threshold overlays, and document slippage behavior when SL is exceeded.
