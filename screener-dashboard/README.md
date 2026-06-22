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

## Live Data (Dhan)

The screener has an optional Express backend (`server/`) that pulls real-time data from the [DhanHQ v2 API](https://dhanhq.co/docs/v2/). When the backend is absent or has no token, the frontend shows sample data automatically — no configuration required just to run the UI.

### Quick setup

```bash
# 1. Install new deps (express, cors, dotenv, concurrently)
npm install

# 2. Copy env template and fill in your credentials
cp server/.env.example server/.env
# Edit server/.env:
#   DHAN_CLIENT_ID=<your client id>
#   DHAN_ACCESS_TOKEN=<your access token>

# 3. Run frontend + backend together
npm run dev:all
```

Or in two terminals:
```bash
npm run dev      # terminal 1 — Vite frontend (http://localhost:5173)
npm run server   # terminal 2 — Express backend (http://localhost:8787)
```

### Environment variables

| Variable | Required | Description |
|---|---|---|
| `DHAN_ACCESS_TOKEN` | Yes (for live data) | JWT from Dhan dashboard (Profile → DhanHQ APIs) |
| `DHAN_CLIENT_ID` | Recommended | Your Dhan client/user ID |
| `PORT` | No (default 8787) | Port for the Express backend |
| `VITE_API_BASE` | No (default http://localhost:8787) | Frontend env var pointing at the backend |

Add `VITE_API_BASE` to a root `.env` file (e.g. `.env.local`) if you change the backend port.

### How it falls back

The header badge shows **LIVE** (green) or **SAMPLE DATA** (amber). Fallback triggers when:
- `DHAN_ACCESS_TOKEN` is not set → backend returns 503
- Backend is not running → frontend fetch times out (6 s)
- Any Dhan API error (auth, subscription, rate limit) → backend returns 503

For step-by-step Dhan account setup see **[DHAN_SETUP.md](./DHAN_SETUP.md)**.

## Stack

- React 18.3 · Vite 5 · Tailwind CSS v4 (via `@tailwindcss/vite` plugin)
- No chart/icon libraries — SVG sparklines and icons are written inline
- No runtime state management library — plain React hooks

## Disclaimer

This tool is for education and decision-support only. It is not financial advice. Always confirm with volume profile, order flow, and price action before entering a trade.
