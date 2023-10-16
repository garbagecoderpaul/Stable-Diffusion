import json
import subprocess

# Read gender from prompt_log.json
prompt_log_path = '/workspace/Stable-Diffusion/prompt_log.json'

with open(prompt_log_path, 'r') as json_file:
    prompt_log = json.load(json_file)

gender = prompt_log.get('gender')

if gender == 'm':
    # Execute the shell script for downloading men's images
    subprocess.run(['bash', 'download_man_reg_imgs_1024x1024.sh'])
elif gender == 'f':
    # Execute the shell script for downloading women's images
    subprocess.run(['bash', 'download_women_reg_1024.sh'])
else:
    print("Wrong gender:", gender)
