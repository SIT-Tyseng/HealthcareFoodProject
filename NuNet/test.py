import torch
from model import *
from dataset import *
# from pytorch_lightning.loggers import TensorBoardLogger
from pytorch_lightning.loggers import WandbLogger
import os
from config_parser import *

# torch.set_float32_matmul.precision('high')
torch.set_float32_matmul_precision('medium')

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
# Define the set of cores you want to run the process on
#cpu_set = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
#          40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59}

# Set the CPU affinity of the current process to the defined set of cores
#os.sched_setaffinity(0, cpu_set)

# Get the CPU affinity of the current process
#cpu_set = os.sched_getaffinity(0)

project_name = "NuNet_deepsupervision"
#if torch.cuda.get_device_name(torch.cuda.current_device()) in ["NVIDIA RTX A6000", "NVIDIA T600 Laptop GPU"]:
    # for local workstation
project_name = "NuNet_deepsupervision_check"

def main(parser, args_dict):
    args, group_name, run_tags = get_experiment_name(parser, args_dict)

    Reproducibility = True
    Deterministic = True
    seed = 3

    if Reproducibility:
        torch.manual_seed(seed)
    else:
        torch.random.seed()
        print(f'torch.initial_seed():{torch.initial_seed()}')
    os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8' # or ':16:8'
    if Deterministic:
        torch.use_deterministic_algorithms(True, warn_only=True)

    # Load the Wandb run ID
    wandb_run_id = '37c9ed248cc58c1dae423f304c095d48a9f8150e'

    # Initialise the WandbLogger with the saved run ID
    logger = WandbLogger(id=wandb_run_id, resume="allow",
                         project=project_name, group=group_name)
    ckpt_path = f"{args.save_dir}{logger.experiment.name}.ckpt"
    model = RGB_D_Constructor.load_from_checkpoint(args=args, checkpoint_path=ckpt_path)

    model.eval()

    dm = n5kDataModule(
        args = args
    )

    tester = pl.Trainer(
        logger=logger,
        accelerator=args.accelerator,
        devices=1,
        precision=args.precision,
    )
    tester.test(model, dm)

if __name__ == "__main__":
    parser, args_dict = get_parser()
    main(parser, args_dict)