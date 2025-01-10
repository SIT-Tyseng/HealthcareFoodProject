import torch
from model import *
from dataset import *
from pytorch_lightning.loggers import WandbLogger
from pytorch_lightning.strategies import DDPStrategy
import os
from config_parser import *
from custom_callbacks import *

torch.set_float32_matmul_precision('medium')

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# Check if CUDA is available
if torch.cuda.is_available():
    torch.cuda.empty_cache()

project_name = "NuNet_check"

# Function to load the model from a checkpoint
def load_model(checkpoint_path):
    parser, args_dict = get_parser()
    args, group_name, run_tags = get_experiment_name(parser, args_dict)

    model = RGB_D_Constructor.load_from_checkpoint(
        args=args,
        checkpoint_path=checkpoint_path,
    )
    print("Model loaded from checkpoint")
    total_params = sum(p.numel() for p in model.parameters()) / 1e6
    print(f"Total number of parameters: {total_params} Million")
    return model, args


def main(parser, args_dict):
    args, group_name, run_tags = get_experiment_name(parser, args_dict)

    if args.Reproducibility:
        torch.manual_seed(args.seed)
    else:
        torch.random.seed()
        print(f'torch.initial_seed():{torch.initial_seed()}')
    os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
    if args.Deterministic:
        torch.use_deterministic_algorithms(True, warn_only=True)

    # Load the Wandb run ID
    wandb_run_id = 'Example'

    # Initialise the WandbLogger with the saved run ID
    logger = WandbLogger(id=wandb_run_id, resume="allow",
                         project=project_name, group=group_name)
    logger.experiment.tags = logger.experiment.tags + run_tags
    logger.experiment.notes = str(args.description)

    # Path to your saved checkpoint
    checkpoint_path = "experiment/Example.ckpt"

    # Load the model from the checkpoint if it exists
    if os.path.exists(checkpoint_path):
        model, args = load_model(checkpoint_path)
    else:
        # If no checkpoint is found, initialize a new model
        model = RGB_D_Constructor(args=args)

    dm = n5kDataModule(args=args)

    if args.strategy == "None":
        print(f'args.strategy:{args.strategy}')
        trainer = pl.Trainer(
            fast_dev_run=args.fast_dev_run,
            logger=logger,
            devices=1,
            accelerator='cuda',
            min_epochs=1,
            max_epochs=75,
            precision=args.precision,
            enable_checkpointing=False,
            callbacks=[TrainCallback()],
        )

    trainer.fit(model, dm)


if __name__ == "__main__":
    parser, args_dict = get_parser()
    main(parser, args_dict)
