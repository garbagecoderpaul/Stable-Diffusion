#!/bin/bash

apt-get update
apt-get install imagemagick
echo "Y" | ./converter.sh

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
