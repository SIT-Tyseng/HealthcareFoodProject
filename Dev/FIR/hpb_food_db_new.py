import sqlite3
from fuzzywuzzy import fuzz, process

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
        best_match, match_score = process.extractOne(dish_name_normalized, matching_dishes, scorer=fuzz.token_set_ratio)

        if match_score >= 85:
            # Step 3: Fetch all nutritional values for the best-matched dish name
            cursor.execute("SELECT nutrient, numeric_value, unit FROM nutritional_values WHERE food_name = ?", (best_match,))
            results = cursor.fetchall()

            if results:
                return format_nutritional_values(results, best_match, dish_mass)
    else:
        # No matching dishes found using LIKE, try fuzzy matching against all dishes
        cursor.execute("SELECT DISTINCT food_name FROM nutritional_values")
        all_dishes = [row[0] for row in cursor.fetchall()]

        best_match, match_score = process.extractOne(dish_name_normalized, all_dishes, scorer=fuzz.token_set_ratio)

        if match_score >= 85:
            # Fetch all nutritional values for the best-matched dish name
            cursor.execute("SELECT nutrient, numeric_value, unit FROM nutritional_values WHERE food_name = ?", (best_match,))
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
