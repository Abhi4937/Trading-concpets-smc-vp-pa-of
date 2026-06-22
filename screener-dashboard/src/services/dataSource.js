/**
 * dataSource.js — Swappable data layer for NSE Intraday Screener
 *
 * Current mode: SAMPLE DATA (static, for UI demo)
 *
 * ────────────────────────────────────────────────────────────────
 * HOW TO WIRE LIVE DATA
 * ────────────────────────────────────────────────────────────────
 * NSE has NO public real-time API. Your options:
 *
 * 1. Zerodha Kite Connect WebSocket + REST (/quote):
 *    - GET https://api.kite.trade/quote?i=NSE:RELIANCE&i=NSE:HDFCBANK...
 *    - Headers: Authorization: token <api_key>:<access_token>
 *    - Map response: instruments[sym].last_price → ltp, etc.
 *    - Relative volume: compare current volume vs 20-day avg vol at same time of day
 *    - WebSocket for streaming: wss://ws.kite.trade (binary OHLC packets)
 *
 * 2. Upstox v2 API:
 *    - GET https://api.upstox.com/v2/market-quote/quotes?instrument_key=NSE_EQ|...
 *    - Headers: Authorization: Bearer <access_token>
 *
 * 3. Free 15-min delayed (NSE unofficial):
 *    - nsepython library (scrapes NSE website, unofficial, fragile)
 *    - NSE bhavcopy CSV (end-of-day only, not intraday)
 *    - Chartink screener webhooks (pre-built Pine-style scans, 15-min delay)
 *
 * 4. Angel One SmartAPI / Fyers API — similar to Kite
 *
 * Vault reference: "10 — APIs (broker + data)" in the Intraday Stock Screener vault.
 *
 * ────────────────────────────────────────────────────────────────
 * TO SWAP IN LIVE DATA:
 *   Replace the body of fetchScreenerData() below with your live API call.
 *   The rest of the app consumes the same enriched shape — no other changes needed.
 *   The raw quote shape each API response must produce:
 *     { symbol, name, sector, ltp, prevClose, open, dayHigh, dayLow, vwap,
 *       relVol, rsRank, orHigh, orLow, pdh, pdl, spark: number[], oiChangePct }
 * ────────────────────────────────────────────────────────────────
 */

import { sampleQuotes } from '../data/sampleQuotes.js';
import { enrich } from '../lib/screener.js';

// ── LIVE API EXAMPLE (uncomment + fill in credentials to activate) ────────────
//
// const API_KEY = import.meta.env.VITE_KITE_API_KEY;
// const ACCESS_TOKEN = import.meta.env.VITE_KITE_ACCESS_TOKEN;
// const SYMBOLS = ['RELIANCE','HDFCBANK','ICICIBANK',...]; // full F&O list
//
// async function fetchKiteQuotes() {
//   const params = SYMBOLS.map(s => `i=NSE:${s}`).join('&');
//   const res = await fetch(`https://api.kite.trade/quote?${params}`, {
//     headers: { Authorization: `token ${API_KEY}:${ACCESS_TOKEN}` }
//   });
//   if (!res.ok) throw new Error(`Kite API error: ${res.status}`);
//   const json = await res.json();
//   return SYMBOLS.map(sym => {
//     const d = json.data[`NSE:${sym}`];
//     return {
//       symbol: sym,
//       name: SYMBOL_NAMES[sym],
//       sector: SYMBOL_SECTORS[sym],
//       ltp: d.last_price,
//       prevClose: d.ohlc.close,  // previous day close
//       open: d.ohlc.open,
//       dayHigh: d.ohlc.high,
//       dayLow: d.ohlc.low,
//       vwap: d.average_price,
//       relVol: d.volume / AVG_VOLUME_AT_THIS_TIME[sym], // need pre-computed avg
//       rsRank: RS_RANKS[sym], // need separate RS calc vs Nifty
//       orHigh: OR_HIGHS[sym], // first 15-min candle high — from intraday bars
//       orLow: OR_LOWS[sym],
//       pdh: PREV_DAY[sym].high,
//       pdl: PREV_DAY[sym].low,
//       spark: SPARKLINES[sym], // last 30 intraday ticks
//       oiChangePct: d.oi_day_change_percentage,
//     };
//   });
// }
// ─────────────────────────────────────────────────────────────────────────────

export async function fetchScreenerData() {
  // Simulate network latency for realistic UI behaviour
  await new Promise(r => setTimeout(r, 350));

  // Swap out sampleQuotes.map(enrich) for your live fetch above:
  return sampleQuotes.map(enrich);
}
