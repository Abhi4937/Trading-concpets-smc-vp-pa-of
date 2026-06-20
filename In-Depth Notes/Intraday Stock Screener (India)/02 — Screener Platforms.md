---
title: "02 — Screener Platforms"
tags: [intraday, screener, india, chartink, tradingview, tools]
created: 2026-06-21
---

# 02 — Screener Platforms

A map of every major Indian-market screener, what it actually does, and where it fits in an intraday workflow. Not all tools marketed as "screeners" are equal — some are charting tools, some are fundamentals databases, and only a handful are usable for live intraday scanning.

---

## Comparison Table

| Platform | Real-time? | Intraday scans | Custom formula | Best use-case |
|---|---|---|---|---|
| **Chartink** | Free = ~15 min delay; paid = near-RT | Yes (daily + intraday TFs) | Yes — full scan builder | Primary free intraday screener |
| **TradingView** | Paid plan (live NSE feed) | Yes | Yes + Pine alerts | Paid intraday / global stocks |
| **Trendlyne** | Delayed | Partial (alerts, prebuilt) | Limited | EOD prep, DVM scoring |
| **Tickertape** | Delayed | Weak | Limited | Investors, not intraday |
| **StockEdge** | EOD only | No (EOD combos only) | Combo scans | Morning prep, sectoral reads |
| **Screener.in** | N/A | No | No | Fundamentals only |
| **GoCharting** | N/A | No — charting tool | No | Order-flow/footprint charts |

---

## Per-Platform Breakdown

### Chartink
The de-facto standard for free intraday screening in India. A web-based scan builder where every OHLCV attribute accepts an offset prefix: `latest` = current candle; `1 day ago` = previous candle. This offset syntax is the core of the platform.

Example gap-up scan:
```
Latest Open > 1 day ago Close * 1.03
```

Supported indicators include SMA, EMA, WMA, TMA, RSI, MACD, ADX, Bollinger Bands, ATR, and Supertrend — parameters passed in parentheses, e.g. `RSI(close,14)`. Timeframes span daily, weekly, monthly, and multiple intraday intervals.

Critical caveat: **the free tier is approximately 15 minutes delayed**. For intraday use, a gap-up scan run at 9:30 IST on free data reflects prices from ~9:15 — still useful for first-pass filtering, but never treat it as real-time. Paid tiers remove this lag. A large community of shared public scans exists, and open-source scrapers/automators are available (see [[12 — GitHub Tool Deep-Dives]]).

Scans feed directly into the long and short setups in [[03 — Long Scans — Breakout & Bounce]].

### TradingView
Strong technical filter set with Pine Script-based alerts. The built-in screener covers NSE/BSE stocks but **live NSE data requires a paid plan** — on the free tier, data is delayed. For traders who already pay for TradingView Pro+, this is a capable intraday tool with tighter integration between alert and chart. Global coverage is an advantage when cross-referencing sectoral moves.

### Trendlyne
Screener, analytics platform, and broker-integration layer combined. Known for the DVM score (Durability / Valuation / Momentum) and prebuilt screens for earnings, promoter pledging, and technical signals. Alerts can be set on DVM thresholds. Useful for EOD watchlist building and morning preparation rather than live intraday scanning.

### Tickertape
Clean, modern UI with a filter-based screener. Skews heavily toward investing/fundamental metrics (P/E, ROE, debt). Intraday filter capability is limited. Not a primary intraday tool.

### StockEdge
Mobile-first platform built around end-of-day "combo scans" that combine price action with delivery quantity, FII/DII activity, and sectoral data. No intraday scanning. Primary value is structured morning-prep workflows and sector-rotation reads.

### Screener.in
Pure fundamentals database (income statement, balance sheet, cash flow). Not relevant for intraday. Included here only to prevent confusion — the name creates false expectations.

### GoCharting
A charting platform specialising in order-flow, footprint charts, and volume profile — **not a stock screener**. It has no public data API and no scan functionality. Use it manually for order-flow confirmation on a specific name after the screener has already surfaced it. Cross-ref [[13 — Which Technical Analysis to Use]] for when footprint adds signal.

---

## Which to Use for Intraday

- **Primary scanner (free):** Chartink — accept the 15-minute delay; run scans at 9:30–9:45 IST for opening-range setups, refresh at 10:15 for second-wave entries.
- **Primary scanner (paid):** TradingView with a live NSE data add-on, or Chartink paid tier.
- **EOD/morning prep:** StockEdge (combo scans) + Trendlyne (DVM momentum list).
- **Broker-integrated alerts:** Trendlyne if your broker is supported.
- **Order-flow confirmation:** GoCharting manually — not a screener, not automatable.

For broker and data feed connections that power these platforms, see [[10 — APIs (broker + data)]].

---

## Limitations

- **Chartink free delay** is the single biggest operational risk for intraday traders who do not upgrade. A 15-minute-old gap-up is not a gap-up — the move may have already reversed.
- **No platform provides real-time Level 2 / market-depth scanning** in the free tier; depth data requires direct broker API access.
- **Backtesting is absent** across all platforms listed above — you cannot test scan performance historically within the tool. Backtesting requires exporting data and using external scripts (see [[12 — GitHub Tool Deep-Dives]]).
- **Alert reliability varies** — TradingView and Trendlyne alerts have documented lag under high-volatility conditions; never treat an alert as a trigger, only as a prompt to look at the chart.
