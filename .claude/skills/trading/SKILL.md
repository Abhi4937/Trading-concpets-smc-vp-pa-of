---
name: trading
description: Use when trading or analyzing markets with this vault's methodology — Indian intraday index options (Nifty/BankNifty/FinNifty/Sensex), volume profile, VWAP, order flow/footprint, price action, breakouts, opening range, reversals, or BTC options; when deciding which setup to take, sizing/risk, picking strikes, classifying the day/regime, or routing to the order-flow, price-action, intraday-options, or btc-gex sub-skills and the In-Depth Notes Obsidian vault.
---

# Trading (master)

## Overview
The spine of this vault: **one repeatable, regime-gated decision** for Indian intraday index options, fed by order flow, price action, and volume profile. This skill enforces the guardrails and routes to the right depth. The vault lives at `In-Depth Notes/`. **Trading is selection, not prediction** — the edge is *which* trade is legal today, taken selectively, sized by expectancy.

## Non-negotiable guardrails (enforce these first)
1. **Futures to read, options to execute.** Map levels / regime / reactions on **NIFTY1!/BANKNIFTY1!** futures (spot indices have no real volume). Options are only the vehicle.
2. **Timeframes:** 1h/30m = bias+regime, 15m = the level, 5m = the trigger. **Never invent a level on 5m. Never make 1m/tick your decision timeframe.**
3. **Expectancy > win-rate.** Demand gross R:R ≥ 1:2 (≈1:1.5 net of costs). A 40% win rate at 1:3 beats 70% at 1:1.
4. **Selectivity over frequency.** Few A+ setups; cap trades/day; overtrading is the documented killer (SEBI: 93% of F&O traders lose; loss-makers trade *more*).
5. **Defined-risk on balance/positive-GEX/expiry-afternoon days.** Theta + pinning dominate → avoid directional long-premium buying; fade toward max-pain or stand aside.
6. **Stop must fit the per-instrument point budget** (Nifty ~30–40 pref / 50–60 max; BankNifty/Sensex ~2–3×). If invalidation > budget → **wait for a retest that shrinks it, or skip.** Never widen the budget to fit a trade.
7. **WAIT is not a signal.** Entering out of a WAIT is the #1 avoidable loss.
8. **The veto rule:** CVD divergence / absorption / OI re-defense *against* your trade overrides a high confluence count. Two clean witnesses beat four noisy ones.
9. **Risk ≤1–2% per trade, uniform.** Daily circuit-breaker (stop after 2 losses or a pre-written ₹ cap). After wins, tighten, not loosen.
10. **Scalping verdict = NO** as a primary edge in India (reconstructed aggressor data is least accurate on 1m; costs/theta punish frequency). 5m drop is execution *timing* only.

## The one repeatable decision (run every time)
1. **Pre-open:** mark ≤4–5 *qualified* levels (fresh OB/FVG, swing H/L, PDH/PDL, liquidity pools, OI walls). More lines = meaningless.
2. **Classify regime/day** (decode FADE vs BREAK *before* price reaches a level): gap type, balance-vs-trend, options regime (GEX/IV/PCR/max-pain). Regime collapses 5 plays → at most 2 legal ones.
3. **At the level, read the *reaction*** → **HOLD / BREAK / WAIT**.
4. **The verdict IS the play** — one of the five (below).
5. **Drop to 5m for the trigger only.**
6. **Convert to options:** ATM/1-OTM strike where the stop fits the budget; else retest or skip.

## The five plays (legal verdicts, not 5 strategies)
| Play | Fires when | Regime |
|------|-----------|--------|
| **Breakout** | acceptance/conviction close beyond level + delta expansion + structure | negative-GEX / trend |
| **Fakeout reversal** | sweep → no acceptance → close back inside + CVD divergence + OI re-defense | positive-GEX / balance |
| **Reversal at exhaustion** | V-climax at naked HTF extreme + CVD divergence | balance / at walls |
| **Pullback / mitigation** | retrace into trend at fresh aligned zone | trending |
| **Continuation** | trend-leg resumes after BOS-pullback completes | trending |
> Same hammer-after-sweep = **spring (reversal)** in balance, **pullback-to-continue** in trend. The pre-written regime label is the tiebreaker.

## Route to depth
| Topic | Sub-skill / note |
|-------|------------------|
| Which play + strategy specs (Breakout/Fakeout/ORB, Decision Engine) | **intraday-options** sub-skill |
| Order flow, footprint, delta, VP shapes, absorption, traps (Faber Vaale/Chart Fanatics/Trader Dale) | **order-flow** sub-skill |
| Candlesticks, pullback entries, fast patterns, reversals, options strategy menu (Fractal Flow Pro) | **price-action** sub-skill |
| BTC gamma exposure / dealer hedging / GEX dashboards | **btc-gex** sub-skill |
| Does it actually work? evidence/scorecard/scalping verdict | `In-Depth Notes/research-strategy-evidence-and-mastery-roadmap.md` |
| VP+footprint method (India) / aggressor-data reality | `In-Depth Notes/research-volumeprofile-footprint-india.md`, `research-tick-aggressor-india.md` |
| Vault index | `In-Depth Notes/_Home.md` |

> **Division of labor:** **order-flow** = how to *read/confirm* the reaction at a level (footprint/VP/delta). **intraday-options** = the *exact entry, stop (points→strike), target, R:R* for the chosen play. **price-action** = the candle/pattern *trigger*. A typical trade touches all three: read (order-flow) → trigger (price-action) → spec (intraday-options).

## Common mistakes (what NOT to do)
- ❌ Fading a trend / chasing a breakout in the wrong regime — the cardinal error.
- ❌ Reading levels/footprint on spot indices instead of futures.
- ❌ 1m/tick as a decision timeframe; quoting unaudited win-rates (most "50–74%" figures are marketing/targets — see the evidence roadmap).
- ❌ Widening the stop to fit; oversizing after a winning streak; trading a WAIT.
- ❌ Treating any single pattern/indicator as standalone — always location + confluence + trigger + veto-check.
