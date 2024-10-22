import requests
import pandas as pd
import time

# Finnhub API key for authentication
api_key = 'cvg5uopr01qgvsqno7e0cvg5uopr01qgvsqno7eg'

# URL to fetch Bitcoin price data (BTC/USDT) from Finnhub
url = f'https://finnhub.io/api/v1/quote?symbol=BINANCE:BTCUSDT&token={api_key}'

# List to store collected data
data_list = []

# Collect data 5 times, with a 10-second pause between each request
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

        # Use the current system time as the timestamp
        timestamp = int(time.time())  # Current time in seconds

        # Only add data if price is valid (not 0)
        if price == 0:
            print("Invalid price received (price is 0), skipping...")
            break

        # Append data to the list
        data_list.append({'timestamp': timestamp, 'price': price})

        # Display progress
        print(f"Collected price: {price} at timestamp: {timestamp}")

        # Wait 10 seconds to respect API rate limits
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

    # Save DataFrame to a CSV file
    df.to_csv('bitcoin_prices.csv', index=False)
    print("Data saved to bitcoin_prices.csv")