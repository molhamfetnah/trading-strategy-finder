#!/usr/bin/env python3
"""
Live Trading Dashboard Demo
Visualizes trading algorithm performance with real-time simulation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.data.loader import load_data
from src.data.splitter import filter_2025, split_train_test
from src.indicators.scalping import calculate_scalping_indicators
from src.indicators.day_trading import calculate_day_trading_indicators
from src.indicators.intraday import calculate_intraday_indicators
from src.signals.base_signals import (
    generate_scalping_signals,
    generate_day_trading_signals,
    generate_intraday_signals
)
from src.signals.ml_filter import train_ml_filter, apply_ml_filter, add_ml_features
from src.backtest.engine import run_backtest
from src.backtest.metrics import calculate_metrics


def create_live_dashboard():
    """Create comprehensive live trading dashboard."""
    
    print("\n" + "="*80)
    print("🔴 LIVE TRADING DASHBOARD DEMO")
    print("="*80)
    print("\nLoading data...")
    
    df_1min = load_data('1min.csv')
    df_2025 = filter_2025(df_1min)
    train_1min, test_1min = split_train_test(df_2025, '2025-06-30')
    
    print(f"Test data: {len(test_1min)} candles")
    print(f"Date range: {test_1min['Date'].min()} to {test_1min['Date'].max()}")
    
    print("\n" + "-"*80)
    print("📊 PREPING DATA FOR LIVE SIMULATION...")
    print("-"*80)
    
    df = test_1min.copy().reset_index(drop=True)
    df = calculate_scalping_indicators(df)
    df = generate_scalping_signals(df)
    df = add_ml_features(df)
    ml_data = train_ml_filter(df)
    df = apply_ml_filter(df, ml_data)
    
    trades_list = []
    capital = 10000
    position = None
    entry_price = 0
    entry_idx = 0
    entry_time = ""
    
    simulated_trades = []
    
    print(f"\n{'='*80}")
    print("🎯 LIVE TRADING SIMULATION - SCALPING STRATEGY")
    print("="*80)
    print(f"{'Time':<20} {'Price':>10} {'Signal':>8} {'Action':>10} {'P/L':>12} {'Capital':>12}")
    print("-"*80)
    
    for i in range(len(df)):
        row = df.iloc[i]
        
        signal = row.get('ml_signal', row.get('signal', 0))
        
        candle_time = f"{row['Date']} {row['Time']}"
        
        if position is None and signal != 0:
            position = signal
            entry_price = row['Close']
            entry_idx = i
            entry_time = candle_time
            
            action = "📈 BUY" if signal == 1 else "📉 SELL"
            print(f"{candle_time:<20} {entry_price:>10.2f} {signal:>8} {action:>10} {'---':>12} {capital:>12.2f}")
        
        elif position is not None:
            current_price = row['Close']
            price_change_pct = (current_price - entry_price) / entry_price * 100
            
            if position == -1:
                price_change_pct = -price_change_pct
            
            stop_loss_triggered = price_change_pct <= -0.5
            take_profit_triggered = price_change_pct >= 1.5
            
            if stop_loss_triggered or take_profit_triggered:
                profit = capital * (price_change_pct / 100)
                capital += profit
                
                trade_result = {
                    'entry_time': entry_time,
                    'exit_time': candle_time,
                    'direction': 'LONG' if position == 1 else 'SHORT',
                    'entry_price': entry_price,
                    'exit_price': current_price,
                    'profit_pct': price_change_pct,
                    'profit_dollars': profit,
                    'capital_after': capital,
                    'exit_reason': 'TAKE PROFIT' if take_profit_triggered else 'STOP LOSS'
                }
                simulated_trades.append(trade_result)
                
                status = "✅" if profit > 0 else "❌"
                print(f"{candle_time:<20} {current_price:>10.2f} {0:>8} {status} EXIT    {profit:>+10.2f} {capital:>12.2f}")
                
                position = None
    
    print("-"*80)
    
    print(f"\n{'='*80}")
    print("📊 TRADING PERFORMANCE SUMMARY")
    print("="*80)
    
    winning = [t for t in simulated_trades if t['profit_dollars'] > 0]
    losing = [t for t in simulated_trades if t['profit_dollars'] <= 0]
    
    print(f"\n{'📈 TRADE BREAKDOWN':^40}")
    print("-"*40)
    print(f"Total Trades:      {len(simulated_trades)}")
    print(f"Winning Trades:    {len(winning)} ({len(winning)/len(simulated_trades)*100:.1f}%)" if simulated_trades else "Winning Trades:    0")
    print(f"Losing Trades:     {len(losing)} ({len(losing)/len(simulated_trades)*100:.1f}%)" if simulated_trades else "Losing Trades:     0")
    
    print(f"\n{'💰 PROFIT ANALYSIS':^40}")
    print("-"*40)
    total_profit = sum(t['profit_dollars'] for t in simulated_trades)
    gross_profit = sum(t['profit_dollars'] for t in winning) if winning else 0
    gross_loss = abs(sum(t['profit_dollars'] for t in losing)) if losing else 0
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
    
    print(f"Initial Capital:    $10,000.00")
    print(f"Final Capital:      ${capital:,.2f}")
    print(f"Total Profit:       ${total_profit:,.2f}")
    print(f"Profit Factor:      {profit_factor:.2f}")
    print(f"ROI:                {total_profit/100:.2f}%")
    
    print(f"\n{'📋 TRADE LOG':^40}")
    print("-"*40)
    print(f"{'#':<4} {'Direction':<8} {'Entry':>10} {'Exit':>10} {'P/L %':>8} {'P/L $':>10} {'Exit Reason':<15}")
    print("-"*40)
    
    for idx, trade in enumerate(simulated_trades, 1):
        direction_emoji = "📈" if trade['direction'] == 'LONG' else "📉"
        print(f"{idx:<4} {direction_emoji}{trade['direction']:<5} {trade['entry_price']:>10.2f} {trade['exit_price']:>10.2f} {trade['profit_pct']:>+7.2f}% ${trade['profit_dollars']:>+9.2f} {trade['exit_reason']:<15}")
    
    print("-"*40)
    
    return simulated_trades, capital


def create_comparison_dashboard():
    """Create dashboard comparing different strategies."""
    
    print("\n" + "="*80)
    print("🔄 STRATEGY COMPARISON DASHBOARD")
    print("="*80)
    
    df_1min = load_data('1min.csv')
    df_15min = load_data('NQ_15min_processed.csv')
    
    df_1min_2025 = filter_2025(df_1min)
    df_15min_2025 = filter_2025(df_15min)
    
    train_1min, test_1min = split_train_test(df_1min_2025, '2025-06-30')
    train_15min, test_15min = split_train_test(df_15min_2025, '2025-06-30')
    
    results = {}
    
    print("\n🎯 Running Scalping Strategy (1min)...")
    train = calculate_scalping_indicators(train_1min.copy())
    train = generate_scalping_signals(train)
    train = add_ml_features(train)
    ml_data = train_ml_filter(train)
    
    test = calculate_scalping_indicators(test_1min.copy())
    test = generate_scalping_signals(test)
    test = apply_ml_filter(test, ml_data)
    
    trades_scalping, capital_scalping = run_backtest(test, initial_capital=10000, stop_loss=0.5, take_profit=1.5)
    metrics_scalping = calculate_metrics(trades_scalping, 10000)
    results['scalping'] = {'trades': trades_scalping, 'metrics': metrics_scalping}
    print(f"   Trades: {len(trades_scalping)}, Profit: ${metrics_scalping['total_profit']:.2f}")
    
    print("🎯 Running Day Trading Strategy (15min)...")
    train_dt = calculate_day_trading_indicators(train_15min.copy())
    train_dt = generate_day_trading_signals(train_dt)
    train_dt = add_ml_features(train_dt)
    ml_data_dt = train_ml_filter(train_dt)
    
    test_dt = calculate_day_trading_indicators(test_15min.copy())
    test_dt = generate_day_trading_signals(test_dt)
    test_dt = apply_ml_filter(test_dt, ml_data_dt)
    
    trades_day, capital_day = run_backtest(test_dt, initial_capital=10000, stop_loss=1.0, take_profit=2.0)
    metrics_day = calculate_metrics(trades_day, 10000)
    results['day_trading'] = {'trades': trades_day, 'metrics': metrics_day}
    print(f"   Trades: {len(trades_day)}, Profit: ${metrics_day['total_profit']:.2f}")
    
    print("🎯 Running Intraday Strategy (15min)...")
    train_intra = calculate_intraday_indicators(train_15min.copy())
    train_intra = generate_intraday_signals(train_intra)
    train_intra = add_ml_features(train_intra)
    ml_data_intra = train_ml_filter(train_intra)
    
    test_intra = calculate_intraday_indicators(test_15min.copy())
    test_intra = generate_intraday_signals(test_intra)
    test_intra = apply_ml_filter(test_intra, ml_data_intra)
    
    trades_intra, capital_intra = run_backtest(test_intra, initial_capital=10000, stop_loss=1.0, take_profit=2.0)
    metrics_intra = calculate_metrics(trades_intra, 10000)
    results['intraday'] = {'trades': trades_intra, 'metrics': metrics_intra}
    print(f"   Trades: {len(trades_intra)}, Profit: ${metrics_intra['total_profit']:.2f}")
    
    print("\n" + "="*80)
    print("📊 STRATEGY COMPARISON RESULTS")
    print("="*80)
    print(f"{'Strategy':<15} {'Trades':>8} {'Profit':>12} {'Win Rate':>10} {'PF':>8} {'Sharpe':>8} {'DD':>8}")
    print("-"*80)
    
    for name, data in results.items():
        m = data['metrics']
        emoji = "🏆" if m['total_profit'] == max(r['metrics']['total_profit'] for r in results.values()) else "  "
        print(f"{emoji}{name:<13} {m['total_trades']:>8} ${m['total_profit']:>11.2f} {m['win_rate']:>9.1f}% {m['profit_factor']:>8.2f} {m['sharpe_ratio']:>8.2f} {m['max_drawdown']:>7.1f}%")
    
    print("-"*80)
    
    best = max(results.items(), key=lambda x: x[1]['metrics']['total_profit'])
    worst = min(results.items(), key=lambda x: x[1]['metrics']['total_profit'])
    
    print(f"\n🏆 BEST STRATEGY: {best[0].upper()}")
    print(f"   Total Profit: ${best[1]['metrics']['total_profit']:.2f}")
    print(f"   Final Capital: ${best[1]['metrics']['final_capital']:.2f}")
    
    print(f"\n⚠️  WORST STRATEGY: {worst[0].upper()}")
    print(f"   Total Loss: ${worst[1]['metrics']['total_profit']:.2f}")
    
    return results


def create_visual_dashboard():
    """Create visual HTML dashboard."""
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
    except ImportError:
        print("\n⚠️  Plotly not available for HTML dashboard. Install with: pip install plotly")
        return
    
    print("\n" + "="*80)
    print("📊 GENERATING VISUAL DASHBOARD")
    print("="*80)
    
    df_1min = load_data('1min.csv')
    df_2025 = filter_2025(df_1min)
    train_1min, test_1min = split_train_test(df_2025, '2025-06-30')
    
    df = test_1min.head(2000).copy().reset_index(drop=True)
    df = calculate_scalping_indicators(df)
    df = generate_scalping_signals(df)
    df = add_ml_features(df)
    ml_data = train_ml_filter(df)
    df = apply_ml_filter(df, ml_data)
    
    trades, final_capital = run_backtest(df, initial_capital=10000, stop_loss=0.5, take_profit=1.5)
    
    print(f"\nCreating chart with {len(df)} candles and {len(trades)} trades...")
    
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=('Price Chart with Trades', 'RSI', 'Volume'),
        row_heights=[0.5, 0.25, 0.25]
    )
    
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price',
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['ema_5'],
            line=dict(color='#2196F3', width=1),
            name='EMA 5'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['ema_20'],
            line=dict(color='#FF9800', width=1),
            name='EMA 20'
        ),
        row=1, col=1
    )
    
    for trade in trades:
        color = '#00C853' if trade['profit_dollars'] > 0 else '#FF1744'
        
        fig.add_trace(
            go.Scatter(
                x=[trade['entry_idx']],
                y=[df.iloc[trade['entry_idx']]['Low'] * 0.999],
                mode='markers',
                marker=dict(
                    symbol='triangle-up',
                    size=15,
                    color='#00E676',
                    line=dict(width=2, color='#000000')
                ),
                name='Entry',
                showlegend=False
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=[trade['exit_idx']],
                y=[df.iloc[trade['exit_idx']]['High'] * 1.001],
                mode='markers',
                marker=dict(
                    symbol='triangle-down',
                    size=15,
                    color=color,
                    line=dict(width=2, color='#000000')
                ),
                name=f"{'Win' if trade['profit_dollars'] > 0 else 'Loss'} ${trade['profit_dollars']:.0f}",
                showlegend=True
            ),
            row=1, col=1
        )
    
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['rsi_7'],
            line=dict(color='#9C27B0', width=1),
            name='RSI'
        ),
        row=2, col=1
    )
    
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['Volume'],
            marker_color=df['Volume'].apply(lambda x: '#26a69a' if x > df['Volume'].mean() * 1.5 else '#90A4AE'),
            name='Volume'
        ),
        row=3, col=1
    )
    
    metrics = calculate_metrics(trades, 10000)
    
    fig.update_layout(
        title=dict(
            text=f"<b>NASDAQ Scalping Strategy - Live Trading Dashboard</b><br>" +
                 f"<span style='font-size:12px'>Test Period: Jul-Sep 2025 | " +
                 f"Total Profit: ${metrics['total_profit']:.2f} | " +
                 f"Win Rate: {metrics['win_rate']:.1f}% | " +
                 f"Trades: {metrics['total_trades']}</span>",
            x=0.5,
            font=dict(size=16)
        ),
        height=900,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        template="plotly_dark"
    )
    
    equity_curve = [{'idx': 0, 'capital': 10000}]
    for trade in trades:
        equity_curve.append({'idx': trade['exit_idx'], 'capital': trade['capital_after']})
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=[e['idx'] for e in equity_curve],
        y=[e['capital'] for e in equity_curve],
        mode='lines+markers',
        line=dict(color='#00E676', width=2),
        marker=dict(size=4),
        name='Equity Curve'
    ))
    
    fig2.update_layout(
        title=dict(
            text=f"<b>Equity Curve</b><br>" +
                 f"<span style='font-size:12px'>Initial: $10,000 | Final: ${equity_curve[-1]['capital']:.2f} | " +
                 f"Return: {(equity_curve[-1]['capital'] - 10000) / 100:.2f}%</span>",
            x=0.5
        ),
        height=400,
        template="plotly_dark",
        showlegend=False
    )
    
    print("\n💾 Saving dashboard to HTML files...")
    
    fig.write_html('live_trading_dashboard.html', auto_open=False)
    fig2.write_html('equity_curve_dashboard.html', auto_open=False)
    
    print("✅ Dashboard saved: live_trading_dashboard.html")
    print("✅ Equity curve saved: equity_curve_dashboard.html")
    
    return metrics


def main():
    print("\n" + "="*80)
    print("🚀 NASDAQ TRADING ALGORITHM - LIVE DEMO")
    print("="*80)
    
    print("\n📅 Test Period: July - September 2025")
    print("💰 Initial Capital: $10,000")
    print("🎯 Strategy: Scalping (1min)")
    print("⚙️ Stop Loss: 0.5% | Take Profit: 1.5%")
    
    simulated_trades, final_capital = create_live_dashboard()
    
    results = create_comparison_dashboard()
    
    try:
        create_visual_dashboard()
    except Exception as e:
        print(f"\n⚠️  Could not create visual dashboard: {e}")
    
    print("\n" + "="*80)
    print("🎉 DEMO COMPLETE!")
    print("="*80)
    
    print("\n📊 SUMMARY:")
    print(f"   Total Strategies Tested: 3")
    print(f"   Best Strategy: SCALPING (${results['scalping']['metrics']['total_profit']:.2f})")
    print(f"   Total Trades: {sum(len(r['trades']) for r in results.values())}")
    print(f"   Combined Profit: ${sum(r['metrics']['total_profit'] for r in results.values()):.2f}")
    
    print("\n📁 Output Files:")
    print("   - live_trading_dashboard.html (if plotly installed)")
    print("   - equity_curve_dashboard.html (if plotly installed)")
    print("\n🌐 Open HTML files in browser to see visual dashboard!")
    
    print("\n🔗 Next Steps for Live Trading:")
    print("   1. Connect to live data feed (WebSocket/API)")
    print("   2. Add broker integration (Interactive Brokers/Alpaca)")
    print("   3. Implement real-time signal alerts")
    print("   4. Add position management and risk controls")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()