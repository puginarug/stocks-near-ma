# Stock MA Monitor

A serverless web application for monitoring S&P 500 stocks and ETFs, calculating their distance from the 150-day moving average. Deployed on GitHub Pages with automated data updates via GitHub Actions.

## Features

- 🚀 **Fully Serverless**: No backend required - runs entirely on GitHub Pages
- ⚡ **Parallel Processing**: Processes 500+ stocks in ~35 seconds using 10 concurrent workers
- 🔄 **Auto-Updates**: Stock data refreshes every 4 hours via GitHub Actions
- 🔍 **Stock Search**: Quickly find specific stocks (e.g., AAPL, TSLA, SPY)
- 📊 **Real-time Statistics**: Total stocks, near MA count, above/below MA counts
- 🎯 **Advanced Filtering**: Filter by proximity to MA (±5%) and direction (ABOVE/BELOW)
- 📈 **Sortable Table**: Click column headers to sort by any metric
- 🎨 **Color Coding**: Red (above MA), Green (below MA), Yellow (near MA)
- 📱 **Responsive Design**: Works on desktop and mobile
- 💰 **100% Free**: GitHub Pages + JSONBin.io free tiers

## Quick Start

### For Users (View Live Demo)

Simply visit the GitHub Pages URL (if deployed):
```
https://<your-username>.github.io/stocks-near-ma/
```

Stock data updates automatically every 4 hours during market hours (Mon-Fri).

### For Developers (Local Development)

**Option 1: Use Deployed Data (Simplest)**

1. Configure `frontend/js/api.js` with your JSONBin.io credentials
2. Open `frontend/index.html` in your browser
3. Done! No backend server needed.

**Option 2: Run with Local Backend (For Development)**

If you want to test the backend locally or make changes to the data processing:

```bash
# Navigate to backend folder
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

Then open `frontend/index.html` in your browser.

### Deploy Your Own

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions using GitHub Pages + JSONBin.io.

## How It Works

### Serverless Architecture

```
GitHub Actions (Scheduled) → Python Script (Parallel Processing) → JSONBin.io (Storage)
                                                                           ↓
                                                          GitHub Pages ← Fetch Data
```

**Data Pipeline** (GitHub Actions):
- Runs every 4 hours during market hours (Mon-Fri, 9 AM - 4 PM ET)
- Fetches stock data from Yahoo Finance using `yfinance`
- Processes 10 stocks concurrently with ThreadPoolExecutor
- Calculates 150-day moving averages in parallel
- Uploads results to JSONBin.io (~35 seconds total)

**Frontend** (GitHub Pages):
- Pure vanilla JavaScript (no frameworks)
- Fetches pre-processed data from JSONBin.io
- Client-side filtering, sorting, and search
- Responsive table with color coding
- Real-time statistics calculation

### Performance

- **Sequential Processing**: ~260 seconds for 500 stocks
- **Parallel Processing (10 workers)**: ~35 seconds for 500 stocks
- **Speedup**: 7.5x faster! 🚀
- **Deployment**: 100% serverless, 100% free

## Project Structure

```
stocks-near-ma/
├── .github/
│   └── workflows/
│       └── update-stocks.yml     # GitHub Actions workflow (runs every 4 hours)
│
├── scripts/
│   └── fetch_stocks.py           # Data fetcher with parallel processing
│
├── backend/                      # FastAPI backend (optional for local dev)
│   ├── app.py                    # Main FastAPI application
│   ├── requirements.txt          # Backend dependencies
│   ├── models/
│   │   └── stock_models.py       # Pydantic data models
│   ├── services/
│   │   ├── stock_service.py      # Stock data fetching
│   │   └── parallel_processor.py # Parallel processing logic
│   └── utils/
│       ├── cache.py              # In-memory caching
│       └── sp500_fetcher.py      # S&P 500 list fetcher
│
├── frontend/                     # HTML/CSS/JS frontend (deployed to GitHub Pages)
│   ├── index.html               # Main HTML page
│   ├── css/
│   │   └── styles.css           # Styling
│   └── js/
│       ├── app.js               # Main application logic
│       ├── api.js               # API client (fetches from JSONBin.io)
│       ├── table.js             # Table rendering
│       └── filters.js           # Filter & search logic
│
├── DEPLOYMENT.md                 # Detailed deployment guide
└── README.md                     # This file
```

## Data & APIs

### JSONBin.io Storage

Stock data is stored in JSONBin.io with the following structure:
```json
{
  "stocks": [
    {
      "symbol": "AAPL",
      "price": 178.25,
      "ma_150": 175.50,
      "distance_percent": 1.57,
      "distance_abs": 1.57,
      "direction": "ABOVE",
      "near_ma": true
    }
  ],
  "metadata": {
    "total_count": 520,
    "near_ma_count": 42,
    "above_count": 310,
    "below_count": 210,
    "processing_time": 35.2,
    "last_updated": "2026-01-26T14:30:00Z",
    "version": "1.0.0"
  }
}
```

### Local Backend API (Optional)

If running the FastAPI backend locally:

- `GET /api/stocks?include_custom=NVDA,AMD` - Fetch all stock data with parallel processing
- `GET /api/sp500-tickers` - Get S&P 500 ticker list
- `GET /api/statistics` - Get aggregated statistics
- `GET /api/health` - Health check endpoint
- `POST /api/cache/clear` - Clear cached data
- `GET /docs` - Interactive API documentation (Swagger UI)

## Usage

### Search for Stocks

Use the search bar to find specific stocks:
- Type partial symbols (e.g., "AA" finds AAPL, AAL, etc.)
- Or exact symbols (e.g., "TSLA", "SPY", "NVDA")
- Click "Clear" to reset search

### Apply Filters

- **Near MA Filter**: Check "Show only stocks near MA" to see stocks within ±5% of their 150-day MA
- **Direction Filter**: Select "ABOVE" or "BELOW" to filter by direction
- **Sorting**: Click any column header to sort by any metric
- **Combine Filters**: Use search + filters together for precise results

### Color Coding

- 🔴 **Red**: Stock is trading ABOVE its 150-day MA
- 🟢 **Green**: Stock is trading BELOW its 150-day MA
- 🟡 **Yellow highlight**: Stock is within ±5% of its MA (🔔 indicator)

### Adding More Stocks

To include additional stocks in the dataset:

1. Edit `scripts/fetch_stocks.py`
2. Add tickers to `custom_stocks` list:
```python
custom_stocks = [
    'TSLA', 'AAPL', 'NVDA', 'AMD',
    'YOUR_TICKER_HERE',  # Add your stocks
]
```
3. Commit and push to GitHub
4. Next scheduled run (or manual trigger) will include them

## Troubleshooting

### Frontend Shows "Failed to load stock data"

**Check:**
1. Verify `frontend/js/api.js` has correct JSONBin credentials
2. Check JSONBin.io dashboard - does your bin have data?
3. Open browser console (F12) - any error messages?
4. Try refreshing the page

### Data Seems Outdated

**Check:**
1. Look at "Last updated" timestamp on the page
2. Go to GitHub → Actions tab → Check recent workflow runs
3. If workflow failed, check logs for errors
4. Manually trigger workflow: Actions → "Update Stock Data" → "Run workflow"

### GitHub Actions Failing

**Common causes:**
1. GitHub Secrets not set correctly (check JSONBIN_API_KEY and JSONBIN_BIN_ID)
2. JSONBin.io API rate limit (unlikely - free tier is 10k/month, we use ~120/month)
3. Network timeout (retry usually fixes it)

**To debug:**
1. Go to Actions tab → Click failed run
2. Expand failed step to see error logs
3. Check "stock-data-summary" artifact (if available)

### Local Backend Issues

If running backend locally and seeing errors:

**Port Already in Use:**
```bash
# Windows - Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Use different port
python app.py --port 8001
```

**Failed to Install Dependencies:**
- Ensure Python 3.10+ (tested with 3.14)
- Try: `pip install --upgrade pip`
- Then: `pip install -r requirements.txt`

## Development

### Testing Locally

**Frontend Development:**
- Edit files in `frontend/`
- Open `index.html` in browser or use local server:
  ```bash
  cd frontend
  python -m http.server 3000
  ```
- Refresh browser to see changes - no build step required!

**Backend Development (Optional):**
```bash
cd backend
uvicorn app:app --reload --port 8000
```
Code changes automatically restart the server.

**Testing Data Pipeline:**
```bash
# Set environment variables
export JSONBIN_API_KEY=your_key
export JSONBIN_BIN_ID=your_bin_id

# Run data fetcher
python scripts/fetch_stocks.py
```

### Modifying Stock List

Edit `scripts/fetch_stocks.py` to change included stocks:
```python
custom_etfs = [
    'SPY', 'QQQ', 'DIA',  # Major indexes
    # Add your ETFs
]

custom_stocks = [
    'TSLA', 'AAPL', 'NVDA',
    # Add your stocks
]
```

### Running Tests

```bash
cd backend
python -m pytest tests/
```

## Deployment

### Serverless Deployment (Recommended)

**See [DEPLOYMENT.md](DEPLOYMENT.md) for complete step-by-step instructions.**

Quick overview:
1. Create JSONBin.io account (free)
2. Add GitHub Secrets (JSONBIN_API_KEY, JSONBIN_BIN_ID)
3. Update `frontend/js/api.js` with your credentials
4. Enable GitHub Pages
5. Done! Data auto-updates every 4 hours

**Benefits:**
- 100% free (GitHub Pages + JSONBin.io free tiers)
- No server maintenance
- Automatic updates via GitHub Actions
- Global CDN distribution

### Alternative: Traditional Backend Deployment

If you prefer to run the FastAPI backend continuously:

**Backend:**
- **Railway**: Auto-detects FastAPI apps (easiest)
- **Render**: Free tier available
- **Heroku**: `web: uvicorn app:app --host=0.0.0.0 --port=$PORT`
- **AWS Lambda**: Use Mangum adapter

**Frontend:**
- **Netlify/Vercel**: Drag & drop `frontend/` folder
- **GitHub Pages**: Enable in repo settings
- Update `frontend/js/api.js` with backend URL

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - feel free to modify and use as needed.

## Tech Stack

- **Frontend:** Vanilla JavaScript (ES6 modules), HTML5, CSS3
- **Data Processing:** Python 3.10+, yfinance, pandas
- **Automation:** GitHub Actions
- **Storage:** JSONBin.io (free JSON storage)
- **Hosting:** GitHub Pages (free static hosting)
- **Backend (Optional):** FastAPI, uvicorn
- **Parallel Processing:** ThreadPoolExecutor (10 concurrent workers)

## Acknowledgments

- Stock data provided by [Yahoo Finance](https://finance.yahoo.com) via `yfinance`
- S&P 500 list from [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)
- Free hosting by [GitHub Pages](https://pages.github.com/)
- Free JSON storage by [JSONBin.io](https://jsonbin.io)
- Built with [FastAPI](https://fastapi.tiangolo.com/), vanilla JavaScript, and ❤️
