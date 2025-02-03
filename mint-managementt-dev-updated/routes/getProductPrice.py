from flask import Flask, jsonify, request, Blueprint
import json

PRODUCT_DATA_FILE = 'products.json'

# Create a Blueprint for the home route
getProductPrice_bp = Blueprint('getProductPrice_bp', __name__)

app = Flask(__name__)

def read_product_data():
    try:
        with open(PRODUCT_DATA_FILE, 'r') as file:
            data = json.load(file)
            # print("Product Data Loaded:", data)  # Debugging output
            return data
    except FileNotFoundError:
        return {}
    
@getProductPrice_bp.route('/get-product-price')
def get_product_price():
    product_id = request.args.get('product_id')
    products = read_product_data()
    product = products.get(product_id, {})
    return jsonify({'price': product.get('price_per_pair', 0.0)})