import json
from flask import Blueprint,render_template

# create a blueprint for the dashboard route
check_quotation_bp= Blueprint('check_quotation_bp',__name__)

@check_quotation_bp.route('/check_quotation', methods=['GET'])
def check_quotation():
    # Load the data from final.json
    final_data = []
    try:
        with open('quotation_order.json', 'r') as f:
            final_data = json.load(f)
    except FileNotFoundError:
        pass

    # Pass final_data to the HTML template
    return render_template('check_quotation.html', quotations=final_data)
