---
title: What Gamma Exposure (GEX) Is
tags: [gex, concept, gamma, dealers, hedging, btc]
created: 2026-06-20
status: verified-claims
---

# 📖 What Gamma Exposure (GEX) Is

> The single concept the whole vault rests on. Read this first. Every cited line below
> survived 3-vote adversarial verification (sources at the bottom).

---

## 1. The one-sentence definition
**GEX = the open-interest-weighted total gamma across every listed option** — it quantifies **how much aggregate market delta changes per $1 (or 1%) move in BTC**, i.e. *how much options dealers are forced to hedge as price moves.* (CryptoGamma, verified 3-0)

## 2. Why dealers must hedge (the mechanism)
- Options market-makers (dealers) stay **delta-neutral**. When BTC moves, their delta changes — by an amount governed by **gamma**.
- To re-neutralize, they **buy or sell the underlying** (spot/perp/futures). That hedging is *mechanical, predictable flow* — and GEX maps where it concentrates.
- GEX is therefore **"a measure of where options market-makers are forced to hedge."** (GammaFlip, verified 3-0)

## 3. The two regimes — the heart of it
| | **Positive / Long Gamma** | **Negative / Short Gamma** |
|---|---|---|
| Dealer position | Long gamma | Short gamma |
| Hedge on a **dip** | **Buy** (absorb) | **Sell** (accelerate) |
| Hedge on a **rip** | **Sell** (absorb) | **Buy** (accelerate) |
| Effect on price | **Dampens / pins** | **Amplifies / trends** |
| Volatility | Compresses | Expands |
| You should | Fade extremes, mean-revert | Trade momentum, respect breakouts |

> Verified phrasings:
> - "**Positive GEX**: dealers are long gamma and dampen volatility by buying dips and selling rips … **Negative GEX**: dealers are short gamma and amplify moves as they hedge." (CryptoGamma, 3-0)
> - "Positive GEX zones: dealers … typically buy on dips and sell on rallies, which dampens volatility. Negative GEX zones: dealers sell as prices fall and buy as prices rise." (Glassnode, 3-0)
> - Amberdata frames it as positive gamma = stabilizing "buy low, sell high"; negative gamma = destabilizing "sell low, buy high." (3-0)

## 4. The structural levels GEX gives you
- **Gamma Flip / Zero-Gamma:** the price where **net GEX crosses zero** — *"the boundary between low-volatility and high-volatility regimes."* (GammaFlip, 3-0). **The most important single level.**
- **Gamma Wall:** the strike with the largest gamma concentration → acts as a **magnet/barrier** (pin in long-gamma, hard level in short-gamma).
- **Call Wall / Put Wall:** largest call-side / put-side exposure → soft **resistance / support**.

(Math + how each is computed: [[02 — The Math — Greeks to Dollar GEX (with code)]]. Reading them live: [[03 — How to Read a GEX Chart (interpretation)]].)

## 5. Crypto vs equities — a crucial nuance
- The classic equity GEX **assumes dealers are long calls / short puts** (SpotGamma, gex-tracker — verified). This is a *convention*, not a measurement.
- In crypto there's no OCC-style customer/dealer tagging — BUT **Deribit exposes the taker on each trade**, so the *better* crypto method infers **dealer = mirror of the taker** (Glassnode, 3-0). Most free dashboards still use the naive equity assumption.
- → This sign question is the #1 reason two BTC GEX dashboards disagree. See [[08 — Pitfalls and Misconceptions (what NOT to do)]].

## 6. What GEX is **not**
- ❌ Not a directional signal (it's about *environment + levels*, not "up or down").
- ❌ Not a guarantee (walls break; models assume sign).
- ❌ Not real-time-perfect (OI is delayed; dashboards refresh on 1–15 min cadences).

---

### Sources (all verified 3-0 unless noted)
- CryptoGamma — https://cryptogamma.io/ (definition, regimes, Deribit source)
- GammaFlip.io — https://gammaflip.io/ (gamma flip, hedging framing)
- Glassnode — https://research.glassnode.com/gamma-exposure/ (taker-flow method, regimes)
- Amberdata — https://docs.amberdata.io/http/analytics/derivatives/gamma-snapshots-gex (MM hedging definition)
- SpotGamma — https://spotgamma.com/gamma-exposure-gex/ (canonical equity formula)
