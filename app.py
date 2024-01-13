import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
<<<<<<< HEAD
<<<<<<< HEAD
import psycopg2
import os
from datetime import datetime
import pytz
=======
from sqlalchemy import create_engine
import os
>>>>>>> 19837e2 (Updated Flask app to use Heroku Postgres)
=======
import os
from datetime import datetime
import pytz
from sqlalchemy import create_engine
>>>>>>> a10ce65 (Fix R10 boot timeout by binding to correct port and host)

# Initialize Dash app
app = dash.Dash(__name__)

<<<<<<< HEAD
# Heroku Postgres connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgres://udn385mh2lkpp:p3ac1a38bd616e39abcb85bb86071b30e5ec6c49de222fa4fd5e518530e652d10@cbec45869p4jbu.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/db6st1ghre0bl6")
=======
# Get the DATABASE_URL from environment variables (set by Heroku)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///crypto_data.db')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

@app.route('/')
def dashboard():
    # Load data from Postgres
    df = pd.read_sql_query('SELECT * FROM bitcoin_prices_with_sentiment', engine)
>>>>>>> 19837e2 (Updated Flask app to use Heroku Postgres)

# Modify DATABASE_URL for SQLAlchemy (replace 'postgres://' with 'postgresql://')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

def fetch_data():
    """Fetch data from Heroku Postgres using SQLAlchemy."""
    try:
        # Use pandas with SQLAlchemy engine
        df = pd.read_sql_query("SELECT * FROM bitcoin_prices_with_sentiment ORDER BY timestamp", engine)
        df["date"] = pd.to_datetime(df["timestamp"], unit="s")
        print(f"Fetched {len(df)} rows from database at {datetime.now(pytz.UTC)}. Latest timestamp: {df['timestamp'].iloc[-1] if not df.empty else 'N/A'}")
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
        last_updated = f"Last updated: {datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S UTC')} (No data)"
        return empty_fig, empty_fig, last_updated

    # Price graph
    price_fig = px.line(df, x="date", y="price", title="Bitcoin Price Over Time")
    price_fig.update_layout(transition_duration=500)  # Smooth transition for updates

    # Sentiment graph
    sentiment_fig = px.line(df, x="date", y="sentiment", title="Reddit Sentiment Over Time")
    sentiment_fig.update_layout(transition_duration=500)  # Smooth transition for updates

    # Last updated timestamp
    last_updated = f"Last updated: {datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}"

    return price_fig, sentiment_fig, last_updated

# Run the app
if __name__ == "__main__":
    # For Heroku, bind to the correct port and host
    port = int(os.getenv("PORT", 8050))  # Use Heroku's PORT or default to 8050 for local
    app.run(host="0.0.0.0", port=port, debug=False)  # Bind to 0.0.0.0 and disable debug mode for Heroku