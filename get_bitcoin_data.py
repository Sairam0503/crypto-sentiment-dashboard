import requests
import pandas as pd
import time
import sqlite3
from datetime import datetime, timedelta
import pytz

def fetch_bitcoin_data(start_date, end_date):
    """
    Fetch Bitcoin price and volume data from CryptoCompare API for each day in the specified date range.
    Returns a list of dictionaries with timestamp, price, and volume.
    """
    data_list = []
    session = requests.Session()

    # CryptoCompare API endpoint for historical daily data
    fsym = "BTC"
    tsym = "USD"
    limit = 2000  # Maximum number of data points per request

    # Convert dates to timestamps
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    # CryptoCompare API requires the 'toTs' parameter (end timestamp)
    url = f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={fsym}&tsym={tsym}&limit={limit}&toTs={end_timestamp}"

    try:
        response = session.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CryptoCompare: {e}")
        return data_list

    # Check if the response contains data
    if data["Response"] != "Success" or not data["Data"]["Data"]:
        print("No data returned from CryptoCompare. Check the symbol or date range.")
        return data_list

    # Extract daily data
    for entry in data["Data"]["Data"]:
        timestamp = entry["time"]  # Timestamp in seconds
        close_price = entry["close"]  # Closing price
        volume = entry["volumeto"]  # Volume (in USD)

        # Only include data within the requested date range
        if start_timestamp <= timestamp <= end_timestamp:
            data_list.append({
                "timestamp": timestamp,
                "price": close_price,
                "volume": volume
            })

    return data_list

def main():
    # Define the date range (last 30 days from today)
    end_date = datetime.now(pytz.UTC).replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=30)  # 30 days before today

    # Fetch data from CryptoCompare
    print(f"Fetching Bitcoin data from {start_date} to {end_date}...")
    data_list = fetch_bitcoin_data(start_date, end_date)

    # Check if we collected any data
    if not data_list:
        print("No valid data collected. Please check the API or date range.")
        return

    # Convert list to a DataFrame for easy handling
    df = pd.DataFrame(data_list)

    # Sort by timestamp to ensure chronological order
    df = df.sort_values("timestamp")

    # Display collected data
    print("Collected data:")
    print(df)

    # Save to CSV
    try:
        df.to_csv('bitcoin_prices.csv', index=False)
        print("Data saved to bitcoin_prices.csv")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

    # Save to SQLite database (replace existing data)
    try:
        conn = sqlite3.connect('crypto_data.db')
        df.to_sql('bitcoin_prices', conn, if_exists='replace', index=False)
        conn.close()
        print("Data saved to SQLite database (crypto_data.db)")
    except sqlite3.Error as e:
        print(f"Error saving to SQLite: {e}")

if __name__ == "__main__":
    main()