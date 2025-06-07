import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error

# Load the merged dataset
df = pd.read_csv("/Users/katieengel/Library/CloudStorage/OneDrive-Personal/Documents/Programming/OutbreakVision/Google Trends Data/clean_data/flu/flu_united_states_clean_data.csv")

# Sort by YEAR and WEEK (important for time series)
df = df.sort_values(by=["YEAR", "WEEK"])

# Define the Google Trends keywords
google_trends_keywords = [
    "how to stop a cough", "flu", "home remedies for flu", "flu symptoms", "flu outbreak",
    "cold vs flu", "body aches no fever", "sore throat and fever", "where to get a flu shot",
    "flu test near me", "best flu medicine"
]

# Create LAGGED features (Google search trends from past weeks)
LAG_WEEKS = 3  # Increase the number of lag weeks to consider
for lag in range(1, LAG_WEEKS + 1):
    for keyword in google_trends_keywords:
        df[f"{keyword}_lag_{lag}"] = df[keyword].shift(lag)

# Create rolling mean features for the "flu" column (Google Trends data)
df['rolling_mean_3'] = df['flu'].rolling(window=3).mean()  # 3-week rolling mean
df['rolling_mean_5'] = df['flu'].rolling(window=5).mean()  # 5-week rolling mean

# Create trend feature: percentage change in flu searches from week to week
df['flu_trend'] = df['flu'].pct_change()  # Percentage change
df['flu_diff'] = df['flu'].diff()  # Difference from previous week

df["target_3_weeks_ahead"] = df["TOTAL"].shift(-3)

# Drop rows with NaN values (caused by shifting and rolling)
df = df.dropna()

# Define FEATURES and TARGET
# Add "total_positive_specimens" to the FEATURES list
FEATURES = ["YEAR", "WEEK", "TOTAL"] + \
           [col for col in df.columns if "_lag_" in col] + \
           ["rolling_mean_3", "rolling_mean_5", "flu_trend", "flu_diff"]

TARGET = "target_3_weeks_ahead"  # Target variable

# Split the data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(df[FEATURES], df[TARGET], test_size=0.2, shuffle=False)

# Hyperparameter tuning using Grid Search
param_grid = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

model = xgb.XGBRegressor(objective="reg:squarederror")
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring='neg_mean_absolute_error', verbose=1)
grid_search.fit(X_train, y_train)

# Best model from Grid Search
best_model = grid_search.best_estimator_

# Predict on test set
y_pred = best_model.predict(X_test)

# Evaluate model performance
mae = mean_absolute_error(y_test, y_pred)
print(f"📊 Mean Absolute Error: {mae:.2f} cases")

# Create a new column for plotting
X_test['DATE'] = pd.to_datetime(X_test['YEAR'].astype(str) + X_test['WEEK'].astype(str) + '1', format='%G%V%u')

# Plot actual vs predicted cases
plt.figure(figsize=(12, 6))
plt.plot(X_test["DATE"], y_test, label="Actual Cases", marker="o")
plt.plot(X_test["DATE"], y_pred, label="Predicted Cases", marker="x")
plt.xlabel("Year + Week Number")
plt.ylabel("Flu Cases")
plt.legend()
plt.title("Flu Case Prediction vs. Actual Data (3 Weeks Ahead)")
plt.show()