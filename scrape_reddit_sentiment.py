import praw
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pytz

# Reddit API credentials (replace with your own)
reddit = praw.Reddit(
     client_id='YqrKWlN33GrlDd-z9oZrpw',  
    client_secret='ZLzmAuArQyfPXpbbLxhWHLORJnhgPg',
    user_agent='crypto-sentiment-scraper',
    username='Plus_Physics_124',
    password='Sairam@147' 
)

def fetch_reddit_sentiment(start_date, end_date):
    """
    Fetch sentiment data from r/Bitcoin for each day in the specified date range.
    Returns a list of dictionaries with timestamp and sentiment.
    """
    subreddit = reddit.subreddit("Bitcoin")
    analyzer = SentimentIntensityAnalyzer()

    # Initialize a dictionary to store sentiment for each day
    sentiment_dict = {}
    utc = pytz.UTC
    start_date = start_date.replace(tzinfo=utc)
    end_date = end_date.replace(tzinfo=utc)

    # Initialize sentiment for each day in the range
    current_date = start_date
    while current_date <= end_date:
        timestamp = int(current_date.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
        sentiment_dict[timestamp] = []
        current_date += timedelta(days=1)

    # Fetch recent posts (up to 1000 to cover as much of the range as possible)
    try:
        posts = subreddit.new(limit=1000)  # Increase limit to get more posts
    except Exception as e:
        print(f"Error fetching posts from Reddit: {e}")
        return []

    # Process posts and assign sentiment to the correct day
    for post in posts:
        post_timestamp = int(post.created_utc)
        # Find the day this post belongs to (truncate to start of day)
        post_date = datetime.fromtimestamp(post_timestamp, tz=utc).replace(hour=0, minute=0, second=0, microsecond=0)
        post_day_timestamp = int(post_date.timestamp())

        # Only include posts within the date range
        if start_date.timestamp() <= post_timestamp <= end_date.timestamp():
            sentiment = analyzer.polarity_scores(post.title)["compound"]
            if post_day_timestamp in sentiment_dict:
                sentiment_dict[post_day_timestamp].append(sentiment)

    # Calculate average sentiment for each day
    data_list = []
    for timestamp, sentiments in sentiment_dict.items():
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0
        data_list.append({
            "timestamp": timestamp,
            "sentiment": avg_sentiment
        })
        date_str = datetime.fromtimestamp(timestamp, tz=utc).strftime('%Y-%m-%d')
        print(f"Collected sentiment for {date_str}: {avg_sentiment}")

    return data_list

def main():
    # Define the date range (last 30 days from today, March 25, 2025)
    end_date = datetime.now(pytz.UTC).replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=30)  # 30 days before today

    # Fetch sentiment data
    print(f"Fetching sentiment data from {start_date} to {end_date}...")
    data_list = fetch_reddit_sentiment(start_date, end_date)

    # Check if we collected any data
    if not data_list:
        print("No sentiment data collected. Please check the Reddit API credentials or subreddit.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(data_list)

    # Sort by timestamp
    df = df.sort_values("timestamp")

    # Display collected data
    print("Collected sentiment data:")
    print(df)

    # Save to CSV
    try:
        df.to_csv("reddit_sentiment.csv", index=False)
        print("Saved sentiment data to reddit_sentiment.csv")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

    # Save to SQLite
    conn = sqlite3.connect("crypto_data.db")
    df.to_sql("reddit_sentiment", conn, if_exists="replace", index=False)
    conn.close()
    print("Saved sentiment data to SQLite database (crypto_data.db)")

if __name__ == "__main__":
    main()