File: main.py
Relative path: main.py
High-level overview:
- Multi-strategy comparison entrypoint. Loads data, prepares strategy variants (scalping/day/intraday), and executes comparisons.
Purpose:
- Provide CLI entry to run experiments and compare outputs across configurations.
Key functions/sections:
- main(): parses args and orchestrates strategy runs
Inputs/outputs:
- Inputs: CSVs, optional flags; Outputs: summary tables, console output, optional dashboard artifacts
Related files:
- ultimate_dashboard.py, src/data/loader.py, src/indicators/*
Tests referencing this file:
- none specific; integration tests may invoke main.py
Notes / TODOs:
- Add usage examples, CLI flags, and expected outputs section.
Academic notes:
- Discuss experimental setup and train/test split assumptions.
