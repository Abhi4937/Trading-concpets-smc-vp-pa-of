/**
 * dataSource.js — Swappable data layer for NSE Intraday Screener
 *
 * Tries the local Express backend (server/index.js) for live Dhan data first.
 * Falls back to sample data automatically on any failure, timeout, or 503.
 *
 * Backend: GET ${VITE_API_BASE}/api/screener
 *   → { stocks: [...enriched], source: 'live', asOf: <iso> }
 *   → 503 { error, hint }  when token is absent or Dhan returns an error
 *
 * Return shape: { stocks: EnrichedQuote[], source: 'live' | 'sample', asOf: string | null }
 *
 * ─────────────────────────────────────────────────────────────────────────────
 * HOW LIVE DATA WORKS (Dhan v2 backend — see server/)
 * ─────────────────────────────────────────────────────────────────────────────
 * 1. The Express backend (server/index.js) contacts DhanHQ v2 REST APIs:
 *      POST /v2/marketfeed/quote  — batch quote (LTP, OHLC, volume, VWAP, OI)
 *      POST /charts/historical    — daily candles (for PDH/PDL, relVol baseline)
 *      POST /charts/intraday      — 1-min candles (for VWAP, OR, spark)
 * 2. It resolves symbols via the scrip-master CSV (cached at server/instruments-cache.csv).
 * 3. After computing all derived fields it runs the same enrich() from src/lib/screener.js,
 *    so live classification is byte-for-byte identical to the sample-data path.
 * 4. The backend starts even without a token; when credentials are missing it
 *    returns HTTP 503 and this function transparently falls back to sample data.
 *
 * To activate live data:
 *   cp server/.env.example server/.env
 *   # fill DHAN_ACCESS_TOKEN and DHAN_CLIENT_ID
 *   npm run dev:all
 * ─────────────────────────────────────────────────────────────────────────────
 */

import { sampleQuotes } from '../data/sampleQuotes.js';
import { enrich }       from '../lib/screener.js';

const API_BASE = (import.meta.env.VITE_API_BASE || 'http://localhost:8787').replace(/\/$/, '');
const TIMEOUT_MS = 6000;

const SAMPLE_FALLBACK = {
  stocks: sampleQuotes.map(enrich),
  source: 'sample',
  asOf: null,
};

/**
 * fetchScreenerData()
 * Returns { stocks, source, asOf }.
 * Never throws — on any error it returns sample data.
 */
export async function fetchScreenerData() {
  try {
    const controller = new AbortController();
    const tid = setTimeout(() => controller.abort(), TIMEOUT_MS);

    let res;
    try {
      res = await fetch(`${API_BASE}/api/screener`, { signal: controller.signal });
    } finally {
      clearTimeout(tid);
    }

    if (!res.ok) {
      // 503 means backend is up but token missing or Dhan error — intended fallback
      const body = await res.json().catch(() => ({}));
      console.info(
        `[dataSource] Backend returned ${res.status} — falling back to sample data.`,
        body.hint ?? ''
      );
      return SAMPLE_FALLBACK;
    }

    const json = await res.json();
    return {
      stocks: json.stocks ?? [],
      source: json.source ?? 'live',
      asOf:   json.asOf   ?? null,
    };

  } catch (err) {
    // AbortError (timeout), network error, or parse error
    if (err.name !== 'AbortError') {
      console.info('[dataSource] Backend unreachable — falling back to sample data.', err.message);
    } else {
      console.info('[dataSource] Backend request timed out — falling back to sample data.');
    }
    return SAMPLE_FALLBACK;
  }
}
