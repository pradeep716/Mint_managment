import json
from flask import Blueprint,  render_template

DATA_FILE = 'composition_data.json'

# create a blueprint for the dashboard route
final_product_inventory_bp = Blueprint('final_product_inventory_bp',__name__)

# Helper function to load orders from compositon_data.json
def load_composition_orders():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

@final_product_inventory_bp.route('/final_product_inventory', methods=['GET', 'POST'])
def final_product_inventory():
    orders = load_composition_orders()
    # print(orders)
    # Flatten the list if it's a list of lists
    flattened_orders = [order for sublist in orders for order in sublist]
    return render_template('final_product_inventory.html', orders=flattened_orders)
