from datetime import datetime
from flask import Flask, render_template, Blueprint

# Create a Blueprint for the home route
pricePrediction_bp = Blueprint('pricePrediction_bp', __name__)

app = Flask(__name__)

@pricePrediction_bp.route('/price-prediction')
def price():
    return render_template('price.html')