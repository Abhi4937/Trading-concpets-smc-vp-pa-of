---
title: "04 — Short Scans — Breakdown & Reversal-Down"
tags:
  - screener
  - intraday
  - india
  - short
  - breakdown
  - reversal
created: 2026-06-21
---

# 04 — Short Scans — Breakdown & Reversal-Down

> **Shorting rules primer:** Intraday shorting is fully legal in India and carries the **same margin as a long MIS position**. However, it is restricted to the **MIS (intraday) product type only** — you must square off before ~3:20 pm (broker auto-square-off time); overnight carry is not possible for a cash short. Only **F&O-eligible or broker-shortable stocks** qualify; T2T (Trade-to-Trade), Z-group, ASM (Additional Surveillance Measure), and GSM stocks **cannot be shorted intraday**. Always verify eligibility before entry. See [[15 — Shorting Rules (margin, square-off, T2T-ASM)]] for the full rulebook.

All 11 scans below are the **bearish mirrors** of the long scan set. Each has a plain-English idea and a Chartink-style filter. Before running any scan, overlay [[06 — Liquidity & Tradability Filters]] to drop illiquid and non-shortable names.

---

## 1. Relative Volume on a Down Move

**Idea:** Heavy institutional or program selling is signalled when volume spikes 2× its 20-day average on a red candle. Absence of buying at that volume level confirms the sell-side is in control.

**Filter:**
```
volume > 2 * sma(volume, 20)
AND close < open
```

---

## 2. Opening Range Breakdown (ORB Short)

**Idea:** If price cannot hold the low of the first 15-minute candle after the open, sentiment is bearish from the start of the session. The ORB low becomes resistance.

**Filter:**
```
close < min(low, time_0915_to_0930)   // first 15-min candle low
```
*(In Chartink: use the "15-minute opening range low" built-in or construct with `low of first candle` on a 15-min chart.)*

---

## 3. Previous-Day Low Break

**Idea:** The prior session's low is a key reference for trapped longs and stop-loss clusters. A close below it often triggers cascading sell orders.

**Filter:**
```
close < 1 day ago low
```

---

## 4. Below VWAP

**Idea:** VWAP is the institutional fair-value anchor for the session. Stocks persistently trading below VWAP are under net selling pressure; every rally back to VWAP offers a short entry.

**Filter:**
```
close < vwap
```

---

## 5. Gap-Down with Volume

**Idea:** A gap-down of ≥2% on elevated volume shows overnight or pre-market selling has overwhelmed buyers. The gap itself is resistance on any bounce attempt.

**Filter:**
```
open < 1 day ago close * 0.98
AND volume > 2 * sma(volume, 20)
```

---

## 6. EMA Stack Down / Bearish Crossover

**Idea:** When the 9-EMA < 20-EMA < 50-EMA and price trades below all three, every EMA layer above is potential resistance. This is the short-side equivalent of an EMA stack-up.

**Filter:**
```
ema(close, 9) < ema(close, 20)
AND ema(close, 20) < ema(close, 50)
AND close < ema(close, 9)
```

---

## 7. Supertrend Sell Signal

**Idea:** Supertrend (10, 3) flipping from below to above price is a mechanical trend-change signal. The flip candle typically becomes the short entry or the reference for a stop.

**Filter:**
```
supertrend(10, 3) crosses above close    // signal candle
// or: supertrend > close                // continuation filter
```

---

## 8. RSI Momentum Down

**Idea:** RSI(14) crossing below 40 marks the transition from neutral to bearish momentum — sellers are accelerating while buyers are stepping back.

**Filter:**
```
rsi(14) crossed below 40
```

---

## 9. 52-Week Low Breakdown

**Idea:** Breaking a 52-week low removes every remaining long holder's support. Institutional stop-losses and trailing limits trigger, creating a sharp waterfall move.

**Filter:**
```
close < 52 week low
```
*Note: these moves are violent but also prone to reversal bounces — use tight stops and small size.*

---

## 10. Overbought Reversal-Down

**Idea:** Three confluent signals at resistance — RSI > 70 (overbought) turning lower, a shooting-star or bearish-engulfing candlestick pattern, and a bearish RSI divergence (price prints a higher high while RSI makes a lower high). This is the classic counter-trend short.

**Filter:**
```
rsi(14) > 70
AND (shooting star OR bearish engulfing candle pattern)
// RSI divergence must be confirmed visually or via Pine script divergence detector
```

---

## 11. Weak Stock in a Weak Sector

**Idea:** When a stock lags its sector index *and* the sector lags Nifty, the path of least resistance is strongly down. Double relative weakness amplifies the short edge. See [[08 — Sector Rotation & Relative Strength]] for how to measure RS.

**Filter:**
```
// Stock RS vs Nifty < 0 (custom RS column in Chartink or broker terminal)
// Sector ETF (e.g. BANKBEES, ITBEES) also < Nifty on the day
```

---

## Critical Eligibility Filter

Run every scan output through this gate before placing any short order:

- Stock must be **F&O-eligible or on the broker's intraday short list**.
- Exclude T2T, Z-group, ASM Stage III/IV, GSM stocks — these attract an **auction penalty** if a cash short is not covered in time.
- Minimum liquidity: see [[06 — Liquidity & Tradability Filters]].
- Product type: **MIS only** — see [[15 — Shorting Rules (margin, square-off, T2T-ASM)]].

---

## A+ Short Setup

The highest-probability intraday short combines **all four** of:

1. **Below VWAP** (scan 4) — institutional fair value is above price.
2. **Previous-day low break** (scan 3) — key support has failed.
3. **Relative volume on a down move** (scan 1) — real selling, not drift.
4. **Weak stock in a weak sector** (scan 11) — macro tailwind for bears.

Optional confirmation: ORB breakdown (scan 2) or EMA stack down (scan 6). Entry on a VWAP retest that fails, stop above the last swing high, target the next visible support or a 1:2 R:R minimum.

---

## Pitfalls

- **Short squeezes** are sudden and violent — always pre-define your stop before entry, not after.
- **Auto-square-off at ~3:20 pm** — most brokers auto-cover MIS shorts; holding into the last 10 minutes against you guarantees a bad fill.
- **Auction penalty** — if you short a cash stock and fail to cover, the exchange runs a closing auction; the penalty price can be far above your intended exit. T2T stocks make this risk extreme.
- **Shorting strong-uptrend names** — RSI > 70 alone is not a short signal in a strong bull run; require the divergence and candlestick pattern (scan 10) before fading momentum.
- **Violent reversals** — intraday shorts in index-heavy or news-driven stocks can reverse 3–5% in minutes on positive news; size accordingly.
