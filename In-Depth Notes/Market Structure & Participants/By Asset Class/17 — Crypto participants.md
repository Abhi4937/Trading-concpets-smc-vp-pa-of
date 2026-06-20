---
title: Crypto participants
tags: [market-structure, participants, crypto, dex, amm, mev, stablecoins, miners]
created: 2026-06-21
---

# 17 — Crypto participants

Crypto re-invents every traditional role on-chain — and then collapses several of them into single entities. The participants below have no clean equity analogue. See [[20 — Crypto Exchanges (CEX vs DEX-AMM)]].

## Miners / validators
- **Role:** Secure the chain (proof-of-work mining or proof-of-stake validation) and order transactions.
- **How they profit:** Block rewards (newly issued coins) plus transaction fees.
- **Why they matter:** New issuance to miners/validators is **structural sell pressure** — they have real-world costs (power, hardware) to cover, so coins flow to market regardless of price view (✅ verified mechanism).

## Crypto market makers (Wintermute, GSR, Jump Crypto)
- **Role:** Quote two-sided liquidity across CEX and DEX venues.
- **How they profit:** Spread and inventory edge — and often **token deals**, where a project pays them in its own token to provide liquidity at launch.
- **Why they matter:** Their token-loan arrangements mean early "liquidity" can be a thin, conflicted veneer.

## DEX / AMM liquidity providers (LPs)
- **Role:** Deposit token *pairs* into pools (e.g. Uniswap) instead of quoting an order book.
- **How they trade/profit:** Pricing follows the **constant-product** rule x*y=k; LPs earn swap fees but bear **impermanent loss** when the pair's relative price moves (📄 sourced — Uniswap analysed at ~$4B liquidity across ~95.8M interactions, JoF).
- **Why they matter:** This is a genuinely new market-making primitive — passive, permissionless, but with a structural loss-versus-rebalancing drag.

## Stablecoin issuers (Tether, Circle)
- **Role:** Issue USDT/USDC, the dollar rails of crypto.
- **How they profit:** The **float** — they hold reserves (largely T-bills) backing the coins and keep the yield (📄 sourced).
- **Why they matter:** Stablecoin supply expansion/contraction is a proxy for dollar liquidity entering/leaving crypto.

## OTC desks
- **Role:** Execute large block trades off-book to avoid moving the screen price.
- **Why they matter:** Big flows you never see on the exchange tape happen here.

## MEV searchers / validators
- **Role:** Extract value by **reordering or inserting** transactions within a block.
- **How they profit:** Sandwich attacks, on-chain front-running, arbitrage between pools (📄 sourced).
- **Why they matter:** On a public mempool, your DEX swap can be legally front-run — a tax invisible in TradFi.

## Crypto lending / leverage platforms
- **Role:** Supply margin and yield; their liquidation cascades drive the violent wicks crypto is known for.

## Key point
A **centralized crypto exchange often wears ALL hats at once** — broker + market maker + custodian + clearer + sometimes prop trader. That concentration of conflicts is structurally impossible in regulated equities, where these functions are legally separated (✅ verified). See [[20 — Crypto Exchanges (CEX vs DEX-AMM)]].

## What it means for retail
Assume the venue may be trading against you and can see your liquidations. On DEXs, your swaps are front-run by MEV and your LP position bleeds impermanent loss. Track stablecoin supply for liquidity, and miner/issuance flows for structural sell pressure.

## Limitations
On-chain data is transparent but pseudonymous; CEX internals (proprietary trading, custody quality) are opaque and largely unregulated. Token-deal terms and OTC flows are private.

## Sources
- https://docs.uniswap.org/contracts/v2/concepts/protocol-overview/how-uniswap-works
- https://www.theblock.co/data/decentralized-finance/dex-non-custodial
- https://onlinelibrary.wiley.com/journal/15406261
