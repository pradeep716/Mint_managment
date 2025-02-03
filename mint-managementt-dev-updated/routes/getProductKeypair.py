from flask import Flask, jsonify, request, Blueprint
import json

PRODUCT_DATA_FILE = 'products.json'

# Create a Blueprint for the home route
getProductKeypair_bp = Blueprint('getProductKeypair_bp', __name__)

app = Flask(__name__)


def read_product_data():
    try:
        with open(PRODUCT_DATA_FILE, 'r') as file:
            data = json.load(file)
            # print("Product Data Loaded:", data)  # Debugging output
            return data
    except FileNotFoundError:
        return {}

@getProductKeypair_bp.route('/get-product-keypair')
def get_product_keypair():
    product_id = request.args.get('product_id')
    products = read_product_data()
    product = products.get(product_id, {})
    return jsonify({'key_pair': product.get('key_pair', '')})