from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_blueprints.admin_blueprint import admin_bp,get_db_connection


@admin_bp.route('/polaczenia')
def admin_polaczenia():
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login')) 
      

    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            p.id_połączenia,
            sp.nazwa_stacji AS stacja_początkowa,
            sk.nazwa_stacji AS stacja_końcowa,
            p.czas_przejazdu,
            p.godzina_odjazdu,
            p.dni_tygodnia,
            p.cena,
            pr.nazwa
        FROM polaczenia p
        JOIN stacje_kolejowe sp ON p.id_stacji_początkowej = sp.id_stacji
        JOIN stacje_kolejowe sk ON p.id_stacji_końcowej = sk.id_stacji 
        JOIN przewoznicy pr ON p.id_przewoznika = pr.id_przewoznika""")
    connections = cursor.fetchall()

    cursor.close()
    return render_template('admin/polaczenia.html', connections=connections)



@admin_bp.route('/polaczenia/<int:connection_id>/edytuj', methods=['GET', 'POST'])
def edytuj_polaczenie(connection_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login')) 
      

    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM polaczenia WHERE id_połączenia = %s
    """, (connection_id,))
    connection = cursor.fetchone()

    if request.method == 'POST':
        id_stacji_poczatkowej = request.form.get('id_stacji_początkowej')
        id_stacji_koncowej = request.form.get('id_stacji_końcowej')
        czas_przejazdu = request.form.get('czas_przejazdu')
        godzina_odjazdu = request.form.get('godzina_odjazdu')
        dni_tygodnia = ','.join(request.form.getlist('dni_tygodnia'))  
        cena = request.form.get('cena')
        id_przewoznika = request.form.get('id_przewoznika')

        cursor.execute("""
            UPDATE polaczenia SET
                id_stacji_początkowej = %s,
                id_stacji_końcowej = %s,
                czas_przejazdu = %s,
                godzina_odjazdu = %s,
                dni_tygodnia = %s,
                cena = %s,
                id_przewoznika = %s
            WHERE id_połączenia = %s
        """, (id_stacji_poczatkowej, id_stacji_koncowej, czas_przejazdu,
              godzina_odjazdu, dni_tygodnia,cena ,id_przewoznika ,connection_id))
        conn.commit()
        cursor.close()
        return redirect(url_for('admin.admin_polaczenia'))



    cursor.execute("SELECT id_stacji, nazwa_stacji FROM stacje_kolejowe ORDER BY nazwa_stacji")
    stacje = cursor.fetchall()


    cursor.execute("SELECT id_przewoznika, nazwa FROM przewoznicy ORDER BY nazwa")
    przewoznicy = cursor.fetchall()

    cursor.close()
    return render_template('admin/edytuj_polaczenie.html',
                           przewoznicy=przewoznicy,
                           connection=connection,
                           stacje=stacje)



@admin_bp.route('/polaczenia/dodaj', methods=['GET', 'POST'])
def dodaj_polaczenie():
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login')) 
      

    conn = get_db_connection('admin')
    cursor = conn.cursor()

    if request.method == 'POST':
        id_stacji_poczatkowej = request.form.get('id_stacji_początkowej')
        id_stacji_koncowej = request.form.get('id_stacji_końcowej')
        czas_przejazdu = request.form.get('czas_przejazdu')
        godzina_odjazdu = request.form.get('godzina_odjazdu')
        dni_tygodnia = ','.join(request.form.getlist('dni_tygodnia'))
        cena = request.form.get('cena')
        id_przewoznika = request.form.get('id_przewoznika')
        
        cursor.execute("""
            INSERT INTO polaczenia (
                id_stacji_początkowej,
                id_stacji_końcowej,
                czas_przejazdu,
                godzina_odjazdu,
                dni_tygodnia,
                cena,
                id_przewoznika
            ) VALUES (%s, %s, %s, %s, %s,%s,%s)
        """, ( id_stacji_poczatkowej, id_stacji_koncowej,
              czas_przejazdu, godzina_odjazdu,  dni_tygodnia,cena,id_przewoznika))
        
        conn.commit()
        cursor.close()
        return redirect(url_for('admin.admin_polaczenia'))

    cursor.execute("SELECT id_stacji, nazwa_stacji FROM stacje_kolejowe ORDER BY nazwa_stacji")
    stacje = cursor.fetchall()

    cursor.execute("SELECT id_przewoznika, nazwa FROM przewoznicy ORDER BY nazwa")
    przewoznicy = cursor.fetchall()


    cursor.close()

    return render_template('admin/dodaj_polaczenie.html',
                           stacje=stacje,
                           przewoznicy=przewoznicy)



@admin_bp.route('/polaczenia/<int:connection_id>/usun', methods=['POST'])
def usun_polaczenie(connection_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login')) 
         
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM polaczenia WHERE id_połączenia = %s", (connection_id,))
    conn.commit()
    cursor.close()
    return redirect(url_for('admin.admin_polaczenia'))



@admin_bp.route('/polaczenia/<int:connection_id>/przejazdy')
def przejazdy_polaczenia(connection_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login')) 

    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("""SELECT id_przejazdu,
                   data,
                   godzina_odjazdu,
                   czas_przejazdu,
                   cena,opoznienie,
                   nazwa_stacji_początkowej,
                   nazwa_stacji_końcowej,
                   nazwa_przewoznika,
                   nazwa_modelu,
                   id_pociągu,
                   stan
                FROM przejazd_szczeg WHERE id_połączenia=%s""", (connection_id,))

    przejazdy = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin/przejazdy_polaczenia.html', przejazdy=przejazdy, connection_id = connection_id)



@admin_bp.route('/polaczenia/<int:connection_id>/przejazdy/dodaj', methods=['GET', 'POST'])
def dodaj_przejazd(connection_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login')) 
      
    conn = get_db_connection('admin')
    cursor = conn.cursor()

    if request.method == 'POST':
        id_pociagu = request.form.get('id_pociagu')
        data = request.form.get('data_przejazdu')
        stan = request.form.get('stan')
        opoznienie = request.form.get('opoznienie')

        cursor.execute("""
            INSERT INTO przejazdy(
                id_połączenia,
                id_pociągu,
                data,
                stan,
                opoznienie) VALUES (%s,%s,%s,%s,%s)
        """, (connection_id,id_pociagu, data, stan, opoznienie))
        
        conn.commit()
        cursor.close()
        return redirect(url_for('admin.przejazdy_polaczenia', connection_id=connection_id))


    cursor.execute("SELECT id_pociągu, nazwa_modelu,nazwa_przewoznika FROM pociag_szczeg")
    pociagi = cursor.fetchall()

    cursor.close()

    return render_template('admin/dodaj_przejazd.html',
                           pociagi=pociagi,
                           connection_id=connection_id)




@admin_bp.route('/polaczenia/<int:connection_id>/przejazdy/<int:przejazd_id>/usun', methods=['POST'])
def usun_przejazd_polaczanie(connection_id,przejazd_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login')) 
         
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM przejazdy WHERE id_przejazdu = %s", (przejazd_id,))
    conn.commit()
    cursor.close()
    return redirect(url_for('admin.przejazdy_polaczenia', connection_id=connection_id))




@admin_bp.route('/polaczenia/<int:connection_id>/przejazdy/<int:przejazd_id>/edytuj', methods=['GET', 'POST'])
def edytuj_przejazd_polaczenia(connection_id,przejazd_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login')) 
      
    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM przejazdy WHERE id_przejazdu=%s""", (przejazd_id,))
    przejazd = cursor.fetchone()

    if request.method == 'POST':
        id_pociagu = request.form.get('id_pociagu')
        data = request.form.get('data_przejazdu')
        stan = request.form.get('stan')
        opoznienie = request.form.get('opoznienie')

        cursor.execute("""
            UPDATE przejazdy SET
                id_pociągu = %s,
                data = %s,
                stan = %s,
                opoznienie = %s
            WHERE id_przejazdu = %s
        """, (id_pociagu, data, stan, opoznienie,przejazd_id))
        
        conn.commit()
        cursor.close()
        return redirect(url_for('admin.przejazdy_polaczenia',connection_id))


    cursor.execute("SELECT id_pociągu, nazwa_modelu,nazwa_przewoznika FROM pociag_szczeg")
    pociagi = cursor.fetchall()

    cursor.close()

    return render_template('admin/edytuj_przejazd_polaczenia.html',
                           connection_id = connection_id,
                           przejazd=przejazd,
                           pociagi=pociagi)