import torch
import torch.nn.functional as F
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torch.utils.data import random_split
import pytorch_lightning as pl
from torch.utils.data.distributed import DistributedSampler
from torch.utils.data import Dataset
import data_augment
from typing import Any
from PIL import Image
import os


class n5kDataModule(pl.LightningDataModule):
    def __init__(self, args):
        super().__init__()
        self.args = args

        self.args.data_dir="Dataset"
        #if torch.cuda.get_device_name(torch.cuda.current_device()) in ["NVIDIA RTX A6000", "NVIDIA T600 Laptop GPU"]:
            # for local workstation
            #self.args.data_dir="Dataset/nutrition5k_dataset/imagery/"
        
        self.train_label_dir = "train_data.txt"
        self.test_label_dir = "test_data.txt"
        #if self.args.dataset_subset:
            #self.train_label_dir = "rgb_in_overhead_train_processed_subset.txt"
        
        self.standard_transforms_rgb = getattr(
            data_augment, args.standard_transforms)()
        self.norm_transforms_rgb = getattr(
            data_augment, args.norm_transforms)()
        self.norm_transforms_depth = getattr(
            data_augment, args.norm_transforms_depth)()
        self.data_transforms_rgb = getattr(
            data_augment, args.data_transforms)()
        self.identity = getattr(data_augment, "identity")()
        self.dataset_kwargs = {"use_depth": args.use_depth,
                               "mutexlock_rgb_depth": args.mutexlock_rgb_depth}
        
    def setup(self, stage):
        self.train_ds = CustomRegressionDataset(
            "Dataset",  # Path to RGB images
            "Dataset/Depth Maps",  # Path to depth images
            self.train_label_dir,
            None,
            self.standard_transforms_rgb,
            self.data_transforms_rgb,
            self.norm_transforms_rgb,
            self.norm_transforms_depth,
            self.dataset_kwargs
        )
        self.test_ds = CustomRegressionDataset(
            "Dataset",  # Path to RGB images
            "Dataset/Depth Maps",  # Path to depth images
            self.test_label_dir,
            None,
            self.standard_transforms_rgb,
            self.identity,
            self.norm_transforms_rgb,
            self.norm_transforms_depth,
            self.dataset_kwargs
        )
        
    def train_dataloader(self):
        return DataLoader(
            self.train_ds,
            batch_size=self.args.batch_size,
            num_workers=self.args.num_workers,
            shuffle=True,
            pin_memory=True,
            persistent_workers=True
        )
    
    def test_dataloader(self):
        return DataLoader(
            self.test_ds,
            batch_size=self.args.batch_size,
            num_workers=self.args.num_workers,
            shuffle=False,
            pin_memory=True,
            persistent_workers=True
        )

class CustomRegressionDataset(Dataset):
    def __init__(self, rgb_dir, depth_dir, label_dir, indices_to_keep, transform_standard, transform_randomized,
                 transform_rgb_norm, transform_depth_norm, *kwargs: Any):
        self.rgb_dir = rgb_dir  # Directory for RGB images
        self.depth_dir = depth_dir  # Directory for depth images
        self.transform_standard = transform_standard
        self.transform_randomized = transform_randomized
        self.transform_rgb_norm = transform_rgb_norm
        self.transform_depth_norm = transform_depth_norm
        self.samples = []
        self.dataset_kwargs = kwargs[0] if kwargs else {}
        self.retrieve_info(label_dir, indices_to_keep)

    def retrieve_info(self, label_dir, indices_to_keep):
        # Read the data from the txt file and store it in a list
        with open(os.path.join(label_dir), 'r') as f:
            lines = f.readlines()

            # Keep only the lines with the desired indices
            if indices_to_keep is not None:
                new_lines = [lines[i] for i in indices_to_keep]
            else:
                new_lines = lines

            for line in new_lines:
                # Unpack only the necessary parts: sample path, folder name, and total mass
                sample_path, foldername, total_mass = line.strip().split(' ')
                self.samples.append((sample_path, foldername, float(total_mass)))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        sample_path, foldername, total_mass = self.samples[idx]
        image = Image.open(os.path.join(self.rgb_dir, sample_path)).convert('RGB')

        depth_img = 0
        if self.dataset_kwargs["use_depth"] != "None":  # Check if depth images are needed
            if self.dataset_kwargs["use_depth"] == "color":
                # Ensure only one "_depth" suffix is added
                base_name, ext = os.path.splitext(os.path.basename(sample_path))
                depth_filename = f"{base_name}_depth.JPG"
                depth_img = Image.open(os.path.join(self.depth_dir, depth_filename)).convert('RGB')

            if self.dataset_kwargs["mutexlock_rgb_depth"]:
                image = self.transform_standard(image)
                depth_img = self.transform_standard(depth_img)
                concat_chnls = torch.cat([image, depth_img], dim=0)
                concat_chnls = self.transform_randomized(concat_chnls)
                image, depth_img = torch.split(concat_chnls, 3, dim=0)

                image = self.transform_rgb_norm(image)
                depth_img = self.transform_depth_norm(depth_img)

        # Convert the total mass to a float32 tensor
        total_mass = torch.tensor([total_mass], dtype=torch.float32)

        return image, depth_img, total_mass
        