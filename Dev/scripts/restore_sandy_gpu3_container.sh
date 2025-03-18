#!/bin/bash
cd ~/HealthcareFoodProject/Dev/VLM_Fine_Tuning
docker cp Qwen_Fine_Tuning_Sandy/. qwen_ft_dgx:/VLM/.
