# Input
    # gender and faction from prompt_log.json 
    # 5 csv files (rus.csv', 'ukr.csv',...) in Stable Dif Folder
    # loras in Book2_name.csv and faction
    # JSON payloads in Folder
        # if woman: fem_json
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

# Function to extract filename from JSON files
def extract_filename(input_string):
    start = input_string.rfind('/') + 1
    end = input_string.rfind('.json')
    return input_string[start:end]

# Read "prompt_log.json" and assign gender and faction vars
prompt_log_path = '/workspace/Stable-Diffusion/prompt_log.json'

try:
    with open(prompt_log_path, 'r') as json_file:
        prompt_log_dict = json.load(json_file)
except FileNotFoundError:
    print("Error: 'prompt_log.json' not found. Please run the initial setup.")
    exit(1)

# Assign gender and faction vars
gender = prompt_log_dict.get('gender')
faction = prompt_log_dict.get('faction')

# Map faction to the list of jsons
faction_to_csv = {
    'r': 'rus.csv',
    'u': 'ukr.csv',
    'n': 'ntr.csv',
    'g': 'good_rus.csv',
    'c': 'cor_ukr.csv',
}

csvfaction = faction_to_csv[faction]

# Read the CSV file and populate the list of JSONs: jsons_list
with open(csvfaction, newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    jsons_list = [row[0] for row in csvreader]

jsons_dir = '/workspace/Stable-Diffusion/jsons/PayLoads'

# ============1.2. Lora's list

# lora_path = '/workspace/stable-diffusion-webui/models/Lora/model/'

csv_file = 'Book2_name.csv'

lora_dict = {}

# Open the CSV file for reading
with open(csv_file, 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)

    for row in csv_reader:
        # Convert the row of data into a list of values
        char_id, char_name = row[0], row[2]
        lora_name = char_id+'_'+char_name
        lora_dict[char_id] = lora_name

print ('lora_dict from Book2name.csv is', lora_dict)

#==========2. Generate Images
output_dir = '/workspace/Stable-Diffusion/images/'

# Create a directory for each lora_name
for lora_name in lora_dict.values():
    lora_output_dir = os.path.join(output_dir, lora_name)
    os.makedirs(lora_output_dir, exist_ok=True)

count = 0

for char_id, lora_name in lora_dict.items():
    for json_file in jsons_list:
        # Construct the full path to the JSON file
        json_file_path = os.path.join(jsons_dir, json_file)

        # Assign a name to json file
        json_name = extract_filename(json_file)

        # Load the JSON data from the file
        with open(json_file_path, 'r') as json_file:
            payload = json.load(json_file)

        # =============Modify the JSON: 
        # 1st: Replace the lora_name
        payload["alwayson_scripts"]["ADetailer"]["args"][1]["ad_prompt"] = payload["alwayson_scripts"]["ADetailer"]["args"][1]["ad_prompt"].replace("lora_name", lora_name)
        payload["prompt"] = payload["prompt"].replace("lora_name", lora_name)

        # 2nd: Replace the gender
        if gender == "f":
            payload["alwayson_scripts"]["ADetailer"]["args"][1]["ad_prompt"] = payload["alwayson_scripts"]["ADetailer"]["args"][1]["ad_prompt"].replace("man", "woman")
            payload["prompt"] = payload["prompt"].replace("man", "woman")

        # 3rd: Modify the JSON weights
        deltas = [0, 0.4, -0.4]
        for delta in deltas:
            mod_payload = update_weights_in_json(payload, delta)

            # Convert the modified dictionary back to JSON
            payload_json = json.dumps(mod_payload, indent=4)
            print('payload_json', payload_json)

            # Send the JSON payload to the API
            response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=json.loads(payload_json))

            # Process the API response
            response_data = response.json()
            # print('response/n',response_data)

            for i, img_base64 in enumerate(response_data['images']):
                image = Image.open(io.BytesIO(base64.b64decode(img_base64.split(",", 1)[0])))

                # Generate a unique image name
                unique_id = str(uuid.uuid4())[:14]
                # img_name = f'{unique_id}_{lora_name}.png'
                img_name = f'{unique_id}_{lora_name}_{json_name}.png'
                print('im_name', img_name)

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
