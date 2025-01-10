import os
import subprocess
import torch
import wandb
import sys

import torch


print("Is CUDA available:", torch.cuda.is_available())
print("CUDA version:", torch.version.cuda)
print("CUDNN version:", torch.backends.cudnn.version())
print("CUDA device name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No CUDA device detected")
print("CUDA device count:", torch.cuda.device_count())

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

if __name__ == "__main__":
    os.environ['WANDB_RUN_ID'] = wandb.util.generate_id()
    args = sys.argv[1:]

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is not available. Please check your setup.")
    else:
        print("Using device:", torch.cuda.get_device_name(torch.cuda.current_device()))

    try:
        command = ["python", "train.py"] + args
        subprocess.run(command)

        command = ["python", "test.py"] + args
        subprocess.run(command)

    except Exception as e:
        print(f"An error occurred: {e}")
