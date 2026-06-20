# Intraday Options Decision Engine — Exhaustive Research for Indian Intraday Index Options

> The master "decision engine" research that sits ABOVE the two strategy guides. Where `Breakout Trading/` trades the successful break and `Fakeout Reversal Trading/` trades the failed one, THIS note is the **one-decision spine** that decides — *before* the level — which of five plays applies, how heavily to weight each witness, what qualifies as a real level, and exactly how to translate a futures-point thesis into an options trade with a sized stop.
> For **Nifty 50 / Nifty futures** (and BankNifty / FinNifty / Sensex by extension), intraday, executed via index options (ATM / 1-OTM CE/PE). MTF funnel: **1h regime/bias → 15m level → 5m trigger.**
> Synthesis of: repo notes (`options-flow-india.md`, `options-flow-and-dealer-greeks.md`, `order-flow-options-backtesting-india-reference.md`, `volume-footprint-and-data-feeds-india.md`); the two sibling guides; four channel syntheses (Fractal Flow Pro, Tom Vorwald, Trader Dale, Photon Trading); books (Passarelli *Trading Options Greeks*, McMillan *Options as a Strategic Investment*, Sinclair *Volatility Trading*, Dalton *Mind Over Markets*, Coulling *VPA*, Trader Dale VP/OF, ICT/SMC, Douglas *The Disciplined Trader*); and India web sources.
> _Compiled June 2026. Every exchange-set value (lot size, weekly-expiry weekday, STT/charges) is flagged "verify current value on NSE/BSE" — SEBI changed the derivatives framework in late 2024 and again in 2025; these move._

---

## 1. The one-decision spine + the five plays

The engine collapses to **one question asked in a fixed order**: *given the regime, which play does THIS level support, and do enough witnesses agree to fire it?* Every channel converges on the same spine — read the **state of the market first, then match the tactic to the state** (Trader Dale: "the #1 structural mistake is using a trend strategy in a rotation, or vice-versa"; Vorwald: "context beats setups — setups come at step 8, not step 1").

The five plays are not five strategies; they are the **five legal verdicts** the engine can return at a level:

1. **Breakout** — balance→imbalance with acceptance beyond the level (the `Breakout Trading/` guide). Applies when: regime permits trend (negative-or-neutral GEX, away from max-pain), the level is a value edge / IB / OI wall, and effort+structure+options all confirm displacement.
2. **Fakeout reversal** — the failed transition; sweep-and-reverse back inside (the `Fakeout Reversal Trading/` guide). Applies when: regime favours mean-reversion (positive GEX, near max-pain, balance day), the level is swept but witnesses **refuse** to confirm (low-vol poke / absorption / CVD divergence / OI re-defense).
3. **Reversal at exhaustion** — a climax/V-reversal at an HTF extreme without a prior breakout to fade. Applies when: VPA climax (selling/buying climax, Coulling) or footprint absorption prints at a *naked* HTF level (prior-day VAH/VAL, naked POC, call/put wall) with CVD divergence — the move is ending, not pausing.
4. **Pullback / mitigation** — buy the retracement *into* an established trend at a fresh demand/supply zone (Photon: "trade FROM strong structure"; FFP: "be a pullback trader, never a breakout trader"; Vorwald: "continuation in trend, the 2nd test is the high-probability one"). Applies when: HTF is clearly trending and price pulls back to a fresh, HTF-aligned zone in discount (longs) / premium (shorts).
5. **Continuation** — the trend-leg resumption after a flag/BOS-pullback completes (a pullback that has already confirmed). Applies when: a BOS has occurred, price mitigated the OB/FVG, and a continuation candle fires in the trend direction.

> The engine's first job is to **collapse 5 plays to at most 2** using the regime read (§5): a positive-GEX / near-max-pain / balance session legalises {fakeout reversal, reversal, range pullback}; a negative-GEX / trend session legalises {breakout, pullback, continuation}. You should rarely be choosing among all five at once — the regime has already eliminated three.

**Spine in one breath:** *Regime decides the menu → the level decides where → the at-level reaction decides HOLD/BREAK/WAIT → the LTF decides when → the options layer decides what to buy and how much to risk.* Options data sets the **environment**; the chart pulls the **trigger** (repo: options-flow-india.md §5).

---

## 2. Weighted confluence: how to weight the witnesses, and how weights shift by regime

The sibling guides count confluences equally (a 6-of-10 scorecard). The decision engine upgrades this to a **weighted** vote because not all witnesses are equally trustworthy in India, and their weights **shift with regime**.

The three witness buckets (from the breakout note's 3-witness model, here generalised):
- **STRUCTURE** (price action / SMC): the level, the close, BOS vs CHoCH, sweep-and-go vs sweep-and-reverse.
- **EFFORT** (volume profile + order flow): where institutions traded (VP: POC/HVN/LVN/value), and who is the aggressor now (footprint delta/CVD, absorption, stacked imbalance).
- **OPTIONS** (the India edge): OI structure & change-in-OI, premium/IV expansion, GEX/max-pain/PCR.

**Base weights (India default, OI-driven market):** because India is "an OI-driven market, not a GEX-driven one" (repo: options-flow-india.md §0), the options bucket carries *more* weight than the equivalent US framework would give it, but **OI structure** is the high-trust sub-witness while **GEX is secondary** ("lead with OI, use GEX as a confirming overlay"). A workable base split: **Structure ~35%, Effort ~30%, Options ~35%** — with the options 35% itself split ~25% OI/change-in-OI + ~10% GEX/max-pain/PCR.

**How weights shift by regime:**

| Regime | Up-weight | Down-weight | Why |
|---|---|---|---|
| **Expiry afternoon (weekly)** | Options (OI walls, max-pain, GEX) → ~50% | Structure breaks | Gamma is enormous; pinning/max-pain pull dominates; a 5m close-beyond means little vs an OI wall (repo: options-flow-india.md §5; breakout note §16) |
| **Event day (Budget/RBI/results)** | Effort (VPA climax, footprint) + IV context | OI change (laggy, distorted by hedging) | India VIX spikes; IV-crush risk; favour reading the *reaction after* the spike, not OI which is full of hedges |
| **Trend day (negative GEX, thin profile)** | Structure (BOS) + Effort (CVD, stacked imbalance) | Mean-reversion/PCR signals | "Do not fade"; momentum is the edge; OI-wall *resistance* is unreliable when dealers hedge with the move |
| **Balance day (positive GEX, D-profile)** | Options (walls as range) + VP value edges | Breakout structure | Edges hold; the walls ARE the range; breakouts fail (repo: options-flow-and-dealer-greeks.md §3.2) |
| **First 15 min / lunch chop** | Nothing — *raise the bar* | All | Low-vol "feel-out" trap candles (VPA, Coulling Figs 4.12–4.13); breaks are "disproportionately fake" (breakout note §14) |

**The veto rule (more important than the vote):** some witnesses are not additive but **vetoing**. A CVD divergence, footprint absorption, or a naked POC sitting against your trade is a *veto* that overrides a high confluence count (breakout note §12; Trader Dale: absorption is "my favourite reversal signal"). The engine fires only when **the weighted vote clears threshold AND no veto is active.**

---

## 3. Level mapping + the DECLUTTER filter

The hardest skill is not finding levels — every framework generates dozens (OBs, FVGs, swings, HVNs, walls, VWAP, PDH/PDL). The engine's value is the **declutter filter**: which levels *qualify* to be traded, and which to delete from the chart entirely (memory: charts use ONLY the qualifying levels, decluttered).

**The four-gate qualification filter** (a level must pass all four to stay on the chart):

1. **FRESH / unmitigated.** First-touch only. Photon's strongest filter ("unmitigated extreme = strongest reaction; you're only wrong once"); Trader Dale ("first touch only, second tests have much worse win rates"); FFP ("freshness — untested first-touch best"). **Delete** any OB/FVG/zone already tagged.
2. **HTF-ALIGNED.** The level must come from the 1h/15m, and ideally stack with a higher-TF zone. "HTFFVG > LTFFVG" (ICT); Photon's "stacked with a HTF zone" + "HTF alignment" criteria. **Delete** 5m-invented levels — "the 5m never invents a level" (breakout note §13).
3. **NEAR PRICE & IN THE RIGHT HALF.** Within ~1 ATR of price (actionable today, not theoretical), and on the correct side of equilibrium: demand in **discount**, supply in **premium** (Photon; ICT). **Delete** levels deep on the wrong side of the day's range.
4. **CAUSAL / DEFENDED.** It must have *done something*: caused a BOS (Photon's #1 criterion), shown a strong single-rejection (Trader Dale's "strong high/low"), carries real volume (an HVN, not a thin print), or is an OI wall. **Delete** "weak highs/lows" as levels — they are *liquidity to be run*, not levels to trade from (ICT; Photon: "a low's job is to make a high").

**The qualifying level types (after the filter), ranked by India trust:**
- **OI walls** (highest call-OI strike = ceiling, highest put-OI strike = floor) — the India-specific top-trust level; the band between them IS the implied range (repo: options-flow-india.md §2.2).
- **Prior-day VAH / VAL / naked (virgin) POC** — institutional value edges and magnets (Trader Dale; Vorwald: "daily business zones from value areas").
- **IB / opening-range high & low** — engineered liquidity, the day's primary intraday levels (breakout note §14).
- **PDH / PDL** — major reference & liquidity pools.
- **VWAP (+ first deviation band)** — the live institutional benchmark and itself a magnet/level (Trader Dale; Vorwald: "VWAP only with context").
- **A fresh, BOS-causing, HTF-aligned OB / FVG** in discount/premium — the SMC entry zone.

> **The declutter discipline:** an HVN/swing/OB/FVG that fails any gate is *noise on the chart*. The single biggest source of intraday losses is trading an unqualified level — a stale FVG, a weak high, a 5m-invented "support." Keep ≤4–5 qualifying levels marked at any time.

---

## 4. The open read + the news/event/expiry filter

Before the first trade, the engine runs a **pre-session classification** (Vorwald's 13-step prep compressed): *Is today even tradeable, and what kind of day is it?*

**The gap / open read (sets the day's character):**
- **Gap UP into resistance (prior-day VAH / call wall / PDH):** premium-zone open; fade-risk high; watch for an opening-drive that *accepts* (real) vs a gap-fill rejection (fakeout reversal candidate). A gap that fills back into prior value = bearish acceptance.
- **Gap DOWN into support (prior-day VAL / put wall / PDL):** discount open; the mirror — spring/long-fade candidate or downside continuation.
- **FLAT open inside prior value:** balance bias; expect rotation and an IB-range day; favour edge-fades until the IB breaks on effort.
- **Open DRIVE (gaps and runs, no rotation):** trend-day signature; thin profile forming; favour pullback/continuation, never fade (Vorwald: "open drive"; Dalton: trend day).

**Initial Balance (IB):** the first hour's high/low (9:15–10:15 IST). Width relative to ADR is the single best early day-type tell — a **narrow IB (<~30–40% of ADR)** = coiled, breakout-prone day; a **wide IB** = the day's range may already be spent, favouring rotation/fade (breakout note §14–15; Dalton). The IB high/low are simultaneously the day's primary breakout levels AND the engineered liquidity pool (the equal-high/low where stops sit).

**The hard filters (these *forbid* trades, not just downgrade them):**
- **News timetable:** mark high-impact prints (RBI policy, CPI/GDP, Budget, US Fed, major results). Don't initiate day-trades into a high-impact print; let the spike happen, then read the reaction (Vorwald step 1; Trader Dale: "pull limit orders before FOMC"; breakout note §16). India VIX rising into an event = rich premium + IV-crush risk afterward.
- **Overnight shock / large gap:** "any big overnight gap → often best to do nothing" (Vorwald step 2).
- **Expiry day (weekly):** the most important India filter. **Verify the current weekly-expiry weekday on NSE/BSE** — as of mid-2026, NSE Nifty weekly expires **Tuesday** and BSE Sensex weekly expires **Thursday** (post-Sep-2025 SEBI reshuffle; previously Thursday) (web: HDFC Sky, Ventura, Tejimandi). On expiry afternoon, **the options weights dominate** (§2) and the base case is **pinning toward max-pain**, not directional expansion (§5, §8).

---

## 5. Regime: deciding fade-vs-break BEFORE the level

This is the engine's pivot. The regime read **happens before price reaches the level** and decides whether you are hunting breaks or fades today. Five regime sub-reads, in priority order for India:

**5.1 Balance vs Trend (Auction Market Theory — Dalton; Vorwald; Trader Dale).** Every market is in one of two states: **balance (~65–70% of the time)** — fair value, rotation → trade *counter* (fade edges back to POC/VWAP); or **trend/imbalance (~30%)** → trade *with* it (pullback continuation), never counter (Vorwald §0; Trader Dale "four states"). Profile shape reads it: **D-shape = balance**; **P/b-shape = directional**; **thin profile = trend day**. A **failed auction / poor high / poor low** (Dalton) signals balance trying and failing to extend — a fade tell.

**5.2 GEX / dealer gamma (the regime overlay).** **Positive GEX (dealers long gamma)** → they fade moves → **suppressed vol, pinning, mean-reversion, breakouts FAIL** → legalises fades/reversals. **Negative GEX (dealers short gamma)** → they hedge *with* the move → **amplified vol, trends, breakouts WORK, do not fade** (repo: options-flow-and-dealer-greeks.md §3.1; FFP §7: "gamma determines HOW price approaches a level"). The **gamma flip / zero-gamma level** is the regime switch; the **Peak-GEX strike** is a magnet; **Call Wall = upside ceiling, Put Wall = downside floor; spot oscillates between them on positive-GEX days** (web: stockmojo, justticks, Vtrender). **India caveat:** the "short gamma → trend" causality is *weaker* than in the US because much OI is retail/prop, not dealer-hedged — read India GEX as "where are the pinning/acceleration magnets," and **lead with OI, confirm with GEX** (repo: options-flow-india.md §4).

**5.3 IV / India VIX (the go/no-go for option BUYING).** This is the most important *vehicle* filter and the one the sibling guides under-developed. **Compare current IV to its own recent distribution** (a volatility cone / percentile), not to an absolute level — "selling one-month implied volatility at 35% because this is in the 90th percentile for one-month volatility over the past two years can form the basis of a sensible trading plan" (Sinclair, *Volatility Trading*, volatility cone). Practical India version using **IV Rank / IV Percentile**:
- **Low IV rank (cheap premium)** → favours **option BUYING** (you win from delta *and* a likely IV rise on the move). Green light for the buy-the-option engine.
- **High IV rank (rich premium)** → option buying is taxed by IV-crush risk; the move must be large and fast to overcome it. **Red/amber for buying**; favours spreads or trading the future. India VIX elevated pre-event = this regime (repo: options-flow-india.md §2.5; breakout note §7.3).
- Volatility is **mean-reverting and clusters** — "a good estimate of future volatility is whatever current volatility is" near-term, but extremes revert (Sinclair: vol clusters, mean-reverts, "large changes followed by large changes"). So a high-IV-rank reading is also a *warning that IV will likely fall*, hurting a long-option holder.

**5.4 PCR (sentiment lean).** OI-based PCR: **>1.3–1.5 = heavy put writing = support beneath / bullish lean**; **<0.7 = heavy call writing = capped / bearish lean**; **extremes are contrarian** (repo: options-flow-india.md §2.3). Mid-range PCR is noise.

**5.5 Max-pain & range-vs-expansion.** Into weekly expiry, price **gravitates toward max-pain** (where writers profit most), strongest when it aligns with the OI walls (repo: options-flow-india.md §2.4). On expiry afternoon this makes the day a **range/reversion day by default** — *moves away from max-pain that fail to migrate OI are fade candidates; max-pain becomes the reversal TARGET* (`Fakeout Reversal Trading/research.md` §6.5).

> **Regime output:** a single label — e.g., *"Positive-GEX balance day, mid PCR, low IV-rank, spot 60 pts above max-pain into Tuesday expiry"* → the engine pre-selects **fade/reversal plays**, targets max-pain, and **green-lights option buying** (cheap IV). That one sentence eliminates three of the five plays before the level is even tested.

---

## 6. The at-level reaction read: HOLD vs BREAK vs WAIT

When price arrives at a qualifying level, the engine reads the **reaction** — "the reaction to the level is more important than the level itself" (FFP §1). Three verdicts:

**HOLD (the level defends → fade / reversal / pullback-bounce).** The level repels price. Tells:
- **Sweep + reject:** a wick beyond the level, **close back inside** (SFP / turtle-soup close); a shooting star (upside) or hammer (downside) at the extreme (`Fakeout Reversal/research.md` §3–4).
- **Absorption:** heavy volume on **both bid AND ask** at the level, price doesn't move — "one side absorbed → reversal" (Trader Dale, OF); the VPA twin is a narrow-spread/high-volume bar (Coulling).
- **CVD divergence:** price makes a new extreme but cumulative delta does NOT — buyers/sellers exhausting. **The single most trustworthy order-flow read in India** (survives inferred-aggressor misclassification on NSE feeds) (repo: volume-footprint-and-data-feeds-india.md §10).
- **OI re-defense:** the swept strike's OI *rises or holds* (writers adding/defending), no migration to the next strike, premium fails to expand (repo: options-flow-india.md §2.2).

**BREAK (the level gives way → breakout / continuation).** The level fails. Tells:
- **Acceptance:** a wide-bodied conviction **close beyond** (body ≥60–70% of range), new value building outside the old value area (Trader Dale acceptance-vs-rejection; breakout note §8).
- **BOS / displacement:** a close beyond a prior swing in the trend direction, leaving an FVG (ICT).
- **Delta expansion + stacked imbalances:** rising CVD, 3+ diagonal cells ≥300% one side (Trader Dale; breakout note §9).
- **OI migration:** wall OI *drops* at the broken strike (writers capitulating), fresh OI builds at the next strike, premium expands (repo: options-flow-india.md §2.2).

**WAIT (ambiguous → no trade yet).** The make-or-break fork is unresolved: the sweep candle is still forming, CVD is flat, OI hasn't updated (NSE change-in-OI lags 3–5 min). **Do not chase the spike** — wait for the close, and ideally the retest (breakout note §3). "When to wait vs not": wait when only one bucket has spoken; act when two buckets agree and no veto is live.

**The hammer + sweep continue-vs-reverse fork (the subtle case the prompt flags):** the *same* hammer-at-a-low after a sweep can mean two opposite things:
- **Reverse (long the bounce):** the sweep took sell-side liquidity below a *strong* low / put wall, CVD diverges (sellers exhausting), OI re-defends (put writers hold), regime is positive-GEX/balance → the hammer is a **spring** → reversal up.
- **Continue (the down-move resumes):** the same hammer sits below a *weak* low in a negative-GEX **trend** day; the "absorption" is fleeting and price blows through — "every sweep is a sweep-and-go even when it looks like a fakeout" (`Fakeout Reversal/research.md` §8, the cardinal error). **The regime (§5) is the tiebreaker:** a hammer-sweep in positive-GEX/balance = reverse; in negative-GEX/trend = it's a pullback to *continue*, not a reversal. This is why regime is read *before* the level.

---

## 7. LTF entry: which lens when, and the footprint / FVG deep-dive

Once the at-level verdict and the play are set, the engine picks the **LTF entry lens** appropriate to the play — you do not use all lenses for all plays.

**Which lens when:**
- **Breakout / continuation** → **price-action conviction close** + **retest hold** (the A+ entry); confirm with **order-flow stacked imbalance / rising CVD**. SMC for the BOS/OB-retest.
- **Fakeout reversal / reversal** → **SMC sweep→CHoCH→reclaim** + **CVD divergence** (top tell) + **price-action rejection wick/close-back-inside**.
- **Pullback / mitigation** → **VP/supply-demand zone edge** (Trader Dale "edge of the zone, first touch") + **VWAP-pullback** (Vorwald: in a trend, buy the pullback *to* VWAP) + a reaction candle (FFP fractal candle).

**Footprint deep-dive (the order-flow execution layer).** A footprint explodes each bar into **bid (sell-initiated) × ask (buy-initiated)** volume per price; **Delta = Ask − Bid**, **CVD = running sum** (repo: volume-footprint-and-data-feeds-india.md §1). The four reads, ranked by India reliability:
1. **CVD divergence** — most trustworthy; less sensitive to per-trade aggressor misclassification (repo §10).
2. **Absorption** — huge volume both sides, no price progress = reversal (Trader Dale's favourite).
3. **Stacked imbalance** — 3+ diagonal cells ≥300% one side = initiative (compare ask at a price vs bid *one tick below* — imbalance is diagonal, not horizontal; repo §10).
4. **Per-cell raw numbers** — least trustworthy; treat as probabilistic.

**The India paid-data reality (critical execution constraint):** NSE gives **no aggressor flag** on retail feeds, so all footprint is **inferred** (quote/tick rule). Grades: **Grade 1** true order-by-order TBT = institutional/colo only (lakhs/yr); **Grade 2** vendor tick (GoCharting's own feed, TrueData, GDFL, AccelPix) = the realistic retail ceiling; **Grade 3** broker snapshot (~1 packet/sec, Kite/Dhan) = roughest (repo: order-flow-options-backtesting-india-reference.md §2–3). **Recommended:** GoCharting Premium (~₹1,499/mo, Grade-2). **Free fallback:** GoCharting Bar Replay for practice, or rely on **CVD-divergence shape + VPA** when only Grade-3 broker data is available. **Always run footprint on the Nifty FUTURE, never the option strike** (thin strikes/wide spreads make option footprint unreliable — repo: volume-footprint-and-data-feeds-india.md §6).

**FVG-on-LTF mastery + failure modes.** A Fair Value Gap is a 3-candle inefficiency left by displacement; a real break *creates* one, and price often retraces to fill it before continuing (ICT). The entry: pullback into the FVG (often confluent with an OB) → confirmation candle → enter, stop just past the OB/swept extreme (breakout note §10). **Failure modes the engine must screen for (FFP + Vorwald are the skeptics here):**
- **FVGs only act as S/R ~30% of the time** — "in a stable trend with a small opening range"; in balance (~70%) they get traded straight through (Vorwald §2). So an FVG entry is *regime-dependent*: trust it in trend, distrust it in balance.
- An FVG is "a misleading name" — it works because it hides a **Low Volume Node** (FFP §3); judge it by liquidity-before-vs-after and the structure underneath (Vorwald), and **only trade fresh/untested gaps** (Trader Dale).
- **First test holds, second test usually breaks** (Vorwald). Discard a missed/tested FVG.
- A "full-fill" FVG that price closes straight through = the displacement is being reclaimed = the move is failing (ICT mitigation).

---

## 8. The options layer (MOST IMPORTANT): strike, stop, target, sizing, timing, exit

This is the layer the Western books and channel syntheses lack and where the engine earns its keep. The futures-side analysis produces a **thesis in index points**; this layer converts it into a **sized options trade**.

**8.1 Strike selection — ATM vs 1-OTM.** Buy **ATM or 1-OTM** for intraday directional plays. ATM delta ≈ 0.50; 1-OTM ≈ 0.35–0.45 (repo/Passarelli below). ATM gives cleaner delta P&L and tighter spreads; 1-OTM gives more leverage/lower cost but more theta + IV-crush drag. **Avoid far-OTM weeklies** — the bid-ask spread alone can be 5–15% of premium and theta guts them (breakout note §16). On a high-conviction trend with a big expected move, slightly-ITM reduces theta/IV drag.

**8.2 Option-SL via DELTA (the core conversion).** Delta is **the futures→option price-change ratio**: "the delta of a futures option... is the amount by which the option is expected to increase in price for a one-point move in the underlying futures contract" (McMillan, *Options as a Strategic Investment*, Options on Futures ch.). Equivalently: ATM ≈ 0.50, so a 1-point Nifty move ≈ 0.50-point premium move (Passarelli, *Trading Options Greeks* ch.2 Def.1: "if an option has a 50 delta, its price will change by 50 percent of the change of the underlying"; web: Zerodha Varsity, Sahi). **Rule of thumb:** *premium stop ≈ delta × index-point stop.*
- A **30-point** Nifty stop on an ATM option ≈ **~15 points** of premium (0.50 × 30) (web: Sahi, Zerodha).
- A **40–60-point** stop ≈ **~20–30 points** of premium.
- For 1-OTM (delta ~0.40): a 30-pt stop ≈ ~12 pts premium.

**Delta DRIFT (the trap the rule-of-thumb hides):** delta is *not constant* — it changes via **gamma** as price moves ("when the stock price increases by $1, the delta increases by the amount of the gamma... at $62 the call's delta is 0.58" — Passarelli ch.2). A winning long-call's delta *rises* (premium accelerates — good); a losing call's delta *falls* (loss is sub-linear). Practical consequence: **size the stop off entry delta, but expect the realised premium stop slightly *smaller* than delta×points on the adverse move** (delta shrinks against you) and *larger* on the favourable move. ATM futures-call delta is also slightly **>0.50** (futures price distribution, no carry) — don't assume exactly 0.50 (McMillan). **Equivalent Futures Position (EFP) = options × delta** (McMillan): 1 ATM lot ≈ half a futures lot of directional exposure.

**8.3 Option-SL via ATR (the regime-aware sizing of the futures move).** Set the *index-point* stop with ATR, then convert via delta. Use **5m/15m ATR × multiplier** for the expected move / stop distance: classic intraday multipliers are **~2× ATR** (supertrend 7,2 on 5m or 10,3 for slower; web: MQL5, Mudrex, elearnmarkets). A tighter buffer (~0.3–0.5× ATR beyond the swept wick) suits fakeout-reversal stops (precise invalidation); a wider buffer (~0.5–1.0× ATR beyond the level) suits breakouts (avoid the stop-hunt) (sibling guides §10/§7.2). **Widen ATR multiplier on negative-GEX/event days** (overshoots), **tighten on positive-GEX/balance days**.

**8.4 Per-instrument stop budget (the point scales — VERIFY all on NSE/BSE).** The same % risk implies different *point* stops per index because they move at different scales. **BankNifty moves ~2–3× Nifty** in points, so its point-stop budget and ATR are correspondingly larger; Sensex ≈ BankNifty scale; FinNifty ≈ Nifty-ish. Indicative per-trade *index-point* stop budgets (calibrate to live ATR): **Nifty ~25–50 pts; BankNifty ~60–150 pts (≈2–3× Nifty); FinNifty ~30–60 pts; Sensex ~80–200 pts.** **Lot sizes (VERIFY — these changed Jan 2026 and keep changing):** as of the Jan-2026 NSE revision, indicative **Nifty 65, BankNifty 30, Sensex 20** (web: Sahi, HDFC Sky, Ventura; FinNifty not confirmed in sources — check NSE). **Weekly expiry (VERIFY):** Nifty = Tuesday (NSE), Sensex = Thursday (BSE); BankNifty/FinNifty weekly were discontinued (monthly-only) under SEBI's one-weekly-per-exchange rule (repo: options-flow-india.md §1; web: HDFC Sky, Tejimandi).

**8.5 Targets.** T1 = nearest qualifying barrier in the path: **next OI wall / next HVN / VWAP-extension / measured-move** of the range. T2 = **naked POC / prior-day VAH-VAL extreme / next liquidity pool**; on expiry, **max-pain** (the strongest expiry target). Use **naked POCs / failed auctions as magnets** — stretch the target to *just beyond* them, never set it just short (Trader Dale). Inside a D-profile, **POC is the natural target**; in a thin/trend profile, **trail**. Convert each index-point target to premium via delta to read the realised RR.

**8.6 RR + 1-lot sizing.** Define R in **index points**, convert entry/stop/target to premium via delta, then size: **Lots = floor[(Capital × Risk%) ÷ (|entry premium − stop premium| × lot size)]**, keeping premium-at-risk ≤ the 1–2% rule. Because option P&L is **non-linear** (delta + theta + IV), demand **gross RR ≥ 1:2** before costs to net ~1:1.5 after STT/brokerage/spread (~3–6 pts round-trip on ATM weeklies) (sibling guides). A correct-direction trade can still lose if **theta + IV-crush** outrun the delta gain — which is why §5.3 (IV rank) and §8.7 (timing) gate the trade.

**8.7 Option-buying timing (theta / IV-rank).** Two timing gates:
- **IV-rank gate (§5.3):** buy options when IV rank is **low-to-moderate** (cheap premium, room for IV to expand on the move); avoid buying into **high IV rank** (IV-crush will fight you). Sinclair's vol-cone/percentile is the principled version.
- **Theta gate (intraday decay):** **ATM options decay at a NONLINEAR, accelerating rate as expiry approaches** — "ATM options tend to decay at a nonlinear rate... they lose value faster as expiration approaches," and the acceleration continues into the final days (Passarelli ch.2, theta; Exhibit 2.12 "theta as expiration approaches"). On **weekly options, the back half of the week and especially expiry afternoon** is where theta bites hardest. There is also an **intraday "taking the day out"** effect — traders remove the day's theta from their models mid-session once price stabilises, so premiums get cheaper through the day even with no price move (Passarelli ch.2). **Implication:** option *buying* is most efficient **early in the move and early in the week**; on expiry afternoon, theta + pinning make long-premium directional buying a low-EV game unless the move is fast and large (favour the fakeout-reversal-toward-max-pain play instead). Post-~2:30pm IST on weekly expiry, treat directional option *buying* with maximum suspicion.

**8.8 Mid-trade early exit (thesis-broke-before-SL).** The most valuable discretionary rule the engine adds: **exit when the THESIS breaks, even before the hard SL.** If you entered a breakout-continuation and CVD rolls over / absorption appears / OI stops migrating / the option premium *fails to expand* on the favourable futures tick — the reason for the trade is gone; exit now, don't wait for the point-stop (Vorwald: "read acceptance, not your bias... don't bang your head against a wall"; `Fakeout Reversal/research.md` §7.2 invalidation rule). Premium non-expansion on a correct-direction futures move is the clearest "thesis broke" tell on the options side.

---

## 9. Risk governance

Risk governance is *engine-level* (caps that override any single trade):
- **Per-trade risk:** **1–2% of capital** (FFP 0.5–1%, Photon 1%, Trader Dale ~2% — converge on a fixed, constant %; "inconsistent sizing is the #1 cause of blowups," Trader Dale). Size by rule, the same every time regardless of conviction.
- **Daily loss limit:** stop the day after **N losses (typically 2–3)** or a fixed ₹/% daily drawdown — the universal anti-tilt rule (Photon "max 3 losses/day then stop"; breakout note §11; Douglas: predefined limits prevent revenge trading).
- **Max trades / day:** few, high-conviction A+ trades beat many B-grade ones (Trader Dale's prop study: winners traded "few setups on 1–3 markets"; Photon ~10 trades/*month*). Cap intraday entries (e.g., ≤3–4) to force selectivity.
- **Correlated exposure:** don't stack Nifty + BankNifty + FinNifty longs as if independent — halve size on correlated positions (Trader Dale).
- **Psychology under tight capital (Douglas, *The Disciplined Trader*):** "fear narrows perception → creates the loss" — under capital stress you perceive only what you fear, chase the spike (FOMO) or freeze at the retest. The cure is a **pre-defined process**. Think in **probabilities** — each trade has *defined risk* and an uncertain outcome; only the *set* of A+ setups is +EV. **"Learn to take a loss"** — refusing to liquidate an acknowledged loser is the cardinal error. FFP's **Spectral Point of No Return**: overconfidence after a winning streak is *more* dangerous than a losing run — tighten governance after wins, not just losses.

---

## 10. Backtest spec

The honest India architecture (repo: order-flow-options-backtesting-india-reference.md): **futures order-flow/VP signal = the trigger; options historical = the option leg.**

**Signal side (GoCharting on the FUTURE):** compute the footprint/VP/CVD signal in **Lipi** (GoCharting's scripting — exposes `delta`, `maxdelta`, buy/sell volume, aggressor direction, volume imbalance). Backtest the *futures* signal in-platform; export the **signal** (timestamp + direction, +1/−1) via **CSV** (webhooks are live-only). Footprint data itself cannot be exported — only the signal.

**Option side (Dhan):** Dhan Data API (~₹499/mo, or free with 25+ trades/mo) gives **expired options history up to 5 years, minute-level, OHLC+IV+OI+Volume+Strike+Spot, ATM±10** — ideal for ATM/near-ATM strategies (not far-OTM/full-chain). For each signal timestamp, pull the ATM CE/PE and simulate entry/exit/P&L in Python.

**Parameter grid (sweep in Python/VectorBT — option-side params are fully automatable; signal-side params require CSV re-export per setting):**
- **Stop budget:** ATR multiple (0.3 / 0.5 / 1.0 / 2.0×) and/or fixed index-point budget per instrument.
- **RR / target rule:** fixed 1:2 / 1:3 vs structure-target (next wall/HVN/max-pain) vs trail.
- **Confirmation strictness:** weighted-vote threshold (e.g., fire at ≥0.55 vs ≥0.70) and veto on/off.
- **Regime filter:** all-sessions vs {positive-GEX→fades only, negative-GEX→breaks only} vs IV-rank gate for buying.
- **Strike:** ATM vs 1-OTM vs slightly-ITM; entry-time-of-day buckets (open-drive / mid-morning / lunch / expiry-afternoon).

**Metrics:** win rate, **expectancy / avg R-multiple** (the real edge metric, not win rate — Photon/FFP), profit factor (>2 = prop-grade, Trader Dale), max consecutive losses, max drawdown, and **net-of-cost** P&L (STT + brokerage + bid-ask spread modelled, ~3–6 pts/round-trip ATM weekly). **Discount the backtested win rate by 5–10%** for live use (Photon). Walk-forward the regime filter separately for expiry vs non-expiry days.

---

## 11. Learning / training path

Staged drills with exit tests, mapped to the channel CONCEPTS and FREE_CURRICULUM (repo):

- **Stage 0 — Foundations.** Market structure (HH/HL, BOS/CHoCH), risk math (break-even WR = 1/(1+RR); 1:3 → 25%), reading a clean decluttered chart. *Sources:* FREE_CURRICULUM Stages 0–1, FFP §1–2, Photon §1. **Exit test:** mark swings + define a 1:3 trade with entry/stop/target without hesitation.
- **Stage 1 — Regime classification (the engine's first skill).** Drill labelling each session *before* trading: balance vs trend (Dalton/Vorwald), GEX sign, IV rank, PCR, distance to max-pain, gap/IB read. *Sources:* §4–5, Vorwald 13-step, repo options-flow-india.md. **Exit test:** write the one-sentence regime label (§5) for 20 historical opens and predict fade-vs-break; score against what happened.
- **Stage 2 — Level mapping + declutter.** Drill the four-gate filter; mark ≤5 qualifying levels on blank charts; delete the rest. *Sources:* §3, Trader Dale VP, Photon 8-criteria. **Exit test:** on a fresh chart, justify each kept level against all four gates and name what you deleted and why.
- **Stage 3 — The at-level reaction read.** Bar-replay drilling HOLD/BREAK/WAIT, the hammer-sweep fork, sweep-and-go vs sweep-and-reverse. *Sources:* §6, both sibling guides. **Exit test (GoCharting free Bar Replay):** classify 30 level-touches as HOLD/BREAK/WAIT and call the play; ≥70% correct on replay.
- **Stage 4 — LTF entry lenses + footprint/FVG.** Drill the lens-per-play mapping; read CVD divergence, absorption, stacked imbalance on the future; FVG failure modes. *Sources:* §7, Trader Dale OF, ICT, Vorwald (FVG ~30%). **Exit test:** annotate sweep→CHoCH→reclaim and a breakout-retest with the correct LTF lens and confirmation.
- **Stage 5 — The options layer.** Drill delta-conversion (point-stop → premium-stop), delta drift, ATR sizing, per-instrument budgets, IV-rank/theta timing, lot sizing, thesis-broke exit. *Sources:* §8, Passarelli, McMillan, Sinclair, FREE_CURRICULUM Stage 5. **Exit test:** given a 40-pt Nifty thesis at a stated ATM delta + IV rank, produce strike, premium-stop, lots at 1.5% risk, T1/T2, and the no-trade condition.
- **Stage 6 — Governance & psychology.** Daily-loss-limit and max-trades discipline, journaling each play-type *separately* (Vorwald), probability mindset (Douglas), post-win caution (FFP). *Sources:* §9, Douglas, Photon §9, FFP §10. **Exit test:** run 1 week of paper trades obeying the daily limit and journal by play-type; review expectancy per play.
- **Stage 7 — Integration + backtest.** Run the full engine on replay, then the §10 backtest. **Exit test:** a forward-tested edge (expectancy >0, profit factor >1.5 net of costs) on ≥1 month of Nifty data, with the regime filter validated separately for expiry days.

---

## Open gaps / verify on live chart

- **All exchange-set values:** lot sizes (indicative Nifty 65 / BankNifty 30 / Sensex 20 post-Jan-2026; **FinNifty unconfirmed**) and weekly-expiry weekdays (Nifty Tue / Sensex Thu; BankNifty/FinNifty monthly-only) — **re-verify on NSE/BSE before sizing any trade**; SEBI keeps revising these.
- **Per-instrument point-stop budgets:** calibrate the Nifty/BankNifty/FinNifty/Sensex ATR-based stop ranges to *current live ATR* — the BankNifty ≈ 2–3× Nifty multiple drifts with regime; measure on 5m/15m.
- **Delta-drift magnitude:** quantify on live Nifty weeklies how far the realised premium-stop deviates from delta×points as the option goes ITM/OTM intraday (gamma effect) — is the rule-of-thumb off by 10%? 25%?
- **IV-rank go/no-go threshold:** determine the India VIX / option-IV-rank percentile cutoff above which intraday option *buying* turns negative-EV due to IV-crush — build a Nifty-specific volatility cone.
- **Intraday theta curve:** measure the actual post-2:30pm-IST premium decay on Nifty weekly ATM on expiry day (Tuesday) — quantify the "taking the day out" cheapening to set the latest sensible buy time.
- **GEX causality in India:** validate on replay whether published Nifty/BankNifty GEX/gamma-flip levels (justticks, stockmojo, Vtrender) actually mark pinning vs trending sessions — the repo flags weaker causality than the US.
- **Weighted-vote thresholds:** backtest the §2 weights and the fire-threshold; confirm which veto (CVD divergence vs absorption vs OI re-defense) is most predictive in each regime.
- **OI-change latency:** confirm how many minutes NSE change-in-OI lags the price move on Sensibull/Opstra/NSE chain — decides whether OI is usable as a *trigger* or only *confirmation* in the at-level read.
- **Footprint fidelity on Grade-3:** confirm whether broker-snapshot (Dhan/Kite) CVD-divergence shape is clean enough to trade, or whether GoCharting Grade-2 is mandatory for the at-level read.
- **Cost model:** build the exact STT/brokerage/spread round-trip drag per ATM Nifty/BankNifty/Sensex weekly to fix the true minimum gross RR per instrument.
- **Hammer-sweep fork base rates:** on replay, count how often a hammer-after-sweep reverses vs continues, split by GEX regime, to validate that regime is the correct tiebreaker (§6).

---

### Source legend
(Passarelli) = *Trading Options Greeks*, Dan Passarelli, 2nd ed. · (McMillan) = *Options as a Strategic Investment*, 5th ed., L.G. McMillan · (Sinclair) = *Volatility Trading*, 2nd ed., Euan Sinclair · (Dalton) = *Mind Over Markets*, James Dalton (Auction Market Theory) · (Coulling/VPA) = *A Complete Guide to Volume Price Analysis*, Anna Coulling · (Trader Dale, VP/OF) = Volume Profile / Order Flow golden-ticket books · (ICT) = *Advanced ICT / Institutional SMC* 2024 · (Douglas) = *The Disciplined Trader* · (FFP / Vorwald / Trader Dale / Photon) = repo channel `CONCEPTS.md` syntheses · (repo: …) = existing repo notes · (web: …) = India web sources (Sahi, HDFC Sky, Ventura, Tejimandi, Zerodha Varsity, justticks, stockmojo, Vtrender, MQL5, Mudrex, elearnmarkets).
