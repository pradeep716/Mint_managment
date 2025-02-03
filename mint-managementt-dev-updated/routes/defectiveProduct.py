from datetime import datetime
from flask import Flask, redirect, render_template, request, Blueprint, session, url_for
import json

PRODUCT_DATA_FILE = 'products.json'
CUSTOMER_DATA_FILE = 'customers.json'

# Create a Blueprint for the home route
defectiveProduct_bp = Blueprint('defectiveProduct_bp', __name__)

app = Flask(__name__)


def read_product_data():
    try:
        with open(PRODUCT_DATA_FILE, 'r') as file:
            data = json.load(file)
            # print("Product Data Loaded:", data)  # Debugging output
            return data
    except FileNotFoundError:
        return {}

def read_defective_history():
    try:
        with open('defective_history.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def write_product_data(data):
    with open(PRODUCT_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def write_defective_history(data):
    with open('defective_history.json', 'w') as f:
        json.dump(data, f, indent=4)


@defectiveProduct_bp.route('/defective-product', methods=['GET', 'POST'])
def defective_product():
    if 'username' not in session:
        return redirect(url_for('login_bp.login'))

    if request.method == 'POST':
        product_id = request.form['product_id']
        defective_quantity = float(request.form['quantity'])  # Read defective quantity as a float
        selected_unit = request.form['unit']  # Get the unit selected by the user
        date_time = datetime.now().strftime('%Y-%m-%d')  # Only date

        # Load existing data
        products = read_product_data()
        defective_history = read_defective_history()

        if product_id in products:
            current_stock = float(products[product_id]['stock'])  # Ensure stock is handled as a float
            product_unit = products[product_id]['unit']  # Get the original unit of the product

            # Handle conversions between compatible units
            if selected_unit == 'g' and product_unit == 'kg':
                defective_quantity /= 1000  # Convert grams to kilograms
            elif selected_unit == 'kg' and product_unit == 'g':
                defective_quantity *= 1000  # Convert kilograms to grams
            elif selected_unit == 'ml' and product_unit == 'L':
                defective_quantity /= 1000  # Convert milliliters to liters
            elif selected_unit == 'L' and product_unit == 'ml':
                defective_quantity *= 1000  # Convert liters to milliliters
            elif selected_unit != product_unit:
                # If the unit is not compatible, return an error
                return f"Unit mismatch for product ID: {product_id}. Available unit: {product_unit}"

            # Ensure stock is not negative after defective quantity deduction
            if current_stock < defective_quantity:
                return f"Not enough stock for Product ID: {product_id}. Available stock: {current_stock} {product_unit}."

            # Update stock based on defective quantity
            products[product_id]['stock'] = current_stock - defective_quantity
            write_product_data(products)

            # Log defective product entry
            defective_id = len(defective_history) + 1
            defective_history[defective_id] = {
                'product_id': product_id,
                'quantity': defective_quantity,
                'unit': selected_unit,
                'date_time': date_time  # Only date
            }

            write_defective_history(defective_history)

            return f'Defective product entry recorded successfully! <a href="/defective-product">Go back</a>'

    # For GET request, load existing data
    products = read_product_data()
    defective_history = read_defective_history()
    product_classes = list(set(details['product_class'] for details in products.values()))

    return render_template('defective_product.html', products=products, product_classes=product_classes, defective_history=defective_history)