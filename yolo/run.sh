#!/bin/bash

echo "Script should be installed and training images loaded"

# Activate the virtual environment
source venv/bin/activate

export CUDA_VISIBLE_DEVICES=0
python cropper_auto.py

# Deactivate the virtual environment
deactivate
