import json
from flask import Blueprint, jsonify, request

# Create a blueprint for the dashboard route
vendor_get_composition_data_bp = Blueprint('vendor_get_composition_data_bp', __name__)

@vendor_get_composition_data_bp.route('/vendor_get_composition_data', methods=['GET'])
def get_composition_data():
    composition_id = request.args.get('composition_id')

    if not composition_id:
        return jsonify({'success': False, 'message': 'Composition ID is missing'}), 400

    try:
        # Load JSON data
        with open('vendor_composition_data.json', 'r') as file:
            data = json.load(file)

        # Search for the composition ID
        for outer_list in data:
            for section in outer_list:
                if isinstance(section, dict) and 'compositions' in section:
                    for composition in section['compositions']:
                        if composition.get('composition_id') == composition_id:
                            return jsonify({
                                'success': True,
                                'composition_name': composition.get('composition_name', ''),
                                'composition_type': composition.get('composition_type', ''),
                                'amount': composition.get('amount', ''),
                                'unit': composition.get('unit', 'kg')
                            })

        # If no matching ID is found
        return jsonify({'success': False, 'message': f'Composition ID {composition_id} not found'}), 404

    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({'success': False, 'message': 'Error loading composition data'}), 500
