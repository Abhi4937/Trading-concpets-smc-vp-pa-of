---
type: research
title: "Opening Range Breakout (ORB) for Nifty/BankNifty intraday options — deep-research synthesis (web + books)"
date: 2026-06-19
method: "deep-research web harness (18 sources, 25 claims 3-vote-verified, 21 confirmed / 4 refuted) + local books mining (~20 PDFs)"
companion: "[[research-orb-books|research-orb-books.md]] (full book citations)"
---

# ORB for Indian index options — what the evidence actually says

End-to-end, adversarially-verified research on the Opening Range Breakout for Nifty 50 and BankNifty options.
**Bottom line: ORB is widely taught in India but is a *modest, fragile* edge on its own — its naive form has a
~48% win rate with large drawdown. It is a *trigger pattern*, not a system. It only earns its place inside this
engine when it is regime-gated, confirmation-filtered, and fakeout-aware** — which is exactly the breakout-vs-fakeout
fork the engine already runs (§17–24).

## 1. The headline tension (web vs books) — and why it matters

- **Web/broker practitioners (retail consensus): *trade the break.*** Mark the opening range, enter on a break of
  the high (CE) or low (PE), stop at the opposite end. (Tradejini, Groww, Tradersmastermind, Sahi, Zerodha)
- **Your books (Dale, ICT/SMC): *fade the break / trade the retest.*** The first range break is framed as a
  **stop-hunt trap** ("fake breakout to grab retail stops," "Judas swing," "turtle soup"); the genuine trade is the
  reversal or the retest, after 1–3 candles of *acceptance*. Trader Dale explicitly rejects naive breakouts
  ("a lot of false breakouts… doesn't work so well"). (repo: [[research-orb-books]] — Dale *Volume Profile/Order
  Flow*; ICT/SMC)

**Resolution = the engine's existing fork.** An ORB break is just price arriving at the IB boundary (a level). The
engine's at-level read decides whether it is a **BREAK** (real breakout — trade it) or a **HOLD** (failed break →
fakeout-reversal — fade it), gated by regime (§16). ORB does not override that; it *feeds* it. This is why naive
"buy every ORB break" backtests are mediocre.

## 2. Best opening-range window / timeframe (genuinely contested)

| Window | Verdict | Source/why |
|---|---|---|
| **First 15 min (9:15–9:30)** | **The practitioner default** — short enough to avoid a huge range, long enough to filter noise | Tradejini, Sahi, Tradersmastermind, Angel One (high confidence) |
| **First 5 min** | More aggressive; earlier trend-day entry **but more false breakouts** | Tradersmastermind, Groww, MetroTrade (high) |
| **First 3 min** | Many false breakouts from opening volatility; needs extra validation | Medium/redsword (high) |
| **9:15–11:15 (2 hr)** | **Zerodha's own options backtest** found this the *most reliable* for Nifty options | Zerodha "In The Money" (medium, single proprietary backtest) |
| **30 min (9:15–9:45)** | A widely-shared "+91.6% return" backtest for this — **REFUTED (0–3)**; do not trust the number | intradaylab (refuted) |
| **Books' intraday TF** | Dale favours **30-min** for intraday context, 5-min for fine entries (not an OR window) | repo: [[research-orb-books]] |

**Takeaway:** there is **no single backtest-proven optimal window**; 15-min is the safe default for a *break*
read, while a wider window (Zerodha's 2-hr) trades fewer, cleaner signals. This aligns with the engine: read the
IB/level on **15m**, time the entry on **5m** (§10, §25).

## 3. Mechanics (well-corroborated conventions, each with alternatives)

- **Entry:** break of the OR high (long/CE) or low (short/PE); **wait for the candle to CLOSE beyond the range** to
  cut the opening whipsaw (Tradersmastermind, Groww). *Retest entry* is weakly supported on the web but is the
  books' preferred, tighter-stop entry — use it (it shrinks the option stop, §22).
- **Stop-loss:** **opposite end of the opening range** (most common); alternatives = range **midpoint**, **half-range**,
  or **ATR-based** (books: ~10–20% of daily ATR). (Tradersmastermind, Groww, Intradaylab)
- **Target & R:R:** fixed **1:1 to 2:1** (some backtests 2×R), with a **hard intraday time-exit** (e.g., 2:30 PM
  IST) and often a **one-trade-per-day** rule. Books add: trail beyond 1R on trend days, exit just before the next
  S/R barrier. (Groww, Intradaylab; repo: [[research-orb-books]])
- **When to stay out:** very short ranges in the first minutes whipsaw; gap opens distort the range — let the open
  settle. No verified rule beat "wait for the close + a qualified level."

## 4. Confluence (how ORB is combined — matches the engine's lenses)

Widely paired with **VWAP** (break on the right side of VWAP), **volume expansion** on the break candle, **volume
profile / Initial Balance**, **OI profile / option-chain** (Wavesstrategy combines OI + VP + price action), and
**PDH/PDL**. (Groww, Tradejini, Wavesstrategy, Sahi) → these are the engine's existing witnesses (structure +
effort + options flow, §3); ORB just supplies the *level* (the IB boundary).

## 5. Options translation (this is the part that's options-specific)

- **Strike:** buy **ATM or slightly-ITM** CE (bull break) / PE (bear break), **delta ~0.40–0.60**. **Avoid deep
  OTM** — delta too low, premium barely responds. (Tradejini, Groww, Zerodha Varsity)
- **Why:** ATM delta ~0.50 → premium moves ~**₹0.50 per ₹1** of index move — the efficient vehicle for the ORB
  thrust. (Tradejini; Varsity Delta Pt.2)
- **Stop on premium:** Zerodha's variant maps the stop **onto premium directly** — pick the strike ≈ ₹200 premium,
  stop = **20% of entry premium**, enter when *premium* closes above its 9:15–11:15 range high. (Zerodha, medium /
  single source) — *note a competing fixed-₹10–15 SL rule was **REFUTED 0–3***. This sits alongside the engine's
  delta-based stop (§32): convert the index-point OR stop to premium via delta, or use the 20%-of-premium rule;
  either way keep it inside the per-instrument point budget (§33).

## 6. How widely used + the honest edge

- **Very widely taught** in India — every major broker/educator (Zerodha, Groww, Tradejini, Sahi, Angel One) has
  ORB content; it's one of the most popular retail intraday templates. (medium — broker-marketing-heavy evidence,
  not independent usage stats)
- **The honest edge is modest.** Zerodha's Jan 2022–Feb 2026 Nifty **weekly-options** backtest: **~48% win rate,
  ~45% max drawdown for option BUYING**; option **SELLING** marginally better win rate but only **~6% drawdown**
  (medium, single proprietary source). The flashier numbers (+91.6%) were **refuted**. **Implication: naive ORB
  option-buying is roughly a coin-flip with brutal drawdown — the edge comes from selectivity (regime + confluence
  + fakeout-awareness), strike/stop discipline, and that selling-side risk profile, not from the break itself.**

## 7. India structural facts (high confidence, current 2026)

- **Only Nifty 50 retains weekly options** (NSE) after SEBI's Nov 2024 framework; **BankNifty/FinNifty/Midcap/Next-50
  are monthly/quarterly only**; BSE keeps Sensex weekly. (Zerodha, Ventura)
- **Nifty weekly expiry = Tuesday** (shifted from Thursday, Sep 1 2025); Sensex took Thursday. So **weekly-expiry-day
  ORB (elevated theta/gamma, fast premium decay) now lands on Tuesday for Nifty** — buying ORB late on Tuesday is
  theta-hostile (ties to §35). BankNifty ORB option trades sit on **monthly** expiry (no weekly gamma). (Ventura +
  multiple)

## Caveats
- Evidence skews to **broker/educator blogs**, not independent/peer-reviewed research. All win-rate/return figures
  are single-source and period-specific — **illustrative, not validated**. Treat the "best window" as unsettled.

## Open questions
1. Independent (non-broker) 5 vs 15 vs 30 vs 60-min ORB comparison on Nifty **and** BankNifty options.
2. ORB edge on Nifty **expiry-day (Tuesday)** vs non-expiry — and how strike/stop should adapt to the theta/gamma.
3. BankNifty (monthly-only) ORB vs Nifty (weekly) ORB — which is preferable intraday post-SEBI.
4. Quantified retail **execution cost** (slippage + spread + brokerage) on ATM options and how much it erodes a 2:1 ORB.

## Key sources
Zerodha "In The Money" (options ORB backtest) · Tradejini (option strike/scalping) · Groww (5-min ORB option
scalping) · Tradersmastermind (window/mechanics) · Sahi (ORB explained, VWAP) · Wavesstrategy (VP+OI) · intradaylab
(backtest — perf claim refuted) · Ventura / Zerodha Z-Connect (SEBI expiry). Books: Trader Dale *Volume Profile /
Order Flow*, Coulling *VPA*, ICT/SMC (see [[research-orb-books]]).
