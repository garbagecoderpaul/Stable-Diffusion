import subprocess
import re
import csv

# function
def extract_fileid(input_string):
    # Define a regular expression pattern to match the desired part
    # pattern = r'/folders/([a-zA-Z0-9_-]+)'
    pattern = r"/d/([^/]+)/"

    # Use re.search to find the match in the input string
    match = re.search(pattern, input_string)

    # Check if a match is found
    if match:
        # Extract the desired part (group 1)
        fileid = match.group(1)
        return fileid
    else:
        return None
        print("FILEID not found.")

# prep command
def prep_command(file_id):
    command = 'gdrive files download ' + file_id + ' --destination /workspace/stable-diffusion-webui/models/Stable-diffusion'
    return command

# Prep a list of model's file_id list
file_id_list = []

# Reading the CSV file and segregating by extension
with open('gen.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for item in reader:
        url = item[0]
        print(url)
        file_id = extract_fileid(url)
        file_id_list.append(file_id)
        print('file id is \n',  file_id)

# Run the gdrive command using subprocess and capture the output
for item in file_id_list:
    command = prep_command(item)
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    print(result.stdout)
