import pandas as pd
import numpy as np
from typing import List, Dict, Optional


def create_trade_chart(df: pd.DataFrame, trades: List[Dict], strategy_name: str) -> dict:
    """Create trade chart data for visualization.
    
    Args:
        df: Price data DataFrame
        trades: List of trade dictionaries
        strategy_name: Name of the strategy
        
    Returns:
        Dictionary with chart data
    """
    chart_data = {
        'strategy': strategy_name,
        'total_trades': len(trades),
        'trades': []
    }
    
    for trade in trades:
        trade_info = {
            'entry_idx': trade['entry_idx'],
            'exit_idx': trade['exit_idx'],
            'entry_price': trade['entry_price'],
            'exit_price': trade['exit_price'],
            'direction': trade['direction'],
            'profit_pct': trade['profit_pct'],
            'profit_dollars': trade['profit_dollars']
        }
        chart_data['trades'].append(trade_info)
    
    return chart_data


def create_equity_curve(trades: List[Dict], initial_capital: float) -> List[Dict]:
    """Create equity curve data from trades.
    
    Args:
        trades: List of trade dictionaries
        initial_capital: Starting capital
        
    Returns:
        List of equity curve points
    """
    curve = [{'idx': 0, 'capital': initial_capital}]
    capital = initial_capital
    
    for i, trade in enumerate(trades):
        capital = trade['capital_after']
        curve.append({'idx': i + 1, 'capital': capital})
    
    return curve


def calculate_trade_statistics(trades: List[Dict]) -> Dict:
    """Calculate detailed trade statistics.
    
    Args:
        trades: List of trade dictionaries
        
    Returns:
        Dictionary with statistics
    """
    if not trades:
        return {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'avg_win': 0,
            'avg_loss': 0,
            'largest_win': 0,
            'largest_loss': 0
        }
    
    profits = [t['profit_dollars'] for t in trades]
    winning = [p for p in profits if p > 0]
    losing = [p for p in profits if p <= 0]
    
    return {
        'total_trades': len(trades),
        'winning_trades': len(winning),
        'losing_trades': len(losing),
        'avg_win': np.mean(winning) if winning else 0,
        'avg_loss': np.mean(losing) if losing else 0,
        'largest_win': max(winning) if winning else 0,
        'largest_loss': min(losing) if losing else 0
    }