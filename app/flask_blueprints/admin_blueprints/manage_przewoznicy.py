from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_blueprints.admin_blueprint import admin_bp, get_db_connection,MySQLdb
from common import hash_password

@admin_bp.route('/przewoznicy')
def admin_przewoznicy():
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM przewoznicy")
    przewoznicy = cursor.fetchall()
    cursor.close()
    return render_template('admin/przewoznicy.html', przewoznicy=przewoznicy)



@admin_bp.route('/przewoznicy/<int:przewoznik_id>', methods=['GET', 'POST'])
def edytuj_przewoznika(przewoznik_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))   
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM przewoznicy WHERE id_przewoznika=%s""", (przewoznik_id,))
    przewoznik = cursor.fetchall()

    if request.method == 'POST':
        try:
            nazwa = request.form.get('nazwa')
            username = request.form.get('username')
            nowe_haslo = request.form.get('haslo')
            
            hash_haslo = hash_password(nowe_haslo)

            cursor.execute("""
                UPDATE przewoznicy SET
                    nazwa = %s,
                    username = %s,
                    haslo = %s
                WHERE id_przewoznika = %s
            """, (nazwa, username, hash_haslo, przewoznik_id))
            conn.commit()
            cursor.close()
            return redirect(url_for('admin.admin_przewoznicy'))
        except MySQLdb.Error as e:
            conn.rollback()
            flash(f"Błąd MySQL: {e.args[1]}")


    cursor.close()

    return render_template('admin/edytuj_przewoznika.html',
                           przewoznik=przewoznik)


@admin_bp.route('/przewoznicy/dodaj', methods=['GET', 'POST'])
def dodaj_przewoznika():
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))   
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()

    if request.method == 'POST':
        try:
            nazwa = request.form.get('nazwa')
            username = request.form.get('username')
            nowe_haslo = request.form.get('haslo')
            
            hash_haslo = hash_password(nowe_haslo)

            cursor.execute("""
                INSERT INTO przewoznicy(
                    nazwa,
                    username,
                    haslo) VALUES(%s, %s, %s)
            """, (nazwa, username, hash_haslo))
            conn.commit()
            cursor.close()
            return redirect(url_for('admin.admin_przewoznicy'))
        except MySQLdb.Error as e:
            conn.rollback()
            flash(f"Błąd MySQL: {e.args[1]}")



    cursor.close()

    return render_template('admin/dodaj_przewoznika.html')








@admin_bp.route('/przewoznicy/<int:przewoznik_id>/usun', methods=['POST'])
def usun_przewoznika(przewoznik_id):   
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM przewoznicy WHERE id_przewoznika = %s", (przewoznik_id,))
        conn.commit()
    except MySQLdb.Error as e:
        conn.rollback()
        flash(f"Błąd MySQL: {e.args[1]}")
    
    cursor.close()
    return redirect(url_for('admin.admin_przewoznicy', przewoznik_id=przewoznik_id))

