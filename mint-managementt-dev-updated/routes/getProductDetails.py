from flask import Flask, jsonify, request, Blueprint
import json

PRODUCT_DATA_FILE = 'products.json'

# Create a Blueprint for the home route
getProductDetails_bp = Blueprint('getProductDetails_bp', __name__)

app = Flask(__name__)

def read_product_data():
    try:
        with open(PRODUCT_DATA_FILE, 'r') as file:
            data = json.load(file)
            # print("Product Data Loaded:", data)  # Debugging output
            return data
    except FileNotFoundError:
        return {}

@getProductDetails_bp.route('/get-product-details')
def get_product_details():
    product_id = request.args.get('product_id')
    products = read_product_data()

    if product_id in products:
        product_details = products[product_id]
        return jsonify({
            'product_state': product_details['product_state'],
            'manufacture_date': product_details['manufacture_date'],
            'expiry_date': product_details['expiry_date'],
            'unit': product_details['unit'],
            'vendor_name': product_details['vendor_name']
        })
    return jsonify({})