import os
import torch
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# For depth estimation model
import depth_pro
import pillow_heif  # For handling HEIC images

# For NuNet model
from model import RGB_D_Constructor
from data_augment import S0
from config_parser import get_parser

# Register HEIF opener for Pillow
pillow_heif.register_heif_opener()

# ---------------------
# Change Current Working Directory
# ---------------------

# Change the working directory to where the checkpoints directory is located
os.chdir(r"ml-depth-pro")

# ---------------------
# Initialize Models
# ---------------------

# Depth Estimation Model
depth_model, depth_transform = depth_pro.create_model_and_transforms()
depth_model.eval()

# NuNet Mass Estimation Model
parser, args_dict = get_parser()
args = parser.parse_args([])
checkpoint_path = r"experiment/Example.ckpt"
nUNet_model = RGB_D_Constructor.load_from_checkpoint(checkpoint_path, args=args)
nUNet_model.eval()

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
depth_model = depth_model.to(device)
nUNet_model = nUNet_model.to(device)

# Transformation for NuNet model
nuNet_transform = S0()

# ---------------------
# Helper Function
# ---------------------

def format_depth(depth_tensor):
    """
    Formats the depth tensor into a PIL image with a colormap.
    """
    depth_np = depth_tensor.squeeze().cpu().numpy()
    # Normalize depth to 0-1
    depth_normalized = (depth_np - depth_np.min()) / (depth_np.max() - depth_np.min())
    # Apply colormap
    depth_colored = plt.cm.jet(depth_normalized)[:, :, :3]  # Ignore alpha channel
    depth_colored = (depth_colored * 255).astype(np.uint8)
    depth_img = Image.fromarray(depth_colored)
    return depth_img

# ---------------------
# Process Single Image
# ---------------------

image_path = r"Dataset\SGFood\Duck_Rice\Duck_Rice_28_w.jpg"

# Check if the image file exists
if not os.path.exists(image_path):
    raise FileNotFoundError(f"Image file not found: {image_path}")

# Construct the depth image filename with '_depth' suffix
depth_file_name = f"{os.path.splitext(os.path.basename(image_path))[0]}_depth.jpg"
depth_folder = os.path.dirname(image_path)  # Save depth image in the same folder
depth_path = os.path.join(depth_folder, depth_file_name)

# Check if the depth file already exists
if not os.path.exists(depth_path):
    # Generate depth image
    print("Generating depth image for:", image_path)

    # Load the image
    image = Image.open(image_path).convert("RGB")

    # Preprocess the image for depth estimation model
    depth_input = depth_transform(image).unsqueeze(0).to(device)  # Add batch dimension and move to device

    # Run model inference using the 'infer' method
    with torch.no_grad():
        output = depth_model.infer(depth_input)
    depth_tensor = output["depth"]  # Get the depth tensor

    # Format and save depth image
    depth_img = format_depth(depth_tensor)
    depth_img.save(depth_path)
    print("Saved depth image:", depth_path)
else:
    print("Depth image already exists:", depth_path)
    # Load the RGB image
    image = Image.open(image_path).convert('RGB')

# Now, load the depth image
depth_image = Image.open(depth_path).convert('RGB')

# ---------------------
# Prepare Input for NuNet Model
# ---------------------

# Apply the same preprocessing transformations used during training
image_tensor = nuNet_transform(image).unsqueeze(0).to(device)  # Add batch dimension and move to device
depth_tensor_nunet = nuNet_transform(depth_image).unsqueeze(0).to(device)  # Add batch dimension and move to device

# ---------------------
# Run Inference with NuNet Model
# ---------------------

with torch.no_grad():
    output = nUNet_model(image_tensor, depth_tensor_nunet)

# If the output is a tuple, extract the first element
if isinstance(output, tuple):
    output = output[0]  # Adjust this based on your model's actual output structure

# Get the predicted mass
predicted_mass = output.squeeze().item()
print(f"Predicted Mass for {image_path}: {predicted_mass}")
