# Trading Concepts — SMC · Volume Profile · Price Action · Order Flow

A research archive of trading-education material from three well-known YouTube
channels, plus original synthesized concept write-ups and a side-by-side
comparison of their methods.

## What's here

### 📝 Concept write-ups (original synthesis)
Distilled, faithful summaries of each channel's actual method — built by reading
across the full transcript corpus (276 videos):

- [`Trader Dale/CONCEPTS.md`](Trader%20Dale/CONCEPTS.md) — Volume Profile · Order Flow · VWAP · Price Action
- [`Fractal Flow Pro/CONCEPTS.md`](Fractal%20Flow%20Pro/CONCEPTS.md) — first-principles price action, Andrews Pitchfork, "REAL" SMC, FFS/MMS/NTS strategies
- [`Photon Trading/CONCEPTS.md`](Photon%20Trading/CONCEPTS.md) — mechanical smart-money / supply & demand
- [`COMPARISON.md`](COMPARISON.md) — all three methods side-by-side (shared DNA, a "same idea / different names" map, where they disagree)

### 🎬 Transcripts
Full English transcripts of the source videos, organized by channel and topic
playlist, each with a title + source URL header:

| Channel | Topics | Videos |
|---|---|---|
| **Trader Dale** | Volume Profile, Order Flow, VWAP, Price Action | 118 |
| **Fractal Flow Pro** | Market Structure, SMC, TA Vault, Pitchfork, Candlesticks, Strategies, … | 137 |
| **Photon Trading** | Market Structure, Supply & Demand, Profitability, Psychology | 21 |

Each channel folder has an `INDEX.md` listing every video with word counts.

### 📚 Books
Reference trading books (Volume Price Analysis, Order Flow, VWAP, options &
volatility, SMC/ICT, trading psychology).

### 🛠️ Pipeline (reproducible)
The scripts used to build the transcript archive:

- `fetch_channel.py` — config-driven: enumerate a channel's playlists via `yt-dlp`, download English captions, clean VTT → readable prose, write one `.txt` per video + an `INDEX.md`.
- `traderdale.json`, `fractalflowpro.json`, `photontrading.json` — per-channel configs (playlists, output folder, optional skip filters).

Usage: `python fetch_channel.py <channel>.json` (needs `yt-dlp`; authenticated
caption downloads need a `cookies.txt`, which is **not** included).

## ⚠️ Disclaimer

- **Educational / research use only.** Transcripts and books are the
  intellectual property of their respective creators, authors, and publishers
  and are included here for personal study and commentary. No ownership is
  claimed. If you are a rights holder and want material removed, open an issue
  and it will be taken down.
- **Not financial advice.** None of the methods described are independently
  verified or proven profitable. Trading carries substantial risk of loss.
