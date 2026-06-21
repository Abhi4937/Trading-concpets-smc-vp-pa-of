---
title: Accurate DIY GEX — Closing the Gap to Paid
tags: [gex, diy, accuracy, validation, methodology, synthesis, capstone]
created: 2026-06-21
status: grounded-in-source
---

# 🎯 Accurate DIY GEX — Closing the Gap to Paid

> **Capstone note.** This note assumes you have read [[02 — The Math — Greeks to Dollar GEX (with code)]] and [[06 — Build Your Own GEX Engine (architecture)]]. It does not repeat what is already there — it builds on top of them to answer the question: *How accurate can my free-data GEX model get, and what does that actually buy a discretionary trader?*

---

## 1. 🪜 The Accuracy Ladder — framing everything else

The single most important thing to understand before writing a line of code: GEX accuracy is not a continuous dial from "bad" to "good." It is a **discrete set of methodological tiers**, and each tier requires fundamentally different data. The jump from naive to trade-aware is large; the jump from trade-aware to true-dealer-tagged is smaller but still real.

| Tier | Method | Data needed | Who does it | Accuracy level | Effort |
|------|--------|-------------|-------------|----------------|--------|
| **0 — OI naive** | Call + / Put − on static OI | Deribit REST snapshot | CryptoGamma, GammaFlip, Bitcoin-Options-GEX, gex-tracker, zrack | Low — sign is an equity assumption, not a measurement | Very low |
| **1 — Volume-proxy** | Call + / Put − on intraday volume (OI proxy) | Deribit trade feed | zrack (volume weight variant) | Low — inherits OI-naive sign, adds volume-churn noise (documented in zrack's own `model-assumptions.md`) | Low |
| **2 — Trade-aware** | Sign by per-trade buy/sell direction | Deribit trade feed (direction field) | dankbit | Medium — infers long/short from print direction; better than naive, but direction is still a reconstructed inference | Medium |
| **3 — Taker-flow reconstruction** | Dealer = mirror image of cumulative taker flow per strike/maturity | Deribit trade tape (taker field per trade) | Glassnode; replicable in DIY with Deribit trade API | High — the most defensible *free-replicable* method; anchored in actual flow, not static heuristics. Source: [Glassnode research](https://research.glassnode.com/gamma-exposure/) | High |
| **4 — Aggressor-matched (paid)** | Exchange-level quote-to-trade aggressor matching, true dealer-net-inventory | Proprietary institutional feed | Amberdata AD Derivatives (`dealerNetInventory`) | Highest claimed — but vendor self-asserted; no independent benchmark published. ⚠️ Pricing details unverified — treat as institutional-only until independently validated | Very high |

> **Reading note:** the tier number tells you how much you trust the *sign*. The gamma math (Black-Scholes Γ × size × S² × 0.01) is identical at every tier — what differs is whether you know *which side dealers are actually on* at each strike.

### Why the sign matters more than anything else

See [[02 — The Math — Greeks to Dollar GEX (with code)]] §3b worked example: flipping every put from negative to positive converts a net GEX of **+2.2M** to **+8.0M** — a 260% difference in magnitude, and the regime signal is unchanged only because you got lucky. In a real case the sign flip can reverse the regime outright: what reads as net long-gamma (pinning) on the naive model may be net short-gamma (trending) on a taker-flow model. Two dashboards showing opposite regimes for the same chain are almost always a sign-convention disagreement, not a data error.

### Why Tier 3 (taker-flow) is the correct free target

Deribit exposes the taker on every trade in the public API. That is a structural advantage over equity options markets where customer/dealer tagging is done at the OCC level, behind a paywall. The Glassnode approach — "the maker on the other side of the trade is a dealer providing liquidity" — is a reasonable heuristic for Deribit where liquidity provision is concentrated among professional market makers. You can replicate the *spirit* of this method with the Deribit trade API:

```python
# Schematic of taker-flow reconstruction (Tier 3)
# On each trade from Deribit's /public/get_last_trades_by_currency:
#   taker_side: "buy" or "sell"
#   The dealer's side = opposite of taker_side
#   Dealer is long if taker_side == "sell", short if taker_side == "buy"

def dealer_sign(taker_side, option_type):
    """Returns +1 if dealer is long this contract, -1 if short."""
    dealer_is_long = (taker_side == "sell")   # dealer is the maker
    if dealer_is_long:
        return +1   # long call = +GEX; long put = still +GEX (dealer is long gamma either way)
    else:
        return -1   # short option = negative gamma exposure

# Then per-trade contribution:
# gex_contribution = dealer_sign * amount * bs_gamma(S, K, t, r, iv) * S * (S*0.01) * multiplier
# Accumulate across all open trades (or infer from trade tape + expiry/close tracking)
```

> ⚠️ **Honesty note:** Glassnode does not disclose exact algorithmic steps ("please reach out to your account manager" — verified via [research.glassnode.com](https://research.glassnode.com/gamma-exposure/)). The *concept* of taker-mirroring is public; the precise inventory-tracking and decay/rolloff mechanics are proprietary. A DIY taker-flow model will approximate, not replicate, Glassnode.

---

## 2. 🧮 The Error Budget — every source of inaccuracy and the cheap fix

Even within a single tier, your model can be more or less accurate depending on how carefully you handle these inputs. Most errors compound; the sign-convention error alone can dominate everything else.

### 2a. Error sources ranked by impact

| Error source | Potential magnitude | Cheap fix | Notes |
|---|---|---|---|
| **Sign convention** (Tier 0/1 using call+/put−) | Can reverse the regime entirely | Move to Tier 3 (taker-flow) or Tier 2 (trade-aware, see dankbit) | The dominant error. See §1 above. |
| **IV source: mark IV vs your own surface** | 5–20% gamma error on wings, negligible ATM | Use Deribit's `greeks.gamma` directly — they run a calibrated vol surface; don't recompute from mid-quote IV | Deribit's mark IV is model-fit across the surface; recomputing from a single mid-quote gives noisy far-wing gamma |
| **Spot vs index vs futures basis** | 0.1–0.5% on gamma under normal conditions; can spike >1% on high-funding-rate days | Use `public/get_index_price` for S, not the last-traded perp price — Deribit's index is the multi-exchange composite the options are priced off | Deribit options are priced off the BTC index, not the perp. See [Deribit Index Prices](https://support.deribit.com/hc/en-us/articles/25944739377309-Index-Prices) |
| **Stale OI** | 5–15% mismatch intraday after large prints | Poll `get_book_summary_by_currency` every 5 min; do not rely on a daily snapshot for intraday levels | OI is EOD-official on most venues; Deribit's live endpoint is best available but still lags fast clearing |
| **Interest rate r=0 assumption** | <1% error on near-term gamma for BTC options | Set r=0 for most practical purposes; funding rate basis is *not* the Black-Scholes r — it affects forward pricing separately | BTC European options on Deribit settle to the index; crypto yield is near zero in spot terms. This is a minor error. |
| **Ignoring multi-leg / structured trades** | Unknown; multi-leg OTC trades don't split cleanly on the tape | Flag unusually large single-strike prints; check if they have offsetting legs by scanning for near-simultaneous opposite prints | Block and structured deals (e.g. collars, spreads) show up as individual legs — the net GEX may be zero for a spread but your model counts each leg separately, overstating gross exposure |
| **Naive OI split (no customer/dealer tagging)** | Sign-dependent, can be large | Taker-flow reconstruction (Tier 3) is the mitigation — see §1 | Without dealer tagging, you cannot know if a 10,000-OI call strike is 90% customer long (dealer short = negative GEX) or 90% dealer long (positive GEX) |
| **Zero-gamma interpolation method** | $200–500 in live examples (documented) | Use repricing method (compute aggregate gamma across a spot grid, find the root) not per-strike sign-scan | Naive linear-interpolation between the two strikes flanking a sign change "teleports" by hundreds of dollars on minor rebalancing. Source: [FlashAlpha](https://flashalpha.com/articles/gamma-flip-methodology-stable-zero-gamma-level) |
| **Expiry-day pinning / gamma decay** | Large near expiry: ATM gamma spikes, then vanishes at 08:00 UTC | Segregate 0DTE view (see GEX Terminal's 0DTE toggle); re-read model *after* expiry — don't hold a pin thesis through 08:00 UTC | Deribit expiry is 08:00 UTC. The GEX profile at 07:55 UTC is meaningless at 08:05 UTC. |
| **Gamma scaling: per-1% vs per-$1 convention** | 100× difference in the output number, zero impact if consistent | Choose one and be explicit in your output labels; per-1%-move is what dashboards display | See [[02 — The Math — Greeks to Dollar GEX (with code)]] §2 |
| **Contract size / multiplier** | 1× error on BTC inverse options (multiplier=1); different for micro contracts | BTC inverse options on Deribit: contract size = 1 BTC (verified via [Deribit API](https://docs.deribit.com/api-reference/market-data/public-get_contract_size)); confirm per instrument | Get the multiplier from `public/get_contract_size` — do not hardcode across all instruments |
| **Single-venue blindness (Deribit only)** | Structurally significant now that IBIT OI has surpassed Deribit ($27.6B vs $26.9B as of April 2026) | Add IBIT overlay (free Tradier key); add GammaFlip's aggregated view (Deribit+Bybit+OKX) for crypto-native multi-venue | Source: [coinlaw.io options statistics 2026](https://coinlaw.io/options-market-in-crypto-statistics/); CME holds ~$10B additional OI. Total crypto BTC options market is materially larger than Deribit alone. |

### 2b. Which errors to fix first (prioritized)

1. **Fix sign first** (Tier 0 → Tier 3). Everything else is noise if you have the regime backwards.
2. **Fix IV source** (use Deribit's `greeks.gamma` not recomputed IV). Saves implementation effort too.
3. **Fix spot source** (use `get_index_price`, not the perp last-traded).
4. **Fix zero-gamma calculation** (grid reprice, not per-strike linear scan).
5. **Fix single-venue** by layering GammaFlip (multi-venue) and IBIT overlay.
6. Everything else is refinement.

---

## 3. 📡 Data Quality Maximization — best free inputs

### Primary source: Deribit (see [[05 — APIs and Data Sources (Deribit etc.)]])

Deribit remains the deepest crypto options venue for BTC, though IBIT has surpassed it in raw OI. For *gamma exposure construction*, Deribit is still the most tractable because:
- The taker field is public per trade (essential for Tier 3)
- Greeks are published per instrument (`greeks.gamma`, `greeks.delta`, `mark_iv`)
- The full chain is accessible in one REST call via `public/get_book_summary_by_currency`

**The three data streams you need:**

```python
# 1. Index price (use this, not perp last-traded)
GET /public/get_index_price?index_name=btc_usd
# → result.index_price

# 2. Full chain snapshot (OI, mark_iv, greeks.gamma per instrument)
GET /public/get_book_summary_by_currency?currency=BTC&kind=option
# → result[*].{instrument_name, open_interest, greeks.gamma, mark_iv, underlying_price}

# 3. Trade tape for taker-flow reconstruction (Tier 3)
GET /public/get_last_trades_by_currency?currency=BTC&kind=option&count=1000
# → result.trades[*].{instrument_name, direction, amount, iv, price, taker_side}
# taker_side: "buy"/"sell" — use this for Tier 3 dealer-sign inference
```

> For the trade tape, `get_last_trades_by_currency` gives the last N trades. For a running model, subscribe to the WebSocket channel `trades.option.BTC` for real-time ticks.

### Cross-checks: free hosted sources

Use these to validate your engine output, not to replace it:

| Source | What to use it for | Cadence | API available? |
|--------|--------------------|---------|----------------|
| **CryptoGamma** (`/api/public/snapshot?asset=BTC`) | Quick regime cross-check; compare your net GEX sign to their `netGamma` sign; compare squeeze levels to your walls | ~15 min | Yes — free JSON |
| **GammaFlip.io** | Multi-venue cross-check (Deribit+Bybit+OKX); compare their F (gamma flip) level to your zero-gamma | ~60 s | No API confirmed — visual only |
| **GEX Terminal** (gexterminal.net) | Visual validation on a live chart; compare their Call Resistance / Put Support levels to your walls; uses 5-min refresh + IBIT overlay | 5 min | No — eyes-on-glass |
| **Glassnode GEX** | Methodological benchmark for sign: when CryptoGamma and Glassnode disagree on regime, weight Glassnode (taker-flow) | 10 min | Paid tier |

### Combining venues (Deribit + CME + IBIT)

As of April 2026, the BTC options market has structurally bifurcated: IBIT ($27.6B OI) slightly leads Deribit ($26.9B), with CME adding ~$10B. A model that ignores IBIT and CME is missing 40–50% of total notional BTC options OI.

**Practical multi-venue stack:**

| Venue | Free data access | Weight approach |
|-------|-----------------|-----------------|
| **Deribit** | Full public API (greeks, OI, trades, taker) | Anchor venue — compute full Tier 3 model here |
| **IBIT** | Tradier API (free key) or OptionCharts | OI-weight IBIT GEX at ATM strikes; adds US-hours pinning pressure |
| **CME** | EOD data from [CME Group](https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/bitcoin.volume.options.html) | Use for daily regime check only (no real-time free) |
| **OKX / Bybit** | Public REST APIs (comparable to Deribit public endpoints) | Include if you have bandwidth; GammaFlip already aggregates these visually |

**Weighting formula** when merging two venues (e.g. Deribit + CME):

```python
# OI-weighted multi-venue net GEX
total_oi_deribit = sum(chain_deribit.open_interest)
total_oi_cme     = sum(chain_cme.open_interest)
total_oi         = total_oi_deribit + total_oi_cme

w_deribit = total_oi_deribit / total_oi
w_cme     = total_oi_cme / total_oi

net_gex_combined = w_deribit * net_gex_deribit + w_cme * net_gex_cme
# Note: zero-gamma is NOT the weighted average of the two zero-gammas;
# recompute it on the combined per-strike array.
```

### Volume-weighting (VW-GEX)

See [[10 — Volume-Weighted GEX (VW-GEX)]] for the full treatment. The key principle: OI accumulates historical positioning; recent volume is a better proxy for *current* hedging demand. A practical compromise:

```python
# Blend OI and recent volume for recency-sensitive walls
alpha = 0.7   # tune to your lookback preference
weight = alpha * open_interest + (1 - alpha) * volume_24h
gex_at_strike = weight * greeks_gamma * sign * S * (S * 0.01)
```

The blended weight lets short-dated, recently-traded strikes punch above their OI weight — useful for 0DTE sessions where intraday volume dwarfs the resting OI.

### DVOL as a regime sanity check

Deribit's DVOL index (30-day implied vol composite) is free and pairs naturally with your GEX model:
- DVOL rising while total GEX is negative → confirmation of short-gamma / vol-expansion regime
- DVOL falling while total GEX is strongly positive → confirmation of long-gamma / vol-compression regime
- DVOL diverging from GEX signal → flag for closer inspection; one of your inputs may be stale

---

## 4. ✅ Calibration & Validation — you can't get truth, so validate instead

Because there is no "true" dealer inventory published anywhere, you cannot compute your model's absolute accuracy. What you *can* do is validate **relative structure** (are your walls roughly where other methods say they are?) and **predictive value** (do your regimes predict the right vol behaviour?).

### Daily cross-check checklist

Run this every morning before your session:

```
□ Compare your net GEX sign to CryptoGamma netGamma sign
  → If they agree: higher confidence in regime
  → If they disagree: check whether it's a sign-convention difference (Tier 0 vs Tier 3)
    or a data-freshness issue (their cache vs your real-time)

□ Compare your zero-gamma to GammaFlip's F (flip) level
  → Agreement within $500 = reasonable; >$1,000 gap = investigate

□ Compare your gamma wall (strongest strike) to GEX Terminal's Call Resistance / Put Support
  → If your dominant wall matches their CR/PS, you share the same dominant strike — good

□ Note DVOL level: consistent with your GEX regime?

□ Record: today's walls, zero-gamma, regime sign, DVOL
  (Logging this daily is the foundation of backtesting — see below)
```

### Level hit-rate tracker (Python sketch)

The most useful validation for a discretionary trader: did price actually *respect* the levels? Track it:

```python
import json, datetime

LOG_FILE = "gex_level_log.jsonl"

def log_levels(date, walls: list, zero_gamma: float, regime: str, dvol: float):
    """Log GEX levels at session open."""
    record = {
        "date": str(date),
        "walls": walls,            # e.g. [63000, 65000]
        "zero_gamma": zero_gamma,
        "regime": regime,          # "long" or "short"
        "dvol": dvol,
        "outcome": None            # fill in at EOD
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

def update_outcome(date, held: bool, note: str = ""):
    """Update whether the levels held (fill in at EOD)."""
    lines = open(LOG_FILE).readlines()
    updated = []
    for line in lines:
        r = json.loads(line)
        if r["date"] == str(date):
            r["outcome"] = {"held": held, "note": note}
        updated.append(json.dumps(r))
    with open(LOG_FILE, "w") as f:
        f.write("\n".join(updated) + "\n")

def hit_rate(lookback_days=30):
    """Compute level hit-rate over last N days."""
    records = [json.loads(l) for l in open(LOG_FILE)]
    cutoff = datetime.date.today() - datetime.timedelta(days=lookback_days)
    recent = [r for r in records if r["outcome"] and r["date"] >= str(cutoff)]
    hits = sum(1 for r in recent if r["outcome"]["held"])
    return hits / len(recent) if recent else None
```

### Regime backtest — DVOL approach

A light-touch regime validation that does not require perfect data:

1. For each day in your log where you recorded regime = "short-gamma":
   - Check: did realized vol over the next 2 sessions exceed a threshold (e.g. >1.5× DVOL implied)?
2. For "long-gamma" days: did price stay within the two nearest walls for the majority of the session?

You do not need tick data. Daily candles are sufficient to score regime accuracy. Thirty days of logging gives you a meaningful sample.

### Sanity-check: total GEX magnitude

Cross-check your absolute GEX magnitude against CryptoGamma's numbers (they display in the same units if you use the per-1%-move convention). If your total is within 20% of theirs on the same snapshot time, your math is consistent with their implementation. Larger divergence usually means a multiplier error, a different subset of expiries included, or a vol source difference.

---

## 5. 🎯 "Close Enough to Speculate" — the honest verdict

### What precision do you actually need?

A discretionary trader using GEX as context — not as a signal-generator — needs to answer three questions per session:

1. **What is the regime?** (Long gamma / pinning or short gamma / trending)
2. **Where are the major walls?** (Within ±$500 is actionable — exact dollars are not)
3. **Where is zero-gamma?** (Within ±$1,000 is actionable for swing; ±$500 for intraday)

That is it. You do not need to match Amberdata's `dealerNetInventory` to the dollar. The reason: **GEX is an environment and a map, not a prediction** — the wall at $64,000 is useful because dealers are *likely* to hedge there, creating structural flow; it is not a hard line that spot respects on a schedule. The probability it "holds" is regime-dependent, not precision-dependent.

See [[08 — Pitfalls and Misconceptions (what NOT to do)]] §10: "GEX tells you the weather and the landmarks. It does not tell you which direction to drive."

### What the paid tier actually buys you

| Capability | Free DIY (Tier 3) | Paid (Amberdata / Laevitas Premium) |
|------------|-------------------|--------------------------------------|
| Regime sign reliability | High (taker-flow) | Higher (claimed aggressor-match) — but unindependently validated |
| Wall accuracy | ±$500–1,000 is typical | Marginal improvement; same underlying Deribit chain |
| Cross-venue aggregation | Manual (Deribit + IBIT via Tradier) | Automated, more complete |
| Historical data | None free | Laevitas Premium ($50/mo) gives CSV export; Amberdata at enterprise pricing |
| IBIT / CME integration | Manual + Tradier (free) | Automated in Laevitas / Amberdata |
| Real-time latency | 5–60 min on free hosted; real-time on your own Deribit WS engine | Real-time API |
| Support / reliability | OSS / self-hosted | Paid SLA |

> ⚠️ The accuracy gap between a well-built Tier 3 free model and Laevitas/Amberdata is **narrower than most retail traders assume** and **far narrower than vendor marketing implies**. The Deribit taker field is public. What you cannot replicate free is true cross-venue dealer inventory reconciliation and validated historical data for backtesting.

### The recommended "best free stack"

For a sophisticated discretionary trader who will build and maintain a model:

| Layer | Tool / Source | Role |
|-------|---------------|------|
| **Primary engine** | Your own Deribit-WS Tier 3 model (see [[06 — Build Your Own GEX Engine (architecture)]]) | Ground truth for your session |
| **Multi-venue regime check** | GammaFlip.io (free, ~60s, Deribit+Bybit+OKX) | Catch Deribit-only blindspots |
| **IBIT layer** | GEX Terminal + free Tradier key | US ETF options structure (now >Deribit in OI) |
| **API cross-check** | CryptoGamma `/api/public/snapshot` | Sanity-check net sign + squeeze levels |
| **Methodology benchmark** | Glassnode GEX (paid — check if your institution has access) | When free tools disagree, this is the tiebreaker on sign |
| **Validation log** | Your `gex_level_log.jsonl` (§4 above) | 30-day rolling hit-rate; the only honest accuracy metric you have |

> If you can only do one thing: build a Tier 2 or Tier 3 Deribit model using the architecture in [[06 — Build Your Own GEX Engine (architecture)]], cross-check the regime against CryptoGamma daily, and watch GammaFlip for multi-venue divergence. That stack costs $0, runs in real-time, and gives you structural GEX quality that surpasses every Tier 0 free dashboard.

---

## 6. 🏗️ Recommended Architecture Summary

This note is the accuracy layer on top of the architecture defined in [[06 — Build Your Own GEX Engine (architecture)]]. The build prescription is there; the accuracy prescriptions from this note map to it as follows:

| Architecture layer | This note's accuracy upgrade |
|--------------------|------------------------------|
| **Adapter** | Subscribe to `trades.option.BTC` WS channel for taker-field (Tier 3); subscribe to `book.BTC*.100ms` for live IV ticks |
| **Engine (pure)** | Use `greeks.gamma` from Deribit (not recomputed); set S = index price (not perp last); compute zero-gamma via grid reprice (not linear scan) |
| **State** | Track cumulative taker-signed inventory per strike/maturity (not just OI snapshot) |
| **Output** | Log walls + zero-gamma + DVOL + regime to JSONL for hit-rate tracking (§4) |
| **Validation** | Daily CryptoGamma API cross-check automated in the poller; GammaFlip visual review at session open |

Final pointer: [[06 — Build Your Own GEX Engine (architecture)]] §7 "Upgrade path" already maps Tier 0 → Tier 2 → Tier 3 in code. The accuracy work in this note is the *why* behind that upgrade path.

---

## Sources & further reading

- Glassnode: [Introducing Taker-Flow-Based Gamma Exposure](https://research.glassnode.com/gamma-exposure/) — primary methodology source for Tier 3
- Glassnode: [Gamma Exposure Heatmap](https://insights.glassnode.com/gamma-exposure-heatmap/) — heatmap visualization of GEX across strikes over time
- FlashAlpha: [The Gamma Flip Problem](https://flashalpha.com/articles/gamma-flip-methodology-stable-zero-gamma-level) — documents the naive zero-gamma interpolation failure mode and the repricing fix
- Deribit: [Index Prices](https://support.deribit.com/hc/en-us/articles/25944739377309-Index-Prices) — why you must use the index, not the perp, for S
- Deribit: [get_contract_size API](https://docs.deribit.com/api-reference/market-data/public-get_contract_size) — multiplier per instrument
- CoinLaw: [Options Market in Crypto Statistics 2026](https://coinlaw.io/options-market-in-crypto-statistics/) — market share data (IBIT $27.6B, Deribit $26.9B, CME $10B as of April 2026)
- Blockchain News: [Glassnode Launches Taker-Flow-Based GEX](https://blockchain.news/flashnews/glassnode-launches-taker-flow-based-gamma-exposure-gex-for-crypto-options-to-map-dealer-hedging-volatility-regimes-and-key-price-levels) — secondary coverage of the methodology launch

---

*Vault links: [[02 — The Math — Greeks to Dollar GEX (with code)]] · [[06 — Build Your Own GEX Engine (architecture)]] · [[08 — Pitfalls and Misconceptions (what NOT to do)]] · [[Tool Deep-Dives/Glassnode Gamma Exposure]] · [[05 — APIs and Data Sources (Deribit etc.)]] · [[10 — Volume-Weighted GEX (VW-GEX)]] · [[04 — Dashboards Directory + RANKING]] · [[Tool Deep-Dives/dankbit]] · [[Tool Deep-Dives/GEX Terminal Pro]] · [[Tool Deep-Dives/CryptoGamma]] · [[Tool Deep-Dives/GammaFlip.io]]*
