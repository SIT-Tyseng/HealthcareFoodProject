import torch
from model import RGB_D_Constructor
from PIL import Image
from data_augment import S0
from config_parser import get_parser
import os

# Step 1: Initialize the parser and get args
parser, args_dict = get_parser()
args = parser.parse_args()  # This creates the args object

# Step 2: Load the Model from the Checkpoint
checkpoint_path = "experiment/37c9ed248cc58c1dae423f304c095d48a9f8150e.ckpt"

# Load the model
model = RGB_D_Constructor.load_from_checkpoint(checkpoint_path, args=args)

# Step 3: Set the Model to Evaluation Mode
model.eval()

# Step 4: Prepare Your Input Data
# Load and preprocess the RGB image
image_path = "Dataset/SGFood/Duck_Rice/Duck_Rice_28_w.jpg"
image = Image.open(image_path).convert('RGB')

# Load and preprocess the corresponding depth image
depth_image_path = os.path.join(
    "C:/Users/Kingston/PycharmProjects/NuNet/Dataset/Depth Maps",
    os.path.basename(image_path).replace("_w.JPG", "_depth.JPG")
)
depth_image = Image.open(depth_image_path).convert('RGB')

# Apply the same preprocessing transformations used during training
transform = S0()  # Replace with your chosen transformation
image_tensor = transform(image).unsqueeze(0)  # Add a batch dimension
depth_tensor = transform(depth_image).unsqueeze(0)  # Add a batch dimension

# Step 5: Run Inference
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
image_tensor = image_tensor.to(device)
depth_tensor = depth_tensor.to(device)

# Get the prediction
with torch.no_grad():
    output = model(image_tensor, depth_tensor)

# If the output is a tuple, extract the first element
if isinstance(output, tuple):
    output = output[0]  # Adjust this based on your model's actual output structure

# Now you can call .squeeze() and get the predicted mass
predicted_mass = output.squeeze().item()
print(f"Predicted Mass: {predicted_mass}")
