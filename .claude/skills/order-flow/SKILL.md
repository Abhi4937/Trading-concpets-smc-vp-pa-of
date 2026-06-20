---
name: order-flow
description: Use when reading order flow / footprint to confirm a trade — delta, cumulative delta (CVD), bid/ask imbalance, absorption, exhaustion, initiative vs passive, volume profile (VAH/VAL/POC/LVN/HVN), value migration, VP shapes (D/P/b/B), liquidity sweeps, trapped traders, break of structure, failed breakout/breakdown, or deep/big trades. Covers Faber Vaale, Chart Fanatics, and Trader Dale methods, and the NSE aggressor-data reality (tick-rule reconstruction).
---

# Order Flow (footprint confirmation)

## Overview
Order flow is the **confirmation layer**, never the thesis. The verified pro sequence is **location first (Volume Profile), delta second (footprint)** — read at a *marked level*, never blind. Three vault methods converge on this. Use under the **[[trading]]** guardrails; for India, read the aggressor caveat below. Notes in `In-Depth Notes/Faber Vaale/`, `Chart Fanatics/`, `Trader Dale/`.

## ⚠️ India / NSE aggressor-data reality (read first)
- NSE **never tags aggressor side** — footprint buy/sell is **reconstructed via the tick rule (~85%/trade)**: good for aggregate bias, unreliable on any single print. Footprint vendors ("tick query") use the *same* inference — no privileged edge.
- **So:** use **5m/15m** footprint (not 1m); require **stacked 2–3 bar** confluence; read on **NIFTY1!/BANKNIFTY1!** futures (spot has no volume); treat delta as a **bias gauge / divergence tell**, never proof. Detail: `In-Depth Notes/research-tick-aggressor-india.md`, `research-volumeprofile-footprint-india.md`.

## The three methods
### Faber Vaale — bias-first, footprint-second (`Faber Vaale/_Master - The Faber Vaale System/note.md` ⭐)
- VP → daily-profile bias → mark VAH/VAL/POC/LVN at premium/discount → confirm at the level.
- **Effort-vs-Result matrix:** high effort+low result = absorption/reversal; low effort+high result = sweep; etc.
- **Triple-confluence entry:** VAH/VAL level + delta-pressure bar + big "deep" trades. **Stop** just past the zone; **TP1** ~50% at 1:2–1:3, runner trailed; move to break-even fast.

### Chart Fanatics — four tools → zones (`Chart Fanatics/001 - 74pct Win Rate OrderFlow Strategy/note.md`)
- Tools: market-generated levels · volume profile · big trades (75 NQ/200 ES) · delta profile. ≥2 align = zone, 4 = A+.
- **Model 1 (range):** fade VAH/VAL edges (never the middle), TP1 midpoint → opposite edge. **Model 2 (trend):** "look below & fail" into LVN, buy the reclaim. Absorption + trapped-trader squeeze are the tells.

### Trader Dale — value shift, WHERE beats WHEN (`Trader Dale/001 - …/note.md`)
- **WHERE = 90%** (liquidity, FVG, LVN, value areas); **WHEN = 10%** (footprint only). VP shapes **D** (balance) **/P** (bull park top) **/b** (bear bottom) **/B** (double-distribution LVN neck).
- **A+ failed-breakout entry = all four:** key level taken → delta shift → trap (triple-stack wick imbalance ≥3×) → break of structure (close through last swing). Stop past the trap; target a pre-marked VP level; partial → break-even → runner.

## How to apply (in this vault)
1. Get **location** from VP/VWAP (the [[intraday-options]] level map).
2. At the level, read footprint for one verdict: **absorption/divergence → fade; acceptance/expansion → continue.**
3. Require the **veto check** — delta/absorption/OI against you kills the trade regardless of confluence count.
4. Convert to the [[intraday-options]] play + strike.

## Shared vocabulary
order flow, footprint, delta, CVD, cumulative delta, delta divergence, bid/ask imbalance, stacked imbalance, absorption, exhaustion, initiative/passive, value area, VAH, VAL, POC, naked/virgin POC, LVN, HVN, value migration, developing value, profile shape D/P/b/B, liquidity sweep, stop-hunt, trapped traders, break of structure, failed breakout/breakdown, deep/big trades, effort vs result, reload zone, initial balance, absorption reversal.

## What NOT to do
- ❌ Trade footprint signals **in isolation** / in mid-air — only at a marked level.
- ❌ Trust **single 1m-bar delta** on NSE (tick-rule noise) — stack 2–3 bars, use 5m/15m.
- ❌ Read footprint on **spot indices** (no volume) — use futures.
- ❌ Treat **POC as a hard magnet** on trend (P/b/B) days — it migrates, price won't return.
- ❌ Chase breakouts (where stops park) / average **down** (only add **up**) / skip break-even-fast and journaling.
