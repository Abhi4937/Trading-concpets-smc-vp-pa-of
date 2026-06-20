---
title: BTC Gamma Exposure (GEX) — Map of Content
tags: [gex, gamma-exposure, btc, options, deribit, moc]
created: 2026-06-20
status: living-document
---

# 🗺️ BTC Gamma Exposure (GEX) — START HERE

> A complete, self-contained research vault on **Bitcoin gamma exposure**: what it
> is, the exact math, the dashboards/repos that show it, the APIs behind them, how
> to build your own, how to actually trade with it, and the traps to avoid.
>
> Built from **primary-source capture** (live dashboards via Firecrawl + agent-browser,
> GitHub source via API) and **two adversarially-verified deep-research passes**
> (claims voted 2/3 to survive). Vendor self-reported claims are flagged as such.

---

## 📚 The notes (read in order)

| # | Note | What you get |
|---|------|--------------|
| 01 | [[01 — What Gamma Exposure (GEX) Is]] | The concept, dealer hedging, long vs short gamma regimes |
| 02 | [[02 — The Math — Greeks to Dollar GEX (with code)]] | Black-Scholes γ → dollar GEX, walls, zero-gamma, real source code |
| 03 | [[03 — How to Read a GEX Chart (interpretation)]] | Every number/level/color explained; what each tells you |
| 04 | [[04 — Dashboards Directory + RANKING]] | Your 5 links + my discoveries, **ranked best-first**, pricing, APIs |
| 05 | [[05 — APIs and Data Sources (Deribit etc.)]] | Deribit, CryptoGamma, Laevitas, Amberdata endpoints + how to pull |
| 06 | [[06 — Build Your Own GEX Engine (architecture)]] | Full architecture from real OSS source; adapters, engine, math |
| 07 | [[07 — Trader Usage Playbook (how to use together)]] | The combined daily workflow, levels → trades |
| 08 | [[08 — Pitfalls and Misconceptions (what NOT to do)]] | The traps that blow up GEX-based trades |

### 🔬 Per-tool deep-dives (`Tool Deep-Dives/`) — math, APIs, functions, end-to-end
- [[Tool Deep-Dives/CryptoGamma]] · [[Tool Deep-Dives/GammaFlip.io]] · [[Tool Deep-Dives/GEX Terminal Pro]] · [[Tool Deep-Dives/Laevitas]]
- [[Tool Deep-Dives/Glassnode Gamma Exposure]] · [[Tool Deep-Dives/Amberdata AD Derivatives]]
- [[Tool Deep-Dives/Nathan-Hall Bitcoin-Options-GEX]] · [[Tool Deep-Dives/dankbit]] · [[Tool Deep-Dives/zrack gex-terminal]]

---

## ⚡ 60-second summary

- **GEX = dealer gamma exposure** = how much options market-makers must hedge per unit move in BTC. It is a *map of where forced hedging flows live*, not a prediction.
- **Positive/long gamma** → dealers buy dips & sell rips → **price pins, vol compresses**. **Negative/short gamma** → dealers sell dips & buy rips → **trends accelerate, vol expands**.
- Key levels: **Gamma Wall** (biggest exposure strike, acts like a magnet/barrier), **Zero-Gamma / Vol-Flip** (boundary between the two regimes), **Call Wall** (resistance), **Put Wall** (support).
- **BTC data lives on Deribit** (~85–90% of crypto options OI). Everything ultimately reads the Deribit options chain.
- **Best free live monitor:** [GammaFlip.io](https://gammaflip.io/) (~60s, Deribit+Bybit+OKX). **Best free + API:** [CryptoGamma.io](https://cryptogamma.io/dashboard/) (public JSON API). **Best free intraday chart:** [GEX Terminal Pro](https://gexterminal.net/). **Best methodology:** [Glassnode](https://research.glassnode.com/gamma-exposure/) (taker-flow). **Best paid all-rounder:** [Laevitas](https://app.laevitas.ch/assets/options/gex/btc/deribit) (REST API). **Deepest institutional:** Amberdata AD Derivatives.

---

## 🔑 The one thing to remember

> GEX tells you the **environment** (will moves get dampened or amplified?) and the
> **levels** (where do the magnets/barriers sit?). It does **not** tell you direction.
> Combine it with price action and flow — never trade a wall blind. See [[08 — Pitfalls and Misconceptions (what NOT to do)]].

---

## 🧭 Provenance & honesty notes

- Captured live on **2026-06-20** (BTC ~$63.3k at capture time on CryptoGamma).
- Crypto dealer-sign conventions are **less reliable than equities** — there is no centralized OCC-style customer/dealer tagging. Most free tools use a *naive* `OI × Γ × sign` model. Only Amberdata claims *true* aggressor-based dealer positioning (vendor-asserted, not independently benchmarked).
- Where a claim is vendor self-report or unverified, the note says so explicitly.
