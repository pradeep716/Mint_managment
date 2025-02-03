# import all necessary modules
import json
from flask import Blueprint, request, jsonify, render_template

PLACE_ORDER_FILE = 'place_order.json'

# create a blueprint for view placed order
view_placed_order_bp = Blueprint('view_placed_order_bp', __name__)


def load_placed_order():
    try:
        with open(PLACE_ORDER_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_orders(orders):
    with open(PLACE_ORDER_FILE, 'w') as file:
        json.dump(orders, file, indent=4)


@view_placed_order_bp.route('/cancel_order', methods=['POST'])
def cancel_order():
    data = request.json
    order_id = int(data['orderId'])
    composition_id = data['compositionId']

    # Load existing orders
    orders = load_placed_order()

    # Find the order and remove the specified composition
    for order in orders:
        if order['orderId'] == order_id:
            order['composition'] = [
                comp for comp in order['composition'] if comp['compositionId'] != composition_id
            ]
            break

    # Save the updated orders back to the file
    save_orders(orders)

    return jsonify({'message': 'Composition canceled successfully'}), 200


@view_placed_order_bp.route('/view_placed_order', methods=['GET', 'POST'])
def view_placed_order():
    orders = load_placed_order()
    for index, order in enumerate(orders, start=1):
        order['orderId'] = index
    save_orders(orders)  # Save updated orders with orderId
    return render_template('view_placed_order.html', orders=orders)
