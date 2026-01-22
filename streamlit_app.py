"""Streamlit dashboard for S&P 500 stock monitoring."""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import time
import requests

# Page config
st.set_page_config(
    page_title="Stock MA Monitor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_sp500_tickers():
    """Fetch S&P 500 ticker list from Wikipedia and add custom ETFs."""

    # ========================================
    # ADD YOUR FAVORITE ETFs HERE!
    # ========================================
    custom_etfs = [
        # Popular Market ETFs
        'SPY',   # S&P 500
        'QQQ',   # Nasdaq-100
        # 'DIA',   # Dow Jones
        # 'IWM',   # Russell 2000
        # 'VTI',   # Total Stock Market
        # 'VOO',   # Vanguard S&P 500

        # # Sector ETFs
        # 'XLF',   # Financials
        # 'XLK',   # Technology
        # 'XLE',   # Energy
        # 'XLV',   # Healthcare
        # 'XLI',   # Industrials
        # 'XLY',   # Consumer Discretionary
        # 'XLP',   # Consumer Staples

        # # International
        # 'VEA',   # Developed Markets
        # 'VWO',   # Emerging Markets
        # 'EFA',   # EAFE

        # # Bond ETFs
        # 'AGG',   # US Aggregate Bonds
        # 'BND',   # Total Bond Market
        # 'TLT',   # 20+ Year Treasury

        # Other
        'GLD',   # Gold
        'SLV',   # Silver
        'NLR',   # Nuclear Energy (your pick!)
    ]

    # ========================================
    # ADD YOUR FAVORITE STOCKS HERE!
    # ========================================

    custom_stocks = [
        'TSLA',  # Tesla
        'AAPL',  # Apple
        'AMZN',  # Amazon
        'MSFT',  # Microsoft
        'PLTR',  # Palantir
        'NFLX',  # Netflix
        'CEG',   # Constellation Energy
        'VST',   # Vistra Corporation
    ]


    try:
        # Fetch S&P 500 stocks with User-Agent header to avoid 403 error
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers)
        tables = pd.read_html(response.text)
        sp500_table = tables[0]
        tickers = sp500_table['Symbol'].tolist()
        # Clean up tickers
        tickers = [ticker.replace('.', '-') for ticker in tickers]

        # Add custom ETFs and stocks to the list
        all_tickers = tickers + custom_etfs + custom_stocks

        return all_tickers
    except Exception as e:
        st.error(f"Error fetching S&P 500 list: {e}")
        # If S&P 500 fetch fails, return just the ETFs and custom list
        return custom_etfs + custom_stocks

def get_stock_ma_data(symbol, ma_period=150):
    """
    Get stock data and calculate distance from moving average.

    Returns:
        dict with stock info or None if error
    """
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=f"{ma_period + 30}d")

        if len(hist) < ma_period:
            return None

        # Calculate MA
        ma = hist['Close'].rolling(window=ma_period).mean()
        current_price = hist['Close'].iloc[-1]
        current_ma = ma.iloc[-1]

        # Calculate distance
        diff_percent = ((current_price - current_ma) / current_ma * 100)
        distance_abs = abs(diff_percent)
        direction = "ABOVE" if current_price > current_ma else "BELOW"

        return {
            'Symbol': symbol,
            'Price': round(current_price, 2),
            '150-Day MA': round(current_ma, 2),
            'Distance (%)': round(diff_percent, 2),
            'Distance (abs)': round(distance_abs, 2),
            'Direction': direction,
            'Near MA (5%)': '🔔' if distance_abs <= 5.0 else ''
        }
    except Exception as e:
        return None

def load_all_stocks(tickers, progress_bar, status_text):
    """Load data for all stocks with progress tracking."""
    stocks_data = []
    total = len(tickers)

    for i, ticker in enumerate(tickers):
        status_text.text(f"Loading {ticker}... ({i+1}/{total})")
        progress_bar.progress((i + 1) / total)

        data = get_stock_ma_data(ticker)
        if data:
            stocks_data.append(data)

        # Small delay to avoid rate limiting
        if (i + 1) % 50 == 0:
            time.sleep(1)

    status_text.text("Done!")
    return pd.DataFrame(stocks_data)

def color_direction(val):
    """Color code the direction column."""
    if val == 'ABOVE':
        return 'background-color: #ffebee; color: #c62828'
    elif val == 'BELOW':
        return 'background-color: #e8f5e9; color: #2e7d32'
    return ''

def color_near_ma(val):
    """Highlight stocks near MA."""
    if val == '🔔':
        return 'background-color: #fff9c4; font-weight: bold'
    return ''

def main():
    st.title("📈 S&P 500 + ETFs - 150-Day MA Monitor")
    st.markdown("Monitor S&P 500 stocks and popular ETFs - see their distance from 150-day moving average")

    # Sidebar controls
    with st.sidebar:
        st.header("Add Custom Stocks")
        custom_tickers_input = st.text_input(
            "Enter ticker symbols (comma-separated)",
            placeholder="e.g., NVDA, AMD, GOOGL",
            help="Add your own stocks to monitor. Separate multiple tickers with commas."
        )

        st.markdown("---")
        st.header("Filters")
        show_near_only = st.checkbox("Show only stocks near MA (±5%)", value=False)
        direction_filter = st.selectbox(
            "Filter by direction",
            options=["All", "ABOVE", "BELOW"]
        )

        st.markdown("---")
        st.markdown("### About")
        st.markdown("🔔 = Within 5% of 150-day MA")
        st.markdown("**Click column headers to sort**")

    # Get tickers
    tickers = get_sp500_tickers()

    if not tickers:
        st.error("Failed to load tickers")
        return

    # Add user-specified custom tickers from sidebar
    if custom_tickers_input:
        user_tickers = [ticker.strip().upper() for ticker in custom_tickers_input.split(',') if ticker.strip()]
        # Add only unique tickers not already in the list
        for ticker in user_tickers:
            if ticker not in tickers:
                tickers.append(ticker)
        if user_tickers:
            st.info(f"➕ Added {len(user_tickers)} custom ticker(s): {', '.join(user_tickers)}")

    st.info(f"📊 Loading data for {len(tickers)} stocks & ETFs...")

    # Load data with progress
    progress_bar = st.progress(0)
    status_text = st.empty()

    df = load_all_stocks(tickers, progress_bar, status_text)

    # Clear progress indicators
    progress_bar.empty()
    status_text.empty()

    if df.empty:
        st.error("No data loaded")
        return

    # Apply filters
    filtered_df = df.copy()

    if show_near_only:
        filtered_df = filtered_df[filtered_df['Distance (abs)'] <= 5.0]

    if direction_filter != "All":
        filtered_df = filtered_df[filtered_df['Direction'] == direction_filter]

    # Stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Tickers", len(df))

    with col2:
        near_ma = len(df[df['Distance (abs)'] <= 5.0])
        st.metric("Near MA (±5%)", near_ma)

    with col3:
        above = len(df[df['Direction'] == 'ABOVE'])
        st.metric("Above MA", above)

    with col4:
        below = len(df[df['Direction'] == 'BELOW'])
        st.metric("Below MA", below)

    st.markdown("---")

    # Display filtered count
    if show_near_only or direction_filter != "All":
        st.info(f"Showing {len(filtered_df)} of {len(df)} tickers")

    # Display table
    st.dataframe(
        filtered_df.style
            .applymap(color_direction, subset=['Direction'])
            .applymap(color_near_ma, subset=['Near MA (5%)']),
        use_container_width=True,
        height=600
    )

    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"stocks_etfs_ma_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

    # Last update time
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption("Data refreshes every hour (cached)")

if __name__ == "__main__":
    main()
