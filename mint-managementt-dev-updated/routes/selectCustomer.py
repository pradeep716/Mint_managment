from flask import Flask, render_template, redirect, request, url_for, session , Blueprint
import json

CUSTOMER_DATA_FILE = 'customers.json'

# Create a Blueprint for the home route
selectCustomer_bp = Blueprint('selectCustomer_bp', __name__)

app = Flask(__name__)

def read_customer_data():
    try:
        with open(CUSTOMER_DATA_FILE, 'r') as file:
            data = json.load(file)
            print("Customer Data Loaded:", data)  # Debugging output
            return data
    except FileNotFoundError:
        return {}
    
@selectCustomer_bp.route('/select-customer', methods=['GET', 'POST'])
def select_customer():
    if 'username' not in session:
        return redirect(url_for('login_bp.login'))

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        return redirect(url_for('add_product', customer_id=customer_id))

    customers = read_customer_data()
    return render_template('select_customer.html', customers=customers)