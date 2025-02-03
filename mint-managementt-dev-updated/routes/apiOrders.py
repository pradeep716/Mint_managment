from datetime import datetime
from flask import Flask, jsonify, render_template, request, Blueprint
import json

# Create a Blueprint for the home route
apiOrders_bp = Blueprint('apiOrders_bp', __name__)

app = Flask(__name__)

@apiOrders_bp.route('/api/orders')
def get_orders():
    file_path = 'C:\\Users\\prs90\\OneDrive\\Desktop\\Vinesh 07-oct\\orders.json'

    product_class = request.args.get('product_class')
    product_id = request.args.get('product_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    print(
        f"Received product_class: {product_class}, product_id: {product_id}, start_date: {start_date}, end_date: {end_date}")

    try:
        with open(file_path, 'r') as f:
            orders = json.load(f)

        # Initialize filtered_orders
        filtered_orders = []

        # Parse dates if provided
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                print(f"Parsed start_date: {start_date}")
            except ValueError:
                print("Error parsing start_date")
                return jsonify({"error": "Invalid start date format"}), 400

        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                print(f"Parsed end_date: {end_date}")
            except ValueError:
                print("Error parsing end_date")
                return jsonify({"error": "Invalid end date format"}), 400

        # Iterate through orders
        for order in orders.values():
            # Check product class if provided
            if product_class and order["product_class"].lower() != product_class.lower():
                continue

            # Check product ID if provided
            if product_id and order["product_id"].lower() != product_id.lower():
                continue

            # Parse the order date from the order data
            order_date = datetime.strptime(order["order_date"], '%Y-%m-%d')

            # Check date range
            if start_date and order_date < start_date:
                continue
            if end_date and order_date > end_date:
                continue

            # Append filtered orders with the required fields
            filtered_orders.append({
                "invoice_number": order["invoice_number"],
                "customer_name": order["customer_name"],
                "product_class": order["product_class"],  # Product Class
                "product_id": order["product_id"],  # Product ID
                "stock": order["stock"],
                "unit": order["unit"],
                "vendor_name": order["vendor_name"],
                "manufacture_date": order["manufacture_date"],
                "expiry_date": order["expiry_date"],
                "order_date": order["order_date"]
            })

        return jsonify(filtered_orders)

    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to decode JSON"}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500