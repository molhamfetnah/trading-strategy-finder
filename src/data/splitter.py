import pandas as pd


def filter_2025(df: pd.DataFrame) -> pd.DataFrame:
    """Filter DataFrame to include only 2025 data (up to September 2025).
    
    Args:
        df: DataFrame with a 'Date' column in 'YYYY-MM-DD' format
        
    Returns:
        DataFrame filtered to 2025 dates (Jan 1 - Sep 30, 2025)
    """
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    start = pd.Timestamp('2025-01-01')
    end = pd.Timestamp('2025-09-30')
    return df[(df['Date'] >= start) & (df['Date'] <= end)]


def split_train_test(df: pd.DataFrame, split_date: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split DataFrame into training and test sets based on a date.
    
    Args:
        df: DataFrame with a 'Date' column
        split_date: Date string in 'YYYY-MM-DD' format (inclusive for train)
        
    Returns:
        Tuple of (train_df, test_df) where train contains dates <= split_date
    """
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    split = pd.Timestamp(split_date)
    train = df[df['Date'] <= split]
    test = df[df['Date'] > split]
    return train, test