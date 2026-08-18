#!/usr/bin/env python3
"""
Inject auto-gen bar + live trade orders section into every tab in v6_dashboard.html.
Each tab gets its own auto-generated trade orders panel with timestamps.
"""
import re

HTML_PATH = '/home/user/workspace/trading-dashboard/v6_dashboard.html'

with open(HTML_PATH, 'r') as f:
    html = f.read()

# Map of tab IDs to tab names
TABS = {
    'overview': 'Overview',
    'market': 'Live Market',
    'correlation': 'Correlation',
    'qmodels': 'Quantum Models',
    'strategy': 'Strategy Lab',
    'funded': 'Funded Profit',
    'unconstrained': 'Unconstrained PnL',
    'tradehistory': 'Trade History',
    'zenith': 'Zenith Lab',
    'execution': 'Execution Control',
    'advisers': 'AI Advisers',
    'alpaca': 'Alpaca Positions',
    'sovereign': 'Sovereign',
    'omni': 'Omni-Nexus',
    'continuous': 'Continuous Engine',
    'oracle-auto': 'Oracle Auto-Gen',
    'ai-models': 'AI Models',
    'v22900': 'V22900',
    'unlimited': 'Unlimited Engine',
    'topstep': 'TopStep Eval',
    'auto-exec': 'Auto Executor',
    'modelwatch': 'Model Watch',
    'providers': 'Market Providers',
}

# The HTML block to inject before the closing </div> of each tab
def make_inject_block(tab_id, tab_name):
    return f'''
    <!-- AUTO-GEN + LIVE TRADE ORDERS FOR {tab_name.upper()} -->
    <div class="tab-autogen-bar" id="autogen-bar-{tab_id}">
      <span class="ag-dot"></span>
      <span class="ag-label">AUTO-GEN: ON</span>
      <span class="ag-info">Auto-generating trades for {tab_name} | Strategy: <span id="autogen-strategy-{tab_id}">--</span> | Trades: <span id="autogen-count-{tab_id}">0</span> | PnL: <span id="autogen-pnl-{tab_id}">$0.00</span></span>
      <span class="ag-info" style="margin-left:auto" id="autogen-last-{tab_id}">Last order: --</span>
    </div>
    <div class="live-orders-section">
      <div class="live-orders-header">
        <h3><span class="dot dot-live" style="animation:pulse 1s infinite"></span>Live Trade Orders — {tab_name} <span class="auto-badge">AUTO</span></h3>
        <span class="tab-badge" id="live-orders-ts-{tab_id}">--</span>
      </div>
      <table class="live-orders-table">
        <thead><tr><th>Order ID</th><th>Time</th><th>Symbol</th><th>Side</th><th>Type</th><th>Contracts</th><th>Price</th><th>Status</th><th>PnL</th><th>Confidence</th></tr></thead>
        <tbody id="live-orders-{tab_id}"></tbody>
      </table>
    </div>'''

# For each tab, find the closing </div> of the tab-content and inject before it
# We need to find the tab-content div and its matching closing tag
modified = html
injections = 0

for tab_id, tab_name in TABS.items():
    # Find the tab-content div
    pattern = f'<div class="tab-content" id="tab-{tab_id}">'
    if tab_id == 'overview':
        pattern = '<div class="tab-content active" id="tab-overview">'
    
    idx = modified.find(pattern)
    if idx == -1:
        print(f'WARNING: Tab {tab_id} not found')
        continue
    
    # Find the closing </div> for this tab-content
    # We need to count div opens and closes from the tab-content div start
    pos = idx + len(pattern)
    depth = 1
    while depth > 0 and pos < len(modified):
        next_open = modified.find('<div', pos)
        next_close = modified.find('</div>', pos)
        if next_close == -1:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            pos = next_close + 6
    
    if depth == 0:
        inject_block = make_inject_block(tab_id, tab_name)
        modified = modified[:pos] + inject_block + modified[pos:]
        injections += 1
        print(f'Injected auto-gen block into tab: {tab_name} ({tab_id})')
    else:
        print(f'WARNING: Could not find closing </div> for tab {tab_id}')

with open(HTML_PATH, 'w') as f:
    f.write(modified)

print(f'\nTotal injections: {injections}/{len(TABS)}')
