import pandas as pd
import numpy as np
from typing import List, Dict


def calculate_metrics(trades: List[Dict], initial_capital: float = 10000) -> Dict:
    """Calculate all performance metrics including risk metrics.
    
    Args:
        trades: List of trade dictionaries
        initial_capital: Starting capital
        
    Returns:
        Dictionary with all metrics including risk metrics
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
            'final_capital': initial_capital,
            'expected_value': 0,
            'max_consecutive_losses': 0,
            'total_fees': 0
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
    
    expected_value = np.mean(profits)
    
    max_consecutive_losses = calculate_max_consecutive_losses(trades)
    
    total_fees = sum(t.get('fees_paid', 0) for t in trades)
    
    return {
        'total_profit': total_profit,
        'profit_factor': profit_factor,
        'win_rate': win_rate,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_dd,
        'total_trades': len(trades),
        'avg_profit': np.mean(winning_trades) if winning_trades else 0,
        'avg_loss': np.mean(losing_trades) if losing_trades else 0,
        'final_capital': trades[-1]['capital_after'] if trades else initial_capital,
        'expected_value': expected_value,
        'max_consecutive_losses': max_consecutive_losses,
        'total_fees': total_fees
    }


def calculate_max_consecutive_losses(trades: List[Dict]) -> int:
    """Calculate maximum consecutive losing trades."""
    if not trades:
        return 0
    
    max_streak = 0
    current_streak = 0
    
    for trade in trades:
        if trade['profit_dollars'] <= 0:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    
    return max_streak


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