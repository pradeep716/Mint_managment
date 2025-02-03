import json
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for 

QUOTATION_FILE = 'quotation_order.json'

def load_quotation_orders():
    try:
        with open(QUOTATION_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save supply data to a JSON file
def save_supply_data(supply_data, filename='supply_data.json'):
    try:
        # Open the existing file and load the current data
        with open(filename, 'r') as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty, start with an empty list
        existing_data = []

    # Append the new supply data to the existing data
    existing_data.append(supply_data)

    # Write the updated data back to the file
    with open(filename, 'w') as file:
        json.dump(existing_data, file, indent=4)


# create a blueprint for the dashboard route
supply_composition_material_id_bp= Blueprint('supply_composition_material_id_bp',__name__)

@supply_composition_material_id_bp.route('/supply_composition_material/<quotation_id>', methods=['GET', 'POST'])
def supply_composition_material(quotation_id=None):
    orders = load_quotation_orders()  # Load all quotation orders
    quotation_data = None

    # If quotation_id is passed as a URL parameter, load the relevant data
    if quotation_id:
        # Find the quotation with the given ID
        quotation_data = next(
            (order for order in orders if order["quotationId"] == quotation_id), None)
        if not quotation_data:
            flash("Quotation not found. Please select a valid quotation ID.", "error")
            return redirect(url_for('supply_composition_material_id_bp.supply_composition_material', quotation_id=quotation_id))


    # Handle POST request after form submission
    if request.method == 'POST':
        # Debug print the form data
        print("Form data:", request.form)

        # Get the selected quotation_id from the form
        quotation_id = request.form.get('quotation_id')

        # Find the quotation with the given ID
        quotation_data = next(
            (order for order in orders if order["quotationId"] == quotation_id), None)
        if not quotation_data:
            flash("No valid quotation loaded. Please load a quotation first.", "error")
            return redirect(url_for('supply_composition_material_id_bp.supply_composition_material', quotation_id=quotation_id))


        # Gather all submitted data from the form
        shipment_id = request.form.get('shipment_id')
        carrier = request.form.get('carrier')
        delivery_date = request.form.get('delivery_date')

        # Dispatch statuses are stored in a dictionary where keys are compositionId
        # Get the full form data as a dictionary
        dispatch_status = request.form.to_dict(flat=False)

        # Update dispatch statuses for compositions based on compositionId
        if "compositions" in quotation_data:
            for composition in quotation_data["compositions"]:
                composition_id = composition["compositionId"]
                # Construct the key for dispatch_status using compositionId (e.g., 'dispatch_status[1]')
                dispatch_key = f'dispatch_status[{composition_id}]'

                # Get the status from the form data using the generated key
                status = dispatch_status.get(dispatch_key, [None])[
                    0]  # Default to None if not found
                print(
                    f"Dispatch status for composition {composition_id}: {status}")

                if status:
                    composition["dispatchStatus"] = status
                else:
                    # Default to "pending" if no status is found
                    composition["dispatchStatus"] = "pending"

        # Save all the updated data to the supply_data.json file
        supply_data = {
            "quotation_id": quotation_data["quotationId"],
            "shipment_id": shipment_id,
            "carrier": carrier,
            "delivery_date": delivery_date,
            "compositions": quotation_data["compositions"]
        }

        # Function to save the updated data to a JSON file
        save_supply_data(supply_data)

        flash("Supply data submitted successfully!", "success")
        return redirect(url_for('supply_composition_material_bp.supply_composition_material'))

    return render_template('supply_composition_material.html', orders=orders, data=quotation_data)
