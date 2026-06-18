---
title: "Capture Plan — real Nifty / Nifty-futures fakeout-reversal charts"
type: capture-plan
status: pending
related: "[[note]]"
---

# Capture Plan — real charts to layer onto the fakeout-reversal guide

You chose **schematic-first**: the guide ships now with clean SVG schematics + animations, and these real captures get marked up and embedded in a follow-up pass once TradingView Desktop is up with the supporting indicator(s) attached. Each real chart sits *next to* the matching schematic in `note.md` (the schematic is the guaranteed visual; the real chart is enrichment — same policy as [[Breakout Trading/capture_plan|the breakout capture plan]] and the video-notes blueprint).

> [!warning] Prep before capturing (from `STRATEGY_BLUEPRINT.md` §8 / `BLUEPRINT.md` §3)
> - Launch TradingView Desktop via the bridge (`tv_launch`); `tv_health_check` → confirm CDP + symbol/resolution; `chart_get_state` → see attached studies.
> - The bridge **cannot attach a saved Pine script**, but it CAN build one (`pine_new` → `pine_set_source` → `pine_smart_compile` → `pine_get_errors` → `pine_save`) and add built-ins via `chart_manage_indicator` (FULL names). **Declutter** to the intended indicator(s) only, green/red/gold (memory: chart preferences).
> - **Never call** `chart_scroll_to_date` / `draw_clear` / `draw_remove_one` (broken). Clear via `ui_evaluate` (`removeAllDrawingTools`); auto-fit price after each range change via the `setPriceAutoScale` snippet.
> - Draw highlight boxes as **four `trend_line` segments** (the `rectangle` shape stretches ~3×). Daily anchors stamped at 03:45 UTC (`timegm(date)+13500`); intraday bars use real unix.
> - Bridge shows only the most recent ~300 bars → pick **recent, correct-context** instances. Use **NSE:NIFTY1!** (real volume) for the volume/CVD reads; **NSE:NIFTY** (spot) for structure.

## Scenarios to capture (one real chart each, correct-context, recent)

| # | Slug to save as | Symbol / TF | What it must show | Markings |
|---|---|---|---|---|
| 1 | `lifecycle.real.png` | NIFTY1! · 15m | A full failed-breakout reversal: coil → sweep above resistance → close back inside → CHoCH → failed retest → revert to the mean | Range box, level line, sweep wick callout, CHoCH arrow, retest zone, SL/T1/T2 |
| 2 | `sweep-and-reverse.real.png` | NIFTY1! · 5m | A clean sweep-and-reverse: poke beyond the level, long rejection wick, close back inside, reversal | Level line, rejection-wick callout, "fade" arrow |
| 3 | `sweep-and-go.real.png` | NIFTY1! · 5m | The contrast: a sweep that CLOSED beyond and accepted (a real break — stand aside) | Level line, conviction-close box, "do not fade" |
| 4 | `turtle-soup.real.png` | NIFTY1! · 15m | A false break of a prior N-bar (≥4 bar) low that snaps back above it and reverses up | Prior-low line, sweep wick, reclaim close, reverse arrow |
| 5 | `sfp.real.png` | NIFTY · 15m | A swing-failure: a prior swing high swept then a candle closing back below it, reversal down | Swing-high line, sweep, close-back-below callout |
| 6 | `wyckoff-spring.real.png` | NIFTY1! · 15m | A spring: a stab below range support that immediately reclaims, then the low-volume test that holds | Support line, spring zone, test, markup arrow |
| 7 | `wyckoff-upthrust.real.png` | NIFTY1! · 15m | An upthrust/UTAD: a stab above range resistance that fails back inside, then markdown | Resistance line, upthrust zone, markdown arrow |
| 8 | `cvd-divergence-reversal.real.png` | NIFTY1! · 5m | Price prints a new extreme but cumulative delta makes a lower/higher counter-high (the top reversal tell) | New-extreme line, CVD subpanel, divergence callout |
| 9 | `orb-fakeout.real.png` | NIFTY1! · 5m | An opening-range sweep that fails and loses VWAP, fading back into the IB | IB box (first hour), VWAP, sweep arrow, fade arrow |
| 10 | `choch-reclaim.real.png` | NIFTY1! · 5m | The A+ entry: sweep → CHoCH → pullback into the micro-OB / FVG → confirmation candle | Swept level, CHoCH, micro-OB box, entry/SL |
| 11 | `sl-target-geometry.real.png` | NIFTY1! · 15m | A completed reversal trade: entry on the failed retest, SL beyond the sweep + ATR, T1 (range mid/POC) + T2 (opposite edge) hit | Entry, SL, T1, T2, R-multiples |
| 12 | `mtf-1h.real.png` / `mtf-15m.real.png` / `mtf-5m.real.png` | NIFTY1! · 1h / 15m / 5m | The SAME instance nested across the three timeframes (regime → swept edge → reclaim) — do NOT reuse one chart | Regime/level · swept edge · reclaim trigger per TF |

## Acceptance criteria
- **Correct context** (not just shape): a fakeout reversal must sit at a real swept level and **actually reverse back across the range** — verify with what happened *after*. A long must be a swept LOW that reverses up; a short a swept HIGH that reverses down.
- **~100-bar view** so the range before and the reversion after are both visible.
- **Do NOT reuse the same chart** across scenarios (past mistake called out in chart preferences).
- After capture: copy each into `charts/<slug>.real.png`, then edit `note.md` so each schematic is followed by its real chart; record which slugs got a real chart (so the rest stay schematic-only). Flip `status: reviewed` only after the montage QA.

## Optional: option-chain / OI snapshots
For Part 4, capture a **Sensibull/Opstra/NSE option-chain** snapshot at a real Nifty fakeout showing the inverse of a breakout: **call/put-wall OI RISING (re-defended) at the tested strike, NO migration to the next strike, and the breakout-side premium NOT expanding / IV bleeding** → save as `charts/oi-redefense.real.png`. A second snapshot of an expiry-afternoon **max-pain pin** (price magnetised back to the pin after a poke) → `charts/maxpain.real.png`. (Web capture via the `agent-browser` skill, per the browser-automation preference.)
