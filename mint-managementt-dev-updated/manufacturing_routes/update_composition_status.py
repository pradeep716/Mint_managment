import json
from flask import Blueprint, jsonify, request 

# create a blueprint for the dashboard route
update_composition_status_bp= Blueprint('update_composition_status_bp',__name__)

@update_composition_status_bp.route('/update_composition_status', methods=['POST'])
def update_composition_status():
    data = request.get_json()
    quotation_id = data['quotationId']
    composition_index = data['compositionIndex']
    accepted = data['accepted']

    # Load existing data from the JSON file
    try:
        with open('quotation_order.json', 'r') as f:
            quotations = json.load(f)
    except FileNotFoundError:
        return jsonify({"success": False, "message": "Data not found"}), 404

    # Find the correct quotation by ID
    for quotation in quotations:
        if quotation['quotationId'] == quotation_id:
            try:
                # Update the specific composition's status
                quotation['compositions'][composition_index]['accepted'] = accepted
                break
            except IndexError:
                return jsonify({"success": False, "message": "Composition not found"}), 404
    else:
        return jsonify({"success": False, "message": "Quotation not found"}), 404

    # Save the updated data back to the JSON file
    with open('quotation_order.json', 'w') as f:
        json.dump(quotations, f, indent=4)

    return jsonify({"success": True})

