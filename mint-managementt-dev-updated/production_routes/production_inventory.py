import json
import os
from flask import jsonify, Blueprint, render_template, request

PRODUCTION_FILE = 'transfer_production.json'

production_inventory_bp = Blueprint('production_inventory_bp', __name__)


@production_inventory_bp.route('/production_inventory', methods=['GET'])
def production_inventory():
    try:
        # Load transferred compositions from the JSON file
        transferred_compositions = []
        if os.path.exists(PRODUCTION_FILE):
            with open(PRODUCTION_FILE, 'r') as file:
                data = json.load(file)
                # Extract the composition data and datetime from the nested structure
                transferred_compositions = [
                    {
                        "composition_id": item["composition"]["composition_id"],
                        "composition_name": item["composition"]["composition_name"],
                        "composition_type": item["composition"]["composition_type"],
                        "amount": item["composition"]["amount"],
                        "unit": item["composition"]["unit"],
                        "transfer_datetime": item["transfer_datetime"]
                    }
                    for item in data
                ]

        # Check if this is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # print("Sending JSON response:",
            #       transferred_compositions)  # Debug print
            return jsonify({
                'success': True,
                'transferred_compositions': transferred_compositions
            })

        # If not AJAX, render the template
        return render_template('production_inventory.html',
                               transferred_compositions=transferred_compositions)

    except Exception as e:
        # print(f"Error in production_inventory: {str(e)}")  # Debug print
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
        return render_template('production_inventory.html',
                               transferred_compositions=[],
                               error=str(e))
