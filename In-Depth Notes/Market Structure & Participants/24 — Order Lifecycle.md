---
title: "24 — Order Lifecycle"
tags: [market-structure, order-routing, pfof, clearing, settlement, retail]
created: 2026-06-21
---

# 24 — Order Lifecycle

> **Thesis:** When a retail trader taps "Buy," the mental model of "my order goes to the exchange and meets a seller" is *usually wrong*. The order passes through a routing decision, is most often **internalized by a wholesaler**, and only then is it **cleared** and **settled** by a chain of institutions the trader never sees. This note traces that path end to end.

---

## The end-to-end flow

```
                          RETAIL ORDER LIFECYCLE (US equities, marketable order)
                          =========================================================

   (1) CLICK
   ┌─────────────────┐
   │  Broker app     │   Trader taps BUY 100 AAPL @ market
   │  (Robinhood,    │
   │   Schwab, etc.) │
   └────────┬────────┘
            │  order ticket
            ▼
   (2) BROKER ROUTING DECISION  ── the broker chooses where the order goes ──
   ┌──────────────────────────────────────────────────────────────────────┐
   │                                                                        │
   │   (a) WHOLESALER via PFOF          (b) EXCHANGE          (c) DARK POOL │
   │       Citadel Securities,              NYSE / Nasdaq          / SELF-  │
   │       Virtu, etc.                      lit order book        INTERNAL- │
   │       broker is PAID for flow;         (price-time          IZATION    │
   │       wholesaler INTERNALIZES          priority)                       │
   │       at a price slightly             ── 90%+ of marketable retail    │
   │       better than NBBO                    flow goes to ~6 wholesalers  │
   │                                           (📄 Congress / CRS)          │
   └───────────┬─────────────────────┬──────────────────────┬──────────────┘
               │                     │                       │
               ▼                     ▼                       ▼
   (3) EXECUTION
   ┌──────────────────────────────────────────────────────────────────────┐
   │  Matched against the WHOLESALER'S INVENTORY (it takes the other side), │
   │  or against the EXCHANGE ORDER BOOK under price-time priority.         │
   │  A fill price and quantity are returned to the broker → shown to you.  │
   └────────┬───────────────────────────────────────────────────────────────┘
            │  executed trade
            ▼
   (4) CLEARING  ── the trade is NOVATED to a Central Counterparty (CCP) ──
   ┌──────────────────────────────────────────────────────────────────────┐
   │  NSCC (US equities) / OCC (US options) steps in between buyer & seller.│
   │  By NOVATION it becomes BUYER to every seller and SELLER to every      │
   │  buyer, so neither side faces the other's default risk (✅ novation).  │
   └────────┬───────────────────────────────────────────────────────────────┘
            │  netted obligations
            ▼
   (5) SETTLEMENT  ── ownership actually changes hands ──
   ┌──────────────────────────────────────────────────────────────────────┐
   │  T+1 in US equities. The DTC central securities depository moves the   │
   │  shares by BOOK-ENTRY (electronic ledger; no paper certificate).       │
   │  Cash and securities are exchanged; you now legally own the shares.    │
   └────────────────────────────────────────────────────────────────────────┘
```

---

## Stage-by-stage detail

### (1) Click
The lifecycle begins with a tap in the broker app. The trader sees a single "Buy" button; everything downstream is invisible to them. The broker captures the ticket (symbol, side, size, order type) and must now decide **where to send it** — a decision governed by a duty of *best execution*, not by the trader. See [[25 — Regulation by Region]] for who enforces that duty (FINRA Rule 5310 in the US).

### (2) Broker routing decision
The broker has three broad choices:

- **(a) Sell the order to a wholesaler via PFOF.** Payment for Order Flow: the broker is *paid* by a **wholesaler** (Citadel Securities, Virtu, and a handful of others) to send retail flow there. The wholesaler **internalizes** the order — it fills it against its own inventory at a price **slightly better than the NBBO** (the National Best Bid/Offer), capturing the spread while still giving the trader "price improvement." This is the dominant path. **In the US, 90%+ of marketable retail orders are handled by roughly six wholesalers** (📄 Congress / CRS).
- **(b) Route to a lit exchange.** The order is sent to **NYSE or Nasdaq** and posted/matched on the public order book under **price-time priority**. See [[18 — NYSE & Nasdaq (US equities)]].
- **(c) Send to a dark pool or internalize itself.** A larger broker may route to an off-exchange venue (dark pool) or cross the order against its own book.

Why (a) dominates: retail flow is **uninformed** (not driven by private information), so wholesalers can profitably take the other side. PFOF aligns the broker's revenue with routing there.

> **Key point — "trading on the exchange" is frequently NOT what happens.** The most common outcome for a marketable retail order is that it **never touches NYSE or Nasdaq**. It is filled by a wholesaler internalizing it off-exchange. The "market" the retail order meets is usually a single principal counterparty, not a public auction. See [[11 — Wholesalers, Internalizers & PFOF]].

### (3) Execution
- **Wholesaler path:** the wholesaler is the **counterparty**. It fills from inventory, marginally inside the NBBO. There is no "matching" against another retail trader.
- **Exchange path:** the order book matches the incoming order against resting orders by **price-time priority** — best price first, and at a given price, earliest order first.

A fill (price + quantity) is generated and reported back up the chain to the broker, which displays it to the trader as "filled."

### (4) Clearing — novation to a CCP
The executed trade is passed to a **Central Counterparty (CCP)**:
- **NSCC** for US equities,
- **OCC** for US listed options.

Through **novation**, the CCP legally **interposes itself between the two original parties**: it becomes the buyer to every seller and the seller to every buyer. The original bilateral contract is extinguished and replaced by two contracts with the CCP. Consequently **neither side bears the other's counterparty (default) risk** — they face only the CCP, which is backed by margin and a default fund (✅ novation; cf. LCH / RBA explanations of CCP novation). The CCP also **nets** offsetting obligations so only the residual is settled. See [[10 — Clearing Houses, CCPs & Custodians]].

### (5) Settlement
Ownership is transferred:
- **Timing:** **T+1** for US equities (one business day after trade date).
- **Mechanism:** the **DTC** (Depository Trust Company), the US central securities depository, moves the securities by **book-entry** — an electronic ledger update. There is **no paper certificate**; shares are held in immobilized/dematerialized form (📄 DTCC).

Only at settlement does legal ownership actually change hands. Everything the trader "saw" at click and fill was a promise that this step would complete.

---

## Contrast: the retail forex / CFD trade

A retail **forex or CFD** order often follows a completely different — and shorter — path:

```
   CLICK ──► B-BOOK BROKER  ◄── the broker IS your counterparty
              │
              │  (no exchange, no CCP, no central depository)
              ▼
        Position lives ONLY on the broker's own book.
        Nothing is novated. Nothing settles externally.
        Your "trade" is a bilateral bet against the firm.
```

In the **B-book** model the broker takes the opposite side of the client's position and **does not hedge it externally**. The trade **never reaches any exchange**, there is **no CCP**, and **nothing clears or settles through a central depository**. The client's profit is the broker's loss and vice versa — a structural conflict of interest absent in the cleared, exchange-traded equity flow above. See [[21 — Forex & the OTC interbank market]].

> **Takeaway:** The phrase "I traded on the exchange" describes neither the typical US retail *equity* order (internalized by a wholesaler) **nor** the typical retail *forex/CFD* order (a bilateral bet against a B-book). Knowing which path your order actually takes tells you who profits from your flow and who, if anyone, guarantees the trade.

---

## Sources

- https://crsreports.congress.gov/product/pdf/IF/IF11793 (Congressional Research Service — Payment for Order Flow; retail flow concentration among wholesalers) — 📄 sourced
- https://www.dtcc.com/about/businesses-and-subsidiaries/dtc (DTCC / DTC — book-entry settlement, central securities depository) — 📄 sourced
- https://www.dtcc.com/about/businesses-and-subsidiaries/nscc (DTCC / NSCC — central counterparty for US equities) — 📄 sourced
- https://www.theocc.com/ (OCC — central counterparty / clearing for US listed options) — 📄 sourced
- https://www.sec.gov/oiea/investor-alerts-and-bulletins/trade-execution-investor-bulletin (SEC — how trade execution and order routing work) — 📄 sourced
- https://www.lch.com/services/novation (LCH — novation: CCP becomes counterparty to both sides) — ✅ verified
- https://www.rba.gov.au/payments-and-infrastructure/financial-market-infrastructure/central-counterparties.html (Reserve Bank of Australia — CCP novation removes counterparty risk) — ✅ verified

## See also
- [[11 — Wholesalers, Internalizers & PFOF]]
- [[10 — Clearing Houses, CCPs & Custodians]]
- [[18 — NYSE & Nasdaq (US equities)]]
- [[21 — Forex & the OTC interbank market]]
- [[25 — Regulation by Region]]
