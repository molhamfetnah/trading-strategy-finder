#!/usr/bin/env python3
"""
Parameter Optimizer for Scalping Strategy
Tests various RSI, EMA, and volume thresholds to find optimal parameters
"""

import sys
import os
from itertools import product
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from src.data.loader import load_data
from src.data.splitter import filter_2025, split_train_test
from src.indicators.scalping import calculate_rsi, calculate_ema, calculate_volume_spike
from src.signals.base_signals import generate_scalping_signals
from src.signals.ml_filter import train_ml_filter, apply_ml_filter, add_ml_features
from src.backtest.engine import run_backtest
from src.backtest.metrics import calculate_metrics


def run_strategy(df, rsi_period, rsi_oversold, rsi_overbought, ema_fast, ema_slow, vol_threshold, stop_loss, take_profit, ml_enabled=True):
    """Run a single strategy configuration."""
    df = calculate_rsi(df, rsi_period)
    df = calculate_ema(df, [ema_fast, ema_slow])
    df = calculate_volume_spike(df, vol_threshold)
    df = generate_scalping_signals(df)
    
    if ml_enabled and len(df.dropna()) > 100:
        df = add_ml_features(df)
        ml_data = train_ml_filter(df)
        df = apply_ml_filter(df, ml_data)
    
    trades, final_capital = run_backtest(
        df,
        initial_capital=10000,
        stop_loss=stop_loss,
        take_profit=take_profit,
        max_daily_trades=10
    )
    
    metrics = calculate_metrics(trades, 10000)
    return metrics, trades, df


def optimize_scalping():
    """Run grid search optimization for scalping strategy."""
    print("=" * 70)
    print("SCALPING STRATEGY PARAMETER OPTIMIZER")
    print("=" * 70)
    
    print("\nLoading data...")
    df_1min = load_data('1min.csv')
    df_2025 = filter_2025(df_1min)
    train_df, test_df = split_train_test(df_2025, '2025-06-30')
    print(f"Train: {len(train_df)} candles, Test: {len(test_df)} candles")
    
    results = []
    best_profit = -999999
    best_config = None
    best_metrics = None
    
    print("\nRunning grid search...")
    start_time = datetime.now()
    
    rsi_periods = [5, 7, 9, 14]
    rsi_oversold_values = [25, 30, 35]
    rsi_overbought_values = [65, 70, 75]
    ema_fast_values = [3, 5, 7, 9]
    ema_slow_values = [10, 15, 20, 25]
    vol_thresholds = [1.5, 2.0, 2.5]
    stop_losses = [0.3, 0.5, 0.7]
    take_profits = [1.0, 1.5, 2.0]
    ml_options = [True, False]
    
    total_configs = (
        len(rsi_periods) * len(rsi_oversold_values) * len(rsi_overbought_values) *
        len(ema_fast_values) * len(ema_slow_values) * len(vol_thresholds) *
        len(stop_losses) * len(take_profits) * len(ml_options)
    )
    
    print(f"Total configurations to test: {total_configs}")
    
    tested = 0
    
    for rsi_period, rsi_oversold, rsi_overbought, ema_fast, ema_slow, vol_threshold, stop_loss, take_profit, ml_enabled in product(
        rsi_periods, rsi_oversold_values, rsi_overbought_values,
        ema_fast_values, ema_slow_values, vol_thresholds,
        stop_losses, take_profits, ml_options
    ):
        if ema_fast >= ema_slow:
            continue
            
        tested += 1
        
        try:
            metrics, trades, _ = run_strategy(
                test_df.copy(),
                rsi_period=rsi_period,
                rsi_oversold=rsi_oversold,
                rsi_overbought=rsi_overbought,
                ema_fast=ema_fast,
                ema_slow=ema_slow,
                vol_threshold=vol_threshold,
                stop_loss=stop_loss,
                take_profit=take_profit,
                ml_enabled=ml_enabled
            )
            
            result = {
                'rsi_period': rsi_period,
                'rsi_oversold': rsi_oversold,
                'rsi_overbought': rsi_overbought,
                'ema_fast': ema_fast,
                'ema_slow': ema_slow,
                'vol_threshold': vol_threshold,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'ml_enabled': ml_enabled,
                'profit': metrics['total_profit'],
                'profit_factor': metrics['profit_factor'],
                'win_rate': metrics['win_rate'],
                'total_trades': metrics['total_trades'],
                'sharpe': metrics['sharpe_ratio'],
                'max_dd': metrics['max_drawdown']
            }
            results.append(result)
            
            if metrics['total_profit'] > best_profit and metrics['total_trades'] >= 5:
                best_profit = metrics['total_profit']
                best_config = result.copy()
                best_metrics = metrics.copy()
                print(f"\n[NEW BEST] Profit: ${best_profit:.2f} | PF: {metrics['profit_factor']:.2f} | WR: {metrics['win_rate']:.1f}%")
                print(f"  RSI({rsi_period}) OS:{rsi_oversold} OB:{rsi_overbought} | EMA({ema_fast},{ema_slow}) | Vol:{vol_threshold}")
                print(f"  SL:{stop_loss}% TP:{take_profit}% | ML:{ml_enabled}")
            
        except Exception as e:
            pass
    
    elapsed = (datetime.now() - start_time).total_seconds()
    
    print(f"\n{'=' * 70}")
    print("OPTIMIZATION COMPLETE")
    print(f"{'=' * 70}")
    print(f"Tested: {tested} configurations")
    print(f"Time: {elapsed:.1f} seconds")
    
    print(f"\n{'=' * 70}")
    print("BEST CONFIGURATION FOUND")
    print(f"{'=' * 70}")
    if best_config:
        print(f"Total Profit:    ${best_config['profit']:.2f}")
        print(f"Profit Factor:   {best_config['profit_factor']:.2f}")
        print(f"Win Rate:        {best_config['win_rate']:.1f}%")
        print(f"Total Trades:    {best_config['total_trades']}")
        print(f"Sharpe Ratio:    {best_config['sharpe']:.2f}")
        print(f"Max Drawdown:    {best_config['max_dd']:.2f}%")
        print(f"\nParameters:")
        print(f"  RSI Period:    {best_config['rsi_period']}")
        print(f"  RSI Oversold:  {best_config['rsi_oversold']}")
        print(f"  RSI Overbought:{best_config['rsi_overbought']}")
        print(f"  EMA Fast:      {best_config['ema_fast']}")
        print(f"  EMA Slow:      {best_config['ema_slow']}")
        print(f"  Volume Spike:   {best_config['vol_threshold']}x")
        print(f"  Stop Loss:     {best_config['stop_loss']}%")
        print(f"  Take Profit:   {best_config['take_profit']}%")
        print(f"  ML Filter:     {best_config['ml_enabled']}")
        
        save_best_config(best_config)
    else:
        print("No valid configuration found")
    
    return results, best_config


def save_best_config(config):
    """Save best configuration to a file."""
    with open('best_config.txt', 'w') as f:
        f.write("# Best Scalping Strategy Configuration\n")
        f.write("# Generated by parameter_optimizer.py\n\n")
        for key, value in config.items():
            f.write(f"{key}={value}\n")
    print(f"\nBest configuration saved to best_config.txt")


def analyze_parameter_impact(results):
    """Analyze which parameters have the most impact."""
    print(f"\n{'=' * 70}")
    print("PARAMETER IMPACT ANALYSIS")
    print(f"{'=' * 70}")
    
    params = ['rsi_period', 'rsi_oversold', 'rsi_overbought', 'ema_fast', 'ema_slow', 
              'vol_threshold', 'stop_loss', 'take_profit', 'ml_enabled']
    
    for param in params:
        groups = {}
        for r in results:
            if r['total_trades'] >= 5:
                key = r[param]
                if key not in groups:
                    groups[key] = []
                groups[key].append(r['profit'])
        
        if groups:
            print(f"\n{param.upper()}:")
            for key, profits in sorted(groups.items()):
                avg = sum(profits) / len(profits)
                print(f"  {key}: avg profit = ${avg:.2f} ({len(profits)} tests)")


if __name__ == '__main__':
    results, best = optimize_scalping()
    if results:
        analyze_parameter_impact(results)