import os

def count_images_in_directory(directory):
    # Define common image file extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    
    # Initialize counter
    total_images = 0
    
    # Walk through directory and subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file has an image extension (case-insensitive)
            if os.path.splitext(file.lower())[1] in image_extensions:
                total_images += 1
    
    return total_images

# Example usage
folder_path = "UECFOOD256"  # Replace with your folder path
image_count = count_images_in_directory(folder_path)
print(f"Total number of images: {image_count}")