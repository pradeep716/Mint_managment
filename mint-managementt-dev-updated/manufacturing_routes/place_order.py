import json
from flask import Blueprint,render_template

DATA_FILE = 'composition_data.json'

# create a blueprint for the dashboard route
place_order_bp= Blueprint('place_order_bp',__name__)

# Helper function to load orders from compositon_data.json
def load_composition_orders():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
# Route for view compostion inventory form
@place_order_bp.route('/place_order', methods=['GET', 'POST'])
def place_order():
    orders = load_composition_orders()
    # print(orders)
    # Flatten the list if it's a list of lists
    flattened_orders = [order for sublist in orders for order in sublist]
    return render_template('place_order.html', orders=flattened_orders)
