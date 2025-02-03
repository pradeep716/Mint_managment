import json
import os
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

PRODUCT_DATA_FILE = 'products.json'
# create a blueprint for the dashboard route
add_to_enterprise_bp = Blueprint('add_to_enterprise_bp', __name__)


@add_to_enterprise_bp.route('/add_to_enterprise', methods=['GET', 'POST'])
def add_to_enterprise():
    if request.method == 'GET':
        return render_template('add_to_enterprise.html')

    if request.method == 'POST':
        try:
            # Retrieve form data
            product_id = request.form.get('product_id')
            product_class = request.form.get('product_class')
            stock = request.form.get('stock')
            keypair = request.form.get('keypair')
            product_state = request.form['product_state']
            # price = request.form.get('price')  # This will no longer be saved in the new format
            manufacturing_date = request.form.get('manufacturing_date')
            expiry_date = request.form.get('expiry_date')
            # vendor_name = request.form.get('vendor_name')
            unit = request.form['unit']

            # Create a new entry with the required format
            product_entry = {
                "product_class": product_class,
                "product_state": product_state,
                "stock": stock,
                "keypair": keypair,
                'unit': unit,
                # "vendor_name": vendor_name,
                "manufacture_date": manufacturing_date,
                "expiry_date": expiry_date
            }

            # Load the existing inventory data
            try:
                with open(PRODUCT_DATA_FILE, 'r') as file:
                    inventory = json.load(file)
            except FileNotFoundError:
                inventory = {}  # If the file does not exist, initialize as an empty dictionary

            # Add or update the product entry using product_id as the key
            inventory[product_id] = product_entry

            # Save the updated inventory back to the file
            with open(PRODUCT_DATA_FILE, 'w') as file:
                json.dump(inventory, file, indent=4)

            # Redirect back to the dashboard or success page
            return redirect(url_for('production_dashboard_bp.production_dashboard'))
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 400
