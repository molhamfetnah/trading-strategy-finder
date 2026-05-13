import os
import sys
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data.loader import load_data
from src.data.splitter import filter_2025, split_train_test


def test_load_1min_data():
    df = load_data('1min.csv')
    assert 'Date' in df.columns
    assert 'Open' in df.columns
    assert len(df) > 0


def test_load_15min_data():
    df = load_data('NQ_15min_processed.csv')
    assert 'open' in df.columns
    assert 'high' in df.columns


def test_filter_2025_data():
    df = load_data('1min.csv')
    df_2025 = filter_2025(df)
    assert df_2025['Date'].min() >= pd.Timestamp('2025-01-01')
    assert df_2025['Date'].max() <= pd.Timestamp('2025-09-30')


def test_split_train_test():
    df = load_data('1min.csv')
    df_2025 = filter_2025(df)
    train, test = split_train_test(df_2025, '2025-06-30')
    assert train['Date'].max() <= pd.Timestamp('2025-06-30')
    assert test['Date'].min() >= pd.Timestamp('2025-07-01')