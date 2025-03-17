#!/bin/bash
cd ~/HealthcareFoodProject/Dev/VLM_Fine_Tuning
docker cp llamafactory:/app/. LLaMA-Factory/.
#cd LLaMA-Factory
#rm -rf custom_data/UECFOOD256 wandb mlruns
