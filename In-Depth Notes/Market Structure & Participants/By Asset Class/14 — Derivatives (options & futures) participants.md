---
title: Derivatives (options & futures) participants
tags: [market-structure, participants, derivatives, options, futures, gamma, cot]
created: 2026-06-21
---

# 14 — Derivatives (options & futures) participants

These actors exist because derivatives are *contracts*, not assets — someone must quote them, clear them, and take the other side of risk transfer. Universal MMs are in [[06 — Market Makers & Dealers]].

## Options market makers & dealers
- **Role:** Continuously quote bid/ask on options and absorb whatever order flow arrives.
- **How they trade:** They quote, then **delta-hedge** the directional exposure in the underlying, and manage **gamma** as the underlying moves (re-hedging as delta changes).
- **How they profit:** The bid-ask spread plus a modelled edge (selling implied vol they believe is rich); the hedge neutralises direction so the spread/edge is the income.
- **Why they matter:** Their *mechanical* hedging is what creates aggregate **gamma exposure** in the market — dealers short gamma must buy strength / sell weakness (amplifying moves), long gamma does the reverse (dampening). This is the entire premise of the BTC GEX work in `In-Depth Notes/BTC GEX Research/`. (✅ verified mechanism.)

## Hedgers vs speculators
- **Role:** Hedgers (commercials) hold the physical/business exposure and use derivatives to remove price risk; speculators have no underlying exposure and take risk on for profit.
- **How they "profit":** A hedger *loses* on the derivative when the market moves their way — but that loss is offset by a gain on the physical position; the net is locked-in certainty, not P&L (📄 sourced). Speculators profit purely from the price move.
- **Why they matter:** Markets need both — risk transfer requires a willing risk-taker on the other side.

## The OCC (Options Clearing Corporation)
- **Role:** The central counterparty (CCP) for listed US options.
- **How it works:** Via **novation** it becomes buyer to every seller and seller to every buyer, guaranteeing performance and netting exposure. (✅ verified.)
- **Why it matters:** It removes bilateral counterparty risk — you never worry whether the option writer can pay.

## FCMs (Futures Commission Merchants)
- **Role:** Carry customer futures accounts, collect margin, and route trades to clearing.
- **How they profit:** Commissions plus interest on margin balances.
- **Why they matter:** Retail and institutions reach the futures clearinghouse *through* an FCM — see [[08 — Brokers — the business model & conflicts]].

## CFTC Commitments of Traders (COT)
- **Role:** Weekly report splitting open interest into **commercials (hedgers — often "smart money")**, **non-commercials (large speculators / managed money)**, and small/non-reportable traders.
- **Why it matters:** Extreme positioning (e.g. managed money crowded long) is a contrarian/positioning tell (📄 sourced). See the parallel use in [[15 — Commodities participants]].

## What it means for retail
You are usually the *speculator* taking risk from a hedger and paying spread to a dealer. Watch dealer gamma to anticipate whether moves get amplified or pinned, and read COT to see whether you are crowded with the dumb-money cohort.

## Limitations
COT is lagged (Tuesday data, Friday release) and category labels are imperfect — some "commercials" are swap dealers facing index funds. Gamma estimates are modelled, not disclosed.

## Sources
- https://www.theocc.com/company-information/what-is-the-occ
- https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm
- https://www.cboe.com/education/
