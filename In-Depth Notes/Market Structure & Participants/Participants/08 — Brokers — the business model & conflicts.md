---
title: Brokers — the business model & conflicts
tags: [brokers, pfof, a-book, b-book, conflicts, retail]
created: 2026-06-21
status: core
---

# 🏦 Brokers — the business model & conflicts

> The most important note for a retail trader to understand. **A broker is not your
> friend or your enemy — it's a business, and its revenue model determines whether it
> profits from your trading, your losing, or both.** Know which kind you use.

---

## 1. What a broker actually is
The gatekeeper between you and the market — retail can't access exchanges directly, so everything routes through a broker (📄 Euronext). But "broker" hides **two opposite business models**:

| | **Agency broker (A-book)** | **Dealing-desk broker (B-book)** |
|---|---|---|
| Role | **Agent** — passes your order to the market / an LP | **Principal** — takes the *other side* of your trade itself |
| You are | their customer | their **counterparty** |
| They profit from | commission + spread + PFOF | **your losses** (your loss = their P&L) |
| Conflict | order-routing quality | **direct: they win when you lose** |
| Common in | stock brokers (mostly) | **forex / CFD brokers** |

> The single most important question: **"Is my broker the counterparty to my trade?"** In forex/CFD it very often is. A FMLS25 industry panel stated plainly that *the majority of a broker's revenue comes from its B-book functionality* (📄 Finance Magnates).

## 2. How brokers make money (every revenue line)
1. **Commissions / fees** — per trade or per contract.
2. **The spread** — the gap between buy and sell; even "zero-commission" brokers earn here.
3. **Payment for order flow (PFOF)** — they **sell your order** to a wholesaler who fills it and pays the broker a rebate. The 12 largest US brokerages earned **$3.8B** in PFOF in 2021; **Robinhood made $974M** from it — ~half its revenue (✅ Congress CRS IF12594, confirmed verbatim via the official CRS mirror). Deep-dive: [[11 — Wholesalers, Internalizers & PFOF]].
4. **Margin & leverage interest** — lending you money to trade is high-margin revenue (and a liquidation engine — [[09 — Leverage, Margin & Prime Brokers]]).
5. **B-book client losses** — in forex/CFD, internalized losing trades are pure profit.
6. **Financing / swap / overnight fees**, withdrawal fees, data fees, FX conversion.
7. **Securities lending** — lending out your shares to short-sellers.

## 3. A-book vs B-book vs hybrid (how it really works)
```
   YOUR ORDER
       │
       ▼
   ┌─ A-BOOK ─► passed to a liquidity provider / exchange ─► broker earns commission/spread
   │            (broker is neutral; wants you to keep trading)
   │
   └─ B-BOOK ─► broker keeps it in-house, takes the other side ─► broker earns YOUR LOSS
                (broker wins if you lose — and ~74-89% of CFD clients do)
```
Most retail forex/CFD brokers run a **hybrid**: profitable/large clients are A-booked (hedged externally), while the (majority) losing small clients are B-booked. **The model literally sorts you by whether you're worth taking the other side of.**

## 4. Why this is legal but conflicted
- **PFOF** conflicts with the broker's **best-execution** duty. The SEC has no best-execution rule of its own; it's enforced by **FINRA Rule 5310** (📄 CRS). Empirically, more internalization correlates with **wider** spreads and worse price improvement (📄 SEC DERA).
- **B-book** is legal where disclosed, but the incentive is to keep you trading and (quietly) to profit when you lose.
- **Gamification** (confetti, streaks, free-stock wheels) increases trading frequency — and frequency is what every revenue line above scales with.

## 5. The recruitment layer (how they get you in)
Brokers pay **introducing brokers, affiliates, "finfluencers", and rebate sites** a bounty (CPA / revenue-share) per funded account. The incentive is sign-ups and activity, **not your success** — a "mentor" paid per funded account profits whether you win or lose. → [[12 — Finfluencers, IBs & Affiliates]]

## 6. What it means for you (actionable)
- **Find out your broker's model.** Regulated agency stock broker ≠ offshore B-book CFD shop.
- **Prefer A-book / DMA / regulated** venues; be very wary of high-leverage offshore CFD/forex brokers.
- **Assume every "free" feature is monetizing your order flow or your activity.**
- Costs compound: SEBI found Indian F&O traders paid ~₹50,000cr in transaction costs over 3 years — **transaction costs alone were ~28% of active loss-makers' losses** (📄 SEBI). → [[22 — How the Industry Profits from Retail Losses]]

## 7. Honest caveats
- Not all brokers are predatory; regulated agency brokers with good execution exist and PFOF can fund genuinely cheap commissions.
- B-book is not inherently fraud — it's disclosed market-making. The danger is **undisclosed conflict + high leverage + offshore regulation**, which is where real abuse (last-look, requotes, platform "slippage") lives. → [[23 — Manipulation & Predatory Practices]]

## Sources
- Euronext — market participants: https://www.euronext.com/en/news/who-are-market-participants-trading 📄
- Congress CRS (PFOF, $3.8B, Robinhood): https://www.congress.gov/crs-product/IF12594 📄
- SEC DERA PFOF working paper: https://www.sec.gov/files/dera_wp_payment-order-flow-2501.pdf 📄
- Finance Magnates (B-book majority of revenue): https://www.financemagnates.com/forex/the-majority-of-a-brokers-revenue-comes-from-its-b-book-functionality-kieran-duff-at-fmls25/ 📄
- B2Broker (A-book vs B-book): https://b2broker.com/news/a-book-vs-b-book-brokers-whats-the-difference/ 📄
- SEBI F&O study (costs): https://www.sebi.gov.in/media-and-notifications/press-releases/sep-2024/updated-sebi-study-reveals-93-of-individual-traders-incurred-losses-in-equity-fando-between-fy22-and-fy24-aggregate-losses-exceed-1-8-lakh-crores-over-three-years_86906.html 📄
