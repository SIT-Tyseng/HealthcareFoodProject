#!/bin/bash
cd ~/HealthcareFoodProject/Dev/VLM_Fine_Tuning
docker cp qwen_ft_dgx:/VLM/. Qwen_Fine_Tuning_Sandy/.
cd Qwen_Fine_Tuning_Sandy 
rm -rf custom_data/UECFOOD256 wandb mlruns
