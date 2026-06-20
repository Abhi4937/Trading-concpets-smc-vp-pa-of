---
title: Deep-Dive — Nathan-Hall/Bitcoin-Options-GEX
tags: [gex, deep-dive, github, python, deribit, opensource]
created: 2026-06-20
source-quality: primary (source read from raw GitHub 2026-06-20)
repo: https://github.com/Nathan-Hall/Bitcoin-Options-GEX
---

# 🔬 Deep-Dive: Nathan-Hall/Bitcoin-Options-GEX

**Repo:** https://github.com/Nathan-Hall/Bitcoin-Options-GEX (Python, native BTC)
**One line:** The cleanest minimal example of **naive GEX** computed straight from the live Deribit options chain. Author flags it as a messy 2021 learning project — but the math is exactly the industry-standard naive model.

---

## 1. Files
| File | Purpose |
|------|---------|
| `main.py` | Pull Deribit chain → compute per-strike GEX → plot bar chart + gamma-flip |
| `Options Expected Move DVOL.py` | Expected-move from DVOL |
| `BTC *.png` | Example output charts |

## 2. Data flow & the key functions/methods
All data via **Deribit WebSocket** (`wss://www.deribit.com/ws/api/v2/`), JSON-RPC 2.0:

| Function | Deribit method | Returns |
|----------|---------------|---------|
| `get_currency_price('btc_usd')` | `public/get_index_price` | spot index price |
| `retrieve_options_names('BTC')` | `public/get_instruments` (kind=option, expired=False) | all live option names |
| `retrieve_options_data(name)` | `public/get_order_book` | per-option `greeks.gamma`, `open_interest` |
| `options_data_create(name)` | — | parses `[name, gamma, OI, ±1, strike]`; **type = 1 if call, −1 if put** (last char of instrument) |
| `dataframe_create(names)` | — | **ThreadPoolExecutor(8)** fan-out over all options (concurrent fetch) |
| `bootleg_flip_calc(strikes)` | — | crude **gamma-flip**: cumulative-sum of strike-gamma, picks the sign-change extremum |

## 3. The GEX equation (verbatim logic)
```python
# gamma comes from DERIBIT's own greeks (not computed locally)
options_data_df['gex'] = OI * Gamma * PutCall(±1) * 100   # GEX per $100 move, in BTC
sorted_data_df = options_data_df.groupby('Price')['gex'].sum()   # aggregate per strike
```
- **Weighting = Open Interest** (not volume). **Sign = +call / −put** (naive).
- **Gamma source = Deribit server greeks** → no Black-Scholes coded locally (contrast with [[Tool Deep-Dives/dankbit]] and [[Tool Deep-Dives/zrack gex-terminal]] which compute BS γ themselves).
- Units: "Total GEX (BTC per $100 move)".

## 4. Notable engineering touches
- **Relevance filter:** default strike window = spot ±50%; auto-extends if a strike outside that range has |GEX| > median (catches far-OTM gamma walls).
- **Gamma flip** ("bootleg"): accumulate signed gamma; if early cumulative sum < 0 use `min`, else `max` → approximate zero-gamma strike. (Rough — see proper interpolation in zrack.)

## 5. How to use it
- `python main.py` → live BTC GEX-by-strike bar chart, OI as color intensity, gamma-flip estimate.
- Best as a **learning reference**: read it once and you understand naive GEX completely.

## 6. What NOT to do / limits
- **OI-weighted naive model**: assumes all calls long-gamma to dealers, all puts short — not real dealer positioning.
- Uses **Deribit's gamma**, so it inherits Deribit's IV/greeks assumptions.
- 2021 code; expect rough edges (synchronous asyncio, prints everywhere). Good to learn from, not to productionize.

## 7. Verdict
**Rank #5** — the teaching repo for the naive method. → [[06 — Build Your Own GEX Engine (architecture)]]
