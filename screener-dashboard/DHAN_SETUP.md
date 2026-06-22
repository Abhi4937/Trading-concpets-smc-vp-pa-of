# Dhan Account & API Setup

Step-by-step guide to get live NSE data flowing into the screener via DhanHQ v2 API.

---

## Step 1 — Open a Dhan account

1. Go to [dhan.co](https://dhan.co) and click **Open Demat Account**.
2. Complete full KYC: PAN card, Aadhaar, bank account details.
3. Wait for account activation (typically 1–2 business days).

> You need a real, KYC-complete brokerage account — not just a developer account.

---

## Step 2 — Log in to the Dhan web platform

Go to [web.dhan.co](https://web.dhan.co) and log in with your credentials.

---

## Step 3 — Generate an Access Token and note your Client ID

1. In the top-right corner, click your **Profile icon** or name.
2. Look for a menu item called **DhanHQ Trading APIs**, **Access DhanHQ APIs**, or similar.
   > Exact menu names may differ — Dhan updates their UI periodically. If you can't find it,
   > check [dhanhq.co/docs/v2/](https://dhanhq.co/docs/v2/) under the Authentication section.
3. Click **Generate Access Token** (or **Create Token**).
4. Choose a validity period — up to ~30 days is typical.
5. Copy and save:
   - **Access Token** — a long JWT string (starts with `ey...`)
   - **Client ID** — your numeric Dhan user/client identifier

> Tokens expire. If live data stops working, regenerate the token and update `server/.env`.

---

## Step 4 — Check Data API subscription (if quotes stop working)

The standard DhanHQ account includes REST market quotes (`/v2/marketfeed/quote`).  
The **Live Market Feed** (WebSocket) may require a separate **Data API** subscription.

If the backend returns an HTTP 402 or 429 error, check your Dhan dashboard for a
"Data APIs" or "Market Feed" subscription option and enable it.

> This screener uses only the REST endpoints (not WebSocket), so a standard account
> should be sufficient — but verify on your Dhan dashboard if you encounter errors.

---

## Step 5 — Configure the backend

```bash
cd screener-dashboard

# Copy the env template
cp server/.env.example server/.env
```

Open `server/.env` in any text editor and fill in your values:

```
DHAN_CLIENT_ID=1000123456
DHAN_ACCESS_TOKEN=eyJhbGciOiJIUzUxMiJ9.eyJ...
PORT=8787
```

> **Never commit `server/.env`** — it is in `.gitignore`.

---

## Step 6 — Install dependencies and run

```bash
npm install          # installs express, cors, dotenv, concurrently

npm run dev:all      # starts Vite (frontend) + Express (backend) together
```

Or in two separate terminals:

```bash
npm run dev          # terminal 1 — Vite at http://localhost:5173
npm run server       # terminal 2 — Express at http://localhost:8787
```

Open [http://localhost:5173](http://localhost:5173).  
The header badge should change from amber **SAMPLE DATA** to green **● LIVE**.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Badge stays amber (SAMPLE DATA) | Backend not running or token missing | Run `npm run server`, check `server/.env` |
| `401` in server logs | Token invalid or expired | Regenerate token in Dhan dashboard |
| `402` or `429` in logs | Subscription or rate limit | Check Data API subscription on Dhan dashboard |
| Symbol not found in scrip master | Column name mismatch | See `SECURITY_ID_CANDIDATES` in `server/instruments.js` |
| `relVol` looks low early in session | Known limitation | See comment in `server/screenerService.js::computeRelVol` |

---

## API reference

- Overview & auth: [dhanhq.co/docs/v2/](https://dhanhq.co/docs/v2/)
- Market quotes: `POST https://api.dhan.co/v2/marketfeed/quote`
- Daily history: `POST https://api.dhan.co/charts/historical`
- Intraday: `POST https://api.dhan.co/charts/intraday`
- Scrip master CSV: `https://images.dhan.co/api-data/api-scrip-master.csv`
