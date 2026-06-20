---
title: How Screeners Work + The Daily Workflow
tags: [screener, workflow, foundation, intraday]
created: 2026-06-21
status: foundation
---

# ⚙️ How Screeners Work + The Daily Workflow

> A screener is a **filter funnel**: it takes the full stock universe and mechanically keeps
> only those matching your conditions, so you start the day with **5–10 tradable names instead
> of 2,000.** It finds *candidates* — it does not make decisions. This note is the mental model
> and the end-to-end flow; every stage links to its deep-dive.

---

## What a screener actually does
```
   ~2000 NSE stocks
        │  ① UNIVERSE filter  →  keep liquid, tradable, shortable names (F&O ~180–220)
        ▼
   ~200 stocks
        │  ② SETUP filter     →  keep only those matching a scan (breakout / breakdown / reversal)
        ▼
   ~20–40 hits
        │  ③ RANK             →  by relative strength + relative volume + sector
        ▼
   5–10 watchlist names  →  ④ CONFIRM manually (VP / order-flow / price action)  →  trade
```
Each stage is a note:
1. **Universe** → [[06 — Liquidity & Tradability Filters]] + [[07 — Index & Stock Universe]]
2. **Setup** → [[03 — Long Scans — Breakout & Bounce]] · [[04 — Short Scans — Breakdown & Reversal-Down]] · [[05 — Reversal Scans]]
3. **Rank** → [[08 — Sector Rotation & Relative Strength]]
4. **Confirm** → [[13 — Which Technical Analysis to Use]]

## The two ways to run it
- **Hosted (no code):** Chartink (free, ~15-min delay), TradingView (paid, real-time), StockEdge/Trendlyne — build/borrow a scan, run it, read the results. → [[02 — Screener Platforms]]
- **Programmatic (your own):** pull the F&O universe + data (jugaad-data/broker API), compute filters in Python, output a ranked watchlist. → [[09 — NSE Data Sources]] · [[10 — APIs (broker + data)]] · [[11 — Build Your Own Screener]] · open-source templates in [[12 — GitHub Tool Deep-Dives]]

## The core mental model (read this twice)
> **A screener narrows; it does not predict.** It answers *"which stocks are in play and match
> my setup right now?"* — not *"which will go up."* The edge is never the scan (anyone can copy a
> Chartink screen); the edge is **selectivity + confirmation + risk** on the handful it surfaces.
> See [[16 — Evidence & Pitfalls]].

## The daily workflow (compressed)
1. **Pre-market** — global cues, GIFT Nifty, news, F&O ban list, pre-open gap lists. → [[14 — Pre-Market Routine & Watchlist Building]]
2. **9:15–9:30** — let the opening range form; mark levels.
3. **9:30+** — run the scan on the F&O universe → rank by RS + relative volume → **5–10 names** (longs + shorts).
4. **Confirm** each at its level with volume profile / order-flow / price action.
5. **Trade** the A+ ones — the stock intraday (MIS) or the index via options → [[17 — Integration with the Decision Engine]].

## Long *and* short, every day
Indian intraday allows shorting with the **same margin as long** (MIS, square off same day, shortable names only) — so the screener runs **two-sided**: strongest names for longs, weakest for shorts. Rules: [[15 — Shorting Rules (margin, square-off, T2T-ASM)]].

→ Start here, then follow the funnel notes in order. Honest expectations: [[16 — Evidence & Pitfalls]].
