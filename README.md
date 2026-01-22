# Stock Alert System

A simple system for monitoring stocks and ETFs relative to their 150-day moving average. Features an interactive Streamlit dashboard showing all S&P 500 stocks in a sortable table.

## Features

- 📊 **Interactive Streamlit Dashboard** - View all S&P 500 stocks in a sortable table
- 📱 **Mobile-Friendly** - Works great on phones and tablets
- 🔔 **Alert Indicators** - Highlights stocks within 5% of their 150-day MA
- 🎯 **Sortable & Filterable** - Sort by any column, filter by direction or proximity
- 📥 **Export Data** - Download table as CSV
- 🌐 **Shareable** - Deploy to Streamlit Cloud to share with friends
- 🔄 **Auto-Refresh** - Data cached for 1 hour
- ⚡ **Fast & Lightweight** - Efficient data loading with progress tracking

## Requirements

- Python 3.7+
- Windows/macOS/Linux with desktop notification support

## Quick Start

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit dashboard:
```bash
streamlit run streamlit_app.py
```

4. Open your browser to the URL shown (usually http://localhost:8501)

That's it! The dashboard will load all S&P 500 stocks and display them in a sortable table.

## Dashboard Features

### Main View
- **Sortable Table**: Click any column header to sort
- **Color-Coded**:
  - 🔴 Red background = Stock is ABOVE its 150-day MA
  - 🟢 Green background = Stock is BELOW its 150-day MA
  - 🟡 Yellow highlight = Stock within 5% of MA (potential alert)

### Filters (Sidebar)
- **Show only near MA**: Display stocks within ±5% of their 150-day MA
- **Direction filter**: Show only stocks ABOVE or BELOW their MA

### Stats Bar
- Total stocks loaded
- Number of stocks near MA
- Number above/below MA

### Export
- Download button to save current view as CSV

## Sharing with Friends

### Deploy to Streamlit Cloud (Free!)

1. Push your code to GitHub

2. Go to [share.streamlit.io](https://share.streamlit.io)

3. Sign in with GitHub

4. Deploy your app by selecting:
   - Repository: your-repo
   - Branch: main
   - Main file: streamlit_app.py

5. Share the URL with friends!

**Note**: Streamlit Cloud is free and your app will be accessible from any device with a browser.

### Run Locally and Share on LAN

1. Find your local IP address:
   ```bash
   # Windows
   ipconfig

   # Mac/Linux
   ifconfig
   ```

2. Run Streamlit with network access:
   ```bash
   streamlit run streamlit_app.py --server.address 0.0.0.0
   ```

3. Share the URL with friends on the same network:
   ```
   http://YOUR-IP:8501
   ```

## Usage

### Starting the Dashboard

```bash
streamlit run streamlit_app.py
```

The dashboard will:
1. Load all S&P 500 tickers from Wikipedia
2. Fetch current prices and calculate 150-day MA for each stock
3. Display everything in an interactive sortable table
4. Cache data for 1 hour (click "Rerun" in Streamlit to refresh)

### Using the Dashboard

**Sorting**:
- Click any column header to sort by that column
- Click again to reverse sort order

**Filtering**:
- Open sidebar (top-left corner)
- Enable "Show only stocks near MA" to see potential opportunities
- Use direction filter to show only ABOVE or BELOW

**Mobile Use**:
- Dashboard is fully responsive
- Works on phones and tablets
- Sidebar collapses automatically on mobile

**Sharing**:
- Use the download button to export CSV
- Deploy to Streamlit Cloud for permanent access
- Or share your local IP address with friends on same network

To stop the dashboard, press `Ctrl+C` in the terminal.

## Example Dashboard

The dashboard displays a table with these columns:

| Symbol | Price | 150-Day MA | Distance (%) | Distance (abs) | Direction | Near MA (5%) |
|--------|-------|------------|--------------|----------------|-----------|--------------|
| AAPL   | 175.50 | 177.00   | -0.85        | 0.85          | BELOW     | 🔔           |
| MSFT   | 420.30 | 385.20   | 9.11         | 9.11          | ABOVE     |              |
| GOOGL  | 142.80 | 145.60   | -1.92        | 1.92          | BELOW     | 🔔           |

**Stats shown at top**:
- Total Stocks: 503
- Near MA (±5%): 47
- Above MA: 312
- Below MA: 191

## Log Files

All alerts are logged to [alerts.log](alerts.log):
- Alert notifications sent
- Errors and warnings
- System start/stop events

## What's Included

### By Default
The dashboard automatically loads **all S&P 500 stocks** (503 stocks as of 2026).

The S&P 500 includes major companies like:
- AAPL (Apple)
- MSFT (Microsoft)
- GOOGL (Alphabet/Google)
- AMZN (Amazon)
- TSLA (Tesla)
- NVDA (NVIDIA)
- And 497+ more

### Want to Monitor Other Stocks or ETFs?

You can easily modify [streamlit_app.py](streamlit_app.py) to monitor different lists:

**Option 1**: Add specific tickers manually
```python
# Replace the get_sp500_tickers() function with:
def get_sp500_tickers():
    return ['AAPL', 'MSFT', 'GOOGL', 'SPY', 'QQQ', 'VTI']
```

**Option 2**: Monitor popular ETFs
```python
def get_sp500_tickers():
    return ['SPY', 'QQQ', 'VTI', 'IWM', 'DIA', 'VOO', 'VEA', 'VWO', 'AGG', 'BND']
```

**Option 3**: Combine S&P 500 with ETFs
```python
def get_sp500_tickers():
    # Get S&P 500 as usual
    sp500 = [fetch from Wikipedia]
    # Add ETFs
    etfs = ['SPY', 'QQQ', 'VTI', 'IWM']
    return sp500 + etfs
```

## Troubleshooting

### Dashboard loads slowly
- Loading 500+ stocks takes 3-5 minutes on first load
- Data is cached for 1 hour after first load
- Rate limiting by Yahoo Finance may slow things down
- Consider running during off-peak hours

### Some stocks show no data
- Stock may not have 150+ days of historical data
- Recently IPO'd companies won't have enough data
- Ticker symbol may have changed
- Yahoo Finance may be temporarily unavailable for that symbol

### "Connection Error" or rate limiting
- Yahoo Finance has rate limits
- Try again in a few minutes
- The app adds small delays (1 second every 50 stocks) to help avoid limits
- Running multiple instances simultaneously can trigger limits

### Dashboard won't start
- Ensure Streamlit is installed: `pip install streamlit`
- Check Python version (requires 3.7+)
- Try: `pip install --upgrade streamlit yfinance`

### Mobile display issues
- Dashboard is responsive and should work on all devices
- Try landscape mode on phones for better table viewing
- Use the sidebar filters to reduce visible data
- Zoom out if table appears too large

## Project Structure

```
stock-alert-system/
├── streamlit_app.py     # 📊 Main Streamlit dashboard (START HERE!)
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .gitignore          # Git ignore rules
│
├── add_sp500.py        # Helper: Add all S&P 500 to config
├── main.py             # Legacy: Background monitoring system
├── notifier.py         # Legacy: WhatsApp notification handler
├── web_server.py       # Legacy: Flask web dashboard
├── config.yaml         # Legacy: Alert configuration
└── templates/          # Legacy: Flask templates
    └── index.html
```

**Note**: The `main.py`, `notifier.py`, and `web_server.py` files are legacy components for background monitoring and WhatsApp alerts. The Streamlit dashboard ([streamlit_app.py](streamlit_app.py)) is the recommended way to use this tool.

## Deploying to Streamlit Cloud

Want to access your dashboard from anywhere and share with friends? Deploy to Streamlit Cloud for free!

### Step 1: Prepare Your Repository

1. Create a GitHub repository (if you haven't already)
2. Push your code:
   ```bash
   git init
   git add streamlit_app.py requirements.txt .gitignore
   git commit -m "Add stock monitoring dashboard"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Fill in:
   - **Repository**: Select your repo
   - **Branch**: main
   - **Main file path**: streamlit_app.py
5. Click "Deploy"

### Step 3: Share Your Dashboard

After deployment (takes 2-3 minutes), you'll get a URL like:
```
https://your-username-stock-alert-system-streamlit-app-abc123.streamlit.app
```

Share this URL with friends! They can:
- View all S&P 500 stocks and their MA status
- Sort and filter the table
- Download data as CSV
- Access from any device (phone, tablet, computer)

**Notes**:
- Free tier allows unlimited public apps
- App "goes to sleep" after inactivity (wakes up on first visit)
- Data refreshes every hour due to caching
- Perfect for checking stocks on the go!

## Performance Tips

### For Faster Loading
1. The first load takes 3-5 minutes (loading 500+ stocks)
2. After that, data is cached for 1 hour
3. Consider monitoring fewer stocks if speed is critical
4. Deploy to Streamlit Cloud - it stays "warm" with regular visitors

### For Better Mobile Experience
1. Use the sidebar filters to reduce visible data
2. Sort by "Distance (abs)" to see stocks nearest their MA first
3. Enable "Show only near MA" to see just the important stocks
4. Download CSV for offline analysis

## License

MIT License - feel free to modify and use as needed.
