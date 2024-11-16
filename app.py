from flask import Flask, render_template
import pandas as pd
import sqlite3

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Load data from SQLite
    conn = sqlite3.connect('crypto_data.db')
    df = pd.read_sql_query('SELECT * FROM bitcoin_prices_with_sentiment', conn)
    conn.close()

    # Convert DataFrame to HTML table
    data_table = df.to_html(classes='table table-striped', index=False)

    return render_template('dashboard.html', data_table=data_table)

if __name__ == '__main__':
    app.run(debug=True)