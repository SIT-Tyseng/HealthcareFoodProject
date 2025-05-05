from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import requests
import os
import time

# Set up Firefox with geckodriver
gecko_path = "/usr/local/bin/geckodriver"  # Replace with your geckodriver path
service = Service(gecko_path)
driver = webdriver.Firefox(service=service)

# Navigate to Google Images
keyword = "apple"
url = f"https://www.google.com/search?q={keyword}&tbm=isch"
driver.get(url)

# Scroll to load more images
for _ in range(3):  # Scroll 3 times, adjust as needed
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for images to load

# Create output directory
output_dir = "downloads/apple"
os.makedirs(output_dir, exist_ok=True)

# Find and download images
images = driver.find_elements(By.CSS_SELECTOR, "img.rg_i")  # Google Images class
for i, img in enumerate(images[:5], 1):  # Limit to 5 images
    src = img.get_attribute("src")
    if src and "http" in src:  # Check for valid URL
        try:
            response = requests.get(src, stream=True)
            response.raise_for_status()
            with open(f"{output_dir}/image{i}.jpg", "wb") as f:
                f.write(response.content)
            print(f"Downloaded image{i}.jpg")
        except Exception as e:
            print(f"Failed to download image {i}: {e}")

# Clean up
driver.quit()