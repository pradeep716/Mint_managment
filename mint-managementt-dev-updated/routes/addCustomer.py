from flask import Flask, render_template, redirect, request, url_for, session , Blueprint
import json

CUSTOMER_DATA_FILE = 'customers.json'

# Create a Blueprint for the home route
addCustomer_bp = Blueprint('addCustomer_bp', __name__)

app = Flask(__name__)

def read_customer_data():
    try:
        with open(CUSTOMER_DATA_FILE, 'r') as file:
            data = json.load(file)
            # print("Customer Data Loaded:", data)  # Debugging output
            return data
    except FileNotFoundError:
        return {}

def write_customer_data(data):
    with open(CUSTOMER_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@addCustomer_bp.route('/add-customer', methods=['GET', 'POST'])
def add_customer():
    if 'username' not in session:
        return redirect(url_for('login_bp.login'))

    if request.method == 'POST':
        customer_name = request.form['customer_name']
        #customer_email = request.form['customer_email']
        #customer_phone = request.form['customer_phone']

        customers = read_customer_data()
        customer_id = str(len(customers) + 1)  # Simple unique ID generation

        customers[customer_id] = {
            'name': customer_name,
            #'email': customer_email,
            #'phone': customer_phone
        }

        write_customer_data(customers)
        #return redirect(url_for('select_customer'))

    return render_template('add_customer.html')