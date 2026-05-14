import pandas as pd
import numpy as np


def calculate_rsi(df: pd.DataFrame, period: int = 7) -> pd.DataFrame:
    """Calculate RSI indicator."""
    df = df.copy()
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df[f'rsi_{period}'] = 100 - (100 / (1 + rs))
    return df


def calculate_ema(df: pd.DataFrame, periods: list = None) -> pd.DataFrame:
    """Calculate EMA indicators."""
    if periods is None:
        periods = [5, 20]
    df = df.copy()
    for period in periods:
        df[f'ema_{period}'] = df['Close'].ewm(span=period, adjust=False).mean()
    return df


def calculate_volume_spike(df: pd.DataFrame, threshold: float = 2.0) -> pd.DataFrame:
    """Calculate volume spike detection."""
    df = df.copy()
    df['volume_ma'] = df['Volume'].rolling(20).mean()
    df['volume_spike'] = df['Volume'] > (df['volume_ma'] * threshold)
    return df


def calculate_scalping_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate all scalping indicators (RSI, EMA, Volume)."""
    df = calculate_rsi(df, 7)
    df = calculate_ema(df, [5, 20])
    df = calculate_volume_spike(df)
    return df