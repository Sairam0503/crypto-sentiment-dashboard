import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings("ignore")  # Suppress warnings for cleaner output

# Load Bitcoin price data from SQLite
conn = sqlite3.connect('crypto_data.db')
df = pd.read_sql_query('SELECT * FROM bitcoin_prices', conn)
conn.close()

# Convert timestamp to datetime
df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')

# Sort by timestamp to ensure chronological order
df = df.sort_values('timestamp')

# Since the data was collected at 10-second intervals, ensure the index reflects this
# Create a new datetime index with 10-second intervals starting from the first timestamp
start_time = df['datetime'].iloc[0]
time_index = pd.date_range(start=start_time, periods=len(df), freq='10S')
df['datetime'] = time_index
df.set_index('datetime', inplace=True)

# Use price data for ARIMA
price_series = df['price']

# Fit ARIMA model (p=1, d=1, q=1 for simplicity; can be tuned later)
model = ARIMA(price_series, order=(1, 1, 1))
model_fit = model.fit()

# Forecast the next 10 time steps (100 seconds into the future, based on 10-second intervals)
forecast = model_fit.forecast(steps=10)

# Create a DataFrame for the forecast with correct 10-second intervals
last_timestamp = price_series.index[-1]
forecast_index = pd.date_range(start=last_timestamp, periods=11, freq='10S')[1:]  # 10-second intervals
forecast_df = pd.DataFrame({'forecast': forecast}, index=forecast_index)

# Plot the actual prices and forecast
plt.figure(figsize=(12, 6))
plt.plot(price_series.index, price_series, label='Actual Prices', color='blue')
plt.plot(forecast_df.index, forecast_df['forecast'], label='Forecasted Prices', color='red', linestyle='--')

# Add labels and title
plt.xlabel('Date and Time')
plt.ylabel('Price (USD)')
plt.title('Bitcoin Price Forecast with ARIMA (10-Second Intervals)')
plt.legend()

# Improve x-axis readability: show fewer ticks and format them
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(5))  # Reduce to 5 ticks for better spacing
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.xticks(rotation=45)

# Add grid lines for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Adjust y-axis range to fit the data better
plt.margins(y=0.1)  # Add 10% margin above and below the data

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the plot as an image
plt.savefig('arima_forecast.png', bbox_inches='tight')
print("ARIMA forecast plot saved as arima_forecast.png")

# Display the plot (optional)
plt.show()

# Print the forecast
print("\nForecasted Prices for the Next 10 Time Steps (10-Second Intervals):")
print(forecast_df)