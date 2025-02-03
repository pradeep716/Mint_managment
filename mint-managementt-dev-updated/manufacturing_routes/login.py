import json
from flask import redirect, session, url_for, Blueprint, request, render_template, flash

USERS_FILE = 'users.json'

# Helper function to load users from users.json


def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# create a blueprint for the dashboard route
login_bp = Blueprint('login_bp', __name__)

# Route for user login


@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()

        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('choose_option_bp.choose_option'))
        else:
            flash('Invalid credentials! Please try again.', 'danger')

    return render_template('enterprise_login.html')
