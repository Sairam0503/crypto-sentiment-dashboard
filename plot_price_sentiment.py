import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset with sentiment
df = pd.read_csv('bitcoin_prices_with_sentiment.csv')

# Create a figure with two subplots (one for price, one for sentiment)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

# Plot Bitcoin prices
ax1.plot(df['timestamp'], df['price'], color='blue', label='Bitcoin Price')
ax1.set_title('Bitcoin Price Over Time')
ax1.set_ylabel('Price (USD)')
ax1.legend()
ax1.grid(True)

# Plot sentiment scores
ax2.plot(df['timestamp'], df['sentiment'], color='green', label='Sentiment Score')
ax2.set_title('Sentiment Over Time')
ax2.set_xlabel('Timestamp')
ax2.set_ylabel('Sentiment (-1 to 1)')
ax2.legend()
ax2.grid(True)

# Adjust layout to prevent overlap
plt.tight_layout()

# Save the plot as an image
plt.savefig('price_sentiment_plot.png')
print("Plot saved as price_sentiment_plot.png")

# Display the plot
plt.show()