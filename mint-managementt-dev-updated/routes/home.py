# routes/home.py
from flask import redirect, url_for, Blueprint

# Create a Blueprint for the home route
home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
def home():
    return redirect(url_for('login_bp.login'))
