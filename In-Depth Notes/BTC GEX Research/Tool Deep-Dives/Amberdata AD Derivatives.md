---
title: Deep-Dive — Amberdata AD Derivatives (ex-Genesis Volatility / GVol)
tags: [gex, deep-dive, amberdata, gvol, dealer-positioning, api]
created: 2026-06-20
source-quality: primary docs + marketing (several pricing/coverage claims REFUTED in verification)
---

# 🔬 Deep-Dive: Amberdata AD Derivatives (formerly Genesis Volatility / GVol)

**URLs:** https://www.amberdata.io/ad-derivatives · docs: https://docs.amberdata.io/reference/derivatives-trades-flow-gamma-gex-snapshots
**One line:** The deepest crypto-options data/analytics provider; claims *true* dealer-positioning GEX from quote-to-trade aggressor matching. Enterprise-priced.

> ⚠️ **Honesty flag:** Several Amberdata claims (exact pricing, free tier/no-credit-card, full venue & altcoin coverage, REST/WebSocket/CSV/S3/Python breadth) were **refuted or unverified** in adversarial checking. Treat capabilities as documented-but-self-asserted; do **not** assume a free tier. See [[08 — Pitfalls and Misconceptions (what NOT to do)]].

---

## 1. What makes it different
Free tools compute **naive** GEX (`OI × Γ × assumed-sign`). Amberdata claims to infer the **actual aggressor** of each option trade by matching quote updates to trades (the **"AMBERDATA DIRECTION"** algorithm, 30+ heuristics), producing **true dealer inventory**:
- `dealerNetInventory`, `dealerTotalInventory` fields on Deribit BTC GEX snapshots.
- This is the closest hosted product to *real* dealer positioning (vs the assumed sign everyone else uses).

## 2. Capabilities (verified vs claimed)
| Capability | Status |
|------------|--------|
| Dealer-positioning GEX via aggressor matching (Deribit BTC) | ✅ Documented (2-3 votes) |
| Full greeks + portfolio greeks (delta/gamma/vega) | ✅ Confirmed |
| Gamma profiles, term-structure richness, vol footprints | ✅ Listed first-party |
| Strike/delta/moneyness **vol surfaces** | ✅ Listed |
| REST API + customizable analytics UI | ✅ (REST confirmed; WS/CSV/S3/Python **unverified**) |
| BTC/ETH/SOL + ~90% altcoins, multi-venue (bit.com/Delta/Thalex/LedgerX) | ❌ **Refuted** |
| Free tier / no-credit-card signup | ❌ **Refuted/unverified** |
| Published fixed pricing | ❌ **Unverified** (quote-based, enterprise) |

## 3. Lineage
GVol / **Genesis Volatility** was acquired by **Amberdata in Oct 2022** (confirmed by CoinDesk/Benzinga/StreetInsider + Amberdata blog). Old "GVol" references = today's AD Derivatives.

## 4. How you'd use it
- For **institutions / serious quants** who need true dealer GEX, full vol surfaces, and historical depth via API for systematic strategies.
- Retail: generally **not worth it** — cost is opaque/high and the free tools cover 90% of practical GEX needs.

## 5. What NOT to do
- Don't cite its accuracy as fact — the aggressor precision is **self-asserted, not independently benchmarked**.
- Don't assume you can sign up free. Budget for an enterprise quote.

## 6. Verdict
**Rank #4.** Best-in-class *if* you can pay and need *true* dealer positioning; otherwise informational. → [[04 — Dashboards Directory + RANKING]]
