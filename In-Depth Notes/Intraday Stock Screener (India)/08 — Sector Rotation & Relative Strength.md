---
title: "08 — Sector Rotation & Relative Strength"
tags: [intraday, screener, sector-rotation, relative-strength, india, nifty]
created: 2026-06-21
---

# 08 — Sector Rotation & Relative Strength

## Core Idea

Money rotates between sectors every single day. The intraday edge is simple: **long the strongest stock in the strongest sector, short the weakest stock in the weakest sector.** You are trading with both the sector tailwind and the individual stock's momentum — double confirmation before you even look at a setup.

See [[07 — Index & Stock Universe]] for how sectoral indices are structured and which stocks belong to each.

---

## Relative Strength (RS) — What It Actually Means

RS measures a stock's (or sector's) performance **relative to a benchmark** (Nifty 50 for stocks; Nifty 50 for sectors).

- **RS-line rising** = the instrument is outperforming the index.
- **RS-line falling** = underperforming; a short candidate.
- **Example**: stock up 2% while Nifty is flat → strong RS. Stock up 0.5% while Nifty is up 1.5% → weak RS even though the stock is green.

**RS is NOT RSI.** RSI is a momentum oscillator (0–100, measures speed of price change internally). RS is a ratio vs an external benchmark. Do not conflate them.

---

## Morning Routine — Step by Step

Run this before 9:20 AM using the NSE sectoral-index dashboard and Trendlyne/TradingView heatmap.

1. **Rank sectoral indices by % change vs previous close.**
   Pull Nifty Bank, Nifty IT, Nifty Auto, Nifty Pharma, Nifty FMCG, Nifty Realty, Nifty Metal, Nifty Energy, and Nifty Infra. Sort descending. The top 1–2 are your **leading sectors**; the bottom 1–2 are your **lagging sectors**.

2. **Within the leading sector, list constituents and filter by RS + volume.**
   Pick stocks showing the highest % gain AND volume above their 5-day average. These are long candidates. Feed them into the breakout or bounce scans from [[03 — Long Scans — Breakout & Bounce]].

3. **Within the lagging sector, pick the weakest constituents.**
   Stocks making new intraday lows, highest % loss, or unable to bounce even when the broader index ticks up. These are short candidates. Cross-check with [[04 — Short Scans — Breakdown & Reversal-Down]].

4. **Confirm the broad market context.**
   Only press longs aggressively if Nifty / the sector index is trending up or at minimum holding flat. Do not fight the tape. If Nifty is selling off hard, even a strong RS stock will struggle — reduce size or wait. See [[14 — Pre-Market Routine & Watchlist Building]] for the full pre-open checklist.

---

## RS Scan Logic (Chartink-Style Proxy)

A simple Chartink filter that proxies RS:

- `% change > [Nifty 50 % change]` — stock moving more than the index
- OR: stock making a **new 15-min high** while Nifty is flat or down — this is true intraday RS and is a very high-quality signal

For shorts, flip it: `% change < [Nifty 50 % change]` and stock making new intraday lows while index is flat or up.

---

## Tools

| Tool | Use |
|---|---|
| NSE Indices page | Live sectoral % change ranking |
| Trendlyne / Ticker Tape heatmap | Visual sector heat, top movers per sector |
| TradingView sector indices | Chart-based RS-line comparison |
| Chartink | Screener filters combining RS proxy + technical conditions |

**Note on Bank Nifty heavyweights**: HDFC Bank, ICICI Bank, SBI, Axis Bank, and Kotak together drive both the Bank Nifty and a significant portion of Nifty 50. When financials lead, the index typically leads. When they lag, treat any broad-market long with extra caution.

---

## Key Caveats

- **Sector leadership can flip intraday.** Re-rank after 10:15–10:30 AM once the opening noise settles. What was weak at open can become the day's leader after a news catalyst.
- **RS is a filter, not a trigger.** Use it to narrow the universe, then wait for a proper price-action setup (breakout, bounce, breakdown) with order-flow or volume confirmation before entering.
- **Avoid the second-best stock.** If the top RS stock has already moved 4%, it is not the same trade. Either wait for a pullback entry or skip and find the next cleanest name in the sector.
