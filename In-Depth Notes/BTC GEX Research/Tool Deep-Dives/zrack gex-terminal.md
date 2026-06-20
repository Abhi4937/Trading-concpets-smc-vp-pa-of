---
title: Deep-Dive — zrack/gex-terminal
tags: [gex, deep-dive, github, python, opensource, architecture]
created: 2026-06-20
source-quality: primary (source read from raw GitHub 2026-06-20)
repo: https://github.com/zrack/gex-terminal
---

# 🔬 Deep-Dive: zrack/gex-terminal

**Repo:** https://github.com/zrack/gex-terminal (Python, MIT, created 2026-05-30, 0★)
**One line:** A clean, well-architected intraday GEX terminal UI — **built for ES/NQ equity-index futures, not BTC** — but the single best *architecture* template to copy for a BTC engine.

> ⚠️ **BTC relevance is indirect.** It ships adapters for Tradovate/Databento/IBKR/yfinance/replay (equity/futures), **not** Deribit. Its value here is the **engineering pattern**, which ports to BTC by writing one Deribit adapter. (This is the open-source repo; the unrelated commercial `gexterminal.net` is [[Tool Deep-Dives/GEX Terminal Pro]].)

---

## 1. Project layout (the pattern to copy)
```
gex_terminal/
  engine.py              ← vectorized Black-Scholes + GEX matrix (pure math, no I/O)
  consumer.py            ← StatefulGexConsumer: async, thread-safe state aggregator
  market_data_adapter.py ← MarketDataAdapter ABC (the contract)
  adapters/              ← replay, tradovate, databento, ibkr, yfinance
  tui.py / *.tcss        ← Textual reactive terminal UI
  cli.py / config.py     ← orchestration + env-driven config
  snapshot.py            ← export
sample_data/*.jsonl      ← normalized replay fixtures (test without live data)
tests/                   ← math regression tests
docs/model-assumptions.md← honest limitations doc
```
**Why it's the reference:** clean separation — **math (engine) ⟂ ingestion (adapters) ⟂ state (consumer) ⟂ UI (tui)**. Swap data sources without touching math.

## 2. The engine — exact functions & math (`engine.py`)
`class IntradayGexEngine(multiplier)`:
- `calculate_d1(S,K,t,r,σ)` and `calculate_gamma(...)` → vectorized BS gamma over the whole strike array (NumPy, no per-contract loop):
  $$ \Gamma = \frac{N'(d_1)}{S\,\sigma\sqrt t},\quad N'(d_1)=\tfrac{1}{\sqrt{2\pi}}e^{-d_1^2/2} $$
- `compute_intraday_gex_matrix(...)` → the core. **Scales gamma to dollar GEX per 1% move:**
  ```python
  gex_scaling_factor = gamma * S * (S*0.01) * multiplier
  call_gex =  call_vol * gex_scaling_factor
  put_gex  =  put_vol  * gex_scaling_factor * -1.0
  net_gex  =  call_gex + put_gex
  ```
- Structural outputs: `gamma_wall_strike` (max |net|), `call_wall`, `put_wall`, `zero_gamma_strike` (**linear interpolation** of the net-GEX sign change — `interpolate_zero_gamma_strike`), and a **concentration band** (smallest strike range holding ≥70% of |net| gamma).

## 3. The defining assumption — volume as OI proxy
From `docs/model-assumptions.md` (paraphrased honestly):
- Official OI is delayed → it uses **cumulative intraday session volume** as the live positioning input.
- **Documented limitations:** volume can't tell open vs close, double-counts churn, can't separate customer vs dealer, overstates exposure in high-turnover sessions.
- Sign convention: call+ / put− (naive, same caveat as the others).
- Zero-gamma is a **structural estimate**, not an exact boundary.
> This honesty (it documents what it *can't* do) is the model to imitate — see [[08 — Pitfalls and Misconceptions (what NOT to do)]].

## 4. The adapter contract (how to make it BTC)
```python
class MarketDataAdapter(ABC):
    async def stream_market_data(self) -> None: ...
# emits normalized messages:
{"type":"underlying_tick","symbol":"ES","price":5943.25}
{"type":"options_volume_tick","strike":5950,"option_type":"C","volume":100,"iv":0.15}
```
→ **To use for BTC:** write a `DeribitAdapter` that subscribes to Deribit WS and emits these two message shapes. The engine/UI need no changes. (multiplier=1 for BTC index options.)

## 5. What NOT to do / limits
- **Don't run it expecting BTC out of the box** — no Deribit adapter ships.
- Same naive-sign + volume-proxy caveats as the others.
- New, unproven, 0★ — treat as a template, not a product.

## 6. Verdict
**Rank #7 for trading**, but **#1 as an architecture blueprint.** Copy its layering for [[06 — Build Your Own GEX Engine (architecture)]].
