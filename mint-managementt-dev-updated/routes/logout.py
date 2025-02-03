
from flask import Flask, jsonify,Blueprint, redirect, session, url_for


# Create a Blueprint for the home route
enterprise_logout_bp = Blueprint('enterprise_logout_bp', __name__)

app = Flask(__name__)

@enterprise_logout_bp.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('enterprise_login_bp.login'))