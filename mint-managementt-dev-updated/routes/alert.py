import json
from flask import Flask, render_template, request, redirect, url_for, session , Blueprint

app = Flask(__name__)

# Create a Blueprint for the home route
alert_bp = Blueprint('alert_bp', __name__)

def load_products():
    with open('products.json') as f:
        return json.load(f)
    
@alert_bp.route('/alert')
def alert_page():
    products = load_products()  # Load your product data
    low_stock_products = []

    # Check the 'stock' value, which may include units (e.g., "200 g", "30 L")
    for name, info in products.items():
        try:
            stock_value = float(info['stock'])  # Convert to float to handle numbers
        except ValueError:
            stock_value = 0  # Handle any non-numeric values gracefully

        if stock_value < 5:  # Compare the stock value with threshold (5 units)
            low_stock_products.append({
                "product_id": name,
                "name": name,
                "total_stock": f"{stock_value} {info['unit']}"  # Include the unit in the display
            })

    username = session.get('username', 'User')  # Get username from session

    if low_stock_products:
        return render_template('alert.html', low_stock_items=low_stock_products, username=username)

    return render_template('enterprise_dashboard.html', username=username)  # Render dashboard if no low stock products