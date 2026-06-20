---
title: "16 — Evidence & Pitfalls: What Actually Works vs. What Is Being Sold"
tags: [intraday, screener, india, evidence, research, risk]
created: 2026-06-21
---

# 16 — Evidence & Pitfalls: What Actually Works vs. What Is Being Sold

A screener is a filter, not an edge. This note separates what peer-reviewed research and serious practitioner data actually support from what the retail screener industry sells you. For the broader evidence base underpinning this whole project, see [[In-Depth Notes/research-strategy-evidence-and-mastery-roadmap|research-strategy-evidence-and-mastery-roadmap]].

---

## What Has Genuine Evidence

### Momentum — Real Anomaly, Wrong Timeframe Transfer

Jegadeesh & Titman (1993) is the canonical citation: past 3–12 month winners continue to outperform. The anomaly is robust across replications and markets. But that result is **cross-sectional, monthly rebalancing, multi-month holding periods.** When intraday desks talk about "relative strength" or "stocks in play," they are extending the intuition to a sub-day timeframe where no equivalent peer-reviewed result exists. The practitioner consensus is reasonable — there is a logic to it — but the gap between the monthly academic finding and the intraday application is real and should not be papered over. Trade the idea, but do not cite Jegadeesh & Titman as proof that your 5-minute RS scan has academic backing.

### VWAP — Strongest Intraday Peer-Reviewed Support

Zarattini & Aziz (SSRN) document a directional edge on US ETFs using VWAP-relative positioning. Long above VWAP, short below, is the one intraday signal with the closest thing to formal research support. In the India context, VWAP is also the anchor used by institutional desks for execution benchmarking, which reinforces why price respects it: the institutions are actually trading around it. See [[03 — Long Scans — Breakout & Bounce]] for how VWAP enters the scan logic.

### Relative Volume ("Stocks in Play") — Strong Practitioner, Lighter Academic

High relative volume identifies names where liquidity and participant interest are elevated enough to produce clean intraday structure. This is practitioner consensus from professional prop desks and is directionally sensible — a stock doing 5x its average volume has a reason, and that reason is usually the day's narrative. Formal academic support is thin. Weight it accordingly: high confidence that it identifies *tradable* names, lower confidence that it predicts *direction*.

### ORB — The Edge Is Selectivity, Not the Break

The user's own ORB research found roughly 48% win rate and large drawdown on naive opening-range-breakout signals. A coin flip after costs. The literature on ORB is similarly mixed. The edge, where it exists, comes from regime-gating (trending day vs. choppy open) and selectivity (the break on a stock already in play, with a clean gap and volume confirmation). The break itself is not the signal. See [[14 — Pre-Market Routine & Watchlist Building]] for how the pre-market routine reduces the ORB universe to genuinely gated candidates.

---

## What Is Marketing — Discount on Sight

- Any scan or screener sold with a fixed **80% win-rate** claim. No audited, out-of-sample, cost-adjusted backtest means this number is in-sample fitting or selection bias.
- Backtested scan results without slippage, impact costs, out-of-sample validation, and disclosed sample size. India small/mid-cap impact costs can erase a theoretical edge entirely.
- "Secret scan" products and paid Telegram signal groups built on Chartink filters that anyone can replicate for free. The edge was never in the filter; it never existed.
- "Multibagger intraday calls" — a logical contradiction. Multibaggers require holding time; intraday closes flat at end of day by definition.

---

## The Core Truth

A screener finds candidates. It does not manufacture edge. Edge is: **selectivity** (choosing 3–5 A+ setups from 50 signals, not trading all 50) + **execution** + **risk management**.

The India F&O data is unambiguous: **93% of F&O traders lose money** (SEBI). The primary killer is overtrading — frequency erodes expectancy faster than a bad win-rate does. A screener that delivers 50 signals a day is actively harmful if you act on most of them. A screener that narrows your universe to 3–5 high-conviction names, pre-gated by regime and liquidity, is a tool. The full evidence logic for why expectancy matters more than win-rate, and why frequency kills retail traders specifically, is in [[In-Depth Notes/research-strategy-evidence-and-mastery-roadmap|research-strategy-evidence-and-mastery-roadmap]].

---

## Common Pitfalls

| Pitfall | Why It Hurts |
|---|---|
| Over-filtering | Too many conditions → curve-fit to past data or zero results in live market |
| Chartink free-tier delay | 15-min delay on data; a signal you see is 15 minutes stale — usable only for pre-market, not live scanning |
| Survivorship in shared scans | Community-published Chartink scans are tested on stocks that exist today; delisted names drop out, inflating historical hit rate |
| Trading every signal | Turns a candidate filter into an automatic execution system; destroys selectivity, the only real edge |
| Ignoring liquidity | A technically perfect signal on an illiquid name will have wide spread, poor fill, and high impact cost |
| Ignoring regime | Any scan run on a gap-down, high-VIX, trending-down market day will produce mostly false breakouts |
| Reversal scans without base-rate awareness | Mean-reversion scans have a lower base rate than trend-continuation in intraday; trading them without that context will lose money at a higher win-rate than you expect |
