"""Parallel stock data processor using ThreadPoolExecutor."""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
from models.stock_models import StockData
from services.stock_service import get_stock_ma_data


class ParallelStockProcessor:
    """Process stock data in parallel using ThreadPoolExecutor."""

    def __init__(self, max_workers: int = 10, batch_size: int = 50):
        """
        Initialize parallel processor.

        Args:
            max_workers: Number of parallel workers (default: 10)
            batch_size: Number of stocks to process before rate limiting pause (default: 50)
        """
        self.max_workers = max_workers
        self.batch_size = batch_size

    def fetch_stocks_parallel(self, tickers: List[str]) -> List[StockData]:
        """
        Fetch stock data in parallel using ThreadPoolExecutor.

        Args:
            tickers: List of stock ticker symbols

        Returns:
            List of StockData objects (excludes failed fetches)
        """
        stocks_data = []
        total_tickers = len(tickers)

        # Process in batches for rate limiting
        for batch_start in range(0, total_tickers, self.batch_size):
            batch_end = min(batch_start + self.batch_size, total_tickers)
            batch = tickers[batch_start:batch_end]

            print(f"Processing batch {batch_start//self.batch_size + 1}: "
                  f"Tickers {batch_start+1}-{batch_end} of {total_tickers}")

            # Use ThreadPoolExecutor for parallel processing
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all tasks in the batch
                future_to_ticker = {
                    executor.submit(get_stock_ma_data, ticker): ticker
                    for ticker in batch
                }

                # Collect results as they complete
                for future in as_completed(future_to_ticker):
                    ticker = future_to_ticker[future]
                    try:
                        result = future.result()
                        if result:
                            stocks_data.append(result)
                    except Exception as e:
                        print(f"Error processing {ticker}: {e}")

            # Rate limiting: sleep 1 second after each batch
            if batch_end < total_tickers:
                print(f"Rate limiting: sleeping 1 second before next batch...")
                time.sleep(1)

        print(f"Completed processing {len(stocks_data)} stocks successfully "
              f"out of {total_tickers} total")
        return stocks_data

    def fetch_single_stock(self, symbol: str) -> StockData:
        """
        Fetch data for a single stock (wrapper for compatibility).

        Args:
            symbol: Stock ticker symbol

        Returns:
            StockData object or None
        """
        return get_stock_ma_data(symbol)
