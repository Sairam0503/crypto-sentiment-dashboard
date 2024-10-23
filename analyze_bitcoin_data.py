import pandas as pd

# Load the Bitcoin price data from the CSV file
df = pd.read_csv('bitcoin_prices.csv')

# Calculate basic statistics
average_price = df['price'].mean()  # Average price
min_price = df['price'].min()  # Minimum price
max_price = df['price'].max()  # Maximum price

# Display the results
print("Bitcoin Price Analysis:")
print(f"Average Price: {average_price:.2f}")
print(f"Minimum Price: {min_price:.2f}")
print(f"Maximum Price: {max_price:.2f}")

# Show the full dataset
print("\nFull Dataset:")
print(df)