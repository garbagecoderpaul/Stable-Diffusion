#!/bin/bash

#gdrive
bash gdrive_install.sh

# Start time
start_time=$(date +%s)

# images
gdrive files upload /workspace/Stable-Diffusion/images \
	--recursive --parent 1gIf3G4aGGCkm8spTvS24ikkvr4A4Yf_l & \
	# image gen log
	gdrive files upload /workspace/Stable-Diffusion/DB_gen_img_log.txt \
	--parent 1gIf3G4aGGCkm8spTvS24ikkvr4A4Yf_l & \
	# models
	gdrive files upload /workspace/stable-diffusion-webui/models/Stable-diffusion/model \
	--recursive --parent 1gIf3G4aGGCkm8spTvS24ikkvr4A4Yf_l & \
	# training log
	gdrive files upload /workspace/Stable-Diffusion/train_loras_log.txt \
	--parent 1gIf3G4aGGCkm8spTvS24ikkvr4A4Yf_l $$ fg

wait

# End time
end_time=$(date +%s)

# Print execution time
echo "Total execution time: $(( end_time - start_time )) seconds."