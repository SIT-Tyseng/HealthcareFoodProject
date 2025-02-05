import sqlite3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from fuzzywuzzy import fuzz, process
import re


def get_nutritional_values(dish_name, dish_mass):
    url = "https://focos.hpb.gov.sg/eservices/ENCF/foodsearch.aspx"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    output = f"Dish Name: {dish_name}\nNutritional Values:\n"

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'txtFoodName')))
        search_input = driver.find_element(By.ID, 'txtFoodName')
        search_input.send_keys(dish_name)
        per_100g_checkbox = driver.find_element(By.ID, 'rdPerServing_1')
        per_100g_checkbox.click()
        search_button = driver.find_element(By.ID, 'btnSearch')
        search_button.click()

        try:
            wait.until(EC.presence_of_element_located((By.ID, 'gvData')))
        except TimeoutException:
            try:
                no_records_element = driver.find_element(By.ID, 'divGVNoData')
                no_records_text = no_records_element.find_element(By.ID, 'lblGVReport').text
                if "No records!" in no_records_text:
                    return "Not found"
            except NoSuchElementException:
                pass

        first_result_checkbox = driver.find_element(By.ID, 'gvData_ctl02_chkDeleteThis')
        first_result_checkbox.click()
        confirm_button = driver.find_element(By.ID, 'btnConfirm')
        confirm_button.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table[style="border: solid 1px #c0ebfc;"]')))
        nutritional_table = driver.find_element(By.CSS_SELECTOR, 'table[style="border: solid 1px #c0ebfc;"]')
        rows = nutritional_table.find_elements(By.TAG_NAME, 'tr')

        for row in rows[1:]:
            cells = row.find_elements(By.TAG_NAME, 'td')
            nutrient = cells[0].text.strip()
            value = cells[1].text.strip()
            numeric_matches = re.findall(r'\d+\.?\d*', value)
            if numeric_matches:
                numeric_value = float(numeric_matches[0])
                unit = re.findall(r'[a-zA-Z]+', value)[-1]
                scale_factor = dish_mass / 100.0
                scaled_value = numeric_value * scale_factor
                output += f"{nutrient}: {scaled_value:.2f} {unit}\n"
            else:
                output += f"{nutrient}: 0.00\n"

        return output.strip()
    except (TimeoutException, NoSuchElementException) as e:
        return f"An error occurred: {e}"
    finally:
        driver.quit()

def get_nutritional_values_local(dish_name, dish_mass):
    # Connect to the SQLite database
    conn = sqlite3.connect("nutritional_values.db")
    cursor = conn.cursor()

    # Normalize dish name for better matching
    dish_name_normalized = dish_name.lower().strip()

    # Step 1: Attempt to find matching dish names in the database
    query = "SELECT DISTINCT food_name FROM nutritional_values WHERE LOWER(food_name) LIKE ?"
    cursor.execute(query, (f"%{dish_name_normalized}%",))
    matching_dishes = [row[0] for row in cursor.fetchall()]

    if matching_dishes:
        # Step 2: Use fuzzy matching among the matching dishes
        best_match, match_score = process.extractOne(dish_name_normalized, matching_dishes,
                                                     scorer=fuzz.token_set_ratio)

        if match_score >= 85:
            # Step 3: Fetch all nutritional values for the best-matched dish name
            cursor.execute("SELECT nutrient, numeric_value, unit FROM nutritional_values WHERE food_name = ?",
                           (best_match,))
            results = cursor.fetchall()

            if results:
                return format_nutritional_values(results, best_match, dish_mass)
    else:
        # No matching dishes found using LIKE, try fuzzy matching against all dishes
        cursor.execute("SELECT DISTINCT food_name FROM nutritional_values")
        all_dishes = [row[0] for row in cursor.fetchall()]

        best_match, match_score = process.extractOne(dish_name_normalized, all_dishes,
                                                     scorer=fuzz.token_set_ratio)

        if match_score >= 85:
            # Fetch all nutritional values for the best-matched dish name
            cursor.execute("SELECT nutrient, numeric_value, unit FROM nutritional_values WHERE food_name = ?",
                           (best_match,))
            results = cursor.fetchall()

            if results:
                return format_nutritional_values(results, best_match, dish_mass)

    return "Not found"

def format_nutritional_values(results, dish_name, dish_mass):
    output_lines = []
    output_lines.append(f"**Dish Name:** {dish_name}")
    output_lines.append(f"**Nutritional Values per {dish_mass}g:**\n")

    scale_factor = dish_mass / 100.0  # Assuming the values are per 100g in the database

    for nutrient, numeric_value, unit in results:
        scaled_value = numeric_value * scale_factor
        output_lines.append(f"- **{nutrient}:** {scaled_value:.2f} {unit}")

    return '\n'.join(output_lines)