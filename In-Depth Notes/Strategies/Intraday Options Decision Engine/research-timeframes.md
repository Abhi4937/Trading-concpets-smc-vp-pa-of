---
type: research
title: "Timeframe selection for order-flow + volume-profile intraday options trading (Nifty/BankNifty) — deep-research findings"
date: 2026-06-19
method: "deep-research harness — 6 angles, 22 sources fetched, 98 claims, 25 verified (3-vote adversarial), 22 confirmed / 3 refuted"
---

# Timeframe selection — researched findings

External, adversarially-verified research backing the timeframe choices in [[note|the guide]]. Each finding was
confirmed by a 2/3 (usually 3/0) verifier vote across independent sources. **It validates, rather than
contradicts, the engine's 1h/30m → 15m → 5m stack.**

## Confirmed findings (high confidence)

1. **Multi-timeframe top-down is the practitioner consensus.** Read structural levels / context / bias on a
   *higher* timeframe; time entries on a *short* one. Footprint is read on **1–5 minute** bars ("a solid balance
   between signal quality and noise" — NinjaTrader); **tick/1-min** for scalping, **5–15 min** for swing-oriented
   day trades. *Short-TF-alone is only half the workflow.* (NinjaTrader; TrueData; Bookmap) → **validates the
   guide's 5m trigger + 15m level + 1h/30m bias.**

2. **Volume profile is applied as a session profile anchored to the NSE 9:15 AM open**, with Initial Balance =
   first hour (9:15–10:15 AM IST). Read VPOC / value-area position directionally, plus balance/imbalance, single
   prints, and "unfinished business" as auction acceptance vs rejection. (Vtrender; WavesStrategy)
   *Caveat:* the retail framing of "VPOC = the exact level big players positioned" is an **oversimplification** —
   VPOC is a mechanical volume aggregate and cannot distinguish institutional from retail flow.

3. **Footprint read = bid/ask volume per price level** (who lifted the offer vs hit the bid), POC as magnet,
   imbalances as short-term S/R; **delta is the more honest signal than price when they diverge.** Common
   strong-imbalance threshold ≈ **3:1 to 4:1** (platform defaults vary: ATAS 150%, Exocharts 250%, most 300%).
   (NordFX; NinjaTrader; TrueData; Vtrender)

4. **CVD is the retail-friendly compressed proxy for the full footprint.** Match its window to your horizon; the
   governing rule is *consistency with entry/exit decisions*, not one optimal TF. The actionable intraday method:
   **CVD divergence at a known reference level (prior high/low, VWAP, VPOC/liquidity zone), then wait for a
   reaction** (failure to continue + CVD shift). (Bookmap; TrueData) → **this IS the guide's "read at a level,
   then wait for the trigger."**

5. **India data reality (the central qualifier):** footprint / Market Profile / CVD exist for NSE Nifty/BankNifty
   via **GoCharting, TrueData, Vtrender — but the bid/ask aggressor split is INFERRED from the standard market
   feed, not a true colo-grade trade-by-trade feed.** TrueData self-disclosed this (against marketing interest).
   Claims of genuine exchange-grade tick-by-tick aggressor data for Indian retail (Vtrender "direct from NSE",
   GoCharting "tick-by-tick") were **explicitly refuted** in verification. → **trust CVD/delta DIVERGENCE, treat
   absolute footprint/imbalance values with skepticism.** (GoCharting; TrueData; Vtrender)

6. **Vtrender's three-stage NSE playbook:** **(1) Location first** (Market Profile) → **(2) Pressure second**
   (Gamma / GEX / options positioning) → **(3) Intent third** (Order Flow / COT / VPOC / strength) — *structure
   before signal*. (Vtrender) → **maps one-to-one onto the engine: map levels → read regime/GEX → read the
   at-level reaction.** Strong independent corroboration of the spine and the weighted-confluence order.

7. **SEBI regulatory reality (current as of 2026):** the Oct 1 2024 framework (effective Nov 20 2024) limits
   weekly index-option expiry to **one benchmark index per exchange** — on NSE only **Nifty 50 keeps weekly**;
   **BankNifty, FinNifty, Midcap Select, Next-50 lost weeklies (monthly only)**; BSE keeps **Sensex** weekly.
   (Zerodha; Business Standard; Outlook) → **confirms the guide's expiry facts; intraday weekly-decay scalping
   concentrates on Nifty 50, BankNifty option trades sit on monthly expiry.**

## Refuted (do NOT claim)
- Vtrender sources exchange-grade tick data direct from NSE/BSE (0–3 refuted).
- GoCharting offers true trade-by-trade / tick-by-tick NSE data (0–3 / 1–2 refuted).

## Caveats
- Timeframe/footprint/CVD methodology rests largely on **US-futures-generic vendor blogs** (NinjaTrader, Bookmap,
  TrueData, NordFX) — corroborated and widely accepted, but **not India-empirical or peer-reviewed**; the numbers
  (1–5 min, 3:1–4:1) are conventions/heuristics, not validated optima.
- **No true options footprint exists in India** — all order-flow/VP context is read on the **futures/spot
  underlying** and mapped onto the ATM/near-ATM option.

## Open questions (gaps the research could not close)
1. The exact **futures-signal → option-entry timeframe mapping** has no canonical sourced rule — the guide's
   delta/ATR construction (§31–36) is a reasoned synthesis, not an externally-validated convention.
2. Practical accuracy of **inferred-aggressor CVD** vs true aggressor data — may favour **5–15 min over 1 min** to
   wash out inference noise (worth testing in the backtest, §39).
3. Post-SEBI shift of intraday OF/VP playbooks toward **Nifty 50 weeklies** and whether single-weekly-expiry
   changes TF selection / VP anchoring on expiry day.
4. Specific **HVN/LVN and naked/virgin-POC** anchoring rules (prior-day vs developing vs composite) for Indian
   practitioners — confirmed VPOC/VA use but not these specifics.

## Key sources
NinjaTrader (footprint guide) · Bookmap (CVD) · TrueData (order-flow & CVD on 1/5/15-min, India) · NordFX
(footprint/CVD) · Vtrender (Market Profile pillar, NSE method) · WavesStrategy (Nifty VP+OI) · Zerodha Z-Connect,
Business Standard, Outlook Business (SEBI 2024 rules).
