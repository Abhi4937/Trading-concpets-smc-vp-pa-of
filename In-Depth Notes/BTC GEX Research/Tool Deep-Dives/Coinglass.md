---
title: Deep-Dive — Coinglass
tags: [gex, deep-dive, coinglass, liquidation, funding-rates, open-interest, perps, futures, options, order-flow]
created: 2026-06-21
status: grounded-in-source
---

# 🔬 Deep-Dive: Coinglass

**URL:** https://www.coinglass.com/  
**API docs:** https://docs.coinglass.com/reference  
**API V4 base URL:** `https://open-api-v4.coinglass.com`  
**One line:** The most widely-used aggregator for crypto perp/futures derivatives data — liquidation heatmaps, OI, funding rates, long/short ratios, and order-book depth — across 30+ exchanges. Covers basic options metrics (OI/volume/max pain) but is **NOT a GEX engine**. Complementary to, not a substitute for, the options-GEX tools in this vault.

---

## 1. 🗺️ What Coinglass Is

Coinglass launched around 2020 as a crypto derivatives data aggregator. Its core positioning has always been **perpetual futures** — the dominant instrument for leveraged crypto speculation. It is to perp-OI/liquidation/funding what Deribit's own UI is to BTC options: the go-to first stop.

As of 2026 it has expanded into:
- Spot order-book depth and large-trade detection
- Basic options market data (OI/volume/max pain) including Deribit
- ETF flow monitoring (IBIT, FBTC, etc.)
- On-chain exchange balance data
- Hyperliquid whale tracking (decentralised perps)

> ⚠️ **Scope boundary:** The phrase "crypto derivatives analytics" covers two distinct worlds: (1) **perp/futures** — funding rates, liquidations, OI — where Coinglass is the market leader; and (2) **options** — Greeks, IV surface, GEX — where Coinglass is a surface-level tool. Do not conflate them. For options-GEX, use [[Tool Deep-Dives/Laevitas]], [[Tool Deep-Dives/Amberdata AD Derivatives]], [[Tool Deep-Dives/GammaFlip.io]], or [[Tool Deep-Dives/CryptoGamma]].

---

## 2. 📦 Full Data Product List

### 2a. Futures / Perpetuals

| Product | URL path | What it shows |
|---------|----------|---------------|
| **Liquidation dashboard** | `/liquidations` | Real-time liquidation events, long/short split, exchange breakdown |
| **Liquidation heatmap (Model 1/2/3)** | `/pro/futures/LiquidationHeatMap` | *Estimated* price zones where leveraged positions may be forced to close |
| **Liquidation history heatmap** | `/pro/futures/LiquidationCountHeatMap` | Historical count/intensity of past liquidation events by price zone |
| **Liquidation map / level map** | `/pro/futures/LiquidationHeatMapModel3` | Aggregated heatmap variant, per-coin or per-symbol |
| **Open Interest (OI)** | `/open-interest/BTC` | Aggregated OI across exchanges, OHLC candles, coin/stablecoin-margined split |
| **Funding rates** | `/FundingRate` | Current rates across exchanges, OI-weighted avg, volume-weighted avg, predicted next rate |
| **Funding rate heatmap** | `/FundingRateHeatMap` | Color-coded sentiment: dark = high positive funding (bullish crowding) |
| **Long/short ratio** | — | Top trader long/short (exchange-reported), global account ratio |
| **Taker buy/sell volume** | — | CVD-style metric: buy-initiated vs sell-initiated volume |
| **Basis / premium** | `/Basis` | Futures basis vs spot; contango/backwardation reading |
| **Crypto futures overview** | `/pro/futures/Cryptofutures` | Aggregated volume, OI, funding ranked by asset |
| **Liquidity heatmap** | `/LiquidityHeatmap` | Order-book depth visualization — **distinct from the liquidation heatmap** (see §5) |
| **Large orderbook / limit orders** | `/large-orderbook-statistics` | Large resting limit orders on spot and futures order books |
| **Whale alerts** | `/whale-alert` | Large executed trades and on-chain transfers above threshold |
| **Hyperliquid whale tracker** | `/hyperliquid` | Positions >$1M notional on Hyperliquid perps |

### 2b. Options

| Product | URL path | What it shows |
|---------|----------|---------------|
| **Options OI by strike** | `/pro/options/OIStrike` | Open interest distribution by strike — aggregated, Deribit-weighted |
| **Options OI by expiry** | `/options/Deribit` | Expiry-bucketed OI for Deribit BTC/ETH |
| **Options volume by expiry/strike** | `/options/Deribit` | Volume breakdown similar to OI |
| **Put/call ratio** | `/options/Deribit` | Simple P/C sentiment gauge |
| **Max pain** | `/options/Deribit` | Expiry-level max pain price (the strike where most options expire worthless) |
| **Option Greeks table** | `/options/Deribit` | Per-strike greeks display (vendor-claimed, display loaded partially — see note below) |

> ⚠️ **Coinglass OPTIONS CAVEAT:** The Deribit options page shows OI/volume/max pain/P-C ratio competently. It *lists* a Greeks table but the page loaded with zero values in a live check (Jun 2026), suggesting this view may require interaction or a paid tier. Crucially, **Coinglass does NOT publish a GEX (gamma exposure) dashboard or API endpoint** — it does not aggregate per-strike gamma into a GEX number. The search result claiming "CoinGlass tracks gamma exposure data" refers to a CoinEx Academy article, not a native Coinglass product. For true BTC GEX, use the dedicated tools in this vault.

### 2c. Other data layers

| Product | Notes |
|---------|-------|
| **Bitcoin ETF flows** | Daily inflow/outflow per issuer (IBIT, FBTC, GBTC, etc.) |
| **Fear & Greed Index** | Vendor-computed composite; treat as sentiment colour not signal |
| **On-chain: exchange balances** | BTC/ETH balance on exchanges; sourced from on-chain analytics aggregators |
| **Hyperliquid positions** | Decentralised perp whale positions, open P&L, leverage |

---

## 3. 🔌 Data Sources — Where It Comes From

Coinglass aggregates from **30+ centralised exchanges** (vendor-claimed, unverified exact count). The core perp/futures exchanges explicitly listed in their API documentation include:

> Binance, OKX, Bybit, Bitget, BitMEX, Kraken, Deribit (futures/options OI), Gate.io, MEXC, CoinEx, Huobi/HTX, Phemex, and others.

Key distinctions:

- **Liquidation data** — pulled from each exchange's public WebSocket liquidation stream. The quality of this data is severely limited. See §4 for the full story.
- **Open Interest** — pulled from exchange REST APIs. This is reliable and the most trustworthy number Coinglass provides.
- **Funding rates** — exchange REST API; reliable. OI-weighted and vol-weighted versions are Coinglass-computed.
- **Long/short ratios** — sourced from exchange-published "top trader" APIs (Binance, OKX, Bybit). These are not the same as aggregate market positioning; exchanges define "top traders" differently.
- **Options OI/volume** — pulled from Deribit's public REST API (`/api/v2/public/get_book_summary_by_currency`). Reliable OI numbers. Greeks not re-computed.
- **Liquidity heatmap** — sourced from live order-book snapshots (L2 market depth). Binance BTCUSDT is the default shown. Data source is real CLOB depth — but orders can be cancelled; it is a snapshot not a commitment.
- **Whale orders** — pulled from exchange order-book and trade APIs with size thresholds applied by Coinglass.

---

## 4. ⚠️ ACCURACY & METHODOLOGY — The Critical Section

### 4a. Liquidation data is ESTIMATED, not actual

This is the single most important thing to understand about Coinglass liquidation numbers.

**The mechanism:**

Binance's liquidation WebSocket stream — `forceOrder` stream, USDS-Margined Futures — is documented as follows:

> *"For each symbol, only the largest one liquidation order within 1000ms will be pushed as the snapshot. If no liquidation happens in the interval of 1000ms, no stream will be pushed."*  
> — Binance API docs ([Liquidation Order Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Liquidation-Order-Streams))

This means: **in any given second, only the single largest liquidation per symbol is broadcast**. During high-volatility cascades — when exchanges may be processing dozens or hundreds of liquidations per second per pair — the vast majority are silently dropped from the public feed.

**The scale of the problem:**

Coinglass itself publicly flagged this on **10–11 October 2025**, during the largest liquidation cascade in crypto history (triggered by Trump's surprise 100%-China-tariff announcement, days after BTC set an all-time high above $126k):

> *"The largest liquidation event in crypto history. In the past 24 hours, 1,618,240 traders were liquidated, with a total liquidation amount of $19.13 billion. The actual total is likely much higher — #Binance only reports one liquidation order per second."*  
> — Coinglass official X/Twitter ([source](https://x.com/coinglass_com/status/1976796969961193641))

During that event **Coinglass estimated Binance's reported liquidations were 10–20× too low** (amplified by analysts e.g. "Marty Party"), and Hyperliquid co-founder **Jeff Yan** said the under-reporting "could easily be **100×** under some conditions." This is long-standing, not new: **Vetle Lunde (K33 Research)** has called exchange liquidation data "bogus" and a "vast underrepresentation… wildly underreported," dating the break to Binance's **1-push-per-second throttle introduced April 2021** (Bybit followed September 2021).

**Other exchanges:** Bybit and others have similar constraints on their public liquidation streams. No major CEX provides a complete, unthrottled public liquidation feed.

**Consequence for traders:**

| What you see on Coinglass | What it actually means |
|---------------------------|------------------------|
| "$500M liquidated in 1 hour" | A **floor estimate**. Real number could be 5–20× higher on a volatile day |
| Real-time liquidation feed | Events with <1s resolution are missing; large cascades are severely under-counted |
| Exchange liquidation rankings | Relative ordering may be meaningful; absolute numbers are not |
| Historical liquidation chart | Useful for *pattern* (which days had large events) not *magnitude* |

> ✅ **What to use it for:** Identifying *that* a significant liquidation event occurred (direction, rough timing, which exchange led). **Not** for measuring exact liquidation volume in dollars.

---

### 4b. The Liquidation Heatmap — a Model, Not a Record

The liquidation heatmap (Coinglass has three models) is the most misunderstood product on the platform. Here is precisely what it is:

**What it IS:**
A forward-looking **estimated model** of where leveraged positions are concentrated. It does NOT record where past liquidations happened (that is the separate "Liquidation History Heatmap"). It projects: *if price moves to level X, how many positions are likely to be forcibly closed?*

**How it is built (inferred from Coinglass documentation):**
1. Track where OI builds up over recent history (e.g. the past 3 months).
2. Apply leverage tier assumptions: a trader long at $60k with 10× leverage gets liquidated at ~$54k; at 20× at ~$57k. Coinglass maps the known leverage tier distributions to estimate the concentration of liquidation prices.
3. Weight by volume and time recency.
4. Render as a heatmap — bright yellow = dense estimated liquidation cluster, purple = sparse.

**Coinglass's own admission:** *"The actual liquidation amounts that occur may be lower than the levels shown on the heatmap."* (Coinglass learn article, [source](https://www.coinglass.com/learn/how-to-use-liqmap-to-assist-trading-en))

**Failure modes:**

| Scenario | Why the model breaks |
|----------|---------------------|
| Position sizes shifted via delta-hedging or partial close | Model didn't see those OI changes |
| Exchange changes leverage tier defaults | Model liquidation prices shift systematically |
| OB-heavy institutional positions (no leverage) | Inflate OI without adding liquidation risk |
| Market structure gap (fast move through a zone) | Positions liquidated without "touching" the heatmap zone in the normal sense |
| Stale heatmap (not auto-refreshed on free tier) | Zone was valid 2 hours ago, not now |

**How to read it correctly:**
- Treat bright zones as **price magnets**: if price approaches, there is elevated probability of cascade (forced sells hitting longs below spot, forced buys hitting shorts above).
- The heatmap is a **probabilistic gravity map**, not a deterministic stop-hunt map.
- Zones work best as confluence — combine with VP (POC/HVN/LVN), OI spike levels, VWAP, and GEX walls.
- **Timeframe**: use the 3-month view for swing context, 1-month for intraday confluence.
- Do NOT read a dense heatmap zone as meaning "price WILL go there". Markets regularly skip over or fail to reach prominent zones.

> **Three model variants:** Model 1 is coin-aggregated (all BTC perp venues). Model 2 is the same but per trading pair. Model 3 is the "aggregated symbol" view. The differences are primarily in aggregation scope; the underlying estimation methodology is the same across all three.

---

### 4c. The Liquidity Heatmap — Order-Book Depth (Different Tool)

**People constantly confuse the liquidation heatmap and the liquidity heatmap.** They are entirely different data sources.

| | Liquidation Heatmap | Liquidity Heatmap |
|--|---------------------|-------------------|
| **Data source** | Estimated model from OI + leverage tiers | Live L2 order-book snapshots (real bids/asks) |
| **What it shows** | Where *forced* position closures may occur if price moves there | Where *limit orders* are resting in the order book right now |
| **Forward vs backward** | Forward-looking model | Real-time snapshot of current book |
| **Reliability** | Estimated (model) | Real but impermanent (orders cancel) |
| **Coinglass URL** | `/pro/futures/LiquidationHeatMap` | `/LiquidityHeatmap` |
| **Default exchange** | Aggregated across venues | Binance BTCUSDT (spot) |

**Reading the Liquidity Heatmap:**
- Lighter/brighter zones = larger resting limit orders = natural support/resistance.
- Price tends to either stall at dense zones (absorption) or accelerate through them if a large order is "swept."
- **Critical caveat:** large limit orders on exchange order books can be spoofed (placed then cancelled immediately). The heatmap shows historical density of orders, not a live guarantee they are still there. Treat large walls as *context*, not certainty.
- For a deeper treatment of CLOB mechanics, aggressor vs passive flow, and how order-book structure drives price, see the note on [[11 — Real-Time Dealer Positioning — CLOB Aggressor vs Block-OTC trades]].

---

## 5. 🐳 Large Trade / Whale Indicators

Coinglass has multiple "whale" tracking layers. They mean different things:

### Large Limit Orders (order book)
- **Source:** Live order-book snapshot from Binance, OKX, Bybit, others
- **Thresholds (documented):** Futures: BTC ≥ $1M, ETH ≥ $500K, others ≥ $50K. Spot: BTC ≥ $350K, ETH ≥ $250K, others ≥ $10K
- **What it means:** A large resting limit order at a specific price. Shows intent to buy or sell at that level.
- **Reliability:** Moderate. Real orders show up; spoofed orders also show up and then vanish. Check if the level persists across multiple refreshes.

### Whale Alerts (executed trades)
- **Source:** Trade tick feed from exchange APIs, filtered by size
- **What it means:** A large trade *actually executed* — not just an order placed
- **Threshold:** Site shows Hyperliquid whale positions >$1M notional; executed trade thresholds vary by asset
- **Reliability:** Higher than limit orders — these trades happened. However they tell you *that* a large participant transacted, not *why* (could be hedge, reduce, add).

### Hyperliquid Whale Tracker
- **Source:** Hyperliquid on-chain data (all positions are public on-chain)
- **What it means:** Specific wallet addresses with large perpetual positions — you can see exact entry prices, leverage, unrealised P&L
- **Reliability:** High for position size/level (on-chain data is accurate). Low for inferring direction — large on-chain longs are often hedged off-chain.

### Large Liquidation Events
- **Source:** Exchange liquidation stream (see §4a caveats)
- **Threshold:** Coinglass highlights single-order liquidations above a threshold (e.g. >$1M BTC)
- **Reliability:** These specific *large* events are more likely to be accurately captured because the 1-per-second throttle more frequently captures the largest event when a single liquidation is itself massive. Still estimated, not complete.

> ⚠️ **The whale fallacy:** Large orders and trades are visible but their *meaning* is ambiguous. A $50M BTC buy on Binance could be an institution adding, or a hedge fund closing a short, or a delta-hedging rebalance after options expiry. Never trade on whale order size alone — always cross-reference with GEX regime, OI trend, funding rate direction, and price structure.

---

## 6. 📐 Liquidations vs Liquidity — Definitions

These two terms are used interchangeably in retail discourse and are entirely different:

### Liquidations
A **forced position close** by an exchange when a leveraged trader's margin falls below the maintenance margin threshold. The exchange's risk engine closes the position at market price to prevent negative equity.

- Caused by: adverse price move against a leveraged position
- Effect on price: adds *market orders* (sell pressure if long positions are liquidated; buy pressure if shorts) — this is what makes liquidation cascades self-reinforcing
- Data quality: severely under-reported on public feeds (see §4a)
- **How to use in a trade:** the *heatmap* shows you zones where forced selling/buying may accelerate price; use as "if price reaches X, expect momentum amplification"

### Liquidity
The presence of *limit orders* resting in an order book — willing buyers below market, willing sellers above. Liquidity is what absorbs market orders.

- Caused by: market makers, passive traders, algorithmic order placement
- Effect on price: *absorbs* moves (large bid wall slows down selling pressure)
- Data quality: real but ephemeral (orders cancel freely)
- **How to use in a trade:** the *liquidity heatmap* shows you thick zones where price is likely to stall or reverse; use as "if price approaches X, watch for absorption or sweep"

**The relationship:** liquidation events *consume* liquidity (a cascade of forced market orders eats through the order book). This is why large liquidation heatmap zones often correspond to thin liquidity (the positions there haven't been cleared yet) or to prior high-liquidity areas that attract stops.

---

## 7. 🔌 Access — Free Tier, Prime, and API

### Website (free)
The free web dashboard gives you access to most of the heatmap visualisations in a limited form:
- BTC and ETH liquidation heatmaps (6-month and 12-month views)
- OI charts, funding rates, long/short ratios — all free
- Options OI/volume/max pain — free
- Manual refresh (no auto-update) on free tier heatmaps

### Coinglass Prime ($28/month, ~$268/year)
Unlocks the full liquidation heatmap experience:
- All three heatmap models (not just BTC/ETH — all available coins)
- Extended time ranges: 6-month, 12-month, **24-month+** views
- **Automatic real-time refresh** (eliminates manual reload)
- Web only as of Jun 2026; mobile app support planned

### API V4 (no free tier — API access is paid)
Base URL: `https://open-api-v4.coinglass.com`  
Authentication: header `CG-API-KEY: <your_key>`  
No free trial/sandbox tier is advertised as of 2026.

| Tier | Price | Rate limit | Historical data (1-min bars) | Commercial use |
|------|-------|------------|------------------------------|----------------|
| **Hobbyist** | $29/mo | 30 req/min | 6 days | No |
| **Startup** | $79/mo | 80 req/min | ~30 days | No |
| **Standard** | $299/mo | 300 req/min | 90 days | Yes |
| **Professional** | $699/mo | 1,200 req/min | 180 days | Yes + priority support |
| **Enterprise** | Custom | Custom | Full history | Yes + bulk/CSV + dedicated support |

> Note: "Daily interval" data (1-day bars) appears to be available at all tiers. Only sub-daily resolution is gated by tier. (Pricing sourced from coinglass.com/pricing, Jun 2026.)

### Key API Endpoints (V4)

```
# Open Interest
GET /api/futures/openInterest/ohlc-history
  params: exchange, symbol, interval, startTime, endTime

# Funding Rate (OHLC)
GET /api/futures/fundingRate/ohlc-history
  params: exchange, symbol, interval

# OI-Weighted Funding Rate
GET /api/futures/fundingRate/oi-weight-history

# Liquidation Heatmap (Model 2)
GET /api/futures/liquidation/heatmap/model2
  params: symbol, range  (range: 3=3mo, 6=6mo, 12=12mo)

# Liquidation Heatmap (Model 3 — aggregated coin)
GET /api/futures/liquidation/heatmap/model3
  params: coin, range

# Liquidation Order (past 7 days)
GET /api/futures/liquidation/order
  params: exchange, symbol, startTime, endTime

# Liquidation Max Pain
GET /api/futures/liquidation/max-pain
  (potential pressure zones between current and liquidation prices)

# Large Limit Orders (order book)
GET /api/spot/orderbook/large-order
GET /api/futures/orderbook/large-order

# Options: Max Pain
GET /api/option/max-pain

# Options: Exchange OI History
GET /api/option/exchange-list/open-interest-history
  params: exchange=Deribit, currency=BTC

# Options: Exchange Volume History
GET /api/option/exchange-list/vol-history

# Long/Short Ratio
GET /api/futures/globalLongShortAccountRatio/history

# Taker Buy/Sell Volume
GET /api/futures/taker-buy-sell-vol/history
```

All responses are JSON. WebSocket streams are available for real-time liquidation orders and trade executions. Full OpenAPI spec: https://docs.coinglass.com/llms.txt

---

## 8. 🔄 Similar Platforms — Comparison Table

| Platform | Primary strength | Liquidation data | Options/GEX | Free tier | Notable |
|----------|-----------------|-----------------|-------------|-----------|---------|
| **Coinglass** | Perp OI, funding, liquidation heatmap | Estimated (throttled feeds), heatmap model | OI/vol/max pain only — no GEX | Yes (web); No (API) | Market leader for perp derivatives; Prime $28/mo |
| **Coinalyze** | Aggregated OI + funding, clean UI | Aggregated liquidations, basic charts | No | Yes (limited) | Good free alternative for OI/funding; no heatmap |
| **CoinAnk** | Liquidation heatmap + map, OI, funding | Similar to Coinglass (also estimated) | No | Yes (free app) | Solid free alternative; less history depth |
| **Hyblock Capital** | Predictive liquidation heatmap | Proprietary weighted algorithm | No | Unknown (website blocked for review) | Claims superior heatmap methodology; targets professionals |
| **Velo Data** | Institutional derivatives dashboard | OI, funding, basis | No GEX | Paid (institutional) | Real-time unified dashboard; used by hedge funds; pricing opaque |
| **[[Tool Deep-Dives/Laevitas]]** | Options analytics + GEX + REST API | No liquidation data | Full GEX with history + API | Free view; $50/mo for API | Best paid all-rounder for options/GEX |
| **[[Tool Deep-Dives/Amberdata AD Derivatives]]** | True dealer-positioning GEX | No liquidation data | Deepest options/GEX available | No (enterprise) | Most sophisticated GEX; very expensive |
| **Aggr.trade** | Real-time trade tape audio alerts | Live feed of large liquidation events | No | Free (open source) | Best for real-time liquidation *sound alerts* during trades |
| **Kingfisher** | Order-book heatmap (liquidity) | No | No | No ($70+/mo) | Best pure liquidity/CLOB depth heatmap |

> **For liquidation specifically:** During normal conditions, Coinglass and CoinAnk are equivalent (same throttled source data). During high-volatility events, **all platforms under-report** because the exchanges throttle at the source. There is no hosted platform that shows true unthrottled liquidation data for Binance or OKX — it simply isn't made public.

---

## 9. 🎯 How This Fits the GEX Workflow

Coinglass is a **perp/futures positioning layer**, not a GEX tool. It answers different questions:

| Layer | Question answered | Tool |
|-------|-------------------|------|
| Options GEX | Where are gamma walls? What regime are dealers in? | [[Tool Deep-Dives/CryptoGamma]], [[Tool Deep-Dives/GammaFlip.io]], [[Tool Deep-Dives/Laevitas]] |
| Perp OI / funding | How levered is the market? Is funding extreme? Which side is crowded? | **Coinglass** |
| Liquidation zones | If price moves to X, is there a cascade risk? | **Coinglass** liquidation heatmap |
| Order-book depth | Where are large limit orders resting right now? | **Coinglass** liquidity heatmap / Kingfisher |
| Whale positioning | Who is carrying outsized perp exposure right now? | **Coinglass** Hyperliquid tracker, whale alerts |

**Practical stack integration:**
1. Use the GEX tools to establish the **options-dealer regime** (positive GEX = pinning, negative = trending) — see [[07 — Trader Usage Playbook (how to use together)]].
2. Cross-check Coinglass **funding rate**: if GEX is positive (fade bias) AND funding is deeply negative (shorts overpaying) → fade with conviction. If funding is deeply positive AND GEX is negative → momentum long is crowded; expect violent reversals.
3. Check Coinglass **OI trend**: rising OI + rising price = longs adding (strong trend); rising OI + falling price = shorts adding (strong downtrend). Falling OI in a move = short/long covering, not new positioning.
4. Mark the liquidation heatmap's bright zones on your chart as secondary confluence — they work like "hidden S/R" that the market gravitates toward. Do NOT use them as primary triggers.
5. On **expiry days** (especially Deribit 08:00 UTC), overlay the options max pain level from Coinglass with the GEX pin level — if they converge, pin risk is high.

> **The perp-options feedback loop:** Large open interest in perp longs with positive funding + a large call wall on GEX at a nearby strike = dealers are short calls AND perp shorts are crowded. This creates a squeeze-and-pin dynamic: price rallies into the call wall as squeezed perp shorts cover, then stalls at the call wall as dealer hedging absorbs it. Recognising this loop requires *both* tools.

For CLOB mechanics (how order-book depth translates to price impact), aggressor classification, and block vs OTC flows — see [[11 — Real-Time Dealer Positioning — CLOB Aggressor vs Block-OTC trades]].

---

## 10. ✅ What Coinglass Is Good For / ⛔ What It Is Not

| ✅ Use it for | ⛔ Do NOT use it for |
|--------------|---------------------|
| Watching **OI** trend and magnitude across exchanges | Measuring exact liquidation dollar volume (estimated/throttled) |
| Reading **funding rates** — extreme readings are actionable signals | GEX or options dealer regime analysis |
| Getting a rough visual of **where leveraged positions may cascade** (heatmap as magnet/confluence) | Trusting heatmap zones as guaranteed liquidation levels |
| **Max pain** level on Deribit options by expiry | Per-strike GEX calculations |
| Identifying **anomalous large orders/trades** as context | Blindly following whale orders as direction |
| Cross-exchange **long/short ratio** as crowding gauge | Treating "top trader" ratio as actual market position split |
| **Free** access to most perp derivatives data | API access without paying (no free API tier) |

---

## Sources

- Coinglass main site: https://www.coinglass.com/
- API V4 docs: https://docs.coinglass.com/reference
- API pricing: https://www.coinglass.com/pricing
- Prime pricing: https://www.coinglass.com/prime
- Liquidation heatmap learn: https://www.coinglass.com/learn/how-to-use-liqmap-to-assist-trading-en
- Liquidity heatmap learn: https://www.coinglass.com/learn/liquidity-heatmap-en
- Binance liquidation stream docs: https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Liquidation-Order-Streams
- Coinglass X post on Binance 20× gap: https://x.com/coinglass_com/status/1976796969961193641
- Hyperliquid CEO / Cointelegraph: https://cointelegraph.com/news/centralized-crypto-exchanges-undrerreport-liquidadations-even-100x-hyperliquid-ceo
- API V4 review (DEV Community, 2026): https://dev.to/great-time-flies/coinglass-api-review-2026-is-it-worth-it-for-crypto-quant-traders-2bcf
- Coinglass alternatives comparison: https://www.buildix.trade/blog/coinglass-alternatives-open-interest-funding-rate-tools-2026
- Coinglass intro learn article: https://www.coinglass.com/learn/coinglass-intro-en
- Deribit options page on Coinglass: https://www.coinglass.com/options/Deribit
