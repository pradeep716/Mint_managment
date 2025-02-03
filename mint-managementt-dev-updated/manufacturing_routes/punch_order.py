import json
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

ORDERS_FILE = 'punch_orders.json'

# create a blueprint for the dashboard route
punch_order_bp = Blueprint('punch_order_bp', __name__)

# Helper function to load orders from orders.json


def load_orders():
    try:
        with open(ORDERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Helper function to save orders to orders.json


def save_orders(orders):
    with open(ORDERS_FILE, 'w') as file:
        json.dump(orders, file, indent=4)


@punch_order_bp.route('/punch_order', methods=['GET', 'POST'])
def punch_order():
    if 'username' in session:
        if request.method == 'POST':
            # Collect all form data
            # order_number = request.form['order_number']
            client_name = request.form['client_name']
            client_email = request.form['client_email']
            client_phone = request.form['client_phone']
            client_address = request.form['client_address']
            shoe_types = request.form.getlist('shoe_type')
            quantities = request.form.getlist('quantity')
            key_pairs_per_ctn = request.form.getlist('key_pairs_per_ctn')
            size_ranges = request.form.getlist('size_range')
            materials = request.form.getlist('material')
            colors = request.form.getlist('color')
            custom_prices = request.form.getlist('custom_price')
            production_times = request.form.getlist('production_time')
            approval_status = request.form.get('approval_status') is not None
            additional_notes = request.form['additional_notes']

            # Ensure all entries are filled properly
            if len(shoe_types) != len(quantities) or len(shoe_types) != len(key_pairs_per_ctn):
                flash("Error: Mismatched shoe entries.", "danger")
                return redirect(url_for('punch_order'))

            order_details = {
                # 'order_number': order_number,
                'client_name': client_name,
                'client_email': client_email,
                'client_phone': client_phone,
                'client_address': client_address,
                'shoes': [{
                    'shoe_type': shoe_types[i],
                    'quantity': quantities[i],
                    'key_pairs_per_ctn': key_pairs_per_ctn[i],
                    'size_range': size_ranges[i],
                    'material': materials[i],
                    'color': colors[i],
                    'custom_price': custom_prices[i],
                    'production_time': production_times[i]
                } for i in range(len(shoe_types))],
                'approval_status': approval_status,
                'additional_notes': additional_notes
            }

            # Load existing orders, append the new order, and save it
            orders = load_orders()
            orders.append(order_details)
            save_orders(orders)

            flash("Order received and saved!", "success")
            return redirect(url_for('manufacturing_dashboard_bp.manufacturing_dashboard'))

        return render_template('punch_order.html')
    else:
        flash('Please login to access this page.', 'warning')
        return redirect(url_for('login'))
