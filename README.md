# NASDAQ Trading Strategy Finder

## 📈 Live Demo

**🚀 Live Results Dashboard:** https://molhamfetnah.github.io/trading-strategy-finder/

### Quick Summary

| Metric | Value |
|--------|-------|
| Test Period | July - September 2025 |
| Initial Capital | $10,000 |
| **Final Capital** | **$10,107.66** |
| **Total Profit** | **+$107.66 (1.08%)** |
| Best Strategy | Scalping (1min) |
| Total Trades | 17 |
| Win Rate | 29.4% |
| Profit Factor | 1.17 |

---

## 🎯 Try It Now

```bash
# Run live dashboard
python3 live_dashboard.py

# View interactive demos
open docs/index.html
```

---

## 📊 Strategy Comparison

| Strategy | Trades | Profit | Win Rate | Status |
|----------|--------|--------|----------|--------|
| 🏆 **Scalping** | 17 | +$107.66 | 29.4% | **BEST** |
| Day Trading | 23 | -$719.55 | 26.1% | Failed |
| Intraday | 0 | $0.00 | 0% | No Signals |

---

## 🧠 How It Works

1. **Load Data** → 87,243 price bars from 2025
2. **Calculate Indicators** → RSI, EMA, MACD, Volume
3. **Generate Signals** → Buy/Sell when rules match
4. **ML Filter** → Random Forest enhances signals
5. **Backtest** → Simulate trading with stop loss/take profit
6. **Results** → Profit, win rate, drawdown analysis

---

## 📁 Project Structure

```
trading/
├── src/
│   ├── data/          # Data loading & preprocessing
│   ├── indicators/    # RSI, EMA, MACD, etc.
│   ├── signals/       # Signal generation + ML
│   ├── backtest/      # Trade simulation & metrics
│   └── dashboard/     # Reports & visualization
├── docs/              # GitHub Pages (live demo)
├── demo/live-demo/    # Pre-run demo results
├── tests/             # 29 passing tests
├── main.py            # Main execution
└── live_dashboard.py  # Live demo script
```

---

## 📚 Technical Details

For full technical documentation:
- [docs/PLAYBOOK.md](docs/PLAYBOOK.md) - Trading rules & strategy guide
- [docs/API.md](docs/API.md) - Code reference
- [docs/index.html](docs/index.html) - Live demo dashboard
- [demo/live-demo/](demo/live-demo/) - Demo results & data

---

## 🔧 Setup

```bash
pip install -r requirements.txt
python3 main.py
```

---

## ⚠️ Disclaimer

This is a proof-of-concept. Past performance does not guarantee future results. Always use proper risk management.

---

**Repository:** [github.com/molhamfetnah/trading-strategy-finder](https://github.com/molhamfetnah/trading-strategy-finder)