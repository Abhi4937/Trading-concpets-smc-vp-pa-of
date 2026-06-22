/**
 * instruments.js — Dhan scrip-master loader + symbol→securityId map
 *
 * Downloads the Dhan scrip-master CSV once and caches it locally.
 * Cache file: server/instruments-cache.csv
 *
 * CSV download URL (compact version, ~2 MB):
 *   https://images.dhan.co/api-data/api-scrip-master.csv
 *   Source: https://dhanhq.co/docs/v2/instruments/
 *
 * ⚠️  COLUMN NAME CAVEAT:
 *   The Dhan docs list column names like SM_SYMBOL_NAME, SEM_SEGMENT,
 *   SEM_EXM_EXCH_ID, SEM_EXCH_INSTRUMENT_TYPE — but the SECURITY_ID column
 *   name could NOT be confirmed from public docs at the time of writing.
 *   The code tries several plausible column names in order:
 *     SEM_SMST_SECURITY_ID, SECURITY_ID, SM_SECURITY_ID
 *   Adjust SECURITY_ID_COL if none matches after downloading the real CSV.
 *
 * Parsing: manual split — no csv-parse dep. Handles the simple case where
 * fields do not contain newlines (true for Dhan scrip master).
 */

import { readFile, writeFile, access } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dir = dirname(fileURLToPath(import.meta.url));
const CACHE_PATH   = join(__dir, 'instruments-cache.csv');
const CSV_URL      = 'https://images.dhan.co/api-data/api-scrip-master.csv';

// Column name candidates for the numeric security ID — adjust if Dhan renames them
const SECURITY_ID_CANDIDATES = ['SEM_SMST_SECURITY_ID', 'SECURITY_ID', 'SM_SECURITY_ID'];
const SYMBOL_COL    = 'SM_SYMBOL_NAME';       // or SEM_CUSTOM_SYMBOL
const EXCH_COL      = 'SEM_EXM_EXCH_ID';      // "NSE" | "BSE" | "MCX"
const SEGMENT_COL   = 'SEM_SEGMENT';           // "E" for equity
const INST_COL      = 'SEM_EXCH_INSTRUMENT_TYPE'; // "ES" = Equity Stock on NSE
const SERIES_COL    = 'SEM_SERIES';            // "EQ" for equity series

// Static symbol → { name, sector } map from sampleQuotes (used for live enrichment)
// Kept here so the backend can add name/sector without re-importing the frontend module.
export const SYMBOL_META = {
  RELIANCE:   { name: 'Reliance Industries',           sector: 'Energy' },
  TATASTEEL:  { name: 'Tata Steel',                    sector: 'Metals' },
  HINDALCO:   { name: 'Hindalco Industries',           sector: 'Metals' },
  ADANIENT:   { name: 'Adani Enterprises',             sector: 'Conglomerate' },
  WIPRO:      { name: 'Wipro',                         sector: 'IT' },
  HDFCLIFE:   { name: 'HDFC Life Insurance',           sector: 'Insurance' },
  ULTRACEMCO: { name: 'UltraTech Cement',              sector: 'Cement' },
  INFY:       { name: 'Infosys',                       sector: 'IT' },
  BAJFINANCE: { name: 'Bajaj Finance',                 sector: 'NBFC' },
  HDFCBANK:   { name: 'HDFC Bank',                     sector: 'Banking' },
  SBIN:       { name: 'State Bank of India',           sector: 'Banking' },
  ICICIBANK:  { name: 'ICICI Bank',                    sector: 'Banking' },
  KOTAKBANK:  { name: 'Kotak Mahindra Bank',           sector: 'Banking' },
  TCS:        { name: 'Tata Consultancy Services',     sector: 'IT' },
  LT:         { name: 'Larsen & Toubro',               sector: 'Capital Goods' },
  ITC:        { name: 'ITC Limited',                   sector: 'FMCG' },
  MARUTI:     { name: 'Maruti Suzuki',                 sector: 'Auto' },
  AXISBANK:   { name: 'Axis Bank',                     sector: 'Banking' },
  TATAMOTORS: { name: 'Tata Motors',                   sector: 'Auto' },
  JSWSTEEL:   { name: 'JSW Steel',                     sector: 'Metals' },
  SUNPHARMA:  { name: 'Sun Pharmaceutical',            sector: 'Pharma' },
  BHARTIARTL: { name: 'Bharti Airtel',                 sector: 'Telecom' },
  TITAN:      { name: 'Titan Company',                 sector: 'Consumer' },
  NTPC:       { name: 'NTPC Limited',                  sector: 'Power' },
  POWERGRID:  { name: 'Power Grid Corporation',        sector: 'Power' },
  COALINDIA:  { name: 'Coal India',                    sector: 'Mining' },
  ONGC:       { name: 'Oil & Natural Gas Corporation', sector: 'Energy' },
  GRASIM:     { name: 'Grasim Industries',             sector: 'Cement' },
  CIPLA:      { name: 'Cipla',                         sector: 'Pharma' },
  DRREDDY:    { name: "Dr. Reddy's Laboratories",      sector: 'Pharma' },
  TECHM:      { name: 'Tech Mahindra',                 sector: 'IT' },
  BANKBARODA: { name: 'Bank of Baroda',                sector: 'Banking' },
};

// The live watchlist — 32 F&O names from sampleQuotes
export const WATCHLIST = Object.keys(SYMBOL_META);

// Nifty 50 index security ID on NSE_INDEX segment.
// Dhan security ID for NIFTY 50 index = 13 (widely cited; verify against scrip master).
export const NIFTY_INDEX = { securityId: '13', exchangeSegment: 'NSE_INDEX', instrument: 'INDEX' };

/**
 * Parse a CSV line respecting double-quoted fields.
 * Simple implementation — assumes no embedded newlines in fields.
 */
function parseCsvLine(line) {
  const fields = [];
  let cur = '';
  let inQuote = false;

  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuote && line[i + 1] === '"') { cur += '"'; i++; }
      else { inQuote = !inQuote; }
    } else if (ch === ',' && !inQuote) {
      fields.push(cur);
      cur = '';
    } else {
      cur += ch;
    }
  }
  fields.push(cur);
  return fields;
}

/** Download the CSV (no dep, built-in fetch) */
async function downloadCsv() {
  console.log('[instruments] Downloading scrip master CSV…');
  const res = await fetch(CSV_URL);
  if (!res.ok) throw new Error(`Scrip master download failed: ${res.status}`);
  const text = await res.text();
  await writeFile(CACHE_PATH, text, 'utf8');
  console.log('[instruments] CSV cached to', CACHE_PATH);
  return text;
}

/** Load from cache if present, otherwise download */
async function loadCsv() {
  try {
    await access(CACHE_PATH);
    console.log('[instruments] Using cached scrip master CSV');
    return readFile(CACHE_PATH, 'utf8');
  } catch {
    return downloadCsv();
  }
}

/**
 * Build and return a map: symbol (uppercase) → { securityId, exchangeSegment, instrument }
 * Includes NSE equity stocks (SEM_EXM_EXCH_ID=NSE, SEM_SEGMENT=E).
 *
 * @returns {Map<string, { securityId: string, exchangeSegment: string, instrument: string }>}
 */
export async function buildInstrumentMap() {
  const csv = await loadCsv();
  const lines = csv.split('\n');
  if (lines.length < 2) throw new Error('Scrip master CSV appears empty');

  const headers = parseCsvLine(lines[0]).map(h => h.trim());

  // Find the security-ID column — try candidates in order
  let secIdIdx = -1;
  let usedSecIdCol = '';
  for (const candidate of SECURITY_ID_CANDIDATES) {
    const idx = headers.indexOf(candidate);
    if (idx !== -1) { secIdIdx = idx; usedSecIdCol = candidate; break; }
  }
  if (secIdIdx === -1) {
    // Log all headers so the user can identify the correct column name
    console.warn('[instruments] Could not find security-ID column. Headers found:', headers.join(', '));
    throw new Error(
      `Security-ID column not found in scrip master. ` +
      `Tried: ${SECURITY_ID_CANDIDATES.join(', ')}. ` +
      `Headers: ${headers.slice(0, 20).join(', ')}. ` +
      `Update SECURITY_ID_CANDIDATES in server/instruments.js.`
    );
  }
  console.log(`[instruments] Using security-ID column: ${usedSecIdCol} (idx ${secIdIdx})`);

  const symIdx   = headers.indexOf(SYMBOL_COL);
  const exchIdx  = headers.indexOf(EXCH_COL);
  const segIdx   = headers.indexOf(SEGMENT_COL);
  const instIdx  = headers.indexOf(INST_COL);
  const seriesIdx = headers.indexOf(SERIES_COL);

  const map = new Map();

  for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;

    const fields = parseCsvLine(line);
    const exch   = fields[exchIdx]?.trim().toUpperCase();
    const seg    = fields[segIdx]?.trim().toUpperCase();
    const series = fields[seriesIdx]?.trim().toUpperCase();

    // Filter to NSE equity (EQ series) only
    if (exch !== 'NSE' || seg !== 'E' || series !== 'EQ') continue;

    const symbol    = fields[symIdx]?.trim().toUpperCase();
    const secId     = fields[secIdIdx]?.trim();
    const instType  = fields[instIdx]?.trim() ?? 'EQUITY';

    if (!symbol || !secId) continue;
    map.set(symbol, {
      securityId: secId,
      exchangeSegment: 'NSE_EQ',
      instrument: instType || 'EQUITY',
    });
  }

  console.log(`[instruments] Loaded ${map.size} NSE_EQ instruments`);
  return map;
}

/**
 * Resolve watchlist symbols to Dhan instrument descriptors.
 * Symbols not found in the map are logged and skipped.
 *
 * @param {Map} instrumentMap   Result of buildInstrumentMap()
 * @returns {{ symbol, securityId, exchangeSegment, instrument }[]}
 */
export function resolveWatchlist(instrumentMap) {
  const resolved = [];
  for (const symbol of WATCHLIST) {
    const info = instrumentMap.get(symbol);
    if (!info) {
      console.warn(`[instruments] Symbol not found in scrip master: ${symbol}`);
      continue;
    }
    resolved.push({ symbol, ...info });
  }
  return resolved;
}
