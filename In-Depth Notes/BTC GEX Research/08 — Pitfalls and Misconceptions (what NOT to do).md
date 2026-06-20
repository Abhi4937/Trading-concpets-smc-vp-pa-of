---
title: Pitfalls & Misconceptions — what NOT to do
tags: [gex, pitfalls, misconceptions, risk, what-not-to-do]
created: 2026-06-20
status: critical-read
---

# ⚠️ Pitfalls & Misconceptions — what NOT to do with BTC GEX

> The traps that blow up GEX-based trades. Read this before sizing anything on GEX.
> Many of these come straight from the tools' own honesty docs (e.g. zrack's
> `model-assumptions.md`) and from claims that **failed** verification in this research.

---

## 1. The sign-convention trap (the big one)
- ❌ **Don't treat naive GEX as truth.** CryptoGamma, GammaFlip, gex-tracker, zrack all **assume dealers are long calls / short puts**. That's an *equity convention*, not a crypto measurement.
- ✅ In crypto, the defensible method infers **dealer = mirror of the taker** on each Deribit trade (Glassnode) or signs by trade direction (dankbit) / aggressor matching (Amberdata).
- **Consequence:** two dashboards can show **opposite** net GEX for the same chain. When they disagree, weight the **taker-flow / trade-aware** source. → [[Tool Deep-Dives/Glassnode Gamma Exposure]]

## 2. Volume-as-OI proxy distortions
Tools using **intraday volume** as a positioning proxy (zrack) inherit documented errors (its own `model-assumptions.md`):
- Volume can't tell **opening vs closing** trades.
- **Double-counts churn** at a strike.
- Can't separate **customer vs dealer**.
- **Overstates** exposure in high-turnover sessions; **understates** quiet high-OI strikes.
> ❌ Don't read a volume-proxy "wall" as a confirmed OI wall.

## 3. Walls are not guarantees
- ❌ Gamma walls / zero-gamma are **modeled estimates**, not hard S/R. zrack's docs: read them "as a structural estimate rather than an exact market boundary."
- ✅ Use them as **zones + context**, confirmed by price action — never as blind limit orders.

## 4. Staleness & cadence mismatch
- CryptoGamma ~**15 min**, Glassnode **10 min**, GEX Terminal/Laevitas ~**5 min**, GammaFlip ~**60 s**.
- ❌ Don't scalp a 1-minute chart off a 15-minute snapshot. Match tool cadence to your timeframe.
- OI itself is **delayed** — levels lag fast moves exactly when you need them most.

## 5. Single-venue blindness
- Most tools are **Deribit-only**. Deribit is ~85–90% of crypto options OI, but **CME, OKX, Bybit, and US spot-BTC ETF (IBIT) options** add real hedging pressure GEX dashboards miss.
- ✅ Prefer aggregated (GammaFlip = Deribit+Bybit+OKX) or add IBIT context (GEX Terminal via Tradier).

## 6. Don't trust vendor marketing as fact
Claims that **failed adversarial verification** in this very research (do not repeat them as truth):
- Amberdata: a **free tier / no-credit-card signup**, its **fixed pricing**, and **~90% altcoin / multi-venue (bit.com/Delta/Thalex/LedgerX)** coverage → **refuted/unverified**.
- Amberdata REST/**WebSocket/CSV/S3/Python** breadth → **unverified**.
- **Block Scholes** greeks/IV-surface, WS+REST API, and free Telegram tier → **did not survive verification** (treat as unconfirmed).
> ✅ Capability ("what it does") from a vendor site is usually fine; **accuracy, pricing, and free-tier** claims need independent proof.

## 7. Conceptual misreads
- ❌ "Negative GEX means go short." No — negative GEX means **moves amplify in *both* directions**. It's about *vol*, not direction.
- ❌ "Positive GEX means buy." No — it means **mean-reversion/pinning**; you fade extremes, you don't chase.
- ❌ "The gamma wall is where price *must* stop." No — it's where hedging *resists*; in **short gamma** the same level gets run through.
- ❌ Treating GEX as standalone. It's **context for price/flow**, not a system by itself.

## 8. Expiry mechanics you must respect
- Deribit options expire **08:00 UTC**; front-week gamma dominates pin behavior into expiry.
- ❌ Don't hold a mean-reversion "pin" thesis **through** expiry — after expiry that gamma vanishes and the regime can snap. Re-read GEX post-expiry.

## 9. Open-source caveats
- Bitcoin-Options-GEX = a **2021 learning project** (author's words) — great to learn, not to productionize.
- dankbit/zrack/GammaGEX = **low-star, young** — read the code before trusting numbers.
- zrack is **ES/NQ**, not BTC — needs a Deribit adapter first. → [[Tool Deep-Dives/zrack gex-terminal]]

## 10. The honest summary
> GEX tells you the **weather** (calm-and-pinning vs stormy-and-trending) and the **landmarks**
> (walls, flip). It does **not** tell you the **direction** to drive. Use it to choose your
> *style* (fade vs follow) and your *levels* — then let price and flow pick the trade.

→ Put it together correctly: [[07 — Trader Usage Playbook (how to use together)]]
