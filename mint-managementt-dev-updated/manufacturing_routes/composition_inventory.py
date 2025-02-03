import json
from flask import Blueprint, jsonify, render_template

# create a blueprint for the dashboard route
composition_inventory_bp = Blueprint('composition_inventory_bp', __name__)

# Route for view composition inventory form


@composition_inventory_bp.route('/composition_inventory', methods=['GET', 'POST'])
def get_composition_inventory():
    try:
        # Load the JSON data
        with open('composition_data.json', 'r') as file:
            composition_data = json.load(file)

        # Handle the nested structure
        orders = []
        # composition_data is [[ {...} ]]
        for outer_list in composition_data:
            # outer_list is [ {...} ]
            for item in outer_list:
                # item is {...}
                if isinstance(item, dict) and 'compositions' in item:
                    orders.append(item)

        # print("Debug - orders:", orders)  # Add this debug print
        return render_template('composition_inventory.html', orders=orders)

    except Exception as e:
        # print(f"Error: {str(e)}")  # Add this for debugging
        return jsonify({'success': False, 'message': str(e)}), 500
