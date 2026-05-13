import pandas as pd


def resample_to_timeframe(df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """Resample data to different timeframes.

    Args:
        df: DataFrame with Date, Time, Open, High, Low, Close, Volume columns
        timeframe: Target timeframe ('5min', '15min', '1h', '4h', '1d')

    Returns:
        Resampled DataFrame
    """
    df = df.copy()

    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])
    elif 'Date' in df.columns and 'Time' in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df['Date']):
            df['datetime'] = df['Date'] + pd.to_timedelta(df['Time'])
        else:
            df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    elif 'timestamps' in df.columns:
        df['datetime'] = pd.to_datetime(df['timestamps'])
    elif 'Date' in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df['Date']):
            df['datetime'] = df['Date']
        else:
            df['datetime'] = pd.to_datetime(df['Date'])
    else:
        raise ValueError("No datetime column found")

    df = df.set_index('datetime')

    ohlc = {
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
    }
    
    if 'Volume' in df.columns:
        ohlc['Volume'] = 'sum'

    df_resampled = df.resample(timeframe).agg(ohlc).dropna()
    df_resampled = df_resampled.reset_index()

    return df_resampled