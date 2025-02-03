import json
from flask import Flask, Blueprint, flash, jsonify, redirect, render_template, request, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"

QUOTATION_FILE = 'quotation_order.json'
SUPPLY_FILE = 'supply_data.json'


def load_quotation_orders():
    try:
        with open(QUOTATION_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_quotation_orders(orders):
    with open(QUOTATION_FILE, 'w') as file:
        json.dump(orders, file, indent=4)


def save_supply_data(supply_data):
    try:
        with open(SUPPLY_FILE, 'r') as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(supply_data)

    with open(SUPPLY_FILE, 'w') as file:
        json.dump(existing_data, file, indent=4)


supply_composition_material_bp = Blueprint(
    'supply_composition_material_bp', __name__
)


@supply_composition_material_bp.route('/update_dispatch', methods=['POST'])
def update_dispatch():
    """
    Route to handle dispatch status updates.
    Saves dispatch updates independently in supply_data.json.
    """
    try:
        # Extract data from the request
        data = request.json
        composition_id = data.get('compositionId')
        dispatch_status = data.get('dispatchStatus')

        # Load existing supply data
        try:
            with open(SUPPLY_FILE, 'r') as file:
                supply_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            supply_data = []

        orders = load_quotation_orders()

        # Find and update the specific composition's dispatch status
        for order in orders:
            for composition in order.get("compositions", []):
                if composition["compositionId"] == composition_id:
                    composition["dispatchStatus"] = dispatch_status
                    save_quotation_orders(orders)
        # Check if the composition already exists in supply_data.json
        updated = False
        for record in supply_data:
            for composition in record.get("compositions", []):
                if composition["compositionId"] == composition_id:
                    composition["dispatchStatus"] = dispatch_status
                    updated = True

        # If composition not found, return error
        if not updated:
            return jsonify({"success": False, "message": "Composition not found in supply data!"}), 404

        # Save updated supply data back to file
        with open(SUPPLY_FILE, 'w') as file:
            json.dump(supply_data, file, indent=4)

        return jsonify({"success": True, "message": "Dispatch status updated successfully in supply data!"})

    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500


@supply_composition_material_bp.route('/supply_composition_material', methods=['GET', 'POST'])
@supply_composition_material_bp.route('/supply_composition_material/<quotation_id>', methods=['GET', 'POST'])
def supply_composition_material(quotation_id=None):
    # Load the orders and get the current vendor's name from the session
    orders = load_quotation_orders()
    # Get the logged-in vendor's username
    vendor_name = session.get('username', None)

    if not vendor_name:
        flash("You need to log in first.", "error")
        return redirect(url_for('vendor_login_bp.vendor_login'))

    # Filter orders to show only those belonging to the logged-in vendor
    orders = [order for order in orders if order.get(
        "vendorName") == vendor_name]

    # If no orders exist for the vendor, show an appropriate message
    if not orders:
        flash("No orders found for the logged-in vendor.", "warning")
        # or any other relevant page
        return redirect(url_for('vendor_dashboard_bp.vendor_dashboard'))

    quotation_data = None
    if quotation_id:
        quotation_data = next(
            (order for order in orders if order["quotationId"] == quotation_id), None)
        if not quotation_data:
            flash("Quotation not found. Please select a valid quotation ID.", "error")
            return redirect(url_for('supply_composition_material_bp.supply_composition_material'))

    if request.method == 'POST':

        quotation_id = request.form.get('quotation_id')
        shipment_id = request.form.get('shipment_id')
        carrier = request.form.get('carrier')
        delivery_date = request.form.get('delivery_date')

        dispatch_status = request.form.to_dict(flat=False)
        quotation_data = next(
            (order for order in orders if order["quotationId"] == quotation_id), None)
        if not quotation_data:
            flash("No valid quotation loaded. Please load a quotation first.", "error")
            return redirect(url_for('supply_composition_material_bp.supply_composition_material'))

        if "compositions" in quotation_data:
            for composition in quotation_data["compositions"]:
                composition_id = composition["compositionId"]
                dispatch_key = f'dispatch_status[{composition_id}]'
                status = dispatch_status.get(dispatch_key, [None])[0]
                composition["dispatchStatus"] = status if status else "pending"

        supply_data = {
            "quotation_id": quotation_data["quotationId"],
            "order_id": quotation_data.get("orderId"),
            "shipment_id": shipment_id,
            "carrier": carrier,
            "vendor_name": vendor_name,  # Store vendor name for tracking
            "delivery_date": delivery_date,
            "compositions": quotation_data["compositions"]
        }

        save_supply_data(supply_data)
        flash("Supply data submitted successfully!", "success")
        return redirect(
            url_for('supply_composition_material_bp.supply_composition_material',
                    quotation_id=quotation_id)
        )

    return render_template('supply_composition_material.html', orders=orders, data=quotation_data)
