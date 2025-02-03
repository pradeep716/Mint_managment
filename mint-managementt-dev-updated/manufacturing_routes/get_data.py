import json
import os

from flask import Blueprint, jsonify


DATA_FILE = 'composition_data.json'

# create a blueprint for the dashboard route
get_data_bp = Blueprint('get_data_bp',__name__)

@get_data_bp.route('/get-data')
def get_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            return jsonify(data)
    else:
        return jsonify([])
