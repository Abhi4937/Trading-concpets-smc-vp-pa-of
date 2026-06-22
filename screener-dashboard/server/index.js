/**
 * server/index.js — Express backend for NSE Intraday Screener (Dhan v2)
 *
 * Starts even with no token. Returns 503 when credentials are missing
 * so the frontend can fall back to sample data automatically.
 *
 * Routes:
 *   GET /api/health   → { ok: true }
 *   GET /api/screener → { stocks: [...], source: 'live', asOf: <iso> }
 *                    or 503 { error, hint }
 *
 * Port: process.env.PORT || 8787
 * CORS: http://localhost:5180 (Vite dev server default for this project)
 */

import 'dotenv/config';
import express from 'express';
import cors from 'cors';

import { hasCredentials } from './dhanClient.js';
import { buildInstrumentMap, resolveWatchlist } from './instruments.js';
import { buildScreenerData } from './screenerService.js';

const app  = express();
const PORT = process.env.PORT || 8787;

// ── CORS ──────────────────────────────────────────────────────────────────────
app.use(cors({
  origin: [
    'http://localhost:5173', // Vite default
    'http://localhost:5174', // Vite next port
    'http://localhost:5180', // project-specific override
  ],
  methods: ['GET'],
}));

app.use(express.json());

// ── Instrument map — loaded once at startup, re-used per request ──────────────
let instrumentMap = null;

async function getInstrumentMap() {
  if (!instrumentMap) {
    instrumentMap = await buildInstrumentMap();
  }
  return instrumentMap;
}

// ── Routes ────────────────────────────────────────────────────────────────────

app.get('/api/health', (_req, res) => {
  res.json({
    ok: true,
    credentialsPresent: hasCredentials(),
    ts: new Date().toISOString(),
  });
});

app.get('/api/screener', async (_req, res) => {
  // Guard: no token → 503 immediately so the frontend can fall back cleanly
  if (!hasCredentials()) {
    return res.status(503).json({
      error: 'DHAN_ACCESS_TOKEN is not set',
      hint:  'Copy server/.env.example to server/.env and fill in DHAN_ACCESS_TOKEN. ' +
             'The frontend will fall back to sample data automatically.',
    });
  }

  try {
    const map      = await getInstrumentMap();
    const resolved = resolveWatchlist(map);

    if (resolved.length === 0) {
      return res.status(503).json({
        error: 'No watchlist symbols resolved from scrip master',
        hint:  'The scrip master CSV column names may have changed. ' +
               'Check SECURITY_ID_CANDIDATES in server/instruments.js.',
      });
    }

    const stocks = await buildScreenerData(resolved);
    return res.json({ stocks, source: 'live', asOf: new Date().toISOString() });

  } catch (err) {
    console.error('[/api/screener] Error:', err);

    // Detect auth errors (401/403) or subscription errors (402/429) from Dhan
    const status = err.status;
    if (status === 401 || status === 403) {
      return res.status(503).json({
        error: `Dhan auth error (HTTP ${status}): ${err.message}`,
        hint:  'Check that DHAN_ACCESS_TOKEN is valid and not expired. ' +
               'Tokens have a configurable validity period (up to ~30 days).',
      });
    }
    if (status === 402 || status === 429) {
      return res.status(503).json({
        error: `Dhan subscription/rate-limit error (HTTP ${status}): ${err.message}`,
        hint:  'You may need to subscribe to the Data API on the Dhan dashboard, ' +
               'or you have exceeded the rate limit (5 req/s, 100k/day for data APIs).',
      });
    }

    return res.status(503).json({
      error: err.message,
      hint:  'Check server logs. The frontend will show sample data.',
    });
  }
});

// ── Start ──────────────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`[server] Listening on http://localhost:${PORT}`);
  console.log(`[server] Credentials present: ${hasCredentials()}`);
  if (!hasCredentials()) {
    console.log('[server] No DHAN_ACCESS_TOKEN — /api/screener will return 503; frontend uses sample data.');
  }
});
