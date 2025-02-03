import json
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

PLACE_FILE = 'place_order.json'

# create a blueprint for the dashboard route
place_order_form_bp = Blueprint('place_order_form_bp', __name__)

# Helper function to load orders from place_order.json


def load_place_orders():
    try:
        with open(PLACE_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Helper function to save orders to place_order.json


def save_place_orders(orders):
    with open(PLACE_FILE, 'w') as file:
        json.dump(orders, file, indent=4)


@place_order_form_bp.route('/place_order_form', methods=['GET', 'POST'])
def place_order_form():
    if 'username' in session:
        if request.method == 'POST':
            # print(request.form)

            # Collect all form data (no getlist needed for single input fields)
            # orderId = request.form['orderId']
            customerName = request.form['customerName']
            customerEmail = request.form['customerEmail']
            orderDate = request.form['orderDate']
            deliveryDate = request.form['deliveryDate']
            deliveryAddress = request.form['deliveryAddress']
            # paymentMethod = request.form['paymentMethod']
            rawMaterialRequirements = request.form['rawMaterialRequirements']
            notes = request.form['notes']

            # Collect all composition details
            compositionIds = request.form.getlist('compositionId[]')
            compositionNames = request.form.getlist('compositionName[]')
            materialTypes = request.form.getlist('materialType[]')
            amounts = request.form.getlist('amount[]')
            units = request.form.getlist('unit[]')

            # Validate required fields
            # if not orderId or not customerName or not customerEmail or not orderDate or not compositionIds:
            #     flash("Error: Please fill in all required fields.", "danger")
            #     return redirect(url_for('place_order'))

            # Prepare order details for saving (multiple composition entries)
            compositions = []
            for i in range(len(compositionIds)):
                composition = {
                    'compositionId': compositionIds[i],
                    'compositionName': compositionNames[i],
                    'materialType': materialTypes[i],
                    'amount': int(amounts[i]) if amounts[i].isdigit() else 0,
                    'unit': units[i]
                }
                compositions.append(composition)

            place_order_details = {
                # 'orderId': orderId,
                'customerName': customerName,
                'customerEmail': customerEmail,
                'orderDate': orderDate,
                'composition': compositions,  # Multiple compositions
                'deliveryDate': deliveryDate,
                'deliveryAddress': deliveryAddress,
                # 'paymentMethod': paymentMethod,
                'rawMaterialRequirements': rawMaterialRequirements,
                'notes': notes
            }

            # Load existing orders, append the new order, and save it
            orders = load_place_orders()  # Load existing orders
            orders.append(place_order_details)  # Append new order
            save_place_orders(orders)  # Save orders

            flash("Order received and saved!", "success")
            return redirect(url_for('manufacturing_dashboard_bp.manufacturing_dashboard'))

        return render_template('place_order.html')
    else:
        flash('Please login to access this page.', 'warning')
        return redirect(url_for('login'))
