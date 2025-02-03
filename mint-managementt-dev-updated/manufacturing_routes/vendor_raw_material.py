from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
import json
import os

DATA_FILE = 'vendor_composition_data.json'

# Create a blueprint for the raw material route
vendor_raw_material_bp = Blueprint('vendor_raw_material_bp', __name__)

# Function to save data to a JSON file
def save_data(data, filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            json.dump([], file)  # Create an empty list in the file

    with open(filename, 'r') as file:
        current_data = json.load(file)

    # Ensure current_data is a list of lists
    if not isinstance(current_data, list):
        current_data = []

    current_data.append(data)  # Append the new data

    with open(filename, 'w') as file:
        json.dump(current_data, file, indent=4)

# Helper function to process the composition
def process_composition(composition, vendor_name, current_data):
    for entry in current_data:
        for item in entry:
            for existing_composition in item['compositions']:
                if existing_composition['composition_id'] == composition['composition_id']:
                    if (existing_composition['composition_name'] == composition['composition_name'] and
                        existing_composition['composition_type'] == composition['composition_type'] and
                        existing_composition['unit'] == composition['unit'] and
                        item['vendor_name'] == vendor_name):
                        existing_composition['amount'] += composition['amount']
                        return current_data, False
                    else:
                        break
    new_entry = {'vendor_name': vendor_name, 'compositions': [composition]}
    current_data.append([new_entry])
    return current_data, True

@vendor_raw_material_bp.route('/get_composition_data', methods=['GET'])
def get_composition_data():
    composition_id = request.args.get('composition_id')

    if not composition_id:
        return jsonify({'success': False, 'message': 'Composition ID is required'}), 400

    # Load current data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            current_data = json.load(file)
    else:
        return jsonify({'success': False, 'message': 'No composition data available'}), 404

    # Get vendor name from session
    vendor_name = session.get('username', None)
    if not vendor_name:
        return jsonify({'success': False, 'message': 'Vendor not logged in!'}), 401

    # Search for the composition ID within the vendor's data
    for entry in current_data:
        for item in entry:
            if item.get('vendor_name') == vendor_name:
                for composition in item.get('compositions', []):
                    if composition.get('composition_id') == composition_id:
                        return jsonify({
                            'success': True,
                            'composition_name': composition.get('composition_name'),
                            'composition_type': composition.get('composition_type'),
                            'amount': composition.get('amount'),
                            'unit': composition.get('unit')
                        })

    return jsonify({'success': False, 'message': 'Composition ID not found'}), 404



@vendor_raw_material_bp.route('/vendor_raw_material', methods=['GET', 'POST'])
def raw_material():
    if request.method == 'POST':
        items = []

        # Load current data from the JSON file
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                current_data = json.load(file)
        else:
            current_data = []

        # Get vendor name (username) from session
        vendor_name = session.get('username', 'Unknown Vendor')  # Use username as vendor name

        for item_id in range(1, 100):  # Assuming a max of 100 items
            composition_ids = request.form.getlist(f'composition_id_{item_id}[]')
            if composition_ids:
                compositions = []

                composition_names = request.form.getlist(f'composition_{item_id}[]')
                composition_types = request.form.getlist(f'composition_type_{item_id}[]')
                amounts = request.form.getlist(f'amount_{item_id}[]')
                units = request.form.getlist(f'unit_{item_id}[]')

                for i in range(len(composition_ids)):
                    composition = {
                        'composition_id': composition_ids[i],
                        'composition_name': composition_names[i],
                        'composition_type': composition_types[i],
                        'amount': int(amounts[i]) if amounts[i].isdigit() else 0,
                        'unit': units[i],
                        'vendor_name': vendor_name  # Vendor name comes from session
                    }

                    current_data, is_new_entry = process_composition(composition, vendor_name, current_data)

                    if is_new_entry:
                        flash(f"New entry created for composition ID: {composition['composition_id']} due to field changes.", "info")

        # Save updated data back to JSON file
        with open(DATA_FILE, 'w') as file:
            json.dump(current_data, file, indent=4)

        flash("Raw material data saved successfully!", "success")
        return redirect(url_for('vendor_dashboard_bp.vendor_dashboard'))

    # Retrieve vendor name from session
    vendor_name = session.get('username', 'Unknown Vendor')
    return render_template('vendor_raw_material_check.html', vendor_name=vendor_name)
