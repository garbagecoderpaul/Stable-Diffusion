# Overview
#Inputs: characters.txt

# Gender sensitive
# 1. Reads characters.txt and creates a list of CharatersIDs
# 2. create folders
# 3. move regular images
# 4. For each ch_id:
#   0. prep commands
#   1. empty destin train folder
#   2. move train images
#   3. run the acceleration command
#   4. upload loras to G Folder
# 3. Reports done and time for execution

gender = 2

import os
import shutil
import subprocess
import time

#============ 0. Setting up global vars
start_time = time.time()

#addresses
train_dest_men = '/workspace/stable-diffusion-webui/models/Lora/img/25_ohwx man'
train_dest_women = '/workspace/stable-diffusion-webui/models/Lora/img/25_ohwx woman'
reg_source_men = '/workspace/regimages/1024x1024_2734_imgs'
reg_source_women = '/workspace/regimages/woman_3786_imgs_1024x1024px'
reg_dest_men = '/workspace/stable-diffusion-webui/models/Lora/reg/1_man'
reg_dest_women = '/workspace/stable-diffusion-webui/models/Lora/reg/1_woman'

if gender == 1:
    train_dest = train_dest_men
    reg_source = reg_source_men
    reg_dest = reg_dest_men
else:
    train_dest = train_dest_women
    reg_source = reg_source_women
    reg_dest = reg_dest_women

# Function for preparation of Accelerate command
def accel_command(char_id):
    original_string = '''accelerate launch --num_cpu_threads_per_process=2 "/workspace/kohya_ss/sdxl_train_network.py" --pretrained_model_name_or_path="/workspace/stable-diffusion-webui/models/Stable-diffusion/sd_xl_base_1.0.safetensors" --train_data_dir="/workspace/stable-diffusion-webui/models/Lora/img" --reg_data_dir="/workspace/stable-diffusion-webui/models/Lora/reg" --resolution="1024,1024" --output_dir="/workspace/stable-diffusion-webui/models/Lora/model" --logging_dir="/workspace/stable-diffusion-webui/models/Lora/log" --network_alpha="1" --save_model_as=safetensors --network_module=networks.lora --text_encoder_lr=0.0004 --unet_lr=0.0004 --network_dim=32 --output_name="88_stolten" --lr_scheduler_num_cycles="1" --no_half_vae --learning_rate="0.0004" --lr_scheduler="constant" --train_batch_size="1" --max_train_steps="700" --save_every_n_epochs="1" --mixed_precision="bf16" --save_precision="bf16" --cache_latents --cache_latents_to_disk --optimizer_type="Adafactor" --optimizer_args scale_parameter=False relative_step=False warmup_init=False --max_data_loader_n_workers="0" --bucket_reso_steps=64 --gradient_checkpointing --xformers --bucket_no_upscale --noise_offset=0.0'''
    # Define replacement values
    replacement_values = {
        '88_stolten': char_id+'_name'
    }
    # Perform replacements
    for old_value, new_value in replacement_values.items():
        mod_string = original_string.replace(old_value, new_value)
    return mod_string


#=============1. counts and creates a list of Char IDs

# Specify the file path
file_path = 'characters.txt'

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

# Print the list of values
count = 0
for item in char_list:
    print("Prep command for ",item)
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
for ch_id in char_list:
    #=============4.a empty destin train folder
    if os.path.exists(train_dest):
        shutil.rmtree(train_dest)  # Clear the train folder

    #=============4.b move train images
    #workspace/train_img/2/train
    train_source = '/workspace/train_img/'+ ch_id + '/train'
    shutil.copytree(train_source, train_dest)  # Copy train images
    print('4b: copied training images to destin folder')

    #============4.c run the acceleration command:
    command = accel_command(ch_id)
    print("Performing Accel Command:", command)
    os.system(command)

    #============4.d upload loras to G Folder
#   gdrive files upload --parent 1mB3koZyL35ZSgqrbcOmjVTYgt9XbGbD6 <FILENAME>
    gd_str = 'gdrive files upload --parent 1mB3koZyL35ZSgqrbcOmjVTYgt9XbGbD6 '
    output_dir = '/workspace/stable-diffusion-webui/models/Lora/model/'
    fname = ch_id + '_name.safetensors'
    upl_command = gd_str+output_dir+fname
    # run
    print('4.d: Uploading:', upl_command)
    os.system(upl_command)

    #==========4.e report
    count = count + 1
    print('===For '+ch_id+'done'+' Count =', count)

# Record the end time
end_time = time.time()

# Calculate and print the execution time
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")
