# Opening Range Breakout — Implementation Plan

> Follows `Strategies/STRATEGY_BLUEPRINT.md` (battle-tested on Breakout/Fakeout/Decision-Engine). Schematic-first;
> real charts deferred to `capture_plan.md`. Research is ALREADY DONE — reuse, don't re-run.

**Goal:** A standalone, exhaustive Obsidian guide on the **Opening Range Breakout** for Nifty/BankNifty intraday
options — beginner→pro, both directions — that teaches ORB *honestly*: a popular but fragile trigger whose edge is
**selectivity** (regime-gate it, confirm it, know the first break is as often a trap as a real break). It is the
sibling of `[[Breakout Trading/note]]` and the deep-dive for the ORB sub-case referenced in the Decision Engine §10.1.

## Research basis (reuse — do NOT re-research)
- `In-Depth Notes/Strategies/Intraday Options Decision Engine/research-orb.md` (web synthesis, cited)
- `In-Depth Notes/Strategies/Intraday Options Decision Engine/research-orb-books.md` (book citations)
Drafters READ both (absolute paths) first.

## The organising thesis (the spine)
> **The Opening Range Breakout is just the Initial-Balance break dressed up — the single most popular retail
> intraday template in India, and a *coin-flip with brutal drawdown* when traded naively (~48% win rate). It earns
> an edge only when it is REGIME-GATED and CONFIRMED: on a trend / negative-GEX day the OR break extends (trade the
> breakout); on a balance / positive-GEX day the first break is a stop-hunt that reverts (fade it — the fakeout).
> Mark the range on the 15m, time the entry on the 5m, confirm with VWAP + volume + OI, stop at the opposite end,
> target a measured move to the next level at 1:1–2:1, and put it on an ATM/near-ATM option whose stop fits the
> point budget. The break is the trigger; the selectivity is the edge.**

## Global constraints
- **Location:** `In-Depth Notes/Strategies/Opening Range Breakout/` — linked from `_Home.md` under `## Strategies`.
- **Instrument & TF:** Nifty 50 / NIFTY1! worked example; BankNifty/Sensex scale + monthly-expiry notes. **Mark OR on 15m → time entry on 5m**; HTF (1h/30m) for bias/regime.
- **Voice:** exhaustive, beginner→pro, nothing skipped; tables + `> [!tip]/[!warning]/[!example]/[!note]/[!summary]`; BOTH directions (CE long / PE short).
- **Colour code:** 🟢 demand/bull · 🔴 supply/bear · 🟡 the OR level/liquidity · 🔵 entry/OB · 🟦 targets. SVG palette from `breakout_svg.py`.
- **Embeds:** `![](charts/slug.svg)` + italic caption; anims `![](anim/slug.anim.svg)`. Cross-link `[[Breakout Trading/note|Breakout Trading]]`, `[[Fakeout Reversal Trading/note|Fakeout Reversal Trading]]`, `[[Intraday Options Decision Engine/note|Decision Engine]]`.
- **Hedge exchange-set values** ("verify on NSE/BSE"): Nifty weekly = Tuesday; BankNifty/FinNifty weekly discontinued (monthly only); lots Nifty 65 / BankNifty 30 / Sensex 20.
- **Token policy:** deterministic Python + Opus orchestration cheap; research/drafts/QA on Sonnet. Register bg agents with `scripts/agent_watch.py`.

## Canonical asset slugs (orb_svg.py → charts/<slug>.svg, anim/<slug>.anim.svg)
| slug | scene |
|---|---|
| `orb-lifecycle` | mark OR (9:15–9:30) → break → retest → run to target (also `--anim`) |
| `or-window-comparison` | 5 / 15 / 30 / 60-min OR windows side by side (noise vs timing tradeoff) |
| `open-types` | gap-up / gap-down / flat — how the OR forms & resolves in each |
| `narrow-vs-wide-ib` | narrow IB (breakout-prone) vs wide IB (rotation/fade) |
| `dalton-open-types` | open-drive / open-test-drive / open-rejection-reverse / open-auction |
| `orb-real-vs-trap` | real break (acceptance, extends) vs trap (sweep + close back in) (also `--anim`) |
| `entry-break-vs-retest` | break-close entry vs retest entry (tighter stop) (also `--anim`) |
| `sweep-and-go-vs-reverse` | the fork: OR break that goes vs OR break that reverses (also `--anim`) |
| `sl-target-geometry` | SL at opposite OR end / ATR / midpoint; measured-move + next-level targets; RR bracket |
| `measured-move-target` | OR width projected from the break = T1; next level = T2 |
| `retest-shrinks-stop` | retest entry shrinks the option stop vs chasing the break (also `--anim`) |
| `vwap-volume-confluence` | break on the right side of VWAP + volume expansion |
| `oi-confluence` | fresh OI in break direction / away from max-pain confirms |
| `daytype-decision-tree` | regime/day-type → trade the break vs fade it vs stand aside |
| `honest-edge` | the ~48% WR / ~45% DD (buying) vs ~6% DD (selling) reality infographic |
| `orb-scorecard` | A+/A/skip confluence scorecard for an ORB trade |
| `options-translation` | spot OR signal → ATM/near-ATM strike (delta 0.4–0.6), premium stop (20% rule) |
| `expiry-theta` | Nifty Tuesday weekly-expiry late-day theta hostility to ORB buying |
| `mtf-nesting` | 1h/30m regime → 15m OR → 5m trigger funnel |
| `per-daytype-cards` | compact cards: trend-day ORB · balance-day ORB-fade · gap-day ORB |

Anims: `orb-lifecycle`, `orb-real-vs-trap`, `entry-break-vs-retest`, `sweep-and-go-vs-reverse`, `retest-shrinks-stop`.

## Section → part-file map (~30 sections, 5 parts + header)
| Part | Sections | Coverage | Embeds |
|---|---|---|---|
| `0_header.md` (Opus) | frontmatter, TL;DR, how-to-read | the spine in one breath | `orb-lifecycle` |
| `1_foundations.md` | §1–6 | what ORB is (the IB break) · the opening range / IB · the lifecycle · **the honest edge** (popular but fragile, the backtest) · web-chases-break vs books-fade-trap · the OR-window debate | `orb-lifecycle`+anim, `honest-edge`, `or-window-comparison` |
| `2_daytypes.md` | §7–12 | gap up/down/flat open read · narrow vs wide IB · Dalton open types · when to trade vs stay out (whipsaw/first-candle) · Nifty Tuesday expiry behaviour · BankNifty monthly vs Nifty weekly | `open-types`, `narrow-vs-wide-ib`, `dalton-open-types`, `expiry-theta` |
| `3_confluence.md` | §13–18 | VWAP · volume expansion · VP/IB/VPOC · order-flow/CVD (India inferred-aggressor) · OI/option-chain/max-pain · PDH/PDL — the witnesses; real-vs-fake break | `vwap-volume-confluence`, `oi-confluence` |
| `4_plays.md` | §19–24 | the two plays — ORB **breakout** (real) vs ORB **fakeout** (trap), regime decides · entry models (break-close vs retest), both directions · sweep-and-go vs sweep-and-reverse · the day-type decision tree | `orb-real-vs-trap`+anim, `entry-break-vs-retest`+anim, `sweep-and-go-vs-reverse`+anim, `daytype-decision-tree` |
| `5_execution.md` | §25–30 | SL (opposite-end/ATR/midpoint) · targets (measured move/levels) + R:R · **options layer** (ATM/ITM delta, premium 20% stop, strike) · sizing + expiry/theta · the ORB scorecard · two worked setups (long CE + short PE) · mistakes/psychology · master SOP · one-page summary · backtest note | `sl-target-geometry`, `measured-move-target`, `retest-shrinks-stop`+anim, `options-translation`, `orb-scorecard`, `mtf-nesting`, `per-daytype-cards` |

## Pipeline
1. Scaffold + _PLAN ✓ → 2. Visuals (orb_svg.py, bg Sonnet) → 3. Draft 5 parts (parallel bg Sonnet, read research-orb.md/-books.md) → 4. Header (Opus) → 5. Assemble + footer → 6. QA note (Sonnet) → 7. Index _Home + capture_plan → 8. (real charts deferred). Validate embeds + §1–30 contiguous; commit.
