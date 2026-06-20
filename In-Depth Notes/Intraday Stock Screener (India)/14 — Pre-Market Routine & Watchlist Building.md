---
title: "14 — Pre-Market Routine & Watchlist Building"
tags:
  - intraday
  - screener
  - pre-market
  - watchlist
  - routine
  - india
created: 2026-06-21
---

# 14 — Pre-Market Routine & Watchlist Building

The pre-market window is where edge is built or lost. A disciplined routine compresses hours of noise into a 5–10 name watchlist you know cold before the bell rings.

---

## Night Before / 8:00–8:45 am — Global Cues & News Scan

**Global cues (5 min)**
- US close: Dow, Nasdaq, S&P 500 direction and magnitude.
- Asian markets open: Nikkei, Hang Seng, SGX Nifty.
- **GIFT Nifty** — the single most reliable early read on Nifty's gap direction; treat anything beyond ±0.5% as a meaningful gap signal.

**Overnight news scan (10 min)**
- Earnings/results due today — check the BSE/NSE corporate calendar the night before.
- Bulk deals, block deals, promoter pledging/unpledging overnight.
- RBI/SEBI announcements, macro events (CPI, GDP, policy), global earnings (e.g., major US tech after India's close).
- **F&O ban list** — stocks in ban cannot have fresh F&O positions; remove them from any derivative setup. Carry-forward positions still exist so price can still move; just no new entries via F&O.

**Flag candidates (5 min)**
- Any stock with a big catalyst — results surprise, large order win, rating upgrade/downgrade, M&A — goes into a "news play" sub-list. These are "stocks in play": wider-than-usual range expected, higher relative volume near certain.

---

## 9:00–9:08 am — NSE Pre-Open Session

- NSE's call-auction window; indicative equilibrium price updates every minute.
- Watch the **indicative open price** vs. the previous close to get raw gap magnitude.
- Look at the **order imbalance** column (buy qty vs. sell qty at the indicative price) — a heavy buy-side imbalance at a gap-up price signals strong institutional interest and vice versa.
- Build two raw lists:
  - **Gap-up list**: stocks opening >1% above prior close with volume confirming.
  - **Gap-down list**: stocks opening >1% below prior close with volume confirming.
- Big gap + news catalyst = "stock in play" — flag it with ★.

---

## 9:08–9:15 am — Finalise & Level-Mark

- Freeze the gap lists; add any late-breaking news flags.
- Read which **sectors** are gapping coherently — a sector gap (e.g., PSU banks all up, IT all down) signals institutional rotation; cross-reference with [[08 — Sector Rotation & Relative Strength]].
- On each candidate chart (use saved layout templates), mark:
  - **Prior-day High / Low** — first hard reference levels.
  - **VWAP anchor** — yesterday's anchored VWAP if relevant; today's VWAP starts fresh at open.
  - **Key support / resistance** — weekly swing points, prior distribution zones, round numbers.
- Mark these in advance so you are clicking a watchlist, not drawing during a move.

---

## 9:15–9:30 am — Let the Opening Range Form. Do Not Chase.

- The first candle (9:15 bar) is auction noise, not signal. Every intraday trader is seeing the same spike; liquidity is thin and spreads are wide.
- Use this window to confirm rather than enter.
- Mark the **15-minute Opening Range (OR)**: the high and low of the 9:15–9:30 candle on each watch candidate.
- The OR becomes your primary trigger reference: breakout above OR high = long setup; breakdown below OR low = short setup.
- This is the foundation of the ORB strategy; see [[03 — Long Scans — Breakout & Bounce]] for long triggers and [[04 — Short Scans — Breakdown & Reversal-Down]] for short triggers.

---

## 9:30 am Onward — Live Scan & Final Watchlist

**Filter sequence**
1. Pull the F&O universe (~180 liquid names).
2. Sort by **relative volume** (current volume / average volume for this time-of-day) — only names trading >1.5–2× average are in play.
3. Layer in **relative strength** — price % change vs. Nifty; strongest outperformers go on the long side, weakest underperformers on the short side.
4. Cross with the gap list and sector leaders from 9:08 am.
5. Output: **5–10 names maximum**. More names = less focus = worse execution.

**Split the list**
- **LONG side**: strongest stocks/sectors, price above VWAP, OR broken to upside. See [[03 — Long Scans — Breakout & Bounce]].
- **SHORT side**: weakest stocks/sectors, price below VWAP, OR broken to downside. Confirm the name is **MIS-shortable** (not in F&O ban; equity short is MIS-only, so must close by 3:20 pm). See [[04 — Short Scans — Breakdown & Reversal-Down]].

**Tag each name with a trade card**

| Field | Example |
|---|---|
| Setup type | Breakout / Bounce / Breakdown / Reversal-Down |
| Direction | Long / Short |
| Key levels | Prev-day H: 1240 / Prev-day L: 1195 / OR-H: 1228 / VWAP: 1210 |
| Trigger | Break and close above OR-H with RVol >2× |
| Target / Stop | T: 1255 / SL: 1215 (below OR midpoint) |

A trade card written before the session means you execute the plan, not the emotion.

---

## First-Hour Management

- **Trade only A+ confluence** — OR break + sector leader + relative volume. Anything less is a skip.
- **10:15 am checkpoint**: re-check sector leadership; the dominant theme can shift. Drop any watchlist name that has lost relative strength or is now lagging its sector.
- **Avoid 12:00–1:30 pm lunch lull**: volume dries up, fakeouts increase, spread widens. Best taken as a review window, not an entry window.
- **MIS auto-square-off**: brokers begin auto-closing MIS positions around 3:20 pm. Set a manual reminder at 3:10 pm; do not rely on the broker alert alone.
- **Keep the list small**: five names you know cold beat fifty you are scrolling through when a move starts. Selectivity is edge.

---

## Feeding the Watchlist into the Decision Engine

Once the morning list is finalised, route each flagged name into [[17 — Integration with the Decision Engine]] — the Decision Engine consumes the setup type, direction, and key levels to output a position-size-adjusted trade plan, confirm whether an options overlay is appropriate (e.g., buying a call instead of a long MIS equity position), and log the trade rationale before entry.
