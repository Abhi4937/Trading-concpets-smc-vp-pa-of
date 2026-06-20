---
title: "07 — Index & Stock Universe"
tags:
  - screener
  - universe
  - nse
  - fno
  - india
  - intraday
created: 2026-06-21
---

# 07 — Index & Stock Universe

**Core question: which index and which stocks should I actually scan for intraday?**

---

## The Indices You Need to Know

### Broad-Market Indices (NSE)

| Index | Constituents | Practical use |
|---|---|---|
| **Nifty 50** | 50 most-liquid large caps | Benchmark; trades as an index directly (futures + options) |
| **Nifty 100** | Nifty 50 + Next 50 | Tight, calm intraday universe; good for beginners |
| **Nifty 200** | Top 200 by free-float market cap | Wider, moderate liquidity tail |
| **Nifty 500** | Top 500 — the "broad market" | Full market proxy; mid/small cap tail gets illiquid |
| **Nifty Midcap 100 / 150** | Mid-cap tier | Higher volatility, wider spreads, use only after filtering |
| **Nifty Smallcap 100** | Small-cap tier | Mostly noise for intraday; avoid unless you know the name |

**Rule of thumb**: the further down the cap ladder, the wider the spread, the thinner the book, and the harder it is to size in or out cleanly. See [[06 — Liquidity & Tradability Filters]].

### Sectoral Indices (for rotation reads)

These are not scan universes — they are **thermometers**. Check them every morning to identify which sectors are leading or lagging before you pull stock-level signals.

Bank Nifty · Nifty Financial Services · Nifty IT · Nifty Auto · Nifty Pharma · Nifty FMCG · Nifty Metal · Nifty Energy · Nifty Realty · Nifty PSU Bank · Nifty Media

How to use them → [[08 — Sector Rotation & Relative Strength]].

---

## The Practical Intraday Universe: The F&O List (~180–220 Stocks)

**This is the answer.** Do not scan all 2,000+ NSE-listed stocks. Scan the **derivatives-eligible (F&O) list**.

### Why the F&O list is the right filter

SEBI's criteria for including a stock in the F&O segment effectively pre-select the most institutionally-traded names:

- **Market-wide position limit (MWPL)** — minimum ₹500 cr notional in open interest headroom; filters out illiquid names
- **Median quarter-sigma order size** — a liquidity proxy: the order size required to move the price by 0.25% must exceed ₹25 lakh; eliminates thin-book stocks
- **Average daily delivery value** — minimum ₹10 cr average over the last six months; ensures consistent institutional participation

The practical outcome: every stock on the F&O list has a **tight bid-ask spread**, **sufficient depth to absorb retail size**, and — critically — you can **short it intraday via futures or stock options** without the BTST restriction that hits non-F&O cash positions.

Scanning outside this list is mostly noise: illiquid moves, operator-driven spikes, and setups you cannot safely short.

**Maintenance**: download the current F&O list from NSE's website (`nseindia.com → Derivatives → F&O Securities`). Refresh it monthly — SEBI adds and removes names each expiry cycle.

---

## How to Select the Day's 5–10 Stocks Within the Universe

Running a full 180-stock scan every day is fine as a first pass, but you need to narrow to a **watchlist of 5–10 actionable names** before the open.

1. **Sector rotation read** — identify the 2–3 strongest and 2–3 weakest sectors using the sectoral indices. This determines your bias direction by sector. → [[08 — Sector Rotation & Relative Strength]]

2. **Relative strength within sectors** — within the strongest sector, find the stocks outperforming it; within the weakest sector, find the stocks underperforming it. These are your long and short candidates respectively.

3. **Stocks in play** — apply a **relative volume** filter (today's volume vs. 10-day average at the same time of day; target ≥ 1.5×). High relative volume flags institutional interest and ensures the setup has participation. Typically yields 5–10 clean names.

---

## If You Trade Index Options (Nifty / BankNifty)

The relevant universe shrinks to:

- The **index itself** (chart + options chain)
- Its **heavyweight constituents** — HDFC Bank, ICICI Bank, Reliance, Infosys, HDFC Ltd, Kotak, L&T, TCS, Axis Bank. These move Bank Nifty and Nifty disproportionately and are leading indicators for the index on trending days.

A strong-trending index day favors riding index momentum directly via options. A rotational or choppy day favors stock-level relative-strength plays over broad index trades.

---

## Summary

| Situation | Scan universe |
|---|---|
| Default intraday stock trading | NSE F&O list (~180–220 names), filtered daily |
| Tighter / calmer environment | Nifty 100 |
| Index options trader | Nifty / BankNifty + top-10 heavyweights |
| Sector rotation read | 11 sectoral indices (not for stock picks — for context) |
