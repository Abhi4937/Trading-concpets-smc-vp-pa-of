---
type: capture-plan
title: "Intraday Options Decision Engine — real-chart capture plan (deferred 2nd pass)"
date: 2026-06-19
status: pending
---

# Capture Plan — Intraday Options Decision Engine

Real, marked-up TradingView captures to layer **next to** the schematics in `note.md`. Schematic-first is shipped;
this is the enrichment pass. Follow `In-Depth Notes/BLUEPRINT.md` §3 and `Strategies/STRATEGY_BLUEPRINT.md` §8
bridge quirks verbatim. Use **NIFTY1!** (real volume/CVD) for any volume/footprint scene. Each capture is saved as
`charts/<slug>.real.png` and embedded right after the matching `![](charts/<slug>.svg)`.

> [!note] Indicator & Volume Profile status
> The custom **Decision Engine Toolkit [Course]** Pine indicator is built and live on the chart (BOS/CHoCH,
> fresh OB/FVG capped to the most-recent per type, PDH/PDL/PDC — decluttered). **Volume Profile (Fixed/Visible
> Range) could not be added via the study API** (it is a premium TradingView feature / interactive tool) — add it
> manually in the UI before the VP-dependent captures, or rely on the indicator's levels + the schematic VP.

## Scenarios

| # | slug → `charts/<slug>.real.png` | Symbol · TF | Must show | Markings |
|---|---|---|---|---|
| 1 | `level-map` ✅ done | NIFTY1! · 15m | A real session with only the qualified levels | OB, one FVG, swing H/L, PDH/PDL, a liquidity pool, VP HVN/LVN/POC — **≤6 levels**, declutter rule visible — *captured `level-map.real.png` via the custom indicator* |
| 2 | `at-level-fork` | NIFTY1! · 5m | Same level producing HOLD on one test and BREAK on another | reject wick vs conviction close; label HOLD/BREAK/WAIT |
| 3 | `hammer-sweep-branch` | NIFTY1! · 5m/15m | A sweep+hammer at demand that **continued** AND (separate) one that **reversed** | sweep wick, hammer, the regime tag that decided it |
| 4 | `wait-vs-retest` | NIFTY1! · 5m | A break, then the retest entry | first-touch (wide stop) vs retest (tight stop) with point distances |
| 5 | `grinding-up-case` | NIFTY1! · 15m/5m | High → fall to demand → sweep + bullish reaction → grind to resistance → break | demand zone, resistance, Plan A (reversal) vs Plan B (breakout) entries |
| 6 | `fvg-ltf-entry` | NIFTY1! · 5m | A valid LTF FVG entry **and** a failed/filled FVG (skip) | FVG box, entry candle, SL; the failure annotation |
| 7 | `footprint-read` | NIFTY1! · 5m | CVD divergence / absorption at a level (the trustworthy India read) | price vs CVD divergence; absorption note |
| 8 | `targets-map` | NIFTY1! · 5m/15m | A move that ran into the next HVN / naked-POC / OI wall | VP, the target node(s), measured move |
| 9 | `mtf-nesting` | NIFTY1! · 1h→15m→5m | The SAME instance nested across the three TFs | level set on 1h/15m, trigger on 5m |
| 10 | `oi-redefense` (option-chain) | NSE option chain | OI build / IV / premium behaviour confirming a real-day read | via `agent-browser`: OI walls, IV, premium expand/non-expand |

## Acceptance criteria
- **Correct context:** verify each instance with what happened *after* (don't cherry-pick a level that failed).
- **~100-bar view**, decluttered to the custom SMC indicator + Volume Profile only (memory: `teaching-and-chart-preferences`).
- **No reused chart** across scenarios; recent instances only (bridge shows ~last 300 bars).
- Per-instrument note: repeat key scenes on **BankNifty / Sensex** to show the 2–3× point-scale where it matters.

## Bridge prep notes (from BLUEPRINT.md §3 — still apply)
- `tv_health_check` → confirm CDP + symbol/resolution; `chart_get_state` → see attached studies.
- The bridge can **build** a Pine indicator (`pine_new` → `pine_set_source` → `pine_smart_compile` → `pine_get_errors` → `pine_save`) and add built-ins via `chart_manage_indicator` (FULL names). Confirm the user's custom all-in-one SMC/structure indicator name/inputs first; declutter to it + Volume Profile only.
- **Never** call `chart_scroll_to_date` / `draw_clear` / `draw_remove_one` (broken). Clear via `ui_evaluate` removeAllDrawingTools; auto-fit via the `setPriceAutoScale` snippet.
- Draw highlight boxes as **4 `trend_line` segments** (the `rectangle` shape stretches ~3×). Daily anchors at `timegm(date)+13500`; intraday bars use real unix.
- Per scenario: set symbol → set TF → set visible range (~100 bars) → CLEAR → draw markings → FIT → `capture_screenshot(region=chart)` → copy to `charts/<slug>.real.png` → embed next to the schematic. Then flip `status: reviewed`.
