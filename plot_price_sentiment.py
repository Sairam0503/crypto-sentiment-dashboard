import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from matplotlib.dates import DateFormatter

# Load the data with sentiment from SQLite
try:
    conn = sqlite3.connect('crypto_data.db')
    df = pd.read_sql_query('SELECT * FROM bitcoin_prices_with_sentiment', conn)
    conn.close()
except sqlite3.Error as e:
    print(f"Error connecting to database or querying data: {e}")
    exit()

# Convert timestamp to datetime for better x-axis readability
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

# Create a line plot with two y-axes
fig, ax1 = plt.subplots(figsize=(12, 6))  # Slightly wider for date labels

# Plot Bitcoin price on the left y-axis
ax1.plot(df['timestamp'], df['price'], color='blue', label='Bitcoin Price')
ax1.set_xlabel('Date')
ax1.set_ylabel('Price (USD)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True, linestyle='--', alpha=0.7)  # Add gridlines

# Format x-axis with readable dates
ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')  # Rotate for readability

# Create a second y-axis for sentiment
ax2 = ax1.twinx()
ax2.plot(df['timestamp'], df['sentiment'], color='green', label='Sentiment')
ax2.set_ylabel('Sentiment Score', color='green')
ax2.tick_params(axis='y', labelcolor='green')

# Add a title and legend
plt.title('Bitcoin Price vs. Sentiment Over Time')
fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)  # Adjusted position

# Save the plot as an image
plt.savefig('price_vs_sentiment.png', bbox_inches='tight', dpi=100)
print("Plot saved as price_vs_sentiment.png")

# Display the plot (optional, might not work in some environments)
plt.show()