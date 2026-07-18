# ATH Drop Scanner 📉🔔

Scans the **top ~100 global stocks** every hour using Yahoo Finance data.  
When any stock drops **50% or more from its all-time high (5-year)**, you get a **Telegram notification** instantly.

---

## Setup (2 minutes)

### 1 — Create a Telegram Bot (free)

1. Open Telegram → search **@BotFather** → `/newbot`
2. Copy your **BOT_TOKEN** (looks like `123456:ABCdef...`)
3. Start a chat with your new bot
4. Visit this URL in your browser to get your **CHAT_ID**:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
   Look for `"chat":{"id":XXXXXXX}` in the response

### 2 — Configure

Edit `config.py`:

```python
TELEGRAM_BOT_TOKEN = "123456:ABCdef..."   # from BotFather
TELEGRAM_CHAT_ID   = "987654321"          # your chat ID
```

You can also tweak:
- `ATH_DROP_THRESHOLD = 0.50` → alert when 50%+ below ATH (change to 0.40 for 40%, etc.)
- `SCAN_INTERVAL_MINUTES = 60` → how often to scan

### 3 — Install dependencies

```bash
pip install yfinance requests schedule
```

### 4 — Run

```bash
# Continuous (scans every hour forever):
python scanner.py

# Single scan then exit:
python scanner.py --once
```

---

## What it does

| Step | Detail |
|------|--------|
| 📡 Fetch | Downloads 5-year price history for each ticker via Yahoo Finance (free, no API key) |
| 📊 Calculate | Finds the highest price in 5 years (ATH) vs current close price |
| 🚨 Alert | If `(ATH - current) / ATH ≥ 50%`, fires a Telegram message |
| ⏱ Schedule | Re-runs every 60 minutes (configurable) |
| ✅ Summary | Sends a scan summary after every run |

---

## Example Telegram Alert

```
🚨 ATH DROP ALERT

📉 BABA
Current price : USD 78.50
All-Time High : USD 317.14
Drop from ATH : -75.2%

⚠️ This stock is ≥50% below its 5-year ATH.
🕒 Scanned at 18 Jul 2026 14:00
```

---

## Customise Tickers

Edit the `TOP_100_TICKERS` list in `config.py` — any Yahoo Finance ticker works (e.g. `AAPL`, `9984.T`, `005930.KS`, `RELIANCE.NS`).

---

## Run as a background service (macOS)

```bash
nohup python scanner.py > scanner.log 2>&1 &
echo "Scanner running in background. PID: $!"
```

To stop it: `kill <PID>`
