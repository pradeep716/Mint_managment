from datetime import datetime
from io import BytesIO
from flask import Flask, redirect, render_template, request, Blueprint, send_file, session, url_for
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle

# CUSTOMER_DATA_FILE = 'customers.json'

# Create a Blueprint for the home route
generateBill_bp = Blueprint('generateBill_bp', __name__)

app = Flask(__name__)

def read_customer_data():
    try:
        with open('customers.json', 'r') as file:
            data = json.load(file)
            # print("Customer Data Loaded:", data)  # Debugging output
            return data
    except FileNotFoundError:
        return {}

def read_orders_data():
    try:
        with open('orders.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file doesn't exist

@generateBill_bp.route('/generate-bill', methods=['GET', 'POST'])
def generate_bill():
    if 'username' not in session:
        return redirect(url_for('login_bp.login'))

    customers = read_customer_data()
    orders = read_orders_data()
    filtered_orders = []
    selected_customer = None
    total_payable_amount = 0
    invoice_numbers = set()
    selected_invoice_number = None

    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Initialize variables safely
    start_date = None
    end_date = None
    customer_name = None  # Explicit initialization to ensure no UnboundLocalError

    if request.method == 'POST':
        # Get form data with safe defaults
        customer_name = request.form.get('customer_name', None)
        start_date_str = request.form.get('start_date', None)
        end_date_str = request.form.get('end_date', None)
        selected_invoice_number = request.form.get('invoice_number', None)

        try:
            # Parse dates only if provided
            if start_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."

    # Process the orders based on form filters
    for order_id, order in orders.items():
        invoice_numbers.add(order.get('invoice_number', 'N/A'))

        try:
            order_date = datetime.strptime(order['order_date'], '%Y-%m-%d')
        except ValueError:
            continue

        # Apply logic filters safely
        if (
            (not customer_name or order.get('customer_name') == customer_name) and
            (not start_date or (order_date.date() >= start_date if start_date else True)) and
            (not end_date or (order_date.date() <= end_date if end_date else True))
        ):
            if selected_invoice_number and order.get('invoice_number') != selected_invoice_number:
                continue

            total_pair = order.get('stock', 0)
            total_amount_inr = total_pair * 100  # Example calculation
            total_payable_amount += total_amount_inr

            filtered_orders.append({
                "product_class": order.get('product_class', 'N/A'),
                "product_id": order.get('product_id', 'N/A'),
                "stock": order.get('stock', 0),
                "price_per_pair": 100,  # Example price
                "total_amount_inr": total_amount_inr,
                "order_date": order_date.strftime('%Y-%m-%d'),
                "invoice_number": order.get('invoice_number', 'N/A')
            })

    return render_template('generate_bill.html',
                           customers=customers,
                           orders=filtered_orders,
                           total_payable_amount=total_payable_amount,
                           selected_customer=selected_customer,
                           selected_invoice_number=selected_invoice_number,
                           current_date=current_date,
                           invoice_numbers=sorted(invoice_numbers),
                           customer_name=customer_name)  # Pass to template safely
