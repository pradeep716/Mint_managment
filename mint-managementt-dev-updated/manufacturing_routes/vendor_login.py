from flask import Flask, flash, redirect, render_template, Blueprint, request, session, url_for
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Use a secure key for sessions

VENDOR_USERS_FILE = 'vendor_users.json'

# Helper function to load users from vendor_users.json
def load_users():
    try:
        with open(VENDOR_USERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Return empty if the file does not exist

# Create a blueprint for the login and dashboard routes
vendor_login_bp = Blueprint('vendor_login_bp', __name__)

@vendor_login_bp.route('/vendor_login', methods=['GET', 'POST'])
def vendor_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        users = load_users()

        if username in users and users[username] == password:
            session['username'] = username  # Store username in session as the vendor name
            flash('Login successful!', 'success')
            return redirect(url_for('vendor_dashboard_bp.vendor_dashboard'))  # Redirect to dashboard
        else:
            flash('Invalid credentials! Please try again.', 'danger')

    return render_template('vendor_login.html')  # Render the login page on GET or error

@vendor_login_bp.route('/vendor_dashboard')
def vendor_dashboard():
    if 'username' not in session:
        return redirect(url_for('vendor_login_bp.vendor_login'))  # Redirect to login if no session exists
    return render_template('vendor_dashboard.html', username=session['username'])
