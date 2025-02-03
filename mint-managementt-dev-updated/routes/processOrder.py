from flask import Flask, jsonify, request, Blueprint
import json

PRODUCT_DATA_FILE = 'products.json'

# Create a Blueprint for the home route
processOrder_bp = Blueprint('processOrder_bp', __name__)

app = Flask(__name__)

def read_product_data():
    try:
        with open(PRODUCT_DATA_FILE, 'r') as file:
            data = json.load(file)
            print("Product Data Loaded:", data)  # Debugging output
            return data
    except FileNotFoundError:
        return {}

def write_product_data(data):
    with open(PRODUCT_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def update_inventory_after_order(order_data):
    # Load current inventory
    inventory = read_product_data()
    print("Initial Inventory:", inventory)  # Debugging output

    # Extract order details
    product_class = order_data["product_class"]
    stock_quantity = order_data["stock"]  # In kg
    print("Stock Quantity to Deduct:", stock_quantity)  # Debugging output

    # Convert stock quantity from kg to grams
    stock_quantity_grams = stock_quantity * 1000  # Convert kg to grams

    # Update inventory
    if product_class in inventory:
        product_details = inventory[product_class]
        print("Current Product Details:", product_details)  # Debugging output
        if product_details['stock'] >= stock_quantity:  # Check stock availability
            product_details['stock'] -= stock_quantity
            print("Updated Stock:", product_details['stock'])  # Debugging output
        else:
            print("Insufficient stock!")  # Debugging output
    else:
        print("Product class not found in inventory!")  # Debugging output

    # Save updated inventory
    write_product_data(inventory)

@processOrder_bp.route('/process-order', methods=['POST'])
def process_order():
    order_data = request.get_json()  # Assuming you're sending JSON data

    # Call the function to update inventory after the order
    update_inventory_after_order(order_data)

    return jsonify({"message": "Order processed successfully!"}), 200
