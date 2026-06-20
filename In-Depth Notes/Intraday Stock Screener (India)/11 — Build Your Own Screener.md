---
title: "11 — Build Your Own Screener"
tags: [screener, python, pipeline, intraday, NSE, indicators, VWAP, jugaad-data, pandas-ta]
created: 2026-06-21
---

# 11 — Build Your Own Screener

End-to-end guide to building a Python-based intraday stock screener for Indian markets (NSE F&O universe). Start simple, stay operational.

---

## Pipeline Overview

```
┌──────────────┐     ┌───────────────────┐     ┌─────────────────────────┐
│  UNIVERSE    │────▶│  DATA INGESTION   │────▶│  INDICATORS             │
│  F&O list    │     │  EOD: jugaad-data │     │  VWAP, EMA 9/20/50      │
│  (~170 stks) │     │  Live: websocket  │     │  RSI, ATR, RelVol       │
└──────────────┘     └───────────────────┘     └────────────┬────────────┘
                              │                              │
                     [[09 — NSE Data Sources]]    [[10 — APIs (broker + data)]]
                                                             │
                                                             ▼
                                              ┌─────────────────────────┐
                                              │  FILTERS                │
                                              │  Long scan (breakout)   │
                                              │  Short scan (mirror)    │
                                              │  Liquidity gate FIRST   │
                                              └────────────┬────────────┘
                                                           │
                                                           ▼
                                              ┌─────────────────────────┐
                                              │  RANK                   │
                                              │  Relative strength      │
                                              │  + Relative volume      │
                                              └────────────┬────────────┘
                                                           │
                                                           ▼
                                              ┌─────────────────────────┐
                                              │  OUTPUT                 │
                                              │  CSV / Telegram alert   │
                                              └─────────────────────────┘
```

---

## Step 0: Liquidity Gate (Run This First)

Apply [[06 — Liquidity & Tradability Filters]] before computing a single indicator. Calculating RSI on an illiquid stock wastes time and generates false signals.

```python
# Minimum thresholds (adjust per your capital size)
MIN_PRICE = 50          # avoid sub-50 Rs noise
MIN_AVG_VOLUME = 500_000  # 5L shares/day average
MIN_ATR_PCT = 0.015     # at least 1.5% daily range

def passes_liquidity(df: pd.DataFrame) -> bool:
    avg_vol = df["VOLUME"].rolling(20).mean().iloc[-1]
    atr_pct = (df["atr"].iloc[-1] / df["CLOSE"].iloc[-1])
    return (
        df["CLOSE"].iloc[-1] > MIN_PRICE
        and avg_vol > MIN_AVG_VOLUME
        and atr_pct > MIN_ATR_PCT
    )
```

---

## Step 1: Universe — F&O Symbol List

The F&O list (~170 stocks) is a ready-made liquidity filter. Refresh it monthly from NSE. See [[09 — NSE Data Sources]] for the direct download URL.

```python
import pandas as pd

# Download from NSE (update URL monthly)
FO_URL = "https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O"
# Simpler: cache a local CSV and refresh monthly
universe = pd.read_csv("fo_universe.csv")["Symbol"].tolist()
```

---

## Step 2: EOD Data via jugaad-data

```python
from jugaad_data.nse import stock_df
from datetime import date, timedelta

def get_eod(symbol: str, lookback: int = 60) -> pd.DataFrame:
    to_date = date.today()
    from_date = to_date - timedelta(days=lookback + 30)  # buffer for holidays
    df = stock_df(symbol=symbol, from_date=from_date, to_date=to_date, series="EQ")
    df = df.sort_values("DATE").reset_index(drop=True)
    return df
```

See [[09 — NSE Data Sources]] for alternatives (NSEPy, eod2, nselib).

---

## Step 3: Compute Indicators

```python
import pandas_ta as ta

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df["ema9"]  = ta.ema(df["CLOSE"], 9)
    df["ema20"] = ta.ema(df["CLOSE"], 20)
    df["ema50"] = ta.ema(df["CLOSE"], 50)
    df["rsi"]   = ta.rsi(df["CLOSE"], 14)
    df["atr"]   = ta.atr(df["HIGH"], df["LOW"], df["CLOSE"], 14)
    df["relvol"] = df["VOLUME"] / df["VOLUME"].rolling(20).mean()
    # VWAP on EOD is a daily proxy; for true intraday VWAP see Step 5
    df["vwap_proxy"] = (df["HIGH"] + df["LOW"] + df["CLOSE"]) / 3
    return df
```

---

## Step 4: Apply Scans

### Long Scan (Breakout / Trend)

```python
def long_scan(df: pd.DataFrame) -> bool:
    r = df.iloc[-1]
    return (
        r["CLOSE"] > r["ema9"]
        and r["ema9"] > r["ema20"]
        and r["ema20"] > r["ema50"]   # full stack alignment
        and r["relvol"] > 2.0         # volume surge
        and r["rsi"] > 60             # momentum confirmation
        and r["CLOSE"] > MIN_PRICE
    )
```

### Short Scan (Mirror)

```python
def short_scan(df: pd.DataFrame) -> bool:
    r = df.iloc[-1]
    return (
        r["CLOSE"] < r["ema9"]
        and r["ema9"] < r["ema20"]
        and r["ema20"] < r["ema50"]
        and r["relvol"] > 2.0
        and r["rsi"] < 40
    )
```

---

## Step 5: Live Intraday — Broker Websocket

EOD scans give you candidates for tomorrow. For real intraday VWAP and ORB you need live 1m/5m bars from a broker API. See [[10 — APIs (broker + data)]].

```python
# Pseudocode — adapt to Dhan / Upstox / Fyers SDK
from broker_sdk import WebSocket

ws = WebSocket(api_key=API_KEY, access_token=ACCESS_TOKEN)
intraday_frames: dict[str, pd.DataFrame] = {}

def on_tick(tick):
    sym = tick["symbol"]
    # Append tick to rolling intraday frame
    intraday_frames.setdefault(sym, pd.DataFrame())
    # Recompute VWAP, relvol, ORB on every new bar
    # Emit ranked list when conditions met

ws.subscribe(fo_symbols, on_tick=on_tick)
ws.run_forever()
```

**Key point**: intraday VWAP requires intraday bars. EOD data cannot substitute.

---

## Step 6: Rank and Output

```python
def run_screener(universe: list[str]) -> pd.DataFrame:
    results = []
    for sym in universe:
        try:
            df = get_eod(sym)
            df = add_indicators(df)
            if not passes_liquidity(df):
                continue
            r = df.iloc[-1]
            direction = "LONG" if long_scan(df) else ("SHORT" if short_scan(df) else None)
            if direction:
                results.append({
                    "symbol": sym, "direction": direction,
                    "close": r["CLOSE"], "rsi": round(r["rsi"], 1),
                    "relvol": round(r["relvol"], 2), "atr": round(r["atr"], 2),
                })
        except Exception as e:
            print(f"{sym}: {e}")
    out = pd.DataFrame(results).sort_values("relvol", ascending=False)
    out.to_csv("watchlist.csv", index=False)
    return out
```

Send the watchlist to Telegram with `python-telegram-bot` or a simple `requests.get(TELEGRAM_URL)` call.

---

## Reference Implementations

See [[12 — GitHub Tool Deep-Dives]] for walkthroughs of:

- **PKScreener** — battle-tested EOD screener, F&O universe built-in, good filter reference
- **Screeni-py** — similar philosophy, easy to fork
- **eod2** — clean EOD data pipeline, good ingestion patterns
- **Hummingbird** — more advanced, live streaming architecture

Read their filter logic before building your own; avoid re-inventing what is already validated.

---

## Don't Over-Engineer

> Start with EOD data + 3-4 robust filters. Ship something runnable in a weekend. Add live streaming only after the EOD version is producing actionable candidates.

Checklist:
- [ ] F&O universe CSV, refreshed monthly
- [ ] EOD fetch loop with jugaad-data (batch overnight)
- [ ] Liquidity gate runs before any indicator math
- [ ] Long + short scans, ranked by relative volume
- [ ] Output to CSV; Telegram alert is optional phase 2
- [ ] Live websocket streaming: phase 3, once EOD is proven
