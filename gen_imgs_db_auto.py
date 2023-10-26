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
import subprocess

start_time = time.time()

url = "http://127.0.0.1:3000"

code_version = 'v.2.2'


#===========1.0 Functions

#  Function to update the JSON with modified weights
def update_weights_in_json(json_data, weight_delta):
    # Define a regular expression pattern to match weight values like (ohwx:1.5)
    pattern = r'\(ohwx\s*:\s*([0-9.]+)\)'

    # Convert the JSON data to a string
    json_str = json.dumps(json_data)

    # Find all matches of the pattern in the string
    matches = re.findall(pattern, json_str)

    # Convert the matched values to floats, add 0.5 to each, and store them in a list
    modified_values = [str(float(x) + weight_delta) for x in matches]

    # Replace the original values with the modified values in the input string
    output_string = re.sub(pattern, lambda x: f'(ohwx:{modified_values.pop(0)})', json_str)

    # Convert the modified JSON string back to a dictionary
    modified_json_data = json.loads(output_string)
    # print('modified_json_data', modified_json_data)

    # Debug function
    print('44444444444444====Start Function debugging')
    # print('original JSON:', json_data)
    # print('matches', matches)
    print('modified_values', modified_values)
    # print('output_string', output_string)
    # print('modified JSON:', modified_json_data)
    print('555555555555555====Finish Function debugging')

    return modified_json_data

# Function to extract filename from JSON files
def extract_filename(input_string):
    start = input_string.rfind('/') + 1
    end = input_string.rfind('.json')
    return input_string[start:end]

# Function to refresh the checkpoints
def refresh_checkpoints(url):
    response = requests.get(url=f'{url}/sdapi/v1/refresh-checkpoints')

# Function to show the current checkpoint and VAE
def show_ckpt_vae(url):
    response = requests.get(url=f'{url}/sdapi/v1/options')
    options_json = response.json()
    ckpt = options_json['sd_model_checkpoint']
    vae = options_json['sd_vae']
    print(f'Current ckpt {ckpt}, VAE {vae}')

def setup_ckpt (options_json, url, model_title):
    options_json['sd_vae'] = 'sdxl_vae.safetensors'
    options_json['sd_model_checkpoint'] = model_title
    print ('modified JSON is \n', 
           options_json['sd_model_checkpoint'], 
           options_json['sd_vae'])
    # Send the JSON payload to the API to change the ckpt
    response = requests.post(url=f'{url}/sdapi/v1/options', json=options_json)
    print('POST response', response)
    # Refresh ckpt and show updated ckpt
    response = requests.get(url=f'{url}/sdapi/v1/refresh-checkpoints')
    print('refreshed', response)
    response = requests.get(url=f'{url}/sdapi/v1/options')
    options_json = response.json()
    print('updated current ckpt', options_json['sd_model_checkpoint'])

# Function to create a filtered dictionary with checkpoints
def request_and_filter_checkpoints(url, substrings_to_remove):
    response = requests.get(url=f'{url}/sdapi/v1/sd-models')
    response_json = response.json()
    # Original list (dict) of ckpt's
    orig_ckpt_dict = {}
    for item in response_json:
        model_title = item['title']
        lora_name = item['model_name']
        orig_ckpt_dict[lora_name] = model_title
    # Filtered list: Removed standard SDXL's
    filtered_ckpt_dict = {lora_name: model_title for lora_name, model_title in orig_ckpt_dict.items() if all(sub not in model_title for sub in substrings_to_remove)}
    return filtered_ckpt_dict

# Function to create img directories related to model
def create_model_img_directories(output_dir, ckpt_name):
    model_output_dir = os.path.join(output_dir, ckpt_name)
    os.makedirs(model_output_dir, exist_ok=True)
    print('Directory created', model_output_dir)

def create_meta_json(ckpt_name, payload, img_name, img_path, code_version):
    # Create a dictionary with 'ckpt_name' and 'payload' keys
    meta_data = {
        'code_version': code_version,
        'ckpt': ckpt_name,
        'payload': payload,
    }
    # Convert the dictionary to a JSON string
    meta_json = json.dumps(meta_data, indent=4)
    # Extract the directory from the img_path
    directory = os.path.dirname(img_path)
    # Define the filename for the JSON file (same as img_name)
    json_filename = os.path.join(directory, f"{img_name}.json")
    # Write the JSON string to the JSON file
    with open(json_filename, 'w') as json_file:
        json_file.write(meta_json)
    print(f"Meta JSON file '{json_filename}' created.")

#==== 1.1 Gender and Faction vars from "prompt_log.json" & assign the right JSONs
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

jsons_dir = '/workspace/Stable-Diffusion/jsons'

# Get the latest sample of Options JSON  for API
response_options = requests.get(url=f'{url}/sdapi/v1/options')
options_json = response_options.json()
print (response_options)

# ============1.2. Character's table: char_id | link | char_name | kw_list
csv_file = 'Book2_name.csv'

# Create char_dict = char_id: [ckpt_name, kw_list]; ckpt_name = 'char_id'_'char_name'.safetensors
char_dict = {}
with open(csv_file, 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    for row in csv_reader:
        # Convert the row of data into a list of values
        char_id, char_name = row[0], row[2] 
        # Check if the row has a fourth element
        kw_list = row[3] if len(row) > 3 else ''  # Default value is an empty string
        ckpt_name = char_id+'_'+char_name + '.safetensors'
        char_dict[char_id] = [ckpt_name, kw_list]

print ('char_dict from Book2name.csv is', char_dict)

# ============1.1. prep ckpt
#===== 1.1.2. Refresh ckpt and show
refresh_checkpoints(url)
show_ckpt_vae(url)

# =====1.1.3. Request, Filter & Create Dictionary filtered_ckpt_dict[lora_name]=model_title
substrings_to_remove = ["sd_xl_base_1.0.safetensors", "sd_xl_refiner_1.0.safetensors"]
filtered_ckpt_dict = request_and_filter_checkpoints(url, substrings_to_remove)
print('filtered_ckpt_dict is', filtered_ckpt_dict)

#==========2. Generate Images: # Ensure model_name == ckpt_name
# # 2.1.a. Create a directory for each ckpt_name from the models Folder
# output_dir = '/workspace/Stable-Diffusion/images/'
# for ckpt_name in filtered_ckpt_dict.keys():
#     create_model_img_directories(output_dir, ckpt_name)

# 2.1.b Create a directory for each ckpt_name
output_dir = '/workspace/Stable-Diffusion/images/'
for ckpt_name in list(char_dict.values())[0]:
    create_model_img_directories(output_dir, ckpt_name)

#========== 2.2. Gen img's
count = 0
for value in char_dict.values():
    ckpt_name, kw_list = value[0], value[1]
    # 2.2.1.===== setup ckpt & VAE
    setup_ckpt (options_json, url, ckpt_name)

    # 2.2.2.====== for each JSON: 
    for json_file in jsons_list:
        # Construct the full path to the JSON file
        json_file_path = os.path.join(jsons_dir, json_file)

        # Assign a name to json file
        json_name = extract_filename(json_file)

        # Load the JSON data from the file
        with open(json_file_path, 'r') as json_file:
            payload = json.load(json_file)

        # =============Modify the JSON: 
        # 1st: Remove the lora_name from the prompt
        payload["alwayson_scripts"]["ADetailer"]["args"][1]["ad_prompt"] = payload["alwayson_scripts"]["ADetailer"]["args"][1]["ad_prompt"].replace("<lora:lora_name:1>", '')
        payload["prompt"] = payload["prompt"].replace("<lora:lora_name:1>", '')

        # Add keywords
        payload["alwayson_scripts"]["ADetailer"]["args"][1]["ad_prompt"] = payload["alwayson_scripts"]["ADetailer"]["args"][1]["ad_prompt"] + ', ' + kw_list
        payload["prompt"] = payload["prompt"] + ', ' + kw_list

        # 2nd: Replace the gender
        if gender == "f":
            payload["alwayson_scripts"]["ADetailer"]["args"][1]["ad_prompt"] = payload["alwayson_scripts"]["ADetailer"]["args"][1]["ad_prompt"].replace("man", "woman")
            payload["prompt"] = payload["prompt"].replace("man", "woman")

        # 3rd: Modify the JSON weights
        deltas = [0, 0.3, -0.3]
        for delta in deltas:
            mod_payload = update_weights_in_json(payload, delta)
            mod_prompt = mod_payload['prompt']

            # Convert the modified dictionary back to JSON
            payload_json = json.dumps(mod_payload, indent=4)

            print('6666666666666666======mod_prompt', mod_prompt)
            print('payload_json', payload_json)

            # Send the JSON payload to the API
            response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=json.loads(payload_json))

            # Process the API response
            response_data = response.json()

            for i, img_base64 in enumerate(response_data['images']):
                image = Image.open(io.BytesIO(base64.b64decode(img_base64.split(",", 1)[0])))

                # Generate a unique image name
                unique_id = str(uuid.uuid4())[:14]
                # img_name = f'{unique_id}_{lora_name}.png'
                img_name = f'{unique_id}_{ckpt_name}_{json_name}.png'
                print('im_name', img_name)

                # Save the image with appropriate metadata in the lora's directory
                img_path = os.path.join(output_dir, ckpt_name, img_name)
                image.save(img_path)
                print(f'Image {img_name} saved')

                print('77777777777777777======mod_prompt', mod_prompt)

                # Write meta data
                create_meta_json(ckpt_name, mod_payload, img_name, img_path, code_version)

            count += len(response_data['images'])

print(f"All {count} images have been created and saved.")

# Record the end time
end_time = time.time()

# Calculate and print the execution time
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")

# Write logs
log_file = 'DB_gen_img_log.txt'
with open('DB_gen_img_log.txt', 'w') as log:
    log.write(f"All {count} images have been created and saved.\n")
    log.write(f"Execution time: {execution_time:.2f} seconds\n")
