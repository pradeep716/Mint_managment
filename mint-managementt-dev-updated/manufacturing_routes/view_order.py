import json
from flask import Blueprint, render_template

ORDERS_FILE = 'punch_orders.json'

# create a blueprint for the dashboard route
view_order_bp = Blueprint('view_order_bp', __name__)

# Helper function to load orders from orders.json


def load_orders():
    try:
        with open(ORDERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_orders(orders):
    with open(ORDERS_FILE, 'w') as file:
        json.dump(orders, file, indent=4)


# Route for view order details form
@view_order_bp.route('/view_order', methods=['GET', 'POST'])
def view_order():
    orders = load_orders()
    for index, order in enumerate(orders, start=1):
        order['orderId'] = index
    save_orders(orders)  # Save updated orders with orderId
    return render_template('view_order.html', orders=orders)
