"""
Fetch stock data using parallel processing and upload to JSONBin.io
This script is designed to run in GitHub Actions on a schedule.
"""

import os
import sys
import time
import json
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import yfinance as yf
import pandas as pd


# Pydantic-like data class (simplified for standalone script)
class StockData:
    def __init__(self, symbol, price, ma_150, distance_percent, distance_abs, direction, near_ma):
        self.symbol = symbol
        self.price = price
        self.ma_150 = ma_150
        self.distance_percent = distance_percent
        self.distance_abs = distance_abs
        self.direction = direction
        self.near_ma = near_ma

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'price': self.price,
            'ma_150': self.ma_150,
            'distance_percent': self.distance_percent,
            'distance_abs': self.distance_abs,
            'direction': self.direction,
            'near_ma': self.near_ma
        }


def get_sp500_tickers() -> List[str]:
    """Fetch S&P 500 ticker list from Wikipedia and add custom ETFs."""

    # Major ETFs to include
    custom_etfs = [
        'SPY', 'QQQ', 'DIA', 'IWM', 'VTI', 'VOO',  # Market indexes
        'XLF', 'XLK', 'XLE', 'XLV', 'XLI', 'XLY', 'XLP',  # Sectors
        'VEA', 'VWO', 'EFA',  # International
        'AGG', 'BND', 'TLT',  # Bonds
        'GLD', 'SLV', 'NLR',  # Commodities/Others
    ]

    # Popular individual stocks
    custom_stocks = [
        'TSLA', 'AAPL', 'AMZN', 'MSFT', 'GOOGL', 'META', 'NVDA',
        'PLTR', 'NFLX', 'CEG', 'VST', 'AMD', 'INTC'
    ]

    try:
        # Fetch S&P 500 stocks
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Use StringIO to avoid file path issues
        from io import StringIO
        tables = pd.read_html(StringIO(response.text))
        sp500_table = tables[0]
        tickers = sp500_table['Symbol'].tolist()

        # Clean up tickers
        tickers = [ticker.replace('.', '-') for ticker in tickers]

        # Combine all
        all_tickers = list(set(tickers + custom_etfs + custom_stocks))
        print(f"Fetched {len(all_tickers)} unique tickers")
        return all_tickers
    except Exception as e:
        print(f"Error fetching S&P 500 list: {type(e).__name__}")
        print(f"Falling back to custom ETFs and stocks only ({len(custom_etfs + custom_stocks)} tickers)")
        return custom_etfs + custom_stocks


def get_stock_ma_data(symbol: str, ma_period: int = 150) -> Optional[StockData]:
    """Get stock data and calculate distance from moving average."""
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
        near_ma = distance_abs <= 5.0

        return StockData(
            symbol=symbol,
            price=round(float(current_price), 2),
            ma_150=round(float(current_ma), 2),
            distance_percent=round(float(diff_percent), 2),
            distance_abs=round(float(distance_abs), 2),
            direction=direction,
            near_ma=bool(near_ma)
        )
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None


def fetch_stocks_parallel(tickers: List[str], max_workers: int = 10, batch_size: int = 50) -> List[dict]:
    """Fetch stock data in parallel using ThreadPoolExecutor."""
    stocks_data = []
    total_tickers = len(tickers)

    # Process in batches for rate limiting
    for batch_start in range(0, total_tickers, batch_size):
        batch_end = min(batch_start + batch_size, total_tickers)
        batch = tickers[batch_start:batch_end]

        print(f"Processing batch {batch_start//batch_size + 1}: "
              f"Tickers {batch_start+1}-{batch_end} of {total_tickers}")

        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_ticker = {
                executor.submit(get_stock_ma_data, ticker): ticker
                for ticker in batch
            }

            for future in as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    result = future.result()
                    if result:
                        stocks_data.append(result.to_dict())
                except Exception as e:
                    print(f"Error processing {ticker}: {e}")

        # Rate limiting: sleep 1 second after each batch
        if batch_end < total_tickers:
            print(f"Rate limiting: sleeping 1 second...")
            time.sleep(1)

    print(f"Successfully processed {len(stocks_data)} stocks out of {total_tickers}")
    return stocks_data


def upload_to_jsonbin(data: dict, api_key: str, bin_id: str):
    """Upload data to JSONBin.io."""
    url = f"https://api.jsonbin.io/v3/b/{bin_id}"
    headers = {
        'Content-Type': 'application/json',
        'X-Master-Key': api_key
    }

    try:
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        print(f"Successfully uploaded to JSONBin.io: {response.status_code}")
        return True
    except Exception as e:
        print(f"Error uploading to JSONBin.io: {e}")
        return False


def main():
    """Main execution function."""
    print("=" * 60)
    print("Stock Data Fetcher - GitHub Actions")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")

    # Get environment variables
    api_key = os.environ.get('JSONBIN_API_KEY')
    bin_id = os.environ.get('JSONBIN_BIN_ID')

    if not api_key or not bin_id:
        print("ERROR: JSONBIN_API_KEY or JSONBIN_BIN_ID not set")
        print("Please add these as GitHub Secrets")
        sys.exit(1)

    # Fetch tickers
    print("\nFetching ticker list...")
    tickers = get_sp500_tickers()

    # Fetch stock data with parallel processing
    print(f"\nFetching data for {len(tickers)} stocks with parallel processing...")
    start_time = time.time()
    stocks_data = fetch_stocks_parallel(tickers, max_workers=10, batch_size=50)
    processing_time = time.time() - start_time

    print(f"\nProcessing completed in {processing_time:.2f} seconds")
    print(f"Successfully fetched {len(stocks_data)} stocks")

    # Calculate statistics
    near_ma = sum(1 for s in stocks_data if s['near_ma'])
    above = sum(1 for s in stocks_data if s['direction'] == 'ABOVE')
    below = sum(1 for s in stocks_data if s['direction'] == 'BELOW')

    # Prepare data for upload
    upload_data = {
        'stocks': stocks_data,
        'metadata': {
            'total_count': len(stocks_data),
            'near_ma_count': near_ma,
            'above_count': above,
            'below_count': below,
            'processing_time': round(processing_time, 2),
            'last_updated': datetime.now().isoformat(),
            'version': '1.0.0'
        }
    }

    # Upload to JSONBin.io
    print("\nUploading to JSONBin.io...")
    success = upload_to_jsonbin(upload_data, api_key, bin_id)

    # Write summary file for GitHub Actions artifact
    summary = f"""Stock Data Update Summary
========================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
Total Stocks Processed: {len(stocks_data)}
Processing Time: {processing_time:.2f} seconds
Near MA (±5%): {near_ma}
Above MA: {above}
Below MA: {below}
Upload Status: {'SUCCESS' if success else 'FAILED'}
"""

    with open('stock_summary.txt', 'w') as f:
        f.write(summary)

    print("\n" + summary)
    print("=" * 60)

    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
