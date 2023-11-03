#!/bin/bash

# Check if ImageMagick is installed
if ! command -v convert &> /dev/null; then
    echo "ImageMagick is not installed. Installing..."
    
    # Set the DEBIAN_FRONTEND variable to noninteractive
    export DEBIAN_FRONTEND=noninteractive
    
    # Update the package repository
    apt-get update
    
    # Install ImageMagick
    apt-get install -y imagemagick
    
    # Check if installation was successful
    if [ $? -eq 0 ]; then
        echo "ImageMagick installation completed."
    else
        echo "Failed to install ImageMagick."
        exit 1
    fi
fi

# Specify the input folder where your image files are located
input_folder="/workspace/train_img"

# Use 'find' to locate image files in all subfolders of the input folder
find "$input_folder" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.webp" -o -iname "*.avif" \) -exec bash -c '
    for file; do
        ext="${file##*.}"
        if [ "$ext" != "png" ]; then
            convert "$file" "${file%.*}.png"
            echo "Converted $file to ${file%.*}.png"
            rm "$file"
            echo "Deleted $file"
        fi
    done
' bash {} +

echo "Conversion complete."
