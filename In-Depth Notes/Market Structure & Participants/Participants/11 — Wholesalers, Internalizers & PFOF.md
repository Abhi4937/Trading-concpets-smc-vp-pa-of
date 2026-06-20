---
title: "Wholesalers, Internalizers & PFOF"
tags: [market-structure, participants, pfof, internalization, wholesaler, best-execution]
created: 2026-06-21
---

# 11 — Wholesalers, Internalizers & PFOF

## What they are
**Retail wholesalers** (also called **internalizers**) — chiefly **Citadel Securities, Virtu Financial, and G1 Execution** — are off-exchange market makers that buy retail order flow from brokers and fill it themselves. The brokers are paid for routing those orders: **payment for order flow (PFOF)**.

## How they operate
When you place a market order at a commission-free broker, it is usually not sent to an exchange. The broker sells it to a wholesaler, which **internalizes** it — fills it in-house against its own book at a price slightly better than the **NBBO** (National Best Bid and Offer). The wholesaler profits because retail flow is **uninformed**: it carries low **adverse-selection** risk (retail traders rarely know something the market maker doesn't), so the spread captured exceeds the small price improvement given back. **📄 sourced** (SEC DERA working paper on internalization).

## How they make money
The wholesaler captures the bid-ask spread on flow it can fill confidently, returning a sliver of price improvement to the customer and a PFOF rebate to the broker. The model only works at scale and on flow that is statistically harmless to trade against.

## Why they matter / conflicts
**Concentration is extreme.** Three wholesalers handle roughly **70–82% of stock PFOF and 73–90% of options PFOF**; **Citadel + Virtu alone bought 60–70%** of purchased retail flow (2017–2021) **📄 sourced** (SEC DERA). By order share in 2022: **Citadel ~41%, Virtu ~26%, G1 ~16%** **📄 sourced** (Congressional Research Service IF12594). PFOF generated **~$3.8B** for the 12 largest US brokerages in 2021 **📄 sourced**.

The core conflict: PFOF pits the broker's revenue against its **best-execution duty** (**FINRA Rule 5310** — note the SEC has no standalone best-ex rule of its own) **📄 sourced**. The broker is paid to route where the rebate is highest, not necessarily where execution is best. Empirically, **more internalization is associated with WIDER quoted spreads and worse price improvement**, an effect amplified when PFOF is concentrated in a few hands **📄 sourced** (SEC DERA).

## What it means for retail
The "zero-commission" you pay is funded by selling your order flow. You typically get marginal price improvement, but the system's incentives don't align with getting you the *best* possible fill — and the market-wide spread effects can quietly cost more than the visible commission ever did. For large or marketable limit orders, routing transparency matters; check your broker's Rule 606 reports.

## Limitations
PFOF is legal in the US, banned in the UK/EU; rules are evolving. The DERA spread findings are correlational, and "price improvement vs NBBO" can flatter execution quality when the NBBO itself is wide.

See also [[08 — Brokers — the business model & conflicts]], [[22 — How the Industry Profits from Retail Losses]], [[24 — Order Lifecycle]].

## Sources
- https://www.sec.gov/dera/staff-papers
- https://crsreports.congress.gov/product/pdf/IF/IF12594
- https://www.finra.org/rules-guidance/rulebooks/finra-rules/5310
- https://www.sec.gov/files/rules/proposed/2022/34-96495.pdf
