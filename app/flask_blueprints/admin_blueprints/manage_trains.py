from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_blueprints.admin_blueprint import admin_bp, get_db_connection,MySQLdb


@admin_bp.route('/pociagi')
def admin_pociagi():
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()
    
    cursor.execute(""" SELECT * FROM pociag_szczeg """)

    trains = cursor.fetchall()
    cursor.close()

    return render_template('admin/pociagi.html', trains=trains)



@admin_bp.route('/pociągi/<int:train_id>/wagony')
def pokaz_wagony(train_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM wagony WHERE id_pociągu = %s", (train_id,))
    wagons = cursor.fetchall()

    cursor.close()
    return render_template('admin/wagony.html', wagons=wagons, train_id = train_id)



@admin_bp.route('/pociągi/<int:train_id>/wagony/<int:wagon_id>/usun', methods=['POST'])
def usun_wagon(train_id,wagon_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))

    conn = get_db_connection('admin')
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM wagony WHERE id_wagonu = %s", (wagon_id,))
        conn.commit()
    except MySQLdb.Error as e:
        conn.rollback()
        flash(f"Błąd MySQL: {e.args[1]}")

    cursor.close()
    return redirect(url_for('admin.pokaz_wagony', train_id=train_id))



@admin_bp.route('/pociągi/<int:train_id>/wagony/<int:wagon_id>/edytuj', methods=['POST'])
def edytuj_wagon(train_id, wagon_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    liczba_miejsc = request.form.get('liczba_miejsc')
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE wagony SET liczba_miejsc = %s WHERE id_wagonu = %s
        """, (liczba_miejsc , wagon_id))
        conn.commit()
    except MySQLdb.Error as e:
        conn.rollback()
        flash(f"Błąd MySQL: {e.args[1]}")


    cursor.close()

    return redirect(url_for('admin.pokaz_wagony', train_id=train_id))


@admin_bp.route('/pociągi/<int:train_id>/wagony/dodaj', methods=['POST'])
def dodaj_wagon(train_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    liczba_miejsc = request.form.get('liczba_miejsc')
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO wagony(id_pociągu, liczba_miejsc) VALUES(%s,%s)    """
                    , (train_id,liczba_miejsc))
        conn.commit()
    except MySQLdb.Error as e:
        conn.rollback()
        flash(f"Błąd MySQL: {e.args[1]}")
    
    cursor.close()

    return redirect(url_for('admin.pokaz_wagony', train_id=train_id))





@admin_bp.route('/pociągi/<int:train_id>', methods=['GET', 'POST'])
def edytuj_pociag(train_id):   
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM pociagi WHERE id_pociągu=%s""", (train_id,))
    train = cursor.fetchall()

    if request.method == 'POST':
        try:
            model = request.form.get('id_modelu')
            id_przewoznika = request.form.get('id_przewoznika')
            stan = request.form.get('stan')
            
            cursor.execute("""
                UPDATE pociagi SET
                    id_modelu = %s,
                    id_przewoźnika = %s,
                    stan = %s
                WHERE id_pociągu = %s
            """, (model, id_przewoznika, stan, train_id))
            
            conn.commit()
            cursor.close()
            return redirect(url_for('admin.admin_pociagi'))
        except MySQLdb.Error as e:
            conn.rollback()
            flash(f"Błąd MySQL: {e.args[1]}")

    cursor.execute("SELECT id_przewoznika,nazwa FROM przewoznicy ORDER BY nazwa")
    przewoznicy = cursor.fetchall()

    cursor.execute("SELECT id_modelu,nazwa_modelu FROM modele_pociagow ORDER BY nazwa_modelu")
    models = cursor.fetchall()

    cursor.close()

    return render_template('admin/edytuj_pociag.html',
                           train=train,
                           przewoznicy=przewoznicy,
                           models = models)





@admin_bp.route('/pociągi/dodaj', methods=['GET', 'POST'])
def dodaj_pociag():   
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()

    if request.method == 'POST':
        try:
            model = request.form.get('id_modelu')
            id_przewoznika = request.form.get('id_przewoznika')
            stan = request.form.get('stan')
            
            cursor.execute("""
                INSERT INTO pociagi (
                    id_modelu, id_przewoźnika,stan
                ) VALUES (%s,%s,%s)
            """, (model, id_przewoznika, stan))
            
            conn.commit()
            cursor.close()
            return redirect(url_for('admin.admin_pociagi'))
        except MySQLdb.Error as e:
            conn.rollback()
            flash(f"Błąd MySQL: {e.args[1]}")

    cursor.execute("SELECT id_przewoznika,nazwa FROM przewoznicy ORDER BY nazwa")
    przewoznicy = cursor.fetchall()

    cursor.execute("SELECT id_modelu,nazwa_modelu FROM modele_pociagow ORDER BY nazwa_modelu")
    models = cursor.fetchall()

    cursor.close()

    return render_template('admin/dodaj_pociag.html',
                           przewoznicy=przewoznicy,
                           models = models)



@admin_bp.route('/pociągi/<int:train_id>/usun', methods=['POST'])
def usun_pociag(train_id):   
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM pociagi WHERE id_pociągu = %s", (train_id,))
        conn.commit()
    except MySQLdb.Error as e:
        conn.rollback()
        flash(f"Błąd MySQL: {e.args[1]}")

    cursor.close()
    return redirect(url_for('admin.admin_pociagi'))



@admin_bp.route('/pociągi/modele')
def modele_pociagow():
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM modele_pociagow")
    models = cursor.fetchall()

    cursor.close()
    return render_template('admin/modele_pociagow.html', models=models)



@admin_bp.route('/pociągi/modele/<int:model_id>/usun', methods=['POST'])
def usun_model(model_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))

    conn = get_db_connection('admin')
    cursor = conn.cursor()
    try:    
        cursor.execute("DELETE FROM modele_pociagow WHERE id_modelu = %s", (model_id,))
        conn.commit()
    except MySQLdb.Error as e:
        conn.rollback()
        flash(f"Błąd MySQL: {e.args[1]}")

    cursor.close()
    return redirect(url_for('admin.modele_pociagow'))



@admin_bp.route('/pociągi/modele/<int:model_id>/edytuj', methods=['POST'])
def edytuj_model(model_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    model_pociagu = request.form.get('model_pociagu')
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE modele_pociagow SET nazwa_modelu = %s WHERE id_modelu = %s
        """, (model_pociagu , model_id))
        conn.commit()
    except MySQLdb.Error as e:
        conn.rollback()
        flash(f"Błąd MySQL: {e.args[1]}")
    
    cursor.close()

    return redirect(url_for('admin.modele_pociagow'))


@admin_bp.route('/pociągi/modele/dodaj', methods=['POST'])
def dodaj_model():
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    model_pociagu = request.form.get('model_pociagu')
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO modele_pociagow(nazwa_modelu) VALUES(%s)    """
                    , (model_pociagu,))
        conn.commit()
    except MySQLdb.Error as e:
        conn.rollback()
        flash(f"Błąd MySQL: {e.args[1]}")
    
    cursor.close()

    return redirect(url_for('admin.modele_pociagow'))
