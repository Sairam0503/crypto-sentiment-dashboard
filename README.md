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