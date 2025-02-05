import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
USDA_API_URL = 'https://api.nal.usda.gov/fdc/v1/foods/search'

def search_ingredient(ingredient, mass):
    if not ingredient:
        print('No ingredient provided')
        return

    params = {
        'api_key': api_key,
        'query': ingredient,
        'pageSize': 1  # Request only the most relevant result
    }

    response = requests.get(USDA_API_URL, params=params)
    if response.status_code != 200:
        print('Failed to fetch data from USDA')
        return

    data = response.json()
    foods = data.get('foods', [])
    if foods:
        food = foods[0]  # Take the most relevant (first) food item
        details = [{'name': nutrient['nutrientName'], 'value':  round(nutrient['value'] * (mass / 100), 5)} for nutrient in food.get('foodNutrients', [])]
        result = {
            'name': food.get('description', 'Unknown'),
            'details': details
        }
        return result
    else:
        print('No matching ingredient found')


categories = {
    "Energy": "Energy (kcal)",
    "Protein": "Protein (g)",
    "Total lipid (fat)": "Total fat (g)",
    "Saturated fat": "Saturated fat (g)",
    "Dietary fibre": "Dietary fibre (g)",
    "Carbohydrate, by difference": "Carbohydrate (g)",
    "Cholesterol": "Cholesterol (mg)",
    "Sodium": "Sodium (mg)"
}
