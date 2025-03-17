#!/bin/bash
cd ~/HealthcareFoodProject/Dev/VLM_Fine_Tuning
docker cp llamafactory-gpu0:/app/. LLaMA-Factory/.
cd LLaMA-Factory
rm -rf custom_data/UECFOOD256 wandb mlruns
