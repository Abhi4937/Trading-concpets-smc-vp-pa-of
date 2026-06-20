---
title: Deep-Dive — GEX Terminal Pro (gexterminal.net)
tags: [gex, deep-dive, gexterminal, deribit, hyperliquid, ibit]
created: 2026-06-20
source-quality: primary (live capture 2026-06-20)
---

# 🔬 Deep-Dive: GEX Terminal Pro (gexterminal.net)

**URL:** https://gexterminal.net/
**One line:** Free intraday charting terminal that overlays Deribit GEX/DEX levels + IBIT flow + classic TA and scores "confluence" trade zones.
**⚠️ Not the same as** the `zrack/gex-terminal` GitHub repo — unrelated.

---

## 1. What it is
A browser trading terminal (TradingView-like) purpose-built for BTC options structure. Instead of a static GEX bar chart, it draws the **levels on a live candle chart** and tells you where multiple signals stack up.

## 2. Architecture / data flow
```
Hyperliquid WebSocket ───► live BTC candles (1m..1D)
Deribit options chain ───► GEX + DEX levels (5-min refresh)
Tradier API (your key) ──► IBIT (US ETF) options levels overlay
        │
        ▼
Confluence engine: score = agreement across
   GEX clusters · DEX bias · IBIT walls · VWAP · EMAs(9/21/50/200)
   · RSI(ob/os) · Volume Profile(POC/VA) · 1D range · Max Pain
        ▼
Chart UI: Levels / Options / Stats panels + drawing tools + replay
```

## 3. What every overlay means (where & how to read)
| Overlay | Where | Meaning |
|---------|-------|---------|
| **GEX clusters** (CR / PS / walls) | Horizontal levels | Call Resistance, Put Support, gamma walls = hedging magnets/barriers |
| **DEX** (delta exposure) | Bias indicator | Directional hedging pressure (not just magnitude) |
| **IBIT walls** | Levels (if Tradier key set) | US ETF options structure — cross-market confluence |
| **Volume Profile** POC/VA | Side histogram | Acceptance/value area, fair-price magnet |
| **VWAP / EMAs 9·21·50·200** | On candles | Trend/mean context |
| **RSI ob/os** | Sub-pane | Momentum extension |
| **1D Range** edges | Levels | Intraday boundaries |
| **Max Pain** | Level | Strike that maximizes option-writer profit at expiry |
| **Confluence score** | Zone shading | More signals agree → higher-quality zone |

## 4. How to use it
- Pick timeframe (0DTE/1m for scalps, 4h/1D for swing). Identify the **highest-confluence zone** near price.
- Trade *toward* confluence in positive-gamma (pin) regimes; respect *breaks* of walls in negative-gamma regimes.
- Add your free **Tradier API key** to unlock the IBIT overlay (extra confirmation from US flow).

## 5. What NOT to do / limits
- **No data API/export** — you can't automate or backtest off it; it's eyes-on-glass only.
- **Confluence scoring is a black box** — don't outsource judgment to the score; verify each component.
- Levels refresh **~5 min** — fine for intraday, not tick-level.
- Candles come from **Hyperliquid**, levels from **Deribit** — two venues; minor basis differences are normal.

## 6. Verdict
🥈 **Rank #2 for retail** — the best *free intraday visual*. Use alongside CryptoGamma (which adds the API + explicit pin/squeeze metrics). → [[04 — Dashboards Directory + RANKING]]
