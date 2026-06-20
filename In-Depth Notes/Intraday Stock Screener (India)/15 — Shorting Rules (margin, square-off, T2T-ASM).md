---
title: "15 — Shorting Rules (margin, square-off, T2T-ASM)"
tags:
  - intraday-screener
  - shorting
  - margin
  - sebi
  - t2t
  - asm
  - india
created: 2026-06-21
---

# 15 — Shorting Rules (margin, square-off, T2T-ASM)

## Can You Short Intraday in Indian Equities?

Yes — but with hard structural constraints. In the **cash/equity segment**, you may short a stock intraday using an intraday product type (**MIS / Cover Order / Bracket Order**). The position **must be squared off the same session**. You cannot carry a naked cash-equity short overnight.

This is not a broker restriction — it is a consequence of SEBI's settlement framework. If you fail to deliver shares on settlement day, the exchange treats it as a **short delivery** and buys the stock in an **auction session (T+1)**. The cost — auction price plus a penalty — is debited to you. The exchange is indifferent to intent; failure to deliver is failure to deliver.

---

## Margin: Symmetric Long and Short

Since SEBI's **peak-margin surveillance rules came into full effect on 1 September 2021**, intraday leverage has been capped system-wide. The margin required is:

> **VAR (Value at Risk) + ELM (Extreme Loss Margin)**

This is **identical whether you are buying or selling intraday**. Margin is direction-neutral. For most liquid large-cap stocks the combined VAR+ELM comes to roughly **20%, implying ~5x leverage**. Some volatile or mid-cap stocks carry higher VAR, so effective leverage is lower.

Stock futures (F&O) carry **SPAN + Exposure margin**, also symmetric long vs short, and allow overnight holding.

---

## Auto Square-Off

Brokers are required to square off open MIS positions before market close. In practice, most brokers trigger auto square-off between **3:20 pm and 3:25 pm IST**. If your intraday short is still open at that window, the broker squares it at prevailing market price — no manual confirmation. Factor this into stops and trailing exits when shorting late in the session.

---

## Carrying a Short Overnight: F&O Only

To hold a short position beyond the same session:

- **Short a stock future** — SPAN+exposure margin required; can be held to expiry.
- **Buy put options** — premium paid upfront; defined risk; can be held to expiry.

There is no mechanism to carry a cash-segment short overnight in India.

---

## Where You Cannot Short Intraday

Certain stock categories are delivery-only — **MIS is not permitted**, meaning intraday shorting is blocked entirely:

| Category | Reason | Short allowed intraday? |
|---|---|---|
| **T2T (Trade-to-Trade)** | Delivery compulsory; no netting | No |
| **Z-group** | Settlement/compliance risk | No |
| **ASM Stage I / II** | SEBI Additional Surveillance | No (often) |
| **GSM (Graded Surveillance)** | Elevated trade-to-trade restrictions | No |
| **F&O ban-period stocks** | SEBI position limit breach | Restricted |
| **Illiquid / thin float** | Broker risk policy | Often No |

Brokers publish and update an **MIS-allowed / short-selling permitted list** daily. Your screener's shortable universe must be filtered against this list — see [[06 — Liquidity & Tradability Filters]].

---

## Practical Shortable Universe

The cleanest, most reliable universe for intraday shorting is the **F&O-eligible stocks** — approximately **180–220 names** as of the current SEBI list. These are liquid, have defined margin schedules, are rarely in T2T or ASM, and have deep enough order books to absorb a short entry and exit without excessive slippage. The breakdown and reversal-down scans target this universe — see [[04 — Short Scans — Breakdown & Reversal-Down]].

---

## Long vs Short Intraday — Quick Comparison

| Dimension | Long Intraday (MIS Buy) | Short Intraday (MIS Sell) |
|---|---|---|
| **Allowed in cash segment?** | Yes | Yes — same session only |
| **Margin required** | VAR + ELM (~20% for most) | VAR + ELM — identical |
| **Overnight hold?** | No (MIS); convert to CNC to hold | No; must square off |
| **Auto square-off** | ~3:20–3:25 pm | ~3:20–3:25 pm |
| **Failure consequence** | None (you hold shares) | Short delivery → auction + penalty |
| **Exceptions / blocks** | T2T, Z-group, ASM (less impact long) | T2T, Z-group, ASM, illiquid = blocked |
| **Overnight alternative** | CNC (cash, full margin) | Stock futures short / buy puts |

---

*Scope: cash equity (NSE/BSE) intraday shorting mechanics under SEBI peak-margin framework. Not trading advice.*
