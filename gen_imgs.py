# Input
    # char2lora.csv - char_id - loras in csv
    # loras in Folder
    # JSON payloads in Folder
# Output - Gen images

import csv
import os
import json
import requests
import io
import base64
import re
from PIL import Image, PngImagePlugin
import time
import uuid

start_time = time.time()

url = "http://127.0.0.1:3000"

#===========1. Prep variables

#  Function to update the JSON with modified weights
def update_weights_in_json(json_data, weight_delta):
    # Define a regular expression pattern to match weight values like (ohwx:1.5)
    pattern = r'\(ohwx\s*:\s*([0-9.]+)\)'

    # Convert the JSON data to a string
    json_str = json.dumps(json_data)

    # Find all matches of the pattern in the string
    matches = re.findall(pattern, json_str)
    print('matches', matches)

    # Convert the matched values to floats, add 0.5 to each, and store them in a list
    modified_values = [str(float(x) + weight_delta) for x in matches]

    print('modified_values', modified_values)

    # Replace the original values with the modified values in the input string
    output_string = re.sub(pattern, lambda x: f'(ohwx:{modified_values.pop(0)})', json_str)

    # Convert the modified JSON string back to a dictionary
    modified_json_data = json.loads(output_string)
    # print('modified_json_data', modified_json_data)

    return modified_json_data


#========1.1. Create a list of JSONs in the folder
jsons_dir = input("Enter the path to JSONs within the server: ")
# jsons_dir = '/workspace/Stable-Diffusion/jsons/Payloads JSON by Faction/UKR'

# List all JSON files in the directory
jsons_list = os.listdir(jsons_dir)

# Now, jsons_list contains the names of JSON files in the folder
for json_file in jsons_list:
    print('JSONs list:', json_file)

#========1.2. Char_id to Loras mapping
# Create a dictionary to map char_id to lora_name
char2lora_dict = {}

# Read the CSV file and populate the dictionary
with open('char2lora.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)

    for row in csvreader:
        char_id, lora_name = row[0], row[1]
        char2lora_dict[char_id] = lora_name

# Now, char2lora_dict contains the char_id to lora_name mapping
print('Char_id to Loras mapping:', char2lora_dict)

#==========2. Generate Images
output_dir = '/workspace/Stable-Diffusion/images/'

# Create a directory for each lora_name
for lora_name in char2lora_dict.values():
    lora_output_dir = os.path.join(output_dir, lora_name)
    os.makedirs(lora_output_dir, exist_ok=True)

count = 0

for char_id, lora_name in char2lora_dict.items():
    for json_file in jsons_list:
        # Construct the full path to the JSON file
        json_file_path = os.path.join(jsons_dir, json_file)

        # Load the JSON data from the file
        with open(json_file_path, 'r') as json_file:
            payload = json.load(json_file)

        # 1st: Modify the JSON with the lora_name
        payload["alwayson_scripts"]["ADetailer"]["args"][1]["ad_prompt"] = payload["alwayson_scripts"]["ADetailer"]["args"][1]["ad_prompt"].replace("lora_name", lora_name)
        payload["prompt"] = payload["prompt"].replace("lora_name", lora_name)

        # 2nd: Modify the JSON weights
        deltas = [0, 0.4, -0.4]
        for delta in deltas:
            mod_payload = update_weights_in_json(payload, delta)

            # Convert the modified dictionary back to JSON
            payload_json = json.dumps(mod_payload, indent=4)

            # Send the JSON payload to the API
            response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=json.loads(payload_json))

            # Process the API response
            response_data = response.json()
            # print('response/n',response_data)

            for i, img_base64 in enumerate(response_data['images']):
                image = Image.open(io.BytesIO(base64.b64decode(img_base64.split(",", 1)[0])))

                # Generate a unique image name
                unique_id = str(uuid.uuid4())[:12]
                img_name = f'{unique_id}_{lora_name}.png'

                # Save the image with appropriate metadata in the lora's directory
                img_path = os.path.join(output_dir, lora_name, img_name)
                image.save(img_path)
                print(f'Image {img_name} saved')

            count += len(response_data['images'])

print(f"All {count} images have been created and saved.")

# Record the end time
end_time = time.time()

# Calculate and print the execution time
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")
