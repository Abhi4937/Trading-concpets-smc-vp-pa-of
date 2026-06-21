---
title: CME Bitcoin Options & Futures as a GEX Input
tags: [gex, cme, bitcoin, options, futures, data-sources, institutional, brr, quikstrike, cot]
created: 2026-06-21
status: grounded-in-source
---

# 🏛️ CME Bitcoin Options & Futures as a GEX Input

> The vault is otherwise Deribit-centric — and for good reason: Deribit is still the dominant
> crypto options venue by OI. But CME represents **US institutional and regulated flow**, a
> wholly different trader cohort. When CME gamma levels and Deribit levels agree, you have
> confluence across both offshore *and* regulated market-makers. This note is the complete
> guide to using CME as a complementary GEX source: what they list, how the math adjusts,
> where free data lives, and exactly what degrades when you use it.

---

## 1. 📋 What CME Lists — the full product set for GEX

### 1a. Futures (the underlying for options)

| Product | Ticker | Contract Size | Settlement | Reference Rate |
|---------|--------|---------------|------------|----------------|
| Bitcoin Futures | BTC | **5 BTC** | Cash (USD) | CME CF Bitcoin Reference Rate (BRR) at 4 pm London |
| Micro Bitcoin Futures | MBT | **0.1 BTC** (1/50th of BTC) | Cash (USD) | BRR |
| Bitcoin Friday Futures | BFF | ~1 BTC equivalent | Cash (USD) | CME CF Bitcoin Reference Rate – New York Variant (BRRNY) at 4 pm ET every Friday |
| Ether Futures | ETH | 50 ETH | Cash (USD) | CME CF Ether-Dollar Reference Rate |
| Micro Ether Futures | MET | 0.1 ETH | Cash (USD) | same |

> ⚠️ **GEX-relevant spec:** the **BTC contract multiplier is 5 BTC**, not 1 BTC. When you compute dollar GEX for a CME option, contract size = 5. For MBT options it is 0.1 BTC. This is a critical difference from Deribit (where each option is on 1 BTC notional). Getting this wrong inflates or deflates your CME GEX by a factor of 5.

Sources: [CME Bitcoin Futures Contract Specs](https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/bitcoin.contractSpecs.html) · [CME Micro Bitcoin Futures Contract Specs](https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/micro-bitcoin.contractSpecs.html) · [CME Bitcoin Friday Futures Contract Specs](https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/bitcoin-friday-futures.contractSpecs.html)

### 1b. Options (the GEX input)

CME lists **three families of options on Bitcoin futures**:

| Family | Underlying | Exercise Style | Expiry Cycle | Notes |
|--------|------------|----------------|--------------|-------|
| Options on BTC Futures | 1 BTC futures contract (represents 5 BTC) | **European** — exercise only at expiration | Monthly (last Friday of month), 6 consecutive months + 2 December contracts; **also Monday–Friday weekly options** | Primary CME BTC option product |
| Options on Micro Bitcoin (MBT) | 1 MBT futures contract (0.1 BTC) | **European** (monthly); physical delivery into MBT futures | Monthly + **Tuesday/Thursday weekly options** | Smaller size, same BRR settlement chain |
| Bitcoin Friday Futures Options | BFF futures contract | European / short-dated | Expire every Friday (two consecutive Fridays listed at any time) | Very short-dated; useful for weekly GEX if OI is meaningful |

> **European style confirmed**: "All Cryptocurrency options are European-style, meaning they can only be exercised on the last day of trading; early exercise is strictly prohibited."
> Source: [FAQ: Options on Cryptocurrency Futures — CME Group](https://www.cmegroup.com/articles/faqs/frequently-asked-questions-options-on-cryptocurrency-futures.html)

**Strike spacing on BTC options**: Dependent on the futures price and expiry, strike intervals are offered at 50, 100, 500, 1,000, 5,000, and 10,000 points. Near-the-money strikes use the tighter increments; far-OTM strikes use the wider ones. ([CME Education: Options on Bitcoin Futures — Expiration Date and Strike Price](https://www.cmegroup.com/education/courses/introduction-to-bitcoin/options-on-bitcoin-futures))

**Settlement chain**: On expiry, in-the-money options deliver into **1 BTC futures contract** which then **immediately cash-settles to the BRR**. Net result is always USD cash, no physical bitcoin. For GEX purposes: the final delta hedge is in the BTC futures market, not spot or perpetual.

**Minimum tick**: $25 per option (5 points × $5/point). If option price ≤ $25, minimum tick is $5 (1 point).

---

## 2. 🏦 Why CME Matters for GEX — the institutional angle

### 2a. A completely different trader cohort

Deribit is an offshore, crypto-native venue. CME operates under CFTC regulation and requires institutional-grade compliance. The participants who **cannot** trade Deribit — US hedge funds, asset managers, pension allocators — **can** trade CME. That means CME and Deribit option books represent largely non-overlapping player bases.

From a GEX perspective: if the **same strike/level** shows up as a gamma concentration on *both* Deribit and CME, two independent populations of dealers are forced to hedge at the same price. That is genuine confluence, not a double-count of the same position.

> [!note] The institutional/regulatory divide
> Deribit derives roughly 80% of its volume and OI from institutional participants as of early 2026 (CoinLaw data, sourced from Deribit public filings). But those institutions are globally distributed. CME's institutional base is specifically **US-regulated**, with CFTC reporting requirements. The COT report (see §4) provides weekly visibility into CME positioning that has **no Deribit equivalent**.

### 2b. Relative size — honest numbers (April 2026)

| Venue | BTC Options OI | Notes |
|-------|----------------|-------|
| Deribit | ~$26.9 billion | Still the dominant offshore venue |
| IBIT (BlackRock ETF options) | ~$27.6 billion | Overtook Deribit in April 2026 |
| CME | ~$4.5–5 billion (BTC futures options; ~25,000 contracts) | ~10–15% of Deribit size |

Sources: [CoinLaw: Options Market in Crypto Statistics 2026](https://coinlaw.io/options-market-in-crypto-statistics/) · [CoinDesk: Bitcoin options open interest extends dominance (Jan 2026)](https://www.coindesk.com/markets/2026/01/13/bitcoin-options-open-interest-extends-dominance-over-futures-damping-btc-volatility)

> ⚠️ **FLAG — partially verified**: The $4.5 billion CME figure is from an external aggregator (CoinLaw) pulling December 2025 data and the ~25,000 contracts figure is inferred from April 2026 data. CME does not publish a single "options OI in USD" headline figure on a real-time basis on its free pages. Treat these as order-of-magnitude estimates, not precise current readings.

**Practical implication**: CME option OI is roughly 10–15% of Deribit's. A CME gamma wall that aligns with a Deribit wall carries meaningful extra weight; a CME wall *without* Deribit corroboration is a weaker signal. Never weight CME and Deribit equally by default — **weight by OI** (see §6).

### 2c. CME in the COT report

The CFTC publishes weekly [Commitments of Traders (COT)](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm) data for CME Bitcoin futures and options combined, broken down by trader category (commercial hedgers, non-commercial / large specs, small specs). This gives you a positioning lens with **no equivalent on Deribit**:

- **Commercial net short + rising OI** = institutional hedging supply against BTC long positions (producers / ETF issuers hedging spot holdings).
- **Large spec net long + rising OI** = momentum-driven institutional longs; squeeze risk if they flip.
- COT data lags by **~3 business days** (Tuesday positions published Friday afternoon). Use for context, not intraday levels.

Free sources: [CFTC COT page](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm) · [The Block: CME Bitcoin COTs](https://www.theblock.co/data/crypto-markets/cme-cots) · [CME QuikStrike COT tool](https://www.cmegroup.com/tools-information/quikstrike/commitment-of-traders.html)

---

## 3. 🔧 How CME Data Differs from Deribit for Computing GEX

This is the section most traders skip. The math from [[02 — The Math — Greeks to Dollar GEX (with code)]] applies — but with five critical adjustments.

### Adjustment 1: Use the futures price (F), not spot (S)

On Deribit, options are on the **BTC index** (a spot-equivalent composite). On CME, options are on **BTC futures contracts**. The correct pricing model is **Black's model (Black-76)**, not Black-Scholes, because the underlying is a forward/futures price:

$$\Gamma_{\text{Black-76}} = \frac{N'(d_1)}{F \cdot \sigma \sqrt{t}}$$

$$d_1 = \frac{\ln(F/K) + \tfrac{1}{2}\sigma^2 t}{\sigma\sqrt{t}}$$

where **F** = the current CME BTC front-month futures price (not CME CF BRR spot index), **K** = strike, **t** = time to expiry in years, **σ** = implied vol. The risk-free rate **r** drops out of the Black-76 formula entirely (the futures price already embeds carrying costs).

> **Why it matters**: During periods of elevated basis (futures premium over spot), using spot as S instead of F misinforms d₁ and gamma. When the BTC front-month futures trades at a 2–5% annualized premium over spot (typical in contango), ATM gamma can differ materially. Always pull the **live futures price** from CME (or Barchart) as F.

```python
import numpy as np
from scipy.stats import norm

def black76_gamma(F, K, t, sigma):
    """
    Gamma for a European option on a futures contract (Black-76 model).
    F: futures price (not spot)
    K: strike price
    t: time to expiry in years
    sigma: implied vol (annualized)
    """
    t = max(t, 1e-6)  # avoid div/0 at expiry
    d1 = (np.log(F / K) + 0.5 * sigma**2 * t) / (sigma * np.sqrt(t))
    return norm.pdf(d1) / (F * sigma * np.sqrt(t))
```

### Adjustment 2: Map to the correct futures contract month

CME lists up to 6 monthly BTC option expiries simultaneously. Each monthly option is on its *own* futures month:
- The December 2026 option → underlying is the December 2026 BTC futures contract.
- The front-month option → front-month futures price.

You must use **the price of the corresponding futures contract** as F, not a single spot price. As you approach a quarterly expiry the front/back spread can be non-trivial.

```python
# Pseudo-mapping: for each CME option row, look up its futures month price
option_to_futures_price = {
    "BTCG7": front_month_price,   # Feb 2027 option → Feb 2027 futures
    "BTCZ6": dec_2026_price,      # Dec 2026 option → Dec 2026 futures
}
F = option_to_futures_price[option.contract_month]
```

### Adjustment 3: Contract size multiplier = 5 (BTC), 0.1 (MBT)

Dollar GEX formula (per-1%-move convention) becomes:

$$\text{GEX}_{\text{strike}} = \Gamma_{\text{Black-76}} \times OI \times \underbrace{5}_{\text{BTC contract size}} \times F^2 \times 0.01$$

For MBT options: replace 5 with 0.1. Do not mix BTC and MBT options in the same GEX sum without normalizing to a common BTC notional.

### Adjustment 4: European exercise means no early-assignment delta-hedging

On Deribit (also European), this is the same. But confirm: CME BTC options are **unambiguously European** (confirmed above). No early exercise, so no early-assignment gamma spikes the day before expiry that you'd see with American-style equity options.

### Adjustment 5: Expiry calendar ≠ Deribit

Deribit concentrates OI in specific quarterly expiries (last Friday of March/June/September/December) plus monthly last-Fridays and some daily/weekly. CME also uses last-Friday monthly expiries *plus* daily or Mon–Fri weekly options. When aligning GEX profiles across both venues:

- Match on **calendar date**, not "front-month." A CME June 2026 expiry (last Friday June) will align with the Deribit June 2026 expiry.
- Weekly CME options (Mon–Fri) expire into the **front-month futures** which then cash-settles immediately. Their OI tends to be small but spikes in the week of their expiry.

---

## 4. 💾 Data Access — the honest map (free vs paid)

### 4a. Free / cheap tier

| Source | What you get | Delay | Per-strike OI? | Per-strike greeks? | Notes |
|--------|-------------|-------|----------------|-------------------|-------|
| [CME Bitcoin Options Quotes](https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/bitcoin.quotes.options.html) | Live option chain (bid/ask/last, volume, OI by strike) | ~10 min (CME delayed quote tier) | ✅ Yes | ⚠️ Delta shown; gamma not explicit | Requires free CME account |
| [CME QuikStrike — OI Heatmap](https://www.cmegroup.com/tools-information/quikstrike/open-interest-heatmap.html) | OI by strike × expiry, heatmap + matrix views | Prior day (EOD) | ✅ Yes, visually | ❌ No greeks | Free tool on CME site; browser-only, no API |
| [CME QuikStrike — OI Profile](https://www.cmegroup.com/tools-information/quikstrike/options-open-interest-profile.html) | OI distribution profile with IV skew overlay | EOD | ✅ Yes | IV only (no gamma) | Free; browser-only |
| [CME Daily Settlements](https://www.cmegroup.com/market-data/daily-settlements.html) | Settlement prices per strike for all listed options; includes settlement IV for some products | EOD (published after 4 pm CT) | ✅ Yes (by strike) | ❌ Greeks not in settlement file; IV is present | Free download; CSV format possible |
| [CME Final Settlements](https://www.cmegroup.com/market-data/final-settlements.html) | Expiry-day settlement prices | On expiry | ✅ Yes | ❌ No | Free |
| [CME CVOL / CME CF Bitcoin Volatility Index (BVX)](https://www.cmegroup.com/market-data/cme-group-benchmark-administration/cme-group-volatility-indexes.html) | Aggregate 30-day implied vol index derived from CME BTC options; published every second 7am–4pm CT | Varies; BVX published live; historical requires CF Benchmarks license | ❌ Not per-strike | Single-number IV index | BVX is free to view on CME site; historical/embedded licensing requires CF Benchmarks contact |
| [Barchart Bitcoin Futures Options](https://www.barchart.com/futures/quotes/BT*0/options) | Full options chain: OI, volume, bid/ask, IV, delta, gamma, theta, vega by strike | 10–15 min delay | ✅ Yes | ✅ Yes (BS-computed) | **Best free per-strike greeks source**; free tier, 10–15 min delayed |
| [Barchart Volatility & Greeks tab](https://www.barchart.com/futures/quotes/BT*0/volatility-greeks) | IV skew + all greeks by strike; uses Black-Scholes (not Black-76) | 10–15 min | ✅ Yes | ✅ Yes | Note: Barchart uses BS not Black-76; minor gamma error at high-basis |
| [CFTC COT Report](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm) | Aggregated net futures + options positioning by trader category | ~3 business days (Tues positions → Friday publication) | ❌ No | ❌ No | Free; no strike detail, but valuable regime context |
| [The Block: CME BTC Options OI](https://www.theblock.co/data/crypto-markets/options/volume-and-oi-of-cme-bitcoin-options) | Aggregate CME BTC options OI + volume over time | 1 day | ❌ No (aggregate only) | ❌ No | Free for charts; data export may require subscription |

> ⚠️ **FLAG — QuikStrike data access**: CME describes QuikStrike as providing "free pricing and analytics tools." However, some QuikStrike features (especially historical data export and the "Essentials" bundle) may require a free CME login and have terms-of-service restrictions on automated/programmatic access. The OI Heatmap and OI Profile are browser-based tools — there is **no documented public API endpoint** for QuikStrike data as of June 2026. Do not attempt to scrape QuikStrike programmatically without reviewing CME's data terms.

### 4b. Paid tier

| Source | What you get | Notes |
|--------|-------------|-------|
| [CME DataMine](https://www.cmegroup.com/datamine.html) | Historical tick-level + EOD data for all CME products including Bitcoin options; delivery via S3, SFTP, API, file browser | Subscriptions from ~$105/month per dataset; 5+ years of history available; includes greeks / IV historical files |
| [CME Options Analytics REST API](https://www.cmegroup.com/market-data/greeks-and-implied-volatility-data.html) | Strike-level delta, gamma, theta, vega, rho, IV across all CME options in real-time via REST; covers crypto | Paid; self-service onboarding via CME data API portal or contact CME Data Sales; confirmed to cover crypto asset class |
| CME MDP 3.0 feed | Real-time market data platform; BTC options on Channel 319, BTC futures on Channel 326 | Requires CME market data license; broker/vendor distribution |
| Licensed vendors | Bloomberg, Refinitiv, Interactive Brokers, FactSet, Cboe Datashop | Resell CME data with varying depth; IB provides real-time if you have a funded CME account |

> [!note] The free-data verdict for building a CME GEX map
> The practical answer: **Barchart is your best free EOD/delayed source**. It gives you per-strike OI + BS-computed gamma (10–15 min delayed) with no account required. Combining Barchart's greeks with CME settlement IV from the daily settlement file gets you an end-of-day CME GEX map. Real-time intraday CME GEX requires paid access (CME Options Analytics API or a live brokerage feed).

---

## 5. 🍳 A Practical Free-Data Recipe — EOD CME BTC GEX Map

This is an end-of-day snapshot approach. It is **not** intraday. Data is T+0 settlement (published ~5–6 pm CT) plus Barchart's 10–15 min delayed chain.

### Step 1 — Pull live futures price

```python
import requests

# Barchart free delayed quote for front-month BTC futures
# Ticker convention on Barchart: BT*0 = continuous front-month
# For a specific month: BTM26 = June 2026

BARCHART_URL = "https://www.barchart.com/futures/quotes/BT*0/options"
# NOTE: Barchart has no free public JSON API for options chain as of 2026.
# Their free data is HTML-rendered. Use their paid API ($99+/mo) for programmatic access.
# Workaround: use CME's own delayed quote page or a free broker API (e.g., Interactive Brokers
# paper account) to get the futures price.

# For the free recipe we use CME settlement price published each day at ~5:30 pm CT:
# https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/bitcoin.settlements.html
# This is a webpage but the underlying data is accessible via CME DataMine or can be
# screen-parsed from the settlements page.

F = 105000.0  # replace with today's CME BTC front-month settlement price
```

### Step 2 — Pull per-strike OI and settlement IV

```python
# CME publishes daily settlement prices per strike at:
# https://www.cmegroup.com/market-data/daily-settlements.html
# The settlement file includes: product, expiry, put/call, strike, settlement price, IV (for some products)
# Format: CSV / downloadable from the CME settlements page (free, requires navigation)
# ⚠️ FLAG: CME does NOT currently provide settlements for option strikes that have
# not traded that day and have no open interest. Low-OI wings are missing.
# Source: CME Access to Settlement Data FAQ

# After downloading/parsing, you have:
# df columns: ['expiry', 'put_call', 'strike', 'settlement_price', 'settlement_iv', 'oi']
# Note: OI in the settlement file is as of prior day's close (T-1), not same-day.
```

### Step 3 — Compute gamma using Black-76

```python
import numpy as np
from scipy.stats import norm
import pandas as pd

def black76_gamma(F, K, t, sigma):
    t = max(t, 1e-8)
    d1 = (np.log(F / K) + 0.5 * sigma**2 * t) / (sigma * np.sqrt(t))
    return norm.pdf(d1) / (F * sigma * np.sqrt(t))

def time_to_expiry_years(expiry_date, today):
    """Calendar days / 365 (simplified; use 252 trading days if preferred)"""
    return max((expiry_date - today).days / 365.0, 0.0)

# --- CME BTC options GEX (per 1% move, in USD) ---
CONTRACT_SIZE_BTC = 5.0      # BTC futures contract = 5 BTC
# CONTRACT_SIZE_BTC = 0.1   # for Micro Bitcoin (MBT) options

rows = []
for _, row in df.iterrows():
    t = time_to_expiry_years(row["expiry"], today)
    if t <= 0:
        continue  # skip expired

    sigma = row["settlement_iv"]   # use CME settlement IV directly
    # If settlement IV is missing (wings): use BVX as a flat proxy — this is a rough
    # approximation; ideally interpolate from available strikes.
    if pd.isna(sigma) or sigma <= 0:
        sigma = bvx_today / 100.0  # BVX in percent → decimal

    # Use the futures price for the correct contract month (not a single spot price)
    F_month = futures_prices.get(row["expiry"].strftime("%b%y"), F)

    gamma = black76_gamma(F_month, row["strike"], t, sigma)

    # Dollar GEX per 1% move
    dollar_gex = gamma * row["oi"] * CONTRACT_SIZE_BTC * F_month**2 * 0.01

    # Naive sign convention: call = +, put = −
    sign = 1 if row["put_call"] == "C" else -1

    rows.append({
        "strike": row["strike"],
        "expiry": row["expiry"],
        "gex": dollar_gex * sign
    })

gex_df = pd.DataFrame(rows)
gex_by_strike = gex_df.groupby("strike")["gex"].sum().sort_index()

# Structural levels
gamma_wall = gex_by_strike.abs().idxmax()
call_wall   = gex_by_strike[gex_by_strike > 0].idxmax()
put_wall    = gex_by_strike[gex_by_strike < 0].abs().idxmax()

# Zero-gamma interpolation (from note 02)
strikes = gex_by_strike.index.values
net     = gex_by_strike.values
s = np.sign(net)
cross = np.where(s[:-1] * s[1:] < 0)[0]
if len(cross):
    i = cross[0]
    zero_gamma = strikes[i] - net[i] * (strikes[i+1] - strikes[i]) / (net[i+1] - net[i])
else:
    zero_gamma = strikes[np.argmin(np.abs(net))]

print(f"CME EOD GEX: gamma_wall={gamma_wall}, call_wall={call_wall}, put_wall={put_wall}, zero_gamma={zero_gamma:.0f}")
```

> [!warning] What this recipe does NOT give you
> - **No intraday updates** — settlement IV is EOD only; Barchart is 10–15 min delayed.
> - **No same-day OI** — CME OI in settlement files reflects the prior close.
> - **No missing-strike coverage** — strikes with no OI and no trades that day are absent from the settlement file. This can create artificial gaps in the GEX profile at low-OI strikes.
> - **Barchart's greeks use Black-Scholes, not Black-76** — introducing a small error in gamma at high basis; negligible when basis is <1% but meaningful at 3–5% premium.
> - This is **not a Deribit replacement**. It is a daily institutional cross-check.

---

## 6. 🔀 Combining CME + Deribit — overlay and confluence

### 6a. The overlay logic

Both GEX maps share the same x-axis (BTC price in USD) and the same y-axis (dollar GEX per 1% move). They can be added if you normalize correctly:

```python
# Step 1: Build Deribit GEX by strike (from note 05 / 06 pipeline)
deribit_gex = pull_deribit_gex()   # dict: {strike: net_dollar_gex}

# Step 2: Build CME GEX by strike (recipe above)
cme_gex = dict(zip(gex_by_strike.index, gex_by_strike.values))

# Step 3: OI-weighted combination
# Weight = total absolute GEX from each venue (proportional to OI × gamma)
w_deribit = sum(abs(v) for v in deribit_gex.values())
w_cme     = sum(abs(v) for v in cme_gex.values())
total_w   = w_deribit + w_cme

all_strikes = set(deribit_gex) | set(cme_gex)
combined = {}
for k in all_strikes:
    d_gex = deribit_gex.get(k, 0)
    c_gex = cme_gex.get(k, 0)
    # Straight sum (additive — same price axis, same notional units)
    combined[k] = d_gex + c_gex

# Weights for context printing:
print(f"Deribit weight: {100*w_deribit/total_w:.1f}%  CME weight: {100*w_cme/total_w:.1f}%")
# Typical output (2026): Deribit weight: 85–90%  CME weight: 10–15%
```

### 6b. How to read agreement vs divergence

| Scenario | Interpretation |
|----------|----------------|
| **CME and Deribit gamma wall at same strike (±250 pts)** | Strong confluence — both the regulated institutional cohort and offshore market-makers have maximum hedging obligation here. Treat the level as high-conviction. |
| **CME gamma wall absent / at different strike** | Offshore book drives; the CME book has its own structure at a different level. If CME and Deribit walls are separated by >$2–3k, two competing pin/magnet zones exist; interpret the higher-OI one (almost always Deribit) as primary. |
| **CME net GEX positive, Deribit net GEX negative** | Regime divergence between cohorts — unusual and unstable. The much larger Deribit book will likely dominate; treat as a signal of transitional/noisy environment, not a clean GEX read. |
| **CME COT showing commercial net short → rising** | Institutional hedging supply building (e.g., ETF issuers shorting futures to hedge spot holdings). Bearish futures bias from the regulated cohort — adds context to any directional lean. |
| **CME zero-gamma aligns with Deribit zero-gamma** | Strong regime boundary confirmation — above/below this level has the same meaning to two independent dealer populations. |

### 6c. IBIT options — the third leg (brief mention)

As of early 2026, IBIT (BlackRock iShares Bitcoin ETF) options have surpassed Deribit in raw OI dollar terms ($27.6B vs $26.9B in April 2026). IBIT options trade on CBOE/Nasdaq, not CME. They are **on the ETF, not futures** — so the GEX math uses spot-equivalent pricing (Black-Scholes, S = IBIT NAV ≈ ~0.0001 × BTC spot). The zrack/GEX Terminal already wires in IBIT via Tradier API (see [[05 — APIs and Data Sources (Deribit etc.)]]). IBIT gamma walls are now at least as important as Deribit ones for US-hours price action.

> ⚠️ **FLAG — IBIT OI size claim**: The $27.6B figure is from CoinLaw, citing April 2026 data. Both IBIT and Deribit OI fluctuate significantly with spot BTC price. Do not assume this ordering is stable. Check current data at [The Block](https://www.theblock.co/data/crypto-markets/options) before citing.

Cross-links: [[05 — APIs and Data Sources (Deribit etc.)]] · [[07 — Trader Usage Playbook (how to use together)]] · [[13 — Accurate DIY GEX — closing the gap to paid]]

---

## 7. ⚖️ Honesty Box — what degrades on free/delayed CME data

This table is the most important part of the note for a trader deciding how much to trust a CME-derived level.

| What degrades | Specific impact | How bad? |
|--------------|-----------------|----------|
| **OI is T-1 (prior close)** | If a large option block was traded today, it's not in your CME GEX map | Moderate — intraday positioning shifts are invisible until next morning |
| **Settlement IV is EOD only** | If spot has moved 5% intraday, the IV surface has shifted; your computed gammas are wrong | Moderate — ATM gamma is most sensitive to IV; error is directional not random |
| **No per-strike data for untraded strikes** | Wings of the OI profile are missing; put wall and call wall may appear closer-in than they really are | Low (wings have low gamma anyway) to Moderate (matters if a large OTM position exists) |
| **Barchart greeks use Black-Scholes not Black-76** | At 3–5% futures basis, gamma can be off by 5–15% for strikes nearest ATM | Low-Moderate — the level locations are correct; the magnitude of hedging pressure is slightly miscalibrated |
| **10–15 min quote delay (Barchart)** | In fast-moving markets, the real futures price and IV can be $500–$1000 off; gamma profile shifts | Low for EOD use; Moderate to High if trying to use during a volatile session |
| **No real-time CME options flow** | You cannot see an aggressive option sweep (a large buyer of calls or puts) until it shows in next-day OI | High for intraday — exactly the kind of trade that shifts a wall is invisible to you |
| **COT delay of ~3 days** | Positioning data is stale during fast-moving markets; a large commercial hedge built Monday is invisible until Friday | Low for strategic context; irrelevant for intraday |

**Bottom line**: a free-data CME GEX map is a **morning-brief tool** — set it up before the session opens using prior-day settlement data, treat CME levels as ~EOD-accurate, and upgrade to real-time only if you take the CME Options Analytics REST API or a live brokerage feed.

> Do NOT use a free-data CME GEX map for intraday scalping. The OI lag, the IV lag, and the missing untraded-strike gaps make it unreliable at that granularity. Use it as a daily confirmation layer alongside your Deribit dashboard.

---

## 8. 🗂️ Quick-Reference: CME vs Deribit Side-by-Side

| Dimension | **Deribit** | **CME BTC Options** |
|-----------|-------------|---------------------|
| Venue type | Offshore crypto-native | US CFTC-regulated exchange |
| Options underlying | BTC Index (spot-equivalent) | BTC Futures contract (5 BTC) |
| Exercise style | European | European |
| OI (approx, mid-2026) | $26–30B | $4–5B |
| Dominant trader cohort | Global institutional + crypto-native | US institutional, regulated |
| COT reporting | ❌ No | ✅ Yes (CFTC weekly) |
| GEX computation model | Black-Scholes with S = spot | Black-76 with F = futures price |
| Contract size for GEX | 1 BTC per option | 5 BTC (BTC) / 0.1 BTC (MBT) |
| Free per-strike OI + greeks | ✅ Deribit REST API (real-time, free) | ✅ Barchart (10–15 min delay) |
| Free real-time greeks | ✅ Yes (Deribit API) | ❌ No (paid only) |
| Settlement reference | Deribit BTC Index | CME CF BRR (or BRRNY for Fridays) |
| Expiry calendar | Quarterly + monthly + daily weeklies | Monthly (last Friday) + Mon–Fri weeklies |
| Strike spacing (near ATM) | $100 to $500 increments typical | $500 to $1,000 increments typical |
| Relative GEX weight | ~85–90% | ~10–15% |

---

### Sources (verified and cited)

- [CME Bitcoin Futures Contract Specs](https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/bitcoin.contractSpecs.html)
- [CME Micro Bitcoin Futures Contract Specs](https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/micro-bitcoin.contractSpecs.html)
- [CME Bitcoin Friday Futures Contract Specs](https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/bitcoin-friday-futures.contractSpecs.html)
- [CME Bitcoin Options Contract Specs](https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/bitcoin.contractSpecs.options.html)
- [CME Micro Bitcoin Options Contract Specs](https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/micro-bitcoin.contractSpecs.options.html)
- [FAQ: CME Options on Bitcoin Futures](https://www.cmegroup.com/trading/cryptocurrency-indices/cme-options-bitcoin-futures-frequently-asked-questions.html)
- [FAQ: Options on Cryptocurrency Futures](https://www.cmegroup.com/articles/faqs/frequently-asked-questions-options-on-cryptocurrency-futures.html)
- [CME Education: Options on Bitcoin Futures — Strike Price & Expiry](https://www.cmegroup.com/education/courses/introduction-to-bitcoin/options-on-bitcoin-futures)
- [CME QuikStrike — Open Interest Heatmap](https://www.cmegroup.com/tools-information/quikstrike/open-interest-heatmap.html)
- [CME QuikStrike — Open Interest Profile](https://www.cmegroup.com/tools-information/quikstrike/options-open-interest-profile.html)
- [CME CVOL / Volatility Indexes](https://www.cmegroup.com/market-data/cme-group-benchmark-administration/cme-group-volatility-indexes.html)
- [CF Benchmarks: CME CF Bitcoin Volatility Index (BVX) launch](https://www.cfbenchmarks.com/blog/cf-benchmarks-launches-cf-bitcoin-volatility-index-first-and-only-direct-measure-of-cme-group-bitcoin-implied-volatility)
- [CME Daily Settlements](https://www.cmegroup.com/market-data/daily-settlements.html)
- [CME Options Analytics: Greeks and Implied Volatility](https://www.cmegroup.com/market-data/greeks-and-implied-volatility-data.html)
- [CME DataMine](https://www.cmegroup.com/datamine.html)
- [CME DataMine FAQ](https://www.cmegroup.com/market-data/datamine-faq.html)
- [CFTC Commitments of Traders](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm)
- [CME QuikStrike COT Tool](https://www.cmegroup.com/tools-information/quikstrike/commitment-of-traders.html)
- [The Block: CME Bitcoin COTs](https://www.theblock.co/data/crypto-markets/cme-cots)
- [The Block: Volume and OI of CME Bitcoin Options](https://www.theblock.co/data/crypto-markets/options/volume-and-oi-of-cme-bitcoin-options)
- [Barchart: Bitcoin Futures Options Chain](https://www.barchart.com/futures/quotes/BT*0/options)
- [Barchart: Bitcoin Futures Volatility & Greeks](https://www.barchart.com/futures/quotes/BT*0/volatility-greeks)
- [CoinLaw: Options Market in Crypto Statistics 2026](https://coinlaw.io/options-market-in-crypto-statistics/)
- [CoinDesk: Bitcoin options open interest extends dominance (Jan 2026)](https://www.coindesk.com/markets/2026/01/13/bitcoin-options-open-interest-extends-dominance-over-futures-damping-btc-volatility)
- [CME: Understanding Micro Crypto Options](https://www.cmegroup.com/education/courses/micro-bitcoin-basics/understanding-options-on-micro-bitcoin-and-micro-ether-futures.html)
