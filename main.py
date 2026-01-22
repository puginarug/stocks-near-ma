"""Stock Alert System - Monitor S&P 500 stocks and send alerts."""

import time
import yaml
import yfinance as yf
import json
from datetime import datetime
from notifier import AlertNotifier

# Configure yfinance to use browser-like headers to avoid blocking
yf.set_tz_cache_location("custom_cache")  # Optional: helps with timezone caching


class StockMonitor:
    """Monitor stocks and trigger alerts based on configured conditions."""

    def __init__(self, config_file='config.yaml'):
        """
        Initialize the stock monitor.

        Args:
            config_file: Path to YAML configuration file
        """
        self.config = self.load_config(config_file)
        whatsapp_config = self.config.get('whatsapp', {})
        self.notifier = AlertNotifier(
            cooldown_minutes=self.config.get('alert_cooldown', 60),
            whatsapp_phone=whatsapp_config.get('phone'),
            whatsapp_api_key=whatsapp_config.get('api_key')
        )
        self.stocks_data = []  # Store data for web display

    def load_config(self, config_file):
        """Load configuration from YAML file."""
        try:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            raise

    def check_near_ma(self, stock_data, params):
        """
        Check if current price is near moving average.

        Args:
            stock_data: yfinance Ticker object
            params: Dict with 'ma_period' and 'threshold_percent'

        Returns:
            tuple: (bool: condition_met, str: message)
        """
        ma_period = params.get('ma_period', 150)
        threshold_percent = params.get('threshold_percent', 5.0)

        # Get historical data
        hist = stock_data.history(period=f"{ma_period + 30}d")

        if len(hist) < ma_period:
            return False, f"Insufficient data (need {ma_period} days)"

        # Calculate moving average
        ma = hist['Close'].rolling(window=ma_period).mean()
        current_price = hist['Close'].iloc[-1]
        current_ma = ma.iloc[-1]

        # Check if price is within threshold of MA
        diff_percent = abs((current_price - current_ma) / current_ma * 100)

        if diff_percent <= threshold_percent:
            # Determine if approaching from above or below
            direction = "from ABOVE" if current_price > current_ma else "from BELOW"

            return True, (
                f"Price ${current_price:.2f} is {diff_percent:.2f}% "
                f"from {ma_period}-day MA (${current_ma:.2f}) - approaching {direction}"
            )

        return False, None

    def check_above(self, stock_data, params):
        """
        Check if current price is above threshold.

        Args:
            stock_data: yfinance Ticker object
            params: Dict with 'price'

        Returns:
            tuple: (bool: condition_met, str: message)
        """
        threshold = params.get('price')
        hist = stock_data.history(period='1d')

        if hist.empty:
            return False, "No data available"

        current_price = hist['Close'].iloc[-1]

        if current_price > threshold:
            return True, f"Price ${current_price:.2f} is above ${threshold:.2f}"

        return False, None

    def check_below(self, stock_data, params):
        """
        Check if current price is below threshold.

        Args:
            stock_data: yfinance Ticker object
            params: Dict with 'price'

        Returns:
            tuple: (bool: condition_met, str: message)
        """
        threshold = params.get('price')
        hist = stock_data.history(period='1d')

        if hist.empty:
            return False, "No data available"

        current_price = hist['Close'].iloc[-1]

        if current_price < threshold:
            return True, f"Price ${current_price:.2f} is below ${threshold:.2f}"

        return False, None

    def check_percent_change(self, stock_data, params):
        """
        Check if daily percent change exceeds threshold.

        Args:
            stock_data: yfinance Ticker object
            params: Dict with 'threshold_percent'

        Returns:
            tuple: (bool: condition_met, str: message)
        """
        threshold = params.get('threshold_percent', 5.0)
        hist = stock_data.history(period='5d')

        if len(hist) < 2:
            return False, "Insufficient data"

        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2]

        change_percent = abs((current_price - prev_price) / prev_price * 100)

        if change_percent > threshold:
            direction = "up" if current_price > prev_price else "down"
            return True, (
                f"Price changed {change_percent:.2f}% {direction} "
                f"(${prev_price:.2f} → ${current_price:.2f})"
            )

        return False, None

    def check_alert(self, alert_config):
        """
        Check a single alert condition and collect data for web display.

        Args:
            alert_config: Dict with alert configuration

        Returns:
            dict: Stock data for web display
        """
        if not alert_config.get('enabled', True):
            return None

        name = alert_config.get('name', 'Unknown')
        symbol = alert_config.get('symbol')
        condition = alert_config.get('condition')
        params = alert_config.get('params', {})

        stock_info = {
            'symbol': symbol,
            'name': name,
            'alert_triggered': False,
            'message': None,
            'current_price': 0,
            'ma_value': 0,
            'distance_percent': 0,
            'direction': None
        }

        try:
            # Fetch stock data with retry logic
            stock = yf.Ticker(symbol)

            # Test if we can get data - this will trigger the actual API call
            test_data = stock.history(period='1d')
            if test_data.empty:
                self.notifier.log_error(f"No data available for {symbol}")
                return stock_info

            # Check condition
            condition_met = False
            message = None

            if condition == 'near_ma':
                condition_met, message = self.check_near_ma(stock, params)

                # Get detailed data for web display
                ma_period = params.get('ma_period', 150)
                hist = stock.history(period=f"{ma_period + 30}d")
                if len(hist) >= ma_period:
                    ma = hist['Close'].rolling(window=ma_period).mean()
                    current_price = hist['Close'].iloc[-1]
                    current_ma = ma.iloc[-1]
                    diff_percent = abs((current_price - current_ma) / current_ma * 100)
                    direction = "ABOVE" if current_price > current_ma else "BELOW"

                    stock_info.update({
                        'current_price': float(current_price),
                        'ma_value': float(current_ma),
                        'distance_percent': float(diff_percent),
                        'direction': direction,
                        'alert_triggered': condition_met,
                        'message': message
                    })

            elif condition == 'above':
                condition_met, message = self.check_above(stock, params)
            elif condition == 'below':
                condition_met, message = self.check_below(stock, params)
            elif condition == 'percent_change':
                condition_met, message = self.check_percent_change(stock, params)
            else:
                self.notifier.log_error(f"Unknown condition: {condition}")
                return stock_info

            # Send alert if condition is met
            if condition_met:
                alert_key = f"{symbol}_{condition}"
                self.notifier.send_alert(
                    title=f"Stock Alert: {symbol}",
                    message=f"{name}\n{message}",
                    alert_key=alert_key
                )

        except Exception as e:
            self.notifier.log_error(f"Error checking {symbol}: {e}")

        return stock_info

    def save_web_data(self):
        """Save stock data to JSON file for web display."""
        try:
            data = {
                'stocks': self.stocks_data,
                'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            with open('alerts_data.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.notifier.log_error(f"Error saving web data: {e}")

    def run(self):
        """Main monitoring loop."""
        check_interval = self.config.get('check_interval', 5) * 60  # Convert to seconds
        alerts = self.config.get('alerts', [])

        if not alerts:
            print("No alerts configured!")
            return

        self.notifier.log_info(f"Stock Alert System started. Monitoring {len(alerts)} alerts.")
        self.notifier.log_info(f"Check interval: {check_interval // 60} minutes")

        try:
            while True:
                self.notifier.log_info("Checking alerts...")
                self.stocks_data = []  # Reset data for this check

                for alert in alerts:
                    stock_info = self.check_alert(alert)
                    if stock_info:
                        self.stocks_data.append(stock_info)

                # Save data for web display
                self.save_web_data()

                self.notifier.log_info(f"Check complete. Sleeping for {check_interval // 60} minutes.")
                time.sleep(check_interval)

        except KeyboardInterrupt:
            self.notifier.log_info("Stock Alert System stopped by user.")


if __name__ == '__main__':
    monitor = StockMonitor()
    monitor.run()
