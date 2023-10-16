import os
import json

# Directory path where your JSON files are located
json_directory = '/workspace/Stable-Diffusion/jsons/Payloads'

# Initialize a counter
removed_count = 0

# Loop through all files in the directory
for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        json_file_path = os.path.join(json_directory, filename)
        
        # Read the JSON file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        
        # Check if "API payload" exists and remove it
        if "API payload" in data["alwayson_scripts"]:
            data["alwayson_scripts"].pop("API payload")
            removed_count += 1
        
        # Write the modified JSON back to the file
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)

        print(f'Removed "API payload" from {filename}')

# Print the count of removed payloads
print(f'Total "API payload" removed from {removed_count} files.')
