---
title: "03 — Long Scans — Breakout & Bounce"
tags:
  - screener
  - intraday
  - long
  - breakout
  - bounce
  - chartink
  - india
created: 2026-06-21
---

# 03 — Long Scans — Breakout & Bounce

Intraday bullish scans for the Indian cash/futures market. Each scan is a single signal; stacking 2–3 is how you find high-probability setups. Apply [[06 — Liquidity & Tradability Filters]] before acting on any hit.

---

## Scan Reference

| # | Scan Name | Idea | Chartink-Style Filter Logic | Intraday Use |
|---|-----------|------|-----------------------------|--------------|
| 1 | **Relative Volume Surge** | Unusual participation = event in play | `volume > 2 * sma(volume, 20)` | First alert after 9:30. Confirms breakout is real, not noise. |
| 2 | **15-Min ORB Breakout** | Price clears the opening range; range traders trapped | `close > highest(high, 3)` on 5-min chart (first 3 candles = first 15 min); or day-high break proxy on 15-min | Wait for candle *close* above range high, not just wick. |
| 3 | **Previous-Day-High Break** | Prior resistance flips to support | `latest close > 1 day ago high` | Strong momentum trigger. Use as entry or add-on to existing long. |
| 4 | **Above VWAP** | Institutional fair-value anchor; bullish above | `close > vwap` | Bias filter, not standalone. Longs taken above VWAP have institutional tailwind. |
| 5 | **Gap-Up with Volume** | Supply absorbed pre-open; continuation likely | `latest open > 1 day ago close * 1.02 AND volume > 2 * sma(volume, 20)` | Trade continuation, not mean-reversion. Wait 15 min for range to form, then trade range break. |
| 6 | **EMA Stack / Crossover** | All time-frames aligned bullish | `ema(close,9) > ema(close,20) > ema(close,50) AND close > ema(close,9)` | Trend filter. Only take long setups in EMA-stacked stocks. |
| 7 | **Supertrend Buy Signal** | Trend-following with ATR-based stop | Supertrend (10,3) value below price AND color = green (signal flipped in last 1–5 bars) | Entry on fresh flip; stop at Supertrend level. Avoid chasing established trends. |
| 8 | **RSI Momentum Ignition** | Momentum accelerating into bullish territory | `rsi(14) crossed above 60` (daily or 15-min) | Strong signal in early session. Avoid if RSI already >75 — extension, not ignition. |
| 9 | **52-Week-High Breakout** | Jegadeesh-Titman momentum effect; no overhead resistance | `close > 52 week high` | Highest-conviction breakout. Volume must confirm. Add scan 1 as mandatory co-filter. |
| 10 | **NR7 Range Breakout** | Volatility compression → expansion | `range today < range of each of last 6 days` (narrowest 7-day range), then `close > high of NR7 bar` | Set alert at NR7 high the prior evening. Trade the break with a tight stop below NR7 low. |
| 11 | **Pullback Bounce (Long-with-Trend)** | Buy dip in an uptrend; better R:R than chasing | Uptrend stock (EMA stack): `low touched ema(close,20) or vwap` AND `close > open` (bullish reversal candle) | Best used 10:30–13:00. Requires manual chart review after Chartink hit. |

---

## Combining for an A+ Long

Stack **three or more signals at a liquid stock** to filter down to highest-conviction setups:

**Tier 1 (must-have):** Above VWAP + Relative Volume Surge
**Tier 2 (pick one trigger):** Prev-Day-High Break **or** 15-Min ORB Breakout **or** 52-Week-High Breakout
**Tier 3 (context):** EMA Stack aligned + strong sector (see [[08 — Sector Rotation & Relative Strength]])

Example checklist for a single trade:
- [ ] Stock above VWAP
- [ ] Volume > 2× 20-day average
- [ ] Close above previous-day high
- [ ] EMA 9 > EMA 20 > EMA 50
- [ ] Sector index also green / outperforming NIFTY

If 4–5 boxes checked on a liquid (>₹50 Cr daily volume) NSE stock, that is an A+ setup. See [[06 — Liquidity & Tradability Filters]] for the minimum tradability bar.

---

## Pitfalls

- **Chasing extended RSI (>75–80):** Momentum scans are *entry* triggers, not chase signals. Once RSI is extended, the easy money is gone.
- **Low-liquidity false breakouts:** Scans 2, 9, 10 fail disproportionately in illiquid stocks. Volume filter (scan 1) is non-negotiable. Filter list with [[06 — Liquidity & Tradability Filters]] first.
- **Chartink 15-min delay on free tier:** The free Chartink scanner refreshes every 15 minutes. An ORB breakout signal may arrive late — price has already moved. Either use the paid real-time tier or manually verify on a live chart before entry.
- **Breakouts fail on balance/range days:** On a market in balance (NIFTY flat, narrow range), breakout scans produce the most false signals. Check the broader market regime before firing. On trending days, scans 2, 3, 9 outperform; on range days, scan 11 (pullback bounce) is safer.
- **Gaps that don't hold:** Gap-up with volume (scan 5) sometimes fades if the gap is on weak news or broad market weakness. Confirm gap direction aligns with index sentiment by 9:30–9:45.
- **ORB range width:** A very wide ORB (>2% range in 15 min) produces a large stop. Avoid unless position size is adjusted; the risk per trade balloons.

For deeper evidence on what actually works in Indian markets versus what is marketing, see [[16 — Evidence & Pitfalls]]. For indicator selection rationale, see [[13 — Which Technical Analysis to Use]]. Pre-market watchlist building workflow using these scans is in [[14 — Pre-Market Routine & Watchlist Building]].
