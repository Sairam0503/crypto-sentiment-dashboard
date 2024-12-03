import requests
import pandas as pd
import time
import sqlite3
from datetime import datetime, timedelta

# Finnhub API key for authentication
api_key = 'cvhhqcpr01qgkck3vkl0cvhhqcpr01qgkck3vklg'

# URL to fetch Bitcoin price data (BTC/USDT) from Finnhub
url = f'https://finnhub.io/api/v1/quote?symbol=BINANCE:BTCUSDT&token={api_key}'

# List to store collected data
data_list = []

# Simulate collecting 1 data point per day for 30 days (Nov 3, 2024 to Dec 2, 2024)
start_date = datetime(2024, 11, 3)  # Start date: November 3, 2024
for i in range(30):
    try:
        # Send request to API and retrieve data
        response = requests.get(url)
        data = response.json()

        # Check if the response contains an error
        if 'error' in data:
            print(f"Error from API: {data['error']}")
            break

        # Extract current price
        price = data.get('c', 0)  # Current price, default to 0 if missing

        # Calculate the timestamp for the current day
        simulated_date = start_date + timedelta(days=i)
        timestamp = int(simulated_date.timestamp())

        # Only add data if price is valid (not 0)
        if price == 0:
            print("Invalid price received (price is 0), skipping...")
            break

        # Append data to the list
        data_list.append({'timestamp': timestamp, 'price': price})

        # Display progress
        print(f"Collected price: {price} at timestamp: {timestamp} (date: {simulated_date})")

        # Wait 10 seconds for testing (in production, this would be 24 hours/86400 seconds)
        time.sleep(10)

    except Exception as e:
        # Handle any unexpected errors
        print(f"An error occurred: {e}")
        break

# Check if we collected any data
if not data_list:
    print("No valid data collected. Please check the API or symbol.")
else:
    # Convert list to a DataFrame for easy handling
    df = pd.DataFrame(data_list)

    # Save to CSV
    df.to_csv('bitcoin_prices.csv', index=False)
    print("Data saved to bitcoin_prices.csv")

    # Save to SQLite database (replace existing data)
    conn = sqlite3.connect('crypto_data.db')
    df.to_sql('bitcoin_prices', conn, if_exists='replace', index=False)
    conn.close()
    print("Data saved to SQLite database (crypto_data.db)")