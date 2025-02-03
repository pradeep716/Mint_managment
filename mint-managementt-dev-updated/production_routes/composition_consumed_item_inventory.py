import json
from flask import Blueprint, render_template

PRODUCTION_COMPOSITION_FILE = 'production_composition_consume.json'

# create a blueprint for the dashboard route
composition_consumed_item_inventory_bp = Blueprint(
    'composition_consumed_item_inventory_bp', __name__)

# Helper function to load orders from quotation_order.json


def load_consumed_composition():
    try:
        with open(PRODUCTION_COMPOSITION_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


@composition_consumed_item_inventory_bp.route('/composition_consumed_item_inventory', methods=['GET', 'POST'])
def consumed_composition_items():
    orders = load_consumed_composition()
    flattened_orders = [order for sublist in orders for order in sublist]

    return render_template('composition_consumed_item_inventory.html', orders=flattened_orders)
