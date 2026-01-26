"""Pydantic models for stock data."""

from pydantic import BaseModel
from typing import List


class StockData(BaseModel):
    """Model for individual stock data."""
    symbol: str
    price: float
    ma_150: float
    distance_percent: float
    distance_abs: float
    direction: str  # "ABOVE" or "BELOW"
    near_ma: bool   # True if within 5% of MA


class StockResponse(BaseModel):
    """Model for stock API response."""
    stocks: List[StockData]
    total_count: int
    processing_time: float
    cache_hit: bool = False


class Statistics(BaseModel):
    """Model for statistics response."""
    total_tickers: int
    near_ma_count: int
    above_count: int
    below_count: int


class TickersResponse(BaseModel):
    """Model for tickers list response."""
    tickers: List[str]
    count: int
