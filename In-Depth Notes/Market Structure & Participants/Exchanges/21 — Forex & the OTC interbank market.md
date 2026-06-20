---
title: "Forex & the OTC interbank market"
tags: [market-structure, exchanges, forex, otc, interbank, last-look]
created: 2026-06-21
---

# 21 — Forex & the OTC interbank market

## What it is
Spot FX has **no central exchange and no central clearing** — it is a **decentralized OTC web** of bilateral credit relationships layered in a strict liquidity hierarchy. Price and access depend on where you sit in that hierarchy, not on a single matching engine.

## Architecture (matching engine, order book, latency/colocation)
There is no single book. The top of the market is the **interbank** layer, where tier-1 banks trade on primary venues — **EBS** and **Reuters Matching** — which do run electronic order books. Below that, liquidity is **aggregated and re-distributed** down the chain. Retail trades a synthetic price assembled by their broker from upstream feeds.

```
LIQUIDITY HIERARCHY (top = tightest pricing)
  Tier-1 banks ── EBS / Reuters Matching (interbank book)
        │
  Prime brokers (PB)
        │
  Prime-of-prime (PoP)
        │
  ECNs
        │
  Retail FX / CFD brokers ──► you
```

## Order lifecycle (click → execution → clearing → settlement)
Retail click → broker either **A-books** (ECN/STP pass-through to liquidity providers) or **B-books** (internalizes, takes the other side) → fill (subject to **last look**) → for the interbank leg, settlement via **correspondent banking** or **CLS** to mitigate settlement (Herstatt) risk. **Retail CFDs never settle a real currency** — they are cash-settled bets on price. See [[24 — Order Lifecycle]].

## Who provides liquidity
Tier-1 banks at the top, then prime brokers, prime-of-prime, ECNs, and aggregators feeding retail/CFD brokers. See [[16 — Forex participants]].

## Execution models
- **A-book (ECN/STP)**: broker passes the order through to LPs and earns commission/markup — interests aligned.
- **B-book (market maker)**: broker **internalizes** and takes the opposite side; the client's loss is the broker's revenue — a direct conflict. See [[08 — Brokers — the business model & conflicts]].

## How the venue makes money
- **Spread** (bid/ask markup).
- **B-book client losses** (broker is the counterparty).
- **Swap / financing** on overnight positions.
- **Commissions** (on A-book/ECN accounts).

## Regulation
Fragmented by jurisdiction: **FCA / ESMA** impose strict leverage caps and conduct rules; many brokers operate **offshore** with light-touch oversight. There is no single global FX regulator.

## Limitations / controversies
- **Last look**: an LP or broker may **reject a trade after seeing the price** in the hold window — a latency option against the client. Documented abuse: **Barclays paid $150M to the NY DFS** over last-look practices (📄 NYDFS pr1511181).
- **B-book conflict**: when the broker profits from client losses, incentives diverge from best execution.
- **No central clearing**: counterparty/credit risk is bilateral; settlement risk is real outside CLS.
- **Opacity**: no consolidated tape — the "price" you see is broker-constructed.

## Sources
- https://www.dfs.ny.gov/reports_and_publications/press_releases/pr1511181
- https://www.bis.org/cpmi/publ/d164.htm
- https://www.cls-group.com/products/settlement/clssettlement/
- https://www.fca.org.uk/firms/financial-promotions-and-adverts/cfds
