# How to Customize Your ETF List

## Quick Guide

Open [streamlit_app.py](streamlit_app.py) and find the `custom_etfs` list (around line 20). It looks like this:

```python
custom_etfs = [
    # Popular Market ETFs
    'SPY',   # S&P 500
    'QQQ',   # Nasdaq-100
    'DIA',   # Dow Jones
    'IWM',   # Russell 2000
    'VTI',   # Total Stock Market
    'VOO',   # Vanguard S&P 500

    # ... more ETFs
]
```

## To Add Your Favorite ETFs

Simply add the ticker symbol to the list:

```python
custom_etfs = [
    'SPY',
    'QQQ',
    'YOUR_ETF_HERE',  # Add your ETF
    'ANOTHER_ONE',     # Add another
]
```

## To Remove ETFs

Delete or comment out lines you don't want:

```python
custom_etfs = [
    'SPY',
    # 'QQQ',  # Commented out - won't show up
    'VTI',
]
```

## Popular ETF Categories

### Broad Market
- **SPY** - S&P 500
- **QQQ** - Nasdaq-100 (Tech-heavy)
- **DIA** - Dow Jones Industrial Average
- **IWM** - Russell 2000 (Small-cap)
- **VTI** - Total US Stock Market
- **VOO** - Vanguard S&P 500

### Sector ETFs (SPDR Sectors)
- **XLK** - Technology
- **XLF** - Financials
- **XLE** - Energy
- **XLV** - Healthcare
- **XLI** - Industrials
- **XLY** - Consumer Discretionary
- **XLP** - Consumer Staples
- **XLU** - Utilities
- **XLRE** - Real Estate
- **XLB** - Materials
- **XLC** - Communication Services

### International
- **VEA** - Developed Markets (ex-US)
- **VWO** - Emerging Markets
- **EFA** - EAFE (Europe, Asia, Far East)
- **EEM** - Emerging Markets
- **FXI** - China Large-Cap
- **EWJ** - Japan

### Bonds
- **AGG** - US Aggregate Bonds
- **BND** - Total Bond Market
- **TLT** - 20+ Year Treasury Bonds
- **SHY** - 1-3 Year Treasury Bonds
- **LQD** - Investment Grade Corporate Bonds
- **HYG** - High Yield Corporate Bonds

### Commodities & Alternative
- **GLD** - Gold
- **SLV** - Silver
- **USO** - Crude Oil
- **UNG** - Natural Gas
- **DBC** - Commodities

### Thematic & Specialized
- **ARKK** - ARK Innovation (Disruptive Tech)
- **ICLN** - Clean Energy
- **TAN** - Solar Energy
- **NLR** - Nuclear Energy
- **XBI** - Biotech
- **SOXX** - Semiconductors
- **FINX** - Fintech
- **HACK** - Cybersecurity
- **UFO** - Space & Defense

### Dividend Focused
- **VYM** - High Dividend Yield
- **SCHD** - Dividend Appreciation
- **DGRO** - Dividend Growth
- **DVY** - Dividend Select

### Volatility & Inverse
- **VXX** - VIX Short-Term Futures
- **SVXY** - Short VIX
- **SH** - Inverse S&P 500
- **PSQ** - Inverse Nasdaq-100

## Example Configurations

### Conservative Portfolio Tracker
```python
custom_etfs = [
    'SPY', 'AGG', 'GLD',  # Stocks, Bonds, Gold
    'VYM', 'SCHD',         # Dividend ETFs
]
```

### Tech-Focused Tracker
```python
custom_etfs = [
    'QQQ', 'XLK', 'SOXX',  # Tech sectors
    'ARKK', 'FINX', 'HACK', # Thematic tech
]
```

### All Sectors Tracker
```python
custom_etfs = [
    'SPY',  # Overall market
    'XLK', 'XLF', 'XLE', 'XLV', 'XLI',  # Sectors
    'XLY', 'XLP', 'XLU', 'XLRE', 'XLB', 'XLC',
]
```

### International Focus
```python
custom_etfs = [
    'VEA', 'VWO', 'EFA', 'EEM',  # Broad international
    'FXI', 'EWJ', 'EWG', 'EWU',  # Country-specific
]
```

## To Monitor ONLY ETFs (No S&P 500 Stocks)

Replace the entire `get_sp500_tickers()` function with:

```python
@st.cache_data(ttl=3600)
def get_sp500_tickers():
    """Return only custom ETFs."""
    return [
        'SPY', 'QQQ', 'DIA', 'IWM',
        'XLK', 'XLF', 'XLE', 'XLV',
        # Add your favorites here
    ]
```

## After Making Changes

1. Save the file
2. Refresh your browser (or click "Rerun" in Streamlit)
3. The dashboard will reload with your new list!

## Tips

- The more tickers you add, the longer initial load time
- Keep it under ~50 tickers for best performance
- ETFs work exactly like stocks in the dashboard
- All sorting and filtering features work the same

## Need Help?

Check the main [README.md](README.md) for more information!
