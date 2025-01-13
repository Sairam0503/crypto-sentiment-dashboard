import pandas as pd
import sqlite3

# Connect to SQLite
conn = sqlite3.connect("crypto_data.db")

# Load price and volume data
df_prices = pd.read_sql_query("SELECT timestamp, price, volume FROM bitcoin_prices", conn)
print("Timestamps in bitcoin_prices:")
print(df_prices["timestamp"].head())
print(f"Number of rows in bitcoin_prices: {len(df_prices)}")

# Load sentiment data
df_sentiment = pd.read_sql_query("SELECT timestamp, sentiment FROM reddit_sentiment", conn)
print("Timestamps in reddit_sentiment:")
print(df_sentiment["timestamp"].head())
print(f"Number of rows in reddit_sentiment: {len(df_sentiment)}")

# Merge on timestamp
df = pd.merge(df_prices, df_sentiment, on="timestamp", how="inner")
print("Merged data sample:")
print(df.head())
print(f"Number of rows after merge: {len(df)}")

# Save merged data to SQLite
df.to_sql("bitcoin_prices_with_sentiment", conn, if_exists="replace", index=False)

# Close connection
conn.close()

# Save to CSV for reference
try:
    df.to_csv("bitcoin_prices_with_sentiment.csv", index=False)
    print(f"Saved {len(df)} rows to SQLite database and bitcoin_prices_with_sentiment.csv")
except Exception as e:
    print(f"Error saving to CSV: {e}")