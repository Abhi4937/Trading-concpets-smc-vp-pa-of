---
title: BTC GEX Dashboards Directory + RANKING
tags: [gex, dashboards, ranking, deribit, laevitas, cryptogamma, amberdata]
created: 2026-06-20
status: verified-2026-06-20
---

# 🏆 BTC GEX Dashboards, Tools & Repos — Directory + RANKING

> Ranked for a **retail BTC options/futures trader** (weighting: cost + ease of use +
> working API). Institutions would push Amberdata/Laevitas higher. Every entry was
> captured/verified on **2026-06-20**. Vendor self-reported claims are marked ⚠️.
> Full per-tool teardown (math, APIs, functions): see `Tool Deep-Dives/`.

---

## 📊 The ranking at a glance

> Two strong free dashboards discovered in round-2 research — **GammaFlip.io** (fastest/broadest)
> and **Glassnode** (best methodology) — join the original five. Hosted tools ranked first, then OSS.

| Rank | Tool | Type | Cost | API? | Best for | Deep-dive |
|------|------|------|------|------|----------|-----------|
| 🥇 1 | **CryptoGamma.io** | Hosted dashboard | **Free** | ✅ Public JSON | Live net/call/put gamma + squeeze/pin levels **+ an API** | [[Tool Deep-Dives/CryptoGamma]] |
| 🥇 1= | **GammaFlip.io** | Hosted dashboard | **Free** | ❔ unconfirmed | **Fastest (~60s) + multi-venue** flip/regime read | [[Tool Deep-Dives/GammaFlip.io]] |
| 🥈 2 | **GEX Terminal Pro** (gexterminal.net) | Hosted terminal | **Free** | ❌ (UI only) | Intraday confluence trade zones + IBIT flow | [[Tool Deep-Dives/GEX Terminal Pro]] |
| 🥉 3 | **Laevitas** | Hosted + API | Free→$50→$500/mo | ✅ REST V1.0 | Cross-exchange, history, automation | [[Tool Deep-Dives/Laevitas]] |
| 4 | **Glassnode — Gamma Exposure** | Research metric | Paid (research) | (metrics platform) | **Best methodology** (taker-flow), validation benchmark | [[Tool Deep-Dives/Glassnode Gamma Exposure]] |
| 5 | **Amberdata AD Derivatives** (ex-GVol) | Institutional data/API | ⚠️ Quote-based | ✅ REST | *True* dealer-positioning GEX, vol surfaces | [[Tool Deep-Dives/Amberdata AD Derivatives]] |
| 6 | **Nathan-Hall/Bitcoin-Options-GEX** | OSS Python | Free (self-host) | — (uses Deribit) | Learn naive OI×Γ GEX from scratch | [[Tool Deep-Dives/Nathan-Hall Bitcoin-Options-GEX]] |
| 7 | **fshahy/dankbit** | OSS Python (Odoo) | Free (self-host) | — (uses Deribit) | Trade-direction dealer gamma, pin risk | [[Tool Deep-Dives/dankbit]] |
| 8 | **zrack/gex-terminal** | OSS Python (TUI) | Free (self-host) | — (multi-provider) | Architecture reference (⚠️ ES/NQ, not BTC) | [[Tool Deep-Dives/zrack gex-terminal]] |

**Equity/reference repos (not BTC, but canonical for the math):** `Matteo-Ferrara/gex-tracker` (CBOE scrape, classic dealers-long-calls/short-puts formula), `jensolson/SPX-Gamma-Exposure`, `aakash-code/GammaGEX`. **Library shortcut:** **CCXT** Deribit connector (`fetchGreeks`, `fetchOption`, `fetchOptionChain`, `fetchOpenInterest`) → see [[05 — APIs and Data Sources (Deribit etc.)]].

> **How to think about the top:** **GammaFlip** = best *live monitor* (60s, Deribit+Bybit+OKX). **CryptoGamma** = best *automatable* (public JSON API + explicit pin/squeeze metrics). **Glassnode** = most *correct* (taker-flow sign, not the naive equity assumption). Use GammaFlip + CryptoGamma live, validate sign against Glassnode/dankbit.

> **Not covered / unverified:** Block Scholes (greeks/API/free-tier claims did **not** survive verification — treat as unconfirmed), Deribit DVOL, Greeks.live, Volmex, Coinglass, Paradigm (no surviving verified GEX-specific claims). See [[08 — Pitfalls and Misconceptions (what NOT to do)]] on trusting vendor marketing.

---

## 🥇 1. CryptoGamma.io — *best free, ready-to-use*

- **URL:** https://cryptogamma.io/dashboard/ (assets: BTC, ETH)
- **What it does:** Computes net / call / put gamma, a directional **bias**, **squeeze levels** (support/resistance/breakout), **pin risk**, **delta-hedging** and **squeeze-risk** metrics, plus realized vs implied vol and 24h call/put flow + C/P ratio.
- **Data source:** Public **Deribit API** (orderbook, OI, mark IV, index price). Independent, not affiliated with Deribit.
- **Refresh:** ~**15 min** (Next.js revalidate cache) + manual refresh button.
- **API:** ✅ **Public JSON** — `GET https://cryptogamma.io/api/public/snapshot?asset=BTC` (also `=ETH`). A fuller "Market Intel API" is *Coming Soon*.
- **Strengths:** Zero setup, free, has an API, gives *actionable levels* not just a chart, export button.
- **Weaknesses:** Naive OI×Γ model (no true dealer tagging); single venue (Deribit); 15-min cadence too slow for scalping; squeeze "support=resistance" can collapse to one number in tight regimes.
- **Verification:** 3-0 confirmed; live JSON fetched 2026-06-20.

## 🥈 2. GEX Terminal Pro — *best free intraday*

- **URL:** https://gexterminal.net/  (distinct from the unrelated `zrack/gex-terminal` repo)
- **What it does:** Full charting terminal. Plots **GEX/DEX option levels** (call/put walls, CR/PS clusters, zero-gamma) and scores **confluence trade zones** across GEX, DEX, **IBIT ETF flow**, VWAP, EMAs (9/21/50/200), RSI, volume profile (POC/VA), the 1-day range, and **Max Pain**. Higher confluence score = more signals agree.
- **Data source:** **Levels from Deribit (5-min refresh)**; **candles streamed from Hyperliquid WS**; optional **US IBIT options overlay via Tradier API** (you supply a free Tradier key).
- **Refresh:** Levels **~5 min**; candles live.
- **API:** ❌ No public data API — it's a front-end terminal. Has TradingView-style drawing tools, screenshot, replay.
- **Strengths:** Free, fastest refresh of the hosted tools, blends options structure with classic TA + ETF flow, intraday-focused (0DTE/1m–4h timeframes).
- **Weaknesses:** No data export/API for automation; confluence scoring is a black box; IBIT overlay needs your own Tradier key.
- **Verification:** 3-0 confirmed; live fetch 2026-06-20.

## 🥉 3. Laevitas — *best paid all-rounder*

- **URL (BTC GEX):** https://app.laevitas.ch/assets/options/gex/btc/deribit
- **What it does:** Institutional crypto-derivatives analytics suite. Dedicated **BTC-Deribit GEX dashboard** (Highcharts: GEX by strike Calls vs Puts, "USD GEX per 1% Move", **GEX term structure**), plus full options stack: option chain, flows, time & sales, vol monitor, skew & butterfly, max pain, etc.
- **Data source:** **15+ exchanges** (Deribit, Bybit, OKX, Hyperliquid…), real-time, **5+ years history** (history gated by tier).
- **API:** ✅ **REST V1.0** — per-strike GEX endpoints:
  - `GET /analytics/options/gex_date_all/{market}/{currency}` (e.g. `/deribit/BTC`) → all options
  - `GET /analytics/options/gex_date/{market}/{currency}/{maturity}` → one maturity
  - Returns `strike`, option type (P/C), GEX value. Docs: https://docs.laevitas.ch/options/analytic
- **Pricing (per seat, as of Jun 2026):** Free $0 (≈1 week history) · Premium **$50/mo** (1yr history, 3 custom dashboards, CSV export, full toolkit) · Enterprise **$500/mo** (unlimited dashboards, **API historical access**, priority) · Custom (contact sales). The GEX **page** is free to view; the **API/history** sit behind paid tiers.
- **Strengths:** Cross-exchange, documented API, deep history, full options suite beyond GEX.
- **Weaknesses:** Best features paywalled; API history is the $500 tier; heavier UI.
- **Verification:** 3-0 confirmed (dashboard, API endpoints, pricing).

## 4. Amberdata AD Derivatives (formerly Genesis Volatility / GVol)

- **URLs:** https://www.amberdata.io/ad-derivatives · docs: https://docs.amberdata.io/reference/derivatives-trades-flow-gamma-gex-snapshots
- **What it does:** Deepest analytics. Claims **true dealer-positioning GEX** by matching option **quote updates to trades to infer the aggressor** (the "AMBERDATA DIRECTION" algorithm, 30+ heuristics), exposing `dealerNetInventory` / `dealerTotalInventory`. Plus full greeks, **portfolio greeks** (delta/gamma/vega), gamma profiles, term-structure richness, and **strike/delta/moneyness vol surfaces**. (Acquired GVol/Genesis Volatility, Oct 2022.)
- **Data source:** Deribit BTC options (broader venue/altcoin coverage was **claimed but refuted** in verification — treat as unconfirmed).
- **API:** ✅ REST + customizable analytics UI (vendor-asserted; exact integration breadth — WebSocket/CSV/S3/Python — was **not** verified).
- **Pricing:** ⚠️ **Quote-based / enterprise**; specific figures and any free tier **could not be verified** — do not assume a free tier.
- **Strengths:** Only tool here claiming *true* aggressor-based dealer GEX vs naive OI×Γ; institutional depth.
- **Weaknesses:** Cost opaque/likely high; methodology accuracy is self-asserted, not independently benchmarked; overkill for most retail.
- **Verification:** Core capability 2-3 votes confirmed; **pricing/free-tier/venue-coverage claims refuted or unverified**.

## 5–7. Open-source repos (self-host)

| Repo | Method | Stack | BTC? | Notes |
|------|--------|-------|------|-------|
| **Nathan-Hall/Bitcoin-Options-GEX** | `OI × Γ(Deribit) × ±1 × 100`, per-strike sum, "bootleg" gamma-flip via cumulative sign change | asyncio + websockets + pandas + matplotlib | ✅ Native BTC | Author calls it a messy 2021 learning project, but the cleanest *naive GEX* example. [[Tool Deep-Dives/Nathan-Hall Bitcoin-Options-GEX]] |
| **fshahy/dankbit** | `Σ sign(buy/sell) × amount × BS_dollar_gamma(Γ·S²)` — **trade-direction** weighted dealer gamma + pin risk | Odoo app + Deribit WS batch service, Docker | ✅ BTC/ETH | Closest OSS to "true" dealer positioning. [[Tool Deep-Dives/dankbit]] |
| **zrack/gex-terminal** | Vectorized BS γ, **volume-as-OI proxy**, walls/zero-gamma/concentration band | NumPy + Textual TUI, provider adapters | ⚠️ **ES/NQ** (0★, new) | Best *architecture* reference; ports to BTC by writing a Deribit adapter. [[Tool Deep-Dives/zrack gex-terminal]] |

---

## 🔗 Best combined workflow (the short version)

1. **Live monitoring:** CryptoGamma (levels + bias + pin risk) **+** GEX Terminal Pro (intraday confluence on the chart).
2. **Automation/alerts:** Poll CryptoGamma `/api/public/snapshot` (free) or Laevitas `gex_date` endpoints (paid) → fire alerts when price approaches the gamma wall / zero-gamma.
3. **History / cross-exchange:** Laevitas API (or Amberdata for institutions).
4. **Validate the math:** Self-host Bitcoin-Options-GEX or dankbit to reproduce the numbers and trust what you trade.

→ Full daily routine in [[07 — Trader Usage Playbook (how to use together)]]. Integration code in [[05 — APIs and Data Sources (Deribit etc.)]].

---

## Sources
- CryptoGamma: https://cryptogamma.io/dashboard/ · https://cryptogamma.io/api/public/snapshot
- GEX Terminal Pro: https://gexterminal.net/
- Laevitas: https://app.laevitas.ch/assets/options/gex/btc/deribit · https://docs.laevitas.ch/options/analytic
- Amberdata: https://www.amberdata.io/ad-derivatives · https://docs.amberdata.io/reference/derivatives-trades-flow-gamma-gex-snapshots
- Repos: https://github.com/Nathan-Hall/Bitcoin-Options-GEX · https://github.com/fshahy/dankbit · https://github.com/zrack/gex-terminal
