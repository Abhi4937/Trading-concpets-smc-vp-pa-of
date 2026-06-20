---
title: Deep-Dive — CryptoGamma.io
tags: [gex, deep-dive, cryptogamma, deribit, api]
created: 2026-06-20
source-quality: primary (live capture 2026-06-20)
---

# 🔬 Deep-Dive: CryptoGamma.io

**URL:** https://cryptogamma.io/dashboard/ · **API:** https://cryptogamma.io/api/public/snapshot?asset=BTC
**One line:** Free, Deribit-derived BTC/ETH gamma dashboard with actionable squeeze/pin levels and a public JSON API.

---

## 1. What it is & what problem it solves
A hosted dashboard that turns the raw Deribit options chain into a **single decision screen**: net/call/put gamma, a directional bias, and the price levels where dealer hedging should pin or squeeze BTC. It saves you from building your own engine.

## 2. End-to-end architecture (how data flows)
```
Deribit public API (orderbook, OI, mark IV, index price)
        │  (server-side fetch)
        ▼
CryptoGamma compute layer  →  naive GEX = Σ strike  OI × Γ × sign
        │   + squeeze model (support/resistance/breakout)
        │   + riskMetrics (deltaHedging, squeezeRisk, pinRisk)
        ▼
Next.js cache (ISR, revalidate ~15 min)
        ├──► /dashboard/  (rendered UI)
        └──► /api/public/snapshot?asset=BTC  (JSON)
```
- **Stack signal:** Next.js with Incremental Static Regeneration (the "revalidated every 15 min" string is the ISR cache TTL).
- **Sign convention:** call gamma positive, put gamma negative (naive model — see [[02 — The Math — Greeks to Dollar GEX (with code)]]).

## 3. The data fields (what every number means)
From the live `/api/public/snapshot?asset=BTC` payload + dashboard:

| Field | Meaning | How to read it |
|-------|---------|----------------|
| `netGamma` | Call gamma + put gamma (net dealer exposure) | **Negative → short-gamma, trends amplify**; positive → pinning |
| `callGamma` / `putGamma` | Side breakdown | Magnitude & balance → who dominates |
| `bias` | BEARISH / BULLISH / NEUTRAL + "% call weighted" | Quick read of net positioning skew |
| `squeeze.support` / `.resistance` | Nearest gamma-derived defended levels | Where pinning/bounce is likely |
| `squeeze.breakout` | Level beyond which squeeze accelerates | Break → momentum/vol expansion |
| `realized` vs `implied` vol + premium | IV richness vs delivered vol | High premium → options "expensive", vol-sellers active |
| `flow` (24h call/put) + C/P ratio | Recent volume tilt | Demand pressure direction |
| `riskMetrics.deltaHedging` | Expected dealer hedge intensity | Higher → more mechanical flow |
| `riskMetrics.squeezeRisk` | Likelihood of a squeeze | Rising → fragile, trend-prone |
| `riskMetrics.pinRisk` | Likelihood price pins a strike near expiry | High → range/mean-revert into expiry |
| `generatedAt` | Snapshot timestamp (UTC) | Confirm freshness (≤15 min old) |

## 4. How to actually use it
- **Open the dashboard**, read `bias` + `netGamma` sign → decide regime (pin vs trend).
- Mark `squeeze.support / resistance / breakout` on your TradingView chart as horizontal lines.
- Near expiry, watch `pinRisk` → fade extensions back toward the pin.
- For automation: poll the JSON API (code in [[05 — APIs and Data Sources (Deribit etc.)]]).

## 5. What NOT to do / limitations
- **Naive model:** no true customer/dealer tagging — sign is assumed, not measured. Don't treat "BEARISH bias" as a directional signal; it's a *positioning* read.
- **Single venue (Deribit only).** Misses CME/OKX/Bybit/IBIT context.
- **15-min cadence** → useless for sub-15-min scalps; levels can be stale around fast moves.
- **Squeeze support==resistance** sometimes collapses to the same number in tight regimes — that's a degenerate output, not a high-conviction level.

## 6. Verdict
🥇 **Rank #1 for retail.** Best free "look once, get levels + an API" tool. Pair with GEX Terminal Pro for the intraday chart. → [[04 — Dashboards Directory + RANKING]]
