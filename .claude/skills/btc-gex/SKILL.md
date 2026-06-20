---
name: btc-gex
description: Use when analyzing or trading Bitcoin with gamma exposure (GEX), dealer/market-maker hedging, gamma walls, zero-gamma / gamma flip, call/put walls, pin risk, squeeze levels, or BTC options positioning on Deribit; or when reading GEX dashboards (CryptoGamma, GammaFlip, GEX Terminal, Laevitas, Glassnode, Amberdata) or building/validating a GEX calculation.
---

# BTC Gamma Exposure (GEX)

## Overview
GEX measures how much BTC options dealers must hedge per unit move — it tells you the **environment** (vol dampened vs amplified) and the **levels** (walls, flip), **not direction**. Backed by the research vault at `In-Depth Notes/BTC GEX Research/` (primary-source + adversarially-verified). Always read the relevant vault note before giving depth; cite the honesty flags.

## Core principle
> Above the gamma flip + positive GEX → **fade/mean-revert**.
> Below the flip + negative GEX → **follow/breakout**.
> The flip cross is the trade. Walls are targets/triggers, not certainties.

## The decision workflow (run in order)
1. **Regime** — net GEX sign. `+` = long gamma (dealers buy dips/sell rips → pin, vol compress). `−` = short gamma (sell dips/buy rips → trend, vol expand).
2. **Flip** — is price above or below zero-gamma / the gamma flip (net GEX = 0)? That's the regime boundary.
3. **Levels** — mark gamma wall (max |GEX|), call wall (resistance), put wall (support), max pain.
4. **Fragility** — pin risk (↑ into expiry → range), squeeze risk (↑ → breakout-prone), DVOL/IV-vs-RV.
5. **Trigger** — never trade GEX alone; require a price/flow trigger and tool **agreement**.

**For alerts/automation, default to polling CryptoGamma's free `/api/public/snapshot?asset=BTC`** (fire on net-GEX sign flip, wall/flip approach, or high pin risk). Use the **Laevitas REST API only when you need history or cross-exchange** depth.

## Quick reference — which tool, when
| Need | Use | Note |
|------|-----|------|
| Fast live regime/flip | **GammaFlip.io** (~60s, Deribit+Bybit+OKX) | best monitor |
| Levels + risk + **API** | **CryptoGamma.io** (`/api/public/snapshot?asset=BTC`) | best automatable |
| Intraday chart confluence | **GEX Terminal Pro** (gexterminal.net) | +IBIT/Tradier |
| History / cross-exchange / REST | **Laevitas** (`gex_date_all/{market}/{currency}`) | paid API |
| Correct sign (methodology) | **Glassnode** (taker-flow) / **dankbit** | validate naive tools |
| Institutional true dealer GEX | **Amberdata** | quote-priced |

## Data + math (one line)
Root source = **Deribit** (~85–90% crypto options OI). Per-strike (equity convention):
`GEX = Γ × OI × ContractSize × S² × 0.01`; `Net = ΣCallGEX − ΣPutGEX`. Sign tiers: naive (call+/put−) → trade-aware (dankbit) → **taker-flow (Glassnode)** → aggressor-matched (Amberdata). Full code/derivation: vault note `02 — The Math …`.

## Vault map (read for depth)
- Concept → `01 — What Gamma Exposure (GEX) Is`
- Math + code → `02 — The Math — Greeks to Dollar GEX (with code)`
- Reading dashboards + scenario matrix → `03 — How to Read a GEX Chart (interpretation)`
- Tool ranking + per-tool deep-dives → `04 — Dashboards Directory + RANKING` and `Tool Deep-Dives/`
- APIs + copy-paste code → `05 — APIs and Data Sources (Deribit etc.)`
- Build your own engine → `06 — Build Your Own GEX Engine (architecture)`
- Trading playbook → `07 — Trader Usage Playbook (how to use together)`
- Pitfalls → `08 — Pitfalls and Misconceptions (what NOT to do)`

## Common mistakes (what NOT to do)
- ❌ Reading naive GEX as truth — call+/put− is an *equity assumption*; in crypto prefer taker-flow (Glassnode/dankbit). Disagreement between tools = sign ambiguity.
- ❌ Treating walls / flip as guaranteed S/R — they're modeled estimates; confirm with price.
- ❌ Cadence mismatch — don't scalp a 1m chart off a 15-min snapshot.
- ❌ "Negative GEX → go short" — it means amplified moves **both** ways (vol, not direction).
- ❌ Holding a pin thesis **through** the Deribit 08:00 UTC expiry — re-read GEX after.
- ❌ Repeating unverified vendor claims (Amberdata free-tier/pricing/multi-venue, Block Scholes API) as fact — flagged unconfirmed in the vault.
