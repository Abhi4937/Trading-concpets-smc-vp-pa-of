---
title: "09 — NSE Data Sources"
tags: [screener, nse, data, india, python, bhavcopy, options]
created: 2026-06-21
---

# 09 — NSE Data Sources

NSE publishes a surprisingly rich set of free data products on nseindia.com. The catch: there is no official public real-time API, and the site aggressively rate-limits bots. Everything useful here is EOD or snapshot-level — good for overnight prep and morning setup, not for live tick polling.

---

## Free NSE Data Products

| Product | What It Contains | Best Use |
|---|---|---|
| **Bhavcopy** | Full equity + F&O OHLCV for every instrument; published after market close | Backbone for all EOD screening; builds your nightly watchlist |
| **Pre-open data** | 9:00–9:08 indicative open price + order imbalance by stock | Gap read; flag stocks with large buy/sell side imbalance before open |
| **Option chain** | Live OI, IV, bid/ask by strike for all F&O names | Identify key support/resistance via max OI; see OI build-up |
| **Security-wise delivery** | Delivery % of traded volume per stock | Conviction filter — high delivery % = real buying/selling, not just noise |
| **Index constituents** | Nifty 50, Nifty 500, F&O-eligible list | Restrict your universe to liquid, institutionally traded stocks |
| **Most-active / top gainers-losers / volume gainers** | Ready-made momentum lists | Starting point for relative-strength scans |
| **Circuit limits** | Upper/lower circuit levels per stock | Filter out or flag stocks hitting circuits (gap risk, illiquidity) |
| **F&O ban list / MWPL** | Stocks in OI ban (>95% MWPL) | Skip these: no fresh futures/options positions allowed; erratic behaviour |

---

## Limitations to Know

- **No official real-time public API.** Everything is scraped or downloaded from the NSE website.
- **Rate-limiting and bot detection are aggressive.** Raw `requests` calls fail without browser-like headers, a valid session cookie, and randomised delays.
- **Bhavcopy is best consumed once nightly**, not re-fetched intraday.
- For live intraday ticks you must use a broker API — see [[10 — APIs (broker + data)]].

---

## Unofficial Python Libraries

| Library | Status | Strengths |
|---|---|---|
| **jugaad-data** | Active (preferred) | Bhavcopy download, historical OHLCV, live quotes; well-maintained |
| **nsepython** | Active (preferred) | Option chain, live quotes, derivatives data; clean interface |
| **nsetools** | Older, basic | Simple quote lookups; limited scope |
| **nsepy** | DEPRECATED | Author notice: cannot maintain; last release v0.8 Mar 2020; README now redirects users to jugaad-data / nsepython / NSEDownload. Do not start new projects on it. |
| **eod2** (BennyThadikaran, ~150 stars) | Active | Automated pipeline that downloads and incrementally updates NSE EOD stock, index, and delivery data locally — a ready-made data layer for a screener; see [[12 — GitHub Tool Deep-Dives]] |

---

## What to Use When

**EOD prep (nightly):** Pull Bhavcopy via jugaad-data, merge delivery % from the security-wise delivery file, run your scans. This builds the morning watchlist.

**Morning setup:** Hit the NSE option chain via nsepython for max-OI levels on index/major stocks. Check pre-open data at 9:08 for gap + imbalance signals.

**Delivery % filter:** Use as a quality gate — stocks with consistently high delivery are cleaner trending instruments; low delivery often means purely intraday retail churn.

**Live intraday ticks:** NSE site cannot be polled fast or reliably. Hand off to a broker WebSocket — see [[10 — APIs (broker + data)]].

**Building a local historical database:** eod2 is the easiest starting point; it handles incremental updates automatically so you are not re-downloading the full history every session. More in [[11 — Build Your Own Screener]].

---

*Next: [[10 — APIs (broker + data)]] | [[11 — Build Your Own Screener]]*
