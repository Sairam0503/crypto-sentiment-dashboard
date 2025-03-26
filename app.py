from flask import Flask, render_template
import pandas as pd
from sqlalchemy import create_engine
import os

app = Flask(__name__)

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

    # Convert DataFrame to HTML table
    data_table = df.to_html(classes='table table-striped', index=False)

    return render_template('dashboard.html', data_table=data_table)

if __name__ == '__main__':
    app.run(debug=True)