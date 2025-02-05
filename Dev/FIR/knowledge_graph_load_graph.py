import sqlite3
import networkx as nx
import matplotlib.pyplot as plt

def load_graph_from_sqlite():
    conn = sqlite3.connect('instance/site.db')  # Connect to site.db
    cursor = conn.cursor()

    # Create a directed graph
    G = nx.DiGraph()

    # Load Users
    cursor.execute("SELECT id, username FROM user")
    users = cursor.fetchall()
    for user in users:
        node_id = ('User', user[0])
        G.add_node(node_id, type='User', name=user[1])

    # Load Health Conditions
    cursor.execute("SELECT id, condition_name FROM health_conditions")
    conditions = cursor.fetchall()
    for condition in conditions:
        node_id = ('HealthCondition', condition[0])
        G.add_node(node_id, type='HealthCondition', name=condition[1])

    # Load Ingredients
    cursor.execute("SELECT id, ingredient_name FROM ingredients")
    ingredients = cursor.fetchall()
    for ingredient in ingredients:
        node_id = ('Ingredient', ingredient[0])
        G.add_node(node_id, type='Ingredient', name=ingredient[1])

    # Load Food Items
    cursor.execute("SELECT id, food_name FROM food_items")
    foods = cursor.fetchall()
    for food in foods:
        node_id = ('Food', food[0])
        G.add_node(node_id, type='Food', name=food[1])

    # Load Relationships
    cursor.execute("SELECT source_id, source_type, target_id, target_type, relation_type FROM relationships")
    relationships = cursor.fetchall()
    for relation in relationships:
        source_id = (relation[1], relation[0])  # (source_type, source_id)
        target_id = (relation[3], relation[2])  # (target_type, target_id)
        relation_type = relation[4]
        friendly_relation_type = relation_type.replace("_", " ").title()
        if source_id in G and target_id in G:
            G.add_edge(source_id, target_id, relation_type=friendly_relation_type)
        else:
            print(f"Warning: One of the nodes {source_id} or {target_id} does not exist in the graph.")

    conn.close()
    return G

# Load and debug the graph
graph = load_graph_from_sqlite()

def debug_graph(G):
    print("Nodes in the graph:", G.nodes(data=True))
    print("Edges in the graph:", G.edges(data=True))

debug_graph(graph)

# Visualization
def visualize_graph(G):
    pos = nx.kamada_kawai_layout(G)

    # Create different node colors based on the node type
    node_colors = []
    labels = {}
    for node, data in G.nodes(data=True):
        node_type = data['type']
        if node_type == 'User':
            node_colors.append('dodgerblue')
            labels[node] = f"User: {data['name']}"
        elif node_type == 'HealthCondition':
            node_colors.append('firebrick')
            labels[node] = f"Condition: {data['name']}"
        elif node_type == 'Ingredient':
            node_colors.append('mediumseagreen')
            labels[node] = f"Ingredient: {data['name']}"
        elif node_type == 'Food':
            node_colors.append('darkorange')
            labels[node] = f"Food: {data['name']}"

    # Set custom figure size
    plt.figure(figsize=(8, 6))  # Adjust window size for better visibility

    # Draw the graph with smaller node size and thinner edges
    nx.draw(G, pos, with_labels=False, node_color=node_colors, node_size=3000,  # Smaller node size
            font_size=8, font_color='white', edgecolors='black', linewidths=1)  # Reduce linewidths and font size

    # Add node labels with adjusted font size
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_color='black')

    # Increase edge thickness and add different styles if needed
    nx.draw_networkx_edges(G, pos, width=1.5)  # Thinner edges

    # Draw edge labels (relationships) with smaller font size
    edge_labels = nx.get_edge_attributes(G, 'relation_type')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)  # Smaller edge label font size

    # Show the plot
    plt.tight_layout()  # Ensure the layout fits within the figure area
    plt.show()


def visualize_filtered_graph_with_ingredients_local_test(G, user_id):
    # Filter to show conditions, ingredients, and foods relevant to the user's allergies
    relevant_nodes = set()
    edges_to_display = []

    # Retrieve the user's name based on the user_id
    user_name = None
    for node, data in G.nodes(data=True):
        if node == ('User', user_id):
            user_name = data['name']  # Get the correct username
            break

    # Ensure we have a valid user_name before continuing
    if not user_name:
        print(f"User with ID {user_id} not found in the graph.")
        return

    # Find the conditions the user is allergic to
    for u, v, edge_data in G.edges(data=True):
        if u == ('User', user_id) and edge_data['relation_type'] == 'Has Condition':
            relevant_nodes.update([u, v])
            edges_to_display.append((u, v))
            health_condition = v

            # Find ingredients that cause this health condition
            for ingredient, condition, edge_data_2 in G.edges(data=True):
                if condition == health_condition and edge_data_2['relation_type'] == 'Causes Allergy':
                    relevant_nodes.update([ingredient, condition])
                    edges_to_display.append((ingredient, condition))

                    # Find foods that contain this ingredient
                    for food, ingredient_in_food, edge_data_3 in G.edges(data=True):
                        if ingredient_in_food == ingredient and edge_data_3['relation_type'] == 'Contains Ingredient':
                            relevant_nodes.update([food, ingredient_in_food])
                            edges_to_display.append((food, ingredient_in_food))

    # Create a subgraph based on relevant edges
    subgraph = G.edge_subgraph(edges_to_display).copy()

    # Visualize the subgraph
    pos = nx.spring_layout(subgraph)  # Use spring layout for better positioning

    # Set custom figure size
    plt.figure(figsize=(10, 8))  # Set window size to be larger (10x8)

    node_colors = []
    labels = {}
    for node, data in subgraph.nodes(data=True):
        node_type = data['type']
        if node_type == 'User':
            node_colors.append('dodgerblue')
            labels[node] = f"User: {user_name}"  # Correctly display the user's name
        elif node_type == 'HealthCondition':
            node_colors.append('firebrick')
            labels[node] = f"Condition: {data['name']}"
        elif node_type == 'Ingredient':
            node_colors.append('mediumseagreen')
            labels[node] = f"Ingredient: {data['name']}"
        elif node_type == 'Food':
            node_colors.append('darkorange')
            labels[node] = f"Food: {data['name']}"

    nx.draw(subgraph, pos, with_labels=False, node_color=node_colors, node_size=6000, font_size=12, font_color='white',
            edgecolors='black', linewidths=2)

    # Add labels to the nodes
    nx.draw_networkx_labels(subgraph, pos, labels, font_size=12, font_color='black')

    # Draw edges
    nx.draw_networkx_edges(subgraph, pos, width=2)

    # Draw edge labels (relationships)
    edge_labels = nx.get_edge_attributes(subgraph, 'relation_type')
    nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=edge_labels, font_size=10)

    # Show the plot
    plt.show()


# Call the visualization function, passing in the graph and the specific user ID
visualize_filtered_graph_with_ingredients_local_test(graph, user_id=3)


# Visualize the graph (ALL)
visualize_graph(graph)

# Visualize filtered graphs for each user
#for user in users:
#    username = user[0]
#    cursor.execute("SELECT id FROM Users WHERE username = ?", (username,))
#    user_id = cursor.fetchone()[0]
#    print(f"Visualizing graph for {username} (User ID: {user_id})")
#    visualize_filtered_graph_with_ingredients(graph, user_id=user_id)


#For website graph:
def visualize_filtered_graph_with_ingredients(G, user_id, dish_name, dish_ingredients):

    import matplotlib.pyplot as plt
    import networkx as nx

    # Filter to show only the relevant parts for the current dish and user's allergies
    relevant_nodes = set()
    edges_to_display = []

    # Retrieve the user's name based on the user_id
    user_node = ('User', user_id)
    user_name = G.nodes[user_node]['name'] if user_node in G else None

    # Ensure we have a valid user_name before continuing
    if not user_name:
        print(f"User with ID {user_id} not found in the graph.")
        return None  # Return None to indicate failure

    # Find the dish node in the graph
    dish_node = None
    for node, data in G.nodes(data=True):
        if data['type'] == 'Food' and data['name'].lower() == dish_name.lower():
            dish_node = node
            break

    if not dish_node:
        print(f"Dish '{dish_name}' not found in the graph.")
        return None  # Return None to indicate failure

    # Add the dish node to the relevant nodes
    relevant_nodes.add(dish_node)

    # For each ingredient in the dish, check if it causes any allergies the user has
    # First, get the ingredient nodes corresponding to dish_ingredients
    dish_ingredient_nodes = []
    for ingredient_name in dish_ingredients:
        # Find the ingredient node
        ingredient_node = None
        for node, data in G.nodes(data=True):
            if data['type'] == 'Ingredient' and data['name'].lower() == ingredient_name.lower():
                ingredient_node = node
                break
        if ingredient_node:
            dish_ingredient_nodes.append(ingredient_node)
            # Add edge from dish to ingredient if it exists
            if G.has_edge(dish_node, ingredient_node):
                edges_to_display.append((dish_node, ingredient_node))
                relevant_nodes.update([dish_node, ingredient_node])
            elif G.has_edge(ingredient_node, dish_node):
                edges_to_display.append((ingredient_node, dish_node))
                relevant_nodes.update([dish_node, ingredient_node])
            else:
                # Edge does not exist; we can add it temporarily for visualization
                edges_to_display.append((dish_node, ingredient_node))
                relevant_nodes.update([dish_node, ingredient_node])
        else:
            print(f"Ingredient '{ingredient_name}' not found in the graph.")

    # Now, for each ingredient in the dish, check if it causes any allergies the user has
    for ingredient_node in dish_ingredient_nodes:
        # For each health condition that this ingredient causes
        for _, health_condition_node, edge_data in G.edges(ingredient_node, data=True):
            if edge_data['relation_type'] == 'Causes Allergy':
                # Check if the user has this health condition
                if G.has_edge(user_node, health_condition_node):
                    # User has this allergy
                    relevant_nodes.update([ingredient_node, health_condition_node])
                    edges_to_display.append((ingredient_node, health_condition_node))
                    edges_to_display.append((user_node, health_condition_node))
                    relevant_nodes.update([user_node, health_condition_node])

    # Create a subgraph based on relevant edges
    subgraph = G.edge_subgraph(edges_to_display).copy()

    # Visualization code with adjustments
    # Increase the figure size for better readability
    fig, ax = plt.subplots(figsize=(12, 8))

    # Use spring layout with adjusted parameters to reduce overlap
    pos = nx.spring_layout(subgraph, k=1.2, iterations=100)

    # Prepare node colors and labels
    node_colors = []
    labels = {}
    for node, data in subgraph.nodes(data=True):
        node_type = data['type']
        if node_type == 'User':
            node_colors.append('dodgerblue')
            labels[node] = f"User: {user_name}"
        elif node_type == 'HealthCondition':
            node_colors.append('firebrick')
            labels[node] = f"Condition: {data['name']}"
        elif node_type == 'Ingredient':
            node_colors.append('mediumseagreen')
            labels[node] = f"Ingredient: {data['name']}"
        elif node_type == 'Food':
            node_colors.append('darkorange')
            labels[node] = f"Food: {data['name']}"

    # Draw nodes and edges
    nx.draw_networkx_edges(subgraph, pos, width=2, alpha=0.5, ax=ax)
    nx.draw_networkx_nodes(subgraph, pos, node_color=node_colors, node_size=800, alpha=0.9, edgecolors='black', linewidths=1.5, ax=ax)

    # Adjust label positions to prevent overlap with nodes
    label_pos = {node: (x, y + 0.05) for node, (x, y) in pos.items()}

    # Draw labels with bounding boxes to enhance readability
    nx.draw_networkx_labels(
        subgraph,
        label_pos,
        labels,
        font_size=9,
        font_family='sans-serif',
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=0.2),
        ax=ax
    )

    # Optionally, draw edge labels
    edge_labels = nx.get_edge_attributes(subgraph, 'relation_type')
    nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=edge_labels, font_size=8, ax=ax)

    plt.axis('off')
    plt.tight_layout()

    # Return the figure
    return fig

