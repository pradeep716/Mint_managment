import json
from flask import Blueprint, jsonify, request

# Create a blueprint for the dashboard route
get_composition_data_bp = Blueprint('get_composition_data_bp', __name__)

@get_composition_data_bp.route('/get_composition_data', methods=['GET'])
def get_composition_data():
    composition_id = request.args.get('composition_id')

    # Handle missing composition_id in the query
    if not composition_id:
        return jsonify({
            'success': False,
            'message': 'Composition ID is missing in the request'
        }), 400

    try:
        # Attempt to open and read the JSON file
        with open('composition_data.json', 'r') as file:
            data = json.load(file)

        # Search for the composition in the JSON structure
        for outer_list in data:
            if isinstance(outer_list, list):
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

        # If no matching composition ID is found
        return jsonify({
            'success': False,
            'message': f'Composition with ID {composition_id} not found'
        }), 404

    except FileNotFoundError:
        # Handle case when the file doesn't exist
        return jsonify({
            'success': False,
            'message': 'Composition data file is missing'
        }), 500
    except json.JSONDecodeError:
        # Handle JSON parsing errors
        return jsonify({
            'success': False,
            'message': 'Error parsing composition data file'
        }), 500
    except Exception as e:
        # Catch-all for unexpected errors
        return jsonify({
            'success': False,
            'message': f'An unexpected error occurred: {str(e)}'
        }), 500
