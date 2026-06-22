/**
 * dhanClient.js — Thin wrapper over the DhanHQ v2 REST API
 *
 * Uses Node built-in fetch (Node 18+). No axios.
 *
 * Verified endpoints (source: https://dhanhq.co/docs/v2/):
 *   Base URL  : https://api.dhan.co/v2
 *   Auth      : header `access-token: <JWT>`  (confirmed from auth docs)
 *               header `dhanClientId: <ID>`   (shown in some endpoint examples)
 *   Quote     : POST /v2/marketfeed/quote      — up to 1000 instruments, 1 req/s
 *   LTP       : POST /v2/marketfeed/ltp
 *   Daily hist: POST /charts/historical        — arrays open/high/low/close/volume/timestamp
 *   Intraday  : POST /charts/intraday          — interval: 1|5|15|25|60 (minutes); 90-day max window
 *   Rate limits (Data APIs): 5 req/s; 100,000 req/day (source: dhanhq.co/docs/v2/ overview)
 *   NOTE: The /v2/marketfeed/* endpoints appear to be part of the standard API —
 *         the docs do not mention a separate paid "Data API" subscription for REST quotes,
 *         but the Live Market Feed (WebSocket) may require one. Verify on your account dashboard.
 */

const BASE = 'https://api.dhan.co';

const CLIENT_ID    = process.env.DHAN_CLIENT_ID    ?? '';
const ACCESS_TOKEN = process.env.DHAN_ACCESS_TOKEN ?? '';

/** Shared headers for every request */
function authHeaders() {
  return {
    'Content-Type': 'application/json',
    'access-token': ACCESS_TOKEN,
    // dhanClientId is shown as a header in some Dhan endpoint examples.
    // We send it on every call; it's harmless if not required.
    ...(CLIENT_ID ? { 'dhanClientId': CLIENT_ID } : {}),
  };
}

/**
 * Check whether credentials are configured.
 * Call this before making API requests; if false, return 503 early.
 */
export function hasCredentials() {
  return Boolean(ACCESS_TOKEN);
}

/**
 * getQuotes(securitiesBySegment)
 *
 * Fetches the full quote (LTP + OHLC + volume + VWAP + OI) for a batch of securities.
 *
 * @param {Object} securitiesBySegment  e.g. { "NSE_EQ": [1333, 11536], "NSE_INDEX": [13] }
 *   Keys are Dhan exchange-segment strings; values are arrays of integer security IDs.
 *   Supports up to 1000 instruments per request.
 *   Source: https://dhanhq.co/docs/v2/market-quote/
 *
 * Response shape per instrument:
 *   { last_price, ohlc: { open, high, low, close }, volume, average_price,
 *     oi, net_change, upper_circuit_limit, lower_circuit_limit }
 *
 * @returns {Object} Raw Dhan response (keyed by "SEGMENT:securityId")
 */
export async function getQuotes(securitiesBySegment) {
  const res = await fetch(`${BASE}/v2/marketfeed/quote`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify(securitiesBySegment),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => '');
    const err = new Error(`Dhan /marketfeed/quote ${res.status}: ${text}`);
    err.status = res.status;
    throw err;
  }

  const json = await res.json();
  // Dhan wraps the payload in a `data` key
  return json.data ?? json;
}

/**
 * getDailyHistory(securityId, exchangeSegment, instrument, fromDate, toDate)
 *
 * Fetches daily OHLCV candles.
 * Source: https://dhanhq.co/docs/v2/historical-data/
 *
 * @param {string} securityId       e.g. "1333"
 * @param {string} exchangeSegment  e.g. "NSE_EQ"
 * @param {string} instrument       e.g. "EQUITY"
 * @param {string} fromDate         "YYYY-MM-DD"
 * @param {string} toDate           "YYYY-MM-DD"
 *
 * Response: { open:[], high:[], low:[], close:[], volume:[], timestamp:[], open_interest:[] }
 */
export async function getDailyHistory(securityId, exchangeSegment, instrument, fromDate, toDate) {
  const res = await fetch(`${BASE}/charts/historical`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify({
      securityId: String(securityId),
      exchangeSegment,
      instrument,
      expiryCode: 0,
      oi: false,
      fromDate,
      toDate,
    }),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => '');
    const err = new Error(`Dhan /charts/historical ${res.status}: ${text}`);
    err.status = res.status;
    throw err;
  }

  return res.json();
}

/**
 * getIntraday(securityId, exchangeSegment, instrument, interval, fromDate, toDate)
 *
 * Fetches intraday OHLCV candles.
 * Source: https://dhanhq.co/docs/v2/historical-data/
 *
 * @param {string} securityId
 * @param {string} exchangeSegment
 * @param {string} instrument
 * @param {number} interval         1 | 5 | 15 | 25 | 60 (minutes)
 * @param {string} fromDate         "YYYY-MM-DD HH:mm:ss"
 * @param {string} toDate           "YYYY-MM-DD HH:mm:ss"
 *   Note: max window is 90 days (source: Dhan docs).
 *
 * Response: { open:[], high:[], low:[], close:[], volume:[], timestamp:[] }
 */
export async function getIntraday(securityId, exchangeSegment, instrument, interval, fromDate, toDate) {
  const res = await fetch(`${BASE}/charts/intraday`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify({
      securityId: String(securityId),
      exchangeSegment,
      instrument,
      interval,
      oi: false,
      fromDate,
      toDate,
    }),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => '');
    const err = new Error(`Dhan /charts/intraday ${res.status}: ${text}`);
    err.status = res.status;
    throw err;
  }

  return res.json();
}
