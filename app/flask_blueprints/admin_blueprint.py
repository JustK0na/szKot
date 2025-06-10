from flask import Blueprint, render_template, request, redirect, url_for, session, flash

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

from flask_blueprints.admin_blueprints.manage_connection import *
from flask_blueprints.admin_blueprints.manage_users import *
from flask_blueprints.admin_blueprints.manage_lines import *
from flask_blueprints.admin_blueprints.manage_stations import *

@admin_bp.route('/', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('admin/admin.html')










