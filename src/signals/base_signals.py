import pandas as pd
import numpy as np


def generate_scalping_signals(df: pd.DataFrame, rsi_period: int = 5) -> pd.DataFrame:
    """Generate scalping signals based on RSI, EMA, and volume."""
    df = df.copy()
    df['signal'] = 0
    
    rsi_col = f'rsi_{rsi_period}'
    
    long_condition = (
        (df['Close'] > df['ema_5']) &
        (df[rsi_col] < 30) &
        (df['volume_spike'] == True)
    )
    
    short_condition = (
        (df['Close'] < df['ema_5']) &
        (df[rsi_col] > 70) &
        (df['volume_spike'] == True)
    )
    
    df.loc[long_condition, 'signal'] = 1
    df.loc[short_condition, 'signal'] = -1
    
    return df


def generate_day_trading_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Generate day trading signals based on MACD, RSI, and VWAP."""
    df = df.copy()
    df['signal'] = 0
    
    if 'rsi_7' in df.columns:
        rsi_col = 'rsi_7'
    elif 'rsi' in df.columns:
        rsi_col = 'rsi'
    else:
        rsi_col = None
    
    long_condition = (df['macd'] > df['macd_signal'])
    if rsi_col:
        long_condition = long_condition & (df[rsi_col] < 70)
    long_condition = long_condition & (df['Close'] > df['vwap'])
    
    short_condition = (df['macd'] < df['macd_signal'])
    if rsi_col:
        short_condition = short_condition & (df[rsi_col] > 30)
    short_condition = short_condition & (df['Close'] < df['vwap'])
    
    df.loc[long_condition, 'signal'] = 1
    df.loc[short_condition, 'signal'] = -1
    
    return df


def generate_intraday_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Generate intraday/swing signals based on Supertrend, ADX, and Stochastic."""
    df = df.copy()
    df['signal'] = 0
    
    long_condition = (
        (df['supertrend_direction'] == 1) &
        (df['adx'] > 25) &
        (df['stoch_k'] < 20)
    )
    
    short_condition = (
        (df['supertrend_direction'] == -1) &
        (df['adx'] > 25) &
        (df['stoch_k'] > 80)
    )
    
    df.loc[long_condition, 'signal'] = 1
    df.loc[short_condition, 'signal'] = -1
    
    return df