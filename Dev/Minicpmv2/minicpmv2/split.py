import json
import random
from collections import defaultdict

def split_dataset(file_path, train_ratio=0.8, seed=42):
    random.seed(seed)
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    category_dict = defaultdict(list)
    images_with_mass = []

    # Group images by category and check for mass info
    for entry in data:
        category = entry['image'].split('/')[-2]  # Extract category from path
        category_dict[category].append(entry)
        if any("mass" in conv['content'].lower() for conv in entry['conversations']):
            images_with_mass.append(entry)
    
    train_set, test_set = [], []
    
    for category, entries in category_dict.items():
        random.shuffle(entries)
        split_index = int(len(entries) * train_ratio)
        
        # Split data
        train_set.extend(entries[:split_index])
        test_set.extend(entries[split_index:])
    
    # Ensure mass images are represented in both sets
    train_with_mass = [img for img in train_set if img in images_with_mass]
    test_with_mass = [img for img in test_set if img in images_with_mass]

    # Print final results
    print(f"Total images: {len(data)}")
    print(f"Training set: {len(train_set)} ({len(train_with_mass)} with mass info)")
    print(f"Testing set: {len(test_set)} ({len(test_with_mass)} with mass info)")
    
    return train_set, test_set

if __name__ == "__main__":
    input_file = "output_minicpm_format.json" # replace file path with all food images entries here
    train_set, test_set = split_dataset(input_file)

    # Save results
    with open("train.json", "w") as train_file:
        json.dump(train_set, train_file, indent=4)
    
    with open("test.json", "w") as test_file:
        json.dump(test_set, test_file, indent=4)
    
    print("Datasets split and saved as train.json and test.json.")
