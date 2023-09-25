
wget https://github.com/glotlabs/gdrive/releases/download/3.9.0/gdrive_linux-x64.tar.gz

mkdir gdrive

tar -xvzf gdrive_linux-x64.tar.gz

#mv gdrive /bin/
# cp gdrive /bin/gdrive
cp gdrive /bin

chmod a+x /bin/gdrive

cd /workspace/Stable-Diffusion

gdrive account import gdrive_export-ukrconfidential_gmail_com.tar
