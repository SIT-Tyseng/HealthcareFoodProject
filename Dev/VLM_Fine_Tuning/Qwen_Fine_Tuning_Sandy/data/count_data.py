import json

# Open and read the JSON file
# with open('uecfood256_sharegpt_test.json', 'r') as file:
with open('uecfood256_sharegpt_train.json', 'r') as file:
    data = json.load(file)  # Load JSON into a Python object

# Check the number of elements in the list
num_elements = len(data)
print(f"The list in .json file has {num_elements} elements.")