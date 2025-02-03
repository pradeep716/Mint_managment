import json
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for 

DATA_FILE = 'composition_data.json'

# Helper function to load orders from compositon_data.json
def load_composition_orders():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# create a blueprint for the dashboard route
order_of_composition_bp= Blueprint('order_of_composition_bp',__name__)


# Route for order_of_composition
@order_of_composition_bp.route('/order_of_composition', methods=['GET', 'POST'])
def order_of_composition():
    orders = load_composition_orders()
    # print(orders)
    # Flatten the list if it's a list of lists
    flattened_orders = [order for sublist in orders for order in sublist]
    return render_template('order_of_composition.html', orders=flattened_orders)
