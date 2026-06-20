---
title: "NSE & BSE (India)"
tags: [market-structure, exchanges, india, sebi, index-options]
created: 2026-06-21
---

# 19 — NSE & BSE (India)

## What it is
The **NSE** (National Stock Exchange, dominant by volume) and **BSE** (Bombay Stock Exchange — Asia's oldest) are India's two principal venues. Both run fully electronic order-book matching engines under **SEBI** regulation. India's defining feature: it is **dominated by index options** (Nifty, BankNifty), with derivative volumes among the **highest globally** — the FIA has described its "meteoric rise" (📄 FIA).

## Architecture (matching engine, order book, latency/colocation)
Both exchanges operate central limit order-book matching engines with **price-time priority**. Brokers connect via exchange-provided gateways and **colocation** facilities; tick-by-tick (TBT) data feeds drive algorithmic and HFT participation. Critically, **the broker sits between client and exchange** — there is **no direct retail market access**; every retail order is routed through a registered broker member.

```
CLIENT ──> BROKER (member) ──> EXCHANGE GATEWAY ──> MATCHING ENGINE
                                                          │
                                                  price-time book
                                                          │
                                                   CCP (NCL / ICCL)
                                                          │
                                                     SETTLEMENT
```

## Order lifecycle (click → execution → clearing → settlement)
Client click → broker risk-checks & forwards → exchange matching engine pairs against the book → execution → **clearing via a CCP**: **NSE Clearing Ltd (NCL)** for NSE, **Indian Clearing Corporation (ICCL)** for BSE, which novate and guarantee trades → **settlement**. India moved to a rolling **T+1** cycle and is **piloting T+0**. See [[24 — Order Lifecycle]] and [[10 — Clearing Houses, CCPs & Custodians]].

## Who provides liquidity
Proprietary/HFT desks, registered brokers, institutional (FII/DII) flow, and a very large retail options base. Market-making in index options and ETFs is increasingly algorithmic. Unlike the US, there is no PFOF-wholesaler tier — order flow goes broker → exchange.

## How the venue makes money
- **Transaction charges** (per-trade, with notional-based options charges).
- **Market data** feeds (including TBT/colocation feeds).
- **Colocation** rack and connectivity fees.
- **Listing fees** from issuers.

## Regulation
**SEBI** is the statutory regulator. Recent reform agenda (📄 SEBI) targets retail derivative losses:
- **Expiry rationalization** (limiting weekly expiries per exchange).
- **Higher F&O lot sizes / contract values** to deter under-capitalized speculation.
- Policy is driven by SEBI's finding that **~93% of individual F&O traders lose money** over the studied period — a headline statistic shaping the entire reform package.

## Limitations / controversies
- **NSE co-location scandal**: certain brokers obtained **preferential early access** to the **tick-by-tick data feed** — exploiting the **order in which servers connected** and **dark-fibre** routing — an unfair latency edge. SEBI imposed **fines and disgorgement** (📄 scroll.in; ICSI case snapshot).
- **Retail derivative harm**: the 93%-lose study underscores that the world's largest options market is, for individuals, largely wealth-destructive.
- **Broker-gating**: mandatory broker intermediation concentrates operational/credit risk at the member layer — see [[08 — Brokers — the business model & conflicts]].

## Sources
- https://www.fia.org/marketvoice/articles/meteoric-rise-indian-derivatives-markets
- https://www.sebi.gov.in/
- https://scroll.in/article/921893/explained-the-nse-co-location-scam-and-why-it-matters
- https://www.nseindia.com/products-services/clearing-settlement-process
- https://www.bseindia.com/
