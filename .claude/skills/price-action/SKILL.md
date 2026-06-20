---
name: price-action
description: Use when reading candlestick patterns, catching pullbacks / trend entries, trading fast few-bar price-action patterns, anticipating reversals, or selecting an options strategy by market view (Fractal Flow Pro material). Triggers: hammer, engulfing, doji, morning/evening star, three soldiers, harami, FVG, inside bar, NR4/NR7, hikkake, outside bar, AVWAP, fib cluster, supertrend, RSI/volume divergence, Wyckoff spring/upthrust, Dow theory, Elliott, harmonic, straddle, iron condor, IV rank.
---

# Price Action (Fractal Flow Pro)

## Overview
Pattern libraries that produce **triggers and entries**, never standalone systems. The unifying law: **never trade in isolation — demand location (at a strong barrier) + confluence (2–3 independent methods agree) + a trigger (next candle / divergence / trap completion).** Bulkowski's data: ~94% of isolated pattern-conditions fail to beat random. Use under **[[trading]]** guardrails; these feed the 5m **trigger** in [[intraday-options]]. Notes in `In-Depth Notes/Fractal Flow Pro/`.

## The four toolkits
### Candlesticks — read by body/wick/location, not by name
`06_FreeTradingCourses/001 - …CANDLESTICK PATTERNS/note.md` (49) · `016 - The Definitive Guide…/note.md` (57+)
- **Body** = who won; **wick** = where the battle was; **location** = whether it matters. A hammer mid-air ≠ a hammer at support.
- **Pattern sentiment vs trend sentiment:** agree → continuation; disagree → reversal. Watch the named-vs-real trap (inverted hammer acts bearish-continuation ~65%; hanging man bullish-continuation ~59% **without** strong location).
- Candlesticks are fractal: scan location on 1h/15m, trigger on 5m.

### Catching a pullback — 20 with-trend entries
`04_TechnicalAnalysisVault/002 - 20 Ways of CATCHING A PULLBACK/note.md`
- Menu by family: **horizontal** (S/R switch, POC, runaway gap, minor consolidation) · **geometry** (trendline, ABC channel, sloped S/R, pitchfork, fib cluster, trend angle) · **dynamic** (AVWAP, steep MA, supertrend) · **timing** (cycles) · **divergence** (continuation divergence, expanding-pivot S/D, trap+candle).
- **Use:** confirm trend (HTF) → mark level by **stacking 2–3 methods** at one price → wait for trigger → enter, stop *beyond* the stack → refine on 5m.

### Fast few-bar patterns — precise triggers
`04_TechnicalAnalysisVault/003 - 20 FAST Price Action Patterns/note.md`
- **Gaps:** breakaway, runaway, exhaustion, FVG, island. **Reversal bars:** one-bar, hook, naked, outside, Oops!, pipe, horn, spike, dead-cat. **Trap:** hikkake (failed-breakout snap-back). **Contraction:** inside bar, NR4, NR7, shark + ORB.
- Each = setup + trigger + clean invalidation. **Only** at a barrier, with trend, with confluence.

### Anticipating reversals — 16 "is trend power fading?" lenses
`04_TechnicalAnalysisVault/004 - 16 Ways of Anticipating Reversals/note.md`
- Measure fading power: cycle amplitude/length, ATR decline at new extremes, price persistence, candle stochastic, body-to-range, trend angle (flat *or* too steep). Confirm with **divergence** (RSI + volume), **structure** (Dow HH/HL break, Wyckoff spring/upthrust, Elliott 5-complete), **late patterns** (double/triple top, harmonic). **Act only where 3+ agree at a strong barrier.**

## Options strategy menu (by view)
`06_FreeTradingCourses/002 - …Stock Options Trading (+51 …)/note.md` — 51 strategies by outlook (bullish/bearish/big-move/range) + Greeks. **Core rule: buy options at LOW IV, sell at HIGH IV;** prefer **defined risk**. (For Indian intraday strike choice, defer to [[intraday-options]]: ATM/1-OTM, theta/expiry gates.)

## Vocabulary
hammer, inverted hammer, shooting star, hanging man, doji (gravestone/dragonfly/long-legged), engulfing, piercing, dark cloud, harami (+cross), morning/evening star, three white soldiers, three black crows, tweezer, abandoned baby, three inside/outside, kicking, tasuki gap, mat hold, rising/falling three methods, belt hold; breakaway/runaway/exhaustion gap, FVG, island, one-bar/hook/naked/outside/Oops/pipe/horn/spike/dead-cat, hikkake, inside bar, NR4, NR7, shark, ORB; S/R switch, POC, AVWAP, fib cluster, trendline, ABC channel, supertrend, cycle, continuation/reversal divergence; ATR, VSA, price persistence, body-to-range, Dow theory, Wyckoff spring/upthrust, Elliott wave, harmonic (Gartley/butterfly/crab/AB=CD); delta/gamma/theta/vega, IV rank, straddle, strangle, iron condor, butterfly, vertical spread, covered call, protective put.

## What NOT to do
- ❌ Trade a pattern **in isolation** or by its name (ignore Bulkowski's reliability + the location filter).
- ❌ Pullback entries **with no trend** (falling knife) or **one method only** (need 2–3 stacked); stop *beyond* the stack, not an arbitrary tick.
- ❌ Mistake **exhaustion for strength** (too-steep/vertical = reversal candidate, not buy).
- ❌ Trade Elliott/harmonic/chart patterns as **primary triggers** — they're late confirmation; Dow + Wyckoff structure must confirm first.
- ❌ Buy options at **high IV** into an event (IV-crush) — trade the underlying or a spread.
