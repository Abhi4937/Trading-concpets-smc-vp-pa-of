---
title: Real-Time Dealer Positioning — CLOB Aggressor vs Block/OTC
tags: [gex, dealer-positioning, deribit, clob, block-trade, otc, taker-flow, aggressor, paradigm, python]
created: 2026-06-21
status: grounded-in-source
---

# 🎯 Real-Time Dealer Positioning — CLOB Aggressor vs Block/OTC

> **Core question this note answers:** You want to know, right now, what the dealers (market-makers) are net-long or net-short on each BTC options strike. How do you reconstruct that from Deribit's public data — and what are the hard limits of the inference?
>
> This note builds directly on [[06 — Build Your Own GEX Engine (architecture)]] §7 ("upgrade to real dealer GEX") and the taker-flow methodology explained in [[Tool Deep-Dives/Glassnode Gamma Exposure]]. Read those first if you need the conceptual foundation.

---

## 1. 📖 What Is a CLOB? (First Principles)

A **Central Limit Order Book (CLOB)** is the matching engine at the heart of any exchange. Every listed option on Deribit trades on a CLOB. Understanding how it works is the prerequisite for everything that follows.

### 1.1 The structure

| Role | Who they are | What they do |
|------|--------------|--------------|
| **Maker / Liquidity Provider** | Market-makers, dealers, prop shops | Post **resting limit orders** at a price level — they provide liquidity. Their order sits in the book until hit. |
| **Taker / Aggressor** | Directional traders, hedgers, speculators | Send a **market order or an immediately-crossing limit order** that removes resting liquidity from the book. They *take* liquidity. |

The CLOB organizes all resting bids and asks by price, with time priority at the same price level (first-in, first-served). When a taker's order arrives:

1. The matching engine finds the best resting order on the opposite side.
2. A trade is printed. The **aggressor** is the taker — the one who caused the match.
3. The trade is signed as **"buy"** if the taker lifted the ask (taker bought), **"sell"** if the taker hit the bid (taker sold).

### 1.2 Why "aggressor side" matters for dealer inference

The fundamental insight: **if the taker bought, someone had to sell**. In a liquid options market, that seller is very often the market-maker / dealer. They do not take directional views — they quote both sides and manage inventory. So:

```
Taker BUYS a call  →  Dealer is likely SHORT that call  →  Dealer short gamma (negative GEX contribution)
Taker SELLS a call →  Dealer is likely LONG that call   →  Dealer long gamma  (positive GEX contribution)
Taker BUYS a put   →  Dealer is likely SHORT that put   →  Dealer short gamma (positive GEX from the dealer's perspective... wait, no)
```

Wait — this is where put sign trips people up. From the **dealer's perspective**:

- Dealer **short call** → dealer is short gamma (call gamma is positive; if dealer is short the call, they have negative gamma exposure → they must buy as price rises, selling as it falls → **amplifying**)
- Dealer **long call** → dealer is long gamma → dampening
- Dealer **short put** → dealer is short gamma (put gamma is also positive; short put = short gamma)
- Dealer **long put** → dealer is long gamma

> So the sign of the taker-inferred dealer GEX is: if taker **buys** any option (call or put), the dealer is short that option, meaning **negative gamma for the dealer**. If taker **sells** any option, dealer is long → **positive gamma**.

This is the **taker-flow / aggressor-matching** method. It is the method Glassnode uses (see [[Tool Deep-Dives/Glassnode Gamma Exposure]]) and is fundamentally different from the naive equity convention (call+ / put−). The naive convention *assumes* dealers are long calls and short puts — which is not reliably true in crypto.

### 1.3 Why price-time priority matters

In a CLOB with price-time priority, the order sitting at the best price *and* having arrived earliest fills first. This means large resting orders from a single market-maker can be visible in the order book before being hit — the "making" activity is publicly observable (but order-book data is separate from trade data). The trade feed only records what *executed*, not what was resting.

---

## 2. 🏛️ Deribit's Market Structure

Deribit is a **CLOB exchange** for BTC/ETH/SOL/XRP options and futures. Every option trade — whether a simple call purchase or a complex spread — ultimately clears through Deribit. It held approximately **85% of global crypto options open interest** as of end-2024 (Coinbase acquired Deribit in 2025 for $2.9B, confirming its dominance).

> Sources: [CoinGlass 2025 Derivatives Market Report via RootData](https://www.rootdata.com/news/480534); [Coindesk Deribit IBIT comparison](https://www.coindesk.com/markets/2025/03/06/deribit-launches-block-rfq-system-to-improve-liquidity-for-large-over-the-counter-trades)

There are **two distinct ways** a trade gets printed to Deribit's tape:

| Trade type | Mechanism | Aggressor field reliable? |
|------------|-----------|--------------------------|
| **On-book / CLOB trade** | Taker order crosses resting maker orders via the matching engine | ✅ Yes — `direction` = taker side |
| **Block trade / RFQ** | Negotiated off-book, then registered and printed to the tape | ⚠️ No — direction field is present but semantically ambiguous for negotiated trades |

---

## 3. 🔌 Pulling Trades from Deribit — Exact API Fields

Deribit's public API exposes the full trade tape with no authentication required. There are three ways to access it:

### 3.1 REST endpoints (snapshot / history)

```
GET https://www.deribit.com/api/v2/public/get_last_trades_by_currency
    ?currency=BTC&kind=option&count=1000&sorting=desc

GET https://www.deribit.com/api/v2/public/get_last_trades_by_instrument
    ?instrument_name=BTC-27DEC24-100000-C&count=100
```

### 3.2 WebSocket (real-time stream)

Subscribe to the trades channel for all BTC options:
```json
{
  "jsonrpc": "2.0",
  "method": "public/subscribe",
  "params": {
    "channels": ["trades.option.BTC.raw"]
  },
  "id": 1
}
```

For a specific instrument:
```json
"channels": ["trades.BTC-27DEC24-100000-C.raw"]
```

### 3.3 Full per-trade field schema (verified from Deribit API docs)

Source: [Deribit API Reference — public/get_last_trades_by_currency](https://docs.deribit.com/api-reference/market-data/public-get_last_trades_by_currency)

| Field | Type | Meaning |
|-------|------|---------|
| `trade_id` | string | Unique trade identifier (per currency) |
| `trade_seq` | integer | Sequence number within the instrument |
| `instrument_name` | string | e.g. `BTC-27DEC24-100000-C` |
| `timestamp` | integer | Unix milliseconds at execution |
| **`direction`** | enum `buy`/`sell` | Schema lists it tersely as "buy/sell". For **CLOB trades** = the **taker/aggressor** side (`buy` = taker lifted ask; `sell` = taker hit bid). For **block trades** Deribit reports it from the **maker's** side → unreliable (see §5.3). |
| `tick_direction` | integer 0–3 | Price tick classification (0=Plus, 1=Zero-Plus, 2=Minus, 3=Zero-Minus) — not for GEX use |
| `price` | number | Execution price in BTC (for inverse options) |
| `amount` | number | **For options: size in the base currency (BTC)** — 1 contract = 1 BTC, already in BTC, **no conversion needed**. (The USD-denomination rule applies only to **inverse futures/perpetuals**, not options.) |
| `contracts` | number | Optional — size in contract units |
| `iv` | number | Implied volatility at trade time (options only); use for BS gamma recalculation |
| `mark_price` | number | Mark price at trade moment |
| `index_price` | number | BTC index price at trade moment (spot) |
| **`liquidation`** | enum `M`/`T`/`MT` | Present only for liquidation trades. `M`=maker liquidated, `T`=taker liquidated, `MT`=both. Skip these for dealer inference — they are forced/involuntary. |
| **`block_trade_id`** | string | Present **only if this trade was part of a block trade**. The ID is shared across all legs of a multi-leg block. If absent → regular CLOB trade. |
| **`block_trade_leg_count`** | integer | Number of legs in the block trade (e.g. 2 for a call spread, 3 for a risk reversal with delta hedge). Present alongside `block_trade_id`. |
| `combo_id` | string | Present if part of a combo instrument (Deribit-defined strategy) |
| `combo_trade_id` | string | Shared ID across combo trade legs |
| **`block_rfq_id`** | integer | Present if the block was executed via Deribit's Block RFQ system (launched March 2025) |

> ✅ **Field-meaning note (verified against Deribit docs):** the schema lists `direction` tersely as "buy / sell". For **matched on-book (CLOB) trades** this is the **taker/aggressor** side by convention — the basis of all taker-flow analysis (incl. Glassnode). ⚠️ For **block trades**, Deribit expresses `direction` from the **maker's** perspective, which is a further reason it is unreliable for blocks (see §5.3). Sources: [Deribit trades.(kind).(currency).(interval) subscription docs](https://docs.deribit.com/subscriptions/upcoming/trades/tradeskindcurrencyinterval); [Deribit Block Trading support](https://support.deribit.com/hc/en-us/articles/25944688627229-Block-Trading)

> ⚠️ **Critical caveat:** Deribit's own documentation and independent analysis of options flow have flagged that the `direction` field is **not always reliable for block trades**. For regular CLOB trades it is clean; for block/combo/RFQ trades, more complex heuristics are required (see §4 and §5).

---

## 4. 🟢 On-Book CLOB Trades — Reconstructing Dealer Gamma in Real Time

### 4.1 The inference logic

For each on-book trade (no `block_trade_id`):

```
direction = "buy"  → taker BOUGHT → dealer likely SOLD → dealer is SHORT the option
                   → delta_dealer_gamma = -(amount × BS_gamma(instrument)) × S²

direction = "sell" → taker SOLD  → dealer likely BOUGHT → dealer is LONG the option
                   → delta_dealer_gamma = +(amount × BS_gamma(instrument)) × S²
```

Note: the sign is **uniform for calls and puts**. This is the key departure from the naive method. The taker direction tells you directly — no need to apply call+ / put− rules.

### 4.2 Python — real-time dealer GEX accumulator (WebSocket)

```python
import asyncio, json, websockets
from scipy.stats import norm
import numpy as np
from collections import defaultdict
from datetime import datetime, timezone

WS_URL = "wss://www.deribit.com/ws/api/v2/"

# ─── Black-Scholes Gamma (annualized) ────────────────────────────────────────
def bs_gamma(S: float, K: float, T: float, sigma: float, r: float = 0.0) -> float:
    """Returns Γ per-contract (Δ per $1 move in spot)."""
    if T <= 0 or sigma <= 0:
        return 0.0
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))

def dollar_gamma(S: float, K: float, T: float, sigma: float, amount_btc: float) -> float:
    """Dollar GEX contribution: Γ × S² × amount_btc.
    For Deribit OPTIONS the trade `amount` is ALREADY in BTC (1 contract = 1 BTC),
    so there is NO /S conversion — that rule applies only to inverse futures/perps."""
    g = bs_gamma(S, K, T, sigma)
    return g * (S ** 2) * amount_btc

# ─── State ────────────────────────────────────────────────────────────────────
# Per-strike running dealer GEX estimate:
#   positive = dealer net LONG gamma at this strike (dampening)
#   negative = dealer net SHORT gamma at this strike (amplifying)
dealer_gex_by_strike: dict[int, float] = defaultdict(float)

# ─── Trade classifier ─────────────────────────────────────────────────────────
def classify_trade(trade: dict) -> str:
    """Return 'clob', 'block', 'liquidation', or 'combo'."""
    if trade.get("liquidation"):
        return "liquidation"
    if trade.get("block_trade_id") or trade.get("block_rfq_id"):
        return "block"
    if trade.get("combo_trade_id"):
        return "combo"
    return "clob"

def parse_strike_and_type(instrument_name: str) -> tuple[int, str]:
    """'BTC-27DEC24-100000-C' → (100000, 'C')"""
    parts = instrument_name.split("-")
    return int(parts[2]), parts[3]   # strike, option_type (C or P)

# ─── Time-to-expiry (DTE) from the instrument name ───────────────────────────
_MONTHS = {m: i for i, m in enumerate(
    ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
     "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"], start=1)}

def expiry_utc(instrument_name: str) -> datetime:
    """'BTC-27DEC24-100000-C' → expiry datetime. Deribit options expire 08:00 UTC.
    Day is NOT zero-padded (e.g. 'BTC-3JAN25-...'), so slice from the right:
    last 2 chars = year, the 3 before = month, the rest = day."""
    d = instrument_name.split("-")[1]          # e.g. '27DEC24' or '3JAN25'
    day   = int(d[:-5])                         # everything before the month
    month = _MONTHS[d[-5:-2]]                    # 3-letter month
    year  = 2000 + int(d[-2:])                   # 2-digit year → 20xx
    return datetime(year, month, day, 8, 0, tzinfo=timezone.utc)

def dte_years(instrument_name: str, now_ms: int) -> float:
    """Time-to-expiry in YEARS, measured from the trade's own timestamp (ms since
    epoch) so it's deterministic per trade. Floored at ~1 hour so 0-DTE / expired
    trades don't blow up the BS gamma formula (T→0 ⇒ division by ~0)."""
    now  = datetime.fromtimestamp(now_ms / 1000, tz=timezone.utc)
    secs = (expiry_utc(instrument_name) - now).total_seconds()
    return max(secs, 3600.0) / (365.0 * 24.0 * 3600.0)

# ─── Update dealer GEX from a single CLOB trade ──────────────────────────────
def update_dealer_gex(trade: dict, spot: float) -> None:
    """
    For CLOB trades only. Signs dealer position as mirror of taker.
    dealer long  (positive GEX) if taker SOLD → direction == 'sell'
    dealer short (negative GEX) if taker BOUGHT → direction == 'buy'
    """
    if classify_trade(trade) != "clob":
        return   # block/liquidation handled separately

    instr = trade["instrument_name"]
    if not instr.endswith(("-C", "-P")):
        return   # not an option

    strike, _ = parse_strike_and_type(instr)
    direction  = trade["direction"]           # 'buy' or 'sell' — taker side
    amount_btc = float(trade["amount"])       # options: size already in BTC (1 contract = 1 BTC)
    iv         = float(trade.get("iv", 0))   # option's IV at time of trade
    ts_ms      = trade["timestamp"]
    T          = dte_years(instr, ts_ms)      # exact time-to-expiry in years (08:00 UTC expiry)

    if iv <= 0:
        return  # can't compute gamma without IV

    dgex = dollar_gamma(spot, strike, T, iv / 100.0, amount_btc)

    # Taker buys  → dealer sold → dealer short gamma → subtract from dealer's total
    # Taker sells → dealer buys → dealer long gamma  → add to dealer's total
    sign = -1.0 if direction == "buy" else +1.0
    dealer_gex_by_strike[strike] += sign * dgex

# ─── WebSocket listener ───────────────────────────────────────────────────────
async def stream_trades():
    spot = 65000.0   # seed; update from public/get_index_price or ticker feed

    async with websockets.connect(WS_URL) as ws:
        sub = {
            "jsonrpc": "2.0", "id": 1,
            "method": "public/subscribe",
            "params": {"channels": ["trades.option.BTC.raw"]}
        }
        await ws.send(json.dumps(sub))

        async for raw in ws:
            msg = json.loads(raw)
            if msg.get("method") != "subscription":
                continue
            trades = msg["params"]["data"]
            for t in trades:
                update_dealer_gex(t, spot)

        # In production: also subscribe to "deribit_price_index.btc_usd" to keep spot fresh

asyncio.run(stream_trades())
```

### 4.3 Computing live GEX walls from accumulated state

```python
import pandas as pd

def get_live_gex_levels() -> dict:
    """Derive walls and zero-gamma from accumulated dealer inventory."""
    strikes = sorted(dealer_gex_by_strike.keys())
    gex_vals = [dealer_gex_by_strike[k] for k in strikes]

    s_arr = np.array(strikes, dtype=float)
    g_arr = np.array(gex_vals, dtype=float)

    total = g_arr.sum()
    gamma_wall = float(s_arr[np.argmax(np.abs(g_arr))])

    # Zero-gamma: interpolate sign change
    signs = np.sign(g_arr)
    crossings = np.where(signs[:-1] * signs[1:] < 0)[0]
    if len(crossings):
        i = crossings[0]
        zero_gamma = float(s_arr[i] - g_arr[i] * (s_arr[i+1] - s_arr[i]) / (g_arr[i+1] - g_arr[i]))
    else:
        zero_gamma = float(s_arr[np.argmin(np.abs(g_arr))])

    return {
        "total_dealer_gex": total,
        "gamma_wall": gamma_wall,
        "zero_gamma": zero_gamma,
        "strikes": strikes,
        "gex_per_strike": gex_vals,
        "regime": "long_gamma" if total > 0 else "short_gamma",
    }
```

> **Production note:** DTE (`T`) is now computed exactly by `dte_years()` above — it parses the expiry from `instrument_name` (format `BTC-DDMMMYY-STRIKE-C/P`, day **not** zero-padded) and measures time-to-expiry from the trade's own `timestamp` to the **08:00 UTC** expiry, flooring at ~1 hour so 0-DTE trades don't divide by zero. Use the `iv` field from each trade (already annualized, in %) as the volatility input — do not recompute from mark price.

---

## 5. 🟡 Block Trades and OTC — Why the Inference Breaks Down

### 5.1 What is a Deribit Block Trade?

A **block trade** is a large trade negotiated privately between two counterparties *outside the open order book*, then registered with the exchange for clearing and printed to the public tape. The minimum size is **25 BTC notional** for BTC options (verified — Deribit support documentation).

Deribit offers two block trade mechanisms:

| Mechanism | Launched | How it works |
|-----------|----------|--------------|
| **Direct Block Trade** | Older | Two parties negotiate price/size directly (via phone, chat, Paradigm); one submits to Deribit as a block trade, the other confirms. |
| **Block RFQ** | March 2025 | Initiating party submits a Request-For-Quote to Deribit; up to 20-leg structures supported; responding dealers quote back; match is printed. ([CoinDesk](https://www.coindesk.com/markets/2025/03/06/deribit-launches-block-rfq-system-to-improve-liquidity-for-large-over-the-counter-trades)) |

Both types are **printed to the public trade feed** and will appear in `get_last_trades_by_currency` results. They are flagged via `block_trade_id` (and `block_rfq_id` for the newer RFQ type).

### 5.2 Paradigm — the dominant intermediary for Deribit block flow

**[Paradigm](https://www.paradigm.co/)** is described as "the largest institutional liquidity network in crypto" providing multi-dealer RFQ for listed futures and options across Deribit, Bit.com, and CME. Key facts (sourced from search results — treat volume share as self/secondary-reported, not independently audited):

- Paradigm accounts for approximately **17% of cumulative BTC/ETH options activity on Deribit** (as of May 2024 — [CoinDesk](https://www.coindesk.com/markets/2024/05/14/paradigm-unveils-block-trading-facility-for-matic-sol-xrp-options)).
- The broader claim that "almost all block options trades on Deribit and CME are traded via Paradigm" appears in secondary sources and Paradigm's own marketing — **treat as plausible but unverified**.
- Paradigm has 1,000+ counterparties and supports complex multi-leg strategies (risk reversals, call spreads, calendars, delta-hedged structures).
- Trades negotiated on Paradigm are "submitted to Deribit for execution and clearing" and appear on the public tape as block trades. ([Deribit Insights](https://insights.deribit.com/exchange-updates/deribit-paradigm-launching-solution/))

> ⚠️ **Flag:** The "17% of Deribit cumulative volume" figure is from May 2024 secondary reporting; Paradigm's dominance of the *block trade subset specifically* (not total volume) is likely higher. No audited figure is publicly available for 2025–2026.

### 5.3 Why `direction` is unreliable for block trades

For a regular CLOB trade, `direction` is mechanically determined: the taker's order hits the book and the exchange engine tags who crossed. For a **negotiated block trade**:

1. The two parties have already agreed on price and size before submission.
2. There is no "aggressor" in the economic sense — both parties consented simultaneously.
3. For blocks, Deribit reports `direction` from the **maker's perspective** (per its block-trading docs) — not the taker/initiator — so the usual aggressor interpretation is inverted and effectively meaningless here.
4. Deribit's own documentation and Amberdata's analysis have noted that the direction field "was not always reliable under certain scenarios" for non-CLOB trades, requiring more nuanced heuristics. ([Amberdata Block Volumes blog](https://blog.amberdata.io/use-block-volumes-decorated-trades-to-detect-large-block-trade-opportunity))

Additionally, multi-leg block trades (risk reversals, spreads, butterflies) carry a **structural ambiguity**: even if you knew which side was the "initiator," signing a risk reversal (long call + short put) as a single directional label collapses nuanced gamma exposures into a single trade label.

### 5.4 Visual summary — what you can and cannot use

```
Trade arrives in feed
        │
        ▼
  block_trade_id present?
        │
   YES  │  NO (regular CLOB trade)
        │        │
        ▼        ▼
   ┌─────────┐  ┌──────────────────────────────────┐
   │  BLOCK  │  │  CLOB / ON-BOOK AGGRESSOR TRADE   │
   │         │  │                                   │
   │direction│  │ direction = taker side (reliable) │
   │ present │  │ → safe to use for dealer sign     │
   │ but NOT │  │ → update dealer_gex_by_strike[]   │
   │ reliable│  └──────────────────────────────────┘
   │ for sign│
   │ inference│
   │         │
   │ Options:│
   │ 1. Track│
   │  block  │
   │  OI by  │
   │  strike │
   │  (flow, │
   │  not    │
   │  sign)  │
   │ 2. Infer│
   │  from   │
   │  delta  │
   │  context│
   │ 3. Down-│
   │  weight │
   │  in GEX │
   └─────────┘
```

---

## 6. 🔧 Handling Block Trades in Your Pipeline

### 6.1 Detect and classify

```python
def classify_trade_detailed(trade: dict) -> dict:
    """
    Returns a classification dict with type and any special flags.
    """
    is_block      = bool(trade.get("block_trade_id"))
    is_rfq        = bool(trade.get("block_rfq_id"))
    is_liquidation = bool(trade.get("liquidation"))
    is_combo      = bool(trade.get("combo_trade_id"))
    leg_count     = trade.get("block_trade_leg_count", 1)

    return {
        "type": (
            "liquidation" if is_liquidation else
            "block_rfq"   if is_rfq else
            "block"       if is_block else
            "combo"       if is_combo else
            "clob"
        ),
        "is_multi_leg": leg_count > 1,
        "leg_count": leg_count,
        "direction_reliable": not (is_block or is_rfq or is_combo),
    }
```

### 6.2 Three strategies for handling block OI

**Strategy A — Track separately (recommended for a first build)**

```python
block_oi_by_strike: dict[int, float] = defaultdict(float)  # unsigned — just size

def handle_block_trade(trade: dict, spot: float) -> None:
    """
    For block trades: accumulate unsigned OI (we don't know sign reliably).
    Display as a secondary 'block flow' layer — size, not direction.
    """
    instr = trade["instrument_name"]
    if not instr.endswith(("-C", "-P")):
        return
    strike, opt_type = parse_strike_and_type(instr)
    amount_btc = float(trade["amount"])        # options: size already in BTC
    block_oi_by_strike[strike] += amount_btc   # unsigned — can't reliably sign it
```

This gives you a "big money was active at this strike" signal even without direction. Combine with the on-book signed GEX for a layered picture.

**Strategy B — Infer from delta (advanced, fragile)**

If you also subscribe to the order book for the instrument around the block trade timestamp, you can compare the block trade price to the prevailing best bid/ask to infer who was lifting vs hitting. But block trades do not cross the book — the price may be at, above, or below mid — making even this heuristic unreliable.

**Strategy C — Use Amberdata's Decorated Trades (paid)**

Amberdata's `Decorated Trades` endpoint enriches each trade with pre-trade and post-trade level-1 order book snapshots, allowing a pre/post comparison to determine whether the block was initiated from the buy or sell side. This is the commercial solution — see [[Tool Deep-Dives/Amberdata AD Derivatives]].

### 6.3 Multi-leg blocks — why single-strike sign inference fails

A risk reversal printed as a block trade has **two legs** (`block_trade_leg_count: 2`):
- Leg 1: BTC-27DEC24-80000-P (put, say sold by the taker)
- Leg 2: BTC-27DEC24-120000-C (call, say bought by the taker)

Even if you correctly identify the taker as the party buying the call and selling the put, these cancel in delta but create complex net-gamma profiles across two strikes. Assigning a single `direction` label to "the block" and applying it to both legs uniformly will produce **wrong GEX contributions at both strikes**.

The correct handling: process each leg independently by its individual instrument_name and amount, then sign each leg based on the leg-level trade type — which is exactly why Amberdata and Glassnode's methodology papers emphasize per-leg processing.

---

## 7. 🏗️ Complete Real-Time Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  DATA INGESTION                                                               │
│   Deribit WS ──► trades.option.BTC.raw                                      │
│   Deribit WS ──► deribit_price_index.btc_usd  (keep spot fresh)             │
│   Deribit REST ─► public/get_instruments (build expiry lookup at startup)   │
└───────────────────────┬─────────────────────────────────────────────────────┘
                        │ per-trade message
                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  CLASSIFIER                                                                   │
│   classify_trade_detailed()                                                   │
│   → type: clob / block / block_rfq / combo / liquidation                    │
│   → direction_reliable: True / False                                         │
└───────────────────┬──────────────────────┬──────────────────────────────────┘
                    │                      │
              direction_reliable           direction_reliable
                  True                       False
                    │                      │
                    ▼                      ▼
┌──────────────────────────┐   ┌────────────────────────────────────────────────┐
│  GEX UPDATER (signed)    │   │  BLOCK FLOW ACCUMULATOR (unsigned)              │
│  update_dealer_gex()     │   │  handle_block_trade()                           │
│  → dealer_gex_by_strike  │   │  → block_oi_by_strike (size only)               │
│    (signed ± per strike) │   │  (flag: "institutional flow here" — no sign)    │
└──────────┬───────────────┘   └─────────────────────────────────────────────────┘
           │
           ▼ (every 5s)
┌──────────────────────────────────────────────────────────────────────────────┐
│  GEX CALCULATOR                                                               │
│  get_live_gex_levels()                                                        │
│  → total_dealer_gex, gamma_wall, zero_gamma, regime                          │
└──────────────────────────────────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  OUTPUT                                                                       │
│  Bar chart: dealer GEX by strike (signed CLOB-inferred)                      │
│  Overlay:   block flow by strike (unsigned, hatched)                          │
│  Alerts:    price near gamma_wall, total_dealer_gex sign flip                │
└──────────────────────────────────────────────────────────────────────────────┘
```

This extends the architecture in [[06 — Build Your Own GEX Engine (architecture)]] with the trade classification and block-handling layers.

---

## 8. ⚖️ What You CAN and CANNOT Infer for Free

> **Honesty box — read this before building anything.**

### ✅ What you CAN infer from Deribit's public trade feed

| Inference | Reliability | Notes |
|-----------|-------------|-------|
| On-book CLOB taker direction (buy/sell) | High | `direction` field is mechanically assigned by the exchange matching engine |
| Which strike had the most CLOB taker activity | High | Simple count/sum of on-book trades |
| Running signed dealer gamma estimate (CLOB trades only) | Moderate | Valid only if market-maker = mirror of taker, which holds most of the time in liquid options |
| Identifying that a block trade occurred at a given strike | High | `block_trade_id` presence is reliable |
| Block trade size and instrument | High | `amount` and `instrument_name` are reliable |
| IV at time of each trade | High | `iv` field is reliable for options |

### ❌ What you CANNOT reliably infer for free

| What | Why |
|------|-----|
| Block trade aggressor direction | `direction` field is not mechanically guaranteed for negotiated trades; Amberdata's 30+ heuristic approach exists precisely because this is hard |
| Multi-leg block trade per-leg sign | Single direction label on a 2–20-leg structure collapses all legs |
| Whether the CLOB "maker" is actually a dealer vs a directional trader | The market-maker = CLOB maker assumption is a heuristic, not a certainty. A hedge fund may post limit orders too. |
| Wash trades / internalized flow | Some "taker" flow may be a firm trading with itself (two accounts); no public flag for this |
| True cumulative dealer inventory (net position built up over weeks) | The trade feed is a flow, not a stock. You can only accumulate since your subscriber started — you have no knowledge of positions entered before your observation window. |
| Paradigm block trade directionality | Paradigm represents ~17% of Deribit volume (secondary-sourced); most Paradigm trades are blocks with ambiguous direction. |

### 🔑 The gap to paid data (Amberdata)

The `dealerNetInventory` and `dealerTotalInventory` fields in [[Tool Deep-Dives/Amberdata AD Derivatives]] are Amberdata's attempt to solve the problems above: 30+ heuristics, pre/post order book snapshots per trade, and historical accumulation. This is the right approach — but it is enterprise-priced, vendor self-reported accuracy, and not independently benchmarked.

> See also: [[13 — Accurate DIY GEX — closing the gap to paid]] for strategies to narrow the gap using only public data.

---

## 9. 🔬 The Glassnode Connection

Glassnode's taker-flow GEX (see [[Tool Deep-Dives/Glassnode Gamma Exposure]]) applies exactly the methodology this note describes: treat each Deribit trade's taker direction as the observable side, infer dealer as mirror. Their documentation does not disclose how they handle block trades specifically — whether they exclude them, down-weight them, or apply heuristics. Given that blocks are ~17–30% of total flow, this is a non-trivial gap in their public methodology disclosure.

Implication for you: **your DIY version of Glassnode's method will behave differently from theirs if your block-trade handling differs**. Track both the signed CLOB component and the unsigned block component separately so you can see the divergence.

---

## 10. 📊 Quick-Reference Cheat Sheet

| Signal | API field | Reliable for dealer inference? |
|--------|-----------|-------------------------------|
| Taker bought (on-book) | `direction: "buy"`, no `block_trade_id` | ✅ Yes — dealer likely sold |
| Taker sold (on-book) | `direction: "sell"`, no `block_trade_id` | ✅ Yes — dealer likely bought |
| Block trade flagged | `block_trade_id` present | ✅ Flag reliable; direction is ⚠️ |
| Block RFQ flagged | `block_rfq_id` present | ✅ Flag reliable; direction is ⚠️ |
| Liquidation trade | `liquidation: "T"` or `"M"` | ❌ Exclude — forced flow, not dealer |
| Multi-leg block | `block_trade_leg_count > 1` | ❌ Do not sign as a single unit |
| IV at trade time | `iv` field | ✅ Use this for BS gamma calculation |
| Combo trade | `combo_trade_id` present | ⚠️ Treat like block; direction ambiguous |

---

## 11. 🔗 Related Notes

- [[02 — The Math — Greeks to Dollar GEX (with code)]] — the dollar GEX formula used in §4
- [[05 — APIs and Data Sources (Deribit etc.)]] — REST endpoints, CryptoGamma, Laevitas, Amberdata overview
- [[06 — Build Your Own GEX Engine (architecture)]] — the system design this note's pipeline extends; §7 references this note
- [[08 — Pitfalls and Misconceptions (what NOT to do)]] — why naive call+/put− sign convention fails in crypto
- [[Tool Deep-Dives/Glassnode Gamma Exposure]] — the published taker-flow GEX methodology
- [[Tool Deep-Dives/dankbit]] — OSS implementation of trade-direction-signed dealer gamma
- [[Tool Deep-Dives/Amberdata AD Derivatives]] — paid true-dealer positioning via aggressor matching
- [[13 — Accurate DIY GEX — closing the gap to paid]] — strategies to tighten the DIY reconstruction

---

## Sources

- [Deribit API Reference — public/get_last_trades_by_currency](https://docs.deribit.com/api-reference/market-data/public-get_last_trades_by_currency)
- [Glassnode — Introducing Taker-Flow-Based Gamma Exposure](https://research.glassnode.com/gamma-exposure/)
- [Deribit Insights — Deribit & Paradigm Block Trading Solution](https://insights.deribit.com/exchange-updates/deribit-paradigm-launching-solution/)
- [Deribit Block RFQ Support Article](https://support.deribit.com/hc/en-us/articles/25951371614621-Deribit-Block-RFQ)
- [CoinDesk — Deribit Launches Block RFQ (March 2025)](https://www.coindesk.com/markets/2025/03/06/deribit-launches-block-rfq-system-to-improve-liquidity-for-large-over-the-counter-trades)
- [CoinDesk — Paradigm 17% of Deribit cumulative BTC/ETH options (May 2024)](https://www.coindesk.com/markets/2024/05/14/paradigm-unveils-block-trading-facility-for-matic-sol-xrp-options)
- [Amberdata — Use Block Volumes & Decorated Trades](https://blog.amberdata.io/use-block-volumes-decorated-trades-to-detect-large-block-trade-opportunity)
- [Paradigm.co](https://www.paradigm.co/)
- [Deribit Insights — Decoding Option Flows Q2 2023](https://insights.deribit.com/industry/decoding-option-flows-q2-2023/)
