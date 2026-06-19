---
type: capture-plan
title: "Opening Range Breakout — real-chart capture plan (deferred 2nd pass)"
date: 2026-06-19
status: pending
---

# Capture Plan — Opening Range Breakout

Real, marked-up TradingView captures to layer **next to** the schematics in `note.md`. Schematic-first is shipped;
this is the enrichment pass. Follow `In-Depth Notes/BLUEPRINT.md` §3 / `STRATEGY_BLUEPRINT.md` §8. Reuse the custom
**Decision Engine Toolkit** Pine indicator (`../Intraday Options Decision Engine/decision-engine-toolkit.pine`) +
**Visible Range Volume Profile** + the chart's **VWAP**, on **NIFTY1!** (real volume). Each saved as
`charts/<slug>.real.png` and embedded after the matching schematic.

## Scenarios

| # | slug → `charts/<slug>.real.png` | Symbol · TF | Must show | Markings |
|---|---|---|---|---|
| 1 | `orb-lifecycle` | NIFTY1! · 15m/5m | A real day: 9:15–9:30 OR box → break → retest → run to target | OR box (4 trend-lines), break candle, retest, T1/T2 |
| 2 | `orb-real-vs-trap` | NIFTY1! · 5m | One real break (extends) + one trap (poke + close back in + reverse) | OR edge, the two outcomes; CVD/delta if available |
| 3 | `entry-break-vs-retest` | NIFTY1! · 5m | A break with both the break-close and the retest entry | entry markers + the two stop distances |
| 4 | `sl-target-geometry` | NIFTY1! · 15m | OR box with SL at opposite end and measured-move + next-level targets | SL line, T1 (OR width), T2 (PDH/level) |
| 5 | `vwap-volume-confluence` | NIFTY1! · 5m | OR break on the right side of VWAP with a volume-expansion candle | VWAP, OR edge, the break candle |
| 6 | `narrow-vs-wide-ib` | NIFTY1! · 15m | A narrow-IB breakout day vs a wide-IB rotation day (two captures) | IB box each; outcome |
| 7 | `daytype-decision-tree` (trend) | NIFTY1! · 15m/5m | A trend/neg-GEX day where the OR break extended | regime note, the break, the run |
| 8 | `daytype-decision-tree` (balance) | NIFTY1! · 15m/5m | A balance/pos-GEX day where the OR break failed and reverted | the sweep + reversal |
| 9 | `expiry-theta` (Tuesday) | NIFTY options | A Nifty Tuesday weekly-expiry session showing late-day premium decay vs an OR break | premium chart / option-chain via agent-browser |
| 10 | `oi-confluence` | NSE option chain | OI build in the break direction / re-defense / max-pain pull | via `agent-browser`: OI, IV, premium |

## Acceptance criteria
- **Correct context:** verify each with what happened *after*; don't cherry-pick a clean break that actually failed (unless that IS the trap example).
- **~100-bar view** for the day captures (and a tight intraday view that shows the 9:15–9:30 OR clearly), decluttered to the indicator + VP + VWAP only.
- **No reused chart** across scenarios; recent instances. Repeat key scenes on **BankNifty** to show the ~2–3× scale + monthly-expiry difference.
- Mark the OR box as **4 `trend_line` segments** (the `rectangle` shape stretches ~3×). Enable **"Scale price chart only"** on the price axis so the indicator boxes don't squish the candles.

## Bridge prep (from BLUEPRINT.md §3)
`tv_health_check` → `chart_get_state`; build/attach the Decision Engine Toolkit via the Pine tools; **never** call `chart_scroll_to_date`/`draw_clear`/`draw_remove_one` (clear via `ui_evaluate` removeAllDrawingTools — but do NOT wipe the user's own drawings without asking); auto-fit via the `setPriceAutoScale` snippet; daily anchors at `timegm(date)+13500`, intraday bars real unix; per scenario set symbol→TF→visible range→mark→fit→`capture_screenshot(region=chart)`→copy to `charts/<slug>.real.png`→embed. Then flip `status: reviewed`.
