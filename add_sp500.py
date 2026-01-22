"""Helper script to add all S&P 500 stocks to config.yaml"""

import yaml
import pandas as pd

def get_sp500_tickers():
    """Fetch S&P 500 ticker list from Wikipedia."""
    try:
        # Get S&P 500 list from Wikipedia
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        tables = pd.read_html(url)
        sp500_table = tables[0]

        # Extract ticker symbols
        tickers = sp500_table['Symbol'].tolist()

        # Clean up tickers (some have special characters)
        tickers = [ticker.replace('.', '-') for ticker in tickers]

        return tickers
    except Exception as e:
        print(f"Error fetching S&P 500 list: {e}")
        return []

def generate_config_entries(tickers, ma_period=150, threshold=5.0):
    """Generate alert entries for all tickers."""
    alerts = []

    for ticker in tickers:
        alert = {
            'name': f"{ticker} near {ma_period}-day MA",
            'symbol': ticker,
            'condition': 'near_ma',
            'params': {
                'ma_period': ma_period,
                'threshold_percent': threshold
            },
            'enabled': True
        }
        alerts.append(alert)

    return alerts

def update_config(alerts, backup=True):
    """Update config.yaml with new alerts."""
    config_file = 'config.yaml'

    try:
        # Read existing config
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        # Backup existing config
        if backup:
            with open('config.yaml.backup', 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            print("✓ Backed up existing config to config.yaml.backup")

        # Replace alerts
        config['alerts'] = alerts

        # Write updated config
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        print(f"✓ Updated config.yaml with {len(alerts)} S&P 500 stocks")

    except Exception as e:
        print(f"Error updating config: {e}")

def main():
    print("Fetching S&P 500 stock list...")
    tickers = get_sp500_tickers()

    if not tickers:
        print("Failed to fetch S&P 500 tickers")
        return

    print(f"Found {len(tickers)} S&P 500 stocks")

    # Ask for confirmation
    print("\n⚠️  WARNING:")
    print("- This will replace ALL existing alerts in config.yaml")
    print("- Monitoring 500+ stocks may hit Yahoo Finance rate limits")
    print("- Consider increasing check_interval to 30-60 minutes")
    print("- Your current config will be backed up to config.yaml.backup")

    response = input("\nContinue? (yes/no): ").strip().lower()

    if response == 'yes':
        print("\nGenerating config entries...")
        alerts = generate_config_entries(tickers)

        print("Updating config.yaml...")
        update_config(alerts)

        print("\n✓ Done! Don't forget to:")
        print("  1. Increase check_interval in config.yaml (suggest 30-60 minutes)")
        print("  2. Configure WhatsApp credentials if not already done")
        print("  3. Run: python main.py")
    else:
        print("Cancelled")

if __name__ == '__main__':
    main()
