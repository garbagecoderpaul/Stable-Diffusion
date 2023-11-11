# switch to alternative brunch

wget https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors?download=true

mv sdxl_vae.safetensors?download=true \
	/workspace/stable-diffusion-webui/models/VAE/SDXL_FP32_VAE.safetensors

git pull sd-scripts-dev

git pull origin sd-scripts-dev

git checkout sd-scripts-dev

git pull origin sd-scripts-dev



