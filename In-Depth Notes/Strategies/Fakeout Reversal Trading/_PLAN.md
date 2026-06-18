# Fakeout Reversal Trading — Implementation Plan

> **For agentic workers:** Execute task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. This plan follows `Strategies/STRATEGY_BLUEPRINT.md` (the battle-tested recipe proven on Breakout Trading) — read it and `In-Depth Notes/BLUEPRINT.md` before starting.

**Goal:** Build an exhaustive, visually-rich Obsidian strategy note that teaches trading the **failed breakout (fakeout) as a reversal** — the offensive twin of `Strategies/Breakout Trading/` — from foundations to pro, both directions, for Nifty intraday traded via ATM/near-ATM options.

**Architecture:** Reuse the strategy-guide pipeline end-to-end: parametric Python SVG generator for all schematics/animations (~0 model tokens), one Sonnet research subagent → `research.md`, five parallel Sonnet drafting subagents (one per part-file) → assembled `note.md`, one Sonnet QA subagent over the whole note, Opus orchestrates + QAs + writes the header. Schematic-first; real TradingView charts deferred to a `capture_plan.md`.

**Tech Stack:** Python 3 (stdlib only — SVG generation, `xml.etree` validation), system Chrome headless (SVG→PNG QA render), Obsidian markdown (callouts, wikilinks, embeds), `scripts/agent_watch.py` (subagent liveness), TradingView MCP (optional 2nd pass only).

---

## Global Constraints

- **Vault location:** `In-Depth Notes/Strategies/Fakeout Reversal Trading/` — linked from `_Home.md` under `## Strategies`.
- **Instrument & timeframes (verbatim from sibling note):** Nifty 50 / Nifty futures · index options (ATM/near-ATM CE/PE). MTF funnel: **1h (regime/level) → 15m (sweep level) → 5m (reclaim trigger)**.
- **Voice:** exhaustive, beginner→pro, *nothing skipped*; tables + `> [!tip]/[!warning]/[!example]/[!note]/[!summary]` callouts; full worked setups (sweep→confirm→entry→SL→exit) for **both long and short**. (memory: `teaching-and-chart-preferences`.)
- **Colour code (identical to breakout note):** 🟢 green = bullish/demand · 🔴 red = bearish/supply · 🟡 gold = the level/liquidity pool · 🔵 blue = entry/OB · 🟦 teal = targets. House SVG palette: `BG #131722`, bull `#089981`, bear `#f23645`, gold `#f0b90b`.
- **Schematic-first:** SVG schematics are the guaranteed visual and never block delivery. Real charts are an enrichment in a later pass.
- **Token policy:** deterministic Python + Opus orchestration are cheap; the prose bulk (research, 5 part drafts, QA) runs on **Sonnet** subagents. (memory: `model-division-token-optimization`.)
- **Stale-proofing:** never trust `in_progress`; register every subagent with `python scripts/agent_watch.py add <id> "<purpose>" <expect_min>`; `OVERDUE` (>2× expected) = dead → TaskStop + relaunch just that part. Must-complete single deliverables run foreground. (memory: `agent-stale-proofing`.)
- **Embeds use markdown** `![](charts/slug.svg)` + an italic caption line — NOT wikilinks. Cross-references to the sibling note use `[[Breakout Trading/note|Breakout Trading]]`.
- **Hedge every exchange-set value** (lot size, weekly-expiry weekday, STT/charges) → "verify current value on NSE before trading."

---

## The organising thesis (the spine)

> **A fakeout reversal trades the FAILED transition: price attempts balance→imbalance, fails to find acceptance, and reverts. It is tradeable only when the breakout's three witnesses all REFUSE to confirm — effort fails (low-vol poke / absorption / CVD divergence), structure sweeps-and-reverses (sweep wick + close back inside + CHoCH, no BOS), and the options tape re-defends (wall OI rises not unwinds, premium won't expand, positive-GEX pin, max-pain pull). The breakout note's "abort / fade instead" conditions ARE this note's entry checklist.**

Regime-complementary spine: **read GEX/range first to decide which game today is** — positive-GEX / balance / pin → reversals; negative-GEX / trend → breakouts. The two notes are two halves of one decision.

---

## File structure

```
In-Depth Notes/Strategies/Fakeout Reversal Trading/
├── _PLAN.md            ← this file
├── note.md             ← the canonical guide (assembled; ~15–17k words, ~32 sections)
├── research.md         ← cited research (Sonnet subagent, ~3.5–4.5k words)
├── capture_plan.md     ← real-chart scenarios for the deferred TradingView pass
├── charts/             ← ~20 static schematics (*.svg)
├── anim/               ← 5 animated schematics (*.anim.svg)
└── parts/              ← 6 drafting checkpoints (deleted after assembly)
    ├── 0_header.md  1_foundations.md  2_lenses.md
    ├── 3_mtf_india.md  4_options_edge.md  5_execution.md
scripts/
└── fakeout_svg.py      ← copied & adapted from scripts/breakout_svg.py
```

### Section → part-file map (32 sections, 5 parts + header)

| Part file | Sections | Coverage |
|---|---|---|
| `0_header.md` | frontmatter, TL;DR, how-to-read | Opus-written; the spine in one breath |
| `1_foundations.md` | §1–6 | thesis + inverted 3-witness · lifecycle · why fakeouts are your edge (trap mechanics) · the fork (sweep-and-reverse vs sweep-and-go) · named-patterns family (Turtle Soup / SFP / Wyckoff Spring-Upthrust / failed auction / stop-hunt) · legend |
| `2_lenses.md` | §7–13 | structures that produce fakeouts · Lens 1 VPA (low-vol poke, absorption, climax) · Lens 2 Volume Profile (rejection inside value, poor highs/lows, naked POC magnet) · Lens 3 order-flow/CVD (absorption + CVD divergence = top tell) · Lens 4 SMC (sweep→CHoCH→reclaim, SFP, micro-OB) · Lens 5 price action (rejection wick, reclaim close, failed retest) · stacking → conviction |
| `3_mtf_india.md` | §14–17 | MTF nesting for reversals · Indian session — when fakeouts dominate · ORB-fakeout & VWAP-rejection reversal · expiry/event nuances (pin = best friend) |
| `4_options_edge.md` | §18–23 | OI re-defense · failed OI migration · IV/premium non-expansion · dealer gamma (positive-GEX = reversal regime) · max-pain as target / PCR extremes · end-to-end options-flow fakeout checklist |
| `5_execution.md` | §24–32 | two entry models · SL beyond the sweep + ATR · targets & trailing · R:R & sizing math · 10-point reversal scorecard · master SOP · two full worked setups (long & short) · mistakes & psychology · one-page summary |

---

## Task 1: Scaffold the strategy folder

**Files:**
- Create: `In-Depth Notes/Strategies/Fakeout Reversal Trading/charts/.gitkeep`
- Create: `In-Depth Notes/Strategies/Fakeout Reversal Trading/anim/.gitkeep`
- Create: `In-Depth Notes/Strategies/Fakeout Reversal Trading/parts/.gitkeep`

- [ ] **Step 1: Create the directory tree**

```bash
cd "C:/dev/trading_concepts/In-Depth Notes/Strategies/Fakeout Reversal Trading"
mkdir -p charts anim parts
touch charts/.gitkeep anim/.gitkeep parts/.gitkeep
```

- [ ] **Step 2: Verify**

Run: `ls -R "In-Depth Notes/Strategies/Fakeout Reversal Trading"`
Expected: `charts/`, `anim/`, `parts/`, `_PLAN.md` all present.

---

## Task 2: Research → `research.md` (1 Sonnet subagent, background, registered)

**Files:**
- Create: `In-Depth Notes/Strategies/Fakeout Reversal Trading/research.md`

**Interfaces:**
- Produces: `research.md` — dense, cited, organised by the lenses this strategy needs; ends with an **"Open gaps / to verify on live chart"** list. Consumed by every drafting subagent in Task 5.

- [ ] **Step 1: Dispatch one `general-purpose` (Sonnet) subagent, run in background.** Prompt shape:
  - **Read FIRST:** `Strategies/Breakout Trading/research.md` and `note.md` (this is the inverted twin — reuse its India-options findings), then repo notes `options-flow-india.md`, `options-flow-and-dealer-greeks.md`, `order-flow-options-backtesting-india-reference.md`, `volume-footprint-and-data-feeds-india.md`.
  - **Then mine books** in `books/` via `/mingw64/bin/pdftotext` (target chapters only): Raschke & Connors *Street Smarts* (Turtle Soup), Wyckoff/Pruden (Spring & Upthrust/UTAD), Al Brooks (failed breakouts/fades), Dalton *Mind Over Markets* (failed auction, poor highs/lows), Coulling *VPA* (absorption/exhaustion/climax), Trader Dale (absorption, naked-POC magnet), Douglas *The Disciplined Trader* (psychology of fading).
  - **Then targeted web** (load `WebSearch`/`WebFetch` via ToolSearch): Swing Failure Pattern (SFP) mechanics, Nifty expiry-day pinning & max-pain, positive-GEX mean-reversion, NSE OI re-defense reads.
  - **Write ONE file** `research.md` with inline tags `(Author)` / `(repo: file.md)` / `(web: src)`, organised by: the fork (sweep-and-reverse vs sweep-and-go), the named patterns, the five lenses (read for failure), the India options inversion, regime (GEX/pin), execution/risk, psychology. End with **"Open gaps / to verify on live chart."**
  - **Return** only a 10–15 bullet summary of non-obvious findings.
- [ ] **Step 2: Register the agent**

```bash
python scripts/agent_watch.py add <agent_id> "fakeout research.md" 12
```

- [ ] **Step 3: Poll for completion**

Run: `python scripts/agent_watch.py`
Expected: agent reaches `done`; if `OVERDUE`, TaskStop + relaunch. Confirm `research.md` exists and is ~3.5–4.5k words, cited.

---

## Task 3: Build `scripts/fakeout_svg.py` → 20 schematics + 5 animations

**Files:**
- Create: `scripts/fakeout_svg.py` (copy & adapt `scripts/breakout_svg.py`)
- Create: `In-Depth Notes/Strategies/Fakeout Reversal Trading/charts/*.svg` (20)
- Create: `In-Depth Notes/Strategies/Fakeout Reversal Trading/anim/*.anim.svg` (5)

**Interfaces:**
- Consumes: the declarative `render_scene(scene, anim=False)` engine from `breakout_svg.py` (supports `candles`, `levels`, `zones`, `arrows`, `curves`, `annot`, `profile`, `delta`, `sl_tp`, plus non-candle infographic renderers). Reuse `esc()` on ALL dynamic text.
- Produces: the exact slugs below (these are the embed targets the Task 5 drafters drop in verbatim).

**Scene catalog (slug → what it shows):**

| # | Slug (`charts/…svg`) | Scene |
|---|---|---|
| 1 | `lifecycle.svg` | range → liquidity build → sweep/raid → rejection close-back-inside → CHoCH → reclaim/retest → revert to mid/opposite edge (also rendered `--anim`) |
| 2 | `sweep-and-reverse-fork.svg` | two-panel: sweep-and-reverse (trade) vs sweep-and-go (stand aside) from the same poke |
| 3 | `turtle-soup.svg` | false break of an N-bar high/low + snap-back reversal |
| 4 | `sfp.svg` | swing-failure: sweep of prior swing high, close back below, reversal |
| 5 | `wyckoff-spring.svg` | false break of support → spring → reversal up (also `--anim`) |
| 6 | `wyckoff-upthrust.svg` | false break of resistance (UTAD) → reversal down |
| 7 | `absorption-reversal.svg` | high volume into the level, no progress; passive absorption → reversal |
| 8 | `cvd-divergence-reversal.svg` | price new extreme, CVD does not confirm (delta subpanel) |
| 9 | `poor-high-low-failed-auction.svg` | single-print/poor high revisited; naked POC as magnet/target |
| 10 | `choch-reclaim-entry.svg` | sweep → CHoCH → reclaim of level + micro-OB → confirmation candle entry (also `--anim`) |
| 11 | `orb-fakeout-vwap-reject.svg` | opening-range sweep → reclaim; VWAP rejection reversal |
| 12 | `oi-redefense.svg` | wall OI RISING at the tested strike (writers defending = break fails) |
| 13 | `failed-oi-migration.svg` | no fresh OI at the next strike; range not re-pricing |
| 14 | `gex-pin-regime.svg` | positive-GEX dealers fade the move → pin/mean-reversion = reversal regime |
| 15 | `maxpain-magnet-target.svg` | price magnetised back to max-pain as the reversal target |
| 16 | `sl-target-geometry-reversal.svg` | SL beyond the sweep extreme + ATR; T1 range-mid/POC, T2 opposite edge; R-multiples |
| 17 | `reversal-scorecard.svg` | the 10-point reversal confluence scorecard infographic |
| 18 | `mtf-nesting-reversal.svg` | 1h regime/level → 15m sweep level → 5m reclaim trigger, stacked panels |
| 19 | `regime-decision-tree.svg` | which game today: GEX/range → breakout vs reversal branch |
| 20 | `patterns-taxonomy.svg` | the named-patterns family at a glance (Turtle Soup/SFP/Spring/Upthrust/failed-auction) |

**Animations (`anim/…anim.svg`):** `lifecycle.anim.svg`, `sweep-reverse.anim.svg`, `turtle-soup.anim.svg`, `choch-reclaim.anim.svg`, `wyckoff-spring.anim.svg`.

- [ ] **Step 1: Copy the generator**

```bash
cp scripts/breakout_svg.py scripts/fakeout_svg.py
```

- [ ] **Step 2: Replace the `SCENES` catalog** with the 20 hand-tuned OHLC scenes above (normalised 0–100 scale; reuse the existing `levels`/`zones`/`arrows`/`profile`/`delta`/`sl_tp` primitives; add a `choch` glyph and a `sweep-wick` callout helper if not present). Keep `esc()` on every dynamic string.
- [ ] **Step 3: Generate all assets**

```bash
python scripts/fakeout_svg.py --out "In-Depth Notes/Strategies/Fakeout Reversal Trading"
python scripts/fakeout_svg.py --out "In-Depth Notes/Strategies/Fakeout Reversal Trading" --anim
```

- [ ] **Step 4: Verify count**

Run: `ls "In-Depth Notes/Strategies/Fakeout Reversal Trading/charts" | wc -l && ls "In-Depth Notes/Strategies/Fakeout Reversal Trading/anim" | wc -l`
Expected: `20` charts, `5` anims.

---

## Task 4: QA the visuals (XML + bounds + headless-Chrome render)

**Files:** read-only over `charts/*.svg`, `anim/*.anim.svg`.

- [ ] **Step 1: Validate XML + coordinate bounds for every SVG**

```bash
python - <<'PY'
import glob, xml.etree.ElementTree as ET
base="In-Depth Notes/Strategies/Fakeout Reversal Trading"
bad=[]
for f in glob.glob(base+"/charts/*.svg")+glob.glob(base+"/anim/*.anim.svg"):
    try: ET.parse(f)
    except Exception as e: bad.append((f,str(e)))
print("INVALID:",bad or "none")
PY
```
Expected: `INVALID: none` (if any fail, it is almost always a bare `&`/`<`/`>` — wrap with `esc()` and regenerate).

- [ ] **Step 2: QA-render the key scenes to PNG via system Chrome headless** (must be an absolute `file:///` URL)

```bash
"<chrome>" --headless --disable-gpu --force-device-scale-factor=2 --window-size=900,560 \
  --screenshot=/tmp/qa_lifecycle.png \
  "file:///C:/dev/trading_concepts/In-Depth%20Notes/Strategies/Fakeout%20Reversal%20Trading/charts/lifecycle.svg"
```
Repeat for `sl-target-geometry-reversal.svg`, `reversal-scorecard.svg`, `mtf-nesting-reversal.svg`, `choch-reclaim-entry.svg`. Eyeball each PNG: no clipped SL/TP labels, no MTF-panel collision, legible text. Fix the generator and regenerate if any clip.

---

## Task 5: Draft the 5 parts in parallel (Sonnet subagents, registered)

**Files:**
- Create: `parts/1_foundations.md`, `2_lenses.md`, `3_mtf_india.md`, `4_options_edge.md`, `5_execution.md`

**Interfaces:**
- Consumes: `research.md` (each subagent reads it FIRST). Each gets its section spec, the exact embed lines, word target, and the house voice.
- Produces: five part-files, each starting at `## ` (no frontmatter), returning a 3-line summary.

**Each subagent prompt MUST contain:** the `research.md` absolute path; the exact `## N.` headings from the section→part map; the **exact embed lines** for its part (below); the house voice block (exhaustive, beginner→pro, tables + callouts, both directions, Nifty-options framing, cross-link `[[Breakout Trading/note|Breakout Trading]]` for shared lenses instead of re-deriving at full length); a word target (~2.5–3.5k each); and "**write ONLY this file, start at `## `, return a 3-line summary.**"

**Exact embeds per part:**
- `1_foundations.md`: `![](anim/lifecycle.anim.svg)`, `![](charts/sweep-and-reverse-fork.svg)`, `![](anim/sweep-reverse.anim.svg)`, `![](charts/patterns-taxonomy.svg)`, `![](charts/turtle-soup.svg)`, `![](anim/turtle-soup.anim.svg)`, `![](charts/sfp.svg)`, `![](charts/wyckoff-spring.svg)`, `![](anim/wyckoff-spring.anim.svg)`, `![](charts/wyckoff-upthrust.svg)`
- `2_lenses.md`: `![](charts/absorption-reversal.svg)`, `![](charts/cvd-divergence-reversal.svg)`, `![](charts/poor-high-low-failed-auction.svg)`, `![](charts/choch-reclaim-entry.svg)`, `![](anim/choch-reclaim.anim.svg)`
- `3_mtf_india.md`: `![](charts/mtf-nesting-reversal.svg)`, `![](charts/orb-fakeout-vwap-reject.svg)`, `![](charts/regime-decision-tree.svg)`
- `4_options_edge.md`: `![](charts/oi-redefense.svg)`, `![](charts/failed-oi-migration.svg)`, `![](charts/gex-pin-regime.svg)`, `![](charts/maxpain-magnet-target.svg)`
- `5_execution.md`: `![](charts/sl-target-geometry-reversal.svg)`, `![](charts/reversal-scorecard.svg)`

- [ ] **Step 1: Dispatch 5 Sonnet subagents in parallel** (one message, 5 tool calls).
- [ ] **Step 2: Register each**

```bash
python scripts/agent_watch.py add <id> "fakeout part N" 8
```

- [ ] **Step 3: Poll; relaunch any OVERDUE part only.** Confirm all five part-files exist and start at `## `.

---

## Task 6: Write the header (Opus, foreground)

**Files:**
- Create: `parts/0_header.md`

- [ ] **Step 1: Write frontmatter + TL;DR + how-to-read.** Frontmatter mirrors the breakout note: `type: strategy-guide`, `instrument`, `timeframes: "1h (regime) → 15m (sweep level) → 5m (reclaim trigger)"`, `concepts` (fakeout, liquidity-sweep, turtle-soup, swing-failure-pattern, wyckoff-spring, upthrust, absorption, cvd-divergence, failed-auction, naked-poc, oi-re-defense, positive-gex, max-pain, multi-timeframe, risk-management, trade-psychology), `tags`, `difficulty: "beginner→pro"`, `sources`, `status: draft`. H1 = "Fakeout Reversal Trading — Trading the Failed Breakout (Nifty Intraday Options)". TL;DR = the spine in one breath + the regime-complementary link to `[[Breakout Trading/note|Breakout Trading]]`. A `> [!tip] How this guide is organised` callout listing the 5 parts.

---

## Task 7: Assemble → `note.md`

**Files:**
- Create: `In-Depth Notes/Strategies/Fakeout Reversal Trading/note.md`

- [ ] **Step 1: Concatenate** `parts/0..5` with blank-line joins:

```bash
cd "In-Depth Notes/Strategies/Fakeout Reversal Trading"
cat parts/0_header.md parts/1_foundations.md parts/2_lenses.md \
    parts/3_mtf_india.md parts/4_options_edge.md parts/5_execution.md > note.md
```

- [ ] **Step 2: Append the footer** — `## Related notes & sources`: `[[research]]`, `[[capture_plan]]`, `[[Breakout Trading/note|Breakout Trading]]` (the twin), repo notes, books (Raschke/Connors, Wyckoff/Pruden, Brooks, Dalton, Coulling, Trader Dale, Douglas), and a `> [!quote]` one-line summary.
- [ ] **Step 3: Validate embeds + numbering**

```bash
python - <<'PY'
import re,os
p="In-Depth Notes/Strategies/Fakeout Reversal Trading"
t=open(p+"/note.md",encoding="utf-8").read()
miss=[m for m in re.findall(r'!\[\]\(([^)]+)\)',t) if not os.path.exists(os.path.join(p,m))]
print("MISSING EMBEDS:",miss or "none")
nums=[int(n) for n in re.findall(r'^## (\d+)\.',t,re.M)]
print("SECTION NUMS:",nums)
PY
```
Expected: `MISSING EMBEDS: none`; section numbers contiguous `1..32`.

---

## Task 8: QA the whole note (1 Sonnet subagent)

**Files:** edits `note.md` in place.

- [ ] **Step 1: Dispatch a Sonnet QA subagent** to read the entire `note.md` and fix IN PLACE: broken internal `§N` cross-references (parts were drafted against per-part numbering — this WILL happen), jarring seams (add `---` or a one-line bridge), threshold contradictions between parts (reconcile to the scorecard values), heading/numbering contiguity, markdown hygiene (table separators, valid callout types, no drafting artifacts), and market-accuracy red flags (hedge anything exchange-set). Return a ≤20-line report.
- [ ] **Step 2: Verify the report**, spot-check 2–3 fixed cross-refs, re-run the Task 7 Step 3 validator. Then delete `parts/`:

```bash
rm -rf "In-Depth Notes/Strategies/Fakeout Reversal Trading/parts"
```

---

## Task 9: Index + capture plan

**Files:**
- Modify: `In-Depth Notes/_Home.md` (`## Strategies` link + status row)
- Create: `In-Depth Notes/Strategies/Fakeout Reversal Trading/capture_plan.md`

- [ ] **Step 1: Wire `_Home.md`** — add under `## Strategies` a link to `[[Strategies/Fakeout Reversal Trading/note|Fakeout Reversal Trading]]` and a status-table row (date `2026-06-19`, "Strategy", title link, word/asset count, `schematic-first / real-charts-pending`).
- [ ] **Step 2: Write `capture_plan.md`** — a table of real-chart scenarios (slug, symbol/TF, what it must show, markings), mirroring the breakout `capture_plan.md` structure and bridge-prep warnings. Scenarios: `turtle-soup.real.png` (NIFTY1!·15m, false N-bar-high break + reversal), `sfp.real.png` (NIFTY·15m, swing-high sweep + close back below), `wyckoff-spring.real.png` (NIFTY1!·15m, support false-break + spring up), `orb-fakeout.real.png` (NIFTY1!·5m, OR sweep + reclaim), `vwap-reject.real.png` (NIFTY1!·5m), `choch-reclaim.real.png` (NIFTY1!·5m, sweep→CHoCH→reclaim entry), `sl-target-geometry.real.png` (completed reversal trade w/ SL beyond sweep + T1/T2), `mtf-1h/15m/5m.real.png` (same instance nested), and an option-chain `oi-redefense.real.png` (wall OI rising + no migration + premium not expanding, via `agent-browser`). Acceptance: correct context (verify with what happened after), ~100-bar view, no reused charts.

---

## Task 10 (optional 2nd pass): Real-chart capture via TradingView MCP

Only when the user opts in and TV Desktop is up. Follow `STRATEGY_BLUEPRINT.md` §8 / `BLUEPRINT.md` §3 quirks verbatim: `tv_health_check` → `chart_get_state`; build/attach the supporting indicator via Pine tools if needed; declutter to the intended indicator only; **never** call `chart_scroll_to_date`/`draw_clear`/`draw_remove_one` (clear via `ui_evaluate`, auto-fit via `setPriceAutoScale`); draw boxes as 4 `trend_line` segments; daily anchors at `timegm(date)+13500`; pick recent correct-context instances on **NIFTY1!**; per scenario set symbol→TF→visible range(~100 bars)→clear→mark→fit→`capture_screenshot(region=chart)`→copy to `charts/<slug>.real.png`→embed next to the schematic. Then flip `status: reviewed`.

---

## Self-review (against the spec/blueprint)

- **Spec coverage:** every section in the design (§1–32) is owned by a part-file in the Task-5 map; the inverted 3-witness, the named-patterns family, the regime-complementary spine, MTF, the India options inversion, SL/targets/sizing/scorecard/SOP/worked-setups/psychology all have a home. ✓
- **Visual coverage:** all 20 schematics + 5 anims have an embed target in a part. ✓
- **Blueprint fidelity:** 10-step pipeline, parallel checkpointed parts + `agent_watch`, schematic-first, headless-Chrome QA render, `_Home` indexing + `capture_plan.md` stub — all followed. ✓
- **Hedging:** lot size / expiry weekday / STT flagged "verify current value." ✓
```
