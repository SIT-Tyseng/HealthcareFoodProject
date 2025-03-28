import os
import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import quote_plus
from PIL import Image

# List of 50 Singaporean food classes
SINGAPORE_FOODS = [
    "Ang_Ku_Kueh", "Ayam_Panggang", "Ayam_Penyet", "Bak_Chor_Mee", "Bak_Kut_Teh",
    "Ban_Mian_Dry", "Ban_Mian_Soup", "Big_Pau", "Black_Pepper_Crab", "Cereal_Prawns",
    "Char_Kway_Teow", "Char_Siew_Pau", "Char_Siew_Rice", "Char_Siu_Roasted_Pork_Rice",
    "Chee_Cheong_Fun", "Chendol", "Chicken_Rice_Roasted", "Chicken_Rice_Steamed",
    "Chicken_Rice_Steamed_Porridge", "Chilli_Crab", "Chinese_Dumplings", "Chwee_Kueh",
    "Claypot_Rice", "Congee", "Curry_Puff", "Duck_Rice", "Durian", "Economy_Bee_Hoon",
    "Economy_Rice", "Fan_Choy", "Fish_Ball_Noodle", "Fried_Carrot_Cake_Black",
    "Fried_Carrot_Cake_Mixed", "Fried_Carrot_Cake_White", "Fried_Dumplings",
    "Fried_Hokkien_Mee", "Fried_Rice", "Grilled_Fish_with_Rice", "Hainanese_Curry_Rice",
    "Har_Gow", "Kaya_Toast", "Ke_Kou_Mian", "Kway_Chap", "Laksa", "Lor_Mee",
    "Mala_Dry_Pot", "Mala_Soup", "Mee_Gerong", "Mee_Hoon_Kueh", "Mee_Rebus", "Mee_Siam",
    "Mee_Soto", "Muah_Chee", "Nasi_Briyani", "Nasi_Lemak", "Oyster_Omelette", "Pani_Puri",
    "Plain_Prata", "Prawn_Noodles_Dry", "Prawn_Noodles_Soup", "Putu_Piring", "Rice_Dumpling",
    "Roasted_Duck_Roasted_Pork_Rice", "Roasted_Pork_Rice", "Rojak", "Sambal_Kangkong",
    "Sambal_Sotong", "Sambal_Stingray", "Satay", "Siew_Mai", "Sliced_Fish_Soup", "Soon_Kueh",
    "Tang_Yuan", "Tau_Sar_Pau", "Wanton_Mee_Dry", "Wanton_Mee_Soup", "Xiao_Long_Bao",
    "Xingzhou_Bee_Hoon", "Yong_Tau_Foo_Dry", "Yong_Tau_Foo_Soup", "You_Mian"
]

def create_directories(base_path, classes):
    """Create directories for each food class"""
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    for food_class in classes:
        path = os.path.join(base_path, food_class.replace(' ', '_'))
        if not os.path.exists(path):
            os.makedirs(path)

def process_image(filepath, min_size=(300, 300)):
    """Resize image to meet minimum dimensions while maintaining aspect ratio"""
    try:
        with Image.open(filepath) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            original_width, original_height = img.size
            
            # Check if resizing is needed
            if original_width >= min_size[0] and original_height >= min_size[1]:
                return True

            # Calculate new dimensions maintaining aspect ratio
            ratio = max(min_size[0]/original_width, min_size[1]/original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            
            # Resize with high-quality Lanczos filter
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img.save(filepath, quality=95)
            return True
            
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return False

def bing_image_scraper(query, num_images, save_dir):
    """Scrape Bing Images with size validation and processing"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.bing.com/'
    }
    
    # Add size filter for images larger than 300x300
    size_filter = "+filterui:imagesize-medium"
    search_url = f"https://www.bing.com/images/search?q={quote_plus(query)}&qft={size_filter}&first=1"
    
    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Search failed: {str(e)}")
        return 0

    soup = BeautifulSoup(response.text, 'html.parser')
    images = []
    
    # Extract image URLs
    for img in soup.find_all('img', {'class': 'mimg'}):
        img_url = img.get('src') or img.get('data-src')
        if img_url and img_url.startswith('http'):
            images.append(img_url)

    downloaded = 0
    attempt = 0
    max_attempts = num_images * 3  # Allow more attempts for quality filtering
    
    while downloaded < num_images and attempt < max_attempts:
        if attempt >= len(images):
            break
            
        img_url = images[attempt]
        attempt += 1
        
        try:
            # Download image
            response = requests.get(img_url, headers=headers, stream=True, timeout=20)
            response.raise_for_status()
            
            # Determine file extension
            content_type = response.headers.get('content-type', '')
            if 'image/' in content_type:
                ext = content_type.split('/')[-1]
                if ext == 'jpeg':
                    ext = 'jpg'
            else:
                ext = 'jpg'

            # Create filename
            filename = os.path.join(save_dir, f"{query.replace(' ', '_')}_{attempt}.{ext}")
            
            # Save image
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            
            # Process and validate image
            if process_image(filename):
                downloaded += 1
                print(f"Downloaded {filename} ({downloaded}/{num_images})")
            else:
                continue  # Skip failed images
                
            time.sleep(0.75)  # Respectful delay
            
        except Exception as e:
            print(f"Error downloading image {attempt}: {str(e)}")
            continue
            
    return downloaded

def main():
    BASE_DIR = "singapore_food_dataset"
    IMAGES_PER_CLASS = 50  # Adjust this number as needed
    
    create_directories(BASE_DIR, SINGAPORE_FOODS)
    
    for food_class in SINGAPORE_FOODS:
        class_dir = os.path.join(BASE_DIR, food_class.replace(' ', '_'))
        print(f"\n=== Downloading {IMAGES_PER_CLASS} images for {food_class} ===")
        
        downloaded_count = bing_image_scraper(
            query=f"{food_class} Singapore local food",
            num_images=IMAGES_PER_CLASS,
            save_dir=class_dir
        )
        
        print(f"Successfully downloaded {downloaded_count} valid images for {food_class}")
        time.sleep(15)  # Extended delay between classes

if __name__ == "__main__":
    main()