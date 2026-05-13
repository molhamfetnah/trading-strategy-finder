import pandas as pd
import numpy as np


def add_ml_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add features for ML model."""
    df = df.copy()
    
    df['price_change'] = df['Close'].pct_change()
    df['price_change_5'] = df['Close'].pct_change(5)
    
    if 'Volume' in df.columns:
        df['volume_change'] = df['Volume'].pct_change()
        df['volume_ma_ratio'] = df['Volume'] / df['Volume'].rolling(20).mean()
    
    df['next_direction'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
    
    return df


def get_feature_columns(df: pd.DataFrame) -> list:
    """Get feature columns available in DataFrame."""
    base_features = ['price_change', 'price_change_5']
    
    if 'volume_change' in df.columns:
        base_features.append('volume_change')
    if 'volume_ma_ratio' in df.columns:
        base_features.append('volume_ma_ratio')
    
    indicator_features = ['rsi_7', 'macd', 'adx', 'supertrend', 'macd_hist', 'atr', 'stoch_k']
    for col in indicator_features:
        if col in df.columns:
            base_features.append(col)
    
    return base_features


def train_ml_filter(df: pd.DataFrame, n_estimators: int = 100, max_depth: int = 10) -> dict:
    """Train ML model to filter signals."""
    try:
        from sklearn.ensemble import RandomForestClassifier
    except ImportError:
        return None
    
    df = add_ml_features(df)
    feature_cols = get_feature_columns(df)
    
    df_clean = df.dropna(subset=feature_cols + ['next_direction'])
    
    if len(df_clean) < 50:
        return None
    
    X = df_clean[feature_cols]
    y = df_clean['next_direction']
    
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    model.fit(X, y)
    
    return {'model': model, 'feature_cols': feature_cols}


def apply_ml_filter(df: pd.DataFrame, ml_data: dict) -> pd.DataFrame:
    """Apply ML filter to signals."""
    if ml_data is None or 'model' not in ml_data:
        df = df.copy()
        df['ml_signal'] = df['signal']
        return df
    
    df = df.copy()
    df = add_ml_features(df)
    df['ml_signal'] = df['signal']
    
    model = ml_data['model']
    feature_cols = ml_data['feature_cols']
    
    signal_mask = df['signal'] != 0
    
    for idx in df[signal_mask].index:
        if idx in df.index:
            row = df.loc[idx]
            try:
                features = row[feature_cols].values.reshape(1, -1)
                if not np.isnan(features).any():
                    prediction = model.predict(features)[0]
                    if prediction == 0 and row['signal'] == 1:
                        df.at[idx, 'ml_signal'] = 0
                    elif prediction == 1 and row['signal'] == -1:
                        df.at[idx, 'ml_signal'] = 0
            except:
                pass
    
    return df