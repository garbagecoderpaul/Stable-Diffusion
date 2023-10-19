# Prep list of CharacterIDs from destination folder
cd /workspace/train_img/

ls -h > /workspace/Stable-Diffusion/characters.txt


cd /workspace/Stable-Diffusion/

# Install virtual environment
source /workspace/kohya_ss/venv/bin/activate

# Run the command
## Input = characters.txt
echo '777777777777777777 all good'
python train_DBs.py