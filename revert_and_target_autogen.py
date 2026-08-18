#!/usr/bin/env python3
"""
1. Remove account generator (panel, 50K tab, functions) from v6_dashboard.html
2. Add auto-gen + live trade orders ONLY to tabs that show accounts/trade results
3. Keep all other tabs untouched
"""
import re

HTML_PATH = '/home/user/workspace/trading-dashboard/v6_dashboard.html'

with open(HTML_PATH, 'r') as f:
    html = f.read()

# ============================================================
# STEP 1: Remove account generator
# ============================================================

# Remove 50K Accounts nav tab
html = html.replace(
    '    <button class="nav-tab" data-tab="topstep50k" style="color:#f39c12">50K Accounts</button>\n    <button class="nav-tab" data-tab="modelwatch" style="color:#2ecc71">Model Watch</button>',
    '    <button class="nav-tab" data-tab="modelwatch" style="color:#2ecc71">Model Watch</button>'
)

# Remove account input panel
acct_panel_pattern = r'  <!-- ACCOUNT INPUT PANEL -->.*?</div>\n\n  <!-- AUTO-TRADE SIGNAL PANEL -->'
html = re.sub(acct_panel_pattern, '  <!-- AUTO-TRADE SIGNAL PANEL -->', html, flags=re.DOTALL)

# Remove 50K Accounts tab content
topstep50k_pattern = r'  <!-- 50K ACCOUNTS TAB -->.*?</div>\n\n  <!-- MODEL WATCH TAB -->'
html = re.sub(topstep50k_pattern, '  <!-- MODEL WATCH TAB -->', html, flags=re.DOTALL)

# Remove autoGenAccounts function
autogen_pattern = r'// ============================================================\n// AUTO-GEN ACCOUNTS\n// ============================================================\nfunction autoGenAccounts\(\).*?\n}\n\n'
html = re.sub(autogen_pattern, '', html, flags=re.DOTALL)

# Remove loadTopStep50K function
load50k_pattern = r'// ============================================================\n// 50K TOPSTEP ACCOUNTS\n// ============================================================\nlet topstep50kChart = null;\n\nasync function loadTopStep50K\(\).*?\n}\n\n'
html = re.sub(load50k_pattern, '', html, flags=re.DOTALL)

# Remove loadTopStep50K() calls in renderAll and autoRefresh
html = html.replace('  loadTopStep50K();\n  loadMarketCharts();', '  loadMarketCharts();')
html = html.replace('  loadTopStep50K();\n  loadMarketCharts();\n  renderTests();', '  loadMarketCharts();\n  renderTests();')

# Remove account input panel CSS
acct_css_pattern = r'/\* Account input panel \*/.*?\.btn-gen:hover\{background:rgba\(56,189,248,0\.25\)\}\n'
html = re.sub(acct_css_pattern, '', html, flags=re.DOTALL)

# Update Model Watch tab list (remove 50K Accts)
html = html.replace("'50K Accts','Providers'", "'Model Watch','Providers'")

print('Step 1: Account generator removed')

# ============================================================
# STEP 2: Add auto-gen + live trade orders to account/trade tabs only
# ============================================================

# Tabs that show accounts and trade results
AUTOGEN_TABS = {
    'overview':       {'name': 'Overview',          'symbols': ['SPY','QQQ','DIA'],              'strategy': 'Broad Market Index',      'contracts': [1,2,5]},
    'funded':         {'name': 'Funded Profit',    'symbols': ['SPY','QQQ','DIA'],              'strategy': 'Funded Account PnL',     'contracts': [1,2,5,10]},
    'unconstrained':  {'name': 'Unconstrained PnL','symbols': ['SPY','QQQ','GLD','USO'],         'strategy': 'No-Limit PnL',            'contracts': [5,10,20,50]},
    'tradehistory':   {'name': 'Trade History',    'symbols': ['SPY','QQQ','TLT','GLD','USO','IWM','DIA'], 'strategy': 'Historical Replay', 'contracts': [1,2,3]},
    'execution':      {'name': 'Execution Control','symbols': ['SPY','QQQ','IWM','DIA'],         'strategy': 'Smart Order Execution',   'contracts': [1,2,5,10]},
    'alpaca':         {'name': 'Alpaca Positions', 'symbols': ['SPY','QQQ','TLT'],              'strategy': 'Alpaca Paper API',        'contracts': [1,2,5]},
    'continuous':     {'name': 'Continuous Engine','symbols': ['SPY','QQQ','TLT','GLD','USO'],    'strategy': 'Continuous Cycle',        'contracts': [1,2,3,5]},
    'unlimited':      {'name': 'Unlimited Engine', 'symbols': ['SPY','QQQ','TLT','GLD','USO'],    'strategy': 'Unlimited Evolution',      'contracts': [1,2,5,10]},
    'topstep':        {'name': 'TopStep Eval',     'symbols': ['SPY','QQQ','IWM','DIA'],         'strategy': 'Eval Pass-Through',       'contracts': [1,2,3]},
    'auto-exec':      {'name': 'Auto Executor',    'symbols': ['SPY','QQQ','TLT','GLD','USO','IWM','DIA'], 'strategy': 'Auto Order Execution', 'contracts': [1,2,3,5,10]},
}

def make_autogen_block(tab_id, config):
    name = config['name']
    return f'''
    <!-- AUTO-GEN + LIVE TRADE ORDERS FOR {name.upper()} -->
    <div class="tab-autogen-bar" id="autogen-bar-{tab_id}">
      <span class="ag-dot"></span>
      <span class="ag-label">AUTO-GEN: ON</span>
      <span class="ag-info">Auto-generating trades for {name} | Strategy: <span id="autogen-strategy-{tab_id}">{config['strategy']}</span> | Trades: <span id="autogen-count-{tab_id}">0</span> | PnL: <span id="autogen-pnl-{tab_id}">$0.00</span></span>
      <span class="ag-info" style="margin-left:auto" id="autogen-last-{tab_id}">Last order: --</span>
    </div>
    <div class="live-orders-section">
      <div class="live-orders-header">
        <h3><span class="dot dot-live" style="animation:pulse 1s infinite"></span>Live Trade Orders — {name} <span class="auto-badge">AUTO</span></h3>
        <span class="tab-badge" id="live-orders-ts-{tab_id}">--</span>
      </div>
      <table class="live-orders-table">
        <thead><tr><th>Order ID</th><th>Time</th><th>Symbol</th><th>Side</th><th>Type</th><th>Contracts</th><th>Price</th><th>Status</th><th>PnL</th><th>Confidence</th></tr></thead>
        <tbody id="live-orders-{tab_id}"></tbody>
      </table>
    </div>'''

# Inject into each target tab
for tab_id, config in AUTOGEN_TABS.items():
    pattern = f'<div class="tab-content" id="tab-{tab_id}">'
    if tab_id == 'overview':
        pattern = '<div class="tab-content active" id="tab-overview">'
    
    idx = html.find(pattern)
    if idx == -1:
        print(f'WARNING: Tab {tab_id} not found')
        continue
    
    pos = idx + len(pattern)
    depth = 1
    while depth > 0 and pos < len(html):
        next_open = html.find('<div', pos)
        next_close = html.find('</div>', pos)
        if next_close == -1:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            pos = next_close + 6
    
    if depth == 0:
        block = make_autogen_block(tab_id, config)
        html = html[:pos] + block + html[pos:]
        print(f'Injected auto-gen into: {config["name"]} ({tab_id})')
    else:
        print(f'WARNING: Could not find closing </div> for tab {tab_id}')

print(f'Step 2: Auto-gen added to {len(AUTOGEN_TABS)} account/trade tabs')

# ============================================================
# STEP 3: Add CSS for auto-gen + live orders
# ============================================================

css_block = """
/* Live trade orders — auto-gen for account/trade tabs */
.live-orders-section{margin-top:20px;border:1px solid var(--border);border-radius:12px;overflow:hidden}
.live-orders-header{display:flex;justify-content:space-between;align-items:center;padding:12px 16px;background:var(--surface2);border-bottom:1px solid var(--border)}
.live-orders-header h3{font-size:13px;font-weight:700;color:var(--accent);margin:0;display:flex;align-items:center;gap:8px}
.live-orders-header .auto-badge{font-size:10px;font-weight:700;color:#2ecc71;background:rgba(46,204,113,0.15);padding:2px 8px;border-radius:4px;border:1px solid #2ecc71}
.live-orders-header .tab-badge{font-size:10px;color:var(--text-faint);font-weight:600}
.live-orders-table{width:100%;border-collapse:collapse;font-size:11px}
.live-orders-table th{background:var(--surface);padding:8px 10px;text-align:left;font-size:10px;color:var(--text-faint);text-transform:uppercase;letter-spacing:0.5px;border-bottom:1px solid var(--border)}
.live-orders-table td{padding:6px 10px;border-bottom:1px solid rgba(255,255,255,0.03);color:var(--text)}
.live-orders-table tr.new-order{animation:flashGreen 0.8s ease}
.live-orders-table tr.new-order-sell{animation:flashRed 0.8s ease}
@keyframes flashGreen{0%{background:rgba(46,204,113,0.2)}100%{background:transparent}}
@keyframes flashRed{0%{background:rgba(231,76,60,0.2)}100%{background:transparent}}
.side-buy{color:var(--success);font-weight:700}
.side-sell{color:var(--danger);font-weight:700}
.status-open{color:var(--accent);font-size:10px}
.status-filled{color:var(--success);font-size:10px}
.status-closed{color:var(--text-faint);font-size:10px}
.status-pending{color:var(--warning);font-size:10px}
.tab-autogen-bar{display:flex;align-items:center;gap:10px;padding:10px 16px;background:rgba(46,204,113,0.05);border:1px solid rgba(46,204,113,0.2);border-radius:8px;margin-bottom:12px}
.tab-autogen-bar .ag-label{font-size:12px;font-weight:700;color:#2ecc71}
.tab-autogen-bar .ag-info{font-size:11px;color:var(--text-dim)}
.tab-autogen-bar .ag-dot{width:8px;height:8px;border-radius:50%;background:#2ecc71;animation:pulse 1s infinite}
"""

# Insert CSS before the closing </style>
style_close = html.find('</style>')
if style_close != -1:
    html = html[:style_close] + css_block + html[style_close:]
    print('Step 3: CSS added')

# ============================================================
# STEP 4: Add JavaScript auto-gen engine for account/trade tabs only
# ============================================================

js_block = """
// ============================================================
// AUTO-GEN + AUTO-TRADE ENGINE — ACCOUNT/TRADE TABS ONLY
// ============================================================
// Only tabs showing accounts and trade results get auto-gen.
// Each generates timestamped paper trade orders every 1 second.
// ALL TRADES ARE PAPER/SIMULATED. Not financial advice.

const AUTOGEN_TAB_CONFIGS = {
  overview:       {name:'Overview',         symbols:['SPY','QQQ','DIA'],              strategy:'Broad Market Index',     contracts:[1,2,5]},
  funded:         {name:'Funded Profit',    symbols:['SPY','QQQ','DIA'],              strategy:'Funded Account PnL',     contracts:[1,2,5,10]},
  unconstrained:  {name:'Unconstrained PnL',symbols:['SPY','QQQ','GLD','USO'],         strategy:'No-Limit PnL',           contracts:[5,10,20,50]},
  tradehistory:   {name:'Trade History',   symbols:['SPY','QQQ','TLT','GLD','USO','IWM','DIA'], strategy:'Historical Replay', contracts:[1,2,3]},
  execution:      {name:'Execution Control',symbols:['SPY','QQQ','IWM','DIA'],        strategy:'Smart Order Execution',  contracts:[1,2,5,10]},
  alpaca:         {name:'Alpaca Positions',symbols:['SPY','QQQ','TLT'],              strategy:'Alpaca Paper API',        contracts:[1,2,5]},
  continuous:     {name:'Continuous Engine',symbols:['SPY','QQQ','TLT','GLD','USO'],  strategy:'Continuous Cycle',       contracts:[1,2,3,5]},
  unlimited:      {name:'Unlimited Engine', symbols:['SPY','QQQ','TLT','GLD','USO'],  strategy:'Unlimited Evolution',    contracts:[1,2,5,10]},
  topstep:        {name:'TopStep Eval',    symbols:['SPY','QQQ','IWM','DIA'],        strategy:'Eval Pass-Through',      contracts:[1,2,3]},
  'auto-exec':    {name:'Auto Executor',   symbols:['SPY','QQQ','TLT','GLD','USO','IWM','DIA'], strategy:'Auto Order Execution', contracts:[1,2,3,5,10]},
};

const tabTradeState = {};
Object.keys(AUTOGEN_TAB_CONFIGS).forEach(tabId => {
  tabTradeState[tabId] = { trades: [], totalPnl: 0, tradeCount: 0, wins: 0, closedCount: 0 };
});

let globalTradeCounter = 0;
let autoTradeEngineRunning = true;

function generateLiveTrade(tabId) {
  const config = AUTOGEN_TAB_CONFIGS[tabId];
  if (!config) return null;
  const state = tabTradeState[tabId];
  const symbol = config.symbols[Math.floor(Math.random() * config.symbols.length)];
  const basePrice = livePrices[symbol] || 100;
  const priceVar = (Math.random() - 0.5) * 0.006;
  const orderPrice = (basePrice * (1 + priceVar)).toFixed(2);
  const contracts = config.contracts[Math.floor(Math.random() * config.contracts.length)];
  const side = Math.random() > 0.45 ? 'BUY' : 'SELL';
  const orderType = ['MARKET','LIMIT','STOP'][Math.floor(Math.random()*3)];
  const confidence = (55 + Math.random() * 40).toFixed(1);
  globalTradeCounter++;
  
  const now = new Date();
  const ts = now.toISOString();
  const tsHuman = now.toLocaleTimeString() + ' CST';
  
  const isClosed = Math.random() < 0.4;
  let pnl = 0, status = 'OPEN', exitPrice = null;
  if (isClosed) {
    exitPrice = (parseFloat(orderPrice) * (1 + (Math.random() - 0.5) * 0.01)).toFixed(2);
    pnl = (parseFloat(exitPrice) - parseFloat(orderPrice)) * contracts * (side === 'BUY' ? 1 : -1);
    pnl = Math.round(pnl * 100) / 100;
    status = 'CLOSED';
    state.closedCount++;
    if (pnl > 0) state.wins++;
  } else {
    status = ['OPEN','PENDING','FILLED'][Math.floor(Math.random()*3)];
  }
  
  state.totalPnl += pnl;
  state.tradeCount++;
  
  return {
    trade_id: 'AUTO-' + tabId.toUpperCase() + '-' + String(globalTradeCounter).padStart(6,'0'),
    symbol, side, orderType, contracts, orderPrice, exitPrice, pnl, status, confidence,
    strategy: config.strategy, timestamp: ts, tsHuman
  };
}

function renderTabOrders(tabId) {
  const state = tabTradeState[tabId];
  const config = AUTOGEN_TAB_CONFIGS[tabId];
  const tbody = document.getElementById('live-orders-' + tabId);
  if (!tbody) return;
  
  const recent = state.trades.slice(0, 20);
  tbody.innerHTML = recent.map((t, i) => {
    const sideClass = t.side === 'BUY' ? 'side-buy' : 'side-sell';
    const statusClass = 'status-' + t.status.toLowerCase();
    const pnlStr = t.pnl !== 0 ? (t.pnl > 0 ? '+' : '') + '$' + t.pnl.toFixed(2) : '--';
    const pnlColor = t.pnl > 0 ? 'var(--success)' : t.pnl < 0 ? 'var(--danger)' : 'var(--text-faint)';
    const newClass = i === 0 ? (t.side === 'BUY' ? 'new-order' : 'new-order-sell') : '';
    return '<tr class="' + newClass + '"><td style="font-family:monospace;font-size:10px">' + t.trade_id + '</td><td style="font-size:10px;color:var(--text-faint)">' + t.tsHuman + '</td><td style="font-weight:700">' + t.symbol + '</td><td class="' + sideClass + '">' + t.side + '</td><td style="font-size:10px">' + t.orderType + '</td><td class="num">' + t.contracts + '</td><td class="num">$' + t.orderPrice + '</td><td class="' + statusClass + '">' + t.status + '</td><td class="num" style="color:' + pnlColor + '">' + pnlStr + '</td><td style="font-size:10px">' + t.confidence + '%</td></tr>';
  }).join('');
  
  const countEl = document.getElementById('autogen-count-' + tabId);
  if (countEl) countEl.textContent = state.tradeCount;
  const pnlEl = document.getElementById('autogen-pnl-' + tabId);
  if (pnlEl) pnlEl.textContent = (state.totalPnl >= 0 ? '+' : '') + '$' + state.totalPnl.toFixed(2);
  const lastEl = document.getElementById('autogen-last-' + tabId);
  if (lastEl && state.trades.length > 0) lastEl.textContent = 'Last order: ' + state.trades[0].tsHuman;
  const tsEl = document.getElementById('live-orders-ts-' + tabId);
  if (tsEl) tsEl.textContent = state.trades.length > 0 ? state.trades[0].tsHuman : '--';
}

function runAutoTradeCycle() {
  if (!autoTradeEngineRunning) return;
  const tabIds = Object.keys(AUTOGEN_TAB_CONFIGS);
  const numNew = Math.floor(Math.random() * 2) + 1;
  for (let i = 0; i < numNew; i++) {
    const tabId = tabIds[Math.floor(Math.random() * tabIds.length)];
    const trade = generateLiveTrade(tabId);
    if (trade) {
      tabTradeState[tabId].trades.unshift(trade);
      if (tabTradeState[tabId].trades.length > 100) {
        tabTradeState[tabId].trades = tabTradeState[tabId].trades.slice(0, 100);
      }
      renderTabOrders(tabId);
    }
  }
  const badge = document.getElementById('autotrade-count');
  if (badge) badge.textContent = globalTradeCounter;
}

// Load pre-generated trades, then start live generation
async function loadAutoTradeOrders() {
  try {
    const res = await fetch('data/auto_trade_orders_live.json?_t=' + Date.now());
    const data = await res.json();
    if (data.trades) {
      data.trades.forEach(t => {
        const tabId = t.tab;
        if (tabTradeState[tabId]) {
          tabTradeState[tabId].trades.unshift({
            trade_id: t.trade_id, symbol: t.symbol, side: t.side,
            orderType: t.order_type, contracts: t.contracts,
            orderPrice: t.price.toFixed(2),
            exitPrice: t.exit_price ? t.exit_price.toFixed(2) : null,
            pnl: t.pnl, status: t.status, confidence: t.confidence.toFixed(1),
            strategy: t.strategy, timestamp: t.timestamp, tsHuman: t.recorded_at
          });
          tabTradeState[tabId].totalPnl += t.pnl;
          tabTradeState[tabId].tradeCount++;
          if (t.status === 'CLOSED') { tabTradeState[tabId].closedCount++; if (t.pnl > 0) tabTradeState[tabId].wins++; }
          globalTradeCounter++;
        }
      });
      Object.keys(tabTradeState).forEach(tabId => {
        if (tabTradeState[tabId].trades.length > 100) tabTradeState[tabId].trades = tabTradeState[tabId].trades.slice(0, 100);
        renderTabOrders(tabId);
      });
      const badge = document.getElementById('autotrade-count');
      if (badge) badge.textContent = globalTradeCounter;
      console.log('[Auto-Trade] Loaded pre-generated trades for ' + Object.keys(AUTOGEN_TAB_CONFIGS).length + ' account/trade tabs');
    }
  } catch(e) { console.warn('[Auto-Trade] Load failed, starting fresh:', e); }
}

loadAutoTradeOrders();
setInterval(runAutoTradeCycle, 1000);
console.log('[Auto-Trade] Engine started — auto-gen for 10 account/trade tabs only');

"""

# Insert JS before START REAL-TIME UPDATES
rt_idx = html.find('// ============================================================\n// START REAL-TIME UPDATES')
if rt_idx != -1:
    html = html[:rt_idx] + js_block + '\n' + html[rt_idx:]
    print('Step 4: JavaScript auto-gen engine added')

# ============================================================
# STEP 5: Add live orders badge to header
# ============================================================

html = html.replace(
    '<span class="clock-display" id="real-clock">--:--:--</span>\n  </div>\n</div>',
    '<span class="clock-display" id="real-clock">--:--:--</span>\n    <span class="badge" id="autotrade-status-badge" style="background:rgba(46,204,113,0.15);color:#2ecc71;border:1px solid #2ecc71;display:inline-flex;align-items:center;gap:4px"><span class="dot dot-live" style="animation:pulse 1s infinite"></span><span id="autotrade-count">0</span> Live Orders</span>\n  </div>\n</div>'
)
print('Step 5: Header badge added')

# Save
with open(HTML_PATH, 'w') as f:
    f.write(html)

print('\nDone! Dashboard reverted + targeted auto-gen for 10 account/trade tabs only.')
