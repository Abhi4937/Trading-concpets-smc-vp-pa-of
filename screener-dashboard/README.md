# NSE Intraday Screener

A professional-grade intraday stock screener dashboard for the Indian NSE F&O universe, built with React 18 + Vite 5 + Tailwind CSS v4.

## Quick Start

```bash
cd screener-dashboard
npm install
npm run dev
```

Open http://localhost:5173 — you should see the dark-theme dashboard with sample data showing all five setup types.

## What It Does

Scans a curated F&O universe and classifies every stock into one of five intraday setups:

| Setup | Direction | Condition |
|---|---|---|
| **Breakout** | Long | LTP > max(ORH, PDH) + above VWAP + RelVol ≥ 2× |
| **Breakdown** | Short | LTP < min(ORL, PDL) + below VWAP + RelVol ≥ 2× |
| **Fakeout** | Short/Long | Poked through level but rejected back — trapped traders |
| **Reversal ↑** | Long | Red on day but reclaimed VWAP + RS ≥ 50 + RelVol ≥ 1.5× |
| **Bounce** | Long | Pullback to VWAP (within 0.6%) in uptrend + RelVol ≥ 1.5× |

For each setup it computes:
- **Trigger / Stop / Target** (level-derived, not arbitrary)
- **R:R** (reward-to-risk ratio)
- **Signal Strength** (0–100, based on RelVol, RS rank, VWAP distance)
- **Rationale** (plain-English explanation)

## The Funnel (Vault References)

The screening logic follows the funnel described in the Intraday Stock Screener vault:

1. **"07 — Index & Stock Universe"** — F&O-listed stocks only (sufficient liquidity, real price discovery)
2. **"06 — Liquidity & Tradability Filters"** — RelVol ≥ 1.5–2× confirms institutional participation
3. **"03 — Long Scans — Breakout & Bounce"** — ORH+PDH breakout, VWAP bounce setups
4. **"05 — Reversal Scans"** — Red-day VWAP reclaim with RS strength
5. **"14 — Pre-Market Routine"** — Universe scan, mark OR levels, rank RS, flag OI changes

**Screener narrows — your order flow / volume profile / price action confirms.**

## Project Structure

```
src/
  data/sampleQuotes.js    — 32 NSE F&O stocks, internally consistent numbers
  lib/screener.js         — Pure screening functions (classify, enrich, levels)
  services/dataSource.js  — Swappable data layer (sample → live API)
  hooks/useWatchlist.js   — Watchlist persisted to localStorage
  components/
    Header.jsx            — Top bar with market regime chips
    SummaryStats.jsx      — In-play / long / short / sector / breakout counts
    FilterRail.jsx        — Search, direction, setup, sector, RelVol, RS, in-play
    StockTable.jsx        — Sortable table (6 sort keys)
    StockRow.jsx          — Individual row with sparkline, badges, levels
    SetupBadge.jsx        — Color-coded pill per setup type
    Sparkline.jsx         — SVG sparkline with gradient fill
    DetailPanel.jsx       — Full setup detail: levels, R:R, key levels, rationale
    WatchlistDrawer.jsx   — Slide-in drawer for starred stocks
    Icons.jsx             — Inline SVG icon components
```

## Swapping to Live Data

Edit `src/services/dataSource.js`. The rest of the app is unchanged — it consumes the same enriched shape from `enrich()`.

### Option 1 — Zerodha Kite Connect

```js
const res = await fetch(
  `https://api.kite.trade/quote?i=${SYMBOLS.map(s => `NSE:${s}`).join('&i=')}`,
  { headers: { Authorization: `token ${API_KEY}:${ACCESS_TOKEN}` } }
);
const json = await res.json();
// Map json.data['NSE:RELIANCE'].last_price → ltp, etc.
```

You need to separately compute:
- **RelVol** = today's volume-so-far ÷ average volume at the same time-of-day over 20 days
- **OR High/Low** = first 15-min candle from intraday bars endpoint
- **RS Rank** = relative strength vs Nifty (rolling 3-month price change percentile)

### Option 2 — Upstox v2

```js
const res = await fetch(
  `https://api.upstox.com/v2/market-quote/quotes?instrument_key=${keys.join(',')}`,
  { headers: { Authorization: `Bearer ${ACCESS_TOKEN}` } }
);
```

### Option 3 — Free / 15-min delayed

- [nsepython](https://github.com/swapniljariwala/nsepython) (unofficial NSE scraper)
- Chartink screener webhook (Pine-like conditions, 15-min delay, no code required)

## Stack

- React 18.3 · Vite 5 · Tailwind CSS v4 (via `@tailwindcss/vite` plugin)
- No chart/icon libraries — SVG sparklines and icons are written inline
- No runtime state management library — plain React hooks

## Disclaimer

This tool is for education and decision-support only. It is not financial advice. Always confirm with volume profile, order flow, and price action before entering a trade.
