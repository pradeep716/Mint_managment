import json
from flask import Blueprint,  render_template

# create a blueprint for the dashboard route
mint_inventory_nav_bp = Blueprint('mint_inventory_nav_bp', __name__)


@mint_inventory_nav_bp.route('/mint_inventory_nav', methods=['GET', 'POST'])
def mint_inventory_nav():
    return render_template('enterprise_dashboard.html')
