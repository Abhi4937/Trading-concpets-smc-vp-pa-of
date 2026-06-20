---
title: Market Structure & Participants — Map of Content
tags: [moc, market-structure, participants, brokers, exchanges, index]
created: 2026-06-21
status: living-document
---

# 🗺️ Market Structure & Participants — START HERE

> An end-to-end study of **who is in the market, what role each plays, how they trade,
> and exactly how they make money** — including the uncomfortable parts: how brokers
> profit when you lose, payment for order flow, B-book dealing desks, leverage as a
> liquidation engine, and documented manipulation. Plus the **architecture of the big
> exchanges** (NYSE, Nasdaq, NSE, BSE, crypto CEX/DEX, forex OTC).
>
> Built from **3 adversarially-verified deep-research passes** over **regulatory/primary
> sources** (SEC, CFTC, ESMA, SEBI, DTCC, NSE, NBER, OCC, LCH). Every number is cited.
> A dedicated **verification pass** (2026-06-21) re-checked the headline claims against
> their primary sources: **✅ verified** = confirmed against the source; **⚠️** = widely
> reported but not confirmable in our pass (source bot-gated); **📄 sourced** = primary
> citation, not separately re-verified. See **§ Verification status** at the bottom.

---

## 📚 The vault

### Foundations
- [[01 — The Market Food Chain]] — the whole ecosystem on one page: who feeds whom, who profits from whom

### 👥 Participants (`Participants/`)
- [[02 — Retail Traders]] · [[03 — Whales & HNW]] · [[04 — Institutions]] · [[05 — Hedge Funds, Prop Firms & HFT]]
- [[06 — Market Makers & Dealers]] · [[07 — Investment Banks (sell-side)]]
- [[08 — Brokers — the business model & conflicts]] — **PFOF, A-book vs B-book, how they profit when you lose**
- [[09 — Leverage, Margin & Prime Brokers]] · [[10 — Clearing Houses, CCPs & Custodians]]
- [[11 — Wholesalers, Internalizers & PFOF]] · [[12 — Finfluencers, IBs & Affiliates]] — **how brokers pay people to recruit you**

### 🧩 By asset class (`By Asset Class/`) — the *class-specific* players
- [[13 — Stocks & Equities participants]] · [[14 — Derivatives (options & futures) participants]]
- [[15 — Commodities participants]] · [[16 — Forex participants]] · [[17 — Crypto participants]]

### 🏛️ Exchanges & venues (`Exchanges/`)
- [[18 — NYSE & Nasdaq (US equities)]] · [[19 — NSE & BSE (India)]]
- [[20 — Crypto Exchanges (CEX vs DEX-AMM)]] · [[21 — Forex & the OTC interbank market]]

### 🎯 The synthesis
- [[22 — How the Industry Profits from Retail Losses]] — follow the money, with the real numbers
- [[23 — Manipulation & Predatory Practices]] — **documented (with enforcement cases) vs exaggerated**
- [[24 — Order Lifecycle]] — your click → routing → execution → clearing → settlement
- [[25 — Regulation by Region]] — SEC/CFTC, FCA/ESMA, SEBI, crypto

---

## ⚡ The 60-second truth

1. **It's a hierarchy, not a level playing field.** Order flow, speed, capital, and information all tier upward: retail → brokers → wholesalers/market makers → exchanges/clearers, with institutions and HFT sitting above retail on every axis.
2. **You usually don't trade "on the exchange."** Your retail order is often **sold** to a wholesaler (PFOF) and filled *off-exchange* (internalized). In the US, 3 wholesalers handle **70–90%** of it.
3. **Many "brokers" are your counterparty.** In forex/CFD, **B-book** brokers take the *other side* of your trade — your loss is literally their revenue.
4. **The house edge is real and measured.** **SEBI: 93%** of Indian F&O traders lose; **ESMA: 74–89%** of retail CFD accounts lose. Costs + leverage + theta do most of the damage.
5. **Manipulation is real but specific.** Spoofing, wash trading, and last-look are *documented and prosecuted* (JPMorgan $920.2M; Sarao/Flash Crash). The vague "my broker hunts my stops" story is mostly **structure + your own leverage**, not a conspiracy — see [[23 — Manipulation & Predatory Practices]].

> **The point of this vault:** understand the machine so you stop being the part it eats.

---

## ✅ Verification status (re-checked 2026-06-21)
A targeted pass ran **3 adversarial fetch-and-check votes per headline claim** against the primary source.

**✅ Confirmed (source substantiates the figures):**
- SEBI Jan-2023: 89% of FY22 F&O traders lost / 11% profited
- SEBI Sep-2024: **93%** lost FY22–24, >₹1.8L cr aggregate, 1% made >₹1L (confirmed verbatim from the study PDF)
- SEBI Sep-2024: ~₹50,000cr transaction costs (51% brokerage / 20% exchange)
- ESMA: **74–89%** of retail CFD accounts lose (€1,600–€29,000 avg)
- PFOF: **$3.8B** (2021), Robinhood **$974M**; wholesaler shares Citadel **41%** / Virtu **26%** / G1 **16%** (CRS IF12594)
- SEC-DERA: 3 wholesalers = 70–82% stock / 73–90% options PFOF; Citadel+Virtu 60–70% (paper *cites* Bryzgalova 2023 & Hu & Murphy 2024)
- CFTC: **JPMorgan $920.2M** spoofing; **Sarao >$38M** (Flash Crash)
- NBER: crypto wash trading **79.1% median**, ~$4.5T fake spot Q1-2020, regulated <3%
- Binance: **0.3%** liquidation fee → insurance fund → ADL
- NY DFS: **Barclays $150M** last-look
- SEC: Reg NMS (eff. 2005, Access-fee cap **$0.003/sh**); Nasdaq price-time + 260 MMs; NYSE DMMs **17%** (2019)

**⚠️ Widely reported but NOT re-confirmed in this pass (source page bot-gated — verify before quoting):**
- SEBI FY24 **prop +₹33,000cr / FPI +₹28,000cr / individuals −₹61,000cr**, and **96%/97% of pro profits from algos** (figures live in the SEBI annexure/PDF our verifiers couldn't fetch). Used in [[01 — The Market Food Chain]], [[05 — Hedge Funds, Prop Firms & HFT]], [[22 — How the Industry Profits from Retail Losses]] with this caveat.

**🔧 Corrected during verification:**
- The "transaction costs = ~28% of net losses for active loss-makers" figure was **re-attributed** from the Sep-2024 release (where it does not appear) to the **SEBI Jan-2023 study** (where it does).
