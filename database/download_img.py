import os
import csv
import json
import re

#=====================1. Prepare command

def extract_folder_id(input_string):
    # Define a regular expression pattern to match the desired part
    pattern = r"drive/folders/([^?]+)"

    # Use re.search to find the match in the input string
    match = re.search(pattern, input_string)

    # Check if a match is found
    if match:
        # Extract the desired part (group 1)
        folder_id = match.group(1)
        return folder_id
    else:
        return None
        print("FILEID not found.")

def substitute_parameters(input_string, folder_id):
    # Use regular expressions to find and substitute FILEID and FILENAME
    input_string = re.sub(r'FILEID', folder_id, input_string)

    return input_string

def prepare_gdrive_command(folderlink, input_string):
    # Extract FILEID from the provided Google Drive file link
    folder_id = extract_folder_id(folderlink)
    print('folder_id:', folder_id)

    if folder_id is None:
        return None

    # Substitute placeholders in the input string
    modified_command = substitute_parameters(input_string, folder_id)

    return modified_command

#=====================2. Read folder links from CSV

csv_file_path = 'folders_list.csv'

# Input string with placeholders
input_string = "gdrive files download --recursive FILEID --destination /workspace/images"

# Create a list to store folder links
folder_links = []

# Read folder links from the CSV file
with open(csv_file_path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row:
            # Assuming each row contains a single folder link
            folder_links.append(row[0])

#=====================3. Download files for each folder link

for gdrive_folder_link in folder_links:
    # Prepare the GDrive command for the current folder link
    gdrive_command = prepare_gdrive_command(gdrive_folder_link, input_string)
    print('gdrive_command:', gdrive_command)

    download_dir = '/workspace/images'
    os.makedirs(download_dir, exist_ok=True)
    
    if gdrive_command:
        # Execute the GDrive command to download files
        os.system(gdrive_command)

    print(f"Images from {gdrive_folder_link} have been added to {download_dir}")
