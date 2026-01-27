# Deployment Guide - Serverless Architecture

This guide will help you deploy the Stock MA Monitor using a fully serverless architecture with GitHub Pages (frontend) and JSONBin.io (data storage), powered by GitHub Actions for automated data updates.

## Architecture Overview

```
┌─────────────────┐      Schedule        ┌──────────────────┐
│  GitHub Actions │ ──────────────────> │  Python Script    │
│  (Every 4 hrs)  │                      │  (Parallel Fetch) │
└─────────────────┘                      └─────────┬────────┘
                                                   │
                                                   │ Upload
                                                   ▼
                                         ┌──────────────────┐
┌─────────────────┐      Fetch           │   JSONBin.io     │
│  GitHub Pages   │ ◄─────────────────── │  (JSON Storage)  │
│   (Frontend)    │                      └──────────────────┘
└─────────────────┘
```

**Benefits:**
- 100% free hosting
- No server maintenance
- Automatic data updates every 4 hours during market hours
- Fast parallel processing (10 concurrent stocks)
- Global CDN distribution via GitHub Pages

---

## Step 1: Create JSONBin.io Account

JSONBin.io provides free JSON storage that we'll use to store stock data.

### 1.1 Sign Up

1. Go to [https://jsonbin.io](https://jsonbin.io)
2. Click "Sign Up" (top right)
3. Create a free account (GitHub login recommended)
4. Verify your email address

### 1.2 Create a New Bin

1. After logging in, click "Create Bin" (or go to dashboard)
2. In the JSON editor, paste this initial structure:
```json
{
  "stocks": [],
  "metadata": {
    "total_count": 0,
    "near_ma_count": 0,
    "above_count": 0,
    "below_count": 0,
    "processing_time": 0,
    "last_updated": null,
    "version": "1.0.0"
  }
}
```
3. Click "Create"
4. **Save the Bin ID** - it's in the URL: `https://jsonbin.io/v3/b/<YOUR_BIN_ID>`
   - Example: If URL is `https://jsonbin.io/v3/b/67a1b2c3d4e5f6g7h8i9j0k1`, your Bin ID is `67a1b2c3d4e5f6g7h8i9j0k1`

### 1.3 Get Your API Key

1. Click your profile icon (top right) → "API Keys"
2. Click "Create Access Key"
3. Name it (e.g., "stocks-near-ma")
4. Leave permissions as default (Read & Write)
5. Click "Create"
6. **Copy the API Key** - it starts with `$2b$10$...`
   - Example: `$2b$10$AbCdEfGhIjKlMnOpQrStUvWxYz1234567890`
7. **Important:** Save this key securely - you won't be able to see it again!

---

## Step 2: Configure GitHub Repository

### 2.1 Add GitHub Secrets

GitHub Secrets store sensitive credentials securely for GitHub Actions.

1. Go to your GitHub repository
2. Click "Settings" tab
3. In left sidebar, click "Secrets and variables" → "Actions"
4. Click "New repository secret"
5. Add **TWO secrets**:

**Secret 1: JSONBIN_API_KEY**
- Name: `JSONBIN_API_KEY`
- Value: Paste your JSONBin API key (e.g., `$2b$10$AbCdEfGhIj...`)
- Click "Add secret"

**Secret 2: JSONBIN_BIN_ID**
- Name: `JSONBIN_BIN_ID`
- Value: Paste your Bin ID (e.g., `67a1b2c3d4e5f6g7h8i9j0k1`)
- Click "Add secret"

### 2.2 Verify GitHub Actions Workflow

The workflow file `.github/workflows/update-stocks.yml` is already set up to:
- Run every 4 hours during market hours (Mon-Fri, 9 AM - 4 PM ET)
- Allow manual triggering via "Actions" tab
- Automatically run on push to main branch

**No changes needed** - it will use the secrets you just added.

---

## Step 3: Configure Frontend

Update the frontend to use your JSONBin.io credentials.

### 3.1 Edit api.js

Open `frontend/js/api.js` and replace the placeholder values:

```javascript
// CONFIGURATION: Update these values with your JSONBin credentials
const JSONBIN_BIN_ID = '67a1b2c3d4e5f6g7h8i9j0k1'; // Replace with YOUR Bin ID
const JSONBIN_API_KEY = '$2b$10$AbCdEfGhIjKlMnOpQrStUv...'; // Replace with YOUR API key
```

**Example (AFTER replacing):**
```javascript
const JSONBIN_BIN_ID = '67a1b2c3d4e5f6g7h8i9j0k1';
const JSONBIN_API_KEY = '$2b$10$xQ9pR7sT3uV2wX1yZ4aB5c6D7e8F9g0H1i2J3k4L5m6N7o8P9q0R1s2T3u4V';
```

**Security Note:** Your API key will be visible in the frontend code. For read-only access, this is acceptable. If you want extra security, you can create a separate "Read-Only" API key in JSONBin.io.

---

## Step 4: Initial Data Upload

Before going live, populate your JSONBin with initial stock data.

### Option A: Manual Trigger via GitHub Actions (Recommended)

1. Push your code to GitHub (with updated `api.js`)
2. Go to your repo → "Actions" tab
3. Click "Update Stock Data" workflow (left sidebar)
4. Click "Run workflow" → "Run workflow"
5. Wait 2-3 minutes for completion
6. Check "stock-data-summary" artifact for results

### Option B: Local Upload (Alternative)

If you want to test locally first:

```bash
# Set environment variables (Windows)
set JSONBIN_API_KEY=your_api_key_here
set JSONBIN_BIN_ID=your_bin_id_here

# Set environment variables (Mac/Linux)
export JSONBIN_API_KEY=your_api_key_here
export JSONBIN_BIN_ID=your_bin_id_here

# Run the script
python scripts/fetch_stocks.py
```

This will:
- Fetch all S&P 500 stocks + major ETFs
- Process them in parallel (10 at a time)
- Upload to JSONBin.io
- Take ~35 seconds total

---

## Step 5: Enable GitHub Pages

Deploy your frontend to GitHub Pages for free hosting.

### 5.1 Configure GitHub Pages

1. Go to your repo → "Settings" → "Pages" (left sidebar)
2. Under "Source", select:
   - **Source:** Deploy from a branch
   - **Branch:** `main` (or `master`)
   - **Folder:** `/frontend` (or `/root` if you move frontend files to root)
3. Click "Save"
4. Wait 2-3 minutes for deployment

### 5.2 Access Your Site

Your site will be available at:
```
https://<your-username>.github.io/<repo-name>/
```

**Example:**
- Username: `johndoe`
- Repo: `stocks-near-ma`
- URL: `https://johndoe.github.io/stocks-near-ma/`

**Note:** If deploying from `/frontend` folder, your URL might be:
```
https://<your-username>.github.io/<repo-name>/frontend/
```

To avoid the `/frontend` in URL, you can:
1. Move `frontend/*` files to repository root
2. Or configure GitHub Pages custom domain

---

## Step 6: Verify Deployment

### 6.1 Check Data in JSONBin.io

1. Go to [https://jsonbin.io](https://jsonbin.io) → Dashboard
2. Click your bin
3. Verify you see stock data (not empty arrays)
4. Check `metadata.last_updated` has a recent timestamp

### 6.2 Test GitHub Actions

1. Go to repo → "Actions" tab
2. Find your latest "Update Stock Data" run
3. Click on it → Check for green checkmarks
4. Download "stock-data-summary" artifact to see statistics

### 6.3 Test Frontend

1. Visit your GitHub Pages URL
2. Verify stocks load (should see 500+ stocks)
3. Test search functionality (try "AAPL", "TSLA", "SPY")
4. Test filters (Near MA, Above/Below)
5. Check "Last updated" timestamp

---

## Maintenance & Monitoring

### Automatic Updates

The GitHub Actions workflow runs automatically:
- **Schedule:** Every 4 hours during market hours (Mon-Fri, 9 AM - 4 PM ET)
- **Cron:** `0 9,13,17,21 * * 1-5` (UTC times: 9:00, 13:00, 17:00, 21:00)

**No manual intervention needed!**

### Manual Updates

To manually trigger an update:
1. Go to repo → "Actions" tab
2. Click "Update Stock Data" → "Run workflow"
3. Data will refresh in 2-3 minutes

### Monitoring

**Check workflow status:**
- Go to "Actions" tab to see recent runs
- Green ✓ = successful
- Red ✗ = failed (check logs)

**Check data freshness:**
- Visit your site
- Look at "Last updated" timestamp
- Should update every 4 hours during market hours

### Troubleshooting

**Problem: Frontend shows "Failed to load stock data"**
- Check that `api.js` has correct Bin ID and API key
- Verify JSONBin.io has data (check dashboard)
- Check browser console for errors (F12)

**Problem: GitHub Actions failing**
- Go to Actions → Click failed run → Check logs
- Common issues:
  - Secrets not set correctly
  - JSONBin.io API rate limit (unlikely on free tier)
  - Network timeout (retry usually works)

**Problem: Data not updating**
- Check Actions tab for failed runs
- Verify cron schedule matches your timezone expectations
- Manually trigger workflow to test

**Problem: GitHub Pages not loading**
- Wait 5-10 minutes after first deployment
- Check Settings → Pages for any errors
- Ensure `index.html` is in correct folder

---

## Cost & Limits

### JSONBin.io Free Tier
- **Storage:** Unlimited bins
- **Requests:** 10,000 requests/month
- **Bin Size:** Up to 500 KB per bin
- **Our Usage:** ~4 updates/day × 30 days = 120 requests/month (well within limit)

### GitHub Actions Free Tier
- **Minutes:** 2,000 minutes/month (Free tier)
- **Our Usage:** ~3 minutes/run × 4 runs/day × 22 business days = ~264 minutes/month
- **Storage:** 500 MB artifacts (our summary files are tiny)

### GitHub Pages
- **Bandwidth:** 100 GB/month
- **Site Size:** 1 GB max
- **Our Usage:** Frontend is <1 MB, bandwidth depends on traffic

**Total Cost: $0/month** 🎉

---

## Advanced Configuration

### Change Update Frequency

Edit `.github/workflows/update-stocks.yml`:

```yaml
schedule:
  - cron: '0 */2 * * 1-5'  # Every 2 hours (Mon-Fri)
  - cron: '0 9,12,15,18 * * 1-5'  # 4 specific times
```

**Cron format:** `minute hour day month weekday`
- Use [crontab.guru](https://crontab.guru) to test schedules

### Add More Stocks

Edit `scripts/fetch_stocks.py`:

```python
custom_stocks = [
    'TSLA', 'AAPL', 'NVDA', 'AMD',
    'YOUR_STOCK_HERE',  # Add your stocks
]
```

Commit and push - next scheduled run will include them.

### Custom Domain

1. Buy a domain (e.g., `stocks.yourdomain.com`)
2. Add CNAME record pointing to `<username>.github.io`
3. In GitHub Settings → Pages → Custom domain, enter your domain
4. Enable "Enforce HTTPS"

---

## Migration from Local Backend

If you previously used the FastAPI backend (`backend/` folder):

**What's changed:**
- ❌ No longer need to run `python backend/app.py`
- ❌ No localhost:8000 server
- ✅ Data pre-generated by GitHub Actions
- ✅ Hosted on GitHub Pages (static files)
- ✅ Fetches from JSONBin.io instead of local API

**What's kept:**
- ✅ Same parallel processing (10 workers, ~35s load time)
- ✅ Same UI/UX (search, filters, sorting)
- ✅ Same S&P 500 + ETF coverage
- ✅ Same 150-day MA calculations

---

## Support

**Issues:**
- Report bugs: [GitHub Issues](https://github.com/YOUR_USERNAME/stocks-near-ma/issues)

**Questions:**
- Check existing issues first
- Provide error messages and logs

**Updates:**
- Star the repo to get notified of updates
- Pull latest changes: `git pull origin main`

---

## Summary Checklist

- [ ] Created JSONBin.io account
- [ ] Created a bin and saved Bin ID
- [ ] Got API key and saved it securely
- [ ] Added JSONBIN_API_KEY to GitHub Secrets
- [ ] Added JSONBIN_BIN_ID to GitHub Secrets
- [ ] Updated `frontend/js/api.js` with your credentials
- [ ] Pushed code to GitHub
- [ ] Triggered initial data upload (via Actions or locally)
- [ ] Enabled GitHub Pages
- [ ] Verified site works at GitHub Pages URL
- [ ] Verified automatic updates are running

**You're done!** Your stock monitor is now fully deployed and will update automatically. 🚀
