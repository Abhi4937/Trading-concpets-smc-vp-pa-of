# ORB (Opening Range Breakout) — what the local book library actually contains

**One-line verdict:** None of the ~20 PDFs in `books/` teach a formal, named "Opening Range Breakout" strategy. The closest, usable material is **session-/day-open price-behaviour trading** in Trader Dale's *Volume Profile: The Insider's Guide* (Open-drive, Session Open, Daily Open, Daily High/Low) and the **Asian-range / session-range model** in the two SMC/ICT books. *VWAP* (Trader Dale) adds the opening-gap-anchored VWAP, the nearest VWAP-to-ORB confluence. The volatility books (Sinclair, Warner, Bennett, McMillan-by-title, Passarelli) contain **zero** ORB content — "opening price" appears there only in the options/gamma sense. There is **no mention of Toby Crabel, NR7, inside-day volatility-contraction, or Dalton's Initial Balance / range-extension / open-type taxonomy anywhere in the library.**

Books scanned (converted with `pdftotext`, grepped for: opening range / ORB / initial balance / first hour / opening drive / Crabel / volatility breakout / NR7 / inside day / gap / range extension):

- `A Complete Guide To Volume Price Analysis` — Anna Coulling (2013)
- `VOLUME-PROFILE-The-insiders-guide-to-trading` — Trader Dale (Dale Woods)
- `VWAP-book-final` — Trader Dale
- `ORDER-FLOW-Trading-Setups` — Trader Dale
- `Investing-with-VP` — Trader Dale
- `advanced-ict-institutional-smc-trading-book-2024` — ICT/SMC (anonymous compilation)
- `The_Smart_Money_Concept_Forex` — "jecool king" / James (SMC)
- `IJCRT2303253.pdf` — academic paper (option-chain/PCR; not ORB)
- Volatility set: Sinclair *Volatility Trading*, Warner *Options Volatility Trading*, Bennett *Trading Volatility*, Passarelli *Trading Options Greeks*, McMillan *Options as a Strategic Investment* (image-only PDF, no text layer)
- `The Disciplined Trader` — Douglas (psychology; not ORB)

---

## 1. ORB definition and mechanics

No book defines ORB as "mark the first N-minute high/low, then trade a break of that box." The functional substitute is Trader Dale's **Open-drive** and **Session/Daily Open** concepts, which treat the *open price level* (not a range box) as the actor.

- **Open-drive**: "a sudden and strong one-sided price movement... The most important thing is the place where the strong buying or selling activity started. If aggressive buyers initiate the open-drive, the price shoots upwards, and the place where the strong buying candle opened is strong support." (Trader Dale, *Volume Profile* — Strategy 2: Open-drive). This is the closest analog to the **"opening drive / open-drive"** open-type, but Dale uses it as a **support/resistance origin to fade back to**, not as a breakout box.
- **Session Open / Daily Open as a level**: "A place where the session opened is... a support/resistance level. If a session starts and price goes down, the place where the session opened becomes a resistance zone." (Trader Dale, *Volume Profile* — Strategy 4/5). The Daily Open is anchored at NY close 5:00 p.m. NY time.

Mechanically these books say **break = need follow-through candles to confirm acceptance**, not a single touch: "wait for a few candles to form below the open-drive to make sure the market accepted the lower prices as a temporary fair value" (*Volume Profile*, Strategy 2).

## 2. Timeframe / range-window guidance

- No book specifies a "first 5 / 15 / 30 / 60 min" opening-range window. The concept of an **Initial Balance (first hour)** does not appear.
- Trader Dale's repeated intraday preference is the **30-minute footprint/chart** (and 5-minute for fine entries): "I like to use the 30 Minute footprint chart" (*Order Flow*, Setup #1); "For intraday trading I prefer 5 or 30-minute timeframes" (*VWAP*, intro); open-drive examples are all "30-minute timeframe" (*Volume Profile*, Strategy 2).
- SMC/ICT books frame the window as a **whole session** rather than minutes: Asian session ≈ 7pm–4am EST, London 3am–12pm EST, NY 8am–5pm EST; "Asian Session sets the parameters for the following London session." (SMC, *Smart Money Concept* — Session Highs/Lows). ICT killzones narrow this to the first ~1–2 hours of London/NY.

## 3. Entry rules

The library's consistent message is **fade-the-retest, do NOT chase the raw breakout**:

- "I wait for previous day's high (resistance) to get breached... then I need to see some price action above the high (at least 1–3 30-minute candles)... I wait for the price to come back to this support. When it returns I enter long." (Trader Dale, *Volume Profile* — Strategy 6, Daily/weekly high & low). He explicitly rejects naive breakouts: "there are a lot of false breakouts through these S/R zones and it just doesn't work so well."
- For open-drive: "wait until the price returns back to this open-drive area and enter a long trade from there." (*Volume Profile*, Strategy 2).
- VWAP entry filter on a gap: "anchor the VWAP to the first candle after the gap (the opening candle)... then execute trades by looking for **pullbacks to the VWAP**." (Trader Dale, *VWAP* — Anchoring VWAP to gaps).
- SMC: "We don't trade breakouts, wait for retest." (SMC book) and "Turtle soup is the initial fake-out outside the Asian range before the real Judas swing" — i.e., the first range break is treated as a stop-raid/trap, and the *true* entry is the reversal (ICT/SMC, *Smart Money Concept* — Asian Session / Judas Swing).

## 4. Stop-loss placement

- **Behind the reaction swing point / opposite side of the level**: "position your Stop Loss behind the swing point of the market's reaction (the Reaction Point)." (Trader Dale, *VWAP* — Stop Loss placement). General rule: "always position it BEHIND a barrier (a support/resistance zone)."
- **ATR-based stop**: "a reasonable Stop Loss size is typically around **10–20% of the average daily volatility** (ATR) of the instrument." (Trader Dale, *VWAP* — ATR-based Stop Loss). Method: ATR period 200 on daily, ~300–500 days of data, take the average ATR as daily volatility.
- No book recommends a range-midpoint stop or an opening-range-width stop specifically.

## 5. Target / R:R guidance, win rates, expectancy

- **Default starter R:R = 1:1**: "Aim for a Risk Reward Ratio of 1. If your Stop Loss is 15 pips, set your Take Profit at 15 pips." (Trader Dale, *VWAP* — recommended starting framework).
- **ATR-based target**: "use **10–20% of the average daily volatility** as your Take Profit." Worked example: EUR/USD ATR ≈ 85 pips → intraday TP ≈ 8.5–17 pips. (Trader Dale, *VWAP* — ATR-based Take Profit).
- **Trend-setup targets are trailed** for >1R: the VWAP Trend setup "offers the advantage of trading with a positive RRR and allows for trailing your Take Profit." (*VWAP* — VWAP Trend strategy).
- **Exit before the next barrier**: "Always exit your trade a bit before it reaches a significant barrier (strong S/R from Price Action, VWAP, or Volume Profile)." (*VWAP* — Take Profit placement).
- **No stated win rates or expectancy numbers** appear in any book. All examples are explicitly hypothetical/educational (*VWAP* risk disclosure).

## 6. Filters / confluence the books pair with the open

- **Volume expansion / footprint delta**: Coulling's whole method is "validate price with volume" — a wide-spread breakout candle is only trusted "where this was confirmed with volume." (Coulling, *Volume Price Analysis* — ch. 3, The Open/High/Low/Close). Dale's order-flow adds **imbalances/HVN**: "You will often see Imbalances at the start of a strong and aggressive trend." (*Order Flow*, Setup #4).
- **VWAP / Anchored VWAP**: anchor to the opening candle after a gap; daily VWAP anchored at the start of the day on a 5-min chart; weekly VWAP on 30-min is Dale's intraday favourite. (Trader Dale, *VWAP* — Anchoring to dates / gaps).
- **Sideways/low-volatility contraction before the drive** (a qualitative cousin of NR7/inside-day, but un-named): "Open-drive occurs most of the time after a sideways price action (tight price channel)... a low-volatility area where volumes are accumulated, then a strong one-sided movement." (Trader Dale, *Volume Profile* — Strategy 2). This is the only volatility-contraction-into-expansion idea in the library, and it is **not** quantified.
- **Gap context**: gaps are "anchoring points where everyone's attention is"; the opening candle after a big gap is the VWAP anchor. (Trader Dale, *VWAP*). Coulling notes electronic 24h index futures have largely killed the classic equity gap-open breakout signal except in cash stocks. (Coulling, *VPA* — ch. on electronic trading effect on the open).
- **Previous-day / session high-low as confluence**: PDH/PDL and session hi/lo are the levels the open interacts with. (SMC + Trader Dale Strategy 6).
- **Time-of-day**: SMC/ICT killzones — London open 06:00–10:00 GMT (ideal 07:00–09:00), "London open posts the high/low of the day," "the Lion's portion of the Daily Range is put in during London and NY." (SMC, *Smart Money Concept* — London Open Tactic).

## 7. Market-profile framing (Dalton / Initial Balance / open types)

**Largely absent.** No Dalton, no *Mind Over Markets*, no formal **Initial Balance**, **range extension**, or the four open types (open-drive / open-test-drive / open-rejection-reverse / open-auction) by name. Partial echoes only:

- **Open-drive** exists by name in Trader Dale's *Volume Profile* but is used as an S/R origin, not the Dalton auction-confidence taxonomy.
- **Failed auction** is a listed Trader Dale price-action concept (TOC of *Volume Profile*) — conceptually near "open-rejection-reverse" but not developed for the open specifically.
- ICT's "Asian range → London break → reversal" is a de-facto **range-extension-of-the-initial-range** idea but framed as manipulation (Judas swing / turtle soup), not auction theory. (SMC, *Smart Money Concept*).

## 8. Failure modes / false breakouts

The books are heavily oriented to treating the **first break as a trap**:

- "There are often many false breakouts — the price leaves the rotation area but quickly returns. Such a strategy gives too many bad signals." (Trader Dale, *Investing with VP* — Why Not Trade This as a Breakout Strategy; echoed in *Volume Profile* Strategy 6).
- Coulling on weak vs valid breaks: a breakout candle that closes back near its open on high volume is "not a strong signal" (the test/absorption read). (Coulling, *VPA* — candle anomalies, shooting star/hammer/doji).
- ICT explicitly models the false open break: "Beautiful fake breakout (TRAP) — acquire retail traders' stop losses"; "London open sees stop raid or false breakouts"; "Turtle soup is the initial fake-out outside the Asian range before the real Judas swing." (SMC + ICT books).
- Handling: require **acceptance** (1–3 confirming candles past the level) before trusting the break, then enter on the **retest** of the broken level turned S/R; pair with volume/imbalance confirmation. (Trader Dale, *Volume Profile* Strategies 2 & 6).

## 9. Strong vs weak levels (quality filter useful for ORB edges)

Dale's strong-vs-weak high/low test transfers directly to opening-range edges: "If there is a swing where you can see a strong and quick rejection of lower prices followed by an aggressive up-move, you are looking at a strong low... aggressive change of direction is what matters, not the candle formation." Weak swing points are "many candles testing the same area with no candle testing way beyond." (Trader Dale, *Volume Profile* — Strong or weak highs/lows). Use this to grade whether an OR boundary is a real edge or noise.

---

## Gaps for the web stream to fill

The local library cannot supply, and the web research must cover:

1. **Toby Crabel's original ORB** — the volatility-stretch / opening-range-breakout definition, "stretch" = avg of recent open-to-extreme moves, and his NR7/inside-day setups. Completely absent here.
2. **Explicit opening-range window choice** — empirical comparison of 5/15/30/60-min ranges, why intraday traders favour one, and India-specific (NSE 9:15–9:30 / 9:15–10:15) conventions. Not in any book.
3. **Dalton / Market Profile Initial Balance & range extension**, and the four formal **open types** (open-drive, open-test-drive, open-rejection-reverse, open-auction) with confidence-of-direction logic. Missing.
4. **Quantified entry triggers** — close-beyond vs touch-beyond, retest-entry win-rate trade-offs, buffer/filter sizing. Books are qualitative only.
5. **Stated win rates, expectancy, and backtest stats** for ORB (e.g., index-future ORB studies). Library has none.
6. **NR7 / inside-day / volatility-contraction quantification** as a pre-ORB filter. Only a vague "sideways before the drive" exists here.
7. **Gap-and-ORB interaction rules** (gap-go vs gap-fade, gap size thresholds). Books give only gap-anchored VWAP, no gap classification for breakouts.
8. **Options-specific ORB execution** (strike/expiry selection, IV-crush timing at the open, theta vs the first-30-min move) — the volatility/options books here do not connect their greeks material to ORB at all.
