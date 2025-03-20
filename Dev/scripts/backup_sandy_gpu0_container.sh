#!/bin/bash
cd ~/HealthcareFoodProject/Dev/VLM_Fine_Tuning
docker cp qwen_ft_dgx_gpu0:/VLM/. Qwen_Fine_Tuning_Sandy/.
cd Qwen_Fine_Tuning_Sandy 
rm -rf custom_data/UECFOOD256 wandb mlruns
