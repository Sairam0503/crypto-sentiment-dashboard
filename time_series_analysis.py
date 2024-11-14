import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Load the Bitcoin price data from SQLite
conn = sqlite3.connect('crypto_data.db')
df = pd.read_sql_query('SELECT * FROM bitcoin_prices', conn)
conn.close()

# Convert timestamp to datetime for better readability
df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')

# Sort by timestamp to ensure chronological order
df = df.sort_values('timestamp')

# Calculate a 5-period moving average
df['moving_average'] = df['price'].rolling(window=5).mean()

# Create a line plot of price and moving average
plt.figure(figsize=(12, 6))
plt.plot(df['datetime'], df['price'], label='Bitcoin Price', color='blue')
plt.plot(df['datetime'], df['moving_average'], label='5-Period Moving Average', color='orange')

# Add labels and title
plt.xlabel('Date and Time')
plt.ylabel('Price (USD)')
plt.title('Bitcoin Price Trends with Moving Average')
plt.legend()

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Save the plot as an image
plt.savefig('price_trends.png', bbox_inches='tight')
print("Price trends plot saved as price_trends.png")

# Display the plot (optional)
plt.show()

# Calculate price change over time
df['price_change'] = df['price'].diff()
print("\nPrice Change Statistics:")
print(f"Average Price Change: {df['price_change'].mean():.2f}")
print(f"Maximum Price Increase: {df['price_change'].max():.2f}")
print(f"Maximum Price Decrease: {df['price_change'].min():.2f}")