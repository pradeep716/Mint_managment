from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, Blueprint, session, url_for
import json

PRODUCT_DATA_FILE = 'products.json'
# CUSTOMER_DATA_FILE = 'customers.json'

# Create a Blueprint for the home route
revokeOrder_bp = Blueprint('revokeOrder_bp', __name__)

app = Flask(__name__)


def read_orders_data():
    try:
        with open('orders.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file doesn't exist


def read_product_data():
    try:
        with open(PRODUCT_DATA_FILE, 'r') as file:
            data = json.load(file)
            # print("Product Data Loaded:", data)  # Debugging output
            return data
    except FileNotFoundError:
        return {}


def write_product_data(data):
    with open(PRODUCT_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


def write_orders_data(orders):
    with open('orders.json', 'w') as f:
        json.dump(orders, f, indent=4)


@revokeOrder_bp.route('/revoke-order', methods=['GET', 'POST'])
def revoke_order():
    if 'username' not in session:
        return redirect(url_for('login_bp.login'))

    # Read the current orders and products
    orders = read_orders_data()
    products = read_product_data()

    if request.method == 'POST':
        order_id = request.form.get('order_id')

        # Check if the order exists
        if order_id and order_id in orders:
            order = orders[order_id]
            product_id = order['product_id']
            # Get the stock to be returned from the order
            stock_to_restock = order.get('stock', 0)

            # Fetch the product details from products.json
            if product_id in products:
                # Get the current stock from products.json
                current_stock = products[product_id].get('stock', 0)

                # Ensure current_stock and stock_to_restock are properly converted to floats
                current_stock = float(current_stock) if isinstance(current_stock, (int, float, str)) and str(
                    current_stock).replace('.', '', 1).isdigit() else 0
                stock_to_restock = float(stock_to_restock) if isinstance(stock_to_restock, (int, float, str)) and str(
                    stock_to_restock).replace('.', '', 1).isdigit() else 0

                # Convert stock_to_restock to the appropriate base unit based on the unit in the order
                unit = order.get('unit', '').lower()

                if unit == 'g':
                    # If the unit in the order is grams, no conversion needed
                    pass
                elif unit == 'kg':
                    # If the unit is kilograms, convert to grams
                    stock_to_restock *= 1000
                elif unit == 'ml':
                    # If the unit in the order is milliliters, no conversion needed
                    pass
                elif unit == 'l':
                    # If the unit is liters, convert to milliliters
                    stock_to_restock *= 1000

                # Add the restocked quantity to the current stock
                # Ensure we are working with the correct unit from products.json
                if products[product_id]['unit'] == 'kg':
                    current_stock_kg = current_stock  # Already in kg
                    stock_to_add_kg = stock_to_restock / 1000  # Convert restocked grams to kg
                    new_stock = current_stock_kg + stock_to_add_kg
                elif products[product_id]['unit'] == 'L':
                    current_stock_L = current_stock  # Already in liters
                    # Convert restocked milliliters to liters
                    stock_to_add_L = stock_to_restock / 1000
                    new_stock = current_stock_L + stock_to_add_L
                else:
                    # If the unit in products.json is grams or milliliters, directly add the quantities
                    new_stock = current_stock + stock_to_restock

                # Ensure the new stock value is valid (not negative)
                if new_stock < 0:
                    new_stock = 0  # Prevent negative stock values

                # Update the product's stock in the products dictionary
                products[product_id]['stock'] = new_stock

                # Write the updated product data back to products.json
                write_product_data(products)

                # Remove the order from orders.json
                del orders[order_id]
                write_orders_data(orders)

                flash('Order revoked and stock updated successfully!', 'success')
                return redirect(url_for('revokeOrder_bp.revoke_order'))
            else:
                return "Product ID not found in inventory.", 404
        else:
            return "Order ID not found.", 404

    # Render the revoke order page with available orders
    return render_template('revoke_order.html', orders=orders)
