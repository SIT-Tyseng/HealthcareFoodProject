import os
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import quote_plus
from PIL import Image
import io

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

def process_image(img_data, min_size=(300, 300)):
    """Process image data to ensure minimum size and JPEG format"""
    try:
        img = Image.open(io.BytesIO(img_data))

        print(f"img.width: {img.width}, img.height: {img.height}")
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'P', 'LA'):
            img = img.convert('RGB')
        
        # Skip if image is too small
        if img.width < min_size[0] or img.height < min_size[1]:
            return None
        
        # Create output buffer
        output_buffer = io.BytesIO()
        
        # Save as JPEG with quality preservation
        img.save(output_buffer, format='JPEG', quality=90)
        
        return output_buffer.getvalue()
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None

def bing_image_scraper(query, num_images, save_dir):
    """Scrape Bing Images with size and format validation"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.bing.com/'
    }
    
    # Size filter for "medium" (typically 300x300 or larger) and photo type
    search_url = f"https://www.bing.com/images/search?q={quote_plus(query)}&qft=+filterui:imagesize-medium+filterui:photo-photo"
    
    try:
        response = requests.get(search_url, headers=headers, timeout=20)
        response.raise_for_status()
    except Exception as e:
        print(f"Search failed: {str(e)}")
        return 0

    soup = BeautifulSoup(response.text, 'html.parser')
    image_elements = soup.find_all('a', {'class': 'iusc'})
    
    downloaded = 0
    attempt = 0
    
    while downloaded < num_images and attempt < len(image_elements):
        try:
            # Extract JSON data containing higher resolution URL
            json_data = image_elements[attempt].get('m')
            if not json_data:
                attempt += 1
                continue
                
            image_info = eval(json_data)
            img_url = image_info.get('murl')
            if not img_url:
                attempt += 1
                continue
                
            # Download image with stream to handle large files
            img_response = requests.get(img_url, headers=headers, stream=True, timeout=30)
            img_response.raise_for_status()
            
            # Read image data
            img_data = img_response.content
            
            # Process image
            processed_img = process_image(img_data)
            if not processed_img:
                attempt += 1
                continue
                
            # Save image
            filename = os.path.join(save_dir, f"{query.replace(' ', '_')}_{downloaded+1}.jpg")
            with open(filename, 'wb') as f:
                f.write(processed_img)
                
            downloaded += 1
            print(f"Downloaded {filename} ({downloaded}/{num_images})")
            attempt += 1
            
            # Respectful delay between requests
            time.sleep(1.5)
            
        except Exception as e:
            print(f"Error downloading image {attempt+1}: {str(e)}")
            attempt += 1
            continue
            
    return downloaded

def main():
    BASE_DIR = "sg_food_images_3"
    IMAGES_PER_CLASS = 100  # Number of images to download per food category
    
    create_directories(BASE_DIR, SINGAPORE_FOODS)
    
    for food_class in SINGAPORE_FOODS:
        class_dir = os.path.join(BASE_DIR, food_class.replace(' ', '_'))
        print(f"\n=== Downloading {IMAGES_PER_CLASS} images for {food_class} ===")
        
        downloaded_count = bing_image_scraper(
            query=f"{food_class} Singapore food",
            num_images=IMAGES_PER_CLASS,
            save_dir=class_dir
        )
        
        print(f"Successfully downloaded {downloaded_count} images for {food_class}")
        
        # Longer delay between categories to avoid rate limiting
        time.sleep(20)

if __name__ == "__main__":
    main()