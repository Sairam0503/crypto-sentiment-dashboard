# Cryptocurrency Sentiment Dashboard
A project to explore Bitcoin price trends and sentiment analysis.

#### `get_bitcoin_data.py`
This script fetches historical daily Bitcoin (BTC) price and volume data in USD from the CryptoCompare API, processes it, and saves it to both a CSV file and a SQLite database.

- **Functionality**:
  - Fetches data for the last 30 days from the current date (UTC).
  - Retrieves closing price and trading volume for each day.
  - Saves data to `bitcoin_prices.csv` (CSV format) and `crypto_data.db` (SQLite database, table `bitcoin_prices`).
  - Handles errors for API requests, file writing, and database operations.

- **Key Components**:
  - `fetch_bitcoin_data(start_date, end_date)`: Queries the CryptoCompare API and returns a list of daily BTC data.
  - `main()`: Manages the workflow, including date range setup, data fetching, and storage.

#### `analyze_bitcoin_data.py`
This script performs a basic statistical analysis of Bitcoin price data stored in `bitcoin_prices.csv`, generated by `get_bitcoin_data.py`.

- **Functionality**:
  - Loads Bitcoin price data from `bitcoin_prices.csv`.
  - Calculates and displays:
    - Average price over the dataset.
    - Minimum price in the dataset.
    - Maximum price in the dataset.
  - Prints the full dataset for review.

#### `add_sentiment_data.py`
This script enhances the Bitcoin price data from `crypto_data.db` by adding mock sentiment scores and saves the updated dataset to both CSV and SQLite.

- **Functionality**:
  - Loads Bitcoin price data from the `bitcoin_prices` table in `crypto_data.db`.
  - Generates random sentiment scores between -1 (negative) and 1 (positive) for each day.
  - Adds these scores as a new `sentiment` column to the dataset.
  - Saves the updated data to:
    - `bitcoin_prices_with_sentiment.csv` (CSV file).
    - `bitcoin_prices_with_sentiment` table in `crypto_data.db` (overwrites if exists).
  - Displays the updated dataset in the console.

#### `plot_price_sentiment.py`
This script generates a dual-axis line plot comparing Bitcoin price and sentiment scores over time, using data from `crypto_data.db`, with enhanced readability and error handling.

- **Functionality**:
  - Loads data from the `bitcoin_prices_with_sentiment` table in `crypto_data.db`.
  - Plots:
    - Bitcoin price (USD) on the left y-axis (blue line).
    - Sentiment scores (-1 to 1) on the right y-axis (green line).
    - X-axis shows dates in `YYYY-MM-DD` format.
  - Includes gridlines for easier value tracking.
  - Saves the plot as `price_vs_sentiment.png`.
![Bitcoin Price vs. Sentiment Plot](static/price_vs_sentiment.png)