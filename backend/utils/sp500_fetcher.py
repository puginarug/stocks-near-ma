"""Fetch S&P 500 ticker list from Wikipedia."""

import pandas as pd
import requests
from typing import List


def get_sp500_tickers() -> List[str]:
    """Fetch S&P 500 ticker list from Wikipedia and add custom ETFs and stocks."""

    # Custom ETFs to monitor
    custom_etfs = [
        'SPY',   # S&P 500
        'QQQ',   # Nasdaq-100
        'GLD',   # Gold
        'SLV',   # Silver
        'NLR',   # Nuclear Energy
    ]

    # Custom stocks to monitor
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

        # Clean up tickers (replace . with -)
        tickers = [ticker.replace('.', '-') for ticker in tickers]

        # Add custom ETFs and stocks to the list
        all_tickers = tickers + custom_etfs + custom_stocks

        return all_tickers
    except Exception as e:
        print(f"Error fetching S&P 500 list: {e}")
        # If S&P 500 fetch fails, return just the ETFs and custom stocks
        return custom_etfs + custom_stocks
