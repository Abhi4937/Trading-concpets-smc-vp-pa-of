---
title: The Market Food Chain
tags: [market-structure, participants, overview, food-chain]
created: 2026-06-21
status: foundation
---

# 🍱 The Market Food Chain — who feeds whom

> The whole ecosystem on one page. The market is **not a level playing field** — order
> flow, speed, capital, and information all tier upward. This note is the map; each layer
> links to its deep-dive.

---

## The hierarchy (top of the food chain = closest to the order flow & fastest)

```
            ┌─────────────────────────────────────────────────────────┐
   ULTIMATE │  CENTRAL BANKS & REGULATORS  (set rates, rules, reserves)│
   FORCES   └─────────────────────────────────────────────────────────┘
            ┌─────────────────────────────────────────────────────────┐
   VENUES   │  EXCHANGES & CLEARING HOUSES (NYSE/Nasdaq/NSE/BSE/CEX)   │ ← sell access, data, colocation
            └─────────────────────────────────────────────────────────┘
            ┌─────────────────────────────────────────────────────────┐
   APEX     │  MARKET MAKERS · WHOLESALERS · HFT · INVESTMENT BANKS    │ ← see your flow, fastest, paid to take the other side
   PREDATORS│  (Citadel Securities, Virtu, Jump…)                      │
            └─────────────────────────────────────────────────────────┘
            ┌─────────────────────────────────────────────────────────┐
   BIG FISH │  INSTITUTIONS · HEDGE FUNDS · PROP FIRMS · WHALES        │ ← huge capital, algos, dark pools, prime-broker leverage
            └─────────────────────────────────────────────────────────┘
            ┌─────────────────────────────────────────────────────────┐
   GATE-    │  BROKERS · PRIME BROKERS · IBs / AFFILIATES / FINFLUENCERS│ ← gate retail access; monetize the flow
   KEEPERS  └─────────────────────────────────────────────────────────┘
            ┌─────────────────────────────────────────────────────────┐
   THE PREY │  RETAIL TRADERS  (no direct market access)              │ ← the product being monetized
            └─────────────────────────────────────────────────────────┘
```

## Who profits from whom (the money flow)
- **Retail** pays: spreads, commissions, financing/leverage interest, and — in B-book forex/CFD — their *losses* directly. ✅ SEBI: **93%** of Indian F&O traders lose (FY22–24).
- **Brokers** earn: commissions, **payment for order flow** (selling your order), margin interest, and (B-book) being your counterparty. → [[08 — Brokers — the business model & conflicts]]
- **Wholesalers / market makers** earn: the **spread** on uninformed retail flow they bought via PFOF. 3 firms handle **70–90%** of US retail flow. → [[11 — Wholesalers, Internalizers & PFOF]]
- **HFT / prop / institutions** earn: speed, scale, and algos. ⚠️ SEBI FY24 (widely reported, *not re-confirmed in our verification pass* — source page bot-gated): prop+FPI made ~₹33,000cr+~₹28,000cr while individuals lost >₹61,000cr, ~96–97% of those pro profits from algorithms. → [[05 — Hedge Funds, Prop Firms & HFT]]
- **Exchanges & clearing houses** earn: transaction fees, **market data**, colocation, listing fees, clearing fees — they profit from *volume*, win or lose. → [[18 — NYSE & Nasdaq (US equities)]]
- **Investment banks** earn: underwriting/advisory fees, trading spreads, information. → [[07 — Investment Banks (sell-side)]]
- **Finfluencers / IBs** earn: bounties from brokers per trader they recruit — whether you win or lose. → [[12 — Finfluencers, IBs & Affiliates]]

## The three axes of edge (why the tiers exist)
| Axis | Retail | Pros at the top |
|------|--------|-----------------|
| **Information** | delayed, public, marketing | order-flow, research, faster data |
| **Speed** | app latency, 15-min feeds | colocation, microseconds |
| **Capital** | small, often leveraged | huge, plus prime-broker leverage |

## The honest framing
This is **structure, not (mostly) conspiracy.** Most of what hurts retail is the *legal* machine — costs, leverage, PFOF, the speed gap — not secret stop-hunting. Genuine illegal manipulation (spoofing, wash trading, last-look) is real, documented, and prosecuted, but it's the minority of why retail loses. Both are covered:
- The legal extraction → [[22 — How the Industry Profits from Retail Losses]]
- The illegal manipulation → [[23 — Manipulation & Predatory Practices]]

## Where to go next
Participants: [[02 — Retail Traders]] · [[04 — Institutions]] · [[05 — Hedge Funds, Prop Firms & HFT]] · [[06 — Market Makers & Dealers]] · [[07 — Investment Banks (sell-side)]] · [[09 — Leverage, Margin & Prime Brokers]] · [[10 — Clearing Houses, CCPs & Custodians]].
By asset class: [[13 — Stocks & Equities participants]] · [[14 — Derivatives (options & futures) participants]] · [[15 — Commodities participants]] · [[16 — Forex participants]] · [[17 — Crypto participants]].
Venues: [[18 — NYSE & Nasdaq (US equities)]] · [[19 — NSE & BSE (India)]] · [[20 — Crypto Exchanges (CEX vs DEX-AMM)]] · [[21 — Forex & the OTC interbank market]].
