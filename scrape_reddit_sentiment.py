import praw
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sqlite3

# Reddit API credentials
reddit = praw.Reddit(
    client_id='YqrKWlN33GrlDd-z9oZrpw',  
    client_secret='ZLzmAuArQyfPXpbbLxhWHLORJnhgPg',
    user_agent='crypto-sentiment-scraper',
    username='Plus_Physics_124',
    password='Sairam@147' 
)

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Load Bitcoin price data from SQLite to get the timestamps
conn = sqlite3.connect('crypto_data.db')
price_df = pd.read_sql_query('SELECT * FROM bitcoin_prices', conn)

# Scrape 30 recent posts from r/Bitcoin
subreddit = reddit.subreddit('Bitcoin')
posts = subreddit.new(limit=30)  # Get the 30 newest posts

# List to store sentiment data
sentiment_data = []

# Analyze sentiment for each post
for post in posts:
    sentiment = analyzer.polarity_scores(post.title)
    compound_score = sentiment['compound']  # VADER's compound score (-1 to 1)
    sentiment_data.append(compound_score)

# Ensure we have 30 sentiment scores (if fewer posts, repeat the last score)
while len(sentiment_data) < 30:
    sentiment_data.append(sentiment_data[-1] if sentiment_data else 0)

# Create a DataFrame with sentiment scores aligned to Bitcoin price timestamps
sentiment_df = pd.DataFrame({
    'timestamp': price_df['timestamp'],
    'sentiment': sentiment_data[:30]  # Take the first 30 sentiment scores
})

# Save to CSV for reference
sentiment_df.to_csv('reddit_sentiment.csv', index=False)
print("Reddit sentiment data saved to reddit_sentiment.csv")

# Merge with Bitcoin price data
merged_df = price_df.merge(sentiment_df, on='timestamp', how='left')

# Save the updated data to SQLite
merged_df.to_sql('bitcoin_prices_with_sentiment', conn, if_exists='replace', index=False)
conn.close()
print("Updated bitcoin_prices_with_sentiment table in SQLite with simulated sentiment data")

# Save to CSV for reference
merged_df.to_csv('bitcoin_prices_with_sentiment.csv', index=False)
print("Updated bitcoin_prices_with_sentiment.csv with simulated sentiment data")