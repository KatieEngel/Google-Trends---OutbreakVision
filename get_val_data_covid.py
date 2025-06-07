import pandas as pd

def extract_country_data_by_code(file_path, country_code, output_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Filter the DataFrame to include only rows where the second column matches the country code
    country_data = df[df.iloc[:, 1] == country_code]
    
    # Save the filtered DataFrame to a new CSV file
    country_data.to_csv(output_file_path, index=False)
    
    return country_data

# Example usage
virus = 'covid'
country_code = 'US'
file_path = '/Users/katieengel/Library/CloudStorage/OneDrive-Personal/Documents/Programming/OutbreakVision/Google Trends Data/covid_val_data/WHO-COVID-19-global-daily-data.csv'
output_file_path = f'/Users/katieengel/Library/CloudStorage/OneDrive-Personal/Documents/Programming/OutbreakVision/Google Trends Data/validation_data/{virus}/{virus}_{country_code}_val_data.csv'
country_data = extract_country_data_by_code(file_path, country_code, output_file_path)

print(f"Data for country code {country_code} saved to {output_file_path}")
