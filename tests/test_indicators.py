import os
import sys
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data.loader import load_data
from src.data.splitter import filter_2025
from src.indicators.scalping import calculate_rsi, calculate_ema, calculate_volume_spike, calculate_scalping_indicators
from src.indicators.day_trading import calculate_macd, calculate_vwap, calculate_atr, calculate_day_trading_indicators
from src.indicators.intraday import calculate_supertrend, calculate_adx, calculate_stochastic, calculate_intraday_indicators


def test_calculate_rsi():
    df = load_data('1min.csv')
    df = filter_2025(df.head(100))  # Use small sample
    df = calculate_rsi(df, period=7)
    assert 'rsi_7' in df.columns


def test_calculate_ema():
    df = load_data('1min.csv')
    df = filter_2025(df.head(100))
    df = calculate_ema(df, periods=[5, 20])
    assert 'ema_5' in df.columns
    assert 'ema_20' in df.columns


def test_volume_spike():
    df = load_data('1min.csv')
    df = filter_2025(df.head(100))
    df = calculate_volume_spike(df)
    assert 'volume_spike' in df.columns


def test_calculate_scalping_indicators():
    df = load_data('1min.csv')
    df = filter_2025(df.head(100))
    df = calculate_scalping_indicators(df)
    assert 'rsi_7' in df.columns
    assert 'ema_5' in df.columns
    assert 'ema_20' in df.columns
    assert 'volume_spike' in df.columns


def test_calculate_macd():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_macd(df)
    assert 'macd' in df.columns
    assert 'macd_signal' in df.columns


def test_calculate_vwap():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_vwap(df)
    assert 'vwap' in df.columns


def test_calculate_atr():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_atr(df)
    assert 'atr' in df.columns


def test_calculate_day_trading_indicators():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_day_trading_indicators(df)
    assert 'macd' in df.columns
    assert 'macd_signal' in df.columns
    assert 'vwap' in df.columns
    assert 'atr' in df.columns


def test_calculate_supertrend():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_supertrend(df)
    assert 'supertrend' in df.columns
    assert 'supertrend_direction' in df.columns


def test_calculate_adx():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_adx(df)
    assert 'adx' in df.columns


def test_calculate_stochastic():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_stochastic(df)
    assert 'stoch_k' in df.columns
    assert 'stoch_d' in df.columns


def test_calculate_intraday_indicators():
    df = load_data('NQ_15min_processed.csv')
    df = calculate_intraday_indicators(df)
    assert 'supertrend' in df.columns
    assert 'supertrend_direction' in df.columns
    assert 'adx' in df.columns
    assert 'stoch_k' in df.columns
    assert 'stoch_d' in df.columns