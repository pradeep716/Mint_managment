import json
from flask import Blueprint, jsonify, render_template, session

# Create a blueprint for the dashboard route
vendor_view_inventory_bp = Blueprint('vendor_view_inventory_bp', __name__)

# Route for viewing the composition inventory form
@vendor_view_inventory_bp.route('/vendor_view_inventory', methods=['GET', 'POST'])
def get_composition_inventory():
    try:
        # Load the JSON data
        with open('vendor_composition_data.json', 'r') as file:
            vendor_composition_data = json.load(file)

        # Get the logged-in vendor's username from the session
        vendor_name = session.get('username', None)

        # If the vendor is not logged in, redirect to login page or show an error
        if not vendor_name:
            return jsonify({'success': False, 'message': 'Vendor not logged in!'}), 401

        # Handle the nested structure
        filtered_orders = []

        # composition_data is [[ {...} ]]
        for outer_list in vendor_composition_data:
            # outer_list is [ {...} ]
            for item in outer_list:
                # item is {...}
                if isinstance(item, dict) and 'compositions' in item:
                    # Check if the vendor_name matches the logged-in vendor name
                    if item.get('vendor_name') == vendor_name:
                        filtered_orders.append(item)

        if not filtered_orders:
         return render_template('vendor_view_inventory.html', orders=[], message="No compositions added yet.")
 
        # Render the template with filtered orders for the logged-in vendor
        return render_template('vendor_view_inventory.html', orders=filtered_orders)

    except Exception as e:
        # Handle any exceptions and print for debugging
        return jsonify({'success': False, 'message': str(e)}), 500
