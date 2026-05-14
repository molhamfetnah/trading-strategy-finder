import pandas as pd


def filter_2025(df: pd.DataFrame) -> pd.DataFrame:
    """Filter DataFrame to include only 2025 data (up to September 2025).
    
    Args:
        df: DataFrame with a 'Date' or 'timestamps' column
        
    Returns:
        DataFrame filtered to 2025 dates (Jan 1 - Sep 30, 2025)
    """
    df = df.copy()
    
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        if df['Date'].dt.hour.min() == 0 and df['Date'].dt.minute.min() == 0:
            df['Date_only'] = df['Date'].dt.normalize()
        else:
            df['Date_only'] = df['Date'].dt.date
        date_col = 'Date_only'
    elif 'timestamps' in df.columns:
        df['timestamps'] = pd.to_datetime(df['timestamps'])
        df['Date_only'] = df['timestamps'].dt.normalize()
        df['Time'] = df['timestamps'].dt.strftime('%H:%M:%S')
        date_col = 'Date_only'
    else:
        raise ValueError("No Date or timestamps column found")
    
    start = pd.Timestamp('2025-01-01')
    end = pd.Timestamp('2025-09-30')
    return df[(df[date_col] >= start) & (df[date_col] <= end)]


def split_train_test(df: pd.DataFrame, split_date: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split DataFrame into training and test sets based on a date.
    
    Args:
        df: DataFrame with a 'Date' column
        split_date: Date string in 'YYYY-MM-DD' format (inclusive for train)
        
    Returns:
        Tuple of (train_df, test_df) where train contains dates <= split_date
    """
    df = df.copy()
    
    split = pd.Timestamp(split_date)
    
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Date_only'] = df['Date'].dt.normalize() if df['Date'].dt.hour.min() == 0 else df['Date'].dt.date
    elif 'timestamps' in df.columns:
        df['timestamps'] = pd.to_datetime(df['timestamps'])
        df['Date_only'] = df['timestamps'].dt.normalize()
    
    train = df[df['Date_only'] <= split]
    test = df[df['Date_only'] > split]
    return train, test