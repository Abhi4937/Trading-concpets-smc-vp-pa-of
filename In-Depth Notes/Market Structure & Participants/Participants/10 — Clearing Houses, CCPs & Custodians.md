---
title: "Clearing Houses, CCPs & Custodians"
tags: [market-structure, participants, ccp, clearing, novation, custodian, default-waterfall]
created: 2026-06-21
---

# 10 — Clearing Houses, CCPs & Custodians

## What they are
A **central counterparty (CCP)** is a clearing house that steps into the middle of a trade so that neither original party faces the other directly. **Custodian banks** (e.g. BNY Mellon, State Street) are the firms that physically hold and service the underlying assets — safekeeping, settlement, corporate actions. Together they are the post-trade infrastructure that turns an agreed trade into a settled, risk-managed position.

## How they operate
The CCP interposes itself via **novation**: once a matched trade is submitted, the single original contract between buyer and seller is legally replaced by **two new contracts** — buyer-to-CCP and CCP-to-seller. The CCP becomes counterparty to both sides, so each participant now faces only the clearing house. **✅ verified** (LCH; Reserve Bank of Australia explainer). This removes direct counterparty risk between members but **concentrates** that risk in the CCP itself.

## How they make money
Revenue is **clearing/transaction fees**, **interest on margin and default-fund balances**, and (for custodians) **asset-servicing and safekeeping fees**. Volume-based and recurring, this is utility-like income rather than directional trading profit.

## Why they matter / conflicts
Concentrating risk in one node means the CCP must be near-unbreakable. It manages this through a layered **default waterfall**, applied in order: (1) membership/participation requirements; (2) the defaulter's posted **margin** (initial + variation); (3) the defaulter's contribution to a **mutualised default fund**; (4) the CCP's own capital — **"skin in the game"**; then (5) surviving members' fund contributions. Funds are sized to a **"cover two"** standard (withstand the simultaneous default of its two largest members). **✅ verified**: e.g. LCH's SwapClear/Rates default fund core was ~£4.6bn with ~€44.1m of CCP own capital at end-Sep 2018.

Major examples: **DTCC/NSCC** (US equities clearing), **OCC** (US listed options and securities lending — acts as principal to each side via novation) **✅ verified**, and India's **NSE Clearing (NCL)** and **Indian Clearing Corporation (ICCL)**. Custodians plug into this: **State Street became OCC's first bank clearing member** **📄 sourced**. The systemic conflict is concentration itself — a CCP failure would be catastrophic, so they are simultaneously the market's greatest risk-mutualiser and its single biggest point of failure.

## What it means for retail
You never deal with a CCP directly, but it is *why* your filled trade is safe even if the firm on the other side defaults — the clearing house guarantees settlement. The cost shows up indirectly in clearing fees embedded in commissions and in the margin your broker must post upstream.

## Limitations
Default-fund sizes and waterfall details change with regulation and market conditions; the figures above are point-in-time. "Cover two" protects against modelled defaults, not arbitrary tail events.

See also [[24 — Order Lifecycle]], [[09 — Leverage, Margin & Prime Brokers]].

## Sources
- https://www.lch.com/risk-collateral-management/default-management
- https://www.rba.gov.au/education/resources/explainers/central-counterparties.html
- https://www.theocc.com/clearance-and-settlement/clearing
- https://www.dtcc.com/clearing-services/equities-clearing-services/nscc
- https://www.nseindia.com/products-services/clearing-settlement-process
