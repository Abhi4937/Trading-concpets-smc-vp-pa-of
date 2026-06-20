---
title: "10 — APIs (Broker + Data)"
tags: [intraday, screener, india, api, broker, data-feed, websocket]
created: 2026-06-21
---

# 10 — APIs (Broker + Data)

Building a live intraday screener requires two things: a **real-time feed** (websocket ticks or 1-min candles) and **historical OHLCV** for lookback calculations (EMA seeds, relative volume baseline, etc.). India's landscape has shifted heavily in favour of free broker APIs — paid third-party feeds are only worth it if you need tick-level reliability at scale.

---

## Comparison Table

| Provider | Type | Live Websocket | Market Depth | Historical OHLCV | Cost | Notes |
|---|---|---|---|---|---|---|
| **Zerodha Kite Connect** | Broker | Yes (tick + OHLC mode) | Up to 5 levels | Yes (1m–day, add-on) | ~₹2,000/mo + historical add-on | Most popular; best docs; largest community; historical is a separate paid add-on |
| **Upstox API** | Broker | Yes | Full depth (20 levels) | Yes | Free | Full market depth is the standout — closest you get to order-flow reconstruction on NSE |
| **Angel One SmartAPI** | Broker | Yes | Yes | Yes | Free | Instrument master included; straightforward REST + websocket |
| **Dhan API** | Broker | Yes | Yes | Yes | Free | Strong retail-algo community; clean docs; reliable uptime reports |
| **Fyers API** | Broker | Yes | Yes | Yes | Free | Charting-library-friendly design; good for Python integration |
| **ICICI Direct Breeze** | Broker | Yes | Partial | Yes | Free | Established broker; API maturity lags pure-play fintechs |
| **5paisa API** | Broker | Yes | Partial | Yes | Free | Adequate; smaller community |
| **TrueData** | Third-party | Yes (tick + 1-min) | No | Yes | Paid (tiered) | Preferred by serious intraday and order-flow traders; high reliability; tick data is clean |
| **GlobalDataFeeds (GFDL)** | Third-party | Yes | No | Yes | Paid | Powers many charting platforms; solid uptime; no aggressor-side data (see below) |
| **Alpha Vantage** | Third-party | No | No | Limited (.NSE) | Free (rate-limited) | NSE coverage is thin and unreliable; avoid for live screeners |
| **yfinance (.NS tickers)** | Unofficial | No | No | EOD + spotty intraday | Free | Unofficial scraper; gaps and delays are common intraday; fine for **EOD prototyping only** |
| **Chartink scan export** | Screener | No | No | No | Free (community scrapers) | Pull pre-built scan results; useful for EOD watchlist seeding, not live streaming |

---

## Practical Guidance

### For a live intraday screener (F&O universe)

A **free broker websocket — Dhan, Upstox, Angel SmartAPI, or Fyers** — is the practical default. The workflow:

1. Pull the F&O instrument list (~200 active symbols) from the broker's instrument master or from [[09 — NSE Data Sources]] (bhavcopy/GICS lists).
2. Subscribe to all symbols via the websocket in **OHLC/1-min mode** (not raw tick, to keep bandwidth manageable).
3. Compute live: VWAP, EMA(9/21), RSI(14), relative-volume (current vol vs. N-day average at the same time of day).
4. Emit a ranked watchlist — top movers, VWAP reclaims, volume spikes — refreshed every candle close.

Zerodha Kite is the most battle-tested choice if you are already a Kite user and can absorb the fee. Upstox is the best free option if you want **full 20-level depth** for any order-flow-ish analysis.

### For EOD preparation

Use jugaad-data, bhavcopy, or NSE direct downloads ([[09 — NSE Data Sources]]) to build your relative-volume baseline and screen candidates the night before.

### Order-flow / footprint — the hard truth

NSE does **not** publish aggressor-side (bid-initiated vs. ask-initiated) volume via any public API. TrueData and GFDL give you tick-by-tick price and volume but not the taker side. If you want footprint delta you must **reconstruct it yourself**: compare each tick's price to the previous bid/ask midpoint and classify it as buy or sell aggression. This is noisy and requires raw tick data — see [[13 — Which Technical Analysis to Use]] for whether this effort is worth it at your trading frequency.

---

## Related Notes

- [[09 — NSE Data Sources]] — bhavcopy, OI data, instrument masters
- [[11 — Build Your Own Screener]] — architecture, code skeleton
- [[13 — Which Technical Analysis to Use]] — VWAP, relative volume, RSI vs. order-flow
