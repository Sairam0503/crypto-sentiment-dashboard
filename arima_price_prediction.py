import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings("ignore")

# Load Bitcoin price data from SQLite
conn = sqlite3.connect('crypto_data.db')
df = pd.read_sql_query('SELECT * FROM bitcoin_prices', conn)
conn.close()

# Convert timestamp to datetime
df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')

# Sort by timestamp and set as index
df = df.sort_values('timestamp')
df.set_index('datetime', inplace=True)

# Use price data for ARIMA
price_series = df['price']

# Fit ARIMA model (p=1, d=1, q=1)
model = ARIMA(price_series, order=(1, 1, 1))
model_fit = model.fit()

# Forecast the next 5 days
forecast = model_fit.forecast(steps=5)

# Create a DataFrame for the forecast with daily intervals
last_timestamp = price_series.index[-1]
forecast_index = pd.date_range(start=last_timestamp, periods=6, freq='1D')[1:]  # Daily intervals
forecast_df = pd.DataFrame({'forecast': forecast}, index=forecast_index)

# Plot the actual prices and forecast
plt.figure(figsize=(12, 6))
plt.plot(price_series.index, price_series, label='Actual Prices', color='blue')
plt.plot(forecast_df.index, forecast_df['forecast'], label='Forecasted Prices', color='red', linestyle='--')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.title('Bitcoin Price Forecast with ARIMA (Daily)')
plt.legend()

# Improve x-axis readability
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(5))
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

# Add grid lines
plt.grid(True, linestyle='--', alpha=0.7)

# Adjust y-axis range
plt.margins(y=0.1)

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('arima_forecast.png', bbox_inches='tight')
print("ARIMA forecast plot saved as arima_forecast.png")

# Display the plot (optional)
plt.show()

# Print the forecast
print("\nForecasted Prices for the Next 5 Days:")
print(forecast_df)