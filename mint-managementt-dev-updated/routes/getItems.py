from flask import Flask, jsonify,Blueprint, request


import pandas as pd

# Create a Blueprint for the home route
getItems_bp = Blueprint('getItems_bp', __name__)

app = Flask(__name__)

# Load the CSV data into a DataFrame
data_sale = pd.read_csv('sales_data.csv')

@getItems_bp.route('/get_items', methods=['POST'])
def get_items():
    selected_category = request.json['category']
    print(f"Selected Category: {selected_category}")  # Debug print
    items = data_sale[data_sale['category'] == selected_category]['item_name'].tolist()
    print(f"Items found: {items}")  # Debug print
    return jsonify(items)