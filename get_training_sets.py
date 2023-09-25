# Input: set of links to G Folders with prepared training images
    # Book1.csv
# Output: folders with images on server
# Overview:
# 1. dict of {id : link}
# 2. dict of {id : ID}
# 3. Count &
#   3.1. create a folder one by one
#   3.2. download to the folder
# report

import csv
import re
import os

#===================1. dict of {id : link}
# Replace 'your_file.csv' with the actual CSV file path
csv_file = 'Book1.csv'

# Initialize an empty dictionary to store the data
links_dict = {}

# Open the CSV file for reading
with open(csv_file, 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)

    # Assuming your CSV file has a single row with values separated by commas
    # If your CSV file has multiple rows or different delimiters, you may need to adjust this logic
    for row in csv_reader:
        # Convert the row of data into a list of values
        if len(row) >= 2:
            id_value, link_value = row[0], row[1]
            links_dict[id_value] = link_value

print(links_dict)

count = 0
# Print the list of vector data
for key, value in links_dict.items():
    count = count+1
    print(f"ID: {key}, link: {value}")

print("1. successfully listed", count, "links")

#===================2. dict of {id : ID}
# Extract file ID
def extract_id(string):
    pattern = r'/folders/([A-Za-z0-9_-]+)'
    match = re.search(pattern, string)
    if match:
        # Extract the desired part (group 1)
        extracted_part = match.group(1)
        print(extracted_part)
        return extracted_part
    else:
        print("No match found")
        return None

count = 0
id_dict = {}
for key, value in links_dict.items():
    id, g_id = key, extract_id(value)
    id_dict[id] = g_id
    count = count+1

print (id_dict)
print("2. successfully extracted", count, "IDs")

#===================3. Folders & Downloads
# prepares command to make a directory with id as the name
def make_dir(id):
    command = "mkdir /workspace/train_img/"+id
    return command

# prepares a name of directory
def dir(id):
    command = "/workspace/train_img/"+id
    return command

# prepares command for download
def gdrive(g_id, fold_dir):
    command = "gdrive files download --recursive "+g_id+" --destination "+fold_dir
    return command

# test the commands
print ("testing commands")
for key, value in id_dict.items():
    print(make_dir(key))
    print(gdrive(value, dir(key)))

# Creates parent's directory
os.system("mkdir /workspace/train_img/")

# Run the commands
for key, value in id_dict.items():
    os.system(make_dir(key))
    os.system(gdrive(value, dir(key)))
    print(f"Training images for {key} successfully downloaded")
