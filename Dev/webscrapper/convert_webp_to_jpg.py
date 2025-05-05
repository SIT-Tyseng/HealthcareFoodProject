import os
from PIL import Image

def convert_webp_to_jpg(directory):
    """
    Convert all .webp images to .jpg in all subdirectories of the specified directory.
    Preserves the original folder structure and deletes the original .webp files after conversion.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.webp'):
                # Full path to the webp file
                webp_path = os.path.join(root, file)
                
                # New path with jpg extension
                jpg_path = os.path.join(root, os.path.splitext(file)[0] + '.jpg')
                
                try:
                    # Open the webp image
                    with Image.open(webp_path) as img:
                        # Convert to RGB if needed (webp might have alpha channel)
                        if img.mode in ('RGBA', 'P'):
                            img = img.convert('RGB')
                        
                        # Save as jpg with quality=90 (adjust as needed)
                        img.save(jpg_path, 'JPEG', quality=90)
                    
                    # Remove the original webp file
                    os.remove(webp_path)
                    print(f"Converted: {webp_path} -> {jpg_path}")
                
                except Exception as e:
                    print(f"Error converting {webp_path}: {str(e)}")

if __name__ == "__main__":
    # Specify your root directory here
    root_directory = "singapore_food_dataset"  # Change this to your directory path
    
    if os.path.exists(root_directory):
        convert_webp_to_jpg(root_directory)
        print("Conversion complete!")
    else:
        print(f"Directory not found: {root_directory}")