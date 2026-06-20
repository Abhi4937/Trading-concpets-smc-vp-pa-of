---
title: Trader Usage Playbook — how to use the GEX tools together
tags: [gex, playbook, workflow, trading, deribit]
created: 2026-06-20
status: usage-guide
---

# 🎯 Trader Usage Playbook — the combined GEX workflow

> How to actually trade BTC with these tools as a stack. Levels → regime → trade.
> Always combine GEX with price action — never trade a wall blind ([[08 — Pitfalls and Misconceptions (what NOT to do)]]).

---

## 1. The tool stack (roles)
| Layer | Tool | Why |
|-------|------|-----|
| **Live regime** | [[Tool Deep-Dives/GammaFlip.io]] (~60s, multi-venue) | fastest, broadest gamma-flip read |
| **Levels + risk + API** | [[Tool Deep-Dives/CryptoGamma]] | net/call/put gamma, squeeze/pin metrics, JSON API |
| **Chart confluence** | [[Tool Deep-Dives/GEX Terminal Pro]] | levels on candles + VWAP/EMA/RSI/VP + IBIT |
| **Validate sign** | [[Tool Deep-Dives/Glassnode Gamma Exposure]] / [[Tool Deep-Dives/dankbit]] | taker-flow / trade-aware truth check |
| **History/cross-exch/automation** | [[Tool Deep-Dives/Laevitas]] (or Amberdata) | API, CSV, multi-exchange, backtest |

## 2. Daily routine (pre-session)
1. **Mark the structure:** open CryptoGamma → note **net GEX sign**, **squeeze support/resistance/breakout**, **pin/squeeze risk**. Open GammaFlip → note the **flip level**.
2. **Plot on chart:** in GEX Terminal (or TradingView) draw horizontal lines at **gamma wall, call wall, put wall, zero-gamma/flip, max pain**.
3. **Set the regime:** price **above flip + net GEX +** → *fade/mean-revert day*; **below flip + net GEX −** → *momentum/breakout day*.
4. **Note expiry:** if today/tomorrow is a Deribit **08:00 UTC** expiry with high pin risk → expect magnet behavior into it.

## 3. The trade decision tree
```
Net GEX sign?
 ├─ POSITIVE (long gamma) ──► FADE mode
 │     • Buy dips toward Put Wall / squeeze support
 │     • Sell rips into Call Wall / squeeze resistance
 │     • Target the Gamma Wall pin; stops just beyond the wall
 │     • Best into expiry when pin risk is high
 └─ NEGATIVE (short gamma) ──► FOLLOW mode
       • Trade breakouts of walls / squeeze breakout level
       • Sell rallies, buy strength — moves accelerate
       • Wider stops (vol expands); no mean-reversion
       • Watch for cascade through Put Wall (air-pocket)
Price crossing the FLIP? ──► switch modes; the highest-alpha transition
```

## 4. Concrete setups
- **Pin fade (long gamma):** price pokes above the call wall on low momentum near expiry → short back toward the gamma wall, stop above the poke, target the pin. (Scenario 2/8 in [[03 — How to Read a GEX Chart (interpretation)]].)
- **Flip break (regime change):** net GEX just turned negative / price breaks below zero-gamma → momentum short, add on the put-wall break, trail wide. (Scenario 5/10.)
- **Support bounce (long gamma):** in +GEX, dip into squeeze support with put wall just below → long, stop under the put wall, target mid-range/call wall. (Scenario 1.)
- **Confluence-only entries:** take it only when GammaFlip regime + CryptoGamma levels + GEX Terminal confluence zone + your price trigger **all agree**.

## 5. Automation (optional, powerful)
Poll the **CryptoGamma JSON API** (free) on a cron; alert when:
- `netGamma` **flips sign** → regime change ping.
- `price` within X% of `squeeze.breakout` / gamma wall → level-approach ping.
- `riskMetrics.pinRisk` high on expiry day → pin-trade ping.
For history/backtest or cross-exchange, swap in the **Laevitas `gex_date` API**. Code in [[05 — APIs and Data Sources (Deribit etc.)]].

## 6. Risk rules (non-negotiable)
- GEX picks **style and levels**, not direction — always need a **price trigger**.
- Size **down** near the flip (unstable) and **into expiry** in short gamma.
- Re-read GEX **after every Deribit 08:00 UTC expiry** — the map changes.
- If tools **disagree**, don't trade — disagreement is information.
- Match **tool cadence to your timeframe** (don't scalp off a 15-min snapshot).

## 7. TL;DR
> **Above the flip + positive GEX → fade the edges.
> Below the flip + negative GEX → follow the breakouts.
> The flip cross is the trade. Walls are targets/triggers, not walls of certainty.**
