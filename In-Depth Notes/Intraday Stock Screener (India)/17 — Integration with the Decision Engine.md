---
title: Integration with the Decision Engine & order-flow vault
tags: [screener, integration, decision-engine, options, workflow]
created: 2026-06-21
status: core
---

# 🔗 Integration — screener → Decision Engine → options

> This vault doesn't stand alone. The screener is the **top of your funnel** — it produces
> the day's tradable stock list. From there it feeds your existing method: the
> [[Strategies/Intraday Options Decision Engine/note|Intraday Options Decision Engine]],
> the [[order-flow]] / [[price-action]] confirmation, and (for the index) the options play.

---

## Where the screener sits in your whole system
```
   SCREENER (this vault)                 →  5–10 in-play stocks (long + short), tagged with levels
        │   F&O universe → filters → RS/rel-vol rank
        ▼
   DECISION ENGINE (existing vault)      →  regime-gate: which play is legal today?
        │   classify the day (trend vs balance), mark qualified levels
        ▼
   ORDER-FLOW / PRICE-ACTION (skills)    →  confirm at the level (VP location + footprint + PA trigger)
        ▼
   EXECUTION                             →  the trade: stock intraday (MIS) OR index options
```

## Two distinct uses of the output
1. **Trading the stock itself, intraday** — long the strongest (MIS), short the weakest (MIS, only shortable names — [[15 — Shorting Rules (margin, square-off, T2T-ASM)]]). The screener gives the name + setup + levels; the Decision Engine's regime logic + your order-flow confirm the entry.
2. **Trading the index via options** — the screener's **breadth and sector read** *informs the index bias*. If the screener shows broad strength (most F&O names long, leaders breaking out, strong sectors leading) → bullish Nifty/BankNifty bias → favors the Decision Engine's long-side plays. Broad weakness → bearish bias. Stock-level relative strength is a **breadth gauge** for the index option trade.

## How the screener maps onto the Decision Engine's five plays
| Screener output | Decision Engine play |
|-----------------|----------------------|
| Breakout long / breakdown short (above/below VWAP, ORB, rel-vol) | **Breakout** (regime: trend/negative-GEX) |
| Failed breakout at prev-day H/L on the watchlist | **Fakeout reversal** (regime: balance/positive-GEX) |
| Oversold/overbought reversal scan hits at a level | **Reversal at exhaustion** |
| Strong stock pulling back to VWAP/EMA20 | **Pullback / continuation** |

So the screener doesn't replace the Decision Engine — it **populates the level map with the right names** before the regime gate decides which play is legal.

## The non-negotiables carry over
The guardrails from your [[trading]] master skill still rule:
- **Futures/stock to read, options to execute** — analyze the stock/index; express via the right vehicle.
- **Selectivity > frequency** — the screener should yield **5–10 names, not 50**. Over-screening = overtrading = the documented killer (your `research-strategy-evidence-and-mastery-roadmap`).
- **Expectancy > win-rate**; **defined-risk on balance days**; **5m/15m, not 1m**; **WAIT is not a signal**.

## The daily handoff (one line)
> **Pre-market screener → watchlist (longs + shorts, with levels) → Decision Engine regime-gate
> → order-flow/price-action confirm → trade the stock (MIS) or the index (options).**

→ The routine that produces the watchlist: [[14 — Pre-Market Routine & Watchlist Building]].
→ What the screener can vs can't do: [[13 — Which Technical Analysis to Use]] and [[16 — Evidence & Pitfalls]].
