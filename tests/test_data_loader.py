import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data.loader import load_data


def test_load_1min_data():
    df = load_data('1min.csv')
    assert 'Date' in df.columns
    assert 'Open' in df.columns
    assert len(df) > 0


def test_load_15min_data():
    df = load_data('NQ_15min_processed.csv')
    assert 'open' in df.columns
    assert 'high' in df.columns