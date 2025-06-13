from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_blueprints.przewoznicy_blueprint import przewoznik_bp, get_db_connection


@przewoznik_bp.route('/pociagi')
def przewoznik_pociagi():
    if 'role' not in session or session['role'] != 'przewoznik':
        flash('Brak dostępu')
        return redirect(url_for('przewoznik.login'))
    
    conn = get_db_connection('przewoznik')
    cursor = conn.cursor()
    
    id_przewoznika = session.get('user_id')

    cursor.execute("""
        SELECT 
            p.id_pociągu,
            m.nazwa_modelu,
            pr.nazwa AS przewoznik,
            p.stan
        FROM pociagi p
        JOIN przewoznicy pr ON p.id_przewoźnika = pr.id_przewoznika
        JOIN modele_pociagow m ON p.id_modelu = m.id_modelu
        WHERE p.id_przewoźnika = %s
    """, (id_przewoznika,))

    trains = cursor.fetchall()
    cursor.close()

    return render_template('przewoznik/pociagi.html', trains=trains)



@przewoznik_bp.route('/pociągi/<int:train_id>/wagony')
def pokaz_wagony(train_id):
    if 'role' not in session or session['role'] != 'przewoznik':
        flash('Brak dostępu')
        return redirect(url_for('przewoznik.login'))
    
    conn = get_db_connection('przewoznik')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM wagony WHERE id_pociągu = %s", (train_id,))
    wagons = cursor.fetchall()

    cursor.close()
    return render_template('przewoznik/wagony.html', wagons=wagons, train_id = train_id)



@przewoznik_bp.route('/pociągi/<int:train_id>/wagony/<int:wagon_id>/usun', methods=['POST'])
def usun_wagon(train_id,wagon_id):
    if 'role' not in session or session['role'] != 'przewoznik':
        flash('Brak dostępu')
        return redirect(url_for('przewoznik.login'))

    conn = get_db_connection('przewoznik')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM wagony WHERE id_wagonu = %s", (wagon_id,))

    conn.commit()

    cursor.close()
    return redirect(url_for('przewoznik.pokaz_wagony', train_id=train_id))



@przewoznik_bp.route('/pociągi/<int:train_id>/wagony/<int:wagon_id>/edytuj', methods=['POST'])
def edytuj_wagon(train_id, wagon_id):
    if 'role' not in session or session['role'] != 'przewoznik':
        flash('Brak dostępu')
        return redirect(url_for('przewoznik.login'))
    
    liczba_miejsc = request.form.get('liczba_miejsc')
    
    conn = get_db_connection('przewoznik')
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE wagony SET liczba_miejsc = %s WHERE id_wagonu = %s
    """, (liczba_miejsc , wagon_id))
    
    conn.commit()
    
    cursor.close()

    return redirect(url_for('przewoznik.pokaz_wagony', train_id=train_id))


@przewoznik_bp.route('/pociągi/<int:train_id>/wagony/dodaj', methods=['POST'])
def dodaj_wagon(train_id):
    if 'role' not in session or session['role'] != 'przewoznik':
        flash('Brak dostępu')
        return redirect(url_for('przewoznik.login'))
    
    liczba_miejsc = request.form.get('liczba_miejsc')
    
    conn = get_db_connection('przewoznik')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO wagony(id_pociągu, liczba_miejsc) VALUES(%s,%s)    """
                   , (train_id,liczba_miejsc))
    
    conn.commit()
    
    cursor.close()

    return redirect(url_for('przewoznik.pokaz_wagony', train_id=train_id))





@przewoznik_bp.route('/pociągi/<int:train_id>', methods=['GET', 'POST'])
def edytuj_pociag(train_id):   
    if 'role' not in session or session['role'] != 'przewoznik':
        flash('Brak dostępu')
        return redirect(url_for('przewoznik.login'))
    
    conn = get_db_connection('przewoznik')
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM pociagi WHERE id_pociągu=%s""", (train_id,))
    train = cursor.fetchall()

    if request.method == 'POST':
        id_modelu = request.form.get('id_modelu')

        id_przewoznika = session.get('user_id')

        stan = request.form.get('stan')
        
        cursor.execute("""
            UPDATE pociagi SET
                id_modelu = %s,
                id_przewoźnika = %s,
                stan = %s
            WHERE id_pociągu = %s
        """, (id_modelu, id_przewoznika, stan, train_id))
        
        conn.commit()
        
        cursor.close()
        return redirect(url_for('przewoznik.przewoznik_pociagi'))


    cursor.execute("SELECT * FROM modele_pociagow")
    models = cursor.fetchall()

    cursor.close()

    return render_template('przewoznik/edytuj_pociag.html',
                           train=train,
                           models=models)





@przewoznik_bp.route('/pociągi/dodaj', methods=['GET', 'POST'])
def dodaj_pociag():   
    if 'role' not in session or session['role'] != 'przewoznik':
        flash('Brak dostępu')
        return redirect(url_for('przewoznik.login'))
    
    conn = get_db_connection('przewoznik')
    cursor = conn.cursor()

    if request.method == 'POST':
        id_modelu = request.form.get('id_modelu')

        id_przewoznika = session.get('user_id')
        
        stan = request.form.get('stan')
        
        cursor.execute("""
            INSERT INTO pociagi (
                id_modelu, id_przewoźnika,stan
            ) VALUES (%s,%s,%s)
        """, (id_modelu, id_przewoznika, stan))
        
        conn.commit()
        cursor.close()
        return redirect(url_for('przewoznik.przewoznik_pociagi'))


    cursor.execute("SELECT * FROM modele_pociagow")
    models = cursor.fetchall()


    cursor.close()

    return render_template('przewoznik/dodaj_pociag.html',models=models)



@przewoznik_bp.route('/pociągi/<int:train_id>/usun', methods=['POST'])
def usun_pociag(train_id):   
    if 'role' not in session or session['role'] != 'przewoznik':
        flash('Brak dostępu')
        return redirect(url_for('przewoznik.login'))
    
    conn = get_db_connection('przewoznik')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM pociagi WHERE id_pociągu = %s", (train_id,))


    conn.commit()
    cursor.close()
    return redirect(url_for('przewoznik.przewoznik_pociagi'))
