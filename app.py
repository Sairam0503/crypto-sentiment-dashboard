import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import os
from datetime import datetime
import pytz
from sqlalchemy import create_engine

# Initialize Dash app
app = dash.Dash(__name__)

# Heroku Postgres connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgres://u345apggsphrfg:p9f4989c39615ae63aea2056d2dfc39d1f67232e11fa3411ddbf58438b1e177e9@cf980tnnkgv1bp.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d55odaqnqfo7j7")

# Modify DATABASE_URL for SQLAlchemy (replace 'postgres://' with 'postgresql://')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Define utc timezone
utc = pytz.utc

def fetch_data():
    """Fetch data from Heroku Postgres using SQLAlchemy."""
    try:
        # Use pandas with SQLAlchemy engine
        df = pd.read_sql_query("SELECT * FROM bitcoin_prices_with_sentiment ORDER BY timestamp", engine)
        # Ensure correct data types
        df["timestamp"] = df["timestamp"].astype(int)
        df["price"] = df["price"].astype(float)
        df["volume"] = df["volume"].astype(float)
        df["sentiment"] = df["sentiment"].astype(float)
        df["date"] = pd.to_datetime(df["timestamp"], unit="s")
        # Log the latest data for debugging
        if not df.empty:
            latest_row = df.iloc[-1]
            print(f"Fetched {len(df)} rows from database at {datetime.now(pytz.UTC)}. Latest timestamp: {df['timestamp'].iloc[-1]}")
            print(f"Latest data: timestamp={latest_row['timestamp']}, price={latest_row['price']}, sentiment={latest_row['sentiment']}")
        else:
            print("No data fetched from database.")
        return df
    except Exception as e:
        print(f"Error fetching data from Heroku Postgres: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

# Layout
app.layout = html.Div([
    html.H1("Crypto Sentiment Dashboard"),
    html.Div(id="last-updated", style={"margin-bottom": "20px"}),
    dcc.Graph(id="price-graph"),
    dcc.Graph(id="sentiment-graph"),
    dcc.Interval(id="interval-component", interval=60*1000, n_intervals=0)  # Update every 60 seconds
])

# Callback to update graphs and last updated time
@app.callback(
    [dash.dependencies.Output("price-graph", "figure"),
     dash.dependencies.Output("sentiment-graph", "figure"),
     dash.dependencies.Output("last-updated", "children")],
    [dash.dependencies.Input("interval-component", "n_intervals")]
)
def update_graphs(n):
    df = fetch_data()

    if df.empty:
        print("No data available to plot.")
        empty_fig = {"data": [], "layout": {"title": "No Data Available"}}
        last_updated = f"Last updated: {datetime.now(pytz.UTC).astimezone(utc).strftime('%Y-%m-%d %I:%M:%S %p UTC')} (No data)"
        return empty_fig, empty_fig, last_updated

    # Price graph
    price_fig = px.line(df, x="date", y="price", title="Bitcoin Price Over Time")
    price_fig.update_layout(transition_duration=500)  # Smooth transition for updates
    # Ensure y-axis range is appropriate
    price_fig.update_yaxes(range=[df["price"].min() * 0.95, df["price"].max() * 1.05])

    # Sentiment graph
    sentiment_fig = px.line(df, x="date", y="sentiment", title="Reddit Sentiment Over Time")
    sentiment_fig.update_layout(transition_duration=500)  # Smooth transition for updates
    # Ensure y-axis range is appropriate
    sentiment_fig.update_yaxes(range=[-1, 1])  # Sentiment should be between -1 and 1

    # Last updated timestamp in UTC
    last_updated = f"Last updated: {datetime.now(pytz.UTC).astimezone(utc).strftime('%Y-%m-%d %I:%M:%S %p UTC')}"

    return price_fig, sentiment_fig, last_updated

# Run the app
if __name__ == "__main__":
    # For Heroku, bind to the correct port and host
    port = int(os.getenv("PORT", 8050))  # Use Heroku's PORT or default to 8050 for local
    app.run(host="0.0.0.0", port=port, debug=False)  # Bind to 0.0.0.0 and disable debug mode for Heroku