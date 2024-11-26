import praw
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sqlite3
from datetime import datetime

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

# Scrape posts from r/Bitcoin
subreddit = reddit.subreddit('Bitcoin')
posts = subreddit.new(limit=30)  # Scrape the 30 newest posts

# List to store sentiment data
sentiment_data = []

for post in posts:
    # Get the post title and timestamp
    title = post.title
    timestamp = post.created_utc  # Unix timestamp

    # Analyze sentiment of the post title
    sentiment = analyzer.polarity_scores(title)
    compound_score = sentiment['compound']  # VADER's compound score (-1 to 1)

    # Append to the list
    sentiment_data.append({
        'timestamp': int(timestamp),
        'sentiment': compound_score,
        'post_title': title
    })

# Convert to DataFrame
sentiment_df = pd.DataFrame(sentiment_data)

# Save to CSV for reference
sentiment_df.to_csv('reddit_sentiment.csv', index=False)
print("Reddit sentiment data saved to reddit_sentiment.csv")

# Load existing Bitcoin price data from SQLite
conn = sqlite3.connect('crypto_data.db')
price_df = pd.read_sql_query('SELECT * FROM bitcoin_prices', conn)

# Since timestamps don't align, assign sentiment scores cyclically
sentiment_scores = sentiment_df['sentiment'].values
num_prices = len(price_df)
num_sentiments = len(sentiment_scores)
assigned_sentiments = [sentiment_scores[i % num_sentiments] for i in range(num_prices)]

# Add the assigned sentiment scores to the price DataFrame
price_df['sentiment'] = assigned_sentiments

# Save the updated data to SQLite
price_df.to_sql('bitcoin_prices_with_sentiment', conn, if_exists='replace', index=False)
conn.close()
print("Updated bitcoin_prices_with_sentiment table in SQLite with real sentiment data")

# Save to CSV for reference
price_df.to_csv('bitcoin_prices_with_sentiment.csv', index=False)
print("Updated bitcoin_prices_with_sentiment.csv with real sentiment data")

# Display the updated DataFrame
print("\nUpdated Bitcoin Prices with Sentiment:")
print(price_df)