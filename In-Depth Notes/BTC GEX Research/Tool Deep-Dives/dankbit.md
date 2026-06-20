---
title: Deep-Dive — fshahy/dankbit
tags: [gex, deep-dive, github, python, deribit, dealer-gamma, opensource]
created: 2026-06-20
source-quality: primary (source read from raw GitHub 2026-06-20)
repo: https://github.com/fshahy/dankbit
---

# 🔬 Deep-Dive: fshahy/dankbit

**Repo:** https://github.com/fshahy/dankbit (Python, BTC/ETH)
**One line:** Structural options analytics for Deribit that computes **trade-direction-weighted** dealer gamma (closest OSS tool to *true* dealer positioning), with pin risk and hedging pressure.

---

## 1. Architecture (it's an Odoo app)
```
dankbit_ws_service/dankbit_ws_batch.py   ← Deribit WebSocket batch collector
        │ (writes trades to DB)
        ▼
my_addons/dankbit/  (Odoo module)
   models/trade.py                ← Trade model (strike, iv, amount, direction, expiry)
   controllers/gamma.py           ← Dollar-gamma + portfolio GEX math
   controllers/delta.py           ← DEX (delta exposure)
   controllers/options.py         ← chain endpoints
   controllers/main.py            ← routes
   wizard/plot_wizard.py          ← charting
   data/ir_cron.xml               ← scheduled refresh (cron)
docker-compose.yml + Dockerfile   ← run Odoo + WS service
```
Runs as a containerized Odoo web app (cron-refreshed), not a script.

## 2. The math — what's genuinely different
Unlike the naive OI model, dankbit computes **Black-Scholes dollar gamma** and signs each position by **actual trade direction** (buy vs sell), summing a portfolio:

```python
# controllers/gamma.py  — Black–Scholes Dollar Gamma  Γ·S²
def bs_gamma(S, K, T, r, sigma, min_time_hours=1.0):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    return gamma * S**2          # dollar gamma = Γ·S² (Δ change per $1 move, dollarized)

def _infer_sign(trd):            # ← the key step
    return  1.0 if trd.direction=="buy" else -1.0 if trd.direction=="sell" else 0.0

def portfolio_gamma(S, trades, r=0.0):
    total = 0.0
    for trd in trades:
        T     = trd.get_hours_to_expiry()/(24*365)
        sigma = trd.iv/100.0
        sign  = _infer_sign(trd)     # trade-direction, NOT just put/call
        total += sign * trd.amount * bs_gamma(S, trd.strike, T, r, sigma)
    return total
```
- **Dollar gamma** convention `Γ·S²` (delta-change per $1 move, dollarized) — see [[02 — The Math — Greeks to Dollar GEX (with code)]].
- **Sign from `direction` (buy/sell)** → infers who's long/short, i.e. dealer-positioning logic rather than the blunt +call/−put assumption.
- Numerical guards: floors time (`min_time_hours`) and `sigma` to avoid divide-by-zero near expiry.
- `S` can be a NumPy array → computes a **gamma profile across a spot grid** (for the GEX-vs-price curve & zero-gamma).

## 3. What it outputs
Dealer **gamma positioning**, **pin risk**, and **hedging pressure** per BTC/ETH expiry; DEX via `delta.py`; charts via the plot wizard.

## 4. How to use it
- `docker-compose up` → run the WS collector + Odoo UI; browse gamma/delta dashboards.
- Best OSS choice if you want **trade-aware** GEX (not OI-naive) without paying Amberdata.

## 5. What NOT to do / limits
- Trade-direction sign is still an **inference** (buy/sell of the printed trade), not exchange-tagged dealer flow — better than naive, not perfect.
- Heavier to run (Odoo + Docker + DB) than a single script.
- Only 2★; small project — read the code before trusting numbers.

## 6. Verdict
**Rank #6** — the OSS bridge toward *real* dealer gamma. Study `gamma.py` alongside the naive [[Tool Deep-Dives/Nathan-Hall Bitcoin-Options-GEX]] to see why sign convention is everything. → [[06 — Build Your Own GEX Engine (architecture)]]
