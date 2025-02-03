from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, Blueprint, session, url_for
import json

PRODUCT_DATA_FILE = 'products.json'
CUSTOMER_DATA_FILE = 'customers.json'

# Create a Blueprint for the home route
enterprise_punchOrder_bp = Blueprint('enterprise_punchOrder_bp', __name__)

app = Flask(__name__)


def read_product_data():
    try:
        with open(PRODUCT_DATA_FILE, 'r') as file:
            data = json.load(file)
            # print("Product Data Loaded:", data)  # Debugging output
            return data
    except FileNotFoundError:
        return {}


def read_customer_data():
    try:
        with open(CUSTOMER_DATA_FILE, 'r') as file:
            data = json.load(file)
            # print("Customer Data Loaded:", data)  # Debugging output
            return data
    except FileNotFoundError:
        return {}


def read_orders_data():
    try:
        with open('orders.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file doesn't exist


def write_orders_data(orders):
    with open('orders.json', 'w') as f:
        json.dump(orders, f, indent=4)


def write_product_data(data):
    with open(PRODUCT_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


def get_product_classes():
    products = read_product_data()  # Load product data
    product_classes = {product['product_class']
                       for product in products.values()}
    return sorted(product_classes)


@enterprise_punchOrder_bp.route('/enterprise-punch-order', methods=['GET', 'POST'])
def punch_order():
    if 'username' not in session:
        return redirect(url_for('login_bp.login'))

    if 'customer_invoice_numbers' not in session:
        session['customer_invoice_numbers'] = {}

    with open('order_number.json', 'r') as f:
        order_data = json.load(f)
    last_order_number = order_data.get('last_order_number', 0)

    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        customer_name = read_customer_data().get(
            customer_id, {}).get('name', 'Unknown')

        product_classes = request.form.getlist('product_class[]')
        product_ids = request.form.getlist('product_id[]')
        stocks = request.form.getlist('stock[]')
        units = request.form.getlist('unit[]')
        vendor_names = request.form.getlist('vendor_name[]')
        manufacture_dates = request.form.getlist('manufacture_date[]')
        expiry_dates = request.form.getlist('expiry_date[]')

        products = read_product_data()  # Assuming this reads from products.json
        orders = read_orders_data()

        new_orders = []

        length = len(product_classes)
        if not (len(product_ids) == len(stocks) == len(units) == len(vendor_names) == len(manufacture_dates) == len(expiry_dates) == length):
            return "Error: All input lists must be of the same length."

        for i in range(length):
            product_class = product_classes[i]
            product_id = product_ids[i]
            # Use float for decimals
            stock = float(stocks[i]) if stocks[i] else 0
            unit = units[i]
            vendor_name = vendor_names[i]
            manufacture_date = manufacture_dates[i]
            expiry_date = expiry_dates[i]

            # Convert stock to kg or L based on unit
            if unit == 'g':
                stock = stock / 1000  # Convert grams to kilograms
                unit = 'kg'  # Update the unit to kg
            elif unit == 'ml':
                stock = stock / 1000  # Convert milliliters to liters
                unit = 'L'  # Update the unit to L

            last_order_number += 1
            invoice_number = f"{last_order_number:05d}"
            # Get the current date only
            order_date = datetime.now().strftime('%Y-%m-%d')

            new_orders.append({
                'invoice_number': invoice_number,
                'customer_name': customer_name,
                'product_class': product_class,
                'product_id': product_id,
                'stock': stock,  # Now in kg or L
                'unit': unit,    # Updated unit
                'vendor_name': vendor_name,
                'manufacture_date': manufacture_date,
                'expiry_date': expiry_date,
                'order_date': order_date
            })

            # Update the stock in products
            if product_id in products:
                products[product_id]['stock'] = float(
                    products[product_id]['stock']) - stock  # Deduct the punched order stock

            # Add new orders to the existing orders
            for order in new_orders:
                order_id = str(len(orders) + 1)  # Create a new order ID
                # Add the new order to the orders dictionary
                orders[order_id] = order

            # Check the orders before saving
            # print("Orders before saving:", orders)

            # Save the new orders to orders.json
            try:
                write_orders_data(orders)
                print("Orders saved successfully.")
            except Exception as e:
                print(f"Error saving orders: {e}")  # Log the error message

                # Update the products.json file with the new stock
            write_product_data(products)

        # Update the products.json file with the new stock
        write_product_data(products)

        with open('order_number.json', 'w') as f:
            json.dump({'last_order_number': last_order_number}, f, indent=4)

        flash('Order punched successfully!', 'success')
        return redirect(url_for('enterprise_dashboard_bp.dashboard'))

    return render_template('enterprise_punch_order.html', product_classes=get_product_classes(), customers=read_customer_data())
