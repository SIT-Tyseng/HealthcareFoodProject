import os
import json
from sklearn.model_selection import train_test_split

# Paths
dataset_dir = "/storage/UECFOOD256"
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# Load category names
category_map = {}
with open(os.path.join(dataset_dir, "category.txt"), "r") as f:
    lines = f.readlines()[1:]  # Skip header
    for line in lines:
        idx, name = line.strip().split("\t")
        category_map[int(idx)] = name

# Collect all image paths and labels
dataset = []
for cat_id in range(1, 257):
    cat_dir = os.path.join(dataset_dir, str(cat_id))
    if not os.path.exists(cat_dir):
        continue
    for img_file in os.listdir(cat_dir):
        if img_file.endswith(".jpg"):
            img_path = os.path.join(cat_dir, img_file)
            dataset.append({
                "instruction": "What is the name of the dish?",
                "input": f"<image>{img_path}</image>",
                "output": f"This is {category_map[cat_id]}.",
                "label": cat_id - 1  # For stratification
            })

# Split: 85% train, 15% test
images = [entry["input"] for entry in dataset]
labels = [entry["label"] for entry in dataset]
train_imgs, test_imgs, _, _ = train_test_split(
    images, labels, test_size=0.15, stratify=labels, random_state=42
)

# Rebuild datasets
train_data = [d for d in dataset if d["input"] in train_imgs]
test_data = [d for d in dataset if d["input"] in test_imgs]

# Remove label field
for split in (train_data, test_data):
    for entry in split:
        del entry["label"]

# Save to JSON files
with open(os.path.join(output_dir, "uecfood256_train_alpaca.json"), "w") as f:
    json.dump(train_data, f, indent=2)
with open(os.path.join(output_dir, "uecfood256_test_alpaca.json"), "w") as f:
    json.dump(test_data, f, indent=2)

print(f"Train: {len(train_data)}, Test: {len(test_data)}")