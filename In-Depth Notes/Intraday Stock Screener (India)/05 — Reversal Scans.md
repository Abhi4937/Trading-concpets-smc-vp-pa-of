---
title: "05 — Reversal Scans"
tags:
  - screener
  - reversal
  - intraday
  - india
  - NSE
  - RSI
  - VWAP
  - order-flow
created: 2026-06-21
---

# 05 — Reversal Scans

Reversal scans look for stocks that may be about to change direction — either bouncing up from a washout or rolling over from a peak. They are **lower base-rate than trend-continuation scans** (see [[16 — Evidence & Pitfalls]]). Treat every result as a *candidate*, never a trade. Manual confirmation via price action and order flow is non-negotiable.

---

## Upside Reversals — Catching a Stock About to Turn Up

### 1. RSI Oversold Turning Up
**Idea:** RSI falling below 30 signals excess selling. A turn back above 30 suggests exhaustion.

**Chartink logic (approximate):**
```
rsi(14) < 30 AND rsi(14) > rsi(14)[1]
```
Stronger signal: **bullish divergence** — price makes a lower low while RSI prints a higher low. Divergence must be confirmed visually; Chartink cannot detect it directly.

**Confirmation needed:** Bullish candle (hammer, engulfing) on elevated volume as RSI hooks. Micro down-structure must break (lower-high sequence gets violated).

---

### 2. Price at Support / Demand Zone
**Idea:** Prior swing lows, round numbers (e.g., ₹500, ₹1000), and high-volume-node levels act as demand.

**Chartink logic:**
```
close <= (low52week * 1.02)
```
Or filtered by distance from a defined moving average. More precisely, maintain a watchlist of stocks near identified support and cross-reference intraday.

**Confirmation needed:** Price stalls at the level, volume spikes on the rejection candle, and the candle closes inside (not through) support.

---

### 3. Bullish Candlestick at Support
**Idea:** Reversal candle patterns carry meaning only when they appear at a meaningful level.

**Patterns to look for:** Hammer, bullish engulfing, piercing line.

**Chartink logic:**
```
[candlestick pattern filter] AND close > open[1]
```
Most screeners include pre-built candle pattern filters (hammer, engulfing).

**Confirmation needed:** Pattern printed at support (not in mid-air). Follow-through candle on the next bar closes above the pattern high.

---

### 4. VWAP Mean-Reversion
**Idea:** Intraday price stretched far below VWAP tends to snap back — institutions use VWAP as a benchmark and defend deviations.

**Chartink logic:**
```
close < vwap * 0.98 AND close > close[1]
```
(Exact VWAP availability varies by screener; TradingView Pine can compute it precisely.)

**Confirmation needed:** Price crosses back above VWAP with above-average volume. See [[13 — Which Technical Analysis to Use]] for how VWAP integrates with order-flow context.

---

### 5. Gap-Down Fill
**Idea:** Stock gaps down at open but reclaims the prior day's close — gap fills are high-probability short-term moves in liquid names.

**Chartink logic:**
```
open < close[1] * 0.99 AND close >= close[1]
```

**Confirmation needed:** Clean reclaim on volume; prior close must act as support on a re-test.

---

### 6. Stochastic Crossover from Oversold
**Idea:** %K crossing above %D while both are below 20 indicates momentum shift from washed-out levels.

**Chartink logic:**
```
stochrsi(14,3,3) < 20 AND stoch_k > stoch_d
```

**Confirmation needed:** Align with a price-level reason (support, VWAP). Stochastic crossovers in downtrends produce many false signals without structural context.

---

### 7. Down-Move Stalling on Rising Volume (Absorption)
**Idea:** Price continues down but volume is rising and candles are shrinking — sellers are being absorbed by buyers. Direct tie to order flow.

**Chartink logic:** Approximate:
```
close < close[1] AND volume > volume[1] * 1.3 AND (high - low) < (high[1] - low[1])
```

**Confirmation needed:** Next bar must close higher (otherwise absorption failed). For precise footprint-level absorption, see [[03 — Long Scans — Breakout & Bounce]] and the order-flow skill.

---

## Downside Reversals — Catching a Stock About to Turn Down (Short Setups)

### 1. RSI Overbought Turning Down
**Idea:** RSI above 70 signals excess buying. A roll back below 70 suggests distribution.

**Chartink logic:**
```
rsi(14) > 70 AND rsi(14) < rsi(14)[1]
```
**Bearish divergence** (price higher high, RSI lower high) strengthens the setup significantly.

**Confirmation needed:** Bearish candle at resistance, volume picking up on the down-bar, micro up-structure breaks (higher-low sequence violated).

---

### 2. Price at Resistance / Supply Zone
**Idea:** Prior swing highs, prior breakout levels that failed, and round numbers overhead create supply.

**Chartink logic:**
```
close >= (high52week * 0.98)
```
Or near a defined resistance level from a watchlist.

**Confirmation needed:** Price stalls and closes below the resistance candle's low. Volume on the rejection bar exceeds the approach bars.

---

### 3. Bearish Candle at Resistance
**Patterns:** Shooting star, bearish engulfing, dark cloud cover.

**Chartink logic:** Use pre-built bearish pattern filters at resistance.

**Confirmation needed:** Pattern at a meaningful level only. Next bar confirms by breaking below the pattern low.

---

### 4. VWAP Rejection from Above
**Idea:** Price rallies to VWAP from below, fails to hold, and reverses — sellers defending VWAP as resistance.

**Chartink logic:**
```
close < vwap AND close[1] >= vwap
```

**Confirmation needed:** Volume spike on the rejection bar. Price should not re-test VWAP without another setup forming.

---

## Critical Caveat — Confirmation is Mandatory

Reversal scans operate against the dominant flow. Most edge in intraday trading is **with-trend** — reversals have lower base-rate success and wider stops by definition.

A screener hit means: *this stock is in a zone where reversals sometimes happen.* It does not mean the reversal is happening now.

Do not act on the screener alert alone. Require:
1. A price-action confirmation candle (pattern + follow-through).
2. Volume that validates the move (absorption on the down-side, expansion on the up-side).
3. A structural break — prior swing point violated — as entry trigger.
4. Order-flow agreement where possible (delta, footprint, tape).

This is exactly the framework described in [[13 — Which Technical Analysis to Use]]. The screener finds the address; price action and order flow tell you whether anyone is home.

For evidence on why reversal hit-rates underperform trend-following in Indian intraday markets, see [[16 — Evidence & Pitfalls]].
