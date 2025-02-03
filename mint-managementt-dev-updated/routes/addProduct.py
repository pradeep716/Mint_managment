from flask import Flask, render_template, redirect, request, url_for, session, Blueprint
import json

CUSTOMER_DATA_FILE = 'customers.json'
PRODUCT_DATA_FILE = 'products.json'

# Create a Blueprint for the home route
addProduct_bp = Blueprint('addProduct_bp', __name__)

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


def write_product_data(data):
    with open(PRODUCT_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


@addProduct_bp.route('/add-product', methods=['GET', 'POST'])
def add_product():

    if request.method == 'POST':
        product_class = request.form['product_class']
        product_id = request.form['product_id']
        stock = request.form['stock']  # Stock will be set based on unit type
        product_state = request.form['product_state']  # Solid or Liquid
        unit = request.form['unit']  # Unit of measurement like kg, g, L, ml

        key_pair = request.form.get('key_pair')  # Optional field for key pair
        # vendor_name = request.form['vendor_name']
        # YYYY-MM-DD format
        manufacture_date = request.form['manufacture_date']
        expiry_date = request.form['expiry_date']  # YYYY-MM-DD format

        products = read_product_data()

        if product_id in products:
            return 'Product ID already exists! <a href="/add-product">Try again</a>'

        products[product_id] = {
            'product_class': product_class,
            'product_state': product_state,  # Solid or Liquid
            'stock': stock,  # Stock quantity with unit
            'unit': unit,  # Unit like kg, g, L, ml
            # 'vendor_name': vendor_name,
            'manufacture_date': manufacture_date,
            'expiry_date': expiry_date,
        }

        write_product_data(products)
        return 'Product added successfully! <a href="/enterprise_dashboard">Go back to dashboard</a>'

    customers = read_customer_data()
    return render_template('add_product.html', customers=customers)
