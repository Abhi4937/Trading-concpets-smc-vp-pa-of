---
title: "Leverage, Margin & Prime Brokers"
tags: [market-structure, participants, prime-broker, leverage, margin, rehypothecation]
created: 2026-06-21
---

# 09 — Leverage, Margin & Prime Brokers

## What they are
Prime brokers (and the smaller **prime-of-prime** firms that resell their services) are banks or registered broker-dealers/FCMs that bundle the financing and back-office infrastructure a hedge fund or large trading firm needs to operate at scale. A single prime-brokerage relationship typically supplies **leverage (margin lending), custody, securities lending, and clearing** across cash equities, futures, and OTC derivatives — letting a fund consolidate positions, financing, and reporting under one counterparty. **✅ verified**: DTCC's FICC membership profiles list "Prime Broker" and "FCM" as distinct member categories, confirming these firms clear directly through the central system.

## How they operate
The prime broker sits *between* the fund and the wider market. The fund executes with many counterparties but **gives up** those trades to the prime, which becomes the fund's single point of custody, financing, and settlement. Against the fund's collateral the prime extends margin, and it can **rehypothecate** that collateral — reusing posted client assets to fund its own borrowing or to support other clients. The same collateral can therefore back multiple obligations simultaneously. In the US this is constrained by **SEC Rule 15c3-3** (the Customer Protection Rule), which caps the use of customer assets and limits rehypothecation. **📄 sourced**.

## How they make money
Three core revenue lines: **(1) margin lending** — net interest earned on financing client positions; **(2) securities lending** — lending out client shares (e.g. to short-sellers) for a fee, sometimes sharing the rebate with the client; and **(3) financing spreads** captured through rehypothecation and collateral transformation. Ancillary fees come from clearing, custody, and capital introduction. **📄 sourced**.

## Why they matter / conflicts
Prime brokers are the plumbing that makes modern leveraged trading possible. The structural tension: **leverage is both the lender's revenue source and the borrower's liquidation engine.** The same margin that amplifies a fund's returns lets the prime force-liquidate the fund when collateral falls short — and rehypothecation chains mean one fund's distress can propagate through reused collateral. The 2021 Archegos collapse showed how concentrated prime-broker leverage transmits losses to the banks themselves.

## What it means for retail
Retail traders rarely touch a true prime broker, but they live downstream of the same logic: margin and leverage offered by a retail broker create the identical asymmetry — the financing is profit for the lender and a forced-exit mechanism for you. Treat any leverage facility as a margin-call risk first and a return-amplifier second.

## Limitations
Rehypothecation limits, collateral terms, and disclosure vary widely by jurisdiction; UK/offshore prime arrangements historically permitted far broader collateral reuse than US Rule 15c3-3 allows. Exact financing economics are negotiated and opaque.

See also [[05 — Hedge Funds, Prop Firms & HFT]], [[10 — Clearing Houses, CCPs & Custodians]].

## Sources
- https://www.dtcc.com/about/businesses-and-subsidiaries/ficc
- https://www.sec.gov/rules/final/34-21651.pdf
- https://www.investor.gov/introduction-investing/investing-basics/glossary/rehypothecation
- https://www.sec.gov/divisions/marketreg/customer-protection-rule.htm
