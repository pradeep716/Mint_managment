import json
from flask import redirect, url_for, Blueprint , request , render_template , flash

USERS_FILE = 'users.json'

# Helper function to load users from users.json
def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Helper function to save users to users.json
def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)
# create a blueprint for the dashboard route
signup_bp = Blueprint('signup_bp',__name__)

# Route for user signup
@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()

        if username in users:
            flash('User already exists! Please login.', 'warning')
            return redirect(url_for('login_bp.login'))

        users[username] = password
        save_users(users)
        flash('Signup successful! Please login.', 'success')
        return redirect(url_for('login_bp.login'))

    return render_template('signup.html')