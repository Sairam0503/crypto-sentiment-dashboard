import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load the data with sentiment from SQLite
conn = sqlite3.connect('crypto_data.db')
df = pd.read_sql_query('SELECT * FROM bitcoin_prices_with_sentiment', conn)
conn.close()

# Prepare the data for modeling
X = df[['sentiment']]  # Feature (independent variable)
y = df['price']  # Target (dependent variable)

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Display the results
print("Linear Regression Model Results:")
print(f"Coefficient (slope): {model.coef_[0]:.4f}")
print(f"Intercept: {model.intercept_:.4f}")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"R-squared Score: {r2:.4f}")

# Interpret the R-squared score
if r2 > 0.7:
    print("Good fit: The model explains a large portion of the variance in Bitcoin prices.")
elif r2 > 0.3:
    print("Moderate fit: The model explains some variance, but there may be other factors influencing price.")
else:
    print("Poor fit: Sentiment alone may not be a good predictor of Bitcoin price.")