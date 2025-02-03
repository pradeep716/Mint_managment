from flask import render_template, request, redirect, url_for, session, Blueprint
import json

USER_DATA_FILE = 'enterprise_users.json'


# Create a Blueprint for the home route
enterprise_login_bp = Blueprint('enterprise_login_bp', __name__)


def read_user_data():
    try:
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


@enterprise_login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = read_user_data()  # Assume this function reads user data from a file or database

        if users.get(username) == password:
            session['username'] = username  # Store the username in the session
            # Redirect to the alert page
            # return redirect(url_for('alert_bp.alert_page'))
            return redirect(url_for('choose_option_bp.choose_option'))

        else:
            return 'Invalid credentials! <a href="/login">Try again</a>'

    return render_template('enterprise_login.html')
