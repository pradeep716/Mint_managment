import json
from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, json

app = Flask(__name__)
app.secret_key = "your_secret_key"

PLACE_FILE = 'place_order.json'

# create a blueprint for the dashboard route
quotation_vendor_bp= Blueprint('quotation_vendor_bp',__name__)

# Helper function to load orders from place_order.json
def load_place_orders():
    try:
        with open(PLACE_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
@quotation_vendor_bp.route('/quotation_vendor', methods=['GET', 'POST'])
def quotation_vendor():
    orders = load_place_orders()  # Load existing orders

    
        # Gather data from the form
        # Get vendor name from session
    vendor_name = session.get('username', 'Unknown Vendor')  # Default to 'Unknown Vendor' if not logged in

    if request.method == 'POST':
        # Gather data from the form
        vendor_name = request.form.get('vendorName')
        # ... handle other form fields ...
        quotation_id = request.form.get('quotationId')
        contact_info = request.form.get('contactInfo')  # New field
        selected_order_id = request.form.get('orderId')

        # Collect composition details
        composition_ids = request.form.getlist('compositionId[]')
        composition_names = request.form.getlist('compositionName[]')
        material_types = request.form.getlist('materialType[]')
        amounts = request.form.getlist('amount[]')
        units = request.form.getlist('unit[]')
        price_quotations = request.form.getlist('priceQuotation[]')
        accept_quotations = request.form.getlist('acceptQuotation[]')
        total_amount = request.form.get('totalAmount')

        # Initialize quotation data structure with contactInfo
        quotation_data = {
            'vendorName': vendor_name,
            'quotationId': quotation_id,
            'contactInfo': contact_info,  # Store contact details
            'orderId': selected_order_id,
            'totalAmount': total_amount,
            'compositions': []
        }

        # Determine the minimum length to avoid index errors
        min_length = min(
            len(composition_ids),
            len(composition_names),
            len(material_types),
            len(amounts),
            len(units),
            len(price_quotations),
            len(accept_quotations)
        )

        # Loop through each composition and include only the entries with complete data
        for i in range(min_length):
            composition = {
                'compositionId': composition_ids[i],
                'compositionName': composition_names[i],
                'materialType': material_types[i],
                'amount': int(amounts[i]) if amounts[i].isdigit() else 0,
                'unit': units[i],
                'priceQuotation': price_quotations[i],
                'accepted': accept_quotations[i] == 'accept'
            }
            quotation_data['compositions'].append(composition)

        # Save to `quotation_order.json` without overwriting existing data
        final_data = []
        try:
            with open('quotation_order.json', 'r') as f:
                final_data = json.load(f)
        except FileNotFoundError:
            pass

        final_data.append(quotation_data)
        with open('quotation_order.json', 'w') as f:
            json.dump(final_data, f, indent=4)

        return redirect(url_for('quotation_vendor_bp.quotation_vendor'))

    return render_template('quotation_vendor.html', orders=orders, vendor_name=vendor_name)

