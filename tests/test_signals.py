import os
import sys
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data.loader import load_data
from src.data.splitter import filter_2025
from src.indicators.scalping import calculate_scalping_indicators
from src.indicators.day_trading import calculate_day_trading_indicators
from src.indicators.intraday import calculate_intraday_indicators
from src.signals.base_signals import (
    generate_scalping_signals,
    generate_day_trading_signals,
    generate_intraday_signals
)
from src.signals.ml_filter import train_ml_filter, apply_ml_filter, add_ml_features


def test_scalping_signals():
    df = load_data('1min.csv')
    df = filter_2025(df.head(500))
    df = calculate_scalping_indicators(df)
    df = generate_scalping_signals(df)
    assert 'signal' in df.columns
    assert df['signal'].isin([0, 1, -1]).all()


def test_day_trading_signals():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_day_trading_indicators(df)
    df = generate_day_trading_signals(df)
    assert 'signal' in df.columns
    assert df['signal'].isin([0, 1, -1]).all()


def test_intraday_signals():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_intraday_indicators(df)
    df = generate_intraday_signals(df)
    assert 'signal' in df.columns
    assert df['signal'].isin([0, 1, -1]).all()


def test_ml_filter():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_day_trading_indicators(df)
    df = generate_day_trading_signals(df)
    df = add_ml_features(df)
    ml_data = train_ml_filter(df)
    if ml_data:
        df_test = apply_ml_filter(df, ml_data)
        assert 'ml_signal' in df_test.columns