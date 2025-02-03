from flask import Blueprint, jsonify, render_template, request
import json

# Create a Blueprint for the order summary route
orderSummary_bp = Blueprint('orderSummary_bp', __name__)

def read_orders_data():
    try:
        with open('orders.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file doesn't exist

# Route to handle both rendering the template and API responses
@orderSummary_bp.route('/order-summary', methods=['GET', 'POST'])
def order_summary():

    orders = read_orders_data()
    
    # Check if the request is an API call (e.g., AJAX) by looking for an 'X-Requested-With' header
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        orders = read_orders_data()

        # Get unique product classes
        product_classes = list(set(order['product_class'] for order in orders.values()))
        return jsonify({'product_classes': product_classes})
    
    # If not an API call, render the template
    return render_template('order_summary.html')

# API Route to fetch product IDs for a specific product class
@orderSummary_bp.route('/get-product-ids', methods=['GET'])
def get_product_ids():
    product_class = request.args.get('product_class')
    orders = read_orders_data()

    # Filter product IDs by the selected product class
    product_ids = [
        order['product_id']
        for order in orders.values()
        if order['product_class'] == product_class
    ]

    return jsonify(product_ids)

# API Route to filter orders based on form inputs
@orderSummary_bp.route('/filter-orders', methods=['POST'])
def filter_orders():
    data = request.form
    product_class = data.get('product_class', '').strip()
    product_id = data.get('product_id', '').strip()
    start_date = data.get('start_date', '').strip()
    end_date = data.get('end_date', '').strip()
    # print('data',data)
    orders = read_orders_data()

    # Apply filters
    filtered_orders = [
        order
        for order in orders.values()
        if (not product_class or order['product_class'] == product_class) and
           (not product_id or order['product_id'] == product_id) and
           (not start_date or order['order_date'] >= start_date) and
           (not end_date or order['order_date'] <= end_date)
    ]
    # print(filtered_orders)
    return jsonify({'filtered_orders': filtered_orders})