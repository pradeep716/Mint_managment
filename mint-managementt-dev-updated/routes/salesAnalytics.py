from datetime import datetime
from flask import Flask, redirect, render_template, request, Blueprint, session, url_for
import json

PRODUCT_DATA_FILE = 'products.json'

# Create a Blueprint for the home route
salesAnalytics_bp = Blueprint('salesAnalytics_bp', __name__)

app = Flask(__name__)


def read_orders_data():
    try:
        with open('orders.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file doesn't exist


def read_product_data():
    try:
        with open(PRODUCT_DATA_FILE, 'r') as file:
            data = json.load(file)
            # print("Product Data Loaded:", data)  # Debugging output
            return data
    except FileNotFoundError:
        return {}


@salesAnalytics_bp.route('/sales-analytics', methods=['GET', 'POST'])
def sales_analytics():
    if 'username' not in session:
        return redirect(url_for('login_bp.login'))

    # Load orders and products
    orders = read_orders_data()
    products = read_product_data()

    # Default values for filters
    graph_type = request.form.get('graph_type', 'bar')
    time_frame = request.form.get('time_frame', 'monthly')
    product_class = request.form.get('product_class', '')
    product_id = request.form.get('product_id', '')
    selected_unit = request.form.get('unit', 'kg')

    # Filter orders
    filtered_orders = [
        order for order in orders.values()  # Change this to .values()
        if (product_class == '' or
            (order.get('product_id') in products and
             products[order.get('product_id')]['product_class'] == product_class)) and
        (product_id == '' or order.get('product_id') == product_id)
    ]

    # Initialize chart data
    chart_data = {
        'labels': [],
        'values': []
    }

    # Debug print
    # print(f"Filtered Orders: {filtered_orders}")

    for order in filtered_orders:
        try:
            order_date = order.get('order_date')
            if not order_date:
                print(f"Skipping order due to missing date: {order}")
                continue

            date = datetime.strptime(order_date, '%Y-%m-%d')

            # Format label based on time frame
            if time_frame == 'monthly':
                label = date.strftime('%Y-%m')
            elif time_frame == 'weekly':
                label = date.strftime('%Y-W%U')
            else:  # quarterly
                quarter = (date.month - 1) // 3 + 1
                label = f"{date.year}-Q{quarter}"

            # Get stock and convert units
            stock = float(order.get('stock', 0))
            unit = order.get('unit', '')

            # Convert units if necessary
            if unit == 'kg' and selected_unit == 'g':
                stock *= 1000
            elif unit == 'g' and selected_unit == 'kg':
                stock /= 1000
            elif unit == 'L' and selected_unit == 'ml':
                stock *= 1000
            elif unit == 'ml' and selected_unit == 'L':
                stock /= 1000

            # Aggregate data
            if label in chart_data['labels']:
                index = chart_data['labels'].index(label)
                chart_data['values'][index] += stock
            else:
                chart_data['labels'].append(label)
                chart_data['values'].append(stock)

        except Exception as e:
            print(f"Error processing order: {order}, Error: {e}")
            continue

    # Sort labels chronologically
    sorted_indices = sorted(range(len(chart_data['labels'])),
                            key=lambda k: chart_data['labels'][k])
    chart_data['labels'] = [chart_data['labels'][i] for i in sorted_indices]
    chart_data['values'] = [chart_data['values'][i] for i in sorted_indices]

    # Debug print
    # print(f"Chart Data: {chart_data}")

    return render_template('sales_analytics.html',
                           chart_data=chart_data,
                           products=products,
                           product_classes=sorted(
                               set(p['product_class'] for p in products.values())),
                           selected_class=product_class,
                           selected_id=product_id,
                           graph_type=graph_type,
                           time_frame=time_frame,
                           selected_unit=selected_unit)
