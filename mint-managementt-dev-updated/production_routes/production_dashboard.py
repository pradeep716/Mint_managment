from flask import flash, redirect, session, url_for, Blueprint, request, render_template

# create a blueprint for the dashboard route
production_dashboard_bp = Blueprint('production_dashboard_bp', __name__)


@production_dashboard_bp.route('/production_dashboard', methods=['GET', 'POST'])
def production_dashboard():
    if 'username' in session:
        if request.method == 'POST':
            return redirect(url_for('punch_order'))
        return render_template('production_dashboard.html')
    else:
        flash('Please login to access this page.', 'warning')
        return redirect(url_for('enterprise_login_bp.enterprise_login'))
