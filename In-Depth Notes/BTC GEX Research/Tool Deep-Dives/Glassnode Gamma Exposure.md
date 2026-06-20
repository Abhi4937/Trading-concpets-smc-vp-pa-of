---
title: Deep-Dive — Glassnode Gamma Exposure
tags: [gex, deep-dive, glassnode, taker-flow, methodology, deribit]
created: 2026-06-20
source-quality: primary (verified 3-0, workflow 2026-06-20)
research: https://research.glassnode.com/gamma-exposure/
---

# 🔬 Deep-Dive: Glassnode Gamma Exposure

**Research/metric:** https://research.glassnode.com/gamma-exposure/
**One line:** On-chain analytics firm's GEX metric — the **most methodologically sound** crypto GEX because it uses a **crypto-specific taker-flow reconstruction** instead of borrowing the equity assumption.

---

## 1. Why this one is special — the methodology
Every other free tool uses the **equity convention** (assume dealers long calls / short puts). Glassnode does **not**. Instead (verified 3-0):

> "Crypto options venues expose **who is the taker on each trade**" → Glassnode infers the
> **dealer as the mirror-image counterparty of the taker** on Deribit trades, reconstructing
> *actual* dealer positioning rather than assuming a fixed sign.

This matters because the naive call+/put− assumption is borrowed from equities and is **not reliably true in crypto** (see [[08 — Pitfalls and Misconceptions (what NOT to do)]]). Taker-flow reconstruction is the same spirit as dankbit's trade-direction signing and Amberdata's aggressor matching — but published as a research metric.

## 2. Spec (verified 3-0)
| Attribute | Value |
|-----------|-------|
| Exchange | **Deribit** |
| Assets | BTC, ETH, SOL, XRP, **PAXG** |
| Resolution | **10-minute** intervals |
| Method | Taker-flow / mirror-counterparty reconstruction |

## 3. The concept it reinforces (verified)
- **Positive GEX zones:** "dealers hedge in a way that tends to absorb price shocks — buy on dips, sell on rallies — which dampens volatility."
- **Negative GEX zones:** "dealer hedging flows … amplify price moves. Dealers sell as prices fall and buy as prices rise."

## 4. How to use it
- Treat Glassnode's GEX as your **methodological benchmark**: if the free naive dashboards (CryptoGamma/GammaFlip) disagree with Glassnode, the taker-flow version is usually more trustworthy on *sign*.
- Available via Glassnode's research/metrics platform (subscription analytics product, not a free public API).

## 5. What NOT to do / limits
- Still **Deribit-only**; still a model (taker inference isn't perfect — wash/maker ambiguity exists).
- It's a **paid research metric**, not a free live trading terminal — use it to validate, not to scalp.

## 6. Verdict
**Best methodology** of the hosted options. The "right way" to compute crypto GEX. Use it (or dankbit / Amberdata) to sanity-check the fast naive dashboards. → [[02 — The Math — Greeks to Dollar GEX (with code)]]
