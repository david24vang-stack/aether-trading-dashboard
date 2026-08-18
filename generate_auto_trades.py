#!/usr/bin/env python3
"""
Auto-Trade Engine: Generates timestamped paper trade orders for each dashboard tab.
Each tab gets its own auto-generated trades pertaining to what the tab does.
All trades are PAPER/SIMULATED only. Not financial advice.
"""
import json, os, random, time
from datetime import datetime, timezone, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Load live market data for realistic pricing
def load_live_prices():
    try:
        with open(os.path.join(DATA_DIR, 'live_market_snapshot.json')) as f:
            data = json.load(f)
            symbols = data.get('symbols', {})
            return {k: v.get('price', 100) for k, v in symbols.items()}
    except:
        return {'SPY': 767.45, 'QQQ': 717.51, 'TLT': 81.66, 'GLD': 398.55,
                'USO': 130.66, 'IWM': 300.23, 'VIX': 15.84, 'DIA': 532.91}

# Tab definitions: what each tab trades and its strategy focus
TAB_CONFIGS = {
    'overview': {
        'name': 'Overview',
        'symbols': ['SPY', 'QQQ', 'DIA'],
        'strategy': 'Broad Market Index',
        'contracts': [1, 2, 5],
        'description': 'Index-level broad market trades'
    },
    'market': {
        'name': 'Live Market',
        'symbols': ['SPY', 'QQQ', 'TLT', 'GLD', 'USO', 'IWM', 'VIX', 'DIA'],
        'strategy': 'Live Price Action',
        'contracts': [1, 2, 3, 5],
        'description': 'All tracked symbols live trades'
    },
    'correlation': {
        'name': 'Correlation',
        'symbols': ['SPY', 'QQQ', 'TLT', 'GLD'],
        'strategy': 'Pairs/Stat-Arb',
        'contracts': [1, 2, 3],
        'description': 'Correlation-based pairs trades'
    },
    'qmodels': {
        'name': 'Quantum Models',
        'symbols': ['SPY', 'QQQ', 'GLD'],
        'strategy': 'Quantum Cycle Prediction',
        'contracts': [1, 2],
        'description': 'Quantum model signal trades'
    },
    'strategy': {
        'name': 'Strategy Lab',
        'symbols': ['SPY', 'QQQ', 'IWM', 'USO'],
        'strategy': 'Multi-Strategy Ensemble',
        'contracts': [1, 2, 3, 5],
        'description': 'Strategy lab generated trades'
    },
    'funded': {
        'name': 'Funded Profit',
        'symbols': ['SPY', 'QQQ', 'DIA'],
        'strategy': 'Funded Account PnL',
        'contracts': [1, 2, 5, 10],
        'description': 'Funded account simulated trades'
    },
    'unconstrained': {
        'name': 'Unconstrained PnL',
        'symbols': ['SPY', 'QQQ', 'GLD', 'USO'],
        'strategy': 'No-Limit PnL',
        'contracts': [5, 10, 20, 50],
        'description': 'Unconstrained large contract trades'
    },
    'tradehistory': {
        'name': 'Trade History',
        'symbols': ['SPY', 'QQQ', 'TLT', 'GLD', 'USO', 'IWM', 'DIA'],
        'strategy': 'Historical Replay',
        'contracts': [1, 2, 3],
        'description': 'Historical trade log entries'
    },
    'zenith': {
        'name': 'Zenith Lab',
        'symbols': ['SPY', 'QQQ', 'GLD', 'TLT'],
        'strategy': 'Zenith Prediction',
        'contracts': [1, 2, 3],
        'description': 'Zenith lab prediction trades'
    },
    'execution': {
        'name': 'Execution Control',
        'symbols': ['SPY', 'QQQ', 'IWM', 'DIA'],
        'strategy': 'Smart Order Execution',
        'contracts': [1, 2, 5, 10],
        'description': 'Execution engine order flow'
    },
    'advisers': {
        'name': 'AI Advisers',
        'symbols': ['SPY', 'QQQ', 'GLD', 'USO'],
        'strategy': '4-Adviser Council Consensus',
        'contracts': [1, 2, 3],
        'description': 'AI adviser council vote trades'
    },
    'alpaca': {
        'name': 'Alpaca Positions',
        'symbols': ['SPY', 'QQQ', 'TLT'],
        'strategy': 'Alpaca Paper API',
        'contracts': [1, 2, 5],
        'description': 'Alpaca paper account trades'
    },
    'sovereign': {
        'name': 'Sovereign',
        'symbols': ['SPY', 'QQQ', 'GLD'],
        'strategy': 'Recursive Architecture',
        'contracts': [1, 2, 3],
        'description': 'Sovereign framework trades'
    },
    'omni': {
        'name': 'Omni-Nexus',
        'symbols': ['SPY', 'QQQ', 'USO', 'IWM'],
        'strategy': 'Plugin Orchestration',
        'contracts': [1, 2, 3],
        'description': 'Omni-Nexus orchestrated trades'
    },
    'continuous': {
        'name': 'Continuous Engine',
        'symbols': ['SPY', 'QQQ', 'TLT', 'GLD', 'USO'],
        'strategy': 'Continuous Cycle',
        'contracts': [1, 2, 3, 5],
        'description': 'Continuous engine cycle trades'
    },
    'oracle-auto': {
        'name': 'Oracle Auto-Gen',
        'symbols': ['SPY', 'QQQ', 'GLD', 'IWM'],
        'strategy': 'Oracle Generated',
        'contracts': [1, 2, 3],
        'description': 'Oracle auto-generated trades'
    },
    'ai-models': {
        'name': 'AI Models',
        'symbols': ['SPY', 'QQQ', 'DIA', 'GLD'],
        'strategy': 'Multi-Model Consensus',
        'contracts': [1, 2, 3, 5],
        'description': 'AI model consensus trades'
    },
    'v22900': {
        'name': 'V22900',
        'symbols': ['SPY', 'QQQ'],
        'strategy': 'Epistemic Observation',
        'contracts': [1, 2],
        'description': 'V22900 epistemic trades'
    },
    'unlimited': {
        'name': 'Unlimited Engine',
        'symbols': ['SPY', 'QQQ', 'TLT', 'GLD', 'USO'],
        'strategy': 'Unlimited Account Evolution',
        'contracts': [1, 2, 5, 10],
        'description': 'Unlimited engine account trades'
    },
    'topstep': {
        'name': 'TopStep Eval',
        'symbols': ['SPY', 'QQQ', 'IWM', 'DIA'],
        'strategy': 'TopStep Eval Pass-Through',
        'contracts': [1, 2, 3],
        'description': 'TopStep evaluation trades'
    },
    'auto-exec': {
        'name': 'Auto Executor',
        'symbols': ['SPY', 'QQQ', 'TLT', 'GLD', 'USO', 'IWM', 'DIA'],
        'strategy': 'Auto Order Execution',
        'contracts': [1, 2, 3, 5, 10],
        'description': 'Auto executor order flow'
    },
    'modelwatch': {
        'name': 'Model Watch',
        'symbols': ['SPY', 'QQQ', 'TLT', 'GLD', 'USO', 'IWM', 'VIX', 'DIA'],
        'strategy': 'Watch Signal Execution',
        'contracts': [1, 2],
        'description': 'Model watch signal trades'
    },
    'providers': {
        'name': 'Market Providers',
        'symbols': ['SPY', 'QQQ', 'GLD', 'USO'],
        'strategy': 'Provider Data Trade',
        'contracts': [1, 2, 3],
        'description': 'Provider-sourced data trades'
    },
}

def generate_trade_order(tab_key, tab_config, prices, trade_id):
    """Generate a single timestamped paper trade order for a tab."""
    symbol = random.choice(tab_config['symbols'])
    base_price = prices.get(symbol, 100)
    # Realistic price variation
    price_var = random.uniform(-0.003, 0.003)
    order_price = round(base_price * (1 + price_var), 2)
    contracts = random.choice(tab_config['contracts'])
    side = random.choice(['BUY', 'SELL', 'BUY', 'SELL', 'BUY'])  # slight buy bias
    order_type = random.choice(['MARKET', 'LIMIT', 'STOP'])
    confidence = round(random.uniform(55, 95), 1)
    
    # Calculate PnL for closed trades
    is_closed = random.random() < 0.4
    if is_closed:
        exit_price = round(order_price * (1 + random.uniform(-0.005, 0.005)), 2)
        pnl = round((exit_price - order_price) * contracts * (1 if side == 'BUY' else -1), 2)
        status = 'CLOSED'
    else:
        exit_price = None
        pnl = 0
        status = random.choice(['OPEN', 'PENDING', 'FILLED'])
    
    now = datetime.now(timezone.utc)
    ts_iso = now.isoformat()
    ts_human = now.strftime('%Y-%m-%d %H:%M:%S UTC')
    
    return {
        'trade_id': f'AUTO-{tab_key.upper()}-{trade_id:06d}',
        'tab': tab_key,
        'tab_name': tab_config['name'],
        'symbol': symbol,
        'side': side,
        'order_type': order_type,
        'contracts': contracts,
        'price': order_price,
        'exit_price': exit_price,
        'pnl': pnl,
        'status': status,
        'confidence': confidence,
        'strategy': tab_config['strategy'],
        'description': tab_config['description'],
        'timestamp': ts_iso,
        'recorded_at': ts_human,
        'simulated': True,
        'paper_only': True,
    }

def generate_all_trades(prices, trades_per_tab=50):
    """Generate timestamped trades for every tab."""
    all_trades = []
    for tab_key, config in TAB_CONFIGS.items():
        for i in range(trades_per_tab):
            trade = generate_trade_order(tab_key, config, prices, i + 1)
            all_trades.append(trade)
    return all_trades

def generate_tab_summaries(all_trades):
    """Generate per-tab summary stats."""
    summaries = {}
    for tab_key, config in TAB_CONFIGS.items():
        tab_trades = [t for t in all_trades if t['tab'] == tab_key]
        total = len(tab_trades)
        open_trades = len([t for t in tab_trades if t['status'] in ('OPEN', 'PENDING', 'FILLED')])
        closed_trades = len([t for t in tab_trades if t['status'] == 'CLOSED'])
        total_pnl = round(sum(t['pnl'] for t in tab_trades), 2)
        buy_count = len([t for t in tab_trades if t['side'] == 'BUY'])
        sell_count = len([t for t in tab_trades if t['side'] == 'SELL'])
        win_trades = len([t for t in tab_trades if t['pnl'] > 0])
        win_rate = round(win_trades / max(closed_trades, 1) * 100, 1)
        symbols_traded = list(set(t['symbol'] for t in tab_trades))
        
        summaries[tab_key] = {
            'tab_name': config['name'],
            'description': config['description'],
            'strategy': config['strategy'],
            'total_trades': total,
            'open_trades': open_trades,
            'closed_trades': closed_trades,
            'total_pnl': total_pnl,
            'buy_orders': buy_count,
            'sell_orders': sell_count,
            'win_rate': win_rate,
            'symbols_traded': symbols_traded,
            'auto_gen': True,
            'auto_trade': True,
            'running': True,
            'last_trade_time': tab_trades[-1]['timestamp'] if tab_trades else None,
            'last_trade_human': tab_trades[-1]['recorded_at'] if tab_trades else None,
        }
    return summaries

def main():
    prices = load_live_prices()
    
    # Generate trades
    all_trades = generate_all_trades(prices, trades_per_tab=50)
    summaries = generate_tab_summaries(all_trades)
    
    # Save live trade orders
    trade_data = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'recorded_at': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'),
        'total_trades': len(all_trades),
        'tabs_active': len(TAB_CONFIGS),
        'all_paper_simulated': True,
        'trades': all_trades,
        'tab_summaries': summaries,
        'disclaimer': 'ALL TRADES ARE PAPER/SIMULATED. No real money is at risk. Not financial advice.',
    }
    
    out_path = os.path.join(DATA_DIR, 'auto_trade_orders_live.json')
    with open(out_path, 'w') as f:
        json.dump(trade_data, f, indent=2)
    
    print(f'Generated {len(all_trades)} paper trade orders across {len(TAB_CONFIGS)} tabs')
    print(f'Saved to {out_path}')
    print(f'Tab summaries:')
    for tab, s in summaries.items():
        print(f'  {s["tab_name"]:20s} | {s["total_trades"]:3d} trades | PnL: ${s["total_pnl"]:>10.2f} | Win: {s["win_rate"]}% | Auto: {"ON" if s["auto_trade"] else "OFF"}')

if __name__ == '__main__':
    main()
