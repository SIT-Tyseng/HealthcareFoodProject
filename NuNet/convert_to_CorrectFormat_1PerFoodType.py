import json
import os
from collections import defaultdict
import random

# Load your JSON data from the master file with utf-8 encoding
with open("Dataset/masterfile.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Base directory paths for images and depth maps
base_dir = "Dataset"
depth_maps_dir = os.path.join(base_dir, "Depth Maps")
sg_food_dir = os.path.join(base_dir, "SGFood")

# List of the 45 specified food types
specified_food_types = [
    "Ban_Mian_Dry", "Chicken_Rice_Roasted", "Duck_Rice", "Kaya_Toast", "Hainanese_Curry_Rice",
    "Economy_Rice", "Laksa", "Mala_Dry_Pot", "Lor_Mee", "Curry_Puff", "Nasi_Lemak",
    "Prawn_Noodles_Soup", "Prawn_Noodles_Dry", "Claypot_Rice", "Ke_Kou_Mian",
    "Chicken_Rice_Steamed", "Chicken_Rice_Steamed_Porridge", "Grilled_Fish_with_Rice",
    "Fried_Rice", "Ayam_Penyet", "Ayam_Panggang", "Bak_Chor_Mee", "Big_Pau", "Char_Siew_Pau",
    "Char_Siew_Rice", "Economy_Bee_Hoon", "Fan_Choy", "Fried_Dumplings", "Fried_Hokkien_Mee",
    "Congee", "Tau_Sar_Pau", "Xingzhou_Bee_Hoon", "Har_Gow", "Plain_Prata",
    "Char_Kway_Teow", "Chee_Cheong_Fun", "Satay", "Chwee_Kueh", "Bak_Kut_Teh",
    "Fried_Carrot_Cake_Black", "Fried_Carrot_Cake_White", "Mee_Rebus", "Mee_Soto",
    "Wanton_Mee_Dry", "Yong_Tau_Foo_Soup"
]

# Shuffle and split the specified food types into two halves
random.shuffle(specified_food_types)
half_index = len(specified_food_types) // 2
train_food_types = set(specified_food_types[:half_index])
test_food_types = set(specified_food_types[half_index:])

# Organize food items by directory name
food_items_by_type = defaultdict(list)

# Populate the dictionary with images and their corresponding weights
for item in data["food_data"]:
    file_path = item.get("file_path")
    directory_name = file_path.split('/')[1] if file_path else "unknown"
    weight = item.get("weight")

    # Skip items with missing/nil weight or not in the specified food types
    if weight is None or weight == "nil":
        continue

    # Add to the dictionary if it belongs to the specified food types
    if directory_name in train_food_types or directory_name in test_food_types:
        # Construct the expected image paths
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

# Collect training data from the first half of the food types
for directory_name in train_food_types:
    if directory_name in food_items_by_type:
        items = food_items_by_type[directory_name]
        if len(items) > 0:
            random.shuffle(items)
            train_data.append(items[0])  # Use one image per food type for training

# Collect testing data from the second half of the food types
for directory_name in test_food_types:
    if directory_name in food_items_by_type:
        items = food_items_by_type[directory_name]
        if len(items) > 0:
            random.shuffle(items)
            split_index = int(len(items) * 0.8)
            test_data.extend(items[split_index:])  # Use 20% for testing

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

print("Data split into train_data.txt and test_data.txt for unseen test data.")
