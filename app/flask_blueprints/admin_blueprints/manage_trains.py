from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_blueprints.admin_blueprint import admin_bp, get_db_connection


@admin_bp.route('/pociagi')
def admin_pociagi():
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            p.id_pociągu,
            p.model_pociągu,
            pr.nazwa AS przewoznik,
            s.nazwa_stacji,
            s.miasto,
            p.stan
        FROM pociagi p
        JOIN przewoznicy pr ON p.id_przewoźnika = pr.id_przewoznika
        JOIN stacje_kolejowe s ON p.id_aktualna_stacja = s.id_stacji
    """)

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
    
    cursor.execute("DELETE FROM wagony WHERE id_wagonu = %s", (wagon_id,))

    conn.commit()

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
    
    cursor.execute("""
        UPDATE wagony SET liczba_miejsc = %s WHERE id_wagonu = %s
    """, (liczba_miejsc , wagon_id))
    
    conn.commit()
    
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

    cursor.execute("""
        INSERT INTO wagony(id_pociągu, liczba_miejsc) VALUES(%s,%s)    """
                   , (train_id,liczba_miejsc))
    
    conn.commit()
    
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
        model = request.form.get('model_pociagu')
        id_przewoznika = request.form.get('id_przewoznika')
        id_stacji = request.form.get('id_stacji')
        stan = request.form.get('stan')
        
        cursor.execute("""
            UPDATE pociagi SET
                model_pociągu = %s,
                id_przewoźnika = %s,
                id_aktualna_stacja = %s,
                stan = %s
            WHERE id_pociągu = %s
        """, (model, id_przewoznika, id_stacji, stan, train_id))
        
        conn.commit()
        
        cursor.close()
        return redirect(url_for('admin.admin_pociagi'))

    cursor.execute("SELECT id_przewoznika,nazwa FROM przewoznicy ORDER BY nazwa")
    przewoznicy = cursor.fetchall()

    cursor.execute("SELECT id_stacji,nazwa_stacji FROM stacje_kolejowe ORDER BY nazwa_stacji")
    stacje = cursor.fetchall()

    cursor.close()

    return render_template('admin/edytuj_pociag.html',
                           train=train,
                           przewoznicy=przewoznicy,
                           stacje=stacje)





@admin_bp.route('/pociągi/dodaj', methods=['GET', 'POST'])
def dodaj_pociag():   
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()

    if request.method == 'POST':
        model = request.form.get('model_pociagu')
        id_przewoznika = request.form.get('id_przewoznika')
        id_stacji = request.form.get('id_stacji')
        stan = request.form.get('stan')
        
        cursor.execute("""
            INSERT INTO pociagi (
                model_pociągu, id_przewoźnika, id_aktualna_stacja,stan
            ) VALUES (%s,%s,%s,%s)
        """, (model, id_przewoznika, id_stacji, stan))
        
        conn.commit()
        cursor.close()
        return redirect(url_for('admin.admin_pociagi'))

    cursor.execute("SELECT id_przewoznika,nazwa FROM przewoznicy ORDER BY nazwa")
    przewoznicy = cursor.fetchall()

    cursor.execute("SELECT id_stacji,nazwa_stacji FROM stacje_kolejowe ORDER BY nazwa_stacji")
    stacje = cursor.fetchall()

    cursor.close()

    return render_template('admin/dodaj_pociag.html',
                           przewoznicy=przewoznicy,
                           stacje=stacje)



@admin_bp.route('/pociągi/<int:train_id>/usun', methods=['POST'])
def usun_pociag(train_id):   
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM wagony WHERE id_pociągu = %s", (train_id,))

    cursor.execute("DELETE FROM polaczenia WHERE id_pociągu = %s", (train_id,)) 

    cursor.execute("DELETE FROM pociagi WHERE id_pociągu = %s", (train_id,))


    conn.commit()
    cursor.close()
    return redirect(url_for('admin.admin_pociagi'))
