import pandas as pd
import os
from pathlib import Path
import shutil

def combine_csv_files(input_directory, output_file):
    # List to hold dataframes
    dataframes = []

    # Iterate over all CSV files in the input directory
    for csv_file in Path(input_directory).glob('*.csv'):
        # Read each CSV file into a dataframe
        df = pd.read_csv(csv_file)
        # Append the dataframe to the list
        dataframes.append(df)

    # Concatenate all dataframes in the list into a single dataframe
    combined_df = pd.concat(dataframes, ignore_index=True)

    combined_df = combined_df.sort_values(by=['YEAR', 'WEEK'])

    combined_df['TOTAL'] = combined_df.drop(columns=['YEAR', 'WEEK', 'TOTAL SPECIMENS']).sum(axis=1)

    combined_df['PERCENT POSITIVE'] = combined_df['TOTAL'] / combined_df['TOTAL SPECIMENS']
    
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

virus = 'flu'
country = 'united_states'

input_directory = f'/Users/katieengel/Library/CloudStorage/OneDrive-Personal/Documents/Programming/OutbreakVision/Google Trends Data/{virus}_{country}_val_data'
output_file = f'/Users/katieengel/Library/CloudStorage/OneDrive-Personal/Documents/Programming/OutbreakVision/Google Trends Data/validation_data/{virus}/{virus}_{country}_val_data.csv'
combine_csv_files(input_directory, output_file)

delete_folder(input_directory)

# Example usage
file_path = '/Users/katieengel/Downloads/FluView_StackedColumnChart_Data.csv'
delete_file(file_path)
for i in range(1, 6):
    file_path = f'/Users/katieengel/Downloads/FluView_StackedColumnChart_Data ({i}).csv'
    delete_file(file_path)



