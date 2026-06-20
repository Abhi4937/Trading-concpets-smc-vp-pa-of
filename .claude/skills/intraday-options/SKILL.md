---
name: intraday-options
description: Use when trading Indian intraday index options (Nifty/BankNifty/FinNifty/Sensex) with the Decision Engine, Breakout, Fakeout Reversal, or Opening Range Breakout (ORB) playbooks; when classifying the day/regime, choosing which of the five plays is legal, marking qualified levels (OB/FVG/VAH/VAL/POC/IB/OI walls), placing point-stops and converting to option strikes, or judging R:R/expectancy. Triggers: ORB, IB, VAH/VAL/POC, VWAP, LVN/HVN, BOS, CHoCH, acceptance, failed auction, SFP, turtle soup, max-pain, retest.
---

# Intraday Options (Decision Engine + strategies)

## Overview
India intraday index options. **One repeatable decision routed across regime → level → reaction → play → strike.** The regime decides the menu *before* price reaches a level; the play *falls out* of the at-level reaction. Read **[[trading]]** master for the guardrails (futures-to-read, 1h/15m/5m, expectancy>win-rate, budget-fit stop, WAIT≠signal, veto). Deep notes in `In-Depth Notes/Strategies/`.

## The decision sequence
1. **Pre-open:** ≤4–5 qualified levels (fresh OB/FVG, swing H/L, PDH/PDL, liquidity pools, OI walls).
2. **Regime gate** (decode FADE vs BREAK first):

| Regime | Signal | Legal plays | Forbidden |
|--------|--------|-------------|-----------|
| Positive-GEX balance | pinning, near max-pain | fakeout-reversal, reversal, range-fade | breakout/continuation |
| Negative-GEX trend | acceleration, away from max-pain | breakout, pullback, continuation | fading the trend |
| Mixed / gamma-flip | coil resolving | raise bar; wait acceptance | pre-committing |
| Event / high-IV | two-way, IV-crush risk | wait for spike reaction | anticipating the print |
| Expiry afternoon (post ~2:30pm IST) | theta + pinning | fade toward max-pain only | directional long-premium buys |

3. **At the level → HOLD / BREAK / WAIT.** The verdict is the play. Drop to 5m for trigger only. Convert to ATM/1-OTM strike where the stop fits budget, else retest/skip.

## Strategy specs
### Breakout — `In-Depth Notes/Strategies/Breakout Trading/note.md`
- **Setup:** balance→imbalance at a fresh value-edge/IB boundary. Regime: **negative-GEX/trend only.**
- **Entry (5m):** wide-body conviction close beyond (body ≥60–70%) + rising CVD + stacked buy imbalances, no CVD divergence. **Prefer retest** of broken level (shrinks stop ~40–50%).
- **Stop:** ~0.5–1.0×ATR beyond level (~25–30 pts Nifty pref). **Target:** next OI wall/HVN (T1), naked POC/PD extreme (T2). Gross R:R ≥1:2.
- **Strike:** ATM (~0.50δ) or slightly-ITM; avoid far-OTM. Custom **Breakout Toolkit** indicator marks levels.

### Fakeout Reversal — `In-Depth Notes/Strategies/Fakeout Reversal Trading/note.md`
- **Setup:** sweep of a strong level → close back inside → CVD divergence + OI re-defense. Regime: **positive-GEX/balance.** Fading in a trend is the cardinal error.
- **Entry (5m):** SFP/turtle-soup close back inside; CVD lower-high into the poke; swept strike OI holds/rises; CHoCH within 1–3 bars. **Prefer failed-retest** entry.
- **Stop:** tight, ~0.3–0.5×ATR beyond the swept wick (~25–35 pts Nifty) — the tight stop *is* the edge. **Range = the measured move** → superior R:R. T1 POC/VWAP, T2 opposite edge.
- **Strike:** ATM/1-OTM. Best window 9:15–11:00; expiry-afternoon fade-to-max-pain is high-EV.

### Opening Range Breakout (ORB) — `In-Depth Notes/Strategies/Opening Range Breakout/note.md`
- **Setup:** 15m OR (9:15–9:30 IST) = qualified level **and** engineered liquidity pool.
- **Entry (5m):** wait for **close** beyond OR (not a wick). **Regime decides:** trend day → break extends (trade it); balance day → break is a trap (fade failed break back inside, or wait). Prefer retest.
- **Stop:** opposite OR end (~25–40 pts Nifty). **R:R 1:1–2:1**, hard time-exit ~2:30pm.
- **Honest edge:** naive ORB option-buying ≈**48% win, ~45% max DD** (Zerodha backtest). The edge is **selectivity + regime-gating + fakeout-awareness**, not the break. See `…/research-orb.md`.

## Routing
| Need | Note |
|------|------|
| The umbrella decision logic, 5 plays, all cards | `Strategies/Intraday Options Decision Engine/note.md` (⭐) |
| ORB evidence / why selectivity | `Strategies/Intraday Options Decision Engine/research-orb.md` |
| Timeframe validation | `Strategies/Intraday Options Decision Engine/research-timeframes.md` |
| Order-flow confirmation at the level | **order-flow** sub-skill |
| Candle/pattern triggers | **price-action** sub-skill |
| Dealer-gamma/GEX regime input | **btc-gex** sub-skill (concept transfers; Nifty uses OI walls/max-pain/India VIX) |

## What NOT to do
- ❌ Buy every ORB break (≈coin-flip with 45% DD); quote "+91.6%" type backtests (refuted, zero-cost/in-sample).
- ❌ Fade in a trend / chase a break without the retest / over-mark levels (≤4–5 qualified).
- ❌ First-15-min entries (disproportionately fake); expiry-afternoon directional long-premium buys.
- ❌ Widen the stop to fit; trade a WAIT; ignore the veto (CVD divergence/absorption/OI re-defense against you).
