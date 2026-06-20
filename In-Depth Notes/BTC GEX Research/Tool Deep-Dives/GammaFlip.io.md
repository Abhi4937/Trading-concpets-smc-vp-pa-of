---
title: Deep-Dive — GammaFlip.io
tags: [gex, deep-dive, gammaflip, deribit, bybit, okx, multi-exchange]
created: 2026-06-20
source-quality: primary (verified 3-0, workflow 2026-06-20)
---

# 🔬 Deep-Dive: GammaFlip.io

**URL:** https://gammaflip.io/
**One line:** Free, fast (~60s) **multi-exchange** crypto GEX dashboard centered on the **gamma flip** level; broadest market coverage of the free tools.

---

## 1. What it is & why it matters
A live GEX dashboard whose headline feature is the **gamma flip** — the price where **net GEX crosses zero**, i.e. the boundary between the low-vol (dealers dampen) and high-vol (dealers amplify) regimes. Its edge over CryptoGamma: **faster refresh and multi-exchange aggregation.**

## 2. Coverage & data (verified 3-0)
| Attribute | Value |
|-----------|-------|
| Exchanges | **Deribit + Bybit + OKX** (aggregated) |
| Assets | BTC, ETH, SOL, XRP |
| Market coverage | claims **"99.5% of the crypto options market"** |
| Refresh | **~60 seconds** (vs CryptoGamma's ~15 min) |

## 3. The core concept it teaches
> "The gamma flip [is] the price level where net GEX crosses zero — the boundary between
> low-volatility (dealers dampen moves) and high-volatility (dealers amplify moves) regimes."

- **Above the flip** → typically long-gamma → mean-reversion, pinning.
- **Below the flip** → typically short-gamma → momentum, squeezes, vol expansion.
- Framing (verified): *Positive GEX → dealers buy dips & sell rallies (compress vol); Negative GEX → amplify moves both directions.*

## 4. How to use it
- Use the **flip level as your regime switch**: trade mean-reversion above it, momentum/breakouts below it.
- Because it **aggregates 3 venues**, its flip is less single-venue-biased than Deribit-only tools.
- Cross-check its flip against CryptoGamma's `squeeze.breakout` and GEX Terminal's zero-gamma cluster — agreement = high conviction.

## 5. What NOT to do / limits
- API availability not confirmed (treat as a **monitoring** tool, not an automation source — unlike CryptoGamma/Laevitas).
- "99.5% coverage" and "~60s" are **vendor self-report** (verified as *stated*, not independently load-tested).
- Still a **naive/aggregated** model — the flip is an estimate, not a hard line. → [[08 — Pitfalls and Misconceptions (what NOT to do)]]

## 6. Verdict
**Co-leader of the free tier** — arguably the best *live monitor* (fastest + broadest), while CryptoGamma wins on the **API**. Use both. → [[04 — Dashboards Directory + RANKING]]
