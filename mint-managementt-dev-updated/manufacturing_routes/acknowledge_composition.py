import json

from flask import Blueprint, jsonify, render_template, request

DATA_FILE = 'composition_data.json'
SUPPLY_DATA_FILE = 'supply_data.json'

# create a blueprint for the dashboard route
acknowledge_composition_bp= Blueprint('acknowledge_composition_bp',__name__)

# Function to get shipment data based on shipment_id


def get_shipment_data(shipment_id):
    try:
        # Load the supply data from the JSON file
        with open(SUPPLY_DATA_FILE, 'r') as file:
            supply_data = json.load(file)

        # Find the shipment based on the shipment_id
        shipment = next(
            (item for item in supply_data if item["shipment_id"] == shipment_id), None)

        # If shipment is found, return it; otherwise, return an error message
        if shipment:
            return shipment
        else:
            return {"error": "Shipment ID not found"}
    except FileNotFoundError:
        return {"error": "Supply data file not found"}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON data"}

@acknowledge_composition_bp.route('/acknowledge_composition', methods=['POST'])
def acknowledge_composition():
    import json
    from pathlib import Path

    data = request.get_json()
    composition_id = data.get('compositionId')
    shipment_id = data.get('shipmentId')

    if not composition_id or not shipment_id:
        return jsonify({"success": False, "message": "Invalid data provided"}), 400

    # Load existing data from composition_data.json
    composition_file = Path('composition_data.json')
    if composition_file.exists():
        with open(DATA_FILE, 'r') as file:
            compositions = json.load(file)
    else:
        compositions = []

    # Normalize the data structure (flatten nested lists if needed)
    normalized_compositions = []
    for item in compositions:
        if isinstance(item, list):  # If it's a nested list, extend the normalized list
            normalized_compositions.extend(item)
        else:  # If it's already a dictionary, add it directly
            normalized_compositions.append(item)

    # Retrieve shipment and composition details
    shipment_data = get_shipment_data(shipment_id)
    composition = next(
        (c for c in shipment_data['compositions'] if c['compositionId'] == composition_id), None)

    if not composition:
        return jsonify({"success": False, "message": "Composition not found"}), 404

    # Format the composition data
    formatted_composition = {
        "composition_id": composition['compositionId'],
        "composition_name": composition['compositionName'],
        "composition_type": composition['materialType'],
        "amount": composition['amount'],
        "unit": composition['unit'],
    }

    # Check if the composition already exists
    found = False
    for entry in normalized_compositions:
        for existing in entry.get('compositions', []):
            if existing['composition_id'] == formatted_composition['composition_id'] and \
               existing['composition_type'] == formatted_composition['composition_type']:
                # Update the existing composition
                existing.update(formatted_composition)
                found = True
                break
        if found:
            break

    if not found:
        # Append new composition entry
        normalized_compositions.append(
            {"compositions": [formatted_composition]})

    # Save updated data to composition_data.json
    with open(DATA_FILE, 'w') as file:
        json.dump(normalized_compositions, file, indent=4)

    return jsonify({"success": True, "message": "Acknowledged successfully"})
