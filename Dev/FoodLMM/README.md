## FoodLMM
### Flash Attention installation 
If the environment requires `flash_attn` package and the system fails to install it after using `pip install flash-attn --no-build-isolation`, go to the `wheels` directory to search for the wheel file and install it with `pip install [wheel file]`, or check out the [release page](https://github.com/Dao-AILab/flash-attention/releases) for the correct wheel file version. 

--- 
### Docker 
1. Go to the root directory of the repo: 
```
cd HealthcareFoodProject
```
2. Run the following docker command to build the image:
Note: It is recommended to install docker buildx for smooth image build
```
docker build \
--build-context wheels=./Dev/FoodLMM/wheels \ #remove this line if docker buildx is not used
-f ./Dev/FoodLMM/dockers/FoodLMM/Dockerfile \
-t foodlmm \
./OpenSource/FoodLMM
```
3. Run the container in background mode: 
```
docker run -d --gpus all -v /path/to/storage:/storage -it foodlmm bash 
```

4. Access the container: 
```
docker exec -it <container_id> /bin/bash
```

5. Run the Deployment command:
```
cd app
CUDA_VISIBLE_DEVICES=0 python online_demo.py --version=/storage/FoodLMM-Chat
```
---
### Download pretrain weight for Inference 
To download the pretrain weight, use the following command 
```
mkdir storage && cd storage [prefer to be outside of the repo folder]
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/Yueha0/FoodLMM-Chat
git lfs pull
```