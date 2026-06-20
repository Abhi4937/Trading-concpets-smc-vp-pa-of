# Intraday Options Decision Engine — Implementation Plan

> **For agentic workers:** Execute task-by-task. Follows `Strategies/STRATEGY_BLUEPRINT.md` (battle-tested on
> Breakout Trading) and `In-Depth Notes/BLUEPRINT.md` — read both before starting. This is the **umbrella/master**
> guide that routes between the per-play deep-dives (`Breakout Trading/`, `Fakeout Reversal Trading/`).

**Goal:** An exhaustive, visually-rich Obsidian guide teaching ONE repeatable intraday-options decision for
Nifty (worked example) + BankNifty/FinNifty/Sensex (parallel tracks): **map levels → read open + regime →
at the level decide HOLD / BREAK / WAIT → pick one of 5 plays (breakout / fakeout / reversal / pullback /
continuation) → enter not-early-not-late on LTF → translate onto an option strike where the stop fits a
30–40 pt (≤50–60 max) per-instrument budget.** Includes the four protective rules (mid-trade exit, daily-loss
governor, news/event filter, option-buying timing), a footprint deep-dive, a learning path, and a backtest spec.

**Architecture:** Reuse the strategy-guide pipeline — parametric Python SVG generator (~0 model tokens), 1 Sonnet
research subagent → `research.md`, 7 parallel Sonnet drafting subagents → assembled `note.md`, 1 Sonnet QA
subagent. Opus orchestrates + writes the header. Schematic-first; real TradingView charts deferred to `capture_plan.md`.

---

## Global constraints

- **Vault location:** `In-Depth Notes/Strategies/Intraday Options Decision Engine/` — linked from `_Home.md` under `## Strategies` as the umbrella entry.
- **Instruments:** Nifty 50 / NIFTY1! = worked example; BankNifty/FinNifty/Sensex = parallel tracks with **per-instrument** point-scale + stop-budget tables (the 30–40/50–60 pt budget is per-instrument, not one number). MTF funnel: **1h/30m (bias+regime) → 15m (the level) → 5m (the trigger)**.
- **Voice:** exhaustive, beginner→pro, *nothing skipped*; tables + `> [!tip]/[!warning]/[!example]/[!note]/[!summary]` callouts; full worked setups (read→decide→enter→SL→exit) for **both long and short**. (memory: `teaching-and-chart-preferences`.)
- **Colour code:** 🟢 green = bullish/demand · 🔴 red = bearish/supply · 🟡 gold = the level/liquidity · 🔵 blue = entry/OB · 🟦 teal = targets. SVG palette from `breakout_svg.py` (`BG #131722`, bull `#089981`, bear `#f23645`, gold `#f0b90b`).
- **Chart cleanliness (HARD rule):** every schematic shows ONLY the levels that matter to *that* lesson — the active level, its 1–2 confluences, the target node. Never "every swing / every FVG". The `level-map` + `level-grading` scenes explicitly teach the relevance filter (strength / freshness / distance-from-price + a max-levels cap of ~3–6 in view).
- **Token policy:** deterministic Python + Opus orchestration cheap; prose bulk (research, 7 drafts, QA) on **Sonnet**. (memory: `model-division-token-optimization`.)
- **Stale-proofing:** never trust `in_progress`; register every subagent with `python scripts/agent_watch.py add <id> "<purpose>" <expect_min>`; `OVERDUE` (>2× expected) = dead → TaskStop + relaunch just that part. (memory: `agent-stale-proofing`.)
- **Embeds use markdown** `![](charts/slug.svg)` + an italic caption line — NOT wikilinks. Cross-references to siblings use `[[Breakout Trading/note|Breakout Trading]]` / `[[Fakeout Reversal Trading/note|Fakeout Reversal Trading]]`.
- **Hedge every exchange-set value** (lot size, weekly-expiry weekday, STT/charges) → "verify current value on NSE/BSE before trading."

---

## The organising thesis (the spine)

> **Every intraday options trade is the same decision repeated.** (1) Pre-open, map the levels (OB, FVG, swing,
> PDH/PDL/PDC, liquidity pool, VP HVN/LVN/naked-POC). (2) Read the open + regime to know today's game —
> balance/positive-GEX → fade levels; trend/negative-GEX → trade breaks. (3) At the level, read **HOLD vs BREAK
> vs WAIT** from the *reaction* (sweep+reject / hammer / absorption / CVD-divergence vs acceptance / BOS /
> delta-expansion), grade on **weighted confluence** (structure + VP/order-flow + options flow); that read *is*
> the play. (4) Enter on the LTF not-early-not-late trigger, then translate onto a strike where invalidation ≤
> your point-budget — if it isn't, WAIT for the retest that shrinks the stop, or skip.

---

## Canonical asset slugs (SHARED — SVG generator produces these; drafters embed these verbatim)

### Static schematics → `charts/<slug>.svg`
| slug | what it shows |
|---|---|
| `master-flowchart` | the whole decision flow: pre-open map → open/regime → at-level HOLD/BREAK/WAIT → 5 plays → entry → option-strike + stop-budget gate |
| `five-plays-taxonomy` | breakout / fakeout / reversal / pullback / continuation at a glance (when each applies) |
| `weighted-confluence` | how much weight structure vs VP/order-flow vs options-flow get, and how the weights SHIFT by regime |
| `level-map` | one decluttered chart: a qualified OB, a fresh FVG, a swing H/L, PDH/PDL, a liquidity pool, VP HVN/LVN/naked-POC — only the ones that qualify |
| `level-grading` | the relevance filter: which OB/FVG/swing/HVN qualifies (fresh, HTF-aligned, near price) vs which to DROP; max-levels cap |
| `news-event-filter` | pre-market go/no-go gate (RBI/Fed/CPI/expiry-day + first-minutes window) |
| `open-types` | 3-panel: gap-up / gap-down / flat, and how price travels to the level in each |
| `ib-travel` | Initial Balance + how price reaches the level (first-hour behaviour) |
| `regime-tree` | decision tree: balance/trend + positive/negative-GEX → fade vs break |
| `at-level-fork` | the core fork: reaction read → HOLD (fade/reversal) / BREAK (breakout/continuation) / WAIT |
| `hammer-sweep-branch` | "hammer + strong sweep → continue or reverse?" branch, both directions |
| `wait-vs-retest` | first-touch vs wait-for-retest; how the retest shrinks the stop |
| `grinding-up-case` | the worked scenario: high → fall to demand → sweep/bullish pattern → grind up → about to break (enter reversal vs wait for breakout) |
| `ltf-lens` | which LTF lens to use when — price action vs SMC vs VP (decision guide) |
| `footprint-read` | footprint deep-dive: bid/ask imbalance, absorption, delta/CVD; what it adds + when you need it |
| `fvg-ltf-entry` | FVG on LTF: valid entry + the failure modes (when NOT to trust it) |
| `option-sl-delta` | option SL from futures stop via delta (option-SL ≈ futures-stop × delta) |
| `option-sl-atr` | option SL via ATR×multiplier estimate of the futures move |
| `strike-selection` | ATM vs 1-OTM payoff/Greeks trade-off |
| `stop-budget-table` | per-instrument point-scale + stop budget (Nifty / BankNifty / FinNifty / Sensex) |
| `theta-decay` | intraday time-of-day premium decay curve (e.g. post-2:30pm) |
| `iv-rank-gate` | IV-rank go/no-go before buying options |
| `mid-trade-exit` | thesis-broke-before-SL early-exit (trail / time-stop) |
| `targets-map` | targets = next HVN / OI-wall / naked-POC / measured move |
| `rr-sizing` | R:R math + 1-lot sizing under capital constraint |
| `daily-loss-governor` | stop-for-the-day after N losses / ₹X; max-trades; capital-stress rule |
| `per-play-cards` | 5 compact play cards (context gate · entry · SL · target · options note) |
| `mtf-nesting` | 1h→15m→5m nesting funnel (adapt `render_mtf` from breakout_svg.py) |
| `backtest-grid` | the parameter grid to tune (stop budget / RR / confirmation / regime filter / strike) |

### Animations → `anim/<slug>.anim.svg` (candle scenes only)
`at-level-fork`, `hammer-sweep-branch`, `wait-vs-retest`, `grinding-up-case`, `fvg-ltf-entry`, `ib-travel`

---

## Section → part-file map (~39 sections, 7 parts + header)

| Part file | Sections | Coverage | Embeds |
|---|---|---|---|
| `0_header.md` (Opus) | frontmatter, TL;DR, how-to-read | the spine in one breath | `![](charts/master-flowchart.svg)` |
| `1_engine_overview.md` | §1–4 | 5 plays defined · weighted-confluence model (+ regime shift) · the one-decision spine · routing to the deep-dives | `five-plays-taxonomy`, `weighted-confluence` |
| `2_level_and_open.md` | §5–12 | HTF level mapping (OB/FVG/swing/PDH-PDL/PDC/liquidity/VP) · level grading + the declutter filter · pre-market checklist · **news/event + expiry filter** · open read (gap up/down/flat) + IB + travel-to-level | `level-map`, `level-grading`, `news-event-filter`, `open-types`, `ib-travel`, `anim/ib-travel.anim.svg` |
| `3_regime.md` | §13–16 | will it be sideways/volatile/then-trend? balance-vs-trend + GEX + IV/PCR/max-pain + range-vs-expansion; fade-vs-break BEFORE the level | `regime-tree` |
| `4_decision_tree.md` | §17–24 | **THE core.** reaction read → HOLD/BREAK/WAIT → 5 plays · hammer+sweep continue-vs-reverse (both ways) · when to wait vs not (confirmation/retest) · the grinding-up case | `at-level-fork`, `anim/at-level-fork.anim.svg`, `hammer-sweep-branch`, `anim/hammer-sweep-branch.anim.svg`, `wait-vs-retest`, `anim/wait-vs-retest.anim.svg`, `grinding-up-case`, `anim/grinding-up-case.anim.svg` |
| `5_ltf_entries.md` | §25–30 | LTF not-early-not-late entry · which lens when (PA/SMC/VP) · **footprint deep-dive** (+ paid-data reality + free fallback) · **FVG on LTF + how to master it** · trigger per play | `ltf-lens`, `footprint-read`, `fvg-ltf-entry`, `anim/fvg-ltf-entry.anim.svg` |
| `6_options_layer.md` | §31–36 | strike (ATM/1-OTM) · **SL via delta** + **via ATR** · **per-instrument stop-budget gate** · targets + RR · 1-lot sizing · **option-buying timing (theta/IV)** · **mid-trade early exit** · high-PoP-but-stop-too-wide → wait/skip | `option-sl-delta`, `option-sl-atr`, `strike-selection`, `stop-budget-table`, `theta-decay`, `iv-rank-gate`, `mid-trade-exit`, `targets-map`, `rr-sizing` |
| `7_playbook_and_path.md` | §37–39 | per-play cards · **daily-loss governor** · learning/training path (drills + exit tests + journaling) · **backtest spec** | `per-play-cards`, `daily-loss-governor`, `mtf-nesting`, `backtest-grid` |

---

## Tasks

1. **Scaffold** `{charts,anim,parts}/` + this `_PLAN.md`. ✓
2. **Research** → `research.md` (1 Sonnet bg subagent, agent_watch). Reads repo notes first (4 India options refs + 4 channel `CONCEPTS.md` + both sibling `note.md`s), mines `books/` via `/mingw64/bin/pdftotext` (target chapters), targeted web for gaps (Nifty/BankNifty delta+ATR→option-stop mapping, current lot sizes/expiry weekdays, IV-rank, theta decay). Ends with "Open gaps / verify on live chart."
3. **Visuals** → `scripts/decision_engine_svg.py` (copy/adapt `breakout_svg.py`); produce the slugs above into `charts/` + `anim/`; `esc()` all dynamic text; declutter every scene. Self-QA: XML parse + bounds; headless-Chrome PNG render of `master-flowchart`, `at-level-fork`, `option-sl-delta`, `stop-budget-table`.
4. **QA visuals** — confirm all slugs exist, valid XML, no clipping.
5. **Draft** 7 parts via parallel Sonnet subagents (research.md path + section spec + exact embeds + voice + word target ~2.5–3.5k each).
6. **Header** — Opus writes `parts/0_header.md`.
7. **Assemble** `0..7` → `note.md` + footer; validate embeds + numbering 1..39.
8. **QA note** — Sonnet reads whole note, fixes cross-refs/seams/contradictions/markdown, hedges exchange-set values; delete `parts/`.
9. **Index** `_Home.md` (umbrella row) + write `capture_plan.md` stub.
10. **Real charts** — deferred 2nd pass (TradingView MCP), not in this build.
