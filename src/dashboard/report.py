import pandas as pd
from typing import Dict, List


def generate_comparison_report(results: Dict[str, Dict]) -> Dict:
    """Generate comparison report for all strategies.
    
    Args:
        results: Dictionary with strategy names as keys and metrics as values
        
    Returns:
        Dictionary with comparison report
    """
    if not results:
        return {'error': 'No results to compare'}
    
    best_strategy = max(results.items(), key=lambda x: x[1].get('total_profit', 0))
    
    report = {
        'best_strategy': best_strategy[0],
        'best_profit': best_strategy[1].get('total_profit', 0),
        'all_results': results,
        'recommendation': f"Use {best_strategy[0]} strategy for production trading.",
        'confidence': calculate_confidence(results, best_strategy[0])
    }
    
    return report


def calculate_confidence(results: Dict[str, Dict], best_strategy: str) -> str:
    """Calculate confidence level for the best strategy.
    
    Args:
        results: Dictionary with strategy results
        best_strategy: Name of the best strategy
        
    Returns:
        Confidence level string ('High', 'Medium', 'Low')
    """
    best = results[best_strategy]
    others = [r.get('total_profit', 0) for k, r in results.items() if k != best_strategy]
    
    if not others:
        return 'High'
    
    avg_others = sum(others) / len(others)
    if avg_others == 0:
        return 'High'
    
    advantage = (best.get('total_profit', 0) - avg_others) / avg_others * 100
    
    if advantage > 50:
        return 'High'
    elif advantage > 20:
        return 'Medium'
    else:
        return 'Low'


def generate_error_analysis(trades: List[Dict]) -> Dict:
    """Generate error analysis for trades.
    
    Args:
        trades: List of trade dictionaries
        
    Returns:
        Dictionary with error analysis
    """
    total_trades = len(trades)
    if total_trades == 0:
        return {'error_rate': 0, 'analysis': 'No trades to analyze'}
    
    losing_trades = [t for t in trades if t['profit_dollars'] <= 0]
    error_rate = len(losing_trades) / total_trades * 100
    
    avg_loss = sum([t['profit_dollars'] for t in losing_trades]) / len(losing_trades) if losing_trades else 0
    
    return {
        'error_rate': error_rate,
        'total_trades': total_trades,
        'losing_trades': len(losing_trades),
        'avg_loss': abs(avg_loss),
        'analysis': f'{error_rate:.1f}% of trades resulted in loss'
    }


def format_metrics_for_display(metrics: Dict) -> Dict:
    """Format metrics for display.
    
    Args:
        metrics: Raw metrics dictionary
        
    Returns:
        Formatted metrics dictionary
    """
    formatted = {}
    for key, value in metrics.items():
        if isinstance(value, float):
            if 'pct' in key or 'rate' in key or 'drawdown' in key:
                formatted[key] = f"{value:.2f}%"
            else:
                formatted[key] = f"${value:.2f}"
        elif isinstance(value, int):
            if 'trades' in key:
                formatted[key] = str(value)
            else:
                formatted[key] = f"{value:.2f}"
        else:
            formatted[key] = str(value)
    
    return formatted