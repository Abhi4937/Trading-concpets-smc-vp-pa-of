---
title: "06 — Liquidity & Tradability Filters"
tags: [intraday, screener, liquidity, filters, india, universe]
created: 2026-06-21
---

# 06 — Liquidity & Tradability Filters

> **Run these filters FIRST — before any setup scan.** A perfect breakout pattern in an illiquid stock is untradeable. These gates define your actionable universe.

---

## Filter Table

| Filter | Threshold (typical) | Chartink-style logic | Why it matters intraday |
|--------|--------------------|--------------------|------------------------|
| **Minimum price** | `close > 50` (conservative: `> 100`) | `close > 50` | Penny stocks are easily manipulated, have erratic spreads, and thin order books. Price floor removes the noise. |
| **Minimum average volume** | `volume > 500000` shares (20-day avg) | `(Volume > 500000)` or `(Volume > 20-day avg volume * 0.8)` | **Single most important filter.** Low volume = you cannot exit at your intended price. Slippage destroys edge. Target daily turnover > ₹10–50 crore. |
| **ATR / Volatility floor** | ATR% > 1.5% (ATR/price × 100) | `(ATR(14) / close * 100) > 1.5` | You need daily range to extract a profit. Flat stocks have no intraday opportunity even if they set up. Also cap the ceiling — erratic ultra-high-vol names (ATR% > 8–10%) carry outsized gap/halt risk. |
| **Relative volume (RVol)** | RVol > 1.5× (today vs 20-day avg) | `(Volume > (20-day avg volume * 1.5))` | "Stocks in play" = elevated RVol + expanded range. Institutional/news-driven activity creates the momentum worth trading. |
| **Beta** | Beta > 0.8 (prefer > 1.0) | Not directly in Chartink; filter via F&O list as proxy | High-beta names amplify index moves — ideal for momentum intraday. Low-beta stocks lag, producing choppy, tight-range action. |
| **F&O eligibility** | SEBI derivatives list (~180–220 stocks) | Maintain a static watchlist; cross-reference [[07 — Index & Stock Universe]] | F&O stocks have the tightest spreads, highest liquidity, and are shortable. They are the de-facto liquid intraday universe in India. |
| **MIS-shortable** | Must be F&O or broker-approved for MIS short | Exclude T2T / Z-group / ASM / GSM stocks | Only approved names can be shorted intraday. T2T and surveillance stocks are delivery-only — critical for [[04 — Short Scans — Breakdown & Reversal-Down]]. Full rules in [[15 — Shorting Rules (margin, square-off, T2T-ASM)]]. |
| **Exclude F&O ban-period stocks** | Check SEBI/exchange ban list daily | Manual exclusion before scan | Stocks in F&O ban cannot have new derivative positions; liquidity dries up and price action becomes erratic. |
| **Exclude circuit-locked stocks** | Upper/lower circuit hit | `(Close != Upper Circuit) AND (Close != Lower Circuit)` | Circuit stocks are untradeable — no matching orders on one side. Any scan hit here is a false positive. |
| **Bid-ask spread** | Tight (< 0.1–0.2% of price) | Proxy: F&O list + high volume; no direct Chartink filter | Wide spreads consume intraday edge immediately on entry. High-volume F&O names implicitly satisfy this. |

---

## Implementation Order

1. **Start with the F&O eligible universe** — this alone handles price, liquidity, shortability, and spread in one filter.
2. **Add volume and ATR floors** inside that universe to isolate stocks in play today.
3. **Remove ban-list and circuit-locked names** daily (manual or broker API).
4. **Then run setup scans** (breakout, breakdown, reversal) on what remains.

---

## Key Principle

> Liquidity is not optional. The universe of ~180–220 F&O stocks is small enough to scan in seconds and large enough to always find setups. Chasing illiquid mid/small-caps for "bigger moves" is how intraday traders blow up — exits become impossible under stress.

See [[07 — Index & Stock Universe]] for how this universe is constructed and maintained.
