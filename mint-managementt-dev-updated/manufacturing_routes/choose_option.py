from flask import Blueprint, render_template, request, redirect, url_for

# create a blueprint for the dashboard route
choose_option_bp = Blueprint('choose_option_bp', __name__)

# Route to choose Manufacturing or Enterprise or production


@choose_option_bp.route('/choose_option', methods=['GET', 'POST'])
def choose_option():
    if request.method == 'POST':
        option = request.form['option']
        if option == 'manufacturing':
            return redirect(url_for('manufacturing_dashboard_bp.manufacturing_dashboard'))
        elif option == 'production':
            return redirect(url_for('production_dashboard_bp.production_dashboard'))
        elif option == 'enterprise':
            return redirect(url_for('enterprise_dashboard_bp.dashboard'))
    return render_template('dashboard.html')
