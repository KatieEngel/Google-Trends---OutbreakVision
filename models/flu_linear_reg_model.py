import pandas as pd
import xgboost as xgb
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler, PolynomialFeatures

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


# Define FEATURES and TARGET
# Add "total_positive_specimens" to the FEATURES list
FEATURES = ["YEAR", "WEEK", "TOTAL"] + \
           [col for col in df.columns if "_lag_" in col] + \
           ["rolling_mean_3", "rolling_mean_5", "flu_trend", "flu_diff"]

TARGET = "target_3_weeks_ahead"  # Target variable

# Define the directory where you want to save the model
directory = '/Users/katieengel/Library/CloudStorage/OneDrive-Personal/Documents/Programming/OutbreakVision/Google Trends Data/models'

if not os.path.exists(directory):
    os.makedirs(directory)

# Save the features (X) and target (y) as CSV files
last_three = df.tail(3)
last_three = last_three[FEATURES]
last_three.to_csv(os.path.join(directory, 'last_x_data.csv'), index=False)

df = df.dropna()

X = df[FEATURES]
y = df[TARGET]

poly = PolynomialFeatures(degree=2)  # Adjust the degree as needed
X_poly = poly.fit_transform(X)

# Feature scaling - Normalize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_poly)

# Split the data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

param_grid = {'alpha': [0.1, 1.0, 10.0, 100.0]}  # Range of alpha values
ridge_model = Ridge()

grid_search = GridSearchCV(ridge_model, param_grid, cv=5, scoring='neg_mean_absolute_error')  # Using MAE as scoring metric
grid_search.fit(X_train, y_train)

# Best model based on GridSearchCV
best_ridge_model = grid_search.best_estimator_

# Step 6: Model Evaluation
# Evaluate the model on the test data
y_pred_test = best_ridge_model.predict(X_test)

# Step 7: Cross-validation (optional, for better model evaluation)
cv_scores = cross_val_score(best_ridge_model, X, y, cv=5, scoring='neg_mean_absolute_error')
print(f"Cross-validated MAE: {-cv_scores.mean():.2f}")


# Step 8: Plot Actual vs Predicted Values
plt.figure(figsize=(12, 6))
plt.plot(y_test.values, label="Actual Flu Cases", color="blue", alpha=0.6)
plt.plot(y_pred_test, label="Predicted Flu Cases", color="red", linestyle="--", alpha=0.6)
plt.title("Actual vs Predicted Flu Cases")
plt.xlabel("3 Weeks Ahead")
plt.ylabel("Number of Flu Cases")
plt.legend()
plt.grid(True)
plt.show()

# # Step 9: Display Model Coefficients (optional, to understand the influence of each feature)
# print(f"Best Alpha (regularization strength): {grid_search.best_params_['alpha']}")
# print("Model Coefficients:", best_ridge_model.coef_)


# # Define the directory where you want to save the model
# directory = '/Users/katieengel/Library/CloudStorage/OneDrive-Personal/Documents/Programming/OutbreakVision/Google Trends Data/models'

# # Check if the directory exists, if not create it
# if not os.path.exists(directory):
#     os.makedirs(directory)

# # Save the features (X) and target (y) as CSV files
# X.to_csv(os.path.join(directory, 'X_data.csv'), index=False)
# y.to_csv(os.path.join(directory, 'y_data.csv'), index=False)

# Save the model to the specified directory
with open(os.path.join(directory, 'flu_model.pkl'), 'wb') as model_file:
    joblib.dump(best_ridge_model, model_file)

print(f'Model and data saved to {directory}')
# Define the file path for saving the model
file_path = os.path.join(directory, 'flu_model.pkl')

# Save the model to the specified directory
joblib.dump(best_ridge_model, file_path)


