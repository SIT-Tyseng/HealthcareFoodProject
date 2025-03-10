import os
import json
import random
from sklearn.model_selection import train_test_split

# Set random seed for reproducibility
random.seed(42)

# Define the root directory of the UEC Food256 dataset
root_dir = './UECFOOD256'
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# Path to the category file
category_file = os.path.join(root_dir, 'category.txt')

# Read category.txt to create a mapping from category ID to dish name
id_to_name = {}
with open(category_file, 'r') as f:
    next(f)  # Skip header line ("id	name")
    for line in f:
        if line.strip():  # Ensure the line is not empty
            category_id, dish_name = line.strip().split('\t', 1)  # Split on first tab
            id_to_name[category_id] = dish_name

# Define a list of question variations with the same meaning
questions = [
    "What is the name of this dish?",
    "Do you know the name of this dish?",
    "Can you tell me what this dish is called?",
    "What is this food called?",
    "Please identify the name of this dish.",
    "What dish is shown in this image?",
    "Could you name this dish for me?",
    "Tell me the name of this food."
]

# Initialize an empty list to store VQA samples
dataset = []

# Traverse the dataset directory to collect image paths and generate samples
for category_id in os.listdir(root_dir):
    category_path = os.path.join(root_dir, category_id)
    # Check if it's a directory and corresponds to a category in id_to_name
    if os.path.isdir(category_path) and category_id in id_to_name:
        dish_name = id_to_name[category_id]
        # Iterate through image files in the category folder
        for image_file in os.listdir(category_path):
            if image_file.lower().endswith('.jpg'):  # Check for .jpg or .JPG extension
                image_path = os.path.join(category_path, image_file)
                # Randomly select a question variation
                question = random.choice(questions)
                # Create the conversation
                conversation = [
                    {"role": "user", "content": f"<image>\n{question}"},
                    {"role": "assistant", "content": f"This is a dish called {dish_name}."}
                ]
                # Create the sample
                sample = {
                    "id": dish_name,
                    "image": image_path,
                    "conversations": conversation
                }
                dataset.append(sample)

# Extract labels (dish names) for stratification
labels = [sample["id"] for sample in dataset]

# Split the dataset into train (85%) and test (15%) sets
train_data, test_data = train_test_split(
    dataset,
    test_size=0.15,  # 15% for test set
    stratify=labels,  # Stratify by dish name
    random_state=42   # For reproducibility
)

# Save the training dataset to vqa_train.json
with open(os.path.join(output_dir,'uecfood256_sharegpt_train.json'), 'w') as f:
    json.dump(train_data, f, indent=4)

# Save the test dataset to vqa_test.json
with open(os.path.join(output_dir,'uecfood256_sharegpt_test.json'), 'w') as f:
    json.dump(test_data, f, indent=4)

print("UECFood256 train and test datasets generated and saved to uecfood256_sharegpt_train.json and uecfood256_sharegpt_test.json")