from flask import Flask, render_template, redirect, request, url_for, session , Blueprint
import json

PRODUCT_DATA_FILE = 'products.json'

# Create a Blueprint for the home route
viewInventory_bp = Blueprint('viewInventory_bp', __name__)

app = Flask(__name__)

def read_product_data():
    try:
        with open(PRODUCT_DATA_FILE, 'r') as file:
            data = json.load(file)
            # print("Product Data Loaded:", data)  # Debugging output
            return data
    except FileNotFoundError:
        return {}

@viewInventory_bp.route('/view-inventory', methods=['GET'])
def view_inventory():
    if 'username' not in session:
        return redirect(url_for('login_bp.login'))

    # Load existing products
    products = read_product_data()

    # Initialize total stock
    total_stock_by_class = {}

    # Ensure correct calculation of stock for display in kg
    for product_id, details in products.items():
        # Convert stock values based on unit
        if details['unit'] == 'grams':
            stock_in_kg = float(details['stock']) / 1000  # Convert grams to kg
            details['stock'] = stock_in_kg                # Update stock to kg
            details['unit'] = 'kg'                        # Update unit to kg
        elif details['unit'] == 'milliliters':
            stock_in_liters = float(details['stock']) / 1000  # Convert milliliters to liters
            details['stock'] = stock_in_liters                # Update stock to liters
            details['unit'] = 'liters'                        # Update unit to liters

        # Aggregate stock by product class
        product_class = details['product_class']
        if product_class in total_stock_by_class:
            total_stock_by_class[product_class] += float(details['stock'])
        else:
            total_stock_by_class[product_class] = float(details['stock'])

    return render_template('view_inventory.html', products=products, total_stock_by_class=total_stock_by_class)