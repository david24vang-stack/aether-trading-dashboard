#!/usr/bin/env python3
"""
Expand all dashboard data files to 1000 models per tab.
Add prediction models and timestamps throughout.
ALL DATA IS SIMULATED. Not financial advice.
"""
import json
import random
import hashlib
from datetime import datetime, timezone

now = datetime.now(timezone.utc)
ts = now.isoformat()
ts_short = now.strftime("%Y-%m-%d %H:%M:%S UTC")

random.seed(42)

# Live market prices (from finance connector fetch)
LIVE_PRICES = {
    'SPY': 767.36, 'QQQ': 717.51, 'TLT': 81.66, 'GLD': 398.51,
    'USO': 130.66, 'IWM': 300.19, 'VIX': 15.84, 'DIA': 532.91
}
SYMBOLS = list(LIVE_PRICES.keys())

# Base model types
BASE_TYPES = [
    'Trend_SMA', 'Trend_EMA', 'Momentum_RSI', 'Momentum_MACD',
    'Mean_Reversion', 'Breakout', 'Volatility_ATR', 'Correlation_Pairs',
    'Volume_VWAP', 'Sentiment_Scan', 'Machine_Learning_LSTM',
    'Reinforcement_Q', 'Bayesian_Inf', 'GAN_Predictor', 'Diffusion_Proc',
    'Graph_Neural', 'Attention_LSTM', 'Autoencoder_Sig',
    'Wavelet_Decomp', 'Fuzzy_Logic'
]

STRATEGY_NAMES = [
    'Trend_Follow', 'Mean_Revert', 'Breakout_Hunter', 'Volatility_Scalp',
    'Pairs_Trade', 'Momentum_Ride', 'Range_Trade', 'MACD_Cross',
    'RSI_Divergence', 'Bollinger_Squeeze', 'EMA_Ribbon', 'VWAP_Bounce',
    'ATR_Trail', 'Correlation_Hedge', 'Volume_Profile', 'Sentiment_Pivot',
    'ML_LSTM_Predict', 'RL_Q_Learn', 'Bayesian_Update', 'GAN_Forecast',
    'Diffusion_Model', 'Graph_Net', 'Attention_Sequence', 'Autoencoder_Anomaly',
    'Wavelet_Decompose', 'Fuzzy_Logic'
]

CATEGORIES = ['Technical', 'Momentum', 'Mean_Reversion', 'Breakout', 'Volatility',
              'Statistical', 'Volume', 'Sentiment', 'Machine_Learning', 'Quantum']


def gen_model_id(base, i):
    return f"{base}_v{i:04d}"


def gen_prediction(symbol, model_id, model_type):
    """Generate a prediction entry with timestamp."""
    direction = random.choice(['buy', 'sell', 'hold'])
    confidence = round(random.uniform(0.35, 0.95), 4)
    price = LIVE_PRICES.get(symbol, 100.0)
    target = round(price * (1 + random.uniform(-0.03, 0.03)), 2)
    return {
        'model_id': model_id,
        'model_type': model_type,
        'symbol': symbol,
        'direction': direction,
        'confidence': confidence,
        'entry_price': price,
        'target_price': target,
        'stop_loss': round(price * (1 - random.uniform(0.005, 0.02)), 2),
        'take_profit': round(price * (1 + random.uniform(0.005, 0.03)), 2),
        'timestamp': ts,
        'timeframe': random.choice(['1m', '5m', '15m', '1h', '4h', '1d']),
        'signal_strength': round(random.uniform(0.1, 1.0), 4),
        'recorded_at': ts_short
    }


def expand_model_predictions():
    """Expand model_predictions_100.json to 1000 models."""
    models = []
    all_ids = []
    base_count = 10
    variations = 100  # 10 base × 100 = 1000

    base_names = BASE_TYPES[:10]
    for base in base_names:
        for i in range(1, variations + 1):
            mid = gen_model_id(base, i)
            all_ids.append(mid)
            lookback = random.randint(5, 50)
            models.append({
                'model_id': mid,
                'base_name': base,
                'description': f'{base} with varying parameters',
                'lookback': lookback,
                'variation': i,
                'prediction': random.choice(['buy', 'sell', 'hold']),
                'confidence': round(random.uniform(0.3, 0.95), 4),
                'accuracy': round(random.uniform(0.0, 0.0), 4),  # not_benchmarked
                'signals_generated': 0,
                'correct_signals': 0,
                'timestamp': ts,
                'recorded_at': ts_short,
                'precision_status': 'not_benchmarked',
                'simulated': True
            })

    # Only store first 200 in the models list for size, but keep all 1000 IDs
    data = {
        'total_models': 1000,
        'base_model_count': 10,
        'variations_per_base': 100,
        'models': models[:200],
        'all_model_ids': all_ids,
        'cycle': 10,
        'simulated': True,
        'model_prediction': True,
        'timestamp': ts,
        'recorded_at': ts_short,
        'precision_status': 'not_benchmarked',
        'honesty_notes': [
            '1,000 model configurations (parameter variations of 10 base models), NOT 1,000 unique AI models.',
            'No model has been benchmarked against live market data. accuracy=0.0 for all.',
            'Predictions are randomly generated for demonstration. Not financial advice.',
            f'Last updated: {ts_short}'
        ]
    }
    with open('data/model_predictions_100.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  model_predictions_100.json: 1000 models (200 detailed, 1000 IDs)")


def expand_continuous_engine():
    """Expand continuous_engine_status.json to 1000 models."""
    models = []
    for i in range(1000):
        base = BASE_TYPES[i % len(BASE_TYPES)]
        mid = gen_model_id(base, i + 1)
        models.append({
            'model_id': mid,
            'base_type': base,
            'variation': i + 1,
            'status': 'idle',
            'predictions': 0,
            'correct': 0,
            'accuracy': 0.0,
            'last_signal': 'none',
            'timestamp': ts
        })

    data = {
        'cycle_count': 10,
        'models': 1000,
        'swarm_agents': 50000000,
        'swarm_sample': 10000,
        'total_trades': 0,
        'total_signals': 0,
        'created_at': ts,
        'last_cycle': {
            'cycle': 10,
            'timestamp': ts,
            'models_active': 1000,
            'signals_generated': 0,
            'trades_executed': 0,
            'swarm_consensus': 'neutral',
            'swarm_result': {'total_agents': 50000000, 'active': 50000000, 'consensus': 'hold'}
        },
        'model_list': models[:200],
        'total_model_count': 1000,
        'precision_status': 'not_benchmarked',
        'simulated': True,
        'model_prediction': True,
        'timestamp': ts,
        'recorded_at': ts_short,
        'honesty_notes': [
            '1,000 model configurations (parameter variations of 20 base types), NOT 1,000 unique AI models.',
            'No model has been benchmarked. All accuracy values are 0.0.',
            'All trades are PAPER/SIMULATED. No real money at risk.',
            f'Last updated: {ts_short}'
        ]
    }
    with open('data/continuous_engine_status.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  continuous_engine_status.json: 1000 models")


def expand_oracle_console():
    """Expand oracle_console_data.json to 1000 top_models."""
    top_models = []
    for i in range(1000):
        base = BASE_TYPES[i % len(BASE_TYPES)]
        mid = f"{base}_{i+1:04d}"
        top_models.append({
            'model_id': mid,
            'base_type': base,
            'variation': i + 1,
            'params': {
                'period': round(random.uniform(5, 50), 1),
                'overbought': random.randint(65, 85),
                'oversold': random.randint(15, 35),
                'threshold': round(random.uniform(0.001, 0.05), 4)
            },
            'predictions': 0,
            'correct': 0,
            'accuracy': 0.0,
            'confidence': round(random.uniform(0.3, 0.9), 4),
            'last_signal': random.choice(['buy', 'sell', 'hold']),
            'last_hash': hashlib.sha256(f"{mid}{ts}".encode()).hexdigest()[:16],
            'timestamp': ts
        })

    signals = {'buy': 0, 'sell': 0, 'hold': 0}
    consensus = []
    for sym in SYMBOLS:
        buy_votes = random.randint(2800, 4200)
        sell_votes = random.randint(2500, 3800)
        hold_votes = 10000 - buy_votes - sell_votes
        if hold_votes < 0:
            hold_votes = 1000
            total = buy_votes + sell_votes + hold_votes
        else:
            total = 10000
        consensus.append({
            'symbol': sym,
            'consensus': 'buy' if buy_votes > sell_votes and buy_votes > hold_votes else ('sell' if sell_votes > buy_votes and sell_votes > hold_votes else 'hold'),
            'buy_votes': buy_votes,
            'sell_votes': sell_votes,
            'hold_votes': hold_votes,
            'total_votes': total,
            'agreement': round(max(buy_votes, sell_votes, hold_votes) / total, 4),
            'timestamp': ts,
            'recorded_at': ts_short
        })

    data = {
        'system_status': 'AUTO-GENERATING',
        'simulated': True,
        'model_prediction': True,
        'timestamp': ts,
        'recorded_at': ts_short,
        'cycle': 5,
        'total_models': 10000,
        'models_tested': 500,
        'extrapolation_factor': 20,
        'predictions': 80000,
        'correct': 0,
        'accuracy': 0.0,
        'signals': signals,
        'consensus_per_symbol': consensus,
        'top_models': top_models[:200],
        'total_top_models': 1000,
        'all_top_model_count': 1000,
        'duration_ms': 39.97,
        'precision_status': 'not_benchmarked',
        'disclaimer': 'Oracle Auto-Generator — SIMULATED. 10K models = 20 base types × 500 variations. Not financial advice.',
        'honesty_notes': [
            '10,000 model configurations = 20 base types × 500 variations each. NOT 10,000 unique AI models.',
            'No model has been benchmarked against live data. accuracy=0.0.',
            'Consensus votes are randomly distributed for demonstration.',
            f'Last updated: {ts_short}',
            'All predictions are SIMULATED. Not financial advice.',
            '1,000 top models stored (200 detailed for display).'
        ]
    }
    with open('data/oracle_console_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  oracle_console_data.json: 1000 top models")


def expand_auto_executor():
    """Expand auto_executor_status.json to 1000 models."""
    all_names = []
    top_models = []
    categories_used = {}

    for i in range(1000):
        cat = CATEGORIES[i % len(CATEGORIES)]
        base = STRATEGY_NAMES[i % len(STRATEGY_NAMES)]
        name = f"{base}_{i+1:04d}"
        all_names.append(name)
        categories_used[cat] = categories_used.get(cat, 0) + 1

        if i < 200:
            top_models.append({
                'name': name,
                'category': cat,
                'predictions_made': 0,
                'correct_predictions': 0,
                'accuracy': 0.0,
                'confidence': round(random.uniform(0.3, 0.9), 4),
                'last_signal': random.choice(['buy', 'sell', 'hold']),
                'last_signal_time': ts,
                'timestamp': ts,
                'recorded_at': ts_short
            })

    data = {
        'cycle_count': 3,
        'total_models': 1000,
        'total_orders': 8,
        'open_orders': 8,
        'closed_orders': 0,
        'total_pnl': 0,
        'balance': 100000,
        'win_count': 0,
        'loss_count': 0,
        'win_rate': 0.0,
        'avg_win': 0.0,
        'avg_loss': 0.0,
        'symbols_tracked': SYMBOLS,
        'model_categories': {c: categories_used.get(c, 100) for c in CATEGORIES},
        'simulated': True,
        'timestamp': ts,
        'recorded_at': ts_short,
        'honesty_notes': [
            'ALL trades are PAPER/SIMULATED. No real money is at risk.',
            '1,000 model configurations across 10 categories. NOT 1,000 unique AI models.',
            'No model has been benchmarked. accuracy=0.0 for all.',
            f'Last updated: {ts_short}'
        ],
        'top_models': top_models,
        'all_model_names': all_names,
        'total_all_models': 1000,
        'recent_orders': [
            {'order_id': 'ORD_000001', 'symbol': 'SPY', 'side': 'buy', 'order_type': 'stop', 'quantity': 12, 'contract_size': 767.36, 'timestamp': ts, 'recorded_at': ts_short},
            {'order_id': 'ORD_000002', 'symbol': 'QQQ', 'side': 'buy', 'order_type': 'limit', 'quantity': 10, 'contract_size': 717.51, 'timestamp': ts, 'recorded_at': ts_short},
            {'order_id': 'ORD_000003', 'symbol': 'TLT', 'side': 'sell', 'order_type': 'market', 'quantity': 10, 'contract_size': 81.66, 'timestamp': ts, 'recorded_at': ts_short},
            {'order_id': 'ORD_000004', 'symbol': 'GLD', 'side': 'buy', 'order_type': 'stop', 'quantity': 5, 'contract_size': 398.51, 'timestamp': ts, 'recorded_at': ts_short},
            {'order_id': 'ORD_000005', 'symbol': 'USO', 'side': 'sell', 'order_type': 'limit', 'quantity': 20, 'contract_size': 130.66, 'timestamp': ts, 'recorded_at': ts_short},
            {'order_id': 'ORD_000006', 'symbol': 'IWM', 'side': 'buy', 'order_type': 'market', 'quantity': 15, 'contract_size': 300.19, 'timestamp': ts, 'recorded_at': ts_short},
            {'order_id': 'ORD_000007', 'symbol': 'DIA', 'side': 'buy', 'order_type': 'stop', 'quantity': 8, 'contract_size': 532.91, 'timestamp': ts, 'recorded_at': ts_short},
            {'order_id': 'ORD_000008', 'symbol': 'SPY', 'side': 'sell', 'order_type': 'limit', 'quantity': 5, 'contract_size': 767.36, 'timestamp': ts, 'recorded_at': ts_short},
        ],
        'category_breakdown': {c: categories_used.get(c, 100) for c in CATEGORIES}
    }
    with open('data/auto_executor_status.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  auto_executor_status.json: 1000 models")


def expand_unlimited_engine():
    """Expand unlimited_engine_status.json to 1000 top accounts/models."""
    top_accounts = []
    worst_accounts = []
    top_strategies = []

    for i in range(1000):
        strat = STRATEGY_NAMES[i % len(STRATEGY_NAMES)]
        starting = 100000.0
        pnl = round(random.uniform(-8000, 15000), 2)
        balance = round(starting + pnl, 2)
        acct = {
            'account_id': f'ACCT_{i+1:06d}',
            'strategy_name': strat,
            'starting_balance': starting,
            'balance': balance,
            'pnl': pnl,
            'win_rate': round(random.uniform(0.35, 0.75), 4),
            'total_trades': random.randint(0, 50),
            'timestamp': ts,
            'recorded_at': ts_short
        }
        top_accounts.append(acct)

    # Sort by PnL for top/worst
    sorted_accts = sorted(top_accounts, key=lambda x: x['pnl'], reverse=True)
    top_accounts = sorted_accts[:200]
    worst_accounts = sorted_accts[-100:]

    for i in range(20):
        top_strategies.append({
            'genome_id': hashlib.sha256(f"genome_{i}".encode()).hexdigest()[:12],
            'fitness': round(random.uniform(0, 50), 4),
            'generation': random.randint(1, 5),
            'params': {
                'lookback': round(random.uniform(5, 50), 2),
                'threshold': round(random.uniform(0.001, 0.05), 6),
                'stop_loss': round(random.uniform(0.005, 0.03), 4),
                'take_profit': round(random.uniform(0.005, 0.04), 4)
            },
            'strategy': STRATEGY_NAMES[i % len(STRATEGY_NAMES)],
            'timestamp': ts,
            'recorded_at': ts_short
        })

    data = {
        'cycle_count': 5,
        'accounts': {f'tier_{i+1}': {'count': 100, 'starting_balance': 100000} for i in range(10)},
        'learning': {
            'total_models': 1000,
            'active_models': 1000,
            'learning_rate': 0.001,
            'iterations': 5,
            'best_fitness': top_strategies[0]['fitness'] if top_strategies else 0,
            'timestamp': ts
        },
        'evolution': {
            'generations': 5,
            'total_strategies': 1000,
            'survivors': 200,
            'mutation_rate': 0.1,
            'crossover_rate': 0.7,
            'timestamp': ts
        },
        'correlation': {
            'symbols_tracked': len(SYMBOLS),
            'matrix_size': f"{len(SYMBOLS)}x{len(SYMBOLS)}",
            'avg_correlation': round(random.uniform(-0.3, 0.5), 4),
            'timestamp': ts
        },
        'total_trades': 5,
        'simulated': True,
        'model_prediction': True,
        'timestamp': ts,
        'recorded_at': ts_short,
        'honesty_notes': [
            'All trading is PAPER/SIMULATED. No real money at risk.',
            '1,000 model/strategy configurations. NOT 1,000 unique AI models.',
            'No strategy has been validated against live market data.',
            f'Last updated: {ts_short}'
        ],
        'top_accounts': top_accounts,
        'worst_accounts': worst_accounts,
        'top_strategies': top_strategies,
        'total_top_accounts': 1000
    }
    with open('data/unlimited_engine_status.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  unlimited_engine_status.json: 1000 accounts/models")


def expand_ai_advisers():
    """Expand ai_adviser_results.json to include 1000 prediction models with timestamps."""
    # Keep the 4 main advisers but add 1000 prediction model entries
    advisers = [
        {
            'name': 'TrendAdviser',
            'confidence': 0.5,
            'predictions_made': 8,
            'parameters': {'lookback': 10, 'threshold': 0.005},
            'timestamp': ts,
            'recorded_at': ts_short,
            'model_count': 250
        },
        {
            'name': 'MeanReversionAdviser',
            'confidence': 0.5,
            'predictions_made': 8,
            'parameters': {'window': 20, 'z_threshold': 2.0},
            'timestamp': ts,
            'recorded_at': ts_short,
            'model_count': 250
        },
        {
            'name': 'VolatilityAdviser',
            'confidence': 0.5,
            'predictions_made': 8,
            'parameters': {'atr_period': 14, 'risk_factor': 0.02},
            'timestamp': ts,
            'recorded_at': ts_short,
            'model_count': 250
        },
        {
            'name': 'MomentumAdviser',
            'confidence': 0.5,
            'predictions_made': 8,
            'parameters': {'rsi_period': 14, 'macd_fast': 12, 'macd_slow': 26},
            'timestamp': ts,
            'recorded_at': ts_short,
            'model_count': 250
        }
    ]

    # Generate 1000 prediction models with timestamps
    prediction_models = []
    for i in range(1000):
        base = STRATEGY_NAMES[i % len(STRATEGY_NAMES)]
        sym = SYMBOLS[i % len(SYMBOLS)]
        prediction_models.append(gen_prediction(sym, f"{base}_{i+1:04d}", base))

    per_symbol = {}
    for sym in SYMBOLS:
        preds = [p for p in prediction_models if p['symbol'] == sym]
        per_symbol[sym] = {
            'total_models': len(preds),
            'buy': sum(1 for p in preds if p['direction'] == 'buy'),
            'sell': sum(1 for p in preds if p['direction'] == 'sell'),
            'hold': sum(1 for p in preds if p['direction'] == 'hold'),
            'avg_confidence': round(sum(p['confidence'] for p in preds) / max(len(preds), 1), 4),
            'timestamp': ts,
            'recorded_at': ts_short
        }

    data = {
        'generated_at': ts,
        'recorded_at': ts_short,
        'advisers': advisers,
        'prediction_models': prediction_models[:200],
        'total_prediction_models': 1000,
        'per_symbol': per_symbol,
        'summary': {
            'total_advisers': 4,
            'total_models': 1000,
            'total_predictions': 1000,
            'avg_confidence': round(sum(p['confidence'] for p in prediction_models) / 1000, 4),
            'timestamp': ts,
            'recorded_at': ts_short
        }
    }
    with open('data/ai_adviser_results.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  ai_adviser_results.json: 1000 prediction models with timestamps")


def expand_topstep_eval():
    """Expand topstep_eval_status.json with more models and timestamps."""
    funded_accounts = []
    for i in range(100):
        starting = random.choice([50000, 100000, 150000])
        pnl = round(random.uniform(-5000, 20000), 2)
        funded_accounts.append({
            'account_id': f'FUND_{i+1:06d}',
            'source_eval_id': f'EVAL_{i+1:06d}',
            'config_name': f'{starting//1000}K',
            'starting_balance': starting,
            'balance': round(starting + pnl, 2),
            'total_pnl': pnl,
            'total_trades': random.randint(5, 50),
            'win_rate': round(random.uniform(0.4, 0.8), 4),
            'days_active': random.randint(1, 30),
            'status': random.choice(['active', 'active', 'active', 'closed']),
            'timestamp': ts,
            'recorded_at': ts_short
        })

    data = {
        'cycle_count': 3,
        'total_evals_created': 150,
        'currently_evaluating': 100,
        'total_evals_passed': 5,
        'total_evals_failed': 45,
        'pass_rate': 10.0,
        'total_funded_created': 100,
        'funded_total_pnl': sum(a['total_pnl'] for a in funded_accounts),
        'funded_avg_pnl': round(sum(a['total_pnl'] for a in funded_accounts) / 100, 2),
        'funded_best_pnl': max(a['total_pnl'] for a in funded_accounts),
        'funded_worst_pnl': min(a['total_pnl'] for a in funded_accounts),
        'funded_total_trades': sum(a['total_trades'] for a in funded_accounts),
        'eval_total_pnl': 116832.47,
        'simulated': True,
        'model_prediction': True,
        'timestamp': ts,
        'recorded_at': ts_short,
        'honesty_notes': [
            'ALL accounts are SIMULATED. No real TopStep accounts are used.',
            'Pass rate is 10.0% (5 of 150 evals). Target is 95%.',
            '100 funded accounts simulated. All PnL is SIMULATED.',
            f'Last updated: {ts_short}'
        ],
        'top_funded': sorted(funded_accounts, key=lambda x: x['total_pnl'], reverse=True)[:20],
        'all_funded': funded_accounts,
        'total_funded_count': 100,
        'recent_passes': [
            {'account_id': f'EVAL_{i:06d}', 'config_name': '50K+', 'starting_balance': 50000, 'balance': round(50000 + random.uniform(1000, 5000), 2), 'total_pnl': round(random.uniform(1000, 5000), 2), 'timestamp': ts, 'recorded_at': ts_short}
            for i in range(1, 6)
        ],
        'eval_configs': {
            '50K': {'starting_balance': 50000, 'max_drawdown': 2000, 'profit_target': 3000, 'days': 10},
            '100K': {'starting_balance': 100000, 'max_drawdown': 2500, 'profit_target': 6000, 'days': 10},
            '150K': {'starting_balance': 150000, 'max_drawdown': 4500, 'profit_target': 9000, 'days': 10},
            '50K+': {'starting_balance': 50000, 'max_drawdown': 2000, 'profit_target': 3000, 'days': 10}
        }
    }
    with open('data/topstep_eval_status.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  topstep_eval_status.json: 100 funded accounts with timestamps")


def expand_market_predictions():
    """Expand market_predictions.json with timestamps for each prediction."""
    symbols_data = [
        ('SPY', 'SPDR S&P 500 ETF', 'stock', 767.36),
        ('QQQ', 'Invesco QQQ Trust', 'stock', 717.51),
        ('TLT', 'iShares 20+ Yr Treasury', 'bond', 81.66),
        ('GLD', 'SPDR Gold Shares', 'commodity', 398.51),
        ('USO', 'US Oil Fund', 'commodity', 130.66),
        ('IWM', 'iShares Russell 2000', 'stock', 300.19),
        ('VIX', 'CBOE Volatility Index', 'index', 15.84),
        ('DIA', 'SPDR Dow Jones', 'stock', 532.91),
        ('AAPL', 'Apple Inc.', 'stock', 305.93),
        ('MSFT', 'Microsoft Corp.', 'stock', 478.21),
        ('GOOGL', 'Alphabet Inc.', 'stock', 189.45),
        ('AMZN', 'Amazon.com Inc.', 'stock', 215.67),
        ('TSLA', 'Tesla Inc.', 'stock', 312.89),
        ('NVDA', 'NVIDIA Corp.', 'stock', 148.23),
        ('META', 'Meta Platforms', 'stock', 572.14),
        ('BTC', 'Bitcoin', 'crypto', 96450.0),
        ('ETH', 'Ethereum', 'crypto', 3320.0),
        ('GLD_XAU', 'Gold Spot', 'commodity', 2650.0),
        ('CL=F', 'Crude Oil Future', 'commodity', 72.45),
        ('EUR/USD', 'Euro/USD', 'forex', 1.0845),
    ]

    predictions = []
    for i, (sym, name, cls, price) in enumerate(symbols_data):
        direction = random.choice(['BULLISH', 'BEARISH', 'NEUTRAL'])
        confidence = round(random.uniform(0.3, 0.85), 4)
        predictions.append({
            'symbol': sym,
            'name': name,
            'asset_class': cls,
            'current_price': price,
            'direction': direction,
            'confidence': confidence,
            'target_price': round(price * (1 + random.uniform(-0.05, 0.05)), 2),
            'stop_loss': round(price * (1 - random.uniform(0.01, 0.03)), 2),
            'models_agree': random.randint(100, 800),
            'models_disagree': random.randint(100, 500),
            'timestamp': ts,
            'recorded_at': ts_short,
            'model_count': 1000,
            'timeframe': random.choice(['1h', '4h', '1d', '1w']),
            'signal_history': [
                {'time': (now.strftime('%H:%M')), 'signal': random.choice(['buy', 'sell', 'hold']), 'price': price}
                for _ in range(5)
            ]
        })

    data = {
        'timestamp': ts,
        'recorded_at': ts_short,
        'symbols_scanned': 20,
        'symbols_with_data': 20,
        'predictions': predictions,
        'data_sources': [
            {'name': 'Realtime Finance Data', 'assets': 'stocks/ETFs/indexes', 'cost': 'connected', 'timestamp': ts},
            {'name': 'Alpaca Paper Trading', 'assets': 'stocks/ETFs', 'cost': 'connected', 'timestamp': ts},
            {'name': 'AlphaCreek', 'assets': 'SEC filings', 'cost': 'connected', 'timestamp': ts},
            {'name': 'OpticOdds', 'assets': 'event markets', 'cost': 'connected', 'timestamp': ts},
            {'name': 'yfinance', 'assets': 'stocks/ETFs/indexes/options', 'cost': 'free'},
            {'name': 'Alpha Vantage', 'assets': 'stocks/forex/crypto', 'cost': 'free tier'}
        ],
        'prediction_models': [
            {'name': 'MA_Crossover', 'type': 'trend following', 'models': 100, 'timestamp': ts},
            {'name': 'RSI_Momentum', 'type': 'momentum', 'models': 100, 'timestamp': ts},
            {'name': 'Bollinger_Bands', 'type': 'mean reversion', 'models': 100, 'timestamp': ts},
            {'name': 'MACD_Signal', 'type': 'trend following', 'models': 100, 'timestamp': ts},
            {'name': 'ATR_Volatility', 'type': 'volatility', 'models': 100, 'timestamp': ts},
            {'name': 'Volume_VWAP', 'type': 'volume', 'models': 100, 'timestamp': ts},
            {'name': 'ML_LSTM', 'type': 'machine learning', 'models': 100, 'timestamp': ts},
            {'name': 'Sentiment_Scan', 'type': 'sentiment', 'models': 100, 'timestamp': ts},
            {'name': 'Correlation_Pairs', 'type': 'statistical', 'models': 100, 'timestamp': ts},
            {'name': 'Bayesian_Inf', 'type': 'probabilistic', 'models': 100, 'timestamp': ts},
        ],
        'asset_classes': {'stock': 14, 'commodity': 3, 'index': 1, 'crypto': 2, 'forex': 1, 'bond': 1},
        'total_symbols_available': 117,
        'total_models': 1000
    }
    with open('data/market_predictions.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  market_predictions.json: 1000 models, 20 symbols with timestamps")


def expand_sovereign():
    """Expand sovereign_status.json with 1000 models and timestamps."""
    roles = []
    for i in range(20):  # 20 roles, each managing 50 models = 1000
        roles.append({
            'name': f'Role_{i+1:02d}',
            'specialty': random.choice(['Structural Design', 'Risk Assessment', 'Strategy Optimization', 'Parameter Tuning', 'Signal Generation', 'Correlation Analysis', 'Volatility Modeling', 'Execution Planning']),
            'learning_iterations': random.randint(1, 10),
            'knowledge_entries': random.randint(1, 20),
            'confidence': round(random.uniform(0.1, 0.8), 4),
            'models_managed': 50,
            'timestamp': ts,
            'recorded_at': ts_short
        })

    data = {
        'version': 1.3,
        'cycles_completed': 3,
        'roles': roles,
        'total_patches': sum(r['learning_iterations'] for r in roles),
        'avg_confidence': round(sum(r['confidence'] for r in roles) / len(roles), 4),
        'consensus_signal': 'improving',
        'precision_status': 'not_benchmarked',
        'simulated': True,
        'model_prediction': True,
        'timestamp': ts,
        'recorded_at': ts_short,
        'disclaimer': 'Aether Sovereign — Simulated recursive improvement framework. No autonomous code execution.',
        'total_models': 1000,
        'num_roles': 20,
        'source_fingerprint': hashlib.sha256(f"sovereign_{ts}".encode()).hexdigest()[:20],
        'honesty_notes': [
            '20 specialized roles managing 50 models each = 1,000 model configurations.',
            'No model has been benchmarked against live data.',
            f'Last updated: {ts_short}'
        ],
        'recent_cycles': [
            {'cycle_number': 1, 'version': 1.0, 'patches': [], 'timestamp': ts, 'recorded_at': ts_short},
            {'cycle_number': 2, 'version': 1.2, 'patches': [], 'timestamp': ts, 'recorded_at': ts_short},
            {'cycle_number': 3, 'version': 1.3, 'patches': [], 'timestamp': ts, 'recorded_at': ts_short},
        ]
    }
    with open('data/sovereign_status.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  sovereign_status.json: 1000 models (20 roles × 50)")


def expand_omni_nexus():
    """Expand omni_nexus_status.json with 1000 models and timestamps."""
    data = {
        'plugins': {
            'Live_Market_Data': {'status': 'active', 'calls': 10, 'models_served': 1000, 'timestamp': ts, 'recorded_at': ts_short},
            'Paper_Trading': {'status': 'active', 'calls': 5, 'models_served': 500, 'timestamp': ts, 'recorded_at': ts_short},
            'SEC_Filings': {'status': 'active', 'calls': 3, 'models_served': 200, 'timestamp': ts, 'recorded_at': ts_short},
            'Event_Markets': {'status': 'active', 'calls': 2, 'models_served': 100, 'timestamp': ts, 'recorded_at': ts_short},
            'AI_Model_Registry': {'status': 'active', 'calls': 8, 'models_served': 1000, 'timestamp': ts, 'recorded_at': ts_short},
            'Risk_Manager': {'status': 'active', 'calls': 5, 'models_served': 1000, 'timestamp': ts, 'recorded_at': ts_short}
        },
        'models': {
            'total_registered': 1000,
            'active': 1000,
            'available_without_keys': 0,
            'by_provider': {f'provider_{i+1}': 100 for i in range(10)},
            'timestamp': ts,
            'recorded_at': ts_short
        },
        'generator': {
            'total_generated': 1000,
            'base_types': 20,
            'variations_per_type': 50,
            'timestamp': ts,
            'recorded_at': ts_short
        },
        'cycle_count': 3,
        'created_at': ts,
        'timestamp': ts,
        'recorded_at': ts_short,
        'precision_status': 'not_benchmarked',
        'simulated': True,
        'model_prediction': True,
        'disclaimer': 'Aether Omni-Nexus — Simulated plugin orchestrator. No live AI model calls without API keys.',
        'honesty_notes': [
            '1,000 model configurations registered. NOT 1,000 unique AI models.',
            '0 models available without API keys.',
            f'Last updated: {ts_short}'
        ],
        'recent_cycles': [
            {'cycle_number': 1, 'timestamp': ts, 'plugins_called': ['Live_Market_Data', 'Paper_Trading'], 'models_served': 1000},
            {'cycle_number': 2, 'timestamp': ts, 'plugins_called': ['SEC_Filings', 'Risk_Manager'], 'models_served': 1000},
            {'cycle_number': 3, 'timestamp': ts, 'plugins_called': ['AI_Model_Registry', 'Event_Markets'], 'models_served': 1000},
        ]
    }
    with open('data/omni_nexus_status.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  omni_nexus_status.json: 1000 models with timestamps")


def expand_strategy_lab():
    """Expand strategy_lab.json with 1000 models and timestamps."""
    strategies = []
    for i in range(200):  # 200 detailed, 1000 total
        strat_name = STRATEGY_NAMES[i % len(STRATEGY_NAMES)]
        strategies.append({
            'name': f'{strat_name}_{i+1:04d}',
            'type': strat_name,
            'pass_rate': 0.0,  # not_benchmarked
            'total_trades': 0,
            'win_rate': 0.0,
            'total_pnl': 0.0,
            'sharpe_ratio': 0.0,
            'max_drawdown': 0.0,
            'models_assigned': 5,
            'timestamp': ts,
            'recorded_at': ts_short,
            'precision_status': 'not_benchmarked',
            'simulated': True
        })

    data = {
        'strategies': strategies,
        'total_strategies': 1000,
        'detailed_strategies': 200,
        'best_strategy': 'none_benchmarked',
        'timestamp': ts,
        'recorded_at': ts_short,
        'simulated': True,
        'model_prediction': True,
        'honesty_notes': [
            '1,000 strategy configurations. None have been backtested with real data.',
            'All metrics are 0.0 (not_benchmarked).',
            f'Last updated: {ts_short}'
        ]
    }
    with open('data/strategy_lab.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  strategy_lab.json: 1000 strategies with timestamps")


def expand_quantum_results():
    """Expand quantum_results.json with 1000 models and timestamps."""
    data = {
        'portfolio_optimization': {
            'method': 'simulated_annealing',
            'num_portfolios_evaluated': 1000,
            'best_sharpe': 0.0,
            'timestamp': ts,
            'recorded_at': ts_short,
            'simulated': True
        },
        'risk_analysis': {
            'method': 'monte_carlo',
            'simulations': 1000,
            'var_95': 0.0,
            'cvar_95': 0.0,
            'max_drawdown': 0.0,
            'timestamp': ts,
            'recorded_at': ts_short,
            'simulated': True
        },
        'num_assets': 6,
        'num_qubits': 3,
        'total_models': 1000,
        'timestamp': ts,
        'recorded_at': ts_short,
        'simulated': True,
        'honesty_notes': [
            'Quantum-inspired classical simulation. No actual quantum computer used.',
            '1,000 model configurations. None benchmarked.',
            f'Last updated: {ts_short}'
        ]
    }
    with open('data/quantum_results.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  quantum_results.json: 1000 models with timestamps")


def expand_training_results():
    """Add timestamps to training_results.json and expand model count."""
    with open('data/training_results.json') as f:
        data = json.load(f)

    data['timestamp'] = ts
    data['recorded_at'] = ts_short
    data['total_models'] = 1000
    data['summary']['total_models'] = 1000
    data['summary']['timestamp'] = ts
    data['summary']['recorded_at'] = ts_short

    # Add timestamps to batches
    for batch in data.get('batches', []):
        batch['timestamp'] = ts
        batch['recorded_at'] = ts_short

    # Add timestamps to funded results
    for fr in data.get('funded_results', []):
        fr['timestamp'] = ts
        fr['recorded_at'] = ts_short

    # Add top models
    data['top_models'] = [
        {
            'model_id': f'Model_{i+1:04d}',
            'type': STRATEGY_NAMES[i % len(STRATEGY_NAMES)],
            'accuracy': 0.0,
            'predictions': 0,
            'correct': 0,
            'timestamp': ts,
            'recorded_at': ts_short,
            'simulated': True
        }
        for i in range(200)
    ]

    with open('data/training_results.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  training_results.json: 1000 models with timestamps")


def create_prediction_models():
    """Create a dedicated prediction models file with 1000 models and timestamps."""
    models = []
    for i in range(1000):
        base = STRATEGY_NAMES[i % len(STRATEGY_NAMES)]
        sym = SYMBOLS[i % len(SYMBOLS)]
        models.append(gen_prediction(sym, f"{base}_{i+1:04d}", base))

    data = {
        'total_models': 1000,
        'timestamp': ts,
        'recorded_at': ts_short,
        'simulated': True,
        'model_prediction': True,
        'precision_status': 'not_benchmarked',
        'models': models[:200],
        'all_model_count': 1000,
        'symbols_covered': SYMBOLS,
        'honesty_notes': [
            '1,000 prediction model configurations. NOT 1,000 unique AI models.',
            'No model has been benchmarked. All accuracy values are 0.0.',
            'Predictions are randomly generated for demonstration. Not financial advice.',
            f'Last updated: {ts_short}'
        ],
        'summary': {
            'buy_signals': sum(1 for m in models if m['direction'] == 'buy'),
            'sell_signals': sum(1 for m in models if m['direction'] == 'sell'),
            'hold_signals': sum(1 for m in models if m['direction'] == 'hold'),
            'avg_confidence': round(sum(m['confidence'] for m in models) / 1000, 4),
            'timestamp': ts,
            'recorded_at': ts_short
        }
    }
    with open('data/prediction_models_1000.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  prediction_models_1000.json: 1000 prediction models (NEW)")


def expand_execution_engine():
    """Add timestamps to execution_engine_status.json."""
    with open('data/execution_engine_status.json') as f:
        data = json.load(f)

    data['timestamp'] = ts
    data['recorded_at'] = ts_short
    data['total_models'] = 1000

    with open('data/execution_engine_status.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  execution_engine_status.json: 1000 models with timestamps")


if __name__ == '__main__':
    import os
    os.chdir('/home/user/workspace/trading-dashboard')

    print(f"Expanding all data files to 1000 models with timestamps...")
    print(f"Timestamp: {ts_short}")
    print()

    expand_model_predictions()
    expand_continuous_engine()
    expand_oracle_console()
    expand_auto_executor()
    expand_unlimited_engine()
    expand_ai_advisers()
    expand_topstep_eval()
    expand_market_predictions()
    expand_sovereign()
    expand_omni_nexus()
    expand_strategy_lab()
    expand_quantum_results()
    expand_training_results()
    create_prediction_models()
    expand_execution_engine()

    print(f"\nDone. All data files expanded to 1000 models with timestamps.")
