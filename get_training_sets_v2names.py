# Input: set of links to G Folders with prepared training images
    # Book2_name.csv
# Output: folders with images on server
# Overview:
# 1. dict of {id : [link, name]}
# 2. dict of {id : ID}
# 3. Count &
#   3.1. create a folder one by one
#   3.2. download to the folder
# report

import csv
import re
import os

#===================1. dict of {id : link}

csv_file = 'Book2_name.csv'

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
        if len(row) >= 3:
            id_value, link_value, name_value = row[0], row[1], row[2]
            links_dict[id_value] = [link_value, name_value]

print(links_dict)

count = 0
# Print the list of vector data
for key, value in links_dict.items():
    count = count+1
    print(f"ID: {key}, link: {value[0]}, name: {value[1]}")

print("1. successfully listed", count, "characters")

#===================2. dict of {id : ID}
# Extract file ID for gdrive
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
    id, g_id, name = key, extract_id(value[0]), value[1]
    id_dict[id] = [g_id, name]
    count = count+1

print (id_dict)
print("2. successfully extracted", count, "IDs")

#===================3. Folders & Downloads
# prepares command to make a directory with id as the name
def make_dir(id, name):
    command = "mkdir /workspace/train_img/"+id+'_'+name
    return command

# prepares a name of directory
def dir(id, name):
    command = "/workspace/train_img/"+id+'_'+name
    return command

# prepares command for download
def gdrive(g_id, fold_dir):
    command = "gdrive files download --recursive "+g_id+" --destination "+fold_dir
    return command

# test the commands
print ("=====Commands to be executed:")
for key, value in id_dict.items():
    print(make_dir(key, value[1]))
    print(gdrive(value[0], dir(key, value[1])))

# Creates parent's directory
os.system("mkdir /workspace/train_img/")

# Run the commands
for key, value in id_dict.items():
    os.system(make_dir(key, value[1]))
    os.system(gdrive(value[0], dir(key, value[1])))
    print(f"Training images for {key}_{value[1]} successfully downloaded")
