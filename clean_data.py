import pandas as pd
import os

virus = 'covid'
country = 'united_states'

keyword_df = pd.read_csv(f"/Users/katieengel/Library/CloudStorage/OneDrive-Personal/Documents/Programming/OutbreakVision/Google Trends Data/keyword_data/{virus}/{virus}_{country}.csv")

keyword_df = keyword_df.dropna()
print(keyword_df.head())
# Convert to datetime format

# # Extract Year & Week Number
# keyword_df["YEAR"] = keyword_df["Week"].dt.year
# keyword_df["WEEK"] = keyword_df["Week"].dt.isocalendar().week

# Load the Flu Cases data (formatted by YEAR & WEEK)
val_df = pd.read_csv(f"/Users/katieengel/Library/CloudStorage/OneDrive-Personal/Documents/Programming/OutbreakVision/Google Trends Data/validation_data/{virus}/{virus}_{country}_val_data.csv")

val_df.rename(columns={'Date_reported': 'Week'}, inplace=True)
val_df = val_df.dropna()
print(val_df.head())

# Merge on "YEAR" and "WEEK"
merged_df = pd.merge(keyword_df, val_df, on=["Week"], how="inner")

column_order = ["Week"] + [col for col in merged_df.columns if col not in ["Week"]]
merged_df = merged_df[column_order]


clean_data_directory = f'/Users/katieengel/Library/CloudStorage/OneDrive-Personal/Documents/Programming/OutbreakVision/Google Trends Data/clean_data/{virus}'

os.makedirs(clean_data_directory, exist_ok=True)

# Save the merged dataset in the base_directory
output_file_path = os.path.join(clean_data_directory, f"{virus}_{country}_clean_data.csv")
merged_df.to_csv(output_file_path, index=False)
# Save the merged dataset
merged_df.to_csv(f"{virus}_{country}_clean_data.csv", index=False)

print("✅ Data successfully merged! Preview:")
print(merged_df.head())