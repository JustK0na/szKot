from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from common import hash_password,get_db_connection


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

from flask_blueprints.admin_blueprints.manage_connection import *
from flask_blueprints.admin_blueprints.manage_users import *
from flask_blueprints.admin_blueprints.manage_lines import *
from flask_blueprints.admin_blueprints.manage_stations import *
from flask_blueprints.admin_blueprints.manage_trains import *
from flask_blueprints.admin_blueprints.manage_przewoznicy import *

@admin_bp.route('/', methods=['GET', 'POST'])
def admin():
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))

    return render_template('admin/admin.html')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection('auth')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM admins WHERE username=%s", (username,))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        if admin and admin[2] == hash_password(password):
            session['user_id'] = admin[0]
            session['user_name'] = admin[1]
            session['role'] = 'admin'
            return redirect(url_for('admin.admin'))
        
        flash('Niepoprawny login lub hasło')
    return render_template('admin/admin_login.html')






