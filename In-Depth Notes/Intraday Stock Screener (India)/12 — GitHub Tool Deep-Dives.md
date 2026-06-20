---
title: "12 — GitHub Tool Deep-Dives"
tags: [screener, open-source, NSE, India, python, tools]
created: 2026-06-21
---

# 12 — GitHub Tool Deep-Dives

A curated map of the best open-source NSE screener and supporting repos, verified via GitHub API on 2026-06-21. See [[02 — Screener Platforms]] for hosted alternatives and [[11 — Build Your Own Screener]] for how to wire these together.

---

## Ranked Table

| Rank | Repo | Stars | Language | Data Source | What It Screens | Maintained? |
|------|------|-------|----------|-------------|-----------------|-------------|
| 1 | [pkjmesra/PKScreener](https://github.com/pkjmesra/PKScreener) | 357 | Python | NSE direct + nsepython | 33+ scanners: breakout/breakdown, momentum, MA, volume, patterns, AI | Yes — Jun 2026 |
| 2 | [pranjal-joshi/Screeni-py](https://github.com/pranjal-joshi/Screeni-py) | 689 | Python | NSE direct | Breakouts, RSI, MA crossovers, candlestick patterns, relative volume | Yes — v3.0.2 Jun 2026 |
| 3 | [BennyThadikaran/eod2](https://github.com/BennyThadikaran/eod2) | 150 | Python | NSE EOD | Data pipeline — delivery, index, EOD (not a screener itself) | Yes |
| 4 | [marketcalls/openalgo](https://github.com/marketcalls/openalgo) | 2112 | Python | Broker APIs | Execution layer (not a screener — pairs with output of above) | Yes |
| 5 | [deshwalmahesh/NSE-Stock-Scanner](https://github.com/deshwalmahesh/NSE-Stock-Scanner) | 320 | Jupyter/Python | NSE live | General long/short scan with live data | Partial |
| 6 | [JittoJoseph/Hummingbird-Project](https://github.com/JittoJoseph/Hummingbird-Project) | — | Java | Upstox V3 API | ORB: relative-volume filter, pre-market ATR, opening-range | Yes |
| 7 | [sgprasad66/ChartInkScreenerScraper](https://github.com/sgprasad66/ChartInkScreenerScraper) | 39 | Python | Chartink (scraped) | Scrapes hosted Chartink scans | Stale |
| 8 | [bogadib/chartink_kite_amo_mean_reversion](https://github.com/bogadib/chartink_kite_amo_mean_reversion) | — | Python | Chartink → Zerodha | Mean-reversion AMO order placement | Stale |
| 9 | [smohapatraa/nse_stock_scanner](https://github.com/smohapatraa/nse_stock_scanner) | — | Python | NSE | Daily long & short scan | Unknown |
| 10 | [TechfaneTechnologies/nse](https://github.com/TechfaneTechnologies/nse) | — | Rust | NSE real-time | Real-time data extractor | Unknown |

---

## Deep Dives

### 1. PKScreener — Most Complete OSS NSE Screener

**https://github.com/pkjmesra/PKScreener** | 357 stars | Python | PyPI / Docker / binaries / Telegram bot

Self-described "India's #1 open-source NSE screener" and it largely earns that. With 33+ named scanners it covers both LONG (probable breakouts, 52-week highs) and SHORT (probable breakdowns, 52-week lows) — a distinction most OSS screeners ignore. Filters span RSI, MFI, CCI momentum, all common MA signals, volume gainers, narrow-range bars (NR4/NR7), inside bars, MACD, Aroon crossover, and a full candlestick/chart-pattern library. An AI layer and built-in backtesting module push it well beyond a basic scan tool. The Telegram bot makes it usable without touching code. **Start here if you want breadth.**

### 2. Screeni-py — Cleanest Breakout GUI

**https://github.com/pranjal-joshi/Screeni-py** | 689 stars | Python | Docker / Streamlit GUI

More opinionated and visually polished than PKScreener. Its core thesis is breakout-probability: for each candidate it computes the breakout level over N days, projects the next resistance, and layers in relative volume vs. the 20-period MA, RSI(14), 50/200 MA/EMA crossovers, and pattern detection (Inside Bar, Bullish Engulfing, Momentum Gainer). Data is pulled directly from NSE — no third-party feed required. The Docker + Streamlit packaging makes it the easiest repo to demo on a new machine. **Short-side support is limited; this is a long/breakout tool.** Use it when you want a GUI and a clean institutional-grade breakout filter.

### 3. eod2 — The Data Layer

**https://github.com/BennyThadikaran/eod2** | 150 stars | Python

Not a screener — a disciplined automated pipeline for downloading and keeping NSE EOD data current, including delivery volumes and index data. This is the missing piece most DIY screeners suffer from: clean, locally stored, consistently updated historical data. Pair eod2 as the data layer underneath any custom screener you build (see [[11 — Build Your Own Screener]]). Prefer **jugaad-data** or **nsepython** for live intraday feeds; **nsepy is deprecated** and should not be used in new projects.

### 4. openalgo — Execution Layer

**https://github.com/marketcalls/openalgo** | 2112 stars | Python

Not a screener at all — it is a broker-agnostic algo-trading platform that normalises order-routing across Zerodha, Fyers, AngelOne, and many other Indian brokers behind a single REST API. Its relevance here: once PKScreener or Screeni-py surfaces a candidate, openalgo is the cleanest OSS path to actual order placement. The star count (highest in the table by far) reflects how broadly the Indian retail-algo community has adopted it.

### 5. Chartink-to-Broker Pattern

**sgprasad66/ChartInkScreenerScraper** and **bogadib/chartink_kite_amo_mean_reversion** represent a pattern that many Indian retail algo traders use: scrape a hosted Chartink scanner (e.g. the popular "Vishal Mehta Mean Reversion" scan) and automatically place AMO or intraday orders via Zerodha KiteConnect. Both repos are partially stale but the pattern itself is sound — replace the scraper with the official Chartink alert webhook if you have a paid plan.

### 6. Hummingbird-Project — Java ORB System

**https://github.com/JittoJoseph/Hummingbird-Project** | Java | Upstox V3 API

Unusual in being Java-based. Implements a disciplined Opening Range Breakout pipeline: a pre-market filter on price, volume, and ATR narrows the universe, a relative-volume gate (relVol >= 100%) picks the top 20 movers, and the first-five-minute range is locked as the "Stocks in Play" opening range. A useful reference for anyone building an ORB system against the Upstox API specifically.

---

## Data-Source Reminder

> Prefer **jugaad-data** or **nsepython** for live/historical NSE data in new projects. **nsepy is unmaintained and broken on current NSE endpoints — do not use it.**
