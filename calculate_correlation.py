import pandas as pd
import sqlite3

# Load the data with sentiment from SQLite
conn = sqlite3.connect('crypto_data.db')
df = pd.read_sql_query('SELECT * FROM bitcoin_prices_with_sentiment', conn)
conn.close()

# Calculate the Pearson correlation coefficient between price and sentiment
correlation = df['price'].corr(df['sentiment'], method='pearson')

# Display the result
print("Correlation Analysis:")
print(f"Pearson Correlation Coefficient between Price and Sentiment: {correlation:.4f}")

# Interpret the correlation
if correlation > 0:
    print("Positive correlation: As sentiment increases, price tends to increase.")
elif correlation < 0:
    print("Negative correlation: As sentiment increases, price tends to decrease.")
else:
    print("No correlation: Sentiment and price do not appear to be related.")