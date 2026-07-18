#!/usr/bin/env python3
"""
ATH Drop Scanner
────────────────
Scans the top 100 global stocks every hour.
If a stock is ≥ 50% below its all-time high, sends a Telegram alert.

Usage:
    python scanner.py          # runs continuously
    python scanner.py --once   # single scan then exit
"""

import sys
import time
import logging
from datetime import datetime

import requests
import schedule
import yfinance as yf

from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    ATH_DROP_THRESHOLD,
    SCAN_INTERVAL_MINUTES,
    TOP_100_TICKERS,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# Track which tickers we've already alerted on (reset each run)
alerted: set[str] = set()


# ── Telegram ──────────────────────────────────────────────────────────────────

def send_telegram(message: str) -> bool:
    """Send a message via the Telegram Bot API."""
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        log.warning("Telegram not configured – printing alert instead.")
        print("\n🔔 ALERT:\n" + message + "\n")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        return True
    except Exception as e:
        log.error("Telegram send failed: %s", e)
        return False


# ── Data Fetching ─────────────────────────────────────────────────────────────

def get_ath_and_current(ticker: str) -> tuple[float, float, str] | None:
    """
    Returns (ath_price, current_price, currency) for a ticker, or None on error.
    Uses full max history to get the true All-Time High.
    """
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="max", auto_adjust=True)
        if hist.empty:
            return None
        ath = float(hist["High"].max())
        current = float(hist["Close"].iloc[-1])
        info = t.fast_info
        currency = getattr(info, "currency", "USD") or "USD"
        try:
            info_full = t.info
            name = info_full.get("longName") or info_full.get("shortName") or ticker
            sector = info_full.get("sector", "")
            summary_text = info_full.get("longBusinessSummary", "")
            # Trim summary to first sentence
            short_summary = summary_text.split(".")[0] + "." if summary_text else ""
        except Exception:
            name = ticker
            sector = ""
            short_summary = ""
        return ath, current, currency, name, sector, short_summary
    except Exception as e:
        log.debug("Failed fetching %s: %s", ticker, e)
        return None


# ── Core Scanner ──────────────────────────────────────────────────────────────

def scan():
    global alerted

    now = datetime.now().strftime("%d %b %Y %H:%M")
    log.info("Starting scan – %d tickers …", len(TOP_100_TICKERS))

    alerts = []
    errors = []

    for ticker in TOP_100_TICKERS:
        result = get_ath_and_current(ticker)
        if result is None:
            errors.append(ticker)
            continue

        ath, current, currency, name, sector, short_summary = result

        if ath <= 0:
            continue

        drop_pct = (ath - current) / ath  # e.g. 0.52 = 52% below ATH

        log.info(
            "%-20s  current=%-10.2f  ATH=%-10.2f  drop=%.1f%%",
            ticker, current, ath, drop_pct * 100,
        )

        if drop_pct >= ATH_DROP_THRESHOLD and ticker not in alerted:
            alerts.append({
                "ticker": ticker,
                "name": name,
                "sector": sector,
                "summary": short_summary,
                "current": current,
                "ath": ath,
                "drop_pct": drop_pct * 100,
                "currency": currency,
            })
            alerted.add(ticker)

    # Send individual alerts
    for a in alerts:
        msg = (
            f"🚨 <b>ATH DROP ALERT</b>\n\n"
            f"<b>{a['ticker']}</b> — {a['name']}\n"
            f"Sector        : {a['sector'] or 'N/A'}\n"
            f"About         : {a['summary'] or 'N/A'}\n\n"
            f"Current price : <b>{a['currency']} {a['current']:,.2f}</b>\n"
            f"All-Time High : <b>{a['currency']} {a['ath']:,.2f}</b>\n"
            f"Drop from ATH : <b>-{a['drop_pct']:.1f}%</b>\n\n"
            f"This stock is ≥{ATH_DROP_THRESHOLD*100:.0f}% below its All-Time High.\n"
            f"Scanned at {now}"
        )
        sent = send_telegram(msg)
        log.info("ALERT sent (%s): %s  drop=%.1f%%", "✓" if sent else "print", a["ticker"], a["drop_pct"])

    # Summary message
    summary = (
        f"<b>Scan complete</b> — {now}\n"
        f"Tickers scanned : {len(TOP_100_TICKERS)}\n"
        f"Alerts fired    : {len(alerts)}\n"
        f"Failed fetches  : {len(errors)}"
    )
    if len(alerts) == 0:
        summary += f"\n\nNo stocks are ≥{ATH_DROP_THRESHOLD*100:.0f}% below ATH right now."
    send_telegram(summary)

    if errors:
        log.warning("Could not fetch: %s", ", ".join(errors))

    log.info("Scan done. Alerts: %d", len(alerts))


# ── Entry Point ───────────────────────────────────────────────────────────────

def main():
    once = "--once" in sys.argv

    log.info("═" * 55)
    log.info("  ATH Drop Scanner  |  threshold: %.0f%%  |  interval: %dmin",
             ATH_DROP_THRESHOLD * 100, SCAN_INTERVAL_MINUTES)
    log.info("═" * 55)

    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        log.warning("Telegram not configured. Edit config.py first.")
        log.warning("   Alerts will be printed to console only.")

    # Run once immediately
    scan()

    if once:
        log.info("--once flag set, exiting.")
        return

    # Then on a schedule
    schedule.every(SCAN_INTERVAL_MINUTES).minutes.do(scan)
    log.info("Scheduler running – scanning every %d min. Ctrl+C to stop.", SCAN_INTERVAL_MINUTES)

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
