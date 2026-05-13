import pandas as pd
import numpy as np
from typing import List, Tuple, Dict


def run_backtest(
    df: pd.DataFrame,
    initial_capital: float = 10000,
    stop_loss: float = 1.0,
    take_profit: float = 1.5,
    max_daily_trades: int = 10
) -> Tuple[List[Dict], float]:
    """Run backtest simulation.
    
    Args:
        df: DataFrame with Close prices and signals
        initial_capital: Starting capital
        stop_loss: Stop loss percentage (0.5 = 0.5%)
        take_profit: Take profit percentage (1.5 = 1.5%)
        max_daily_trades: Maximum trades per day
        
    Returns:
        Tuple of (list of trades, final capital)
    """
    trades = []
    capital = initial_capital
    position = None
    entry_price = 0
    entry_idx = 0
    
    daily_trade_count = 0
    last_date = None
    
    date_col = 'Date' if 'Date' in df.columns else ('datetime' if 'datetime' in df.columns else None)
    
    for idx in range(len(df)):
        row = df.iloc[idx]
        current_date = row[date_col] if date_col else idx
        
        if last_date is not None and str(current_date) != str(last_date):
            daily_trade_count = 0
        last_date = current_date
        
        signal = row.get('signal', row.get('ml_signal', 0))
        
        if position is None and signal != 0 and daily_trade_count < max_daily_trades:
            position = signal
            entry_price = row['Close']
            entry_idx = idx
            daily_trade_count += 1
            
        elif position is not None:
            current_price = row['Close']
            price_change_pct = (current_price - entry_price) / entry_price * 100
            
            if position == -1:
                price_change_pct = -price_change_pct
            
            if price_change_pct <= -stop_loss or price_change_pct >= take_profit:
                profit = capital * (price_change_pct / 100)
                capital += profit
                
                exit_reason = 'STOP LOSS' if price_change_pct <= -stop_loss else 'TAKE PROFIT'
                
                trades.append({
                    'entry_idx': entry_idx,
                    'exit_idx': idx,
                    'entry_price': entry_price,
                    'exit_price': current_price,
                    'direction': 'long' if position == 1 else 'short',
                    'profit_pct': price_change_pct,
                    'profit_dollars': profit,
                    'capital_after': capital,
                    'exit_reason': exit_reason
                })
                
                position = None
    
    return trades, capital


def calculate_max_drawdown(trades: List[Dict], initial_capital: float) -> float:
    """Calculate maximum drawdown from trades."""
    capital_curve = [initial_capital]
    for trade in trades:
        capital_curve.append(trade['capital_after'])
    
    peak = capital_curve[0]
    max_dd = 0
    
    for capital in capital_curve:
        if capital > peak:
            peak = capital
        dd = (peak - capital) / peak * 100
        if dd > max_dd:
            max_dd = dd
    
    return max_dd