import subprocess
import re
import csv
import os

# function
def extract_fileid(input_string):
    pattern = r"/d/([^/]+)/"
    match = re.search(pattern, input_string)
    if match:
        fileid = match.group(1)
        return fileid
    else:
        return None
        print("FILEID not found.")

# prep command
def prep_command(file_id):
    command = 'gdrive files download ' + file_id + ' --destination /workspace/stable-diffusion-webui/models/Stable-diffusion/model'
    return command

# Check if directory exists, if not, create it
directory = '/workspace/stable-diffusion-webui/models/Stable-diffusion/model'
if not os.path.exists(directory):
    os.makedirs(directory)

# Prep a list of model's file_id list
file_id_list = []

# Reading the CSV file and segregating by extension
with open('gen.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for item in reader:
        url = item[0]
        file_id = extract_fileid(url)
        file_id_list.append(file_id)

# Run the gdrive command using subprocess and capture the output
for item in file_id_list:
    command = prep_command(item)
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    print(result.stdout)
