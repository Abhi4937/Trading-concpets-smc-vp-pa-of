---
title: Worked Examples & Annotated Charts — every GEX scenario
tags: [gex, examples, scenarios, annotated-charts, walkthrough]
created: 2026-06-20
status: teaching
---

# 🧩 Worked Examples & Annotated Charts — every GEX scenario

> The "show me, don't just tell me" note. Every definition from [[01 — What Gamma Exposure (GEX) Is]]
> and [[02 — The Math — Greeks to Dollar GEX (with code)]], turned into an **annotated chart + a
> numeric walkthrough + the trade implication.** ASCII charts are schematic (▇ = positive/call GEX,
> ▁ = negative/put GEX, ● = spot). Where possible, anchored to the live BTC capture (2026-06-20,
> spot ≈ $63,300; net −96.37K; call +162.75K; put −259.12K; squeeze sup/res $63,000, breakout $65,500).

---

## How to read every GEX-by-strike chart (the legend, once)
```
   net GEX ($ per 1% move)
        +│        ▇          ← bar ABOVE zero = positive (call-side) GEX at that strike
     ───┼──●──────────────  ← the zero line; ● = current spot;  x-axis = strike price
        −│   ▁              ← bar BELOW zero = negative (put-side) GEX at that strike
```
- **Tall bar** (either side) = lots of dealer hedging concentrated there = a **wall** (magnet/barrier).
- **Where the bars switch from ▁ to ▇** (net crosses zero) = the **zero-gamma / flip** = regime boundary.
- **Sum of all bars** = total net GEX = the **regime** (＋ pin / − trend).
- **Spot's position vs the flip** = whether you're *locally* in pin or trend behavior.

---

## Part A — the four building blocks, each with a picture

### A1. Gamma Wall (the magnet)
**Definition:** strike with the largest |net GEX|.
```
        +│              ▇▇▇▇          ← GAMMA WALL ($64k): tallest bar
        +│       ▇▇     ▇▇▇▇             = strongest hedging concentration
     ───┼───●───▇▇─────▇▇▇▇──────
          $63.3k       $64k     strike →
```
- **In positive GEX:** price is *pulled toward* the wall and *struggles to pass* it → **pin / fade the pokes through it.**
- **In negative GEX:** the same wall is a *hard level that, once broken, releases a fast move* → **trade the break.**
> Example: wall at $64k, spot $63.3k, positive-gamma book → expect drift up into $64k then stall; short the wick that pokes $64.1k back toward $64k.

### A2. Zero-Gamma / Gamma Flip (the regime switch)
**Definition:** the price where net GEX = 0.
```
        +│                    ▇▇▇
        +│           ▇▇      ▇▇▇
     ───┼───────────╫───────────────  ← ZERO-GAMMA $63,766 (net crosses 0)
        −│      ▁▁  ║
        −│   ▁▁▁▁   ║  ● spot $63,300 sits BELOW the flip → short-gamma side
          $61k      $63.8k       strike →
```
- **Above the flip → long-gamma → pin/mean-revert.** **Below the flip → short-gamma → trend/expand.**
- **Crossing it is the single highest-information event** — your whole playbook flips. (Worked computation of this exact $63,766 in [[02 — The Math — Greeks to Dollar GEX (with code)]] §3c.)
> Example: spot reclaims $63,766 → switch from "sell rallies / momentum" to "buy dips / fade extremes."

### A3. Call Wall & Put Wall (soft resistance / support)
**Definition:** strikes with the most positive (call) and most negative (put) GEX.
```
        +│                         ▇▇▇▇   ← CALL WALL $66k = resistance / rally cap
        +│                ▇▇       ▇▇▇▇
     ───┼────●───────────▇▇───────▇▇▇▇──
        −│ ▁▁▁                            ← PUT WALL $61k = support / air-pocket edge
          $61k  $63.3k            $66k   strike →
```
- Rallies **stall into the call wall**; selloffs **slow at the put wall**.
- A **decisive break of the put wall** (OI doesn't migrate down) = **air-pocket** — nothing below to brake the fall.
> Live example: 2026-06-20 squeeze **resistance $63,000** and **breakout $65,500** were the dashboard's call-side levels; a close above $65,500 in the short-gamma book = breakout continuation trigger.

### A4. Total Net GEX sign (the weather)
**Definition:** sum of all bars.
```
  +Σ  → ▇ outweighs ▁ → LONG GAMMA → calm/pinning weather
  −Σ  → ▁ outweighs ▇ → SHORT GAMMA → stormy/trending weather   ← BTC was here (−96.37K)
```
> Example: net −96.37K → "stormy"; favor breakout/momentum, distrust mean-reversion. This is *step 1* every session.

---

## Part B — the 10 scenarios, each fully walked

> Format: **picture → what's happening → the trade.** These expand the matrix in
> [[03 — How to Read a GEX Chart (interpretation)]] §4 with charts + reasoning.

### Scenario 1 — Positive GEX, above flip, below call wall → grind-up pin
```
  +│            ▇▇        ▇▇▇▇(call wall $66k)
  +│     ▇▇  ●  ▇▇        ▇▇▇▇
 ─┼─────╫──────────────────────  flip $62k (spot ABOVE)
  −│  ▁▁ ║
        $62k $63.3k      $66k
```
- **Happening:** dealers long gamma; every dip bought, every rip sold; price drifts up calmly toward the call wall.
- **Trade:** buy dips toward support, **sell into $66k call wall**; small targets; low vol; **do not chase breakouts.**

### Scenario 2 — Positive GEX, price AT the gamma wall → hard pin / chop
```
  +│           ▇▇▇▇●▇▇▇▇        ← spot pinned at the wall $64k
 ─┼───────────▇▇▇▇▇▇▇▇▇────
  −│  ▁▁
        $62k   $64k
```
- **Happening:** maximum hedging right here; pokes above/below get sold/bought straight back.
- **Trade:** **fade both edges of the pin**; scalp the range; expect chop, not trend. Stops just beyond the wall.

### Scenario 3 — Positive GEX, price NEAR the flip → unstable calm
```
  +│        ▇▇
 ─┼──────●─╫──────────────  flip right at spot → coin-flip which regime wins
  −│   ▁▁▁ ║
```
- **Happening:** net GEX small; the regime can tip either way on the next OI shift.
- **Trade:** **reduce size or stand aside**; wait for price to pick a side of the flip before committing.

### Scenario 4 — Negative GEX, below flip, above put wall → trend down
```
  +│
 ─┼──────────╫────────────  flip $64k (spot BELOW)
  −│    ▁▁  ●║
  −│ ▁▁▁▁▁  (put wall $61k)
     $61k $63.3k $64k
```
- **Happening:** dealers short gamma; they **sell into weakness** → downmoves accelerate; vol expands.
- **Trade:** **sell rallies / momentum shorts**; wider stops; targets toward the put wall. No dip-buying. *(This was the live BTC regime.)*

### Scenario 5 — Negative GEX, breaking the put wall → air-pocket / cascade
```
  +│
 ─┼─────────────────────
  −│ ▁▁▁▁●            ← spot punching THROUGH put wall $61k; nothing below
  −│ ▁▁▁▁  ↓↓↓ cascade
     $61k(broken)
```
- **Happening:** support strike breaks, OI doesn't reload lower → no dealer buying beneath → fast flush.
- **Trade:** **breakout short on the break**, expect acceleration; trail wide; cover into the next HVN/round number.

### Scenario 6 — Negative GEX, far from any wall → whippy two-way
```
  +│
 ─┼────────●──────────────
  −│ ▁    (no nearby wall)   ▁
     thin, scattered bars
```
- **Happening:** short-gamma so moves amplify, but no concentration to anchor → erratic.
- **Trade:** **momentum only, both ways**; avoid mean-reversion; smaller size, quicker exits.

### Scenario 7 — Price CROSSING the flip → regime change in progress
```
  before:  −│ ▁▁●        →  after:  +│      ●▇▇
          ─┼────╫──                ─┼──────╫──
             spot below flip          spot reclaimed flip
```
- **Happening:** you are leaving short-gamma and entering long-gamma (or vice-versa).
- **Trade:** **flip the playbook** — stop trading momentum, start fading extremes (or the reverse). Highest-information moment of the day.

### Scenario 8 — Positive GEX into EXPIRY → pin to wall / max-pain
```
  +│         ▇▇▇▇●▇▇▇▇       ← expiry day: magnet to gamma wall / max-pain $64k
 ─┼─────────▇▇▇▇▇▇▇▇▇──
   time → 08:00 UTC expiry
```
- **Happening:** front-week gamma dominates; pin risk high; price gets tractor-beamed to the wall/max-pain.
- **Trade:** **fade extensions toward the pin**; then **re-read GEX after the 08:00 UTC expiry** — the map resets.

### Scenario 9 — Negative GEX into EXPIRY → expiry-driven breakout
```
  +│
 ─┼──────────────────────
  −│  ▁▁▁●▁▁  low pin / high squeeze risk → break, don't fade
```
- **Happening:** short gamma + expiry → squeeze-prone, little pinning.
- **Trade:** **trade the break**, not the fade; reassess fresh after expiry.

### Scenario 10 — Positive → Negative flip just turned negative → calm to violent
```
  net GEX over time:   +++  ++  +  0  −  −−        ← just crossed into negative
                                    ↑ HERE: regime turned
```
- **Happening:** the book just left the pinning world; the next move can be unusually sharp (dealers switch from absorbing to amplifying).
- **Trade:** **the highest-alpha transition** — respect it; momentum setups light up, mean-reversion dies. Size for expansion.

---

## Part C — two end-to-end "session" walkthroughs

### Walkthrough 1 — the live BTC book (2026-06-20), short-gamma day
1. **Weather (Part A4):** net −96.37K → **short gamma → trend day.** Bias: follow, don't fade.
2. **Map levels:** squeeze support $63,000, resistance $63,000, **breakout $65,500**; spot $63,300.
3. **Locate spot vs flip:** spot sits right at support/resistance $63,000-ish cluster, below the breakout → **short-gamma half**.
4. **Scenario match:** this is **Scenario 4/6** (trend / whippy short-gamma).
5. **Plan:** sell rallies that stall below $65,500; if price **closes above $65,500** → **Scenario 5-style breakout long**, expect acceleration (short-gamma feeds it). No mean-reversion longs into support — in short gamma that support is weak.
6. **Risk:** wider stops (vol expands in short gamma); confirm with price action; don't trade the 15-min snapshot on a 1-min chart.

### Walkthrough 2 — a hypothetical pinning day (contrast)
1. **Weather:** net **+180K** → **long gamma → pin day.**
2. **Levels:** gamma wall $64,000, put wall $62,000, zero-gamma $62,500; spot $63,400 (above flip).
3. **Scenario match:** **Scenario 1** (grind-up pin below call wall).
4. **Plan:** buy dips toward $62,500–$63,000, **sell into $64,000 wall**; tight targets; fade the pokes (Scenario 2 if it reaches $64k).
5. **Invalidation:** a **close below $62,500 (zero-gamma)** = **Scenario 7 regime flip** → abandon the fade book, switch to momentum.

---

## Part D — the scenario decision tree (one glance)
```
              ┌─ net GEX > 0 (LONG gamma) ──► PIN world
              │       ├─ price below call wall ........ Scenario 1: buy dips/sell wall
              │       ├─ price AT a wall ............... Scenario 2: fade the pin
   START ─────┤       ├─ price near zero-gamma ........ Scenario 3: reduce/stand aside
   read net   │       └─ into expiry ................... Scenario 8: fade to pin, re-read after
   GEX sign   │
              └─ net GEX < 0 (SHORT gamma) ─► TREND world
                      ├─ above put wall ............... Scenario 4: sell rallies
                      ├─ breaking put wall ............ Scenario 5: breakout short / air-pocket
                      ├─ far from walls ............... Scenario 6: momentum both ways
                      └─ into expiry ................... Scenario 9: trade the break
   ANY TIME price crosses zero-gamma ................... Scenario 7/10: FLIP the playbook
```

→ The terse field-by-field reference: [[03 — How to Read a GEX Chart (interpretation)]]
→ The traps that void these reads: [[08 — Pitfalls and Misconceptions (what NOT to do)]]
→ Trade them as a system: [[07 — Trader Usage Playbook (how to use together)]]
