import json
import os
from collections import defaultdict
import random

# Loads JSON data from the master file with utf-8 encoding
with open("Dataset/masterfile.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Base directory paths for images and depth maps
base_dir = "Dataset"
depth_maps_dir = os.path.join(base_dir, "Depth Maps")
sg_food_dir = os.path.join(base_dir, "SGFood")

# Organize food items by directory name
food_items_by_type = defaultdict(list)

# Populate the dictionary with images and their corresponding weights
for item in data["food_data"]:
    file_path = item.get("file_path")
    directory_name = file_path.split('/')[1] if file_path else "unknown"
    weight = item.get("weight")

    # Skip items with missing or nil weight
    if weight is None or weight == "nil":
        continue

    # Construct the expected image paths for both cases
    if file_path:
        # Navigate to the correct folder under SGFood
        subfolder = os.path.join(sg_food_dir, directory_name)
        base_file_name = os.path.basename(file_path)

        # Paths for different capitalization scenarios
        image_path_upper = os.path.join(subfolder, base_file_name.replace(".jpg", ".JPG"))
        image_path_lower = os.path.join(subfolder, base_file_name.replace(".JPG", ".jpg"))
        depth_image_path_upper = os.path.join(depth_maps_dir,
                                              base_file_name.replace(".jpg", "_depth.JPG").replace(".JPG", "_depth.JPG"))
        depth_image_path_lower = os.path.join(depth_maps_dir,
                                              base_file_name.replace(".jpg", "_depth.jpg").replace(".JPG", "_depth.jpg"))

        # Check if either regular image (upper or lower case) exists
        if not (os.path.exists(image_path_upper) or os.path.exists(image_path_lower)):
            continue  # Skip if neither regular image exists

        # Check if either depth image (upper or lower case) exists
        if not (os.path.exists(depth_image_path_upper) or os.path.exists(depth_image_path_lower)):
            continue  # Skip if neither depth image exists

        # Add to the dictionary
        food_items_by_type[directory_name].append((file_path, weight))

# Split data into training and testing sets
train_data = []
test_data = []

for directory_name, items in food_items_by_type.items():
    if len(items) < 20:
        train_data.extend(items)  # Add all items to the training set if there are fewer than 20 images
    else:
        random.shuffle(items)  # Shuffle the items
        split_index = int(len(items) * 0.8)  # 80/20 split
        train_data.extend(items[:split_index])
        test_data.extend(items[split_index:])

# Write the formatted training data to a file
with open("train_data.txt", "w", encoding="utf-8") as train_file:
    for file_path, weight in train_data:
        directory_name = file_path.split('/')[1]
        train_file.write(f"{file_path} {directory_name} {weight}\n")

# Write the formatted testing data to a file
with open("test_data.txt", "w", encoding="utf-8") as test_file:
    for file_path, weight in test_data:
        directory_name = file_path.split('/')[1]
        test_file.write(f"{file_path} {directory_name} {weight}\n")

print("Data split into train_data.txt and test_data.txt.")
