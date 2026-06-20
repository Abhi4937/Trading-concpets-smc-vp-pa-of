---
title: "25 — Regulation by Region"
tags: [market-structure, regulation, sec, cftc, fca, esma, sebi, mica, enforcement]
created: 2026-06-21
---

# 25 — Regulation by Region

> **Thesis:** Regulators differ less in *intent* (protect markets, protect retail) than in *what they choose to document and restrict*. Comparing the US, UK/EU, India, and crypto regimes reveals a consistent pattern: where regulators have **measured** retail outcomes, the published numbers are bleak — and the restrictions that follow are mostly about leverage, disclosure, and conflicts of interest. This note maps each regime and its landmark enforcement.

---

## United States

Two principal market regulators, split by product:

### SEC — securities (equities, options)
- Governs **disclosure**, market structure (**Reg NMS** — the National Market System rules, including order-protection and the NBBO that underpins [[24 — Order Lifecycle]]), and registration.
- **The SEC has no best-execution rule of its own.** The duty of best execution for broker-dealers is enforced under **FINRA Rule 5310** (a self-regulatory-organization rule), which requires firms to use "reasonable diligence" to obtain the best market for customer orders (✅ verified — FINRA 5310 text).

### CFTC — futures and derivatives
- Governs futures, swaps, and listed derivatives; enforces **anti-spoofing** authority created by **Dodd-Frank §747** (which made spoofing — bidding/offering with intent to cancel before execution — a specific statutory violation).
- **Landmark enforcement:**
  - **JPMorgan — $920.2 million** to the CFTC in **2020** for spoofing in precious-metals and Treasury futures: **the largest monetary relief ever imposed by the CFTC** (✅ CFTC Release 8260-20).
  - **Navinder Sarao** — ordered to pay **>$38 million** for **E-mini S&P 500 spoofing** tied to the **2010 Flash Crash** (✅ CFTC Release 7486-16).

---

## United Kingdom & European Union

Regulated by the **FCA** (UK) and **ESMA** (EU), which converged on aggressive **retail CFD restrictions**:

- **Leverage caps** (tiered by asset class).
- **Negative-balance protection** — a client cannot lose more than the funds in their account.
- **Mandatory standardized risk warnings** on CFD marketing.
- **Ban on binary options** for retail clients.

These measures were grounded in ESMA's own data: **74–89% of retail CFD accounts lose money**, with average losses reported in the range of **€1,600–€29,000** per client depending on the venue (✅ ESMA product-intervention measures). The restriction is explicitly about the *structure* of these products harming retail — directly connected to the B-book conflict described in [[24 — Order Lifecycle]] and [[22 — How the Industry Profits from Retail Losses]].

---

## India

Regulated by **SEBI** (Securities and Exchange Board of India), notable for **measuring and publishing retail loss data** and acting on it:

- **F&O loss study (Sept 2024):** SEBI published that **~93% of individual F&O traders lost money** over the studied period (✅ SEBI Sep-2024 study).
- **NSE co-location scandal:** SEBI investigated and acted on preferential exchange data/access at NSE's co-location facility (an early-tick-feed advantage for some members).
- **Market reforms (2024):** **rationalized weekly expiries** (limiting the number of expiry days), **raised contract lot sizes** (raising the minimum ticket to deter undercapitalized retail), and introduced **finfluencer regulations** restricting unregistered investment advice.

SEBI's posture is the clearest example of a regulator using documented retail-loss statistics as the explicit justification for structural intervention.

---

## Crypto

**Fragmented and inconsistent** across jurisdictions:

- **US:** an ongoing **SEC/CFTC turf war** over whether a given token is a security (SEC) or a commodity (CFTC), leaving classification — and therefore the rulebook — uncertain.
- **EU:** **MiCA** (Markets in Crypto-Assets) provides a comprehensive, harmonized framework — the most complete major-jurisdiction crypto regime.
- **Offshore:** many venues operate from light-touch or **unregulated** jurisdictions, where surveillance is minimal. This is where the **wash-trading** data documented in [[20 — Crypto Exchanges (CEX vs DEX-AMM)]] concentrates — reported volumes on many unregulated CEXs are heavily inflated by self-trading.

---

## Comparison table

| Region | Regulator(s) | Key protections / focus | Notable enforcement / data |
|---|---|---|---|
| **US** | SEC (Reg NMS, disclosure); CFTC (futures, anti-spoofing under Dodd-Frank §747) | Market-structure & disclosure rules; **best-ex via FINRA Rule 5310, not an SEC rule**; statutory anti-spoofing | **JPMorgan $920.2M** to CFTC (2020) — *largest CFTC monetary relief ever*; **Navinder Sarao >$38M** (E-mini spoofing, 2010 Flash Crash) |
| **UK / EU** | FCA; ESMA | CFD **leverage caps**, **negative-balance protection**, mandatory risk warnings, **binary-options ban** | ESMA: **74–89% of retail CFD accounts lose money** (avg loss €1,600–€29,000) |
| **India** | SEBI | Expiry rationalization, **raised lot sizes**, **finfluencer rules (2024)**, co-location oversight | SEBI: **~93% of F&O traders lose** (Sep-2024); acted on **NSE co-location scandal** |
| **Crypto** | Fragmented — US SEC/CFTC; EU **MiCA**; offshore = often unregulated | MiCA = comprehensive EU framework; elsewhere uncertain/absent | SEC/CFTC turf war; rampant **wash trading** on unregulated venues (see [[20 — Crypto Exchanges (CEX vs DEX-AMM)]]) |

---

> **Takeaway:** The two regulators that **published explicit retail-loss percentages** (ESMA 74–89%; SEBI ~93%) are also the two that imposed the most direct *structural* retail restrictions. The US route runs through after-the-fact **enforcement** (record spoofing fines) and a duty (best execution) that lives in a *self-regulatory* rule rather than an SEC statute. Crypto is the regime where retail protection is thinnest — and, not coincidentally, where the manipulation documented in [[23 — Manipulation & Predatory Practices]] is least constrained.

---

## Sources

- https://www.cftc.gov/PressRoom/PressReleases/8260-20 (CFTC — JPMorgan $920.2M resolution; largest CFTC monetary relief) — ✅ verified
- https://www.cftc.gov/PressRoom/PressReleases/7486-16 (CFTC — Navinder Sarao spoofing, E-mini / Flash Crash, >$38M) — ✅ verified
- https://www.finra.org/rules-guidance/rulebooks/finra-rules/5310 (FINRA Rule 5310 — Best Execution and Interpositioning) — ✅ verified
- https://www.esma.europa.eu/press-news/esma-news/esma-agrees-prohibit-binary-options-and-restrict-cfds-protect-retail-investors (ESMA — CFD/binary-options product-intervention measures; retail loss rates) — ✅ verified
- https://www.sebi.gov.in/media-and-notifications/press-releases (SEBI — F&O individual-trader loss study, Sep 2024; ~93% lose) — 📄 sourced
- https://finance.ec.europa.eu/digital-finance/crypto-assets_en (European Commission — MiCA, Markets in Crypto-Assets Regulation) — 📄 sourced
- https://www.sec.gov/files/rules/final/34-51808.pdf (SEC — Regulation NMS final rule) — ✅ verified

## See also
- [[24 — Order Lifecycle]]
- [[23 — Manipulation & Predatory Practices]]
- [[22 — How the Industry Profits from Retail Losses]]
- [[20 — Crypto Exchanges (CEX vs DEX-AMM)]]
