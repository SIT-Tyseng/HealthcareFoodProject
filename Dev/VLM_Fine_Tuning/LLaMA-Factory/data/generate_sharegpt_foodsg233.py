import os
import json
import random
from sklearn.model_selection import train_test_split

# Set random seed for reproducibility
random.seed(42)

# Define the root directory of the dataset
root_dir = '../custom_data/foodsg-233_sample'

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

# Initialize lists to store samples and labels
dataset = []
labels = []

# Traverse the dataset directory to collect image paths and generate samples
for dish_name in os.listdir(root_dir):
    dish_path = os.path.join(root_dir, dish_name)
    # Check if it's a directory
    if os.path.isdir(dish_path):
        # Iterate through image files in the dish folder
        for image_file in os.listdir(dish_path):
            if image_file.lower().endswith('.jpg'):  # Case-insensitive check for .jpg
                image_path = os.path.join(dish_path, image_file)
                # Create the user and assistant messages with the specified format
                question = random.choice(questions)
                user_message = {"content": f"<image>{question}", "role": "user"}
                assistant_message = {"content": f"This is a dish called {dish_name}.", "role": "assistant"}
                # Create the sample in the required format
                sample = {
                    "messages": [user_message, assistant_message],
                    "images": [image_path]
                }
                dataset.append(sample)
                labels.append(dish_name)

# Split the dataset into train (85%) and test (15%) sets using stratified sampling
train_data, test_data = train_test_split(
    dataset,
    test_size=0.15,  # 15% for test set
    stratify=labels,  # Stratify by dish name
    random_state=42   # For reproducibility
)

# Save the training dataset to foodsg233_sharegpt_train.json
with open('foodsg233_sharegpt_train.json', 'w') as f:
    json.dump(train_data, f, indent=4)

# Save the test dataset to foodsg233_sharegpt_test.json
with open('foodsg233_sharegpt_test.json', 'w') as f:
    json.dump(test_data, f, indent=4)

print("Foodsg-233 train and test datasets generated and saved to foodsg233_sharegpt_train.json and foodsg233_sharegpt_test.json")