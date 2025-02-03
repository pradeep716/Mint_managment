# import json
# import os
# from flask import Blueprint, flash, redirect, render_template, request, url_for

# PRODUCTION_COMPOSITION_FILE = 'production_composition_consume.json'
# DATA_FILE = 'transfer_production.json'


# # create a blueprint for the dashboard route
# return_material_bp = Blueprint('return_material_bp', __name__)


# # Function to save data to a JSON file


# def save_data(data, filename):
#     if not os.path.exists(filename):
#         with open(filename, 'w') as file:
#             json.dump([], file)  # Create an empty list in the file

#     with open(filename, 'r') as file:
#         current_data = json.load(file)

#     # Ensure current_data is a list
#     if not isinstance(current_data, list):
#         current_data = []

#     current_data.append(data)  # Append the new data

#     with open(filename, 'w') as file:
#         json.dump(current_data, file, indent=4)


# # def load_data(filename):
# #     if not os.path.exists(filename):
# #         return []  # Return an empty list if the file doesn't exist

# #     with open(filename, 'r') as file:
# #         return json.load(file)


# @return_material_bp.route('/return_material', methods=['GET', 'POST'])
# def return_material():
#     if request.method == 'POST':
#         items = []
#         # Loop through the form data to extract item and composition information
#         for item_id in range(1, 100):  # Assuming a max of 100 items
#             composition_ids = request.form.getlist(
#                 f'composition_id_{item_id}[]')
#             if composition_ids:
#                 compositions = []

#                 # Get all compositions for this item
#                 composition_names = request.form.getlist(
#                     f'composition_{item_id}[]')
#                 composition_types = request.form.getlist(
#                     f'composition_type_{item_id}[]')
#                 amounts = request.form.getlist(f'amount_{item_id}[]')
#                 units = request.form.getlist(f'unit_{item_id}[]')

#                 for i in range(len(composition_ids)):
#                     composition = {
#                         'composition_id': composition_ids[i],
#                         'composition_name': composition_names[i],
#                         'composition_type': composition_types[i],
#                         'amount': int(amounts[i]) if amounts[i].isdigit() else 0,
#                         'unit': units[i]
#                     }
#                     compositions.append(composition)

#                 # Add the compositions (no need for item_name now)
#                 items.append({'compositions': compositions})

#         # Save the data to a JSON file
#         save_data(items, DATA_FILE)

#         flash("Raw material data saved successfully!", "success")
#         # Redirect to a valid route after saving data
#         return redirect(url_for('production_dashboard_bp.production_dashboard'))

#     # Adjust to your template name
#     return render_template('return_material.html')


import json
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

PRODUCTION_COMPOSITION_FILE = 'production_composition_consume.json'
TRANSFER_PRODUCTION_FILE = 'transfer_production.json'

# create a blueprint for the dashboard route
return_material_bp = Blueprint('return_material_bp', __name__)

# Function to save data to a JSON file


def save_data(data, filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            json.dump([], file)  # Create an empty list in the file

    with open(filename, 'r') as file:
        current_data = json.load(file)

    # Ensure current_data is a list
    if not isinstance(current_data, list):
        current_data = []

    current_data.append(data)  # Append the new data
    with open(filename, 'w') as file:
        json.dump(current_data, file, indent=4)

# Function to load data from a JSON file


def load_data(filename):
    if not os.path.exists(filename):
        return []  # Return an empty list if the file doesn't exist

    with open(filename, 'r') as file:
        return json.load(file)

# Function to deduct composition from production inventory


def add_to_production_inventory(compositions_list):
    # Load the existing production inventory
    inventory = load_data(TRANSFER_PRODUCTION_FILE)
    # print("Loaded Inventory:", inventory)  # Debugging log

    # Create a dictionary for faster lookup of inventory items by composition ID
    inventory_dict = {
        item['composition']['composition_id']: item['composition']
        for item in inventory
        if 'composition' in item and 'composition_id' in item['composition']
    }
    # print("Inventory Dictionary:", inventory_dict)  # Debugging log

    for composition in compositions_list:
        print("Processing Composition:", composition)  # Debugging log
        comp_id = composition['composition_id']
        amount_to_add = composition['amount']

        # Check if the composition exists in the inventory
        if comp_id in inventory_dict:
            current_amount = inventory_dict[comp_id].get('amount', 0)
            new_amount = current_amount + amount_to_add

            # Update the amount in the inventory, ensuring it doesn't go negative
            inventory_dict[comp_id]['amount'] = max(new_amount, 0)

    # Update the original inventory with modified composition data
    for item in inventory:
        if 'composition' in item:
            comp_id = item['composition'].get('composition_id')
            if comp_id in inventory_dict:
                item['composition']['amount'] = inventory_dict[comp_id]['amount']

    # Save the updated inventory back to the file
    with open(TRANSFER_PRODUCTION_FILE, 'w') as file:
        json.dump(inventory, file, indent=4)

# Route for composition_consume_inventory Line


@return_material_bp.route('/return_material', methods=['GET', 'POST'])
def return_material():
    if request.method == 'POST':
        compositions_list = []

        # Iterate through posted form data
        for item_id in range(1, 100):  # Assuming a maximum of 100 items
            # Check if compositions for the current item exist
            composition_ids = request.form.getlist(
                f'composition_id_{item_id}[]')
            composition_names = request.form.getlist(
                f'composition_{item_id}[]')
            composition_types = request.form.getlist(
                f'composition_type_{item_id}[]')
            amounts = request.form.getlist(f'amount_{item_id}[]')
            units = request.form.getlist(f'unit_{item_id}[]')

            # Build compositions data for this item
            for i in range(len(composition_ids)):
                composition = {
                    'composition_id': composition_ids[i],
                    'composition_name': composition_names[i],
                    'composition_type': composition_types[i],
                    'amount': int(amounts[i]) if amounts[i].isdigit() else 0,
                    'unit': units[i]
                }
                compositions_list.append(composition)

        # Deduct from production inventory
        add_to_production_inventory(compositions_list)

        # Save only the compositions data to a JSON file
        # save_data(compositions_list, PRODUCTION_COMPOSITION_FILE)

        flash("Consumed composition saved successfully!", "success")
        return redirect(url_for('production_dashboard_bp.production_dashboard'))

    # Render the template for GET requests
    return render_template('return_material.html')
