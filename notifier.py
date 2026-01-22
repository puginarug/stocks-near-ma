"""Notification handler for stock alerts (WhatsApp)."""

import logging
from datetime import datetime, timedelta
import requests
import urllib.parse


class AlertNotifier:
    """Handles WhatsApp notifications and alert logging."""

    def __init__(self, cooldown_minutes=60, whatsapp_phone=None, whatsapp_api_key=None):
        """
        Initialize the notifier.

        Args:
            cooldown_minutes: Minutes to wait before re-alerting for the same condition
            whatsapp_phone: Phone number with country code (e.g., +1234567890)
            whatsapp_api_key: CallMeBot API key
        """
        self.cooldown_minutes = cooldown_minutes
        self.last_alerts = {}  # Track last alert time for each alert
        self.whatsapp_phone = whatsapp_phone
        self.whatsapp_api_key = whatsapp_api_key

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('alerts.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def should_alert(self, alert_key):
        """
        Check if enough time has passed since last alert.

        Args:
            alert_key: Unique identifier for the alert (e.g., "AAPL_near_ma")

        Returns:
            bool: True if alert should be sent
        """
        now = datetime.now()

        if alert_key not in self.last_alerts:
            return True

        last_alert_time = self.last_alerts[alert_key]
        time_diff = now - last_alert_time

        return time_diff >= timedelta(minutes=self.cooldown_minutes)

    def send_alert(self, title, message, alert_key):
        """
        Send a WhatsApp notification and log the alert.

        Args:
            title: Notification title
            message: Notification message
            alert_key: Unique identifier for the alert
        """
        if not self.should_alert(alert_key):
            self.logger.debug(f"Skipping alert {alert_key} (cooldown active)")
            return

        # Send WhatsApp notification via CallMeBot
        if self.whatsapp_phone and self.whatsapp_api_key:
            try:
                full_message = f"*{title}*\n{message}"
                encoded_message = urllib.parse.quote(full_message)
                url = f"https://api.callmebot.com/whatsapp.php?phone={self.whatsapp_phone}&text={encoded_message}&apikey={self.whatsapp_api_key}"

                response = requests.get(url)
                if response.status_code == 200:
                    self.logger.info(f"WHATSAPP ALERT SENT: {title} - {message}")
                else:
                    self.logger.error(f"Failed to send WhatsApp: Status {response.status_code}")
            except Exception as e:
                self.logger.error(f"Failed to send WhatsApp notification: {e}")
        else:
            self.logger.warning("WhatsApp credentials not configured. Alert logged only.")
            self.logger.info(f"ALERT: {title} - {message}")

        # Update last alert time
        self.last_alerts[alert_key] = datetime.now()

    def log_info(self, message):
        """Log informational message."""
        self.logger.info(message)

    def log_error(self, message):
        """Log error message."""
        self.logger.error(message)
