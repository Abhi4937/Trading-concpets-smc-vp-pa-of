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
| 09 | [[09 — Worked Examples and Annotated Charts (all scenarios)]] | Every definition as an annotated chart + numbers + the 10 scenarios walked end-to-end |

### 🎯 Advanced — accuracy, positioning & extra data sources (added 2026-06-21)
| # | Note | What you get |
|---|------|--------------|
| 10 | [[10 — Volume-Weighted GEX (VW-GEX)]] | Volume vs OI vs signed-volume weighting; VW-GEX formula + code; how to read & use it |
| 11 | [[11 — Real-Time Dealer Positioning — CLOB Aggressor vs Block-OTC trades]] | What a CLOB is; on-book taker/aggressor flow vs block/OTC; live dealer-gamma reconstruction |
| 12 | [[12 — CME Bitcoin Options & Futures as a GEX input]] | CME BTC futures/options, free vs paid data, Black-76 adjustments, combining CME + Deribit |
| 13 | [[13 — Accurate DIY GEX — closing the gap to paid]] | The accuracy ladder, the error budget, free-data maximization, "close enough to speculate" verdict |

### 🔬 Per-tool deep-dives (`Tool Deep-Dives/`) — math, APIs, functions, end-to-end
> The four hosted dashboards now include **annotated live-UI walkthroughs** (real screenshots captured 2026-06-20): every panel/chart explained — what it is, how to read it, the logic, assumptions, and limitations. Laevitas (4 charts), CryptoGamma (metrics + heatmap + vol/flow/risk), GammaFlip (marker taxonomy), GEX Terminal Pro (live terminal).
- [[Tool Deep-Dives/CryptoGamma]] · [[Tool Deep-Dives/GammaFlip.io]] · [[Tool Deep-Dives/GEX Terminal Pro]] · [[Tool Deep-Dives/Laevitas]]
- [[Tool Deep-Dives/Glassnode Gamma Exposure]] · [[Tool Deep-Dives/Amberdata AD Derivatives]]
- [[Tool Deep-Dives/Nathan-Hall Bitcoin-Options-GEX]] · [[Tool Deep-Dives/dankbit]] · [[Tool Deep-Dives/zrack gex-terminal]]
- [[Tool Deep-Dives/Coinglass]] — perps/futures positioning: liquidation & liquidity heatmaps (estimated, not actual), funding, OI, whale/large-order indicators, API, and peers (Coinalyze/Hyblock/Velo/CoinAnk)

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
- **2026-06-21 expansion (notes 10–13 + Coinglass):** added volume-weighted GEX, real-time CLOB/aggressor vs block/OTC positioning, CME as a data source, and a DIY-accuracy synthesis. **Material update to the 60-second summary above:** as of April 2026, US-listed **IBIT options OI (~$27.6B, vendor/aggregator-sourced) has reportedly surpassed Deribit (~$26.9B)** for the first time — so a *Deribit-only* model now sees well under half the BTC options market. Multi-venue aggregation (Deribit + CME + IBIT/Bybit/OKX) matters more than when this vault was first built. See [[13 — Accurate DIY GEX — closing the gap to paid]].
