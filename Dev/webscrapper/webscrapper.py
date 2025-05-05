from google_images_download import google_images_download
import os
def read_food_classes(filename):
    with open(filename, 'r') as f:
        food_classes = [line.strip() for line in f.readlines()]
    return food_classes

folder_name = "sg-food-webscrapped"
food_classes = read_food_classes('food_classes.txt')
keywords = [fc + " in Singapore" for fc in food_classes]

num_images_per_class = len(keywords)

# arguments = {
#     "keywords": keywords,
#     "limit": num_images_per_class,
#     "delay": 1,
#     "print_urls": True,
#     "output_directory": folder_name,
# }

arguments = {
    "keywords": "red apple",
    "limit": 10,
    "delay": 5,
    "chromedriver": "chromedriver.exe",
    "print_urls": True,
    "output_directory": folder_name,
}

response = google_images_download.googleimagesdownload()
paths = response.download(arguments)
print(paths)

# for folder in os.listdir(folder_name):
#     if os.path.isdir(os.path.join(folder_name, folder)):
#         new_name = folder.replace(" in Singapore", "").replace("-", " ")
#         os.rename(
#             os.path.join(folder_name, folder),
#             os.path.join(folder_name, new_name)
#         )