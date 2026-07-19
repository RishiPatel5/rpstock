import os

# ── Telegram Bot Config ───────────────────────────────────────────────────────
# Reads from environment variables (set as GitHub repo secrets).
# Locally you can export them in your shell, or paste values directly here.
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID",   "YOUR_CHAT_ID_HERE")

# ── Scanner Settings ──────────────────────────────────────────────────────────
# How far below ATH triggers an alert (0.50 = 50% below ATH)
ATH_DROP_THRESHOLD = 0.50

# How often to scan (minutes) — used for local continuous mode only
SCAN_INTERVAL_MINUTES = 1440  # 24 hours

# ── Top 100 Global Stocks (Yahoo Finance tickers) ────────────────────────────
TOP_100_TICKERS = [
    # US Mega-caps
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "BRK-B", "TSLA", "AVGO", "JPM",
    "V", "WMT", "MA", "UNH", "XOM", "ORCL", "LLY", "HD", "COST", "PG",
    "BAC", "NFLX", "MRK", "ABBV", "CVX", "KO", "CSCO", "WFC", "ACN", "CRM",
    "MCD", "TMO", "IBM", "ABT", "LIN", "PM", "PEP", "AMD", "DHR", "GE",
    "CAT", "TXN", "MS", "AXP", "ISRG", "SPGI", "BX", "PLD", "RTX", "BLK",
    "NOW", "PANW", "AMAT", "ADI", "LRCX", "KLAC", "MSTR", "COIN", "PLTR", "HOOD",
    # International (listed on US exchanges or with .L / .PA etc via yfinance)
    "TSM",   # Taiwan Semiconductor
    "ASML",  # ASML Holding
    "SAP",   # SAP SE
    "TM",    # Toyota
    "NVO",   # Novo Nordisk
    "SHEL",  # Shell
    "AZN",   # AstraZeneca
    "LVMUY", # LVMH
    "IDEXY", # IDEX (Prosus)
    "RHHBY", # Roche
    "NSRGY", # Nestlé
    "SIEGY", # Siemens
    "TCEHY", # Tencent
    "BABA",  # Alibaba
    "JD",    # JD.com
    "PDD",   # PDD Holdings
    "BIDU",  # Baidu
    "NTE",   # NovaTek
    "SNY",   # Sanofi
    "GSK",   # GSK
    "BP",    # BP
    "RIO",   # Rio Tinto
    "BHP",   # BHP
    "VALE",  # Vale
    "RELIANCE.NS", # Reliance Industries
    "HDFCBANK.NS", # HDFC Bank
    "TCS.NS",      # Tata Consultancy
    "INFY",        # Infosys
    "SONY",        # Sony
    "9984.T",      # SoftBank
    "7203.T",      # Toyota (Tokyo)
    "005930.KS",   # Samsung Electronics
    "000660.KS",   # SK Hynix
]
