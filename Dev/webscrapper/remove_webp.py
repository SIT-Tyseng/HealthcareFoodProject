import os

def remove_webp_files(directory):
    """
    Remove all .webp files in all subdirectories of the specified directory
    """
    deleted_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.webp'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    deleted_count += 1
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {str(e)}")
    
    print(f"\nTotal .webp files deleted: {deleted_count}")

if __name__ == "__main__":
    target_directory = "singapore_food_dataset"  # Change this to your directory
    if os.path.exists(target_directory):
        remove_webp_files(target_directory)
    else:
        print(f"Directory not found: {target_directory}")