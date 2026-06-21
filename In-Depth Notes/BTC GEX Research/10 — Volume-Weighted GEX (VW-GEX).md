---
title: Volume-Weighted GEX (VW-GEX)
tags: [gex, volume, weighting, deribit, intraday, methodology, python]
created: 2026-06-21
status: grounded-in-source
---

# 📊 Volume-Weighted GEX (VW-GEX)

> The weight you put on each option contract — OI, today's volume, or trade-signed direction — is the **single biggest methodological fork** in GEX. This note goes deep on the volume case: why it exists, the exact formula, how to build it from Deribit data, and how to use the divergence between OI-GEX and VW-GEX as a live intraday signal.
>
> Pre-reading: [[02 — The Math — Greeks to Dollar GEX (with code)]] (the OI formula baseline) and [[06 — Build Your Own GEX Engine (architecture)]] (which already names all three weighting choices). This note extends and deepens the volume branch.

---

## 1. 🤔 Three weighting philosophies — what each actually measures

The formula skeleton is always the same:

$$\text{GEX}_{\text{strike}} = \Gamma_{\text{BS}} \times \text{weight} \times \text{sign} \times \text{spot scaling}$$

Only the **weight** and **sign** change. Here is what each choice actually tells you:

| Weighting | What it measures conceptually | Analogy |
|-----------|-------------------------------|---------|
| **Open Interest (OI)** | Total standing positions across **all time** until expiry — a stock, a snapshot. Includes contracts opened weeks ago that may have been partially delta-hedged, rolled, or offset elsewhere | The total outstanding balance in a bank account — present state, no information about today's deposits/withdrawals |
| **Volume (today's contracts traded)** | Fresh **activity** on this instrument today — a flow, not a stock. Captures new position-opening, closing, and rolling that occurred during this session | Today's net transaction log — tells you what's happening now, not what accumulates since inception |
| **Trade-signed amount** | Volume with directional intent attached: **buy** = taker bought the option (likely opening a long = dealer sold it, dealer short gamma); **sell** = taker sold (likely opening a short = dealer long gamma). The bridge from flow → dealer-gamma | Not just transactions but who initiated each — distinguishes "customer buying calls" from "market maker layering bids" |

> **Key insight from [[02 — The Math — Greeks to Dollar GEX (with code)]]:** OI-GEX and volume-GEX produce different numbers *and* can produce different signs at the same strike. The weight changes the magnitude; the sign rule changes the regime interpretation. Never mix conventions mid-calculation.

---

## 2. 🔍 Why volume-weight at all — the stale-OI problem

### 2a. OI's structural lag

OI is a **snapshot updated once per day** (Deribit publishes it in near-real-time via API, but it accumulates historically from all sessions). It includes:

- Contracts opened last Tuesday that a hedge fund has since partially offset with futures
- Positions that have been rolled (the old strike shows OI even though the holder's view has shifted to a different strike)
- Structured product legs where the hedge is elsewhere (the option book says long gamma but the hedger already locked in a synthetic short via perp)
- Options sold by retail (small accounts) who have no delta-hedging capability — their gamma has no mechanical market impact

Volume captures **only what traded today**. It is more responsive to intraday regime shifts. This matters most on:

- **Expiry days:** open OI at 09:00 includes contracts that will be settled/closed by 12:00 — OI-GEX at 14:00 is partly fictional on expiry day
- **Large single-session flows:** a block trade of 500 calls opens at 10:00; it doesn't affect OI until next-day reporting. Volume-GEX picks it up immediately
- **Rolling events:** fund rolls 1,000 BTC of Dec calls to Mar — Dec OI looks temporarily high as the position is open on both legs simultaneously; volume shows the net new Mar flow

### 2b. When OI-GEX is better

OI-GEX remains more meaningful for:

- **Multi-day horizon:** position accumulation over weeks reflects where the structural hedging bid/ask is; volume varies daily
- **Low-volume OTM strikes:** far-from-money strikes trade infrequently; volume on any given day is near zero, making VW-GEX noise there. OI still gives you the structural gamma wall
- **Term structure analysis:** looking at the 90-day gamma profile for position sizing — OI is the right input, not today's activity
- **Overnight and pre-open:** no volume yet; VW-GEX is empty. OI-GEX is the only baseline available

### 2c. The trade-off summarised

| | OI-GEX | VW-GEX | Trade-signed GEX |
|--|--------|--------|-----------------|
| **Data freshness** | Session-lagged (WS is near-RT but accumulates history) | Today-only | Real-time, trade-by-trade |
| **Noise level** | Low (smoothed over time) | Medium (churn, see §6) | High (needs aggregation) |
| **Intraday responsiveness** | Low | High | Highest |
| **Information content** | Structural walls | Today's hedging pressure | Actual dealer gamma delta |
| **Horizon best suited for** | Swing / multi-day | Intraday | Scalp / minute-by-minute |
| **Available from** | `get_book_summary_by_currency` + OI field | `get_book_summary_by_currency` + volume field | `get_last_trades_by_currency` + direction |

---

## 3. 🧮 The VW-GEX formula — exact form

The OI formula from [[02 — The Math — Greeks to Dollar GEX (with code)]] (per-1%-move convention):

$$\text{GEX}^{\text{OI}}_{\text{strike}} = \Gamma \times OI \times S^2 \times 0.01 \times \text{sign}$$

**Volume-Weighted GEX replaces OI with today's traded volume:**

$$\boxed{\text{GEX}^{\text{VW}}_{\text{strike}} = \Gamma_{\text{BS}}(S, K, t, \sigma, r) \times V_{\text{today}} \times S^2 \times 0.01 \times \text{sign}}$$

Where:
- $\Gamma_{\text{BS}}$ — Black-Scholes gamma (computed or read from Deribit's `greeks.gamma`)
- $V_{\text{today}}$ — **contracts traded today** (same units as OI: 1 contract = 1 BTC on Deribit inverse options)
- $S$ — spot index price (BTC/USD)
- $S^2 \times 0.01$ — per-1%-move dollarization (identical to OI version — same scaling)
- **sign** — +1 for calls, −1 for puts (naive convention; see below for signed-volume alternative)
- **multiplier** = 1.0 for BTC inverse index options (1 contract = 1 BTC; [Deribit docs](https://docs.deribit.com/))

### 3a. Where it differs from the OI formula

| Component | OI formula | VW formula |
|-----------|-----------|------------|
| Weight | `open_interest` (all-time accumulation) | `volume` (today's 24h trades) |
| Gamma source | Same: BS-computed or Deribit `greeks.gamma` | Same |
| Scaling | `S² × 0.01` | `S² × 0.01` (identical) |
| Sign rule | +call/−put (naive) | +call/−put (naive) **or** sign-from-direction (VW-signed) |
| BTC multiplier | 1.0 | 1.0 |

> The only change is the weight. Everything else — gamma computation, dollarization, sign convention, aggregation by strike — is identical. This means you can reuse the engine from [[06 — Build Your Own GEX Engine (architecture)]] with a single parameter swap.

### 3b. The signed-volume variant (bridge to taker-flow)

The volume from `get_book_summary_by_currency` is **unsigned** (total contracts in + out, no direction). You can improve signal quality by using per-trade direction from `get_last_trades_by_currency`:

$$\text{GEX}^{\text{VW-signed}}_{\text{strike}} = \sum_{\text{trades today}} \text{sign}(\text{taker direction}) \times \text{amount}_i \times \Gamma_i \times S^2 \times 0.01$$

Where `sign(taker direction)` = +1 if the taker bought, −1 if the taker sold. This is the same logic as dankbit's trade-aware sign (see [[02 — The Math — Greeks to Dollar GEX (with code)]], §3), and is the first step toward [[Tool Deep-Dives/Glassnode Gamma Exposure]]'s taker-flow reconstruction.

> Plain VW-GEX (unsigned volume + naive +call/−put) is a pragmatic middle ground between naive OI-GEX and full taker-flow GEX. It is significantly cheaper to compute and interpret without needing per-trade streaming.

---

## 4. 🏗️ Build it from Deribit — exact data and Python

### 4a. Data sources on Deribit

Two paths; use the right one for your latency budget:

**Path A — Bulk REST (polling, simplest):**

`GET /public/get_book_summary_by_currency?currency=BTC&kind=option`

Returns per-instrument: `volume` (24h contracts traded, in BTC for options), `open_interest` (BTC), `mark_iv` (%), `underlying_price` (spot), `instrument_name`. One call gets the whole chain. [Docs](https://docs.deribit.com/api-reference/market-data/public-get_book_summary_by_currency)

> ⚠️ `volume` here is total 24-hour activity — not just today's session if your session started mid-day. `volume` is a **rolling 24h window**, not a calendar-day reset. This is critical for expiry-day distortions (§6). The OI field in this endpoint is the real-time standing position count.

**Path B — Per-trade REST (signed volume):**

`GET /public/get_last_trades_by_currency?currency=BTC&kind=option&count=1000`

Returns up to 1000 most recent trades. Each trade: `instrument_name`, `direction` ("buy"/"sell", **from the taker's perspective**), `amount` (BTC contracts), `iv` (implied vol at trade time), `index_price`, `timestamp`. [Docs](https://docs.deribit.com/api-reference/market-data/public-get_last_trades_by_currency)

> For intraday accumulation you need to **paginate** using `start_timestamp` / `end_timestamp` to cover the full session. Max 1000 per call.

**Path C — Live WebSocket stream (lowest latency):**

Subscribe to `trades.option.BTC.raw` or `trades.option.BTC.100ms` — fires on every new BTC option trade with fields: `instrument_name`, `direction`, `amount`, `iv`, `index_price`, `price`, `timestamp`. [Deribit subscription docs](https://docs.deribit.com/subscriptions/trades/tradesinstrument_nameinterval)

> The WS `direction` field means the same as the REST one: taker's direction. This is the lowest-latency path; build a rolling accumulator keyed by strike.

### 4b. Parsing the instrument name

Deribit instrument names follow the pattern `BTC-DDMMMYY-STRIKE-C/P`:

```
BTC-27JUN25-64000-C  →  strike=64000, call
BTC-27JUN25-58000-P  →  strike=58000, put
```

```python
def parse_instrument(name: str) -> dict:
    parts = name.split("-")          # ["BTC", "27JUN25", "64000", "C"]
    return {
        "expiry": parts[1],
        "strike": int(parts[2]),
        "option_type": parts[3],     # "C" or "P"
    }
```

### 4c. Full VW-GEX engine — bulk REST version

This parallels the OI engine in [[06 — Build Your Own GEX Engine (architecture)]] §3, but substitutes `volume` for OI as the weight:

```python
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timezone

BASE = "https://www.deribit.com/api/v2"


def bs_gamma(S: float, K: np.ndarray, t: np.ndarray, r: float, sigma: np.ndarray) -> np.ndarray:
    """Black-Scholes gamma. S=spot, K=strikes, t=time_to_expiry_years, sigma=IV (decimal)."""
    t = np.where(t <= 0, 1e-5, t)                      # floor at expiry
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * t) / (sigma * np.sqrt(t))
    n_prime = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * d1 ** 2)
    return n_prime / (S * sigma * np.sqrt(t))


def fetch_chain_summary(currency: str = "BTC") -> pd.DataFrame:
    """
    Pull the entire option chain via get_book_summary_by_currency.
    Returns DataFrame with columns: instrument_name, strike, option_type,
    expiry_str, volume (BTC contracts, 24h), open_interest (BTC),
    mark_iv (decimal), underlying_price.
    """
    resp = requests.get(
        f"{BASE}/public/get_book_summary_by_currency",
        params={"currency": currency, "kind": "option"},
        timeout=10,
    ).json()

    rows = []
    for item in resp["result"]:
        name = item["instrument_name"]
        parts = name.split("-")
        if len(parts) != 4:
            continue
        rows.append({
            "instrument_name": name,
            "expiry_str": parts[1],
            "strike": int(parts[2]),
            "option_type": parts[3],                     # "C" or "P"
            "volume": float(item.get("volume") or 0),    # 24h BTC contracts; 0 if None
            "open_interest": float(item.get("open_interest") or 0),
            "mark_iv": float(item.get("mark_iv") or 0) / 100.0,  # % → decimal
            "underlying_price": float(item.get("underlying_price") or 0),
        })
    return pd.DataFrame(rows)


def expiry_to_dte(expiry_str: str) -> float:
    """Convert Deribit expiry string like '27JUN25' to DTE in years."""
    dt = datetime.strptime(expiry_str, "%d%b%y").replace(
        hour=8, minute=0, tzinfo=timezone.utc          # Deribit settles at 08:00 UTC
    )
    now = datetime.now(timezone.utc)
    dte_years = max((dt - now).total_seconds() / (365.25 * 86400), 1e-5)
    return dte_years


def compute_vw_gex(
    df: pd.DataFrame,
    spot: float,
    r: float = 0.0,
    multiplier: float = 1.0,           # 1.0 for BTC inverse index options
    per_pct_move: bool = True,         # True = per 1% move (standard); False = per $1
    use_oi: bool = False,              # swap to OI weighting for comparison
) -> pd.DataFrame:
    """
    Compute volume-weighted (or OI-weighted) GEX per strike.

    Returns DataFrame with: strike, call_vwgex, put_vwgex, net_vwgex.
    All values in USD.
    """
    df = df.copy()

    # Resolve spot if not provided explicitly (use underlying_price from chain)
    if spot == 0:
        spot = df["underlying_price"].median()

    # DTE per expiry
    df["dte"] = df["expiry_str"].map(expiry_to_dte)

    # Choose weight
    weight_col = "open_interest" if use_oi else "volume"

    # Compute gamma vectorised
    S = spot
    K = df["strike"].values.astype(float)
    t = df["dte"].values
    sigma = df["mark_iv"].values
    sigma = np.where(sigma <= 0, 0.001, sigma)            # floor near-zero IV

    df["gamma"] = bs_gamma(S, K, t, r, sigma)

    # Dollarize: per-1%-move convention  →  gamma * S * (S*0.01) * multiplier
    # Equivalently: gamma * S^2 * 0.01 * multiplier
    if per_pct_move:
        df["dollar_gamma"] = df["gamma"] * S * (S * 0.01) * multiplier
    else:
        df["dollar_gamma"] = df["gamma"] * S ** 2 * multiplier

    # Weight by volume (or OI) and apply naive sign (+call / −put)
    df["sign"] = np.where(df["option_type"] == "C", 1.0, -1.0)
    df["gex_per_contract"] = df["dollar_gamma"] * df["sign"]
    df["strike_gex"] = df[weight_col] * df["gex_per_contract"]

    # Aggregate by strike
    agg = (
        df.assign(
            call_gex=np.where(df["option_type"] == "C", df["strike_gex"], 0.0),
            put_gex=np.where(df["option_type"] == "P", df["strike_gex"], 0.0),
        )
        .groupby("strike")
        .agg(call_vwgex=("call_gex", "sum"), put_vwgex=("put_gex", "sum"))
        .reset_index()
    )
    agg["net_vwgex"] = agg["call_vwgex"] + agg["put_vwgex"]
    return agg.sort_values("strike").reset_index(drop=True)


# ──────────────────────────────────────────
# Example: compare OI-GEX vs VW-GEX side by side
# ──────────────────────────────────────────
if __name__ == "__main__":
    chain = fetch_chain_summary("BTC")
    spot_price = chain["underlying_price"].median()

    vw  = compute_vw_gex(chain, spot_price, use_oi=False)
    oi  = compute_vw_gex(chain, spot_price, use_oi=True)

    merged = vw.rename(columns={"net_vwgex": "net_vw"})\
               .merge(oi[["strike","net_vwgex"]].rename(columns={"net_vwgex":"net_oi"}),
                      on="strike")

    # Top 10 strikes by |VW-GEX|
    top = merged.reindex(merged["net_vw"].abs().nlargest(10).index)
    print(top[["strike", "net_vw", "net_oi"]].to_string(index=False))

    # VW gamma wall vs OI gamma wall
    vw_wall  = vw.loc[vw["net_vwgex"].abs().idxmax(), "strike"]
    oi_wall  = oi.loc[oi["net_vwgex"].abs().idxmax(), "strike"]
    print(f"\nVW-GEX wall: {vw_wall:,}   |   OI-GEX wall: {oi_wall:,}")
    if vw_wall != oi_wall:
        print("  ↳ DIVERGENCE: today's volume is concentrating at a different strike than standing OI.")
```

### 4d. Signed-volume VW-GEX — per-trade accumulator

For intraday signed-volume GEX you need to accumulate trades and look up the option's IV (since `get_last_trades_by_currency` returns `iv` per trade). This is the bridge toward taker-flow GEX — see [[Tool Deep-Dives/Glassnode Gamma Exposure]].

```python
from collections import defaultdict

def fetch_session_trades(
    currency: str = "BTC",
    session_start_ms: int | None = None,     # Unix ms; None = last 1000 trades
    max_pages: int = 10,
) -> pd.DataFrame:
    """
    Pull all BTC option trades since session_start_ms.
    Paginates using start_timestamp / end_timestamp (max 1000 per call).
    direction = "buy" | "sell" from the TAKER's perspective (Deribit docs confirmed).
    """
    all_trades = []
    params = {"currency": currency, "kind": "option", "count": 1000, "sorting": "desc"}
    if session_start_ms:
        params["start_timestamp"] = session_start_ms

    for _ in range(max_pages):
        resp = requests.get(
            f"{BASE}/public/get_last_trades_by_currency", params=params, timeout=10
        ).json()["result"]

        trades = resp.get("trades", [])
        if not trades:
            break
        all_trades.extend(trades)

        if not resp.get("has_more"):
            break
        # Next page: walk backwards in time
        params["end_timestamp"] = trades[-1]["timestamp"] - 1

    return pd.DataFrame(all_trades)


def compute_signed_vw_gex(
    trades_df: pd.DataFrame,
    spot: float,
    r: float = 0.0,
    multiplier: float = 1.0,
) -> pd.DataFrame:
    """
    VW-GEX with per-trade sign from taker direction.
    sign = +1 if taker BOUGHT (dealer sold → dealer short gamma → positive dealer GEX)
    sign = −1 if taker SOLD (dealer bought → dealer long gamma → negative dealer GEX)

    NOTE: this uses the Glassnode taker-mirror logic. See §3b and the pitfall in §6
    about sign ambiguity in multi-leg trades and block trades.
    """
    df = trades_df.copy()

    # Filter options only (instrument names end in -C or -P)
    df = df[df["instrument_name"].str.endswith(("C", "P"))].copy()

    # Parse strike and option type
    parsed = df["instrument_name"].str.split("-", expand=True)
    df["strike"] = parsed[2].astype(int)
    df["option_type"] = parsed[3]
    df["expiry_str"] = parsed[1]
    df["dte"] = df["expiry_str"].map(expiry_to_dte)

    # IV from trade (decimal); floor at 0.1%
    df["sigma"] = pd.to_numeric(df["iv"], errors="coerce").fillna(0.5) / 100.0
    df["sigma"] = df["sigma"].clip(lower=0.001)

    # Gamma per trade (using trade-time spot approximation; use index_price if available)
    trade_spot = pd.to_numeric(df["index_price"], errors="coerce").fillna(spot).values
    df["gamma"] = bs_gamma(
        trade_spot,
        df["strike"].values.astype(float),
        df["dte"].values,
        r,
        df["sigma"].values,
    )

    # Dollar gamma per 1% move
    df["dollar_gamma"] = df["gamma"] * trade_spot * (trade_spot * 0.01) * multiplier

    # Taker direction sign: +1 = taker bought, −1 = taker sold
    df["taker_sign"] = np.where(df["direction"] == "buy", 1.0, -1.0)

    # Signed GEX per trade
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df["signed_gex"] = df["taker_sign"] * df["amount"] * df["dollar_gamma"]

    # Aggregate by strike
    agg = df.groupby("strike")["signed_gex"].sum().reset_index()
    agg.columns = ["strike", "net_signed_vwgex"]
    return agg.sort_values("strike").reset_index(drop=True)
```

> ⚠️ **Block trades caveat:** `get_last_trades_by_currency` includes block trades (field `block_trade_id` is non-null). For block trades the direction convention may be less reliable as a dealer-taker inference — the counterparty is a known institution, not a retail-side taker. Filter with `df = df[df["block_trade_id"].isna()]` if you want to exclude blocks from the signed accumulator.

---

## 5. 📖 How to read and use VW-GEX — concrete rules

### 5a. What a VW-GEX wall tells you that OI can't

An OI gamma wall at $64,000 says: "there is a large accumulated position at this strike across all time." It may have been hedged away, rolled, or represent a structural position from months ago.

A VW-GEX wall at $64,000 says: "the most dollar gamma was actively traded at this strike **today**." That means active participants are putting on, taking off, or rolling positions there right now. The hedging delta-flows associated with those contracts are being executed **in the current session**, not some past session.

**Rule 1 — VW-GEX wall = intraday hedging pressure zone.**
When VW-GEX and OI-GEX agree on the same wall strike: high conviction. Both structural and intraday gamma are concentrated there. Expect stronger pinning / resistance.

**Rule 2 — VW-GEX wall diverges above OI wall: fresh call buying.**
If VW-GEX puts the wall at $66,000 but OI-GEX is at $64,000, a block of calls at $66,000 traded today. Dealers who sold those calls are now delta-hedging those positions by buying the underlying — bullish intraday drift toward $66,000 is plausible. The OI wall hasn't moved yet; it will update overnight.

**Rule 3 — VW-GEX wall diverges below OI wall: fresh put buying / call selling.**
Put flows dominate today. Dealers are buying puts (or selling calls), adding negative gamma. Intraday momentum risk increases; the structural OI-GEX wall above may fail as support on the way up.

**Rule 4 — VW-GEX near zero, OI-GEX large: stale book.**
Today is quiet. The structural gamma walls from OI still apply for swing framing but there is no fresh intraday hedging pressure adding to them. Do not expect strong intraday pin behavior.

**Rule 5 — VW-GEX total sign flips vs OI-GEX total sign: regime alert.**
If `sum(net_vwgex) < 0` but `sum(net_oi_gex) > 0`, then *today's flow* is short-gamma even though the book's accumulated position is long-gamma. Treat the current session as a short-gamma environment (trend/momentum bias) even though the headline OI-GEX says long-gamma (pinning bias). This divergence is the strongest intraday signal VW-GEX produces.

### 5b. Intraday regime detection workflow

```
Each hour (or on a major candle close):
 1. Recompute VW-GEX from the last N hours of volume data
 2. Compare:
    a. VW-GEX total sign  vs  OI-GEX total sign   →  regime agreement or divergence?
    b. VW-GEX wall strike vs  OI-GEX wall strike   →  where is today's hedging pressure?
    c. VW-GEX zero-gamma  vs  OI-GEX zero-gamma    →  do the vol-flip levels agree?

 If all three agree: trade off OI-GEX levels with high conviction.
 If VW-GEX total sign diverges from OI-GEX: bias the session toward VW-GEX (fresher).
 If walls diverge: watch both levels; expect a tug between structural and intraday gravity.
```

### 5c. Comparing the two bar charts visually

Run `compute_vw_gex` twice (OI and volume) and overlay the bar charts at each strike. Strikes where VW-GEX bar is large but OI-GEX bar is small: **freshly active today**. Strikes where OI-GEX bar is large but VW-GEX bar is small: **structural but dormant today** — don't weight them for intraday pin.

### 5d. How VW-GEX complements (not replaces) OI-GEX

VW-GEX is a *same-session confirmation or denial* of OI levels. It is not a replacement. The hierarchy:

| Horizon | Primary weighting | Secondary |
|---------|-------------------|-----------|
| Swing (2–5 days) | OI-GEX | VW-GEX as divergence alert |
| Intraday (< 1 day) | VW-GEX | OI-GEX as structural backdrop |
| Expiry day | VW-GEX (OI is decaying fast) | OI at open only |

---

## 6. ⚠️ Pitfalls specific to volume-weighting

Cross-link: [[08 — Pitfalls and Misconceptions (what NOT to do)]] covers the general GEX traps. Below are the pitfalls **unique to or amplified by** volume weighting.

### 6a. Volume ≠ net new position

A contract traded once in the morning and closed in the afternoon shows `volume = 2` but `net new OI = 0`. The gamma was present for half a session then gone. Volume-GEX over-counts short-lived positions. You cannot distinguish opening-volume from closing-volume in `get_book_summary_by_currency` (it gives you a total, not net open).

> Mitigation: use signed-volume (§4d) and accumulate `(buy_volume - sell_volume)` per strike as a proxy for net new inventory. Or use a data service (Tardis.dev, Amberdata) that provides full trade history with open/close flags.

### 6b. Market-maker churn inflates volume

Market makers quote tightly and flip positions many times per session — each flip generates trade volume. A heavily quoted at-the-money strike shows huge volume not because of directional position-opening but because of two-sided liquidity provision. This makes ATM strikes look like massive VW-GEX concentrations even when the net dealer gamma there is near zero.

> Mitigation: use signed-volume accumulator. MM two-sided flow roughly cancels: they sell 100 at ask then buy 100 at bid → +100 taker-buys − 100 taker-sells ≈ 0 net. Unsigned volume (both legs counted) doubles the MM contribution; signed accumulates near zero.

### 6c. 24h rolling window vs. calendar-day reset

`get_book_summary_by_currency` `volume` is a rolling **24-hour** window, not a session reset. At 11:00 UTC it includes trades from yesterday 11:00 through today 11:00. On active days this is close enough; on days with very different morning vs afternoon behavior it dilutes the intraday signal with stale volume.

> Mitigation: use the per-trade endpoint (`get_last_trades_by_currency` with `start_timestamp = session_open_ms`) to build a true session-start-to-now volume accumulation. More work, but accurate.

### 6d. Expiry-day distortions

On expiry day (Deribit BTC options expire at 08:00 UTC), the soon-to-expire contracts trade heavily in the final hours as holders close, exercise, or let expire. Their gamma is collapsing to zero for near-the-money options and is already zero for far ITM/OTM. Volume-GEX from these expiring contracts produces large numbers for strikes that have essentially zero hedging impact after 08:00 UTC.

> Mitigation: filter out today's expiry contracts from the VW-GEX calculation by excluding instruments where `expiry_str == today_deribit_expiry`. This matches how Laevitas offers per-maturity GEX views.

### 6e. Block trades — directionality is unreliable for dealer inference

Block trades (identified by non-null `block_trade_id`) are negotiated off-screen between two institutional counterparties. The "taker" label in the API is less meaningful — either side may have initiated the trade. Including block trades in a signed-volume accumulator can distort the dealer-gamma inference.

> Mitigation: exclude block trades when computing signed VW-GEX. They still count in unsigned volume if you want to see raw activity.

### 6f. Double-counting with combo/multi-leg structures

`kind=option_combo` trades appear as a single combo trade and also as individual legs. If you query `kind=any` without filtering, you can count the same underlying gamma twice.

> Mitigation: always query `kind=option` (not `kind=any`) when building the options-only VW-GEX.

---

## 7. 🗂️ Which weighting should I run? — decision table

| Situation | Best weighting | Why |
|-----------|---------------|-----|
| Swing setup, 2–5 day hold | **OI** | Structural hedge walls; today's volume noise irrelevant |
| Intraday scalp / 1–4h trade | **Volume (VW-GEX)** | Fresh hedging pressure is more relevant than accumulated structure |
| Expiry day after 06:00 UTC | **Volume, filter expiring contracts** | OI on expiring contracts is decaying/noise |
| Building the zero-gamma level for the week | **OI** | Volume resets daily; the vol-flip level is structural |
| Detecting intraday regime flip | **VW-GEX total sign vs OI-GEX total sign** | Use the divergence, not either alone |
| Nearest approximation to true dealer gamma | **Trade-signed volume** (§4d) | Dealer = mirror of taker; signed-volume is the closest public proxy |
| You have only 5 minutes to set up | **OI-GEX from `get_book_summary_by_currency`** | One call, no pagination, same computation pipeline |
| Want to validate paid dashboard readings | **Run OI-GEX first** (matches most tools) then VW-GEX to see divergence | Most dashboards (CryptoGamma, GammaFlip, Bitcoin-Options-GEX) are OI-based |

→ For the overall accuracy gap between all DIY methods and paid tools: [[13 — Accurate DIY GEX — closing the gap to paid]]
→ Full engine with OI weight to modify: [[06 — Build Your Own GEX Engine (architecture)]]
→ Signed-volume taken to its logical conclusion (Glassnode taker-flow): [[Tool Deep-Dives/Glassnode Gamma Exposure]]
→ General GEX pitfalls (sign convention, OI staleness, regime traps): [[08 — Pitfalls and Misconceptions (what NOT to do)]]

---

## 📎 Verified sources

- Deribit `get_book_summary_by_currency` — `volume` field definition (24h, in BTC for options): [https://deribit.mintlify.app/api-reference/market-data/public-get_book_summary_by_currency](https://deribit.mintlify.app/api-reference/market-data/public-get_book_summary_by_currency)
- Deribit `get_last_trades_by_currency` — `direction` is taker's direction, `amount` in BTC for options, max 1000: [https://docs.deribit.com/api-reference/market-data/public-get_last_trades_by_currency](https://docs.deribit.com/api-reference/market-data/public-get_last_trades_by_currency)
- Deribit WS `trades.{instrument_name}.{interval}` subscription — `direction`, `amount`, `iv` fields confirmed: [https://docs.deribit.com/subscriptions/trades/tradesinstrument_nameinterval](https://docs.deribit.com/subscriptions/trades/tradesinstrument_nameinterval)
- BTC inverse options: contract size = 1 BTC, multiplier = 1.0 (confirmed Deribit docs)
- SpotGamma OI+Volume intraday adjustment model (proprietary, equity-focused, cited as conceptual parallel): [https://spotgamma.com/gamma-exposure-gex/](https://spotgamma.com/gamma-exposure-gex/)

> ⚠️ **Unverified / vendor-asserted claims in this note:**
> - That Glassnode's taker-flow method produces a meaningfully more accurate dealer-gamma number than signed-volume in practice (Glassnode self-asserts this; independently verifiable only by comparing against realized hedge flows, which are not public)
> - That Amberdata's `dealerNetInventory` uses true aggressor-matched flow (Amberdata self-asserts, no independent verification found)
> - Note 13 ("Accurate DIY GEX — closing the gap to paid") is a **planned note** that does not yet exist in the vault
