---
title: "NYSE & Nasdaq (US equities)"
tags: [market-structure, exchanges, us-equities, reg-nms, nbbo]
created: 2026-06-21
---

# 18 — NYSE & Nasdaq (US equities)

## What it is
NYSE and Nasdaq are the two dominant US equity venues, operating inside the **Regulation NMS** framework (SEC, effective 2005) that stitches all venues into one virtual national market. Both are electronic today; their historical difference — NYSE's human floor vs Nasdaq's dealer screen — survives only as a hybrid-vs-pure-electronic distinction.

## Architecture (matching engine, order book, latency/colocation)
**Nasdaq** runs a pure electronic central limit order book with a **price-time priority** matching engine and **no single specialist**; instead **260+** competing electronic market makers post two-sided quotes (✅ SEC Nasdaq system description). **NYSE** is hybrid: an electronic book plus **Designated Market Makers (DMMs)** with affirmative obligations to maintain a fair, orderly market in their assigned names — DMMs supplied ~**17% of liquidity-adding volume in 2019** (✅ NYSE). Both sell **colocation** rack space adjacent to the matching engine, where **HFT** firms exploit microsecond latency arbitrage against the consolidated feed.

```
ORDER BOOK (price-time)
 BIDS            ASKS
 100.02 x500  |  100.04 x300   <- inside quote = NBBO
 100.01 x800  |  100.05 x900
 100.00 x1200 |  100.06 x400
   ^matching engine pairs best bid/ask, FIFO at each price^
```

## Order lifecycle (click → execution → clearing → settlement)
Click → broker (may route to a **wholesaler** via PFOF, or to exchange) → matching engine pairs against the book honoring **NBBO** → execution report → **clearing at DTCC's NSCC** (CCP that **novates** and nets trades) → **settlement at DTC** (central securities depository, book-entry transfer) on **T+1** (📄 DTCC). See [[24 — Order Lifecycle]] and [[10 — Clearing Houses, CCPs & Custodians]].

## Who provides liquidity
On-exchange: DMMs (NYSE), 260+ electronic market makers (Nasdaq), and HFT/agency flow. Off-exchange: **dark pools** and broker **internalization**, plus **wholesalers** (Citadel Securities, Virtu) that buy retail flow through **PFOF** — see [[11 — Wholesalers, Internalizers & PFOF]]. A large share of retail volume never touches the lit exchange.

## How the venue makes money
- **Transaction fees** (maker-rebate / taker-fee, constrained by Reg NMS Rule 610).
- **Market data** — proprietary depth feeds (a major and contested profit center).
- **Colocation** and connectivity.
- **Listing fees** from issuers.

## Regulation
**Reg NMS** (✅ SEC Release 34-51808) sets the rules of the road:
- **Rule 611 (Order Protection)** — bars **trade-throughs**; you may not execute at a price inferior to a protected quote elsewhere.
- **Rule 610 (Access)** — caps access fees at **$0.003/share** and addresses locked/crossed markets.
- **Sub-Penny Rule** — generally bars quoting in increments below $0.01.
- **NBBO** — the consolidated best bid/offer all venues must respect.

## Limitations / controversies
- **Latency arbitrage**: colocation + proprietary data feeds let HFT see/react before the public consolidated tape — a structural edge bought, not earned (✅ documented basis of the IEX "speed bump").
- **PFOF & internalization** route most retail flow off-lit, raising best-execution and price-discovery concerns — see [[11 — Wholesalers, Internalizers & PFOF]].
- **Market-data pricing**: exchanges are accused of over-monetizing data the public market generates.
- **Maker-taker rebates** can distort routing toward rebate capture rather than best price.

## Sources
- https://www.sec.gov/rules/final/34-51808.pdf
- https://www.nasdaq.com/market-activity
- https://www.nyse.com/markets/nyse/membership
- https://www.dtcc.com/clearing-services/equities-clearing-services
- https://www.dtcc.com/ust
