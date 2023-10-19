# Overview
#Inputs: 
    #characters.txt
    #accelerate.txt

# Gender sensitive
# 1. Reads characters.txt and creates a list of CharatersIDs
# 1a. reads accelerate.txt to get the sample command
# 2. create folders
# 3. move regular images
# 4. For each lora_name:
#   0. prep commands
#   1. empty destin train folder
#   2. move train images
#   3. run the acceleration command
#   4. upload loras to G Folder
# 3. Reports done and time for execution



import os
import shutil
import subprocess
import time
import json

# Set up the gender for training
prompt_log_path = '/workspace/Stable-Diffusion/prompt_log.json'

try:
    with open(prompt_log_path, 'r') as json_file:
        prompt_log = json.load(json_file)
except FileNotFoundError:
    print("Error: 'prompt_log.json' not found. Please run the initial setup.")
    exit(1)

gender = prompt_log.get('gender')

#============ 0. Setting up global vars
start_time = time.time()

#addresses
train_dest_men = '/workspace/stable-diffusion-webui/models/Stable-diffusion/img/40_ohwx man/'
train_dest_women = '/workspace/stable-diffusion-webui/models/Stable-diffusion/img/40_ohwx woman/'
reg_source_men = '/workspace/regimages/1024x1024_2734_imgs'
reg_source_women = '/workspace/regimages/woman_3786_imgs_1024x1024px'
reg_dest_men = '/workspace/stable-diffusion-webui/models/Stable-diffusion/reg/1_man/'
reg_dest_women = '/workspace/stable-diffusion-webui/models/Stable-diffusion/reg/1_woman/'

if gender == 'm':
    train_dest = train_dest_men
    reg_source = reg_source_men
    reg_dest = reg_dest_men
elif gender == 'f':
    train_dest = train_dest_women
    reg_source = reg_source_women
    reg_dest = reg_dest_women
else:
    # Code to execute when the gender is neither 'm' nor 'f'
    print("Error: Gender not found or invalid in 'prompt_log.json'")
    exit(1)

#========== Function for preparation of Accelerate command

# Specify the file path
file_path = "accelerateDB.txt"

# Initialize the variable
accelerate_string = ""

# Read the contents of the file
try:
    with open(file_path, "r") as file:
        accelerate_string = file.read()
except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print("An error occurred:", str(e))

print ('777777 sample string', accelerate_string)

def accel_command(lora_name, original_string):
    # Define replacement values
    replacement_values = {'88_stolten': lora_name}
    # Perform replacements
    for old_value, new_value in replacement_values.items():
        mod_string = original_string.replace(old_value, new_value)
    return mod_string


#=============1. counts and creates a list of Char IDs

# Specify the file path
file_path = '/workspace/Stable-Diffusion/characters.txt'

# Initialize an empty list to store the values
char_list = []

# Open the file for reading
with open(file_path, 'r') as file:
    # Read the lines of the file
    lines = file.readlines()

    # Loop through each line
    for line in lines:
        # Strip leading and trailing whitespace from the line
        line = line.strip()

        # Check if the line is not empty
        if line:
            char_list.append(line)
            current_value = ''  # Reset the current value

print('77777777777 all good, char_list', char_list)

# Print the list of values
count = 0
for item in char_list:
    print("Prep command for",item)
    count = count + 1
print("In Total characters =", count)

#============= 2.Create Destination folders for Reg and Train
os.makedirs(reg_dest, exist_ok=True)
os.makedirs(train_dest, exist_ok=True)

#============= 3. Move Reg once
if os.path.exists(reg_dest):
    shutil.rmtree(reg_dest)  # Clear the destination folder
    shutil.copytree(reg_source, reg_dest)
    print("Reg files moved successfully.")

count = 0
#=============4. For each id:
for lora_name in char_list:
    #=============4.a empty destin train folder
    if os.path.exists(train_dest):
        shutil.rmtree(train_dest)  # Clear the train folder

    #=============4.b move train images
    #workspace/train_img/2/train
    train_source = '/workspace/train_img/'+ lora_name + '/train'
    shutil.copytree(train_source, train_dest)  # Copy train images
    print('4b: copied training images to destin folder')

    #============4.c run the acceleration command:
    command = accel_command(lora_name, accelerate_string)
    print("Performing Accelerate Command:\n", command)
    os.system(command)

#     #============4.d upload models to G Folder
# #   gdrive files upload --parent 1mB3koZyL35ZSgqrbcOmjVTYgt9XbGbD6 <FILENAME>
#     gd_str = 'gdrive files upload --parent 1mB3koZyL35ZSgqrbcOmjVTYgt9XbGbD6 '
#     output_dir = '/workspace/stable-diffusion-webui/models/Lora/model/'
#     fname = lora_name + '.safetensors'
#     upl_command = gd_str+output_dir+fname
#     # run
#     print('4.d: Uploading:', upl_command)
#     os.system(upl_command)

    #==========4.e report
    count = count + 1
    print('===For '+lora_name+'done'+' Count =', count)

# Record the end time
end_time = time.time()

# Calculate and print the execution time
print ('training accomplished and uploaded successfully: 777777777777777')
execution_time = end_time - start_time
print(f"Execution training time: {execution_time:.2f} seconds")

# Write logs
log_file = 'train_loras_log.txt'
with open(log_file, 'w') as log:
    log.write(f"All {count} loras have been trained and saved.\n")
    log.write(f"Execution time: {execution_time:.2f} seconds\n")