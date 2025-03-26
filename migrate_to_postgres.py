import pandas as pd
import sqlite3
from sqlalchemy import create_engine, text
import os

# Connect to SQLite and read data
try:
    conn_sqlite = sqlite3.connect('crypto_data.db')
    df = pd.read_sql_query('SELECT * FROM bitcoin_prices_with_sentiment', conn_sqlite)
    print(f"Successfully read {len(df)} rows from SQLite database")
    if df.empty:
        print("Error: The bitcoin_prices_with_sentiment table is empty!")
        exit(1)
    print("Sample data from SQLite:")
    print(df.head())
    conn_sqlite.close()
except Exception as e:
    print(f"Failed to read from SQLite database: {e}")
    exit(1)

# Get the DATABASE_URL
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print("Error: DATABASE_URL environment variable is not set!")
    exit(1)
if DATABASE_URL.startswith("sqlite://"):
    print("Error: DATABASE_URL points to a SQLite database, expected a Postgres database!")
    exit(1)

# Replace postgres:// with postgresql:// for SQLAlchemy
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
print(f"Using DATABASE_URL: {DATABASE_URL}")

# Connect to Heroku Postgres
try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        # Verify it's a Postgres database
        result = connection.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        if "PostgreSQL" not in version:
            print("Error: Connected database is not PostgreSQL!")
            exit(1)
        print(f"Successfully connected to Heroku Postgres! (Version: {version})")
except Exception as e:
    print(f"Failed to connect to Heroku Postgres: {e}")
    exit(1)

# Save to Postgres
try:
    df.to_sql('bitcoin_prices_with_sentiment', engine, if_exists='replace', index=False)
    print("Data successfully migrated to Heroku Postgres")
except Exception as e:
    print(f"Failed to write to Heroku Postgres: {e}")
<<<<<<< HEAD
    exit(1)
    
=======
    exit(1)
>>>>>>> 19837e2 (Updated Flask app to use Heroku Postgres)
