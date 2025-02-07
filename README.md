# NutritionAssessmentProject

This repo is mainly focusing on nutrition assessment related models, such as VLM (Visual Language Model), LMM (Large Multi-modal Model), and NuNet (Food Mass Prediction Model). Following are the list of the models which can be found in this repo:

---
## Models
### VLM:
- miniCPM
- Qwen2.5-VL 
- LLaVA-NEXT 
- SAM2 
- VILA 
- Janus 

### LMM:
- FoodLLM

### Food Mass Prediction Model:
- NuNet

---
## Flash Attention installation 
If the environment requires `flash_attn` package and the system fails to install it after using `pip install flash-attn --no-build-isolation`, go to the `wheels` directory to search for the wheel file and install it with `pip install [wheel file]`, or check out the [release page](https://github.com/Dao-AILab/flash-attention/releases) for the correct wheel file version. 

--- 
## Docker 
1. Go to the root directory of the repo: 
```
cd NutritionAssessmentProject
```
2. Run the following docker command to build the image:
```
docker build \
-f ./Dev/dockers/FoodLMM/Dockerfile \
-t foodlmm \
./OpenSource/FoodLMM
```
3. Run the container in background mode: 
```
docker run -d -it foodlmm bash 
```

4. Access the container: 
```
docker exec -it <container_id> /bin/bash
```

---
## Download pretrain weight for Inference 
To download the pretrain weight, use the following command 
```
mkdir storage && cd storage [prefer to be outside of the repo folder]
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/Yueha0/FoodLMM-Chat
git lfs pull
```