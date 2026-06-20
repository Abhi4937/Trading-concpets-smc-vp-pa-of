---
title: How the Industry Profits from Retail Losses
tags: [retail-losses, pfof, costs, leverage, synthesis]
created: 2026-06-21
status: core-synthesis
---

# 💸 How the Industry Profits from Retail Losses

> Follow the money. This note answers the question directly: **when a retail trader
> loses, who got the money, and through which mechanism?** With the real, cited numbers.
> The uncomfortable conclusion: most of it is *legal structure*, not illegal manipulation.

---

## 1. The base rate — retail loses, systematically
| Fact | Source |
|------|--------|
| **93%** of >1 crore Indian individual F&O traders **lost money** FY22–FY24; aggregate losses **>₹1.8 lakh crore**; only **1%** made >₹1 lakh after costs | 📄 SEBI (sep-2024) |
| In FY22, **89%** of individual F&O traders lost (avg ₹1.1 lakh); only **11%** profited | 📄 SEBI (jan-2023) |
| **74–89%** of retail **CFD** accounts lose money (avg loss €1,600–€29,000) | 📄 ESMA |

This is not a run of bad luck — it's the steady-state output of the machine below.

## 2. The five extraction mechanisms (where your money goes)

### ① Transaction costs (the silent killer)
Every trade pays spread + commission + taxes/fees. SEBI: Indian F&O traders paid **~₹50,000cr** in transaction costs over 3 years (51% brokerage, 20% exchange fees); for active loss-makers, costs were **~28% of their net losses**; even *winners* spent **15–50% of profits** on costs (📄 SEBI). **Costs scale with frequency** — which is why the industry encourages activity. Recipients: **brokers, exchanges, the government (taxes).**

### ② The spread → market makers (via PFOF)
Your order is **sold** to a wholesaler who fills it and keeps the spread. Because retail flow is **uninformed**, it carries low adverse-selection risk → near-riskless profit for the wholesaler (📄 SEC DERA). Concentration: **3 wholesalers = 70–82% of stock PFOF, 73–90% of options PFOF**; Citadel + Virtu = **60–70%** of all retail flow 2017-21 (📄 SEC DERA). The broker is paid for handing you over; the wholesaler profits from the spread. Recipients: **wholesalers + your broker.** → [[11 — Wholesalers, Internalizers & PFOF]]

### ③ The other side of the trade → B-book brokers
In forex/CFD, the broker is often your **counterparty** — your loss is its **revenue**. Industry: *"the majority of a broker's revenue comes from its B-book functionality"* (📄 Finance Magnates). With 74–89% of CFD clients losing, internalizing those losses is the business. Recipient: **your broker.** → [[08 — Brokers — the business model & conflicts]]

### ④ Leverage & financing → brokers + the liquidation cascade
Leverage generates **interest revenue** for the broker AND **forces liquidations** that transfer your capital to whoever's on the other side. In crypto, exchanges run **liquidation engines** that charge a fee (Binance: **0.3%** into an insurance fund) and force-close you (📄 Binance). Recipients: **brokers/exchanges (interest + liq fees) + counterparties.** → [[09 — Leverage, Margin & Prime Brokers]]

### ⑤ The speed/algo edge → HFT, prop, FPIs
The pros simply out-trade you. SEBI FY24: **prop traders + FPIs booked ₹33,000cr + ₹28,000cr gross profit while individuals lost >₹61,000cr** — and **96% of prop and 97% of FPI profits came from algorithms** (📄 SEBI). This is the most direct number: pro profits ≈ retail losses, won by speed and code. Recipients: **prop firms, hedge funds, FPIs.** → [[05 — Hedge Funds, Prop Firms & HFT]]

## 3. The money-flow diagram
```
                         RETAIL TRADER'S CAPITAL
                                  │
        ┌──────────────┬──────────┼───────────┬───────────────┐
        ▼              ▼          ▼           ▼               ▼
   transaction      spread     B-book      leverage       out-traded
     costs        (via PFOF)   losses    interest+liq      by algos
        │              │          │           │               │
        ▼              ▼          ▼           ▼               ▼
   brokers,       wholesalers,  the         brokers,      prop firms,
   exchanges,     market         broker     exchanges,    hedge funds,
   govt (tax)     makers        itself      counterparties   FPIs
```

## 4. The recruitment flywheel
Brokers pay **finfluencers / IBs / affiliates** a bounty per funded account (CPA/rev-share). More sign-ups → more activity → more of mechanisms ①–⑤. The "free course" or "signal group" is often the **top of the broker's funnel**, paid whether you win or lose. → [[12 — Finfluencers, IBs & Affiliates]]

## 5. The honest verdict
> **Most retail losses are explained by costs + leverage + the speed gap + your own
> behavior — the *legal* machine — not by your broker secretly hunting your stops.**
> Illegal manipulation exists and is prosecuted (next note), but it's the minority of why
> the 93% lose. The machine doesn't need to cheat; the structure already favors it.

What actually protects you: low frequency, low/no leverage, regulated agency brokers, understanding you're the uninformed flow, and trading an edge you've measured — not the broker's edge on you. → [[25 — Regulation by Region]]

## Sources
- SEBI sep-2024 (93%, ₹1.8L cr, prop/FPI, costs): https://www.sebi.gov.in/media-and-notifications/press-releases/sep-2024/updated-sebi-study-reveals-93-of-individual-traders-incurred-losses-in-equity-fando-between-fy22-and-fy24-aggregate-losses-exceed-1-8-lakh-crores-over-three-years_86906.html 📄
- SEBI jan-2023 (89%/11%): https://www.sebi.gov.in/reports-and-statistics/research/jan-2023/study-analysis-of-profit-and-loss-of-individual-traders-dealing-in-equity-fando-segment_67525.html 📄
- ESMA (74-89% CFD losses): https://www.esma.europa.eu/press-news/esma-news/esma-agrees-prohibit-binary-options-and-restrict-cfds-protect-retail-investors 📄
- SEC DERA (PFOF concentration, internalization): https://www.sec.gov/files/dera_wp_payment-order-flow-2501.pdf 📄
- Finance Magnates (B-book): https://www.financemagnates.com/forex/the-majority-of-a-brokers-revenue-comes-from-its-b-book-functionality-kieran-duff-at-fmls25/ 📄
- Binance (liquidation/insurance fund): https://www.binance.com/en/blog/futures/liquidation--insurance-funds-how-they-work-and-why-they-are-important-to-cryptoderivatives-part-2-421499824684900373 📄
