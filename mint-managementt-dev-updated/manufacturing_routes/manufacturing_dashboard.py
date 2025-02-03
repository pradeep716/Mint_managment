from flask import Blueprint, flash, render_template, request, redirect, session, url_for

# create a blueprint for the dashboard route
manufacturing_dashboard_bp = Blueprint('manufacturing_dashboard_bp', __name__)

# Manufacturing dashboard route


@manufacturing_dashboard_bp.route('/manufacturing_dashboard', methods=['GET', 'POST'])
def manufacturing_dashboard():
    if 'username' in session:
        if request.method == 'POST':
            return redirect(url_for('punch_order'))
        return render_template('manufacturing_dashboard.html')
    else:
        flash('Please login to access this page.', 'warning')
        return redirect(url_for('login_bp.login'))
