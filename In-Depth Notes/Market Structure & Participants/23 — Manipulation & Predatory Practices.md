---
title: Manipulation & Predatory Practices — documented vs myth
tags: [manipulation, spoofing, wash-trading, last-look, enforcement, myth-vs-fact]
created: 2026-06-21
status: core-synthesis
---

# ⚖️ Manipulation & Predatory Practices — documented vs myth

> The honest separation: **what is genuinely illegal and prosecuted** vs **what retail
> blames but is really structure + their own leverage.** Every documented case here has
> an enforcement citation; every "myth" is labeled as such.

---

## 1. ✅ DOCUMENTED & PROSECUTED (this is real)

### Spoofing & layering
Placing large orders you **intend to cancel** to fake supply/demand and move price, then trading the other way.
- **JPMorgan paid $920.2M to the CFTC (Sep 2020)** for spoofing in metals & Treasuries futures — the **largest CFTC monetary relief ever**; spanned 2008–2016, hundreds of thousands of spoof orders (✅ CFTC 8260-20).
- **Navinder Sarao** ordered to pay **>$38M** ($25.7M penalty + $12.9M disgorgement) for "dynamic layering" — 4–6 huge fake sell orders in E-mini S&P futures; on **6 May 2010 (the Flash Crash)** his program ran 4h25m, exerting $170–200M of downward pressure (✅ CFTC 7486-16).
> Spoofing is a **federal crime** under Dodd-Frank §747. It's done by *some* large/HFT players, not by your broker against your single order.

### Wash trading (fake volume)
Trading with yourself to fabricate volume/interest.
- On **unregulated crypto exchanges**, wash trading averages **>70% of reported volume (median 79.1%)** across 29 exchanges — ~**$4.5 trillion** of fake spot volume in **Q1 2020 alone**; regulated exchanges (Coinbase, Gemini…) show normal patterns and **<3%** of spot (✅ NBER w30783). → [[20 — Crypto Exchanges (CEX vs DEX-AMM)]]

### Forex "last look"
A liquidity provider/broker accepts your order, then **rejects it** if the price moved against them in the milliseconds after — a free option against the client.
- **Barclays paid $150M to the NY DFS (2015)** for last-look abuse — rejecting client trades for the bank's benefit (✅ NYDFS). → [[16 — Forex participants]], [[21 — Forex & the OTC interbank market]]

### Other prosecuted practices
Quote stuffing (flooding the book to slow rivals), front-running (trading ahead of a known client order), and insider trading — all illegal and enforced.

## 2. 🟡 REAL BUT STRUCTURAL (legal, not a conspiracy)
These hurt you but are **how the machine is built**, not someone cheating:
- **PFOF / internalization** — your order sold to a wholesaler; legal, disclosed, but conflicted ([[11 — Wholesalers, Internalizers & PFOF]]).
- **B-book** — your broker is your counterparty; legal where disclosed ([[08 — Brokers — the business model & conflicts]]).
- **The speed/algo gap** — colocation & HFT are legal advantages ([[05 — Hedge Funds, Prop Firms & HFT]]).
- **Liquidation engines** — your leverage, the exchange's documented rules ([[09 — Leverage, Margin & Prime Brokers]]).
- **Gamification & cost drag** — legal product design that maximizes your frequency.

## 3. ❌ MOSTLY MYTH / EXAGGERATED (be skeptical)
| Claim | Reality |
|-------|---------|
| **"My broker hunts MY stop loss."** | A regulated agency broker has no position against your single order and can't see/target it profitably. **Stop "hunting" is real as a market phenomenon** — price gravitates to liquidity pools where stops cluster (other traders, algos) — but it's **structural liquidity-seeking, not your broker targeting you.** In a B-book/offshore shop the conflict is real; in a regulated agency broker it's a myth. |
| **"The market makers moved price to stop me out."** | At your size you're irrelevant to them. Price moved to where resting liquidity was — your stop just sat there with thousands of others. |
| **"Brokers spike/freeze the platform to beat me."** | Possible at *unregulated offshore* B-book shops (requotes, asymmetric slippage) — a genuine red flag. Not how regulated exchanges/brokers work. |
| **"It's all rigged so retail can't win."** | The structure is *adversely tilted* (costs, speed, info) — but ~1–11% do profit (SEBI). It's a steep, costly game, not a literally impossible one. |

> **The test:** ask *"does a specific, regulated entity have the means, motive, and a prosecuted record to do this to my individual order?"* For spoofing/wash/last-look at the big-player level: yes. For "my broker hunts my 1-lot stop": almost never — that's structure + leverage + clustering.

## 4. The practical defense
- Use **regulated, agency/DMA** brokers — removes most genuine conflict.
- **Avoid high leverage** — it's what turns normal volatility into your liquidation.
- **Don't cluster stops at obvious levels** (round numbers, prior highs/lows) where liquidity-seeking gravitates.
- Treat any **offshore high-leverage CFD/forex** broacher with deep suspicion — that's where documented platform abuse actually lives.
- Understand you are the **uninformed flow** — trade your own measured edge, not against the house's.

→ Regulatory regimes & protections: [[25 — Regulation by Region]] · The legal extraction machine: [[22 — How the Industry Profits from Retail Losses]]

## Sources
- CFTC — JPMorgan $920.2M spoofing: https://www.cftc.gov/PressRoom/PressReleases/8260-20 📄
- CFTC — Sarao spoofing/Flash Crash: https://www.cftc.gov/PressRoom/PressReleases/7486-16 📄
- NBER — crypto wash trading (w30783): https://www.nber.org/system/files/working_papers/w30783/w30783.pdf 📄
- NY DFS — Barclays last-look $150M: https://www.dfs.ny.gov/reports_and_publications/press_releases/pr1511181 📄
- SEC — spoofing/enforcement context: https://www.sec.gov/newsroom/press-releases/2020-233 📄
