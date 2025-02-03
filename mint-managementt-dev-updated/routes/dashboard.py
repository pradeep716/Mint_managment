from flask import Flask, render_template, redirect, url_for, session, Blueprint, request, flash

# Create a Blueprint for the home route
enterprise_dashboard_bp = Blueprint('enterprise_dashboard_bp', __name__)

# app = Flask(__name__)


@enterprise_dashboard_bp.route('/enterprise_dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login_bp.login'))

    return render_template('enterprise_dashboard.html', username=session['username'])


# from flask import redirect, url_for, Blueprint, request, render_template

# # create a blueprint for the dashboard route
# dashboard_bp = Blueprint('dashboard_bp', __name__)


# @dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
# def dashboard():
#     if request.method == 'POST':
#         option = request.form['option']
#         if option == 'manufacturing':
#             return redirect(url_for('manufacturing_dashboard_bp.manufacturing_dashboard'))
#         elif option == 'production':
#             return redirect(url_for('production_dashboard_bp.production_dashboard'))
#         elif option == 'enterprise':
#             # You can add the enterprise dashboard later
#             # return redirect(url_for('enterprise_login_bp.login'))
#             return redirect(url_for('enterprise_dashboard_bp.dashboard'))

#     return render_template('dashboard.html')  # Handle GET requests
