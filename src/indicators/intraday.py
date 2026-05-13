import pandas as pd
import numpy as np


def calculate_supertrend(df: pd.DataFrame, period: int = 10, multiplier: float = 3.0) -> pd.DataFrame:
    """Calculate Supertrend indicator."""
    df = df.copy()
    
    tr = pd.concat([
        df['High'] - df['Low'],
        abs(df['High'] - df['Close'].shift()),
        abs(df['Low'] - df['Close'].shift())
    ], axis=1).max(axis=1)
    
    atr = tr.rolling(window=period).mean()
    
    hl2 = (df['High'] + df['Low']) / 2
    upper_band = hl2 + (multiplier * atr)
    lower_band = hl2 - (multiplier * atr)
    
    df['supertrend'] = atr
    df['supertrend_direction'] = 0
    
    in_uptrend = True
    for i in range(period, len(df)):
        if df['Close'].iloc[i] > upper_band.iloc[i]:
            in_uptrend = True
            df.iloc[i, df.columns.get_loc('supertrend_direction')] = 1
        elif df['Close'].iloc[i] < lower_band.iloc[i]:
            in_uptrend = False
            df.iloc[i, df.columns.get_loc('supertrend_direction')] = -1
        else:
            df.iloc[i, df.columns.get_loc('supertrend_direction')] = df.iloc[i-1, df.columns.get_loc('supertrend_direction')]
    
    return df


def calculate_adx(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Calculate ADX indicator."""
    df = df.copy()
    
    high_diff = df['High'].diff()
    low_diff = -df['Low'].diff()
    
    plus_dm = high_diff.where((high_diff > low_diff) & (high_diff > 0), 0)
    minus_dm = low_diff.where((low_diff > high_diff) & (low_diff > 0), 0)
    
    tr = pd.concat([
        df['High'] - df['Low'],
        abs(df['High'] - df['Close'].shift()),
        abs(df['Low'] - df['Close'].shift())
    ], axis=1).max(axis=1)
    
    atr = tr.rolling(window=period).mean()
    
    plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr)
    
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    df['adx'] = dx.rolling(window=period).mean()
    df['adx_plus'] = plus_di
    df['adx_minus'] = minus_di
    
    return df


def calculate_stochastic(df: pd.DataFrame, k: int = 14, d: int = 3) -> pd.DataFrame:
    """Calculate Stochastic indicator."""
    df = df.copy()
    
    lowest_low = df['Low'].rolling(window=k).min()
    highest_high = df['High'].rolling(window=k).max()
    
    df['stoch_k'] = 100 * ((df['Close'] - lowest_low) / (highest_high - lowest_low))
    df['stoch_d'] = df['stoch_k'].rolling(window=d).mean()
    
    return df


def calculate_intraday_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate all intraday/swing indicators (Supertrend, ADX, Stochastic)."""
    df = calculate_supertrend(df)
    df = calculate_adx(df)
    df = calculate_stochastic(df)
    return df