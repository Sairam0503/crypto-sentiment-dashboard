import requests
import praw
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pytz
import psycopg2
from psycopg2 import sql
import os

# Reddit API credentials (replace with your own)
reddit = praw.Reddit(
     client_id='YqrKWlN33GrlDd-z9oZrpw',  
    client_secret='ZLzmAuArQyfPXpbbLxhWHLORJnhgPg',
    user_agent='crypto-sentiment-scraper',
    username='Plus_Physics_124',
    password='Sairam@147' 
)

# Heroku Postgres connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgres://udn385mh2lkpp:p3ac1a38bd616e39abcb85bb86071b30e5ec6c49de222fa4fd5e518530e652d10@cbec45869p4jbu.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/db6st1ghre0bl6")

def fetch_current_bitcoin_data():
    """
    Fetch the current Bitcoin price and volume using CryptoCompare API.
    Returns a dictionary with timestamp, price, and volume.
    """
    url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD"
    volume_url = "https://min-api.cryptocompare.com/data/v2/histominute?fsym=BTC&tsym=USD&limit=1"

    try:
        # Fetch price
        price_response = requests.get(url)
        price_response.raise_for_status()
        price_data = price_response.json()
        price = price_data["USD"]

        # Fetch volume (using the last minute's data as a proxy for current volume)
        volume_response = requests.get(volume_url)
        volume_response.raise_for_status()
        volume_data = volume_response.json()
        volume = volume_data["Data"]["Data"][-1]["volumeto"]

        # Get current timestamp (truncate to start of minute)
        utc = pytz.UTC
        current_time = datetime.now(utc).replace(second=0, microsecond=0)
        timestamp = int(current_time.timestamp())

        return {
            "timestamp": timestamp,
            "price": price,
            "volume": volume
        }
    except Exception as e:
        print(f"Error fetching Bitcoin data: {e}")
        return None

def stream_reddit_sentiment():
    """
    Stream new Reddit posts from r/Bitcoin and calculate sentiment.
    Returns the average sentiment for new posts since the last update.
    """
    subreddit = reddit.subreddit("Bitcoin")
    analyzer = SentimentIntensityAnalyzer()
    sentiments = []

    try:
        # Stream new posts (non-blocking, fetch posts for 60 seconds)
        start_time = time.time()
        for post in subreddit.stream.submissions(pause_after=0):
            if post is None:  # No new post, continue waiting
                if time.time() - start_time >= 60:  # Wait for 60 seconds max
                    break
                continue

            sentiment = analyzer.polarity_scores(post.title)["compound"]
            sentiments.append(sentiment)
            print(f"New post sentiment: {sentiment}")

            if time.time() - start_time >= 60:  # Stop after 60 seconds
                break

        # Calculate average sentiment
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0
        print(f"Average sentiment: {avg_sentiment}")
        return avg_sentiment
    except Exception as e:
        print(f"Error streaming Reddit posts: {e}")
        return 0.0

def update_database(data):
    """
    Update the Heroku Postgres database with the new data.
    """
    try:
        # Connect to Heroku Postgres
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cursor = conn.cursor()

        # Check if a row for this timestamp already exists
        cursor.execute(
            "SELECT COUNT(*) FROM bitcoin_prices_with_sentiment WHERE timestamp = %s",
            (data["timestamp"],)
        )
        exists = cursor.fetchone()[0] > 0

        if exists:
            # Update existing row
            cursor.execute(
                """
                UPDATE bitcoin_prices_with_sentiment
                SET price = %s, volume = %s, sentiment = %s
                WHERE timestamp = %s
                """,
                (data["price"], data["volume"], data["sentiment"], data["timestamp"])
            )
        else:
            # Insert new row
            cursor.execute(
                """
                INSERT INTO bitcoin_prices_with_sentiment (timestamp, price, volume, sentiment)
                VALUES (%s, %s, %s, %s)
                """,
                (data["timestamp"], data["price"], data["volume"], data["sentiment"])
            )

        conn.commit()
        print(f"Updated database with timestamp {data['timestamp']}")
    except Exception as e:
        print(f"Error updating database: {e}")
    finally:
        cursor.close()
        conn.close()

def main():
    print("Starting live updates...")
    utc = pytz.UTC
    last_update = None

    while True:
        # Get current time (truncate to start of minute)
        current_time = datetime.now(utc).replace(second=0, microsecond=0)
        current_timestamp = int(current_time.timestamp())

        # Update every minute
        if last_update != current_timestamp:
            # Fetch Bitcoin data
            bitcoin_data = fetch_current_bitcoin_data()
            if bitcoin_data:
                print(f"Fetched Bitcoin data: {bitcoin_data}")
                # Stream Reddit sentiment
                sentiment = stream_reddit_sentiment()
                print(f"Calculated sentiment: {sentiment}")
                # Combine data
                data = {
                    "timestamp": current_timestamp,
                    "price": bitcoin_data["price"],
                    "volume": bitcoin_data["volume"],
                    "sentiment": sentiment
                }
                print(f"Data to update: {data}")
                # Update database
                update_database(data)

            last_update = current_timestamp

        # Sleep until the next minute
        time_to_next_minute = 60 - (time.time() % 60)
        time.sleep(time_to_next_minute)

if __name__ == "__main__":
    main()