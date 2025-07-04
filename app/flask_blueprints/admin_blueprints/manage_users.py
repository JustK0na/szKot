from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_blueprints.admin_blueprint import admin_bp, get_db_connection,MySQLdb


@admin_bp.route('/pasazerowie')
def admin_pasazerowie():
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    

    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("SELECT id_pasażera, imie, nazwisko, mail, telefon, haslo FROM pasazerowie")
    users = cursor.fetchall()
    cursor.close()
    return render_template('admin/pasazerowie.html', users=users)



@admin_bp.route('/pasazerowie/<int:user_id>/bilety')
def pokaz_bilety_pasazera(user_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("SELECT id_biletu, id_pasażera, id_przejazdu, cena, ulgi FROM bilety WHERE id_pasażera = %s", (user_id,))
    tickets = cursor.fetchall()

    cursor.execute("SELECT imie, nazwisko FROM pasazerowie WHERE id_pasażera = %s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    return render_template('admin/bilety_pasazera.html', tickets=tickets, user=user, user_id=user_id)



@admin_bp.route('/pasazerowie/<int:user_id>/bilety/<int:ticket_id>/usun', methods=['POST'])
def usun_bilet(user_id, ticket_id):  
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM bilety WHERE id_biletu = %s", (ticket_id,))
        conn.commit()
    except MySQLdb.Error as e:
        conn.rollback()
        flash(f"Błąd MySQL: {e.args[1]}")

    cursor.close()
    return redirect(url_for('admin.pokaz_bilety_pasazera', user_id=user_id))



@admin_bp.route('/pasazerowie/<int:user_id>/bilety/<int:ticket_id>/edytuj', methods=['POST'])
def edytuj_bilet(user_id, ticket_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    cena = request.form.get('cena')
    ulga = request.form.get('ulga') 

    conn = get_db_connection('admin')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE bilety SET cena = %s, ulgi = %s WHERE id_biletu = %s
        """, (cena, ulga, ticket_id))
        conn.commit()
    except MySQLdb.Error as e:
        conn.rollback()
        flash(f"Błąd MySQL: {e.args[1]}")
    
    cursor.close()

    return redirect(url_for('admin.pokaz_bilety_pasazera', user_id=user_id))



@admin_bp.route('/pasazerowie/<int:user_id>', methods=['GET', 'POST'])
def edytuj_pasazera(user_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))   
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM pasazerowie WHERE id_pasażera=%s""", (user_id,))
    user = cursor.fetchall()

    if request.method == 'POST':
        try:
            imie = request.form.get('imie')
            naziwsko = request.form.get('nazwisko')
            email = request.form.get('email')
            telefon = request.form.get('telefon')
            
            cursor.execute("""
                UPDATE pasazerowie SET
                    imie = %s,
                    nazwisko = %s,
                    mail = %s,
                    telefon = %s
                WHERE id_pasażera = %s
            """, (imie, naziwsko, email, telefon, user_id))
            conn.commit()
            cursor.close()
            return redirect(url_for('admin.admin_pasazerowie'))
        except MySQLdb.Error as e:
            conn.rollback()
            flash(f"Błąd MySQL: {e.args[1]}")

    cursor.close()

    return render_template('admin/edytuj_pasazera.html',
                           user=user,)




@admin_bp.route('/pasazerowie/<int:user_id>/usun', methods=['POST'])
def usun_pasazera(user_id):   
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM pasazerowie WHERE id_pasażera = %s", (user_id,))
        conn.commit()
    except MySQLdb.Error as e:
        conn.rollback()
        flash(f"Błąd MySQL: {e.args[1]}")
        
    cursor.close()
    return redirect(url_for('admin.admin_pasazerowie', user_id=user_id))

