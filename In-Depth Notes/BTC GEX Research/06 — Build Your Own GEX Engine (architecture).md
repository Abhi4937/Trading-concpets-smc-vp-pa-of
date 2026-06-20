---
title: Build Your Own GEX Engine — Architecture
tags: [gex, architecture, engineering, deribit, python]
created: 2026-06-20
status: grounded-in-source
---

# 🏗️ Build Your Own BTC GEX Engine — Architecture

> Modeled on the cleanest open-source pattern ([[Tool Deep-Dives/zrack gex-terminal]]),
> combined with the BTC-native data flow of [[Tool Deep-Dives/Nathan-Hall Bitcoin-Options-GEX]]
> and the trade-aware sign logic of [[Tool Deep-Dives/dankbit]]. Goal: a system you fully
> understand, so you trust what you trade.

---

## 1. The layered design (copy this separation)
```
┌─────────────────────────────────────────────────────────┐
│  UI / OUTPUT      chart · TUI · JSON API · alerts         │
├─────────────────────────────────────────────────────────┤
│  STATE            StatefulConsumer: thread-safe aggregate │
│                   per-strike call/put gamma + walls       │
├─────────────────────────────────────────────────────────┤
│  ENGINE (pure)    BS gamma → dollar GEX → walls/zero-γ    │  ← no I/O, fully testable
├─────────────────────────────────────────────────────────┤
│  ADAPTERS         DeribitAdapter (WS) · replay · others   │  ← normalize to 2 message types
├─────────────────────────────────────────────────────────┤
│  DATA SOURCE      Deribit WS/REST (BTC options chain)     │
└─────────────────────────────────────────────────────────┘
```
**Rule:** the engine never touches the network; adapters never do math. Swap Deribit for OKX/Bybit by writing one adapter — engine/UI unchanged.

## 2. Ingestion layer (Deribit adapter)
Two ways to get the BTC chain (see [[05 — APIs and Data Sources (Deribit etc.)]]):
- **One-shot bulk:** `public/get_book_summary_by_currency` (`currency=BTC, kind=option`) → every instrument's `open_interest`, `mark_iv`, `underlying_price` in one call. Best for a 1–10 min poller.
- **Live stream:** Deribit **WebSocket** subscriptions (book/ticker) → real-time ticks. Best for intraday.
- **Library shortcut:** **CCXT** Deribit connector exposes `fetchGreeks`, `fetchOption`, `fetchOptionChain`, `fetchOpenInterest` — skip hand-rolling JSON-RPC.

Normalize everything to two message shapes (zrack's contract):
```json
{"type":"underlying_tick","symbol":"BTC","price":63311.05}
{"type":"options_volume_tick","strike":65000,"option_type":"C","volume":100,"iv":0.72}
```
(For an OI-weighted model, carry `open_interest` instead of/alongside `volume`.)

## 3. The engine (pure math) — minimal but complete
```python
import numpy as np
class GexEngine:
    def __init__(self, multiplier=1.0):      # BTC index options: 1.0
        self.m = multiplier
    def gamma(self, S, K, t, r, sig):
        t = np.where(t==0, 1e-5, t)
        d1 = (np.log(S/K) + (r+0.5*sig**2)*t)/(sig*np.sqrt(t))
        return (1/np.sqrt(2*np.pi))*np.exp(-0.5*d1**2)/(S*sig*np.sqrt(t))
    def matrix(self, S, K, dte, r, iv, call_w, put_w):
        t = np.full_like(K, dte/365.0, float)
        g = self.gamma(S, K, t, r, iv)
        scale = g * S * (S*0.01) * self.m          # $GEX per 1% move
        call_gex =  call_w * scale
        put_gex  =  put_w  * scale * -1.0          # naive sign; swap for trade-aware
        net = call_gex + put_gex
        wall = K[np.argmax(np.abs(net))]
        zero = self._zero_gamma(K, net)
        return dict(strikes=K.tolist(), net=net.tolist(), total=float(net.sum()),
                    gamma_wall=float(wall), call_wall=float(K[np.argmax(call_gex)]),
                    put_wall=float(K[np.argmax(np.abs(put_gex))]), zero_gamma=zero)
    @staticmethod
    def _zero_gamma(K, net):
        s=np.sign(net); c=np.where(s[:-1]*s[1:]<0)[0]
        if len(c):
            i=c[0]; return float(K[i]-net[i]*(K[i+1]-K[i])/(net[i+1]-net[i]))
        return float(K[np.argmin(np.abs(net))])
```
Weights = OI (Bitcoin-Options-GEX), volume (zrack), or trade-signed amount (dankbit). **Choose deliberately** — it changes the sign → [[02 — The Math — Greeks to Dollar GEX (with code)]].

## 4. State layer (the consumer)
- Maintain a dict `{strike: {call_g, put_g}}` updated on each tick (guard with a lock / async queue — zrack's `StatefulGexConsumer`).
- Recompute walls/zero-gamma on a timer (e.g. every 5 s) not every tick (cheap + stable).

## 5. Output layer
- **JSON API** (mirror CryptoGamma's `/api/public/snapshot`) for your own tools.
- **Alerts:** fire when `price` within X of `gamma_wall`/`zero_gamma`, or when `total` flips sign (regime change).
- **Chart:** bar(net by strike) + vertical lines at walls/zero-gamma.

## 6. Testing & honesty (don't skip)
- **Replay fixtures:** record normalized JSONL, replay deterministically (zrack ships `sample_data/*.jsonl`). Lets you test math with no live key.
- **Regression tests** on the engine (zrack's `tests/test_gex_engine.py` pattern).
- **Document assumptions** like zrack's `model-assumptions.md`: which sign convention, OI vs volume, what you *don't* model. → [[08 — Pitfalls and Misconceptions (what NOT to do)]].

## 7. Upgrade path to "real" dealer GEX
Naive (call+/put−) → trade-aware (sign by aggressor/direction, like dankbit) → **taker-flow reconstruction** (Glassnode's method: dealer = mirror of the taker on each Deribit trade). The last is the most defensible for crypto. → [[Tool Deep-Dives/Glassnode Gamma Exposure]].
