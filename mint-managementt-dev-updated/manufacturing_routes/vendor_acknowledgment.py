import json
from flask import Blueprint, render_template, session, redirect, url_for, flash

SUPPLY_DATA = 'supply_data.json'

# Create a blueprint for the dashboard route
vendor_acknowledgment_bp = Blueprint('vendor_acknowledgment_bp', __name__)

# Helper function to load orders from supply_data.json
def load_orders():
    try:
        with open(SUPPLY_DATA, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Route for view order details form
@vendor_acknowledgment_bp.route('/vendor_acknowledgment', methods=['GET', 'POST'])
def view_order():

    orders = load_orders()
    # Get the vendor's username from session
    vendor_name = session.get('username')

    if not vendor_name:
        flash("You need to log in first.", "error")
        return redirect(url_for('auth.login'))  # Redirect to the login page if not logged in

    # Load orders from the supply data file
    orders = load_orders()

    # Filter orders to only include those belonging to the logged-in vendor
    vendor_orders = [order for order in orders if order.get('vendor_name') == vendor_name]

    # If no orders are found for the vendor, flash a message and redirect
    if not vendor_orders:
        flash("No orders found for the logged-in vendor.", "warning")
        return redirect(url_for('vendor_acknowledgment'))  # Redirect to the vendor dashboard or another page

    return render_template('vendor_acknowledgment.html', orders=vendor_orders)
