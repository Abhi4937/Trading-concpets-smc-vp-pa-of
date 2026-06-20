---
title: The Math — Greeks → Dollar GEX (with code)
tags: [gex, math, black-scholes, gamma, deribit]
created: 2026-06-20
status: grounded-in-source
---

# 🧮 The Math: From Greeks to Dollar GEX

> Every GEX tool — CryptoGamma, Laevitas, the three GitHub repos — is some variation
> of the same pipeline. Learn it once and you can read (or build) any of them.
> Source-grounded in the actual code of [[Tool Deep-Dives/Nathan-Hall Bitcoin-Options-GEX]],
> [[Tool Deep-Dives/dankbit]], and [[Tool Deep-Dives/zrack gex-terminal]].

---

## 1. Gamma (Γ) — the starting Greek
Gamma = the **rate of change of delta** per $1 move in spot. Black-Scholes:

$$ \Gamma = \frac{N'(d_1)}{S\,\sigma\sqrt{t}}, \qquad N'(d_1)=\frac{1}{\sqrt{2\pi}}e^{-d_1^2/2} $$
$$ d_1 = \frac{\ln(S/K) + (r + \tfrac12\sigma^2)\,t}{\sigma\sqrt{t}} $$

where **S**=spot, **K**=strike, **t**=time-to-expiry (years), **σ**=implied vol, **r**=risk-free rate.

```python
import numpy as np
def bs_gamma(S, K, t, r, sigma):
    t = np.where(t == 0, 1e-5, t)              # floor to avoid /0 at expiry
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*t) / (sigma*np.sqrt(t))
    n_prime = (1/np.sqrt(2*np.pi)) * np.exp(-0.5*d1**2)
    return n_prime / (S * sigma * np.sqrt(t))
```
> You can also just **read Γ from Deribit's `greeks.gamma`** instead of computing it (that's what Bitcoin-Options-GEX does). Computing it yourself lets you build a **gamma profile across a spot grid** (needed for the zero-gamma curve).

> [!example] Worked numbers — compute Γ for one BTC option
> Inputs: S=$63,300, K=$64,000, t=7 days = 0.0192 yr, σ=72% (0.72), r=0.
> - `d1 = [ln(63300/64000) + (0 + 0.5·0.72²)·0.0192] / (0.72·√0.0192)`
> - `   = [ln(0.98906) + 0.004977] / (0.72·0.1386)` = `[−0.01100 + 0.004977] / 0.09980` = **−0.0604**
> - `N'(d1) = (1/√2π)·e^(−0.0604²/2)` = `0.39894 · 0.99818` = **0.39822**
> - `Γ = 0.39822 / (63300 · 0.72 · 0.1386)` = `0.39822 / 6317.6` = **6.30 × 10⁻⁵** per $1
> Reading: this option's delta changes ~**0.0000630 per $1**, i.e. ~**0.063 delta per $1,000** BTC move. Gamma is largest **at-the-money** and shrinks as you go far ITM/OTM — that's why the gamma wall clusters near heavily-traded near-the-money strikes.

## 2. From Γ to **dollar gamma** (two conventions — don't mix them)
| Convention | Formula | Used by | Meaning |
|------------|---------|---------|---------|
| **Γ·S²** ("dollar gamma") | `gamma * S**2` | dankbit | $ change in delta per **$1** move |
| **Per 1% move** | `gamma * S * (S*0.01) * multiplier` | zrack | $ change in delta per **1%** move |
Both dollarize gamma; the per-1%-move version is what dashboards usually plot ("USD GEX per 1% Move" on Laevitas).

## 3. Weighting & **sign** — where tools diverge (this is the whole ballgame)
GEX at a strike = (dollar gamma) × (size) × (**sign of dealer position**). The three real implementations:

| Tool | Size weight | Sign rule | Honesty |
|------|-------------|-----------|---------|
| **Bitcoin-Options-GEX** | **Open Interest** | +1 call / −1 put (naive) | assumes dealers short all calls? No — assumes call=+, put=− |
| **zrack** | **intraday volume** (OI proxy) | +1 call / −1 put (naive) | documents the proxy is imperfect |
| **dankbit** | trade **amount** | **+1 buy / −1 put-or-sell direction** (trade-aware) | infers actual long/short |
| **Amberdata** (hosted) | true positions | **measured aggressor** (quote→trade match) | closest to real, but paid & self-asserted |

```python
# Naive (Bitcoin-Options-GEX), GEX per $100 move, in BTC:
gex = OI * gamma * put_call_sign * 100          # +1 call, -1 put
net_per_strike = groupby(strike).sum(gex)

# Trade-aware (dankbit):  Σ sign(buy/sell) * amount * (Γ·S²)
net = sum(sign(trd.direction) * trd.amount * bs_gamma(S, trd.K, T, r, trd.iv) for trd in trades)

# Volume-proxy per 1% move (zrack):
scale   = gamma * S * (S*0.01) * multiplier
call_gex = call_vol * scale
put_gex  = put_vol  * scale * -1.0
net_gex  = call_gex + put_gex
```

> **Key insight:** the *same* gamma can produce opposite GEX depending on the **sign assumption**. Naive (call+/put−) is a convention, not a measurement. This is the #1 reason two dashboards disagree. → [[08 — Pitfalls and Misconceptions (what NOT to do)]]

### 3a. The canonical equity formula (for reference)
The industry-standard equity formula (SpotGamma, verified 3-0) — the per-1%-move convention, dollarized:
$$ \text{GEX}_{\text{strike}} = \Gamma \times OI \times \text{ContractSize} \times S^2 \times 0.01 $$
$$ \text{Net GEX} = \sum \text{Call GEX} - \sum \text{Put GEX}\ \text{(all strikes \& expiries)} $$
`Matteo-Ferrara/gex-tracker` implements exactly this (Call: `+S·Γ·OI·size·S·0.01`; Put: negated). Note `S²·0.01` = `S·(S·0.01)` = the same "per 1% move" scaling zrack uses. **This is the naive model** — calls +, puts −.

### 3b. The four methodology tiers (cheapest → most correct)
| Tier | Sign source | Tools | Trustworthiness |
|------|-------------|-------|-----------------|
| Naive | assume call+/put− | CryptoGamma, GammaFlip, gex-tracker, zrack, Bitcoin-Options-GEX | convention, not measured |
| Trade-aware | buy/sell direction of prints | dankbit | better |
| **Taker-flow** | dealer = **mirror of the taker** on each Deribit trade | **Glassnode** | best public method for crypto |
| Aggressor-matched | quote→trade aggressor inference | Amberdata | best (paid, self-asserted) |
> Crypto's advantage over equities: **Deribit exposes the taker per trade**, so taker-flow (Glassnode) beats the borrowed equity assumption. → [[Tool Deep-Dives/Glassnode Gamma Exposure]]

### 3c. Full worked example — a 5-strike BTC mini-chain (naive model)
Take a toy chain at spot **S = $63,300**, contract size 1, using `GEX = Γ · OI · S² · 0.01` (per-1%-move, calls +, puts −). Γ peaks ATM:

| Strike | side | OI | Γ (×10⁻⁵) | dollar-gamma `Γ·S²·0.01` | sign | **strike GEX ($)** |
|--------|------|----|-----------|--------------------------|------|--------------------|
| 61,000 | put  | 900 | 4.1 | 1,643 | − | **−1,478,700** |
| 62,000 | put  | 600 | 5.6 | 2,244 | − | **−1,346,400** |
| 63,000 | call | 500 | 6.4 | 2,564 | + | **+1,282,000** |
| 64,000 | call | 800 | 6.3 | 2,524 | + | **+2,019,200** |
| 66,000 | call | 1,100 | 3.9 | 1,562 | + | **+1,718,200** |

- **Net GEX** = −1,478,700 − 1,346,400 + 1,282,000 + 2,019,200 + 1,718,200 = **+2,194,300** → net **positive/long-gamma** book → pinning bias.
- **Gamma wall** = max |strike GEX| = **$64,000** (+2.02M) → the dominant magnet.
- **Call wall** = max positive = **$64,000**; **Put wall** = max negative = **$61,000**.
- **Zero-gamma** = where the running sum crosses 0. Cumulative from the bottom: −1.48M, −2.83M, −1.54M, **+0.47M** (crosses between $63,000 and $64,000). Linear-interpolate: `63000 + 1.54M/(1.54M+0.47M)·1000 ≈ ` **$63,766**.
> Read-out: with spot $63,300 **below** zero-gamma $63,766, *this slice* is locally short-gamma (trend-prone) even though the **whole book** is net positive — which is exactly why you watch **both** the total sign (regime) **and** where spot sits vs zero-gamma (local behavior). Flip every put sign to "+" (a wrong sign convention) and net GEX would read **+8.0M** — a totally different regime. **That's the sign-convention trap, quantified.**

## 4. The structural levels (what you actually trade off)
From the per-strike net-GEX array (logic verbatim from zrack `engine.py`):

| Level | Definition | Code |
|-------|------------|------|
| **Gamma Wall** | strike with **max \|net GEX\|** | `strikes[argmax(abs(net))]` |
| **Call Wall** | strike with most **positive** call GEX | `strikes[argmax(call_gex)]` |
| **Put Wall** | strike with most **negative** put GEX | `strikes[argmax(abs(put_gex))]` |
| **Zero-Gamma / Vol-Flip** | where net GEX crosses 0 | linear-interpolate the sign change |
| **Concentration band** | smallest strike range holding ≥70% of \|net\| | sort \|net\| desc, accumulate to 70% |
| **Total net GEX** | `sum(net_gex)` | regime sign (±) for the whole book |

```python
def interpolate_zero_gamma(strikes, net):
    s = np.sign(net)
    cross = np.where(s[:-1]*s[1:] < 0)[0]      # sign-change indices
    if len(cross):
        i = cross[0]; x0,x1 = strikes[i],strikes[i+1]; y0,y1 = net[i],net[i+1]
        return x0 - y0*(x1-x0)/(y1-y0)         # linear interpolation
    return strikes[np.argmin(np.abs(net))]      # fallback: smallest |net|
```

## 5. Total net GEX sign → the regime
- **Total net GEX > 0 (long gamma):** dealers buy dips / sell rips → **mean-reversion, vol compression, pinning**.
- **Total net GEX < 0 (short gamma):** dealers sell dips / buy rips → **momentum, vol expansion, squeezes**.
- **Zero-gamma** = the price boundary between those two worlds. Above it usually long-gamma, below it short-gamma (or vice-versa depending on book).

→ How to read all of this on a live screen: [[03 — How to Read a GEX Chart (interpretation)]]
→ Build the full engine: [[06 — Build Your Own GEX Engine (architecture)]]
