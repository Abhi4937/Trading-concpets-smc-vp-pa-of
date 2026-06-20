---
title: How to Read a GEX Chart — Interpretation & Scenarios
tags: [gex, interpretation, how-to-read, scenarios, dashboards]
created: 2026-06-20
status: usage-guide
---

# 👁️ How to Read a GEX Chart — every number, where it is, what it means when it moves

> Practical reading guide for the live dashboards. For each field: **where** it sits,
> **what it means**, and **what a change in it means**. Ends with a full scenario matrix.

---

## 1. The reading order (do this every time)
1. **Total net GEX sign** → which regime am I in? (+ = pin, − = trend)
2. **Gamma flip / zero-gamma level** → am I above or below it? (regime boundary)
3. **Nearest wall(s)** → where's the magnet/barrier relative to price?
4. **Pin risk / squeeze risk / DVOL** → how fragile is this?
5. **Flow / bias** → which way is fresh pressure leaning?

## 2. Field-by-field (what each number means + what its *change* means)

### On CryptoGamma (https://cryptogamma.io/dashboard/)
| Field | Where | Means | When it **rises** | When it **falls / flips** |
|-------|-------|-------|-------------------|---------------------------|
| **Net Gamma** | top metric | net dealer gamma | more positive → stronger pinning | crosses **negative → regime flips to trend/squeeze** |
| **Call / Put Gamma** | beside net | side split | call-heavy → upside pin/cap | put-heavy → downside support/air-pocket |
| **Bias (% call wtd)** | label | positioning skew | toward calls | toward puts |
| **Squeeze Support/Resistance** | levels | defended prices | — | break = momentum |
| **Squeeze Breakout** | level | acceleration trigger | further away = roomy | price nears it = imminent expansion |
| **Pin Risk** | risk metric | pin-to-strike odds | ↑ into expiry → range/mean-revert | ↓ → freer to trend |
| **Squeeze Risk** | risk metric | breakout odds | ↑ → fragile, prep for vol | ↓ → calm |
| **IV vs RV (premium)** | vol box | option richness | premium ↑ → vol sellers paid | premium ↓/neg → vol buyers favored |

### On a strike chart (Laevitas / GEX Terminal / your own)
| Element | Where | Means |
|---------|-------|-------|
| **Green/positive bars** | strikes above-ish | call/positive GEX — pin/resistance |
| **Red/negative bars** | strikes below-ish | put/negative GEX — support/air-pocket |
| **Tallest bar** | one strike | **Gamma Wall** — strongest magnet |
| **Zero-crossing of net line** | between strikes | **Zero-Gamma / flip** — regime boundary |
| **"USD GEX per 1% Move"** | Laevitas 2nd chart | dollar-hedging size per 1% — the *actionable* magnitude |
| **GEX term structure** | Laevitas 3rd chart | which **expiry** drives the gamma (front-week = pin-heavy into expiry) |

### On GammaFlip.io
- **Gamma Flip level** = the headline number. Above it → pin/mean-revert bias; below → momentum/squeeze bias. Multi-exchange, ~60s refresh → trust it for *live regime*.

## 3. What it means when the **data changes** (dynamics)
- **Net GEX flips + → −:** the market just left the "dampened" world. Expect bigger candles, failed mean-reversion, trend/squeeze. *Stop fading.*
- **Price crosses the gamma flip downward:** entering short-gamma → volatility expands; breakouts work, dip-buying-into-support gets run over.
- **Gamma wall migrates to a new strike (OI builds):** the magnet moved — re-mark your levels.
- **Pin risk spikes near expiry:** price likely gets *tractor-beamed* to the wall/max-pain into the Deribit 08:00 UTC expiry. Fade extensions toward the pin.
- **Squeeze risk + negative GEX together:** highest-energy setup — a break of the breakout level can run fast.
- **Call wall capping rallies repeatedly:** dealers selling into it; until OI there clears, it's resistance. A *decisive* break (OI rolls up) flips it to support.

## 4. Scenario matrix (all the common cases)
| # | Regime | Price vs flip | Near which level | Likely behavior | Play |
|---|--------|---------------|------------------|-----------------|------|
| 1 | **+GEX** | above flip | below call wall | grind up, pin, low vol | buy dips toward support, sell into call wall |
| 2 | **+GEX** | above flip | **at gamma wall** | strong pin / chop | fade pokes through the wall, scalp the range |
| 3 | **+GEX** | near flip | straddling zero-γ | unstable calm | reduce size; wait for side to resolve |
| 4 | **−GEX** | below flip | above put wall | trend down, vol up | sell rallies, momentum shorts, wide stops |
| 5 | **−GEX** | below flip | **breaking put wall** | air-pocket / cascade | breakout short, expect acceleration |
| 6 | **−GEX** | below flip | far from walls | whippy two-way | trade momentum only, avoid mean-reversion |
| 7 | any | **crossing flip** | at zero-γ | regime change in progress | flip your playbook (pin↔trend) |
| 8 | +GEX | into **expiry** | high pin risk | magnet to wall/max-pain | fade extensions toward pin |
| 9 | −GEX | into expiry | low pin, high squeeze | expiry-driven breakout | trade the break, then reassess post-expiry |
| 10 | +GEX→−GEX | flip just turned − | — | calm → violent | **the highest-alpha transition; respect it** |

## 5. Confirmation across tools (don't trade one screen)
High-conviction = **agreement**: CryptoGamma bias/levels **+** GammaFlip flip **+** GEX Terminal confluence zone **+** price action all pointing the same way. Disagreement = stand down. → [[07 — Trader Usage Playbook (how to use together)]] · pitfalls in [[08 — Pitfalls and Misconceptions (what NOT to do)]].
