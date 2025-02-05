import argparse


def get_parser():
    parser = argparse.ArgumentParser()

    args_dict = {
        "b": "backbone",
        "d": "decoder",
        "f": "freeze",
        "bs": "batch_size",
        "dr": "decay_rate",
        "e": "num_epochs",
        "ep": "epsilon",
        "fdr": "fast_dev_run",
        "l": "loss",
        "lr": "learning_rate",
        "o": "optimizer",
        "s": "seed",
        "wd": "weight_decay",
        "dd": "data_dir",
        "dt": "data_transforms",
        "ls": "input_size",
        "nc": "num_classes",
        "nr": "norm_transforms",
        "nd": "norm_transforms_depth",
        "nw": "num_workers",
        "st": "standard_transforms",
        "ud": "use_depth",
        "mrd": "mutexlock_rgb_depth",
        "a": "accelerator",
        "dn": "device_num",
        "sy": "strategy",
        "de": "Deterministic",
        "p": "precision",
        "re": "Reproducibility",
        "des": "description",
        "ts": "to_save",
        "sd": "save_dir",
        "ds": "dataset_subset",
        "cs": "change_test_set",
    }

    # Model Configuration
    parser.add_argument('-b', f'--{args_dict["b"]}', nargs='+', help='backbone class name', default=["SB", "SB"])
    parser.add_argument('-d', f'--{args_dict["d"]}', type=str, help='decoder class name', default="DeepSupervision")
    parser.add_argument('-f', f'--{args_dict["f"]}', type=int, help='Freeze certain layers during training', default=0)

    # Training Settings
    parser.add_argument('-bs', f'--{args_dict["bs"]}', type=int, help='Training batch size', default=16)
    parser.add_argument('-dr', f'--{args_dict["dr"]}', type=float, help='Learning rate decay rate', default=0.99)
    parser.add_argument('-e', f'--{args_dict["e"]}', type=int, help='Number of training epochs', default=75)
    parser.add_argument('-ep', f'--{args_dict["ep"]}', type=float, help='Epsilon for the optimizer stability', default=1e-6)
    parser.add_argument('-fdr', f'--{args_dict["fdr"]}', type=int, help='Integer or boolean value for quick debug run', default=0)
    parser.add_argument('-l', f'--{args_dict["l"]}', type=str, help='Loss function to use', default="ModifiedMAPE")
    parser.add_argument('-lr', f'--{args_dict["lr"]}', type=float, help='Learning rate for the optimizer', default=1e-4)
    parser.add_argument('-o', f'--{args_dict["o"]}', type=str, help='Optimizer type', default="Adam")
    parser.add_argument('-s', f'--{args_dict["s"]}', type=int, help='Initialization seed value', default=3)
    parser.add_argument('-wd', f'--{args_dict["wd"]}', type=float, help='Weight decay for the optimizer', default=1e-5)

    # Data Handling
    parser.add_argument('-cs', f'--{args_dict["cs"]}', type=str, help='v2', default="v2")
    parser.add_argument('-dd', f'--{args_dict["dd"]}', type=str, help='Directory containing the dataset', default="/srv/itpten/training_datasets/nutrition5k_dataset/imagery/")
    parser.add_argument('-dt', f'--{args_dict["dt"]}', type=str, help='Data-specific transforms for RGB images', default="C2_1A")
    parser.add_argument('-ls', f'--{args_dict["ls"]}', type=int, help='Size of the input images', default=224)
    parser.add_argument('-nc', f'--{args_dict["nc"]}', type=int, help='Number of classes in the dataset', default=10)
    parser.add_argument('-nr', f'--{args_dict["nr"]}', type=str, help='Normalization transforms for RGB images', default="C2_1B")
    parser.add_argument('-nd', f'--{args_dict["nd"]}', type=str, help='Perform random transform (optional), normalize for depth', default="D1")
    parser.add_argument('-nw', f'--{args_dict["nw"]}', type=int, help='Number of data loader workers', default=2) # 2, 4, 40
    parser.add_argument('-st', f'--{args_dict["st"]}', type=str, help='Standard transforms for RGB images', default="S0")
    parser.add_argument('-ud', f'--{args_dict["ud"]}', type=str, help='color, None', default="color")
    parser.add_argument('-mrd', f'--{args_dict["mrd"]}', type=str, help='rgb and depth images will be random transformation applied together', default=True)

    # System Configuration 
    parser.add_argument('-a', f'--{args_dict["a"]}', type=str, help='Hardware accelerator to use', default="cuda")
    parser.add_argument('-dn', f'--{args_dict["dn"]}', type=int, help='Number of device', default=1) # 2
    parser.add_argument('-sy', f'--{args_dict["sy"]}', type=str, help='number of device', default="None") # ddp
    parser.add_argument('-de', f'--{args_dict["de"]}', type=str, help='Ensure deterministic behavior', default=True)
    parser.add_argument('-p', f'--{args_dict["p"]}', type=str, help='Training precision', default="32")
    parser.add_argument('-re', f'--{args_dict["re"]}', type=str, help='Enable reproducibility features', default=True)

    # Miscellaneous
    parser.add_argument('-des', f'--{args_dict["des"]}', type=str, help='Description of the model or run', default="Description Placeholder")
    parser.add_argument('-ts', f'--{args_dict["ts"]}', type=str, help='Save best loss value as checkpoint file', default="False")
    parser.add_argument('-sd', f'--{args_dict["sd"]}', type=str, help='Save checkpoint file at following path', default="experiment/")
    parser.add_argument('-ds', f'--{args_dict["ds"]}', type=str, help='Use dataset subset version', default=False)

    return parser, args_dict

def get_experiment_name(parser, args_dict):
    args = parser.parse_args()
    arg_custom = []
    arg_all = []
    del args_dict["des"]
    del args_dict["dd"]
    for key in args_dict:
        arg_value = getattr(args, args_dict[key])
        args_default = parser.get_default(args_dict[key])

        if arg_value != args_default:
            arg_custom.append(f"{key}={arg_value}")
        
        arg_all.append(f"{key};{arg_value}")

    group_name = ".".join(arg_custom)
    tags = tuple(arg_all)

    if group_name == "":
        group_name = "default"

    print(f'group_name: {group_name}')
    print(f'tags: {tags}')
    return args, group_name, tags