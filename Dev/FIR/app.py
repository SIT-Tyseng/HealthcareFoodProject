import json
import sqlite3
import streamlit as st
from fuzzywuzzy import process, fuzz
from app import create_app, db, bcrypt
from app.models import User
from aiModel import analyze_image
from flask_login import login_user, LoginManager
from werkzeug.utils import secure_filename
from streamlit_option_menu import option_menu
import os
from datetime import datetime
from streamlit_lottie import st_lottie
from knowledge_graph_load_graph import visualize_filtered_graph_with_ingredients, load_graph_from_sqlite
from usda_API import search_ingredient, categories
from hpb_food_db_new import get_nutritional_values_local
import re
from PIL import Image
from PIL.Image import Resampling

# New imports for mass estimation
import torch
import numpy as np
import matplotlib.pyplot as plt

import sys

# Add the path to ml-depth-pro directory to sys.path
project_path = os.path.abspath("ml-depth-pro\\src")
if project_path not in sys.path:
    sys.path.append(project_path)

# For depth estimation model
import depth_pro
import pillow_heif  # For handling HEIC images

# For NuNet model
from model import RGB_D_Constructor
from data_augment import S0
from config_parser import get_parser

# Register HEIF opener for Pillow
pillow_heif.register_heif_opener()

# Load the graph only once at startup
if 'knowledge_graph' not in st.session_state:
    st.session_state['knowledge_graph'] = load_graph_from_sqlite()

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_food = load_lottiefile("static/animations/food_served.json")
lottie_vlogger = load_lottiefile("static/animations/food_vlogger.json")
lottie_search = load_lottiefile("static/animations/lottie_search.json")

# User and assistant names
U_NAME = "User"
A_NAME = "Assistant"

# Set page configuration
st.set_page_config(
    page_title="DishVision",
    page_icon="🍽️",
    layout="wide",
)

# Create and configure the Flask app
flask_app = create_app()
login_manager = LoginManager()
login_manager.init_app(flask_app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

flask_app.app_context().push()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{timestamp}_{secure_filename(file.name)}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, 'wb') as f:
        f.write(file.getbuffer())
    return file_path

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'selected_image' not in st.session_state:
    st.session_state['selected_image'] = None

# if 'upload_key' not in st.session_state:
#     st.session_state['upload_key'] = 0

if 'allergies_found' not in st.session_state:
    st.session_state['allergies_found'] = []

if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = []

if 'context' not in st.session_state:
    st.session_state['context'] = []

# Initialize session state for models
if 'depth_model' not in st.session_state:

    # Initialize the depth estimation model
    depth_model, depth_transform = depth_pro.create_model_and_transforms()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    depth_model = depth_model.to(device)
    depth_model.eval()
    st.session_state['depth_model'] = depth_model
    st.session_state['depth_transform'] = depth_transform

if 'nUNet_model' not in st.session_state:
    # Initialize the NuNet mass estimation model
    parser, args_dict = get_parser()
    args = parser.parse_args([])
    checkpoint_path = r"experiment/37c9ed248cc58c1dae423f304c095d48a9f8150e.ckpt"
    nUNet_model = RGB_D_Constructor.load_from_checkpoint(checkpoint_path, args=args)
    nUNet_model.eval()
    st.session_state['nUNet_model'] = nUNet_model

# Set the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Authentication functions
def sidebar_with_logo():
    st.sidebar.image("static/logo.png")
    with st.sidebar:
        selected = option_menu(
            "Menu",
            ["Home", "Allergies", "Logout"] if st.session_state['authenticated'] else ["Login", "Register"],
            icons=["person", "person-add", "house", "door-open"] if st.session_state['authenticated'] else ["person", "person-add"],
            menu_icon="list",
            styles={
                "menu-title": {"font-size": "18px"},
                "icon": {"color": "orange", "font-size": "15px"},
                "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#E86A33"},
            },
            default_index=0,
            key="sidebar_menu"
        )
    return selected


def login():
    st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st_lottie(
            lottie_food,
            speed=1,
            reverse=False,
            loop=True,
            quality='high',
            key="login_lottie",
            height=450,
            width=730
        )

        email = st.text_input("Enter your email", key="email_login")
        password = st.text_input("Enter your password", type='password', key="password_login")
        if st.button("Login", key="login_button"):
            with flask_app.test_request_context('/login'):
                user = User.query.filter_by(email=email).first()
                if user and bcrypt.check_password_hash(user.password, password):
                    login_user(user)
                    st.session_state['user_id'] = user.id
                    st.session_state['authenticated'] = True
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Login Unsuccessful. Please check email and password")


def register():
    st.markdown("<h1 style='text-align: center;'>Register</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st_lottie(
            lottie_vlogger,
            speed=1,
            reverse=False,
            loop=True,
            quality='high',
            key="register_lottie",
            height=450,
            width=730
        )

        username = st.text_input("Enter your username", key="register_username")
        email = st.text_input("Enter your email", key="register_email")
        password = st.text_input("Enter your password", type='password', key="register_password")
        confirm_password = st.text_input("Confirm your password", type='password', key="register_confirm_password")

        if st.button("Sign Up", key="register_button"):
            if password == confirm_password:
                with flask_app.test_request_context('/register'):
                    # Check if the email already exists
                    existing_user = User.query.filter_by(email=email).first()
                    if existing_user:
                        st.error("This email is already registered. Please use another email.")
                        return

                    # Generate hashed password
                    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

                    # Add the user to the `user` table
                    user = User(username=username, email=email, password=hashed_password)
                    db.session.add(user)
                    db.session.commit()

                    st.success("Your account has been created! You can now log in.")
            else:
                st.error("Passwords do not match")

if 'dish_name' not in st.session_state:
    st.session_state.dish_name = None
if 'dish_mass' not in st.session_state:
    st.session_state.dish_mass = None
if 'ingredients' not in st.session_state:
    st.session_state.ingredients = []
if 'ingredients_mass' not in st.session_state:
    st.session_state.ingredients_mass = []

def extract_info_from_response(response):
    import sqlite3
    from fuzzywuzzy import process, fuzz

    # Initialize dish_name and ingredients in session state if not already present
    if 'dish_name' not in st.session_state:
        st.session_state.dish_name = None
    if 'ingredients' not in st.session_state:
        st.session_state.ingredients = []
    if 'dish_mass' not in st.session_state:
        st.session_state.dish_mass = None
    if 'ingredients_mass' not in st.session_state:
        st.session_state.ingredients_mass = []

    # Extract dish name from the response
    dish_name_match = re.search(r'This is a dish called (.+)\.', response)
    if dish_name_match:
        extracted_dish_name = dish_name_match.group(1).strip()
    else:
        # If dish name not found, retain existing value or handle accordingly
        extracted_dish_name = None

    # Fetch ingredients based on the dish name
    if extracted_dish_name:
        conn = sqlite3.connect('instance/site.db')
        cursor = conn.cursor()

        # Find the dish in the database using fuzzy matching
        cursor.execute("SELECT food_name FROM food_items")
        all_food_names = [row[0] for row in cursor.fetchall()]
        matched_food_name, score = process.extractOne(extracted_dish_name, all_food_names)
        if score >= 80:  # Adjust the threshold as needed
            st.session_state.dish_name = matched_food_name

            # Get the food_id for the matched food name
            cursor.execute("SELECT id FROM food_items WHERE food_name = ?", (st.session_state.dish_name,))
            food_id_row = cursor.fetchone()
            if food_id_row:
                food_id = food_id_row[0]

                # Fetch the ingredients for the matched dish using the relationships table
                cursor.execute("""
                    SELECT i.ingredient_name
                    FROM relationships r
                    JOIN ingredients i ON r.target_id = i.id
                    WHERE r.source_type = 'Food' AND r.source_id = ?
                    AND r.target_type = 'Ingredient' AND r.relation_type = 'CONTAINS_INGREDIENT'
                """, (food_id,))
                ingredients = [row[0] for row in cursor.fetchall()]
                st.session_state.ingredients = ingredients
            else:
                st.warning(f"Dish '{st.session_state.dish_name}' not found in the database.")
                st.session_state.ingredients = []
        else:
            st.warning(f"Dish '{extracted_dish_name}' not found in the database.")
            st.session_state.dish_name = extracted_dish_name  # Keep the extracted name for reference
            st.session_state.ingredients = []

        conn.close()
    else:
        st.session_state.ingredients = []

    # Extract dish mass if present and not already set
    if st.session_state.dish_mass is None:
        dish_mass_match = re.search(r'(?:mass is |mass of the dish is |mass of this dish is )([\d.]+)\s*(grams|g)?', response, re.IGNORECASE)
        if dish_mass_match:
            st.session_state.dish_mass = int(float(dish_mass_match.group(1)))
        else:
            # If mass not found, retain existing value
            pass

    # We don't have ingredients_mass since we're getting ingredients from the database
    st.session_state.ingredients_mass = []

    return {
        'dish_name': st.session_state.dish_name,
        'dish_mass': st.session_state.dish_mass,
        'ingredients': st.session_state.ingredients,
        'ingredients_mass': st.session_state.ingredients_mass
    }


def get_ingredient_to_allergy_mapping():
    conn = sqlite3.connect('instance/site.db')
    cursor = conn.cursor()

    # Get all ingredients
    cursor.execute("SELECT id, ingredient_name FROM ingredients")
    ingredients = cursor.fetchall()

    # Initialize the mapping
    ingredient_to_allergies = {}

    for ingredient_id, ingredient_name in ingredients:
        # Get the health conditions caused by this ingredient
        cursor.execute("""
            SELECT hc.condition_name
            FROM relationships r
            JOIN health_conditions hc ON r.target_id = hc.id
            WHERE r.source_type = 'Ingredient' AND r.source_id = ?
            AND r.relation_type = 'CAUSES_ALLERGY'
        """, (ingredient_id,))
        allergies = [row[0].lower() for row in cursor.fetchall()]
        ingredient_to_allergies[ingredient_name.lower()] = allergies

    conn.close()
    return ingredient_to_allergies

def home():
    st.markdown("<h1 style='text-align: center;'>Your Personal Nutrition Guide</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st_lottie(
            lottie_search,
            speed=1,
            reverse=False,
            loop=True,
            quality='high',
            key="register_lottie",
            height=450,
            width=730
        )

    with flask_app.test_request_context('/home'):
        user = db.session.get(User, st.session_state['user_id'])
        if user and user.is_authenticated:
            if not st.session_state['chat_history']:
                st.session_state['chat_history'].append({
                    "role": "assistant",
                    "content": "Welcome! Please upload an image and ask any questions you might have."
                })

            # Sidebar for image uploader
            with st.sidebar:
                uploaded_file = st.file_uploader("Upload an image", type=ALLOWED_EXTENSIONS, key='file_uploader')
                if uploaded_file is not None and allowed_file(uploaded_file.name):
                    # Get file details
                    file_details = {"name": uploaded_file.name, "size": uploaded_file.size}
                    if st.session_state.get('last_uploaded_file_details') != file_details:
                        st.session_state['last_uploaded_file_details'] = file_details

                        # Save the file
                        file_path = save_file(uploaded_file)
                        if file_path:
                            st.session_state['uploaded_files'].append(uploaded_file.name)
                            st.session_state['selected_image'] = file_path
                            st.session_state['context'] = []  # Reset context with new image
                            # Display the image in the chat history
                            st.session_state['chat_history'].append({
                                "role": "user",
                                "content": None,
                                "image": file_path
                            })
                            # Reset the global variables when new image is uploaded
                            st.session_state.dish_name = None
                            st.session_state.dish_mass = None
                            st.session_state.ingredients = []
                            st.session_state.ingredients_mass = []

                            # Automatically process the uploaded image
                            process_uploaded_image()

            # Display chat history
            for i, message in enumerate(st.session_state.chat_history):
                if message["role"] == "user":
                    with st.chat_message(name="user", avatar="user"):
                        if message.get("image") is not None:
                            # Limit the displayed image size to 512 pixels
                            st.image(message["image"], caption='User uploaded image', width=512, use_column_width=False)
                        elif message.get("content") is not None:
                            st.markdown(message["content"])
                else:
                    with st.chat_message(name="assistant", avatar="assistant"):
                        st.markdown(message.get("content", ""))
                        if message.get("image") is not None:
                            st.image(message["image"], caption="Assistant's Image", width=512, use_column_width=False)

            allergies_found = st.session_state.get('allergies_found', [])

            # Display the knowledge graph
            if allergies_found and 'knowledge_graph' in st.session_state and st.session_state.get('dish_name'):
                # Ensure the knowledge graph is loaded
                if not st.session_state.get('knowledge_graph'):
                    st.session_state['knowledge_graph'] = load_graph_from_sqlite()

                graph = st.session_state['knowledge_graph']
                fig = visualize_filtered_graph_with_ingredients(
                    G=graph,
                    user_id=st.session_state['user_id'],
                    dish_name=st.session_state['dish_name'],
                    dish_ingredients=st.session_state.get('ingredients', [])
                )
                if fig:
                    st.markdown("---")
                    st.markdown("### Knowledge Graph")

                    col1, col2, col3 = st.columns([1, 3, 1])  # Restrict graph to center column
                    with col2:
                        st.pyplot(fig)  # Increase DPI for smaller, sharper rendering
                else:
                    st.write("No data available for this user.")

            # Chat input
            user_message = st.chat_input("Type your message and press Enter")

            if user_message:
                with st.chat_message(U_NAME, avatar="user"):
                    st.session_state['chat_history'].append({"role": "user", "content": user_message, "image": None})
                    st.markdown(user_message)

                # Generate reply using the model
                with st.chat_message(A_NAME, avatar="assistant"):
                    # Here, you can integrate any response generation logic if needed
                    # For now, we'll just echo the user's message
                    assistant_response = "I'm here to assist you with any questions about the dish."
                    st.markdown(assistant_response)
                    st.session_state['chat_history'].append({"role": "assistant", "content": assistant_response, "image": None})

            # Clear uploaded files after processing
            st.session_state['uploaded_files'] = []


def process_uploaded_image():
    image_path = st.session_state['selected_image']
    if os.path.exists(image_path):
        # Load the image
        image = Image.open(image_path).convert("RGB")

        max_size = (512, 512)
        image.thumbnail(max_size, Resampling.LANCZOS)

        # Display the image in the assistant's message (optional)
        # st.session_state['chat_history'].append({
        #     "role": "assistant",
        #     "content": "Here's the image you uploaded:",
        #     "image": image_path
        # })

        # ---------------------
        # Run the image through the food classification model
        # ---------------------
        # Assuming 'analyze_image' function returns the dish name
        # and any other relevant information

        imagefile = image_path
        user_message = "Identify the dish in this image."
        bot_response, new_context = analyze_image(imagefile, user_message, st.session_state['context'])
        st.session_state['context'] = new_context
        bot_response_lower = bot_response.lower()

        # Display the classification result as assistant's message
        classification_message = f"**Classification Result:** {bot_response}"
        st.session_state['chat_history'].append({
            "role": "assistant",
            "content": classification_message,
            "image": None
        })

        # Extract information from the response
        info = extract_info_from_response(bot_response)
        print(info)

        # ---------------------
        # Mass Estimation
        # ---------------------
        # Get the models and transforms
        depth_model = st.session_state['depth_model']
        depth_transform = st.session_state['depth_transform']
        nUNet_model = st.session_state['nUNet_model']

        # Preprocess the image for depth estimation model
        depth_input = depth_transform(image).unsqueeze(0).to(device)

        # Run model inference using the 'infer' method
        with torch.no_grad():
            output_depth = depth_model.infer(depth_input)
        depth_tensor = output_depth["depth"]

        # Prepare Input for NuNet Model
        nuNet_transform = S0()
        image_tensor = nuNet_transform(image).unsqueeze(0).to(device)
        # Convert depth_tensor to PIL Image for nuNet_transform
        depth_array = depth_tensor.squeeze().cpu().numpy()
        # Normalize depth array and convert to 8-bit image
        depth_normalized = (depth_array - depth_array.min()) / (depth_array.max() - depth_array.min())
        depth_normalized = (depth_normalized * 255).astype(np.uint8)
        depth_image = Image.fromarray(depth_normalized).convert("RGB")
        depth_tensor_nunet = nuNet_transform(depth_image).unsqueeze(0).to(device)

        # Run Inference with NuNet Model
        with torch.no_grad():
            output_mass = nUNet_model(image_tensor, depth_tensor_nunet)

        # If the output is a tuple, extract the first element
        if isinstance(output_mass, tuple):
            output_mass = output_mass[0]

        # Get the predicted mass
        predicted_mass = output_mass.squeeze().item()

        # Store the predicted mass in session state
        st.session_state.dish_mass = int(predicted_mass)
        print(f"Predicted Mass for {image_path}: {predicted_mass}")

        # Display the predicted mass to the user as assistant's message
        mass_message = f"**Estimated Mass of the Dish:** {predicted_mass:.2f} grams."
        st.session_state['chat_history'].append({
            "role": "assistant",
            "content": mass_message,
            "image": None
        })

        # ---------------------
        # Nutritional Information
        # ---------------------
        dish_name = st.session_state.dish_name
        dish_mass = st.session_state.dish_mass
        if dish_name and dish_mass:
            # Try to get nutritional values for the dish
            nutritional_values = get_nutritional_values_local(dish_name, dish_mass)
            #if not nutritional_values or nutritional_values == "Not found":
            #    nutritional_values = search_ingredient(dish_name + ' raw', dish_mass)

            # Display nutritional values for the dish as assistant's message
            if nutritional_values and nutritional_values != "Not found":
                nutritional_message = f"### Nutritional Information:\n{nutritional_values}"
                st.session_state['chat_history'].append({
                    "role": "assistant",
                    "content": nutritional_message,
                    "image": None
                })
            else:
                st.session_state['chat_history'].append({
                    "role": "assistant",
                    "content": "Nutritional information not found for the dish.",
                    "image": None
                })
        else:
            st.session_state['chat_history'].append({
                "role": "assistant",
                "content": "Dish name or mass not available for nutritional information.",
                "image": None
            })

        # ---------------------
        # Allergy Information
        # ---------------------
        # Fetch user's allergies from the database
        graph = st.session_state['knowledge_graph']  # Use the preloaded graph
        conn = sqlite3.connect('instance/site.db')
        cursor = conn.cursor()

        # Fetch user's allergies via relationships
        cursor.execute("""
            SELECT hc.condition_name
            FROM relationships r
            JOIN health_conditions hc ON r.target_id = hc.id
            WHERE r.source_type = 'User' AND r.source_id = ?
            AND r.target_type = 'HealthCondition' AND r.relation_type = 'HAS_CONDITION'
        """, (st.session_state['user_id'],))
        user_allergies = [row[0].lower() for row in cursor.fetchall()]

        conn.close()

        # Get the ingredient to allergy mapping
        ingredient_to_allergies = get_ingredient_to_allergy_mapping()

        # Debug statements for allergies and ingredients
        print(f"User Allergies: {user_allergies}")
        print(f"Dish Ingredients: {st.session_state.ingredients}")

        # Determine if any of the ingredients match user's allergies
        allergies_found = []
        for ingredient in st.session_state.ingredients:
            ingredient_lower = ingredient.lower()
            if ingredient_lower in ingredient_to_allergies:
                # Get the allergies caused by this ingredient
                allergies_caused = ingredient_to_allergies[ingredient_lower]
                # Check if any of these allergies are in user's allergies
                matched_allergies = [allergy for allergy in allergies_caused if allergy in user_allergies]
                if matched_allergies:
                    allergies_found.append({
                        'ingredient': ingredient,
                        'allergies': matched_allergies
                    })

        # Store allergies_found in session state
        st.session_state['allergies_found'] = allergies_found

        # Debug statement for matched allergies
        print(f"Allergies Found: {allergies_found}")

        # Display allergy warnings as assistant's message
        if allergies_found:
            allergy_messages = []
            for entry in allergies_found:
                ingredient = entry['ingredient']
                allergies = ', '.join(entry['allergies'])
                allergy_messages.append(f"{ingredient} (Causes: {allergies})")
            allergy_message = ', '.join(allergy_messages)
            allergy_warning = f"⚠️ **Warning**: The following ingredients in your dish match your allergies: {allergy_message}"
            st.session_state['chat_history'].append({
                "role": "assistant",
                "content": allergy_warning,
                "image": None
            })
            # Optionally, display the knowledge graph
#            with st.expander(f"Show knowledge graph for {st.session_state['user_id']}", expanded=False):
#                fig = visualize_filtered_graph_with_ingredients(
#                    G=graph,
#                    user_id=st.session_state['user_id'],
#                    dish_name=st.session_state.dish_name,
#                    dish_ingredients=st.session_state.ingredients
#                )
#                if fig:
#                    # Center the figure using columns
#                    col1, col2, col3 = st.columns([1, 2, 1])
#                    with col2:
#                        st.pyplot(fig)
#                else:
#                    st.write("No data available for this user.")
        else:
            st.session_state['chat_history'].append({
                "role": "assistant",
                "content": "✅ You have no allergies related to this dish.",
                "image": None
            })
    else:
        st.error("Image file not found for processing.")



def allergies():
    st.markdown("<h1 style='text-align: center;'>Manage Your Allergies</h1>", unsafe_allow_html=True)

    user_id = st.session_state.get('user_id')
    if user_id:
        conn = sqlite3.connect('instance/site.db')
        cursor = conn.cursor()

        # Fetch existing allergies for the user via relationships
        cursor.execute("""
            SELECT hc.id, hc.condition_name
            FROM relationships r
            JOIN health_conditions hc ON r.target_id = hc.id
            WHERE r.source_type = 'User' AND r.source_id = ?
            AND r.target_type = 'HealthCondition' AND r.relation_type = 'HAS_CONDITION'
        """, (user_id,))
        existing_allergies_data = cursor.fetchall()
        existing_allergies = [row[1] for row in existing_allergies_data]
        existing_allergy_ids = [row[0] for row in existing_allergies_data]

        # Display existing allergies
        st.markdown("### Your Current Allergies:")
        if existing_allergies:
            st.write(", ".join(existing_allergies))
            # Provide an option to delete allergies
            st.markdown("### Remove Allergies:")
            allergies_to_remove = st.multiselect("Select allergies to remove", existing_allergies, key="remove_allergies")
            if st.button("Remove Selected Allergies", key="remove_allergies_button"):
                if allergies_to_remove:
                    # Get the ids of the selected allergies
                    allergies_to_remove_ids = []
                    for allergy in allergies_to_remove:
                        cursor.execute("SELECT id FROM health_conditions WHERE condition_name = ? AND user_id IS NULL", (allergy,))
                        result = cursor.fetchone()
                        if result:
                            allergies_to_remove_ids.append(result[0])

                    # Delete the relationships from the relationships table
                    for allergy_id in allergies_to_remove_ids:
                        cursor.execute("""
                            DELETE FROM relationships
                            WHERE source_type = 'User' AND source_id = ?
                            AND target_type = 'HealthCondition' AND target_id = ?
                            AND relation_type = 'HAS_CONDITION'
                        """, (user_id, allergy_id))
                    conn.commit()
                    st.session_state['knowledge_graph'] = load_graph_from_sqlite()
                    st.success("Selected allergies have been removed.")
                    st.rerun()
        else:
            st.write("You have no recorded allergies.")

        # Fetch all available allergies in the database where user_id is NULL to avoid duplicates
        cursor.execute("SELECT DISTINCT condition_name FROM health_conditions WHERE user_id IS NULL")
        all_allergies = [row[0] for row in cursor.fetchall()]

        # Remove allergies that the user already has
        available_allergies = [allergy for allergy in all_allergies if allergy not in existing_allergies]

        # Add new allergies using multiselect
        st.markdown("### Add New Allergies:")
        if available_allergies:
            allergy_options = sorted(available_allergies)  # Optional: sort the list alphabetically
            selected_allergies = st.multiselect("Select allergies to add", allergy_options, key="new_allergies")
            if st.button("Add Selected Allergies", key="add_allergies_button"):
                if selected_allergies:
                    for selected_allergy in selected_allergies:
                        # Get the health_condition id where user_id is NULL
                        cursor.execute("SELECT id FROM health_conditions WHERE condition_name = ? AND user_id IS NULL", (selected_allergy,))
                        result = cursor.fetchone()
                        if result:
                            health_condition_id = result[0]
                            # Check if the relationship already exists
                            cursor.execute("""
                                SELECT 1 FROM relationships
                                WHERE source_type = 'User' AND source_id = ?
                                AND target_type = 'HealthCondition' AND target_id = ?
                                AND relation_type = 'HAS_CONDITION'
                            """, (user_id, health_condition_id))
                            if cursor.fetchone():
                                st.warning(f"You already have '{selected_allergy}' allergy added.")
                            else:
                                # Insert a HAS_CONDITION relationship
                                cursor.execute("""
                                    INSERT INTO relationships (source_type, source_id, target_type, target_id, relation_type)
                                    VALUES (?, ?, ?, ?, ?)
                                """, ('User', user_id, 'HealthCondition', health_condition_id, 'HAS_CONDITION'))
                                conn.commit()
                    st.session_state['knowledge_graph'] = load_graph_from_sqlite()
                    st.success("Selected allergies have been added successfully!")
                    st.rerun()
        else:
            st.write("No more allergies to add.")

        conn.close()
    else:
        st.error("You need to be logged in to manage allergies.")




def main():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None

    choice = sidebar_with_logo()

    if choice == "Login":
        if st.session_state['authenticated']:
            home()
        else:
            login()
    elif choice == "Register":
        register()
    elif choice == "Home":
        if st.session_state['authenticated']:
            home()
        else:
            st.error("You need to log in to access this page")
    elif choice == "Allergies":
        if st.session_state['authenticated']:
            allergies()
        else:
            st.error("You need to log in to access this page")
    elif choice == "Logout":
        if st.session_state['authenticated']:
            st.session_state['authenticated'] = False
            st.session_state['user_id'] = None
            st.success("Logged out successfully!")
            login()
            st.rerun()

if __name__ == '__main__':
    main()