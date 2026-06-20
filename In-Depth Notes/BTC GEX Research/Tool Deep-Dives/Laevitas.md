---
title: Deep-Dive — Laevitas
tags: [gex, deep-dive, laevitas, deribit, api, rest]
created: 2026-06-20
source-quality: primary (live capture + API docs 2026-06-20)
---

# 🔬 Deep-Dive: Laevitas

**BTC GEX page:** https://app.laevitas.ch/assets/options/gex/btc/deribit
**API docs:** https://docs.laevitas.ch/options/analytic
**One line:** Institutional crypto-derivatives analytics suite with a dedicated BTC-Deribit GEX dashboard and a documented REST API across 15+ exchanges.

---

## 1. What it is
A full options-analytics platform (not just GEX). The GEX page is one module inside a suite: Option Chain, Overview, Screener, Time & Sales, Volume & OI, Flows, Strategies, Volatility, Skew & BF, Vol Monitor, Vol Run, GEX, Max Pain.

## 2. The BTC GEX dashboard (what's on screen)
Captured live via agent-browser (Highcharts 11.4.8):
1. **Gamma Exposure by strike** — Calls vs Puts bar series (toggle each), x-axis = Strike, with expiry and strike-range filters (e.g. All Expirations, 40000–125000).
2. **USD GEX per 1% Move** — dollar-scaled GEX contribution per strike (the practically useful version — see [[02 — The Math — Greeks to Dollar GEX (with code)]]).
3. **GEX Term Structure** — GEX across maturities.
- Selectors: **Asset (BTC)**, **Exchange (Deribit)**, **window (1W)**, **All Expirations / per-maturity**.
- Each chart has "View as data table" → exportable numeric values; publish timestamp shown.

## 3. The REST API (V1.0) — endpoints, params, returns
| Endpoint | Params | Returns |
|----------|--------|---------|
| `GET /analytics/options/gex_date_all/{market}/{currency}` | market=`deribit`, currency=`BTC` | All options: `strike`, option type (P/C), GEX value |
| `GET /analytics/options/gex_date/{market}/{currency}/{maturity}` | + `maturity` (e.g. `24DEC26`) | Single-maturity per-strike GEX |
- Deribit currencies supported: **BTC, ETH, PAXG, SOL, XRP**.
- Auth via API key (paid tiers). Use it to pull per-strike GEX into your own scripts/alerts → [[05 — APIs and Data Sources (Deribit etc.)]].

## 4. Pricing (per seat, Jun 2026)
| Tier | Price | Key unlocks |
|------|-------|-------------|
| Free | **$0** | Live dashboards, ~**1 week** history |
| Premium | **$50/mo** | **1 year** history, 3 custom dashboards, unlimited charting, full toolkit, **CSV export** |
| Enterprise | **$500/mo** | Unlimited dashboards, **API historical data access**, priority support |
| Custom | contact | Bespoke |
> The GEX page itself is **free to view**. The **API + deep history** is what you pay for.

## 5. How to use it
- **Free:** eyeball the BTC GEX page for cross-checking CryptoGamma's levels against a second computation.
- **Premium+:** export CSV / hit the API for **per-strike GEX history**, build alerts, compare exchanges.
- Strength = **cross-exchange + history + a real API**; the only hosted tool here with all three.

## 6. What NOT to do / limits
- Don't expect the **API/history on the free tier** — it's ≈1 week and no API key.
- Heavier, busier UI than CryptoGamma; overkill if you only want one number.
- Still vendor-computed GEX (methodology not fully published) — validate against your own engine for anything you size on.

## 7. Verdict
🥉 **Rank #3 / best paid all-rounder.** The upgrade path once free tools aren't enough (history, automation, cross-exchange). → [[04 — Dashboards Directory + RANKING]]
