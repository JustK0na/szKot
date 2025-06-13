from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from common import hash_password,get_db_connection


przewoznik_bp = Blueprint('przewoznik', __name__, url_prefix='/przewoznik')


from flask_blueprints.przewoznik_blueprints.manage_trains import *
from flask_blueprints.przewoznik_blueprints.manage_connection import *

@przewoznik_bp.route('/', methods=['GET', 'POST'])
def przewoznik():
    if 'role' not in session or session['role'] != 'przewoznik':
        flash('Brak dostępu')
        return redirect(url_for('przewoznik.login'))

    conn = get_db_connection('przewoznik')
    cursor = conn.cursor()

    id_przewoznika = session.get('user_id')

    cursor.execute("""SELECT nazwa FROM przewoznicy WHERE id_przewoznika= %s""", (id_przewoznika,))
    nazwa = cursor.fetchone()

    cursor.close()

    return render_template('przewoznik/przewoznik.html', name=nazwa)


@przewoznik_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection('auth')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM przewoznicy WHERE username=%s", (username,))
        przewoznik = cursor.fetchone()
        cursor.close()
        conn.close()
        if przewoznik and przewoznik[3] == hash_password(password):
            session['user_id'] = przewoznik[0]
            session['user_name'] = przewoznik[2]
            session['role'] = 'przewoznik'
            return redirect(url_for('przewoznik.przewoznik'))
        
        flash('Niepoprawny login lub hasło')
    return render_template('przewoznik/przewoznik_login.html')
