#!/bin/bash

echo "Don't forget to run the install script and make sure that you have changed the paths in cropper_v7.py file"

# Activate the virtual environment
source venv/bin/activate

export CUDA_VISIBLE_DEVICES=0
python cropper_v7.py

# Deactivate the virtual environment
deactivate
