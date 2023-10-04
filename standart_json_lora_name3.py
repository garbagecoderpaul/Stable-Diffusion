import os
import json
import glob
import re

# Define the folder path where JSON files are located
folder_path = "/workspace/Stable-Diffusion/jsons/PayLoads"

# Define the pattern to find using regular expression
pattern = r'<lora:\d+[-_]?[a-zA-Z]*\d*:[0-9]+>'

# Define the replacement string
replacement = '<lora:lora_name:1>'

# Initialize counters for replacements and modified JSON files
total_replacements = 0
modified_files = 0

# Function to recursively search and replace values in a JSON object
def recursive_search_and_replace(obj):
    global total_replacements
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str):
                # Use re.sub to find and replace the pattern within strings
                new_value, replacements = re.subn(pattern, replacement, value)
                if replacements > 0:
                    obj[key] = new_value
                    total_replacements += replacements
            elif isinstance(value, (dict, list)):
                recursive_search_and_replace(value)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, str):
                # Use re.sub to find and replace the pattern within strings
                new_item, replacements = re.subn(pattern, replacement, item)
                if replacements > 0:
                    obj[i] = new_item
                    total_replacements += replacements
            elif isinstance(item, (dict, list)):
                recursive_search_and_replace(item)

# List all JSON files in the folder
json_files = glob.glob(os.path.join(folder_path, "*.json"))

# Iterate through the JSON files
for json_file in json_files:
    with open(json_file, "r") as file:
        # Load the JSON data
        data = json.load(file)

    # Apply the search and replace function to the JSON data
    recursive_search_and_replace(data)

    # Write the modified JSON data back to the file
    with open(json_file, "w") as file:
        json.dump(data, file, indent=2)

    modified_files += 1

# Report the number of replacements and modified JSON files
print(f"Total replacements: {total_replacements}")
print(f"Modified JSON files: {modified_files}")
