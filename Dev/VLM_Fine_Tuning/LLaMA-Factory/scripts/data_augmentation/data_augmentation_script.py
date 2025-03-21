import matplotlib.pyplot as plt
from PIL import Image
import torchvision.transforms as transforms

def save_all_augmented_images(image_path, output_path="augmented_images_grid.png"):
    # Load the image and convert to RGB
    original_image = Image.open(image_path).convert('RGB')
    
    # Define individual augmentations
    augmentations = [
        ("RandomHorizontalFlip", transforms.RandomHorizontalFlip(p=1.0)),  # p=1.0 to ensure it applies
        ("ColorJitter", transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1)),
        ("RandomRotation", transforms.RandomRotation(degrees=15)),
        # ("RandomCrop", transforms.RandomCrop(size=(448, 448), padding=50, fill=(128, 128, 128), padding_mode='constant')),
        ("GaussianBlur", transforms.GaussianBlur(kernel_size=3)),
        ("RandomGrayscale", transforms.RandomGrayscale(p=1.0)),  # p=1.0 to ensure it applies
    ]
    
    # Generate augmented images
    augmented_images = [(name, transform(original_image)) for name, transform in augmentations]
    
    # Create a 2x3 subplot grid (including original image)
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))  # 2 rows, 3 columns
    
    # Flatten axes for easier indexing
    axes = axes.flatten()
    
    # Plot original image in the first slot
    axes[0].imshow(original_image)
    axes[0].set_title('Original')
    axes[0].axis('off')
    
    # Plot augmented images in remaining slots
    for i, (name, aug_img) in enumerate(augmented_images):
        axes[i + 1].imshow(aug_img)
        axes[i + 1].set_title(name)
        axes[i + 1].axis('off')
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    
    # Save the figure to a file
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Images saved to {output_path}")
    
    # Optionally display the plot
    plt.show()

# Example usage (replace with your image path)
image_path = 'food.jpg'  # Update this to your image file
save_all_augmented_images(image_path, output_path='augmented_images_grid.png')