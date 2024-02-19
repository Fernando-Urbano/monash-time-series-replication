import requests
import zipfile
import os
import shutil
from io import BytesIO

def download_and_extract_zip(url, destination_dir):
    # Send a GET request to the URL
    response = requests.get(url)
    # Raise an exception for bad status codes
    response.raise_for_status()
    
    # Extract the content of the zip file into memory
    with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
        # List the contents of the zip file
        file_list = zip_file.namelist()
        # Extract the first file from the zip file (you can modify this as needed)
        first_file_name = file_list[0]
        # Extract the file to a temporary directory
        zip_file.extract(first_file_name, destination_dir)
    
    # Construct the path to the extracted file
    extracted_file_path = os.path.join(destination_dir, first_file_name)
    
    return extracted_file_path


if __name__ == '__main__':
    # Example usage
    url = "https://zenodo.org/records/4656080/files/kaggle_web_traffic_dataset_with_missing_values.zip?download=1"

    # Get the absolute path of the current directory
    current_dir = os.path.abspath(os.getcwd())

    # Construct the destination directory path
    destination_dir = os.path.abspath(os.path.join(current_dir, 'data'))
    # Ensure destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    extracted_file_path = download_and_extract_zip(url, destination_dir)