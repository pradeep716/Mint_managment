# Route for logout


from flask import Blueprint, flash, redirect, session, url_for
# create a blueprint for the dashboard route
logout_bp = Blueprint('logout_bp', __name__)


@logout_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('enterprise_login_bp.login'))
