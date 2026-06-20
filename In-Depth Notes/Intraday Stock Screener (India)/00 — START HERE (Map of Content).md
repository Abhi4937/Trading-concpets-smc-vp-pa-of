---
title: Intraday Stock Screener (India) — Map of Content
tags: [moc, screener, intraday, nse, india, index]
created: 2026-06-21
status: living-document
---

# 🗺️ Intraday Stock Screener (India) — START HERE

> A complete system for **finding stocks to trade intraday** on NSE — both **long
> (breakout/bounce)** and **short (breakdown/reversal)** — what parameters to scan, which
> index/stocks, what NSE data & APIs to use, how to build your own, and how it feeds your
> existing options Decision Engine. Built to **shrink ~2,000 stocks to 5–10 in-play names a day.**
>
> Researched from screener platforms, open-source GitHub repos (source-verified), and your
> existing vault. Where data reliability matters it's flagged.

---

## 📚 The vault (read in funnel order)

### Foundation
- [[01 — How Screeners Work + The Daily Workflow]] — the mental model + end-to-end flow

### The funnel
- **②a Platforms** → [[02 — Screener Platforms]] (Chartink, Trendlyne, TradingView, StockEdge, GoCharting)
- **① Universe** → [[06 — Liquidity & Tradability Filters]] · [[07 — Index & Stock Universe]]
- **② Setups** → [[03 — Long Scans — Breakout & Bounce]] · [[04 — Short Scans — Breakdown & Reversal-Down]] · [[05 — Reversal Scans]]
- **③ Rank** → [[08 — Sector Rotation & Relative Strength]]
- **④ Confirm** → [[13 — Which Technical Analysis to Use]] (maps your VWAP/MA/RSI/VP/footprint/order-flow/price-action)

### Data & building it
- [[09 — NSE Data Sources]] (bhavcopy, option chain, delivery, pre-open; nsepython/jugaad-data)
- [[10 — APIs (broker + data)]] (Kite, Upstox, SmartAPI, Dhan, Fyers; TrueData; the GoCharting/order-flow reality)
- [[11 — Build Your Own Screener]] (Python + API, end-to-end skeleton)
- [[12 — GitHub Tool Deep-Dives]] (PKScreener, Screeni-py, eod2, openalgo, Hummingbird…)

### Running it & the truth
- [[14 — Pre-Market Routine & Watchlist Building]] (the clock-by-clock morning routine)
- [[15 — Shorting Rules (margin, square-off, T2T-ASM)]] (can you short? same margin? the rules)
- [[16 — Evidence & Pitfalls]] (what works vs marketing)
- [[17 — Integration with the Decision Engine]] (screener → options play)

---

## ⚡ The 60-second answer to "give me stocks to trade intraday"

1. **Universe:** scan only the **F&O-eligible ~180–220 stocks** (liquid, tight-spread, shortable). Not all 2,000. → [[07 — Index & Stock Universe]]
2. **In-play filter:** keep names with **relative volume > 2×** average — the single best "is it tradable today?" filter. → [[06 — Liquidity & Tradability Filters]]
3. **Direction filter:** **above VWAP + EMA-stacked-up + RS leader** = long; mirror = short. → [[03]] / [[04]]
4. **Rank:** strongest stock in the **strongest sector** (long), weakest in the weakest (short). → [[08 — Sector Rotation & Relative Strength]]
5. **Confirm** the 5–10 hits manually with **volume profile + order flow + price action** — the screener can't do this; it's your edge. → [[13 — Which Technical Analysis to Use]]

## ✅ Can you short? Yes
Intraday short is allowed with the **same margin as long** (MIS, square off same day, shortable/F&O names only). The screener runs **two-sided** every day. Rules → [[15 — Shorting Rules (margin, square-off, T2T-ASM)]].

## 🔑 The one thing to remember
> **A screener narrows; it doesn't predict.** Its job is to hand you a *small, tradable* watchlist;
> the edge lives in your **selectivity, confirmation, and risk** — not the scan. A screen that
> gives you 50 signals a day will hurt you (frequency kills — see [[16 — Evidence & Pitfalls]]).

## 🧭 Honesty notes
- **Chartink free = ~15-min delayed** — fine for prep, not for live triggers (use a broker API or paid real-time).
- **NSE has no real-time public API and no true order-flow/aggressor data** — footprint/CVD is reconstructed (tick-rule ~85%); read it manually, use as confluence only.
- **nsepy is deprecated** → use jugaad-data / nsepython.
- The screener feeds — it doesn't replace — your [[Strategies/Intraday Options Decision Engine/note|Decision Engine]] and [[order-flow]] / [[price-action]] skills.
