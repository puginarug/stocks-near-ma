"""Stock data fetching and MA calculation service."""

import yfinance as yf
from typing import Optional
from models.stock_models import StockData


def get_stock_ma_data(symbol: str, ma_period: int = 150) -> Optional[StockData]:
    """
    Get stock data and calculate distance from moving average.

    Args:
        symbol: Stock ticker symbol
        ma_period: Moving average period (default: 150 days)

    Returns:
        StockData object or None if error
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
        near_ma = distance_abs <= 5.0

        return StockData(
            symbol=symbol,
            price=round(current_price, 2),
            ma_150=round(current_ma, 2),
            distance_percent=round(diff_percent, 2),
            distance_abs=round(distance_abs, 2),
            direction=direction,
            near_ma=near_ma
        )
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None
