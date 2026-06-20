---
title: "Crypto Exchanges (CEX vs DEX-AMM)"
tags: [market-structure, exchanges, crypto, cex, dex, amm]
created: 2026-06-21
---

# 20 — Crypto Exchanges (CEX vs DEX-AMM)

## What it is
Crypto trades through two opposed venue designs. **Centralized exchanges (CEX)** — Binance, Coinbase, OKX — run a central limit order book and **custody client funds** ("not your keys, not your coins"). **Decentralized exchanges (DEX)** — Uniswap — replace the order book and custodian with on-chain **smart contracts** and **automated market maker (AMM)** pools.

## Architecture (matching engine, order book, latency/colocation)
A **CEX** runs an off-chain matching engine over a central limit order book; deposits sit in exchange-controlled wallets. The operator is frequently **also market maker, clearer, and prop desk** — a stack of conflicts under one roof. A **DEX-AMM** has no order book and no operator-as-counterparty: prices come from a **constant-product** invariant **x · y = k**, where swapping against pool reserves moves price along the curve (📄 Uniswap / JoF).

```
      CEX                               DEX (AMM)
  ┌──────────┐                    ┌────────────────┐
  │ order    │  custody $$$       │  x · y = k     │
  │ book +   │◄── client funds    │  reserve pool  │
  │ engine   │                    │  (LP-supplied) │
  └──────────┘                    └────────────────┘
  operator = MM/clearer/prop      self-custody, on-chain
```

## Order lifecycle (click → execution → clearing → settlement)
**CEX**: deposit (lose key control) → place order → matched off-chain on the book → settled as an **internal ledger entry**; on-chain only at withdrawal. **DEX**: sign a wallet transaction → smart contract swaps against the pool → **atomic on-chain settlement** in one block; **no central custody or clearing**. See [[24 — Order Lifecycle]].

## Who provides liquidity
**CEX**: professional market makers, the exchange's own desk, and taker flow. **DEX**: **liquidity providers (LPs)** deposit token pairs into pools and earn fees (bearing impermanent loss). See [[17 — Crypto participants]].

## How the venue makes money
- **Trading fees** (maker/taker on CEX; swap fees split to LPs + protocol on DEX).
- **Listing fees** (CEX).
- **Liquidation fees** and **funding** on perpetuals (CEX).
- **Withdrawal fees** (CEX).

## Derivatives mechanics (CEX)
**Perpetual futures** with no expiry use a **funding rate** to tether the perp to spot. A **liquidation engine** closes under-margined positions; Binance charges a **0.3% liquidation fee** that feeds an **insurance fund**, and if that fund is insufficient, **auto-deleveraging (ADL)** claws profit from opposing positions (📄 Binance).

## Regulation
Fragmented and jurisdiction-dependent. Regulated venues (Coinbase, Gemini) face securities/AML oversight and show normal trading patterns; many offshore venues operate with minimal supervision.

## Limitations / controversies
- **Wash trading**: on unregulated exchanges it averages **>70% of reported volume (median 79.1%)** across 29 exchanges — roughly **$4.5T of fake spot volume in Q1 2020 alone**; regulated venues show **<3%** of spot (📄 NBER w30783). Reported volume is largely fiction.
- **Custody/conflict stack**: a CEX as custodian + MM + prop desk + clearer is the structural setup behind multiple collapses.
- **DEX trade-offs**: MEV/front-running, impermanent loss, and slippage on the constant-product curve for large orders.

## Sources
- https://www.nber.org/papers/w30783
- https://www.binance.com/en/support/faq/liquidation
- https://uniswap.org/whitepaper.pdf
- https://docs.uniswap.org/concepts/protocol/swaps
