import os

def create_country_folder(country_name, base_directory):
    # Create the full path for the new folder
    raw_data_folder = virus_name + '_' + country_name + '_raw_data'
    raw_data_folder_path = os.path.join(base_directory, raw_data_folder)

    val_data_folder = virus_name + '_' + country_name + '_val_data'
    val_data_folder_path = os.path.join(base_directory, val_data_folder)
    
    # Create the new folder if it doesn't exist
    os.makedirs(raw_data_folder_path, exist_ok=True)
    print(f"Folder created at: {raw_data_folder_path}")
    os.makedirs(val_data_folder_path, exist_ok=True)
    print(f"Folder created at: {val_data_folder_path}")
    
    

# Example usage
virus_name = 'covid'
country_name = 'united_states'
base_directory = '/Users/katieengel/Library/CloudStorage/OneDrive-Personal/Documents/Programming/OutbreakVision/Google Trends Data'
create_country_folder(country_name, base_directory)