---
title: Forex participants
tags: [market-structure, participants, forex, otc, interbank, a-book, b-book, last-look]
created: 2026-06-21
---

# 16 — Forex participants

Forex is a **decentralized, OTC** market — there is no central exchange or single tape. Liquidity flows down a hierarchy, and *where* in that hierarchy you sit determines your price and your conflicts. See [[21 — Forex & the OTC interbank market]].

## The liquidity hierarchy (top to bottom)
- **Central banks** — the ultimate force. They set policy rates, **intervene** directly in FX, and hold the world's FX reserves. Their goal is policy, not profit; a single line from a central bank can reprice a currency instantly (✅ verified). 
- **Tier-1 interbank banks** — the largest dealers, providing the deepest liquidity to each other, historically via platforms like **EBS / Reuters**. They profit on spread and franchise flow.
- **Prime brokers / prime-of-prime** — extend interbank access, credit, and leverage to clients who can't face tier-1 banks directly. They profit on financing and commission. See [[08 — Brokers — the business model & conflicts]].
- **ECNs** — electronic networks aggregating LP quotes into a matched order book.
- **Retail FX / CFD brokers** — the bottom rung, where individual traders connect.

## Execution models: A-book vs B-book
- **ECN / STP (A-book):** The broker passes your order through to liquidity providers and earns commission/markup. Your profit is not their loss — interests are aligned.
- **Market-maker (B-book):** The broker **internalizes** the order and takes the *other side* of your trade. Your loss is directly their revenue — a structural conflict (📄 sourced).
- **Why it matters:** The same "broker" can run both books, routing winners to the market and warehousing losers.

## Last look
- **Role/mechanism:** An LP or broker can **reject** a trade after it has already seen your order and the price has moved — a final option to back out of an unfavourable fill.
- **Why it matters:** It can be abused to fade clients. **Barclays paid $150M to the NY DFS over last-look abuse** (📄 sourced, NYDFS) — documented and penalized, not theoretical.

## Corporates
- **Role:** Multinationals hedging real FX exposure on revenues, costs, and balance sheets.
- **Why they matter:** Like commodity commercials, they trade for need, not view — a natural, non-speculative flow.

## What it means for retail
First ask *which book your broker runs* — in a B-book your stop-out is their P&L. Expect last-look rejections and asymmetric slippage around news. You sit at the bottom of the liquidity stack, so spreads widen against you exactly when central banks or tier-1 desks are most active.

## Limitations
OTC means no consolidated volume or true depth — "volume" indicators are broker-local. Execution quality is opaque and varies by venue; central-bank intervention is discretionary and unannounced.

## Sources
- https://www.bis.org/statistics/rpfx22.htm
- https://www.dfs.ny.gov/reports_and_publications/press_releases/pr1511181
- https://www.investopedia.com/articles/forex/06/interbank.asp
