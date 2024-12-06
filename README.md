# Cryptocurrency Sentiment Dashboard
A project to explore Bitcoin price trends and sentiment analysis.

## Progress
  - Set up project and collected Bitcoin price data using Finnhub API.
  - Fixed API issue by switching to BINANCE:BTCUSDT symbol to fetch real price data.
  - Fixed duplicate timestamps by using system time for unique entries.

  - Updated script to collect 30 Bitcoin price data points.
  - Added analysis script to calculate price statistics.
  - Generated mock sentiment data and visualized price vs. sentiment.

  - Added SQLite database to store Bitcoin price and sentiment data.
  - Calculated correlation between price and sentiment.
  - Updated scripts to read from SQLite for analysis and visualization.

  Created a scatter plot with a trendline to visualize price vs. sentiment.
  - Built a linear regression model to predict Bitcoin prices based on sentiment.
  - Updated README with project overview, key findings, and visualizations.

  - Performed time-series analysis with a moving average to identify price trends.
  - Built a simple web dashboard using Flask to display data and visualizations.

  - Added interactivity to the web dashboard with JavaScript (dropdown to filter data).
  - Deployed the Flask app to Heroku (note: SQLite database not supported in production; requires further configuration).
  - Improved the predictive model by adding hour of the day as a feature.

 - Scraped real sentiment data from r/Bitcoin on Reddit and replaced mock data.
  - Implemented an ARIMA model to forecast Bitcoin prices.

  - Collected daily Bitcoin price data for 30 days (1 data point per day).
  - Updated sentiment data to match the new daily Bitcoin prices.
  - Configured the Flask app to use Heroku Postgres for production deployment.