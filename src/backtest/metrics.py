import pandas as pd
import numpy as np
from typing import List, Dict


def calculate_metrics(trades: List[Dict], initial_capital: float = 10000) -> Dict:
    """Calculate all performance metrics.
    
    Args:
        trades: List of trade dictionaries
        initial_capital: Starting capital
        
    Returns:
        Dictionary with all metrics
    """
    if not trades:
        return {
            'total_profit': 0,
            'profit_factor': 0,
            'win_rate': 0,
            'sharpe_ratio': 0,
            'max_drawdown': 0,
            'total_trades': 0,
            'avg_profit': 0,
            'avg_loss': 0,
            'final_capital': initial_capital
        }
    
    profits = [t['profit_dollars'] for t in trades]
    winning_trades = [p for p in profits if p > 0]
    losing_trades = [p for p in profits if p <= 0]
    
    total_profit = sum(profits)
    gross_profit = sum(winning_trades) if winning_trades else 0
    gross_loss = abs(sum(losing_trades)) if losing_trades else 1
    
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
    win_rate = len(winning_trades) / len(trades) * 100 if trades else 0
    
    returns = [p / initial_capital * 100 for p in profits]
    sharpe_ratio = (np.mean(returns) / np.std(returns)) if np.std(returns) > 0 else 0
    
    max_dd = calculate_max_drawdown_from_trades(trades, initial_capital)
    
    return {
        'total_profit': total_profit,
        'profit_factor': profit_factor,
        'win_rate': win_rate,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_dd,
        'total_trades': len(trades),
        'avg_profit': np.mean(winning_trades) if winning_trades else 0,
        'avg_loss': np.mean(losing_trades) if losing_trades else 0,
        'final_capital': trades[-1]['capital_after'] if trades else initial_capital
    }


def calculate_max_drawdown_from_trades(trades: List[Dict], initial_capital: float) -> float:
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