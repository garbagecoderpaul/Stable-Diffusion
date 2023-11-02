#!/bin/bash

# convert to png
bash converter.sh

# download
wget https://huggingface.co/MonsterMMORPG/SECourses/resolve/main/yolo_v7_auto_cropper_v3.zip
# unzip
unzip /workspace/Stable-Diffusion/yolo_v7_auto_cropper_v3.zip -d /workspace/Stable-Diffusion/yolo

# install
bash /workspace/Stable-Diffusion/yolo/install.sh
echo -e '\n' | your_command_that_prompts_for_input

# do the cropping
bash /workspace/Stable-Diffusion/yolo/run.sh

