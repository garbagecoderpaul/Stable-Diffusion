# Stable-Diffusion

## Commands
* Open a new terminal and execute commands below for initial install:
  * Creates a new folder with files and scripts
  * Downloads regularisation images for men and women
  * Installs gdrive app
```
git clone https://github.com/garbagecoderpaul/Stable-Diffusion.git
cd Stable-Diffusion/

bash gdrive_instal.sh

bash download_man_reg_imgs_1024x1024.sh

bash download_women_reg_1024.sh

```

## Files
* download_gDrive.py
  * downloads a LoRA model from Google Folder
* get_training_sets.py
  * downloads training sets from a .csv file
  * the csv file should be named: "Book1.csv"
* sdxl_preset3.json
  * config file - set for men by default
  



