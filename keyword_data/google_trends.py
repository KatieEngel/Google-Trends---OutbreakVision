import pandas as pd
import os
from pathlib import Path
import shutil

def combine_csv_files(input_directory, output_file):
    # Initialize an empty DataFrame for the combined data
    combined_df = pd.DataFrame()

    # Iterate over all CSV files in the input directory
    for csv_file in Path(input_directory).glob('*.csv'):
        # Read each CSV file into a dataframe
        df = pd.read_csv(csv_file, skiprows=2)
        
        # Extract the keyword and country from the column name
        oldcol = df.columns[1]
        keyword, country = oldcol.split(': ')
        country = country.strip('()')
        
        # Rename the column to the keyword
        df = df.rename(columns={oldcol: keyword})
        
        # Merge the dataframes on 'YEAR' and 'WEEK' columns
        if combined_df.empty:
            combined_df = df
        else:
            combined_df = pd.merge(combined_df, df[['Week', keyword]], on=['Week'], how='outer')

    # Sort the combined dataframe by 'YEAR' and 'WEEK' columns
    combined_df = combined_df.sort_values(by=['Week'])

    # Save the combined dataframe to a new CSV file
    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV saved to: {output_file}")

def delete_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Remove the folder and all its contents
        shutil.rmtree(folder_path)
        print(f"Folder deleted: {folder_path}")
    else:
        print(f"Folder does not exist: {folder_path}")

def delete_file(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        # Remove the file
        os.remove(file_path)
        print(f"File deleted: {file_path}")
    else:
        print(f"File does not exist: {file_path}")

# Example usage
virus = 'covid'
country = 'united_states'

input_directory = f'/Users/katieengel/Library/CloudStorage/OneDrive-Personal/Documents/Programming/OutbreakVision/Google Trends Data/{virus}_{country}_raw_data'
output_file = f'/Users/katieengel/Library/CloudStorage/OneDrive-Personal/Documents/Programming/OutbreakVision/Google Trends Data/keyword_data/{virus}/{virus}_{country}.csv'
combine_csv_files(input_directory, output_file)

delete_folder(input_directory)

# Example usage
file_path = '/Users/katieengel/Downloads/multiTimeline.csv'
delete_file(file_path)
for i in range(1, 12):
    file_path = f'/Users/katieengel/Downloads/multiTimeline ({i}).csv'
    delete_file(file_path)



