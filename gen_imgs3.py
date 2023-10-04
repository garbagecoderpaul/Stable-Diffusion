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
from PIL import Image, PngImagePlugin

url = "http://127.0.0.1:3000"

#===========1. Prep variables

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
count = 0

for char_id, lora_name in char2lora_dict.items():
    for json_file in jsons_list:
        # Construct the full path to the JSON file
        json_file_path = os.path.join(jsons_dir, json_file)

        # Load the JSON data from the file
        with open(json_file_path, 'r') as json_file:
            payload = json.load(json_file)

        # Modify the JSON with the lora_name
        payload["alwayson_scripts"]["ADetailer"]["args"][1]["ad_prompt"] = payload["alwayson_scripts"]["ADetailer"]["args"][1]["ad_prompt"].replace("lora_name", lora_name)
        payload["prompt"] = payload["prompt"].replace("lora_name", lora_name)

        # Convert the modified dictionary back to JSON
        payload_json = json.dumps(payload, indent=4)
        # print('payload:/n',payload_json)

        # Send the JSON payload to the API
        response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=json.loads(payload_json))

        # Process the API response
        response_data = response.json()
        # print('response/n',response_data)

        for i, img_base64 in enumerate(response_data['images']):
            image = Image.open(io.BytesIO(base64.b64decode(img_base64.split(",", 1)[0])))

            # Save the image with appropriate metadata
            img_name = f'output{count + i}.png'
            image.save(os.path.join(output_dir, img_name))
            print(f'Image {img_name} saved')

        count += len(response_data['images'])

print(f"All {count} images have been created and saved.")
