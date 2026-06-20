---
title: Which Technical Analysis to Use (and how)
tags: [screener, technical-analysis, vwap, rsi, volume-profile, order-flow, price-action]
created: 2026-06-21
status: core
---

# 🧭 Which Technical Analysis to Use — and where it belongs in the funnel

> The screener does **not** replace your method — it **feeds** it. This note maps the
> analysis you already use (VWAP, MAs, RSI, volume profile, footprint/order-flow, price
> action) onto the screener funnel: what's a **scan filter** (mechanical, runs on the
> universe) vs a **confirmation tool** (manual, on the shortlist). Ties to your
> [[order-flow]], [[price-action]], and [[trading]] skills.

---

## The two-layer rule
```
  SCAN LAYER  (mechanical, on the whole F&O universe)  →  5–10 candidates
        │   filters that a screener can compute: VWAP, MAs, RSI, relative volume, ATR, ORB
        ▼
  CONFIRM LAYER  (manual, on the shortlist, eyes-on)   →  the actual trade
            volume profile · footprint/CVD · price action · order flow
```
**Why split it:** a screener can compute VWAP/MA/RSI/relative-volume across 200 stocks in milliseconds, but it **cannot** reliably read a footprint absorption or a clean price-action rejection. So you scan with the mechanical tools and **confirm with your discretionary edge.**

## Layer 1 — Scan filters (mechanical, in the screener)
| Tool | As a scan filter | Long / short logic |
|------|------------------|--------------------|
| **VWAP** | the institutional fair-value line | long bias `close > vwap`, short bias `close < vwap` (intraday TF) |
| **MAs (EMA 9/20/50)** | trend alignment | long `ema9>ema20>ema50 & close>ema9`; short the mirror |
| **RSI(14)** | momentum gate | igniting `crossed above 60` (long) / `below 40` (short); flag <30 / >70 for reversal scans |
| **Relative volume** | "is it in play?" | `volume > 2× sma(volume,20)` — the single best intraday filter |
| **ATR / ATR%** | enough range to trade | floor on ATR% so the move pays |
| **ORB / prev-day H-L** | structural breakout | `close > day-high(15m)` / `> 1-day-ago high` (and mirrors) |
| **Relative strength vs Nifty** | leaders & laggards | strongest-in-strong-sector long; weakest-in-weak short ([[08 — Sector Rotation & Relative Strength]]) |

These are exactly the filters in [[03 — Long Scans — Breakout & Bounce]] / [[04 — Short Scans — Breakdown & Reversal-Down]].

## Layer 2 — Confirmation tools (manual, your edge)
Once the screener hands you 5–10 names, **you** confirm with the discretionary read the screener can't do:

- **Volume Profile** — is price at a meaningful node? VAH/VAL/POC/LVN give the *location*. Long breakouts work off LVN/value-edge expansion; fades work at VAH/VAL. (Your [[order-flow]] skill: **location first, delta second**.)
- **Footprint / CVD (order flow)** — at the level, is there **absorption** (effort vs result) or **delta confirmation**? ⚠️ On NSE this is **reconstructed (tick-rule ~85%)** — use it as confluence, never proof, and on 5m/15m not 1m (your `research-tick-aggressor-india` and `research-volumeprofile-footprint-india`). **No clean API gives this — read it manually in GoCharting/your platform** ([[10 — APIs (broker + data)]]).
- **Price action** — the actual trigger: a clean break-and-hold, a hammer/engulfing at support, a failed-breakout reversal. From your [[price-action]] skill — candles read in **context + location + confluence**, never in isolation.
- **VWAP (again, manual)** — the intraday anchor for entries: pullback-to-VWAP longs above it, rejection-from-VWAP shorts below it.

## The clean division of labor
| | Screener (mechanical) | You (discretionary) |
|---|---|---|
| VWAP, MA, RSI, rel-vol, ATR, ORB, RS | ✅ filters the universe | reads the live nuance |
| Volume Profile location | rough (HVN/LVN) | ✅ precise read |
| Footprint / CVD / absorption | ❌ (no NSE aggressor API) | ✅ manual, your edge |
| Price-action trigger | ❌ | ✅ the actual entry |

## The honest point
> The screener's job is to **shrink 200 stocks to 5–10 "in-play" candidates** using mechanical
> filters. Your **order-flow + price-action edge** picks the 1–2 you actually trade and times
> the entry. Don't ask the screener to do your judgment; don't do the screener's mechanical
> filtering by hand. → routine in [[14 — Pre-Market Routine & Watchlist Building]], evidence in [[16 — Evidence & Pitfalls]].
