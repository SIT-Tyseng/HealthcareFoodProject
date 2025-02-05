import sqlite3

def insert_dishes_and_allergens():
    conn = sqlite3.connect('instance/site.db')  # Update the path if necessary
    cursor = conn.cursor()

    # Define new health conditions (add only if not already present)
    health_conditions = [
        'Nut Allergy',
        'Shellfish Allergy',
        'Lactose Intolerance',
        'Gluten Allergy',
        'Egg Allergy',
        'Soy Allergy',
        'Fish Allergy',
        'Peanut Allergy',
        'Tree Nut Allergy',
        'Sesame Allergy',
        'Wheat Allergy',
        'Red Meat Allergy',
        'Mustard Allergy',
        'Legume Allergy',
        'Poultry Allergy',
        'Coconut Allergy',
        'Mollusk Allergy',
        # New health conditions to add
        'Garlic Allergy',
        'Mushroom Allergy',
        'Sulphite Sensitivity',
        'Dairy Allergy',
        'Onion Allergy',
        'Spice Allergy',
        'Nightshade Allergy',
        'Ginger Allergy',
        'Saffron Allergy',
        'Durian Allergy',
        'Banana Allergy',
        'FODMAP Sensitivity',
        'Sugar Sensitivity',
    ]

    # Insert new health conditions
    condition_ids = {}
    for condition in health_conditions:
        # Check if the condition already exists
        cursor.execute("SELECT id FROM health_conditions WHERE condition_name = ? AND user_id IS NULL", (condition,))
        result = cursor.fetchone()
        if result:
            condition_id = result[0]
        else:
            cursor.execute("INSERT INTO health_conditions (condition_name) VALUES (?)", (condition,))
            condition_id = cursor.lastrowid
        condition_ids[condition] = condition_id

    # Define new ingredients (excluding those already in the database)
    ingredients = [
        'Mushrooms',
        'Garlic',
        'Ginger',
        'Onions',
        'Shallots',
        'Leeks',
        'Preserved Radish',
        'Palm Sugar',
        'Mustard Seeds',
        'Egg Yolk',
        'Egg White',
        'Coconut Milk',
        'Coconut',
        'Clams',
        'Squid',
        'Cockles',
        'Oysters',
        'Mustard Oil',
        'Baguette',
        'Semolina',
        'Tapioca Starch',
        'Chickpeas',
        'Lentils',
        'Red Beans',
        'Mung Beans',
        'Chinese Sausage',
        'Flat Rice Noodles',
        'Rice Vermicelli',
        'Curry Leaves',
        'Curry Powder',
        'Curry Paste',
        'Herbs and Spices',
        'Pepper',
        'Banana Leaf',
        'Kaya',
        'Salted Egg Yolk',
        'Sweet Potato',
        'Tamarind',
        'Belacan',
        'Dried Shrimp',
        'Sambal Belacan',
        'Spices',
        'Fish Sauce',
        'Stingray',
        'Sliced Fish',
        'Grilled Fish',
        'Egg Noodles',
        'Kicap Manis',
        'Soybeans',
        'Soy Milk',
        'Miso',
        'Margarine',
        'Condensed Milk',
        'Evaporated Milk',
        'Groundnuts',
        'Pistachios',
        'Walnuts',
        'Sichuan Peppercorns',
        'Star Anise',
        'Cinnamon',
        'Potatoes',
        'Tomato Sauce',
        'Chili Peppers',
        'Eggplant',
        'Saffron',
        'Durian Fruit',
        'Vinegar',
        'Wine',
        'Dried Fruits',
        'Sugar',
        # Existing ingredients to ensure they are accounted for
        'Pork',
        'Chicken',
        'Duck',
        'Mutton',
        'Beef',
        'Fish',
        'Prawns',
        'Crab',
        'Egg',
        'Tofu',
        'Tempeh',
        'Wheat Flour',
        'Rice',
        'Glutinous Rice',
        'Rice Flour',
        'Noodles',
        'Bread',
        'Butter',
        'Ghee',
        'Yogurt',
        'Milk Powder',
        'Peanuts',
        'Almonds',
        'Cashews',
        'Sesame Oil',
        'Sesame Seeds',
        'Soy Sauce',
        'Oyster Sauce',
        'Shrimp Paste',
        'Sambal Chili',
        'Peanut Sauce',
        'Mayonnaise',
        'Anchovies',
        'Fish Balls',
        'Fish Cake',
        'Fish Paste',
    ]

    # Insert new ingredients
    ingredient_ids = {}
    for ingredient in ingredients:
        # Check if the ingredient already exists
        cursor.execute("SELECT id FROM ingredients WHERE ingredient_name = ?", (ingredient,))
        result = cursor.fetchone()
        if result:
            ingredient_id = result[0]
        else:
            cursor.execute("INSERT INTO ingredients (ingredient_name) VALUES (?)", (ingredient,))
            ingredient_id = cursor.lastrowid
        ingredient_ids[ingredient] = ingredient_id

    # Define new foods (excluding those already in the database)
    foods = [
        'Ang Ku Kueh',
        'Ayam Panggang',
        'Ayam Penyet',
        'Bak Chor Mee',
        'Bak Kut Teh',
        'Ban Mian Dry',
        'Ban Mian Soup',
        'Big Pau',
        'Black Pepper Crab',
        'Cereal Prawns',
        'Char Kway Teow',
        'Char Siew Pau',
        'Char Siew Rice',
        'Char Siu Roasted Pork Rice',
        'Chee Cheong Fun',
        'Chendol',
        'Chicken Rice Roasted',
        'Chicken Rice Steamed',
        'Chicken Rice Steamed Porridge',
        'Chilli Crab',
        'Chinese Dumplings',
        'Chwee Kueh',
        'Claypot Rice',
        'Congee',
        'Curry Puff',
        'Duck Rice',
        'Durian',
        'Economy Bee Hoon',
        'Economy Rice',
        'Fan Choy',
        'Fish Ball Noodle',
        'Fried Carrot Cake Black',
        'Fried Carrot Cake Mixed',
        'Fried Carrot Cake White',
        'Fried Dumplings',
        'Fried Hokkien Mee',
        'Fried Rice',
        'Grilled Fish with Rice',
        'Hainanese Curry Rice',
        'Har Gow',
        'Kaya Toast',
        'Ke Kou Mian',
        'Kway Chap',
        'Laksa',
        'Lor Mee',
        'Mala Dry Pot',
        'Mala Soup',
        'Mee Goreng',
        'Mee Hoon Kueh',
        'Mee Rebus',
        'Mee Siam',
        'Mee Soto',
        'Muah Chee',
        'Nasi Briyani',
        'Nasi Lemak',
        'Oyster Omelette',
        'Pani Puri',
        'Plain Prata',
        'Prawn Noodles Dry',
        'Prawn Noodles Soup',
        'Putu Piring',
        'Rice Dumpling',
        'Roasted Duck Roasted Pork Rice',
        'Roasted Pork Rice',
        'Rojak',
        'Sambal Kangkong',
        'Sambal Sotong',
        'Sambal Stingray',
        'Satay',
        'Siew Mai',
        'Sliced Fish Soup',
        'Soon Kueh',
        'Tang Yuan',
        'Tau Sar Pau',
        'Wanton Mee Dry',
        'Wanton Mee Soup',
        'Xiao Long Bao',
        'Xingzhou Bee Hoon',
        'Yong Tau Foo Dry',
        'Yong Tau Foo Soup',
        'You Mian',
        'Youtiao',
    ]

    # Insert new foods
    food_ids = {}
    for food in foods:
        # Check if the food already exists
        cursor.execute("SELECT id FROM food_items WHERE food_name = ?", (food,))
        result = cursor.fetchone()
        if result:
            food_id = result[0]
        else:
            cursor.execute("INSERT INTO food_items (food_name) VALUES (?)", (food,))
            food_id = cursor.lastrowid
        food_ids[food] = food_id

    # Map ingredients to health conditions (which ingredients cause which allergies)
    ingredient_condition_relations = [
        # Red Meat Allergy
        ('Pork', 'Red Meat Allergy'),
        ('Pork Ribs', 'Red Meat Allergy'),
        ('Pork Liver', 'Red Meat Allergy'),
        ('Beef', 'Red Meat Allergy'),
        ('Mutton', 'Red Meat Allergy'),

        # Poultry Allergy
        ('Chicken', 'Poultry Allergy'),
        ('Duck', 'Poultry Allergy'),

        # Fish Allergy
        ('Fish', 'Fish Allergy'),
        ('Stingray', 'Fish Allergy'),
        ('Fish Balls', 'Fish Allergy'),
        ('Fish Cake', 'Fish Allergy'),
        ('Fish Paste', 'Fish Allergy'),
        ('Anchovies', 'Fish Allergy'),
        ('Fish Sauce', 'Fish Allergy'),
        ('Sliced Fish', 'Fish Allergy'),
        ('Grilled Fish', 'Fish Allergy'),

        # Shellfish Allergy
        ('Prawns', 'Shellfish Allergy'),
        ('Shrimp Paste', 'Shellfish Allergy'),
        ('Dried Shrimp', 'Shellfish Allergy'),
        ('Crab', 'Shellfish Allergy'),
        ('Belacan', 'Shellfish Allergy'),
        ('Sambal Belacan', 'Shellfish Allergy'),
        ('Sambal Chili', 'Shellfish Allergy'),  # If contains shrimp paste
        ('Oyster Sauce', 'Shellfish Allergy'),

        # Mollusk Allergy
        ('Squid', 'Mollusk Allergy'),
        ('Cockles', 'Mollusk Allergy'),
        ('Clams', 'Mollusk Allergy'),
        ('Oysters', 'Mollusk Allergy'),
        ('Cuttlefish', 'Mollusk Allergy'),
        ('Sotong', 'Mollusk Allergy'),

        # Egg Allergy
        ('Egg', 'Egg Allergy'),
        ('Egg Yolk', 'Egg Allergy'),
        ('Egg White', 'Egg Allergy'),
        ('Egg Noodles', 'Egg Allergy'),
        ('Mayonnaise', 'Egg Allergy'),
        ('Kaya', 'Egg Allergy'),
        ('Chiffon Cake', 'Egg Allergy'),  # If applicable

        # Soy Allergy
        ('Tofu', 'Soy Allergy'),
        ('Tempeh', 'Soy Allergy'),
        ('Soy Sauce', 'Soy Allergy'),
        ('Kicap Manis', 'Soy Allergy'),
        ('Soybeans', 'Soy Allergy'),
        ('Soy Milk', 'Soy Allergy'),
        ('Miso', 'Soy Allergy'),  # If applicable

        # Gluten and Wheat Allergy
        ('Wheat Flour', 'Gluten Allergy'),
        ('Wheat Flour', 'Wheat Allergy'),
        ('Semolina', 'Gluten Allergy'),
        ('Semolina', 'Wheat Allergy'),
        ('Baguette', 'Gluten Allergy'),
        ('Baguette', 'Wheat Allergy'),
        ('Bread', 'Gluten Allergy'),
        ('Bread', 'Wheat Allergy'),
        ('You Tiao', 'Gluten Allergy'),
        ('You Tiao', 'Wheat Allergy'),
        ('Egg Noodles', 'Gluten Allergy'),
        ('Egg Noodles', 'Wheat Allergy'),
        ('Noodles', 'Gluten Allergy'),
        ('Noodles', 'Wheat Allergy'),
        ('Soy Sauce', 'Gluten Allergy'),  # Due to wheat content
        ('Soy Sauce', 'Wheat Allergy'),
        ('Kicap Manis', 'Gluten Allergy'),
        ('Kicap Manis', 'Wheat Allergy'),
        ('Oyster Sauce', 'Gluten Allergy'),  # If contains wheat
        ('Sambal Belacan', 'Gluten Allergy'),  # If contains wheat

        # Dairy Allergy and Lactose Intolerance
        ('Butter', 'Dairy Allergy'),
        ('Butter', 'Lactose Intolerance'),
        ('Ghee', 'Dairy Allergy'),
        ('Ghee', 'Lactose Intolerance'),
        ('Milk Powder', 'Dairy Allergy'),
        ('Milk Powder', 'Lactose Intolerance'),
        ('Yogurt', 'Dairy Allergy'),
        ('Yogurt', 'Lactose Intolerance'),
        ('Cheese', 'Dairy Allergy'),  # If applicable
        ('Cream', 'Dairy Allergy'),  # If applicable
        ('Margarine', 'Dairy Allergy'),  # If contains milk derivatives
        ('Condensed Milk', 'Dairy Allergy'),
        ('Evaporated Milk', 'Dairy Allergy'),

        # Peanut and Nut Allergy
        ('Peanuts', 'Peanut Allergy'),
        ('Peanuts', 'Nut Allergy'),
        ('Peanut Sauce', 'Peanut Allergy'),
        ('Peanut Sauce', 'Nut Allergy'),
        ('Groundnuts', 'Peanut Allergy'),

        # Tree Nut Allergy
        ('Almonds', 'Tree Nut Allergy'),
        ('Cashews', 'Tree Nut Allergy'),
        ('Chestnuts', 'Tree Nut Allergy'),
        ('Pistachios', 'Tree Nut Allergy'),  # If applicable
        ('Walnuts', 'Tree Nut Allergy'),  # If applicable

        # Sesame Allergy
        ('Sesame Seeds', 'Sesame Allergy'),
        ('Sesame Oil', 'Sesame Allergy'),

        # Mustard Allergy
        ('Mustard Seeds', 'Mustard Allergy'),
        ('Mustard Oil', 'Mustard Allergy'),
        ('Curry Powder', 'Mustard Allergy'),  # If contains mustard
        ('Curry Paste', 'Mustard Allergy'),

        # Coconut Allergy
        ('Coconut', 'Coconut Allergy'),
        ('Coconut Milk', 'Coconut Allergy'),
        ('Kaya', 'Coconut Allergy'),

        # Legume Allergy
        ('Chickpeas', 'Legume Allergy'),
        ('Lentils', 'Legume Allergy'),
        ('Red Beans', 'Legume Allergy'),
        ('Mung Beans', 'Legume Allergy'),
        ('Green Beans', 'Legume Allergy'),
        ('Peas', 'Legume Allergy'),  # If applicable
        ('Soybeans', 'Legume Allergy'),

        # Mushroom Allergy
        ('Mushrooms', 'Mushroom Allergy'),
        ('Shiitake Mushrooms', 'Mushroom Allergy'),

        # Garlic Allergy
        ('Garlic', 'Garlic Allergy'),

        # Onion Allergy
        ('Onions', 'Onion Allergy'),
        ('Shallots', 'Onion Allergy'),
        ('Leeks', 'Onion Allergy'),

        # Sulphite Sensitivity
        ('Preserved Radish', 'Sulphite Sensitivity'),
        ('Dried Fruits', 'Sulphite Sensitivity'),  # If applicable
        ('Vinegar', 'Sulphite Sensitivity'),  # If applicable
        ('Wine', 'Sulphite Sensitivity'),  # If applicable

        # Spice Allergy
        ('Herbs and Spices', 'Spice Allergy'),
        ('Curry Leaves', 'Spice Allergy'),
        ('Sichuan Peppercorns', 'Spice Allergy'),
        ('Star Anise', 'Spice Allergy'),
        ('Cinnamon', 'Spice Allergy'),

        # Nightshade Allergy
        ('Potatoes', 'Nightshade Allergy'),
        ('Tomato Sauce', 'Nightshade Allergy'),
        ('Chili Peppers', 'Nightshade Allergy'),
        ('Eggplant', 'Nightshade Allergy'),  # If applicable

        # Other Allergies
        ('Ginger', 'Ginger Allergy'),  # Rare
        ('Saffron', 'Saffron Allergy'),  # Rare
        ('Durian', 'Durian Allergy'),  # Rare
        ('Banana Leaf', 'Banana Allergy'),  # Rare, mainly for severe cases

        # FODMAP Sensitivity (for those with IBS)
        ('Garlic', 'FODMAP Sensitivity'),
        ('Onions', 'FODMAP Sensitivity'),
        ('Wheat Flour', 'FODMAP Sensitivity'),
        ('Legumes', 'FODMAP Sensitivity'),  # General category
        ('Milk', 'FODMAP Sensitivity'),

        # Sugar Sensitivity (for those with sugar intolerance)
        ('Palm Sugar', 'Sugar Sensitivity'),
        ('Sugar', 'Sugar Sensitivity'),

        # Add any additional ingredient-condition relationships as necessary
    ]

    # Map foods to ingredients (which foods contain which ingredients)
    # Map foods to ingredients (which foods contain which ingredients)
    food_ingredient_relations = []

    # 1. Ang Ku Kueh
    food_ingredient_relations.extend([
        ('Ang Ku Kueh', 'Glutinous Rice Flour'),
        ('Ang Ku Kueh', 'Mung Beans'),  # For mung bean filling
        ('Ang Ku Kueh', 'Peanuts'),  # If peanut filling is used
        ('Ang Ku Kueh', 'Sugar'),
        ('Ang Ku Kueh', 'Vegetable Oil'),
        ('Ang Ku Kueh', 'Food Coloring'),
    ])

    # 2. Ayam Panggang
    food_ingredient_relations.extend([
        ('Ayam Panggang', 'Chicken'),
        ('Ayam Panggang', 'Spices'),
        ('Ayam Panggang', 'Garlic'),
        ('Ayam Panggang', 'Onions'),
        ('Ayam Panggang', 'Coconut Milk'),
    ])

    # 3. Ayam Penyet
    food_ingredient_relations.extend([
        ('Ayam Penyet', 'Chicken'),
        ('Ayam Penyet', 'Sambal Chili'),
        ('Ayam Penyet', 'Tempeh'),
        ('Ayam Penyet', 'Tofu'),
        ('Ayam Penyet', 'Cabbage'),
        ('Ayam Penyet', 'Cucumber'),
    ])

    # 4. Bak Chor Mee
    food_ingredient_relations.extend([
        ('Bak Chor Mee', 'Egg Noodles'),
        ('Bak Chor Mee', 'Pork'),
        ('Bak Chor Mee', 'Minced Pork'),
        ('Bak Chor Mee', 'Pork Liver'),
        ('Bak Chor Mee', 'Mushrooms'),
        ('Bak Chor Mee', 'Vinegar'),
        ('Bak Chor Mee', 'Soy Sauce'),
        ('Bak Chor Mee', 'Chili'),
    ])

    # 5. Bak Kut Teh
    food_ingredient_relations.extend([
        ('Bak Kut Teh', 'Pork Ribs'),
        ('Bak Kut Teh', 'Garlic'),
        ('Bak Kut Teh', 'Pepper'),
        ('Bak Kut Teh', 'Herbs and Spices'),
        ('Bak Kut Teh', 'Soy Sauce'),
    ])

    # 6. Ban Mian Dry
    food_ingredient_relations.extend([
        ('Ban Mian Dry', 'Wheat Flour'),
        ('Ban Mian Dry', 'Minced Pork'),
        ('Ban Mian Dry', 'Anchovies'),
        ('Ban Mian Dry', 'Egg'),
        ('Ban Mian Dry', 'Vegetables'),
        ('Ban Mian Dry', 'Soy Sauce'),
    ])

    # 7. Ban Mian Soup
    food_ingredient_relations.extend([
        ('Ban Mian Soup', 'Wheat Flour'),
        ('Ban Mian Soup', 'Minced Pork'),
        ('Ban Mian Soup', 'Anchovies'),
        ('Ban Mian Soup', 'Egg'),
        ('Ban Mian Soup', 'Vegetables'),
        ('Ban Mian Soup', 'Soup Stock'),
    ])

    # 8. Big Pau
    food_ingredient_relations.extend([
        ('Big Pau', 'Wheat Flour'),
        ('Big Pau', 'Pork'),
        ('Big Pau', 'Egg'),
        ('Big Pau', 'Mushrooms'),
        ('Big Pau', 'Soy Sauce'),
    ])

    # 9. Black Pepper Crab
    food_ingredient_relations.extend([
        ('Black Pepper Crab', 'Crab'),
        ('Black Pepper Crab', 'Black Pepper'),
        ('Black Pepper Crab', 'Butter'),
        ('Black Pepper Crab', 'Soy Sauce'),
        ('Black Pepper Crab', 'Garlic'),
        ('Black Pepper Crab', 'Onions'),
    ])

    # 10. Cereal Prawns
    food_ingredient_relations.extend([
        ('Cereal Prawns', 'Prawns'),
        ('Cereal Prawns', 'Cereal'),
        ('Cereal Prawns', 'Butter'),
        ('Cereal Prawns', 'Egg Yolk'),
        ('Cereal Prawns', 'Curry Leaves'),
        ('Cereal Prawns', 'Chili'),
        ('Cereal Prawns', 'Milk Powder'),
    ])

    # 11. Char Kway Teow
    food_ingredient_relations.extend([
        ('Char Kway Teow', 'Flat Rice Noodles'),
        ('Char Kway Teow', 'Soy Sauce'),
        ('Char Kway Teow', 'Egg'),
        ('Char Kway Teow', 'Chinese Sausage'),
        ('Char Kway Teow', 'Fish Cake'),
        ('Char Kway Teow', 'Cockles'),
        ('Char Kway Teow', 'Bean Sprouts'),
        ('Char Kway Teow', 'Chives'),
        ('Char Kway Teow', 'Garlic'),
    ])

    # 12. Char Siew Pau
    food_ingredient_relations.extend([
        ('Char Siew Pau', 'Wheat Flour'),
        ('Char Siew Pau', 'Pork'),
        ('Char Siew Pau', 'Soy Sauce'),
        ('Char Siew Pau', 'Oyster Sauce'),
    ])

    # 13. Char Siew Rice
    food_ingredient_relations.extend([
        ('Char Siew Rice', 'Pork'),
        ('Char Siew Rice', 'Rice'),
        ('Char Siew Rice', 'Soy Sauce'),
        ('Char Siew Rice', 'Vegetables'),
    ])

    # 14. Char Siu Roasted Pork Rice
    food_ingredient_relations.extend([
        ('Char Siu Roasted Pork Rice', 'Pork'),
        ('Char Siu Roasted Pork Rice', 'Rice'),
        ('Char Siu Roasted Pork Rice', 'Soy Sauce'),
        ('Char Siu Roasted Pork Rice', 'Vegetables'),
    ])

    # 15. Chee Cheong Fun
    food_ingredient_relations.extend([
        ('Chee Cheong Fun', 'Rice Flour'),
        ('Chee Cheong Fun', 'Soy Sauce'),
        ('Chee Cheong Fun', 'Sesame Seeds'),
        ('Chee Cheong Fun', 'Chili Sauce'),
    ])

    # 16. Chendol
    food_ingredient_relations.extend([
        ('Chendol', 'Coconut Milk'),
        ('Chendol', 'Palm Sugar'),
        ('Chendol', 'Red Beans'),
        ('Chendol', 'Rice Flour'),
        ('Chendol', 'Green Rice Flour Jelly'),
    ])

    # 17. Chicken Rice Roasted
    food_ingredient_relations.extend([
        ('Chicken Rice Roasted', 'Chicken'),
        ('Chicken Rice Roasted', 'Rice'),
        ('Chicken Rice Roasted', 'Soy Sauce'),
        ('Chicken Rice Roasted', 'Sesame Oil'),
        ('Chicken Rice Roasted', 'Cucumber'),
    ])

    # 18. Chicken Rice Steamed
    food_ingredient_relations.extend([
        ('Chicken Rice Steamed', 'Chicken'),
        ('Chicken Rice Steamed', 'Rice'),
        ('Chicken Rice Steamed', 'Soy Sauce'),
        ('Chicken Rice Steamed', 'Sesame Oil'),
        ('Chicken Rice Steamed', 'Cucumber'),
    ])

    # 19. Chicken Rice Steamed Porridge
    food_ingredient_relations.extend([
        ('Chicken Rice Steamed Porridge', 'Chicken'),
        ('Chicken Rice Steamed Porridge', 'Rice'),
        ('Chicken Rice Steamed Porridge', 'Soy Sauce'),
        ('Chicken Rice Steamed Porridge', 'Sesame Oil'),
        ('Chicken Rice Steamed Porridge', 'Ginger'),
    ])

    # 20. Chilli Crab
    food_ingredient_relations.extend([
        ('Chilli Crab', 'Crab'),
        ('Chilli Crab', 'Chili Sauce'),
        ('Chilli Crab', 'Tomato Sauce'),
        ('Chilli Crab', 'Egg'),
        ('Chilli Crab', 'Garlic'),
        ('Chilli Crab', 'Ginger'),
    ])

    # 21. Chinese Dumplings
    food_ingredient_relations.extend([
        ('Chinese Dumplings', 'Wheat Flour'),
        ('Chinese Dumplings', 'Pork'),
        ('Chinese Dumplings', 'Shrimp'),
        ('Chinese Dumplings', 'Cabbage'),
        ('Chinese Dumplings', 'Soy Sauce'),
    ])

    # 22. Chwee Kueh
    food_ingredient_relations.extend([
        ('Chwee Kueh', 'Rice Flour'),
        ('Chwee Kueh', 'Preserved Radish'),
        ('Chwee Kueh', 'Garlic'),
        ('Chwee Kueh', 'Oil'),
    ])

    # 23. Claypot Rice
    food_ingredient_relations.extend([
        ('Claypot Rice', 'Rice'),
        ('Claypot Rice', 'Chicken'),
        ('Claypot Rice', 'Chinese Sausage'),
        ('Claypot Rice', 'Mushrooms'),
        ('Claypot Rice', 'Soy Sauce'),
    ])

    # 24. Congee
    food_ingredient_relations.extend([
        ('Congee', 'Rice'),
        ('Congee', 'Pork'),
        ('Congee', 'Chicken'),
        ('Congee', 'Fish'),
        ('Congee', 'Egg'),
        ('Congee', 'Soy Sauce'),
        ('Congee', 'Ginger'),
    ])

    # 25. Curry Puff
    food_ingredient_relations.extend([
        ('Curry Puff', 'Wheat Flour'),
        ('Curry Puff', 'Potatoes'),
        ('Curry Puff', 'Chicken'),
        ('Curry Puff', 'Sardines'),
        ('Curry Puff', 'Curry Powder'),
        ('Curry Puff', 'Butter'),
        ('Curry Puff', 'Egg'),  # For egg wash
    ])

    # 26. Duck Rice
    food_ingredient_relations.extend([
        ('Duck Rice', 'Duck'),
        ('Duck Rice', 'Rice'),
        ('Duck Rice', 'Soy Sauce'),
        ('Duck Rice', 'Herbs and Spices'),
        ('Duck Rice', 'Vegetables'),
    ])

    # 27. Durian
    food_ingredient_relations.extend([
        ('Durian', 'Durian Fruit'),
    ])

    # 28. Economy Bee Hoon
    food_ingredient_relations.extend([
        ('Economy Bee Hoon', 'Rice Vermicelli'),
        ('Economy Bee Hoon', 'Soy Sauce'),
        ('Economy Bee Hoon', 'Egg'),  # If added
        ('Economy Bee Hoon', 'Vegetables'),
    ])

    # 29. Economy Rice
    food_ingredient_relations.extend([
        ('Economy Rice', 'Rice'),
        # Ingredients vary depending on selected dishes
        # Common allergens may include:
        ('Economy Rice', 'Chicken'),
        ('Economy Rice', 'Pork'),
        ('Economy Rice', 'Fish'),
        ('Economy Rice', 'Egg'),
        ('Economy Rice', 'Tofu'),
        ('Economy Rice', 'Soy Sauce'),
    ])

    # 30. Fan Choy
    food_ingredient_relations.extend([
        ('Fan Choy', 'Rice'),
        ('Fan Choy', 'Char Siew (Pork)'),
        ('Fan Choy', 'Chinese Sausage'),
        ('Fan Choy', 'Egg'),
        ('Fan Choy', 'Soy Sauce'),
    ])

    # 31. Fish Ball Noodle
    food_ingredient_relations.extend([
        ('Fish Ball Noodle', 'Egg Noodles'),
        ('Fish Ball Noodle', 'Fish Balls'),
        ('Fish Ball Noodle', 'Soy Sauce'),
        ('Fish Ball Noodle', 'Chili'),
        ('Fish Ball Noodle', 'Vegetables'),
    ])

    # 32. Fried Carrot Cake Black
    food_ingredient_relations.extend([
        ('Fried Carrot Cake Black', 'Rice Flour'),
        ('Fried Carrot Cake Black', 'Radish'),
        ('Fried Carrot Cake Black', 'Egg'),
        ('Fried Carrot Cake Black', 'Preserved Radish'),
        ('Fried Carrot Cake Black', 'Sweet Soy Sauce'),
        ('Fried Carrot Cake Black', 'Garlic'),
    ])

    # 33. Fried Carrot Cake White
    food_ingredient_relations.extend([
        ('Fried Carrot Cake White', 'Rice Flour'),
        ('Fried Carrot Cake White', 'Radish'),
        ('Fried Carrot Cake White', 'Egg'),
        ('Fried Carrot Cake White', 'Preserved Radish'),
        ('Fried Carrot Cake White', 'Garlic'),
    ])

    # 34. Fried Dumplings
    food_ingredient_relations.extend([
        ('Fried Dumplings', 'Wheat Flour'),
        ('Fried Dumplings', 'Pork'),
        ('Fried Dumplings', 'Shrimp'),
        ('Fried Dumplings', 'Vegetables'),
        ('Fried Dumplings', 'Soy Sauce'),
    ])

    # 35. Fried Hokkien Mee
    food_ingredient_relations.extend([
        ('Fried Hokkien Mee', 'Egg Noodles'),
        ('Fried Hokkien Mee', 'Rice Vermicelli'),
        ('Fried Hokkien Mee', 'Prawns'),
        ('Fried Hokkien Mee', 'Squid'),
        ('Fried Hokkien Mee', 'Pork Belly'),
        ('Fried Hokkien Mee', 'Egg'),
        ('Fried Hokkien Mee', 'Sambal Chili'),
        ('Fried Hokkien Mee', 'Lime'),
    ])

    # 36. Fried Rice
    food_ingredient_relations.extend([
        ('Fried Rice', 'Rice'),
        ('Fried Rice', 'Egg'),
        ('Fried Rice', 'Vegetables'),
        ('Fried Rice', 'Chicken'),  # If added
        ('Fried Rice', 'Shrimp'),  # If added
        ('Fried Rice', 'Pork'),  # If added
        ('Fried Rice', 'Soy Sauce'),
    ])

    # 37. Grilled Fish with Rice
    food_ingredient_relations.extend([
        ('Grilled Fish with Rice', 'Fish'),
        ('Grilled Fish with Rice', 'Rice'),
        ('Grilled Fish with Rice', 'Spices'),
        ('Grilled Fish with Rice', 'Sambal Chili'),
        ('Grilled Fish with Rice', 'Banana Leaf'),
    ])

    # 38. Hainanese Curry Rice
    food_ingredient_relations.extend([
        ('Hainanese Curry Rice', 'Rice'),
        ('Hainanese Curry Rice', 'Curry Gravy'),
        ('Hainanese Curry Rice', 'Pork Chop'),
        ('Hainanese Curry Rice', 'Cabbage'),
        ('Hainanese Curry Rice', 'Eggs'),
        ('Hainanese Curry Rice', 'Mustard Seeds'),  # In curry
    ])

    # 39. Har Gow
    food_ingredient_relations.extend([
        ('Har Gow', 'Shrimp'),
        ('Har Gow', 'Wheat Starch'),
        ('Har Gow', 'Tapioca Starch'),
        ('Har Gow', 'Oil'),
    ])

    # 40. Kaya Toast
    food_ingredient_relations.extend([
        ('Kaya Toast', 'Bread'),
        ('Kaya Toast', 'Kaya'),
        ('Kaya Toast', 'Butter'),
    ])

    # 41. Ke Kou Mian
    food_ingredient_relations.extend([
        ('Ke Kou Mian', 'Wheat Flour Noodles'),
        ('Ke Kou Mian', 'Minced Pork'),
        ('Ke Kou Mian', 'Egg'),
        ('Ke Kou Mian', 'Vegetables'),
        ('Ke Kou Mian', 'Soup Stock'),
    ])

    # 42. Kway Chap
    food_ingredient_relations.extend([
        ('Kway Chap', 'Flat Rice Noodles'),
        ('Kway Chap', 'Pork Offal'),
        ('Kway Chap', 'Tofu'),
        ('Kway Chap', 'Egg'),
        ('Kway Chap', 'Soy Sauce'),
        ('Kway Chap', 'Herbs and Spices'),
    ])

    # 43. Laksa
    food_ingredient_relations.extend([
        ('Laksa', 'Rice Noodles'),
        ('Laksa', 'Coconut Milk'),
        ('Laksa', 'Prawns'),
        ('Laksa', 'Fish Cake'),
        ('Laksa', 'Cockles'),
        ('Laksa', 'Tofu Puffs'),
        ('Laksa', 'Sambal Chili'),
        ('Laksa', 'Bean Sprouts'),
    ])

    # 44. Lor Mee
    food_ingredient_relations.extend([
        ('Lor Mee', 'Egg Noodles'),
        ('Lor Mee', 'Starchy Gravy'),
        ('Lor Mee', 'Fish Cake'),
        ('Lor Mee', 'Braised Eggs'),
        ('Lor Mee', 'Pork Belly'),
        ('Lor Mee', 'Vinegar'),
        ('Lor Mee', 'Garlic'),
    ])

    # 45. Mala Dry Pot
    food_ingredient_relations.extend([
        ('Mala Dry Pot', 'Assorted Meats'),  # Chicken, Beef, Pork, etc.
        ('Mala Dry Pot', 'Assorted Vegetables'),
        ('Mala Dry Pot', 'Sichuan Peppercorns'),
        ('Mala Dry Pot', 'Chili Peppers'),
        ('Mala Dry Pot', 'Spices'),
        ('Mala Dry Pot', 'Oil'),
    ])

    # 46. Mala Soup
    food_ingredient_relations.extend([
        ('Mala Soup', 'Assorted Meats'),
        ('Mala Soup', 'Assorted Vegetables'),
        ('Mala Soup', 'Sichuan Peppercorns'),
        ('Mala Soup', 'Chili Peppers'),
        ('Mala Soup', 'Spices'),
        ('Mala Soup', 'Soup Stock'),
    ])

    # 47. Mee Goreng
    food_ingredient_relations.extend([
        ('Mee Goreng', 'Egg Noodles'),
        ('Mee Goreng', 'Tomato Sauce'),
        ('Mee Goreng', 'Soy Sauce'),
        ('Mee Goreng', 'Egg'),
        ('Mee Goreng', 'Chicken'),  # If added
        ('Mee Goreng', 'Shrimp'),  # If added
        ('Mee Goreng', 'Tofu'),
        ('Mee Goreng', 'Vegetables'),
        ('Mee Goreng', 'Chili'),
    ])

    # 48. Mee Hoon Kueh
    food_ingredient_relations.extend([
        ('Mee Hoon Kueh', 'Wheat Flour Dough'),
        ('Mee Hoon Kueh', 'Minced Pork'),
        ('Mee Hoon Kueh', 'Anchovies'),
        ('Mee Hoon Kueh', 'Egg'),
        ('Mee Hoon Kueh', 'Vegetables'),
        ('Mee Hoon Kueh', 'Soup Stock'),
    ])

    # 49. Mee Rebus
    food_ingredient_relations.extend([
        ('Mee Rebus', 'Egg Noodles'),
        ('Mee Rebus', 'Sweet Potato Gravy'),
        ('Mee Rebus', 'Shrimp Paste'),
        ('Mee Rebus', 'Soybeans'),
        ('Mee Rebus', 'Egg'),
        ('Mee Rebus', 'Tofu'),
        ('Mee Rebus', 'Bean Sprouts'),
        ('Mee Rebus', 'Lime'),
    ])

    # 50. Mee Siam
    food_ingredient_relations.extend([
        ('Mee Siam', 'Rice Vermicelli'),
        ('Mee Siam', 'Spicy and Sour Gravy'),
        ('Mee Siam', 'Tamarind'),
        ('Mee Siam', 'Dried Shrimp'),
        ('Mee Siam', 'Tofu'),
        ('Mee Siam', 'Egg'),
        ('Mee Siam', 'Chives'),
    ])

    # 51. Mee Soto
    food_ingredient_relations.extend([
        ('Mee Soto', 'Egg Noodles'),
        ('Mee Soto', 'Chicken'),
        ('Mee Soto', 'Bean Sprouts'),
        ('Mee Soto', 'Kicap Manis'),
        ('Mee Soto', 'Spices'),
        ('Mee Soto', 'Soup Stock'),
    ])

    # 52. Muah Chee
    food_ingredient_relations.extend([
        ('Muah Chee', 'Glutinous Rice Flour'),
        ('Muah Chee', 'Sugar'),
        ('Muah Chee', 'Peanuts'),
        ('Muah Chee', 'Sesame Seeds'),
        ('Muah Chee', 'Oil'),
    ])

    # 53. Nasi Briyani
    food_ingredient_relations.extend([
        ('Nasi Briyani', 'Basmati Rice'),
        ('Nasi Briyani', 'Chicken'),  # Or Mutton
        ('Nasi Briyani', 'Yogurt'),
        ('Nasi Briyani', 'Ghee'),
        ('Nasi Briyani', 'Spices'),
        ('Nasi Briyani', 'Almonds'),
        ('Nasi Briyani', 'Cashews'),
        ('Nasi Briyani', 'Saffron'),
    ])

    # 54. Nasi Lemak
    food_ingredient_relations.extend([
        ('Nasi Lemak', 'Rice'),
        ('Nasi Lemak', 'Coconut Milk'),
        ('Nasi Lemak', 'Anchovies'),
        ('Nasi Lemak', 'Peanuts'),
        ('Nasi Lemak', 'Egg'),
        ('Nasi Lemak', 'Sambal Chili'),
        ('Nasi Lemak', 'Cucumber'),
    ])

    # 55. Oyster Omelette
    food_ingredient_relations.extend([
        ('Oyster Omelette', 'Eggs'),
        ('Oyster Omelette', 'Oysters'),
        ('Oyster Omelette', 'Tapioca Starch'),
        ('Oyster Omelette', 'Chili Sauce'),
        ('Oyster Omelette', 'Garlic'),
    ])

    # 56. Pani Puri
    food_ingredient_relations.extend([
        ('Pani Puri', 'Semolina'),
        ('Pani Puri', 'Wheat Flour'),
        ('Pani Puri', 'Potatoes'),
        ('Pani Puri', 'Chickpeas'),
        ('Pani Puri', 'Tamarind Water'),
        ('Pani Puri', 'Spices'),
    ])

    # 57. Plain Prata
    food_ingredient_relations.extend([
        ('Plain Prata', 'Wheat Flour'),
        ('Plain Prata', 'Ghee'),
        ('Plain Prata', 'Oil'),
        ('Plain Prata', 'Salt'),
    ])

    # 58. Prawn Noodles Dry
    food_ingredient_relations.extend([
        ('Prawn Noodles Dry', 'Egg Noodles'),
        ('Prawn Noodles Dry', 'Prawns'),
        ('Prawn Noodles Dry', 'Pork Ribs'),
        ('Prawn Noodles Dry', 'Bean Sprouts'),
        ('Prawn Noodles Dry', 'Chili'),
        ('Prawn Noodles Dry', 'Soy Sauce'),
    ])

    # 59. Prawn Noodles Soup
    food_ingredient_relations.extend([
        ('Prawn Noodles Soup', 'Egg Noodles'),
        ('Prawn Noodles Soup', 'Prawns'),
        ('Prawn Noodles Soup', 'Pork Ribs'),
        ('Prawn Noodles Soup', 'Bean Sprouts'),
        ('Prawn Noodles Soup', 'Soup Stock'),
        ('Prawn Noodles Soup', 'Chili'),
    ])

    # 60. Putu Piring
    food_ingredient_relations.extend([
        ('Putu Piring', 'Rice Flour'),
        ('Putu Piring', 'Palm Sugar'),
        ('Putu Piring', 'Grated Coconut'),
        ('Putu Piring', 'Pandan Leaves'),
    ])

    # 61. Rice Dumpling
    food_ingredient_relations.extend([
        ('Rice Dumpling', 'Glutinous Rice'),
        ('Rice Dumpling', 'Pork'),
        ('Rice Dumpling', 'Mushrooms'),
        ('Rice Dumpling', 'Chestnuts'),
        ('Rice Dumpling', 'Salted Egg Yolk'),
        ('Rice Dumpling', 'Soy Sauce'),
        ('Rice Dumpling', 'Bamboo Leaves'),
    ])

    # 62. Roasted Duck Roasted Pork Rice
    food_ingredient_relations.extend([
        ('Roasted Duck Roasted Pork Rice', 'Duck'),
        ('Roasted Duck Roasted Pork Rice', 'Pork'),
        ('Roasted Duck Roasted Pork Rice', 'Rice'),
        ('Roasted Duck Roasted Pork Rice', 'Soy Sauce'),
        ('Roasted Duck Roasted Pork Rice', 'Vegetables'),
    ])

    # 63. Roasted Pork Rice
    food_ingredient_relations.extend([
        ('Roasted Pork Rice', 'Pork'),
        ('Roasted Pork Rice', 'Rice'),
        ('Roasted Pork Rice', 'Soy Sauce'),
        ('Roasted Pork Rice', 'Vegetables'),
    ])

    # 64. Rojak
    food_ingredient_relations.extend([
        ('Rojak', 'Cucumber'),
        ('Rojak', 'Pineapple'),
        ('Rojak', 'Turnip'),
        ('Rojak', 'You Tiao'),
        ('Rojak', 'Peanuts'),
        ('Rojak', 'Shrimp Paste Sauce'),
    ])

    # 65. Sambal Kangkong
    food_ingredient_relations.extend([
        ('Sambal Kangkong', 'Water Spinach'),
        ('Sambal Kangkong', 'Sambal Belacan'),
        ('Sambal Kangkong', 'Garlic'),
        ('Sambal Kangkong', 'Oil'),
    ])

    # 66. Sambal Sotong
    food_ingredient_relations.extend([
        ('Sambal Sotong', 'Squid'),
        ('Sambal Sotong', 'Sambal Chili'),
        ('Sambal Sotong', 'Onions'),
        ('Sambal Sotong', 'Garlic'),
        ('Sambal Sotong', 'Oil'),
    ])

    # 67. Sambal Stingray
    food_ingredient_relations.extend([
        ('Sambal Stingray', 'Stingray'),
        ('Sambal Stingray', 'Sambal Chili'),
        ('Sambal Stingray', 'Banana Leaf'),
        ('Sambal Stingray', 'Lime'),
    ])

    # 68. Satay
    food_ingredient_relations.extend([
        ('Satay', 'Chicken'),  # Or Beef, Mutton
        ('Satay', 'Peanut Sauce'),
        ('Satay', 'Ketupat'),
        ('Satay', 'Cucumber'),
        ('Satay', 'Onions'),
        ('Satay', 'Spices'),
    ])

    # 69. Siew Mai
    food_ingredient_relations.extend([
        ('Siew Mai', 'Pork'),
        ('Siew Mai', 'Shrimp'),
        ('Siew Mai', 'Wheat Flour Wrappers'),
        ('Siew Mai', 'Mushrooms'),
        ('Siew Mai', 'Egg'),
    ])

    # 70. Sliced Fish Soup
    food_ingredient_relations.extend([
        ('Sliced Fish Soup', 'Fish Slices'),
        ('Sliced Fish Soup', 'Tofu'),
        ('Sliced Fish Soup', 'Vegetables'),
        ('Sliced Fish Soup', 'Soup Stock'),
        ('Sliced Fish Soup', 'Ginger'),
    ])

    # 71. Soon Kueh
    food_ingredient_relations.extend([
        ('Soon Kueh', 'Rice Flour Skin'),
        ('Soon Kueh', 'Turnip'),
        ('Soon Kueh', 'Bamboo Shoots'),
        ('Soon Kueh', 'Dried Shrimp'),
        ('Soon Kueh', 'Mushrooms'),
        ('Soon Kueh', 'Soy Sauce'),
    ])

    # 72. Tang Yuan
    food_ingredient_relations.extend([
        ('Tang Yuan', 'Glutinous Rice Flour'),
        ('Tang Yuan', 'Peanut Filling'),  # Or Sesame Filling
        ('Tang Yuan', 'Sesame Seeds'),
        ('Tang Yuan', 'Sugar'),
        ('Tang Yuan', 'Ginger'),  # In syrup
    ])

    # 73. Tau Sar Pau
    food_ingredient_relations.extend([
        ('Tau Sar Pau', 'Wheat Flour'),
        ('Tau Sar Pau', 'Red Bean Paste'),
        ('Tau Sar Pau', 'Sugar'),
    ])

    # 74. Wanton Mee Dry
    food_ingredient_relations.extend([
        ('Wanton Mee Dry', 'Egg Noodles'),
        ('Wanton Mee Dry', 'Wantons'),  # Pork filling
        ('Wanton Mee Dry', 'Char Siew (Pork)'),
        ('Wanton Mee Dry', 'Soy Sauce'),
        ('Wanton Mee Dry', 'Chili Sauce'),
        ('Wanton Mee Dry', 'Vegetables'),
    ])

    # 75. Wanton Mee Soup
    food_ingredient_relations.extend([
        ('Wanton Mee Soup', 'Egg Noodles'),
        ('Wanton Mee Soup', 'Wantons'),
        ('Wanton Mee Soup', 'Char Siew (Pork)'),
        ('Wanton Mee Soup', 'Soup Stock'),
        ('Wanton Mee Soup', 'Vegetables'),
    ])

    # 76. Xiao Long Bao
    food_ingredient_relations.extend([
        ('Xiao Long Bao', 'Wheat Flour Wrappers'),
        ('Xiao Long Bao', 'Pork'),
        ('Xiao Long Bao', 'Soup Gelatin'),
        ('Xiao Long Bao', 'Ginger'),
        ('Xiao Long Bao', 'Soy Sauce'),
    ])

    # 77. Xingzhou Bee Hoon
    food_ingredient_relations.extend([
        ('Xingzhou Bee Hoon', 'Rice Vermicelli'),
        ('Xingzhou Bee Hoon', 'Shrimp'),
        ('Xingzhou Bee Hoon', 'Egg'),
        ('Xingzhou Bee Hoon', 'Vegetables'),
        ('Xingzhou Bee Hoon', 'Curry Powder'),
        ('Xingzhou Bee Hoon', 'Soy Sauce'),
    ])

    # 78. Yong Tau Foo Dry
    food_ingredient_relations.extend([
        ('Yong Tau Foo Dry', 'Assorted Stuffed Tofu and Vegetables'),
        ('Yong Tau Foo Dry', 'Fish Paste'),
        ('Yong Tau Foo Dry', 'Egg Noodles'),  # If chosen
        ('Yong Tau Foo Dry', 'Rice Vermicelli'),  # If chosen
        ('Yong Tau Foo Dry', 'Soy Sauce'),
    ])

    # 79. Yong Tau Foo Soup
    food_ingredient_relations.extend([
        ('Yong Tau Foo Soup', 'Assorted Stuffed Tofu and Vegetables'),
        ('Yong Tau Foo Soup', 'Fish Paste'),
        ('Yong Tau Foo Soup', 'Egg Noodles'),
        ('Yong Tau Foo Soup', 'Soup Stock'),
        ('Yong Tau Foo Soup', 'Soy Sauce'),
    ])

    # 80. You Mian
    food_ingredient_relations.extend([
        ('You Mian', 'Thin Wheat Noodles'),
        ('You Mian', 'Minced Pork'),
        ('You Mian', 'Vegetables'),
        ('You Mian', 'Egg'),
        ('You Mian', 'Soup Stock'),
    ])

    # 81. Youtiao
    food_ingredient_relations.extend([
        ('Youtiao', 'Wheat Flour'),
        ('Youtiao', 'Oil'),
        ('Youtiao', 'Salt'),
        ('Youtiao', 'Baking Soda'),  # Leavening agent
    ])

    # Insert relationships between ingredients and health conditions
    for ingredient, condition in ingredient_condition_relations:
        ingredient_id = ingredient_ids.get(ingredient)
        condition_id = condition_ids.get(condition)
        if ingredient_id and condition_id:
            # Check if the relationship already exists
            cursor.execute("""
                SELECT 1 FROM relationships
                WHERE source_type = 'Ingredient' AND source_id = ?
                AND target_type = 'HealthCondition' AND target_id = ?
                AND relation_type = 'CAUSES_ALLERGY'
            """, (ingredient_id, condition_id))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO relationships (source_type, source_id, target_type, target_id, relation_type)
                    VALUES ('Ingredient', ?, 'HealthCondition', ?, 'CAUSES_ALLERGY')
                """, (ingredient_id, condition_id))

    # Insert relationships between foods and ingredients
    for food, ingredient in food_ingredient_relations:
        food_id = food_ids.get(food)
        ingredient_id = ingredient_ids.get(ingredient)
        if food_id and ingredient_id:
            # Check if the relationship already exists
            cursor.execute("""
                SELECT 1 FROM relationships
                WHERE source_type = 'Food' AND source_id = ?
                AND target_type = 'Ingredient' AND target_id = ?
                AND relation_type = 'CONTAINS_INGREDIENT'
            """, (food_id, ingredient_id))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO relationships (source_type, source_id, target_type, target_id, relation_type)
                    VALUES ('Food', ?, 'Ingredient', ?, 'CONTAINS_INGREDIENT')
                """, (food_id, ingredient_id))

    conn.commit()
    conn.close()

# Call the function to insert the additional dishes and allergens
insert_dishes_and_allergens()
