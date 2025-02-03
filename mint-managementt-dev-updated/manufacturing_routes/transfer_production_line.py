import json
import os
from datetime import datetime
from flask import Blueprint, jsonify, render_template, request

DATA_FILE = 'composition_data.json'
TRANFER_FILE = 'transfer_production.json'

transfer_production_line_bp = Blueprint(
    'transfer_production_line_bp', __name__)


@transfer_production_line_bp.route('/transfer_production_line', methods=['GET', 'POST'])
def transfer_production_line():
    if request.method == 'POST':
        try:
            data = request.get_json()
            composition_id = data.get('composition_id')
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Load composition data
            with open(DATA_FILE, 'r') as file:
                composition_data = json.load(file)

            # Initialize transfer file if it doesn't exist
            if os.path.exists(TRANFER_FILE):
                with open(TRANFER_FILE, 'r') as file:
                    transfer_data = json.load(file)
            else:
                transfer_data = []

            # Search for the composition and transfer it
            found = False
            for outer_list in composition_data:  # First level of nesting
                for section in outer_list:  # Second level of nesting
                    if isinstance(section, dict) and 'compositions' in section:
                        compositions = section['compositions']
                        # Create a copy to iterate
                        for composition in compositions[:]:
                            if composition['composition_id'] == composition_id:
                                transfer_record = {
                                    "composition": composition,
                                    "transfer_datetime": current_datetime
                                }
                                transfer_data.append(transfer_record)
                                compositions.remove(composition)
                                found = True
                                break
                        if found:
                            break
                if found:
                    break

            if not found:
                return jsonify({'success': False, 'message': 'Composition not found'}), 404

            # Save updated composition data
            with open(DATA_FILE, 'w') as file:
                json.dump(composition_data, file, indent=4)

            # Save updated transfer data
            with open(TRANFER_FILE, 'w') as file:
                json.dump(transfer_data, file, indent=4)

            return jsonify({
                'success': True,
                'message': f'Composition transferred successfully at {current_datetime}'
            })

        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    # Handle GET request
    try:
        # Load composition data
        with open(DATA_FILE, 'r') as file:
            composition_data = json.load(file)

        # Prepare orders for rendering
        orders = []
        for outer_list in composition_data:  # First level of nesting
            for section in outer_list:  # Second level of nesting
                if isinstance(section, dict) and 'compositions' in section:
                    if section['compositions']:  # Only add if there are compositions
                        orders.append(
                            {"compositions": section['compositions']})

        return render_template('transfer_production_line.html', orders=orders)

    except Exception as e:
        print(f"Error loading composition data: {str(e)}")  # Debug log
        return jsonify({'success': False, 'message': str(e)}), 500
