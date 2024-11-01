import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Load the data with sentiment from SQLite
conn = sqlite3.connect('crypto_data.db')
df = pd.read_sql_query('SELECT * FROM bitcoin_prices_with_sentiment', conn)
conn.close()

# Create a line plot with two y-axes
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot Bitcoin price on the left y-axis
ax1.plot(df['timestamp'], df['price'], color='blue', label='Bitcoin Price')
ax1.set_xlabel('Timestamp')
ax1.set_ylabel('Price (USD)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Create a second y-axis for sentiment
ax2 = ax1.twinx()
ax2.plot(df['timestamp'], df['sentiment'], color='green', label='Sentiment')
ax2.set_ylabel('Sentiment Score', color='green')
ax2.tick_params(axis='y', labelcolor='green')

# Add a title and legend
plt.title('Bitcoin Price vs. Sentiment Over Time')
fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2)

# Save the plot as an image
plt.savefig('price_vs_sentiment.png', bbox_inches='tight')
print("Plot saved as price_vs_sentiment.png")

# Display the plot (optional, might not work in some environments)
plt.show()