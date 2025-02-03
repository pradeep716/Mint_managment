from flask import Blueprint, redirect, url_for

# create a blueprint for the dashboard route
redirection_bp = Blueprint('redirection_bp',__name__)
@redirection_bp.route('/')
def home():
    return redirect(url_for('login_bp.login'))  # Redirect to the login page
