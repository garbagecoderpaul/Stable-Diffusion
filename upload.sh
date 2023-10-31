#!/bin/bash

# gdrive
bash gdrive_install.sh

# Start time
start_time=$(date +%s)

# Get the current date and time
current_datetime=$(date +'%Y%m%d')

# Create a folder with the current date and time in /workspace/Stable-Diffusion
mkdir -p "/workspace/Stable-Diffusion/session_$current_datetime"

# Check if the log files exist before moving them
if [ -f "/workspace/Stable-Diffusion/train_loras_log.txt" ]; then
    mv /workspace/Stable-Diffusion/train_loras_log.txt "/workspace/Stable-Diffusion/session_$current_datetime"
else
    echo "train_loras_log.txt not found. Skipping..."
fi

if [ -f "/workspace/Stable-Diffusion/DB_gen_img_log.txt" ]; then
    mv /workspace/Stable-Diffusion/DB_gen_img_log.txt "/workspace/Stable-Diffusion/session_$current_datetime"
else
    echo "DB_gen_img_log.txt not found. Skipping..."
fi

# Check if the images folder exists before moving it
if [ -d "/workspace/Stable-Diffusion/images" ]; then
    mv /workspace/Stable-Diffusion/images "/workspace/Stable-Diffusion/session_$current_datetime"
else
    echo "Images folder not found. Skipping..."
fi

# Parent folder IDs on Google Drive
session_folder_id="1gIf3G4aGGCkm8spTvS24ikkvr4A4Yf_l"
model_folder_id="1mB3koZyL35ZSgqrbcOmjVTYgt9XbGbD6"

# Upload model & session: (images, tr_log, gen_log)
# Upload the model (recursive)
gdrive files upload --recursive /workspace/stable-diffusion-webui/models/Stable-diffusion/model/ --parent "$model_folder_id"

# Upload the session folder (images, tr_log, gen_log)
gdrive files upload --recursive "/workspace/Stable-Diffusion/session_$current_datetime" --parent "$session_folder_id"
wait

# End time
end_time=$(date +%s)

# Print execution time
echo "Model and Session uploaded, Total upload time: $((end_time - start_time)) seconds."
