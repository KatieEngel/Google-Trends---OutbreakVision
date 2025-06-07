import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import mean_absolute_error

# Load the merged dataset
df = pd.read_csv("/Users/katieengel/Library/CloudStorage/OneDrive-Personal/Documents/Programming/OutbreakVision/Google Trends Data/clean_data/covid/covid_united_states_clean_data.csv")

df.replace("<1", "0", inplace=True)

# Convert the date column to datetime format
df['Week'] = pd.to_datetime(df['Week'])

# Extract date features
df['Year'] = df['Week'].dt.year
df['Month'] = df['Week'].dt.month
df['WeekOfYear'] = df['Week'].dt.isocalendar().week

# Sort by Date (important for time series)
df = df.sort_values(by=["Week"])

# Define the Google Trends keywords
google_trends_keywords = [
    "covid",
    "fever",
    "cough",
    "loss of taste and smell",
    "face masks",
    "vaccine appointment",
    "vaccine availability",
    "covid testing near me"
]

# Create LAGGED features (Google search trends from past weeks)
LAG_WEEKS = 3  # Increase the number of lag weeks to consider
for lag in range(1, LAG_WEEKS + 1):
    for keyword in google_trends_keywords:
        df[f"{keyword}_lag_{lag}"] = df[keyword].shift(lag)

# Create rolling mean features for the "covid" column (Google Trends data)
df['rolling_mean_3'] = df['covid'].rolling(window=3).mean()  # 3-week rolling mean
df['rolling_mean_5'] = df['covid'].rolling(window=5).mean()  # 5-week rolling mean

# Create trend feature: percentage change in covid searches from week to week
df['covid_trend'] = df['covid'].pct_change()  # Percentage change
df['covid_diff'] = df['covid'].diff()  # Difference from previous week

# Create the target variable: cumulative cases 3 weeks ahead
df["target_3_weeks_ahead"] = df["Cumulative_cases"].shift(-3)

# Drop rows with NaN values (caused by shifting and rolling)
df = df.dropna()

# Define FEATURES and TARGET
FEATURES = ["Cumulative_cases", "Year", "WeekOfYear"] + \
           [col for col in df.columns if "_lag_" in col] + \
           ["rolling_mean_3", "rolling_mean_5", "covid_trend", "covid_diff"]

TARGET = "target_3_weeks_ahead"  # Target variable

# Define the directory where you want to save the model
directory = '/Users/katieengel/Library/CloudStorage/OneDrive-Personal/Documents/Programming/OutbreakVision/Google Trends Data/models'

if not os.path.exists(directory):
    os.makedirs(directory)

# Save the features (X) and target (y) as CSV files
last_three = df.tail(3)
last_three = last_three[FEATURES]
last_three.to_csv(os.path.join(directory, 'last_x_data.csv'), index=False)

X = df[FEATURES]
y = df[TARGET]

# Split the data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Hyperparameter tuning using Grid Search
param_grid = {'alpha': [0.1, 1.0, 10.0, 100.0]}  # Range of alpha values
ridge_model = Ridge()

grid_search = GridSearchCV(ridge_model, param_grid, cv=5, scoring='neg_mean_absolute_error')  # Using MAE as scoring metric
grid_search.fit(X_train, y_train)

# Best model based on GridSearchCV
best_ridge_model = grid_search.best_estimator_

# Evaluate the model on the test data
y_pred_test = best_ridge_model.predict(X_test)
mae_test = mean_absolute_error(y_test, y_pred_test)
print(f"Mean Absolute Error on Test Data: {mae_test:.2f}")

# Cross-validation (optional, for better model evaluation)
cv_scores = cross_val_score(best_ridge_model, X, y, cv=5, scoring='neg_mean_absolute_error')
print(f"Cross-validated MAE: {-cv_scores.mean():.2f}")

# Plot Actual vs Predicted Values
plt.figure(figsize=(12, 6))
plt.plot(y_test.values, label="Actual Covid Cases", color="blue", alpha=0.6, marker='o', linestyle='None')
plt.plot(y_pred_test, label="Predicted Covid Cases", color="red", alpha=0.6, marker='x', linestyle='None')
plt.title("Actual vs Predicted Covid Cases")
plt.xlabel("Index")
plt.ylabel("Number of Covid Cases")
plt.legend()
plt.grid(True)
plt.show()

# Save the model to the specified directory
with open(os.path.join(directory, 'covid_model.pkl'), 'wb') as model_file:
    joblib.dump(best_ridge_model, model_file)

print(f'Model and data saved to {directory}')