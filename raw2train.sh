#!/bin/bash

#unificate the directories
python dir_unif.py

# convert to png
bash converter.sh

# Set paths
yolo_archive="/workspace/Stable-Diffusion/yolo_v7_auto_cropper_v3.zip"
yolo_directory="/workspace/Stable-Diffusion/yolo"

# Check if the archive exists and the directory is not already extracted
if [ ! -f "$yolo_archive" ]; then
    # Download the archive if not done already
    if [ ! -f "$yolo_archive" ]; then
        wget https://huggingface.co/MonsterMMORPG/SECourses/resolve/main/yolo_v7_auto_cropper_v3.zip -P "$yolo_directory"
    else
        echo "Yolo archive already exists."
    fi

    # Unzip the archive
    unzip "$yolo_archive" -d "$yolo_directory"

    cd "$yolo_directory"

    # Install if not done already
    if [ ! -f "install_complete" ]; then
        # Install
        bash install.sh
        # Create a file to mark installation completion
        touch install_complete
    else
        echo "Yolo already installed."
    fi
fi

# Do the cropping
cd /workspace/Stable-Diffusion/yolo
bash run.sh

cd /workspace/Stable-Diffusion