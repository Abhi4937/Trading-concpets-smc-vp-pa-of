/**
 * screenerService.js — Build enriched stock objects from live Dhan data
 *
 * For each watchlist symbol this module:
 *   1. Batches all quote requests in a single POST (Dhan allows up to 1000 per call)
 *   2. Fetches ~20 daily candles per symbol (concurrency-limited to 4 at a time)
 *   3. Fetches today's 1-min intraday candles per symbol (same concurrency limit)
 *   4. Computes VWAP, OR high/low, relVol, pdh/pdl, spark, rsRank
 *   5. Runs each raw quote through enrich() from src/lib/screener.js
 *
 * Rate-limit notes (source: https://dhanhq.co/docs/v2/ overview):
 *   Quote APIs  : 1 req/s, unlimited/day
 *   Data APIs   : 5 req/s, 100,000 req/day
 *   We fetch 1 batch quote (1 req) + ~33×2 history calls (66 reqs).
 *   History calls are throttled to HISTORY_CONCURRENCY=4 with HISTORY_DELAY_MS=250 ms
 *   between slots, keeping us well under 5 req/s.
 *
 * Market-closed / missing-data handling:
 *   - If intraday returns no candles (market closed or pre-market), we fall back
 *     to the last daily candle for open/high/low/close and synthesise safe defaults
 *     for OR levels and VWAP. The symbol is still included — never thrown.
 *   - If a symbol has no daily history, it is skipped (logged as a warning).
 */

import { getQuotes, getDailyHistory, getIntraday } from './dhanClient.js';
import { SYMBOL_META, NIFTY_INDEX } from './instruments.js';
// enrich() lives in the frontend lib — but the project is "type":"module" and
// the path is relative to the project root, so we can import it directly.
// This ensures live classification is byte-for-byte identical to the frontend.
import { enrich } from '../src/lib/screener.js';

const HISTORY_CANDLES   = 22;   // ~20 trading days + a small buffer
const HISTORY_CONCURRENCY = 4;  // max parallel history requests
const HISTORY_DELAY_MS  = 250;  // delay between concurrency slots (ms)
const OR_MINUTES        = 15;   // Opening Range = first 15 × 1-min candles
const SPARK_LEN         = 30;   // sparkline length

// ── Date helpers ─────────────────────────────────────────────────────────────

function todayStr() {
  return new Date().toISOString().slice(0, 10); // "YYYY-MM-DD"
}

function daysAgoStr(n) {
  const d = new Date();
  d.setDate(d.getDate() - n);
  return d.toISOString().slice(0, 10);
}

/**
 * Format a date string as Dhan intraday fromDate/toDate: "YYYY-MM-DD HH:mm:ss"
 * For today's session we span 09:00 – 16:00 IST.
 */
function intradayRange() {
  const today = todayStr();
  return { fromDate: `${today} 09:00:00`, toDate: `${today} 16:00:00` };
}

// ── Concurrency helpers ───────────────────────────────────────────────────────

async function delay(ms) {
  return new Promise(r => setTimeout(r, ms));
}

/**
 * Run an array of async tasks with a max concurrency limit.
 * Inserts a small delay between slots to respect rate limits.
 */
async function withConcurrency(tasks, concurrency, delayMs) {
  const results = new Array(tasks.length);
  let index = 0;

  async function worker() {
    while (index < tasks.length) {
      const i = index++;
      results[i] = await tasks[i]().catch(err => ({ __error: err }));
      if (delayMs > 0) await delay(delayMs);
    }
  }

  const workers = Array.from({ length: Math.min(concurrency, tasks.length) }, worker);
  await Promise.all(workers);
  return results;
}

// ── Computation helpers ───────────────────────────────────────────────────────

/**
 * VWAP = Σ(typicalPrice × volume) / Σ(volume)
 * typicalPrice = (high + low + close) / 3
 * Computed over all intraday candles for today.
 */
function computeVwap(intraday) {
  if (!intraday || intraday.close.length === 0) return null;
  const { high, low, close, volume } = intraday;
  let cumTpv = 0, cumVol = 0;
  for (let i = 0; i < close.length; i++) {
    const tp = (high[i] + low[i] + close[i]) / 3;
    cumTpv += tp * volume[i];
    cumVol += volume[i];
  }
  return cumVol > 0 ? cumTpv / cumVol : null;
}

/**
 * Opening Range: high and low of the first OR_MINUTES × 1-min candles.
 * If fewer candles exist (pre-market or very early), uses whatever is available.
 */
function computeOR(intraday) {
  if (!intraday || intraday.close.length === 0) return { orHigh: null, orLow: null };
  const n = Math.min(OR_MINUTES, intraday.high.length);
  let orHigh = -Infinity, orLow = Infinity;
  for (let i = 0; i < n; i++) {
    if (intraday.high[i] > orHigh) orHigh = intraday.high[i];
    if (intraday.low[i]  < orLow)  orLow  = intraday.low[i];
  }
  return { orHigh: isFinite(orHigh) ? orHigh : null, orLow: isFinite(orLow) ? orLow : null };
}

/** Previous trading day high/low from the daily candle array (second-to-last entry). */
function computePDHL(daily) {
  if (!daily || daily.close.length < 2) return { pdh: null, pdl: null };
  const idx = daily.close.length - 2; // last entry = today (partial), second-to-last = prev day
  return { pdh: daily.high[idx], pdl: daily.low[idx] };
}

/**
 * relVol = today's cumulative volume / average daily volume over the last N daily candles.
 *
 * ⚠️  KNOWN LIMITATION: this understates relVol early in the session because
 * today's intraday volume is partial while avgDailyVol is a full-day average.
 * A proper intraday-time-normalised relVol would divide avgDailyVol by the
 * fraction of the session elapsed first, but that requires knowing session length.
 */
function computeRelVol(todayIntradayVol, daily) {
  if (!daily || daily.volume.length < 2) return 1;
  // Use all but the last daily candle (which may be today's incomplete bar)
  const historicalVols = daily.volume.slice(0, -1);
  if (historicalVols.length === 0) return 1;
  const avgVol = historicalVols.reduce((s, v) => s + v, 0) / historicalVols.length;
  return avgVol > 0 ? todayIntradayVol / avgVol : 1;
}

/** Last SPARK_LEN intraday close prices for the sparkline. */
function computeSpark(intraday) {
  if (!intraday || intraday.close.length === 0) return [];
  const closes = intraday.close;
  return closes.slice(Math.max(0, closes.length - SPARK_LEN));
}

/**
 * rsRank = percentile rank (1–100) of (stock%chg − NIFTY%chg) across the universe.
 * A stock at rank 90 outperforms 90% of the universe relative to the index.
 */
function computeRsRanks(relativeReturns) {
  // relativeReturns: array of { symbol, relRet } sorted in any order
  const sorted = [...relativeReturns].sort((a, b) => a.relRet - b.relRet);
  const n = sorted.length;
  const ranks = new Map();
  sorted.forEach((item, i) => {
    ranks.set(item.symbol, Math.round(((i + 1) / n) * 100));
  });
  return ranks;
}

// ── Main service function ─────────────────────────────────────────────────────

/**
 * buildScreenerData(resolvedSymbols)
 *
 * @param {{ symbol, securityId, exchangeSegment, instrument }[]} resolvedSymbols
 *   Instruments from instruments.js::resolveWatchlist()
 * @returns {Promise<{ symbol, name, sector, ltp, ... }[]>}  Array of enrich()ed quotes
 */
export async function buildScreenerData(resolvedSymbols) {
  if (resolvedSymbols.length === 0) throw new Error('No resolved symbols');

  const today = todayStr();
  const fromDaily = daysAgoStr(HISTORY_CANDLES * 2); // buffer for weekends/holidays

  // ── 1. Batch quote request ─────────────────────────────────────────────────
  // Group by exchange segment
  const securitiesBySegment = {};
  for (const { securityId, exchangeSegment } of resolvedSymbols) {
    if (!securitiesBySegment[exchangeSegment]) securitiesBySegment[exchangeSegment] = [];
    securitiesBySegment[exchangeSegment].push(Number(securityId));
  }
  // Also add the NIFTY 50 index for RS calculation
  const niftySeg = NIFTY_INDEX.exchangeSegment;
  if (!securitiesBySegment[niftySeg]) securitiesBySegment[niftySeg] = [];
  securitiesBySegment[niftySeg].push(Number(NIFTY_INDEX.securityId));

  const quoteData = await getQuotes(securitiesBySegment);

  // Helper: extract quote for a given segment + securityId
  function getQuoteEntry(exchangeSegment, securityId) {
    const key = `${exchangeSegment}:${securityId}`;
    return quoteData[key] ?? quoteData[securityId] ?? null;
  }

  // ── 2. NIFTY index quote for RS baseline ──────────────────────────────────
  const niftyQuote = getQuoteEntry(NIFTY_INDEX.exchangeSegment, NIFTY_INDEX.securityId);
  const niftyPrevClose = niftyQuote?.ohlc?.close ?? niftyQuote?.last_price ?? 0;
  const niftyLtp       = niftyQuote?.last_price ?? 0;
  const niftyChgPct    = niftyPrevClose > 0
    ? ((niftyLtp - niftyPrevClose) / niftyPrevClose) * 100
    : 0;

  // ── 3. History + intraday per symbol ──────────────────────────────────────
  const { fromDate: intFrom, toDate: intTo } = intradayRange();

  const historyTasks = resolvedSymbols.map(({ symbol, securityId, exchangeSegment, instrument }) =>
    async () => {
      try {
        const [daily, intraday] = await Promise.all([
          getDailyHistory(securityId, exchangeSegment, instrument, fromDaily, today),
          getIntraday(securityId, exchangeSegment, instrument, 1, intFrom, intTo),
        ]);
        return { symbol, daily, intraday };
      } catch (err) {
        console.warn(`[screenerService] History fetch failed for ${symbol}:`, err.message);
        return { symbol, daily: null, intraday: null };
      }
    }
  );

  const historyResults = await withConcurrency(historyTasks, HISTORY_CONCURRENCY, HISTORY_DELAY_MS);

  // ── 4. Assemble raw quotes + RS ranks ────────────────────────────────────
  const relativeReturns = [];
  const rawQuotes = [];

  for (let i = 0; i < resolvedSymbols.length; i++) {
    const { symbol, securityId, exchangeSegment } = resolvedSymbols[i];
    const hist = historyResults[i];

    if (hist?.__error) {
      console.warn(`[screenerService] Skipping ${symbol} (history error):`, hist.__error.message);
      continue;
    }

    const q = getQuoteEntry(exchangeSegment, securityId);
    if (!q) {
      console.warn(`[screenerService] No quote for ${symbol}, skipping`);
      continue;
    }

    const daily    = hist?.daily ?? null;
    const intraday = hist?.intraday ?? null;

    const ltp       = q.last_price ?? 0;
    const prevClose = q.ohlc?.close  ?? ltp; // Dhan sends prevClose as ohlc.close
    const open      = q.ohlc?.open   ?? ltp;
    const dayHigh   = q.ohlc?.high   ?? ltp;
    const dayLow    = q.ohlc?.low    ?? ltp;

    // VWAP: prefer intraday computed; fallback to Dhan's average_price field
    const vwapCalc = computeVwap(intraday?.close?.length ? intraday : null);
    const vwap     = vwapCalc ?? q.average_price ?? ltp;

    // OR levels
    const { orHigh, orLow } = computeOR(intraday?.close?.length ? intraday : null);

    // PDH / PDL from daily history
    const { pdh, pdl } = computePDHL(daily);

    // Today's volume from intraday candles sum (more accurate than quote volume mid-session)
    const intradayTotalVol = intraday?.volume?.reduce((s, v) => s + v, 0) ?? q.volume ?? 0;
    const relVol = computeRelVol(intradayTotalVol, daily);

    // Sparkline
    const spark = computeSpark(intraday?.close?.length ? intraday : null);

    // For RS rank computation — we need all symbols first, so store for later
    const stockChgPct = prevClose > 0 ? ((ltp - prevClose) / prevClose) * 100 : 0;
    relativeReturns.push({ symbol, relRet: stockChgPct - niftyChgPct });

    const meta = SYMBOL_META[symbol] ?? { name: symbol, sector: 'Unknown' };

    rawQuotes.push({
      symbol,
      name:    meta.name,
      sector:  meta.sector,
      ltp,
      prevClose,
      open,
      dayHigh,
      dayLow,
      vwap:       vwap   ?? ltp,
      relVol:     relVol ?? 1,
      rsRank:     0,     // filled below after ranking across universe
      orHigh:     orHigh ?? open,
      orLow:      orLow  ?? open,
      pdh:        pdh    ?? dayHigh,
      pdl:        pdl    ?? dayLow,
      spark,
      // oiChangePct: Dhan /marketfeed/quote returns oi field but not oi_day_change_pct.
      // True OI-change % needs two snapshots (yesterday vs today) or the F&O segment feed.
      // Set to 0 for now; implement with NSE_FNO data when available.
      oiChangePct: 0,
    });
  }

  // ── 5. Compute RS ranks ───────────────────────────────────────────────────
  const rsRankMap = computeRsRanks(relativeReturns);
  for (const rq of rawQuotes) {
    rq.rsRank = rsRankMap.get(rq.symbol) ?? 50;
  }

  // ── 6. Enrich via the shared screener.js logic ────────────────────────────
  return rawQuotes.map(enrich);
}
