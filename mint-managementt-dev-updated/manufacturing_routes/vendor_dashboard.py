from flask import Blueprint, flash ,render_template, request, redirect, session, url_for

# create a blueprint for the dashboard route
vendor_dashboard_bp= Blueprint('vendor_dashboard_bp',__name__)

# Manufacturing dashboard route
@vendor_dashboard_bp.route('/vendor_dashboard', methods=['GET', 'POST'])
def vendor_dashboard():
    if 'username' in session:
        if request.method == 'POST':
            return redirect(url_for('quotation_vendor'))
        return render_template('vendor_dashboard.html')
    else:
        flash('Please login to access this page.', 'warning')
        return redirect(url_for('vendor_login'))