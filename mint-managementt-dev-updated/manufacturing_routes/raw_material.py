import json
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash

DATA_FILE = 'composition_data.json'

# Create a blueprint for the dashboard route
raw_material_bp = Blueprint('raw_material_bp', __name__)

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

# Function to check and update compositions
def process_composition(composition, current_data):
    for entry in current_data:
        for item in entry:
            for existing_composition in item['compositions']:
                if existing_composition['composition_id'] == composition['composition_id']:
                    if (existing_composition['composition_name'] == composition['composition_name'] and
                        existing_composition['composition_type'] == composition['composition_type'] and
                        existing_composition['unit'] == composition['unit']):
                        # Append amount if all other fields match
                        existing_composition['amount'] += composition['amount']
                        return current_data, False
                    else:
                        # Fields other than amount differ; add as a new entry
                        break
    # If no match or fields differ, add the composition as a new entry
    new_entry = {'compositions': [composition]}
    current_data.append([new_entry])
    return current_data, True

@raw_material_bp.route('/raw_material', methods=['GET', 'POST'])
def raw_material():
    if request.method == 'POST':
        items = []

        # Load current data from the JSON file
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                current_data = json.load(file)
        else:
            current_data = []

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
                        'unit': units[i]
                    }

                    current_data, is_new_entry = process_composition(composition, current_data)

                    if is_new_entry:
                        flash(f"New entry created for composition ID: {composition['composition_id']} due to field changes.", "info")

        # Save updated data back to JSON file
        with open(DATA_FILE, 'w') as file:
            json.dump(current_data, file, indent=4)

        flash("Raw material data saved successfully!", "success")
        return redirect(url_for('manufacturing_dashboard_bp.manufacturing_dashboard'))

    return render_template('raw_material_check.html')
