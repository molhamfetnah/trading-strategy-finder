# NQ Futures Trading Strategy Finder

> **⚠️ DEVELOPMENT BRANCH** - `test-sample-last-week`
> This is where new development happens. For stable version, see `test-sample-last-three-months`.

## Branch Strategy

| Branch | Purpose | Status |
|--------|---------|--------|
| `test-sample-last-three-months` | Frozen v1.0.0 - Production ready | **Stable** |
| `test-sample-last-week` | Active development for new version | **In Development** |

## Working with Branches

```bash
# View all branches
git branch -a

# Switch to stable version
git checkout test-sample-last-three-months

# Switch to development
git checkout test-sample-last-week

# Compare stable vs development
git diff test-sample-last-three-months..test-sample-last-week
```

## Current Status

| Branch | Version | Data Period | Status |
|--------|---------|-------------|--------|
| `test-sample-last-three-months` | v1.0.0 | Jul-Sep 2025 | **Frozen** |
| `test-sample-last-week` | develop | TBD | **In Development** |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate dashboard
python3 ultimate_dashboard.py
```

## Documentation

- [v1.0.0 Frozen Details](docs/V1-FROZEN.md)
- [Complete Documentation](docs/COMPLETE-DOCUMENTATION.md)
- [Trading Playbook](docs/PLAYBOOK.md)