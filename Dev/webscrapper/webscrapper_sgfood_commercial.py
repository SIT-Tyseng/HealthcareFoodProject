import os
import requests
import time
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import random

# Free image sources with commercial licenses
SOURCES = [
    "Wikimedia Commons",
    "Flickr (CC licensed)",
    "Openverse",
    "Pixabay",
    "FoodiesFeed"
]

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

class CommercialScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.delay = random.uniform(1.5, 3.0)  # Random delay between requests

    def download_and_convert(self, url, save_path):
        """Download image and convert to JPEG with minimum size"""
        try:
            # Temporary file path
            temp_path = f"{save_path}.temp"
            
            # Download image
            response = self.session.get(url, stream=True, timeout=15)
            response.raise_for_status()
            
            # Save temporary file
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            
            # Process image
            with Image.open(temp_path) as img:
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if too small
                if img.width < 300 or img.height < 300:
                    ratio = max(300/img.width, 300/img.height)
                    new_size = (int(img.width*ratio), int(img.height*ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Save as high-quality JPEG
                img.save(save_path, 'JPEG', quality=90)
            
            os.remove(temp_path)
            return True
            
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            for path in [temp_path, save_path]:
                if os.path.exists(path):
                    os.remove(path)
            return False

    def scrape_wikimedia(self, query, count):
        """Scrape Wikimedia Commons (public domain/CC licenses)"""
        base_url = "https://commons.wikimedia.org"
        search_url = f"{base_url}/w/api.php?action=query&generator=images&prop=imageinfo&iiprop=url&format=json&titles={quote_plus(query)}"
        
        try:
            response = self.session.get(search_url, timeout=10)
            data = response.json()
            urls = []
            
            for page in data.get('query', {}).get('pages', {}).values():
                if 'imageinfo' in page:
                    urls.append(page['imageinfo'][0]['url'])
            
            return urls[:count]
        except Exception as e:
            print(f"Wikimedia error: {str(e)}")
            return []

    def scrape_flickr_cc(self, query, count):
        """Scrape CC-licensed Flickr images"""
        api_url = "https://api.flickr.com/services/rest/"
        params = {
            'method': 'flickr.photos.search',
            'api_key': 'YOUR_FLICKR_API_KEY',  # Get free key from https://www.flickr.com/services/api/
            'text': f"{query} Singapore food",
            'license': '4,5,6,9,10',  # CC licenses
            'per_page': count,
            'format': 'json',
            'nojsoncallback': 1,
            'sort': 'relevance'
        }
        
        try:
            response = self.session.get(api_url, params=params, timeout=10)
            data = response.json()
            urls = []
            
            for photo in data.get('photos', {}).get('photo', []):
                url = f"https://live.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}_b.jpg"
                urls.append(url)
            
            return urls[:count]
        except Exception as e:
            print(f"Flickr error: {str(e)}")
            return []

    def scrape_pixabay(self, query, count):
        """Use Pixabay API (requires free API key)"""
        api_url = "https://pixabay.com/api/"
        params = {
            'key': 'YOUR_PIXABAY_KEY',  # Get from https://pixabay.com/api/docs/
            'q': f"{query} Singapore food",
            'image_type': 'photo',
            'per_page': min(count, 200),
            'safesearch': 'true'
        }
        
        try:
            response = self.session.get(api_url, params=params, timeout=10)
            data = response.json()
            return [hit['largeImageURL'] for hit in data.get('hits', [])][:count]
        except Exception as e:
            print(f"Pixabay error: {str(e)}")
            return []

    def scrape_foodiesfeed(self, query, count):
        """Scrape FoodiesFeed (free food photos)"""
        search_url = f"https://www.foodiesfeed.com/?s={quote_plus(query)}"
        
        try:
            response = self.session.get(search_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            urls = []
            
            for img in soup.select('img.photo'):
                if img.get('src'):
                    urls.append(img['src'])
            
            return urls[:count]
        except Exception as e:
            print(f"FoodiesFeed error: {str(e)}")
            return []

    def get_images(self, query, count):
        """Get images from all available sources"""
        urls = []
        
        # Try sources in order until we get enough images
        sources = [
            self.scrape_wikimedia,
            self.scrape_flickr_cc,
            self.scrape_pixabay,
            self.scrape_foodiesfeed
        ]
        
        random.shuffle(sources)  # Distribute load
        
        for source in sources:
            if len(urls) >= count:
                break
            new_urls = source(query, count - len(urls))
            urls.extend(new_urls)
            time.sleep(self.delay)
        
        return urls[:count]

    def scrape(self, food_list, per_class, output_dir):
        """Main scraping function"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for food in food_list:
            class_dir = os.path.join(output_dir, food)
            if not os.path.exists(class_dir):
                os.makedirs(class_dir)
            
            print(f"\nScraping {food}...")
            urls = self.get_images(food, per_class)
            
            downloaded = 0
            for idx, url in enumerate(urls):
                save_path = os.path.join(class_dir, f"{food}_{idx+1}.jpg")
                if self.download_and_convert(url, save_path):
                    downloaded += 1
                    print(f"Downloaded {downloaded}/{per_class} - {url[:60]}...")
                    time.sleep(self.delay)
            
            print(f"Finished {food}: {downloaded} images")

if __name__ == "__main__":
    scraper = CommercialScraper()
    
    # Configuration
    OUTPUT_DIR = "commercial_food_images"
    IMAGES_PER_CLASS = 50
    
    # Start scraping
    scraper.scrape(SINGAPORE_FOODS, IMAGES_PER_CLASS, OUTPUT_DIR)