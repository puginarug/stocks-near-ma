"""FastAPI application for stock MA monitoring."""

import time
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from models.stock_models import StockResponse, Statistics, TickersResponse
from services.parallel_processor import ParallelStockProcessor
from utils.sp500_fetcher import get_sp500_tickers
from utils.cache import stock_cache


app = FastAPI(
    title="Stock MA Monitor API",
    description="API for monitoring stocks and their distance from 150-day moving average",
    version="1.0.0"
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize parallel processor
processor = ParallelStockProcessor(max_workers=10, batch_size=50)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Stock MA Monitor API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "version": "1.0.0",
        "timestamp": time.time()
    }


@app.get("/api/sp500-tickers", response_model=TickersResponse)
async def get_tickers():
    """Get S&P 500 ticker list plus custom ETFs and stocks."""
    # Check cache first
    cache_key = "sp500_tickers"
    cached_tickers = stock_cache.get(cache_key)

    if cached_tickers:
        return TickersResponse(
            tickers=cached_tickers,
            count=len(cached_tickers)
        )

    # Fetch fresh data
    tickers = get_sp500_tickers()

    # Cache the result
    stock_cache.set(cache_key, tickers)

    return TickersResponse(
        tickers=tickers,
        count=len(tickers)
    )


@app.get("/api/stocks", response_model=StockResponse)
async def get_stocks(
    include_custom: Optional[str] = Query(None, description="Comma-separated custom tickers to include")
):
    """
    Get stock data with 150-day MA calculations.

    Args:
        include_custom: Optional comma-separated list of custom tickers (e.g., "NVDA,AMD,GOOGL")

    Returns:
        StockResponse with all stock data
    """
    # Build cache key
    cache_key = f"stocks_{include_custom or 'default'}"

    # Check cache first
    cached_data = stock_cache.get(cache_key)
    if cached_data:
        return StockResponse(
            stocks=cached_data,
            total_count=len(cached_data),
            processing_time=0.0,
            cache_hit=True
        )

    # Get base ticker list
    tickers = get_sp500_tickers()

    # Add custom tickers if provided
    if include_custom:
        custom_tickers = [t.strip().upper() for t in include_custom.split(',') if t.strip()]
        for ticker in custom_tickers:
            if ticker not in tickers:
                tickers.append(ticker)

    # Fetch stock data in parallel
    start_time = time.time()
    stocks_data = processor.fetch_stocks_parallel(tickers)
    processing_time = time.time() - start_time

    # Cache the result
    stock_cache.set(cache_key, stocks_data)

    return StockResponse(
        stocks=stocks_data,
        total_count=len(stocks_data),
        processing_time=round(processing_time, 2),
        cache_hit=False
    )


@app.get("/api/statistics", response_model=Statistics)
async def get_statistics(
    tickers: Optional[str] = Query(None, description="Comma-separated tickers to analyze")
):
    """
    Get statistics for stocks.

    Args:
        tickers: Optional comma-separated list of tickers to analyze

    Returns:
        Statistics including total, near MA, above, and below counts
    """
    # If no specific tickers provided, use cached stock data
    if not tickers:
        cache_key = "stocks_default"
        cached_data = stock_cache.get(cache_key)

        if not cached_data:
            # No cached data, fetch it
            stocks_data = processor.fetch_stocks_parallel(get_sp500_tickers())
            stock_cache.set(cache_key, stocks_data)
        else:
            stocks_data = cached_data
    else:
        # Fetch specific tickers
        ticker_list = [t.strip().upper() for t in tickers.split(',') if t.strip()]
        stocks_data = processor.fetch_stocks_parallel(ticker_list)

    # Calculate statistics
    total_tickers = len(stocks_data)
    near_ma_count = sum(1 for s in stocks_data if s.near_ma)
    above_count = sum(1 for s in stocks_data if s.direction == "ABOVE")
    below_count = sum(1 for s in stocks_data if s.direction == "BELOW")

    return Statistics(
        total_tickers=total_tickers,
        near_ma_count=near_ma_count,
        above_count=above_count,
        below_count=below_count
    )


@app.post("/api/cache/clear")
async def clear_cache():
    """Clear all cached data."""
    stock_cache.clear()
    return {"message": "Cache cleared successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
