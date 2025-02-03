import json
from flask import Blueprint, jsonify, request

# create a blueprint for the dashboard route
production_get_composition_data_bp = Blueprint(
    'production_get_composition_data_bp', __name__)


@production_get_composition_data_bp.route('/get_composition_data_production', methods=['GET'])
def get_composition_data():
    composition_id = request.args.get('composition_id')
    if not composition_id:
        return jsonify({'success': False, 'message': 'Composition ID is missing'}), 400

    try:
        # Load data from JSON file
        with open('transfer_production.json', 'r') as file:
            data = json.load(file)

        # Search for the composition in the nested structure
        for item in data:  # Iterate over the outermost list
            # Extract the 'composition' dictionary
            composition = item.get('composition')
            if composition and composition.get('composition_id') == composition_id:
                # Match found, return the data
                return jsonify({
                    'success': True,
                    'composition_name': composition.get('composition_name', ''),
                    'composition_type': composition.get('composition_type', ''),
                    'amount': composition.get('amount', ''),
                    'unit': composition.get('unit', 'kg')
                })

        # No match found
        return jsonify({'success': False, 'message': 'Composition not found'}), 404

    except FileNotFoundError:
        return jsonify({'success': False, 'message': 'Data file not found'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
