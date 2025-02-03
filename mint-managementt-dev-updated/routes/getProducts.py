from flask import Flask, jsonify, request, Blueprint
import json

PRODUCT_DATA_FILE = 'products.json'

# Create a Blueprint for the home route
getProducts_bp = Blueprint('getProducts_bp', __name__)

app = Flask(__name__)

def read_product_data():
    try:
        with open(PRODUCT_DATA_FILE, 'r') as file:
            data = json.load(file)
            # print("Product Data Loaded:", data)  # Debugging output
            return data
    except FileNotFoundError:
        return {}

@getProducts_bp.route('/get-products')
def get_products():
    product_class = request.args.get('product_class')
    products = read_product_data()
    filtered_products = [
        {'id': product_id, 'stock': product['stock']}
        for product_id, product in products.items()
        if product['product_class'] == product_class
    ]
    return jsonify(filtered_products)