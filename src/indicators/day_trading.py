import pandas as pd
import numpy as np


def calculate_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """Calculate MACD indicator."""
    df = df.copy()
    ema_fast = df['Close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['Close'].ewm(span=slow, adjust=False).mean()
    df['macd'] = ema_fast - ema_slow
    df['macd_signal'] = df['macd'].ewm(span=signal, adjust=False).mean()
    df['macd_hist'] = df['macd'] - df['macd_signal']
    return df


def calculate_vwap(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate VWAP indicator."""
    df = df.copy()
    typical_price = (df['High'] + df['Low'] + df['Close']) / 3
    cumulative_tp_volume = (typical_price * df['Volume']).cumsum()
    cumulative_volume = df['Volume'].cumsum()
    df['vwap'] = cumulative_tp_volume / cumulative_volume
    return df


def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Calculate ATR indicator."""
    df = df.copy()
    high_low = df['High'] - df['Low']
    high_close = abs(df['High'] - df['Close'].shift())
    low_close = abs(df['Low'] - df['Close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['atr'] = tr.rolling(window=period).mean()
    return df


def calculate_day_trading_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate all day trading indicators (MACD, VWAP, ATR)."""
    df = calculate_macd(df)
    df = calculate_vwap(df)
    df = calculate_atr(df)
    return df