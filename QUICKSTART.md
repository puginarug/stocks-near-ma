# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Dashboard
```bash
streamlit run streamlit_app.py
```

### 3. Open Your Browser
The dashboard will automatically open, or go to:
```
http://localhost:8501
```

## 📱 Using the Dashboard

### Desktop
- **Sort**: Click any column header
- **Filter**: Open sidebar (☰ icon) and use filters
- **Export**: Click "Download CSV" button at bottom

### Mobile
- Sidebar auto-collapses on mobile
- Tap ☰ icon in top-left to access filters
- Scroll horizontally to see all columns
- Works great in landscape mode!

## 🌐 Sharing with Friends

### Quick Share (Same Network)
1. Find your IP address
2. Run with: `streamlit run streamlit_app.py --server.address 0.0.0.0`
3. Share `http://YOUR-IP:8501` with friends

### Permanent Share (Streamlit Cloud - Free!)
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy your repo
4. Share your public URL!

## 🎯 What You'll See

**Stats Bar**:
- Total stocks monitored
- How many are near their 150-day MA
- How many above/below

**Main Table**:
- Symbol, Price, 150-day MA
- Distance from MA (% and absolute)
- Direction (ABOVE/BELOW)
- 🔔 Alert indicator (within 5%)

**Filters**:
- Show only stocks near MA
- Filter by direction
- Combine both filters

## ⚡ Pro Tips

1. **First load is slow** (3-5 min) - loading 500+ stocks
   - Data is cached for 1 hour after that
   - Click "Rerun" to refresh

2. **Sort by "Distance (abs)"** to see stocks closest to MA first

3. **Enable "Show only near MA"** to focus on opportunities

4. **Download CSV** for offline analysis in Excel/Google Sheets

5. **Deploy to Streamlit Cloud** for 24/7 access from anywhere

## 🆘 Need Help?

See the main [README.md](README.md) for detailed documentation and troubleshooting.

## 🎨 Customization

### Adding Your Favorite ETFs

The dashboard includes 20+ popular ETFs by default! To customize:

1. Open [streamlit_app.py](streamlit_app.py)
2. Find the `custom_etfs` list (around line 20)
3. Add or remove ETF ticker symbols

```python
custom_etfs = [
    'SPY', 'QQQ', 'VTI',  # Keep these
    'YOUR_FAVORITE_ETF',   # Add yours!
]
```

See [CUSTOMIZE_ETFS.md](CUSTOMIZE_ETFS.md) for a complete list of popular ETFs and examples!

### Monitor ONLY Your Favorites (No S&P 500)

Replace the `get_sp500_tickers()` function with:

```python
def get_sp500_tickers():
    return ['AAPL', 'MSFT', 'GOOGL', 'SPY', 'QQQ', 'VTI']
```

That's it! Enjoy tracking stocks! 📈
