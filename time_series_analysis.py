import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Load the Bitcoin price and sentiment data from SQLite
conn = sqlite3.connect('crypto_data.db')
df = pd.read_sql_query('SELECT * FROM bitcoin_prices_with_sentiment', conn)
conn.close()

# Convert timestamp to datetime for better readability
df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')

# Sort by timestamp to ensure chronological order
df = df.sort_values('timestamp')

# Calculate a 5-period moving average for price
df['moving_average'] = df['price'].rolling(window=5).mean()

# Create a line plot with two y-axes
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot Bitcoin price and moving average on the left y-axis
ax1.plot(df['datetime'], df['price'], label='Bitcoin Price', color='blue')
ax1.plot(df['datetime'], df['moving_average'], label='5-Period Moving Average', color='orange')
ax1.set_xlabel('Date and Time')
ax1.set_ylabel('Price (USD)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Create a second y-axis for sentiment
ax2 = ax1.twinx()
ax2.plot(df['datetime'], df['sentiment'], label='Sentiment', color='green')
ax2.set_ylabel('Sentiment Score', color='green')
ax2.tick_params(axis='y', labelcolor='green')

# Add title and legend
plt.title('Bitcoin Price Trends with Moving Average and Sentiment')
fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Save the plot as an image
plt.savefig('price_trends_with_sentiment.png', bbox_inches='tight')
print("Price trends plot with sentiment saved as price_trends_with_sentiment.png")

# Display the plot (optional)
plt.show()

# Calculate price change over time
df['price_change'] = df['price'].diff()
print("\nPrice Change Statistics:")
print(f"Average Price Change: {df['price_change'].mean():.2f}")
print(f"Maximum Price Increase: {df['price_change'].max():.2f}")
print(f"Maximum Price Decrease: {df['price_change'].min():.2f}")