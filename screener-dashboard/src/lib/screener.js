/**
 * screener.js — Pure screening and enrichment logic for NSE Intraday Screener
 *
 * All functions are pure (no side effects). Data flows:
 *   raw quote → enrich() → enriched quote consumed by UI components.
 *
 * Setup taxonomy (from intraday-options vault):
 *   breakout    — price clears OR high + PDH on volume
 *   breakdown   — price loses OR low + PDL on volume
 *   fakeout     — false break (trapped traders)
 *   reversal_up — red on day but reclaiming VWAP on RS strength
 *   bounce      — pullback to VWAP re-entry in uptrend
 */

export function changePct(q) {
  return ((q.ltp - q.prevClose) / q.prevClose) * 100;
}

export function isInPlay(q) {
  return q.relVol >= 2;
}

export function classifySetup(q) {
  const chg = changePct(q);
  const orBreakLevel = Math.max(q.orHigh, q.pdh);
  const orBreakdownLevel = Math.min(q.orLow, q.pdl);

  // breakout — cleared ORH+PDH on volume, above VWAP
  if (q.ltp > orBreakLevel && q.ltp > q.vwap && q.relVol >= 2 && chg > 0) return 'breakout';

  // breakdown — lost ORL+PDL on volume, below VWAP
  if (q.ltp < orBreakdownLevel && q.ltp < q.vwap && q.relVol >= 2 && chg < 0) return 'breakdown';

  // fakeout — failed breakout (poked above but fell back below & VWAP)
  if (q.dayHigh > orBreakLevel && q.ltp < orBreakLevel && q.ltp < q.vwap) return 'fakeout';

  // fakeout — failed breakdown (poked below but reclaimed level & VWAP)
  if (q.dayLow < orBreakdownLevel && q.ltp > orBreakdownLevel && q.ltp > q.vwap) return 'fakeout';

  // reversal_up — red on day but above VWAP with RS strength
  if (chg < 0 && q.ltp > q.vwap && q.relVol >= 1.5 && q.rsRank >= 50) return 'reversal_up';

  // bounce — pullback to VWAP re-entry (within 0.6% of VWAP)
  if (q.ltp > q.vwap && chg > 0 && Math.abs(q.ltp - q.vwap) / q.vwap < 0.006 && q.relVol >= 1.5)
    return 'bounce';

  return null;
}

export function direction(setup, q) {
  if (setup === 'breakout' || setup === 'reversal_up' || setup === 'bounce') return 'long';
  if (setup === 'breakdown') return 'short';
  if (setup === 'fakeout') {
    // failed breakout → short bias; failed breakdown → long bias
    const orBreakLevel = Math.max(q.orHigh, q.pdh);
    return q.dayHigh > orBreakLevel ? 'short' : 'long';
  }
  return null;
}

export function signalStrength(q, setup) {
  if (!setup) return 0;
  let score = 0;

  // Relative volume contribution (max 40 pts) — normalised to 4× = full
  score += Math.min(40, (q.relVol / 4) * 40);

  // RS rank alignment (max 25 pts)
  score += (q.rsRank / 100) * 25;

  // VWAP distance (max 20 pts) — further from VWAP = more committed move
  const vwapDist = Math.abs(q.ltp - q.vwap) / q.vwap * 100;
  score += Math.min(20, vwapDist * 4);

  // In-play bonus (15 pts) — relVol >= 2 confirms institutional activity
  if (q.relVol >= 2) score += 15;

  return Math.round(Math.min(100, score));
}

export function levels(q, setup) {
  if (setup === 'breakout') {
    const trigger = Math.max(q.orHigh, q.pdh);
    const stop = q.vwap;
    const target = trigger + 1.5 * (trigger - stop);
    return { trigger, stop, target };
  }

  if (setup === 'breakdown') {
    const trigger = Math.min(q.orLow, q.pdl);
    const stop = q.vwap;
    const target = trigger - 1.5 * (stop - trigger);
    return { trigger, stop, target };
  }

  if (setup === 'fakeout') {
    const orBreakLevel = Math.max(q.orHigh, q.pdh);
    if (q.dayHigh > orBreakLevel) {
      // failed breakout → short from VWAP
      const trigger = q.vwap;
      const stop = orBreakLevel;
      const target = trigger - 1.5 * (stop - trigger);
      return { trigger, stop, target };
    } else {
      // failed breakdown → long from VWAP
      const trigger = q.vwap;
      const stop = Math.min(q.orLow, q.pdl);
      const target = trigger + 1.5 * (trigger - stop);
      return { trigger, stop, target };
    }
  }

  if (setup === 'reversal_up') {
    const trigger = q.vwap;
    const stop = q.dayLow;
    const target = trigger + 1.5 * (trigger - stop);
    return { trigger, stop, target };
  }

  if (setup === 'bounce') {
    const trigger = q.vwap;
    const stop = q.orLow;
    const target = trigger + 1.5 * (trigger - stop);
    return { trigger, stop, target };
  }

  return { trigger: null, stop: null, target: null };
}

export function rationale(q, setup) {
  const sym = q.symbol;
  if (setup === 'breakout')
    return `${sym} broke above ORH+PDH on ${q.relVol.toFixed(1)}× volume with strong RS — momentum continuation trade.`;
  if (setup === 'breakdown')
    return `${sym} lost ORL+PDL on ${q.relVol.toFixed(1)}× volume below VWAP — short bias, target lower lows.`;
  if (setup === 'fakeout')
    return `${sym} faked a breakout but rejected back below level — trapped longs, mean-reversion opportunity.`;
  if (setup === 'reversal_up')
    return `${sym} red on day but reclaimed VWAP on elevated volume with RS ≥ 50 — potential intraday reversal long.`;
  if (setup === 'bounce')
    return `${sym} pulling back to VWAP in an uptrend on volume — low-risk re-entry near dynamic support.`;
  return '';
}

export function enrich(q) {
  const chg = changePct(q);
  const setup = classifySetup(q);
  const dir = direction(setup, q);
  const strength = signalStrength(q, setup);
  const { trigger, stop, target } = levels(q, setup);
  return {
    ...q,
    changePct: chg,
    inPlay: isInPlay(q),
    setup,
    direction: dir,
    strength,
    trigger,
    stop,
    target,
    rationale: rationale(q, setup),
  };
}
