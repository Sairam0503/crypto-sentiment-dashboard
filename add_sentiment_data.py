import pandas as pd
import numpy as np

# Load the Bitcoin price data
df = pd.read_csv('bitcoin_prices.csv')

# Set a random seed for reproducibility
np.random.seed(42)

# Generate mock sentiment scores between -1 (negative) and 1 (positive)
sentiment_scores = np.random.uniform(low=-1, high=1, size=len(df))

# Add the sentiment scores as a new column
df['sentiment'] = sentiment_scores

# Save the updated dataset
df.to_csv('bitcoin_prices_with_sentiment.csv', index=False)
print("Added mock sentiment data and saved to bitcoin_prices_with_sentiment.csv")
print("\nUpdated Dataset:")
print(df)