import pandas as pd
import numpy as np
import sqlite3

# Load the Bitcoin price data from SQLite
conn = sqlite3.connect('crypto_data.db')
df = pd.read_sql_query('SELECT * FROM bitcoin_prices', conn)

# Generate mock sentiment scores between -1 (negative) and 1 (positive)
np.random.seed(42)  # For reproducibility
sentiment_scores = np.random.uniform(low=-1, high=1, size=len(df))

# Add sentiment scores to the DataFrame
df['sentiment'] = sentiment_scores

# Save the updated DataFrame with sentiment data to CSV
df.to_csv('bitcoin_prices_with_sentiment.csv', index=False)
print("Added sentiment data and saved to bitcoin_prices_with_sentiment.csv")

# Save to SQLite database
df.to_sql('bitcoin_prices_with_sentiment', conn, if_exists='replace', index=False)
conn.close()
print("Added sentiment data and saved to SQLite database (crypto_data.db)")

# Display the updated dataset
print("\nDataset with Sentiment:")
print(df)