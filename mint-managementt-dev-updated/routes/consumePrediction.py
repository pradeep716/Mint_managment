
from flask import Flask, render_template, Blueprint


import pandas as pd

# Create a Blueprint for the home route
consumePrediction_bp = Blueprint('consumePrediction_bp', __name__)

app = Flask(__name__)

# Load the CSV data into a DataFrame
data_sale = pd.read_csv('sales_data.csv')

@consumePrediction_bp.route('/consume-prediction', methods=['GET'])
def consume():
    categories = data_sale['category'].unique()
    return render_template('consume.html', categories=categories)