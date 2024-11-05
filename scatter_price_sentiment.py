import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

# Load the data with sentiment from SQLite
conn = sqlite3.connect('crypto_data.db')
df = pd.read_sql_query('SELECT * FROM bitcoin_prices_with_sentiment', conn)
conn.close()

# Create a scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df['sentiment'], df['price'], color='blue', alpha=0.5, label='Data Points')

# Add a trendline (linear fit)
z = np.polyfit(df['sentiment'], df['price'], 1)  # Fit a 1st-degree polynomial (linear)
p = np.poly1d(z)  # Create a polynomial function
plt.plot(df['sentiment'], p(df['sentiment']), color='red', label='Trendline')

# Add labels and title
plt.xlabel('Sentiment Score')
plt.ylabel('Bitcoin Price (USD)')
plt.title('Bitcoin Price vs. Sentiment (Scatter with Trendline)')
plt.legend()

# Save the plot as an image
plt.savefig('scatter_price_sentiment.png', bbox_inches='tight')
print("Scatter plot saved as scatter_price_sentiment.png")

# Display the plot (optional)
plt.show()