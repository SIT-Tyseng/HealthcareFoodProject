import json
import os
import random
from collections import defaultdict

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

# Convert the list to a set for faster lookup
specified_food_types_set = set(specified_food_types)

# Organize food items by directory name and weight (mass)
food_items_by_type_and_mass = defaultdict(lambda: defaultdict(list))

# Populate the dictionary with images and their corresponding weights
for item in data["food_data"]:
    file_path = item.get("file_path")
    if not file_path:
        continue  # Skip if file_path is missing
    parts = file_path.split('/')
    if len(parts) < 2:
        continue  # Skip if file_path doesn't have expected format
    directory_name = parts[1]
    weight = item.get("weight")

    # Skip items with missing/nil weight or not in the specified food types
    if weight is None or weight == "nil" or directory_name not in specified_food_types_set:
        continue

    # Construct the expected image paths
    # Navigate to the correct folder under SGFood
    subfolder = os.path.join(sg_food_dir, directory_name)
    base_file_name = os.path.basename(file_path)

    # Paths for different capitalization scenarios
    image_path_upper = os.path.join(subfolder, base_file_name.replace(".jpg", ".JPG"))
    image_path_lower = os.path.join(subfolder, base_file_name.replace(".JPG", ".jpg"))
    depth_image_path_upper = os.path.join(
        depth_maps_dir,
        base_file_name.replace(".jpg", "_depth.JPG").replace(".JPG", "_depth.JPG")
    )
    depth_image_path_lower = os.path.join(
        depth_maps_dir,
        base_file_name.replace(".jpg", "_depth.jpg").replace(".JPG", "_depth.jpg")
    )

    # Check if either regular image (upper or lower case) exists
    if not (os.path.exists(image_path_upper) or os.path.exists(image_path_lower)):
        continue  # Skip if neither regular image exists

    # Check if either depth image (upper or lower case) exists
    if not (os.path.exists(depth_image_path_upper) or os.path.exists(depth_image_path_lower)):
        continue  # Skip if neither depth image exists

    # Add to the dictionary grouped by directory and weight
    food_items_by_type_and_mass[directory_name][weight].append((file_path, weight))

# Split data into training and testing sets
train_data = []
test_data = []

# For each food type, select 4 images (from the same mass group) for training
# and split the remaining images into testing data
for directory_name in specified_food_types:
    if directory_name in food_items_by_type_and_mass:
        items_by_mass = food_items_by_type_and_mass[directory_name]
        # Filter mass groups that have at least 4 images
        mass_groups = [group for group in items_by_mass.values() if len(group) >= 4]
        if len(mass_groups) > 0:
            # Randomly select one mass group
            selected_group = random.choice(mass_groups)
            # Randomly select 4 images from the group
            random.shuffle(selected_group)
            selected_images = selected_group[:4]
            # Add these images to the training data
            train_data.extend(selected_images)

            # Remove the selected images from the group
            remaining_images = selected_group[4:] + [
                img for mass, group in items_by_mass.items()
                if group != selected_group for img in group
            ]

            # If there are remaining images, split them into testing data
            if remaining_images:
                random.shuffle(remaining_images)
                split_index = int(len(remaining_images) * 0.8)
                test_data.extend(remaining_images[split_index:])
        else:
            # If no mass group has at least 4 images, skip adding to training data
            # but still collect images for testing
            all_items = []
            for group in items_by_mass.values():
                all_items.extend(group)
            if all_items:
                random.shuffle(all_items)
                split_index = int(len(all_items) * 0.8)
                test_data.extend(all_items[split_index:])
    else:
        print(f"No data found for food type: {directory_name}")

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

print("Data split into train_data.txt and test_data.txt for seen data.")
