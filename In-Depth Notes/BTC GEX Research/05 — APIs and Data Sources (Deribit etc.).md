---
title: APIs & Data Sources (Deribit, CryptoGamma, Laevitas, Amberdata)
tags: [gex, api, deribit, cryptogamma, laevitas, amberdata, integration]
created: 2026-06-20
status: grounded-in-source
---

# 🔌 APIs & Data Sources — pull GEX programmatically

> Everything ultimately reads **Deribit** (≈85–90% of crypto options OI). You can
> either consume a hosted API (CryptoGamma free / Laevitas paid / Amberdata enterprise)
> or hit Deribit directly and compute GEX yourself. Code below is copy-paste ready.

---

## 1. Deribit (the root data source) — free, public, no key
**WebSocket:** `wss://www.deribit.com/ws/api/v2/` · **REST:** `https://www.deribit.com/api/v2/` · JSON-RPC 2.0.

| Method | Gives you |
|--------|-----------|
| `public/get_index_price` (`index_name:"btc_usd"`) | spot index |
| `public/get_instruments` (`currency:"BTC", kind:"option", expired:false`) | all live option names |
| `public/get_order_book` (`instrument_name`) | per-option `greeks.gamma`, `open_interest`, mark IV, bid/ask |
| `public/get_book_summary_by_currency` | bulk OI/IV across the chain (fewer calls) |

```python
# Minimal Deribit GEX pull (sync REST version)
import requests, pandas as pd
B = "https://www.deribit.com/api/v2"
spot = requests.get(f"{B}/public/get_index_price", params={"index_name":"btc_usd"}).json()["result"]["index_price"]
names = [i["instrument_name"] for i in
         requests.get(f"{B}/public/get_instruments",
                      params={"currency":"BTC","kind":"option","expired":"false"}).json()["result"]]
rows=[]
for n in names:                                   # (parallelize in production)
    ob = requests.get(f"{B}/public/get_order_book", params={"instrument_name":n}).json()["result"]
    sign = 1 if n.endswith("C") else -1
    rows.append({"strike":int(n.split("-")[2]), "gamma":ob["greeks"]["gamma"],
                 "oi":ob["open_interest"], "sign":sign})
df = pd.DataFrame(rows)
df["gex"] = df.oi * df.gamma * df.sign * 100      # naive GEX per $100 move
gex_by_strike = df.groupby("strike").gex.sum().sort_index()
```
> Production tip: use the **WebSocket + ThreadPool** (as Bitcoin-Options-GEX does) — the chain is hundreds of instruments.

## 2. CryptoGamma — free public JSON (easiest automation)
```bash
curl -H "User-Agent: Mozilla/5.0" \
  "https://cryptogamma.io/api/public/snapshot?asset=BTC"
```
Returns: `netGamma, callGamma, putGamma, bias, squeeze{support,resistance,breakout}, realized/implied vol, flow, riskMetrics{deltaHedging,squeezeRisk,pinRisk}, generatedAt`. (`?asset=ETH` also.) Refresh ~15 min. A fuller "Market Intel API" is *Coming Soon*.

```python
import requests
s = requests.get("https://cryptogamma.io/api/public/snapshot",
                 params={"asset":"BTC"}, headers={"User-Agent":"Mozilla/5.0"}).json()
if s["netGamma"] < 0 and s["riskMetrics"]["squeezeRisk"] > THRESH:
    alert(f"Short-gamma + squeeze risk; breakout {s['squeeze']['breakout']}")
```
> ⚠️ Send a browser `User-Agent` — bare curl can return empty.

## 3. Laevitas — documented REST V1.0 (paid for key/history)
Docs: https://docs.laevitas.ch/options/analytic

| Endpoint | Returns |
|----------|---------|
| `GET /analytics/options/gex_date_all/{market}/{currency}` e.g. `/deribit/BTC` | per-strike GEX, all options |
| `GET /analytics/options/gex_date/{market}/{currency}/{maturity}` e.g. `…/BTC/24DEC26` | per-strike GEX, one maturity |
Currencies (Deribit): BTC, ETH, PAXG, SOL, XRP. Auth: API key (Premium/Enterprise; **API history = $500 Enterprise tier**). CSV export on Premium ($50).

## 4. Amberdata AD Derivatives — enterprise REST
Docs: https://docs.amberdata.io/reference/derivatives-trades-flow-gamma-gex-snapshots
Deribit BTC **GEX snapshots** with **`dealerNetInventory` / `dealerTotalInventory`** (true dealer-positioning via aggressor matching). ⚠️ Quote-based pricing; key required; WS/CSV/S3/Python breadth was **claimed but unverified**. For institutions.

## 5. Other inputs worth wiring in
| Source | Use | Notes |
|--------|-----|-------|
| **Deribit DVOL** | BTC 30-day implied vol index | regime context (vol expansion/contraction) |
| **Tradier API** (free key) | **IBIT** US ETF options levels | cross-market confluence (GEX Terminal uses this) |
| **Hyperliquid WS** | live BTC perp candles | charting layer (GEX Terminal uses this) |

## 6. Reference integration pattern
```
[Deribit WS] ─┐
[CryptoGamma]─┼─► poller (cron) ─► your store ─► alert engine ─► TradingView/Telegram
[Laevitas API]┘                         │
                                        └─► backtest / dashboard
```
Full build-out: [[06 — Build Your Own GEX Engine (architecture)]]. Trading logic on top: [[07 — Trader Usage Playbook (how to use together)]].
