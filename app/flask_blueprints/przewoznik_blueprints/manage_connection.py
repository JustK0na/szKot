from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_blueprints.przewoznicy_blueprint import przewoznik_bp,get_db_connection


@przewoznik_bp.route('/polaczenia')
def przewoznik_polaczenia():
    if 'role' not in session or session['role'] != 'przewoznik':
        flash('Brak dostępu')
        return redirect(url_for('przewoznik.login')) 
      

    conn = get_db_connection('przewoznik')
    cursor = conn.cursor()

    id_przewoznika = session.get('user_id')


    cursor.execute("""
        SELECT 
            p.id_połączenia,
            l.nazwa_linii AS nazwa_linii,
            sp.nazwa_stacji AS stacja_początkowa,
            sk.nazwa_stacji AS stacja_końcowa,
            p.id_pociągu,
            po.model_pociągu AS model,
            pr.nazwa as przewoznik,
            p.czas_przejazdu,
            p.godzina_odjazdu,
            p.dni_tygodnia
        FROM polaczenia p
        JOIN linie_kolejowe l ON p.id_lini = l.id_linii
        JOIN stacje_kolejowe sp ON p.id_stacji_początkowej = sp.id_stacji
        JOIN stacje_kolejowe sk ON p.id_stacji_końcowej = sk.id_stacji
        JOIN pociagi po ON p.id_pociągu = po.id_pociągu
        JOIN przewoznicy pr ON po.id_przewoźnika = pr.id_przewoznika
        WHERE po.id_przewoźnika = %s
    """, (id_przewoznika,))

    connections = cursor.fetchall()

    cursor.close()
    return render_template('przewoznik/polaczenia.html', connections=connections)



@przewoznik_bp.route('/polaczenia/<int:connection_id>/edytuj', methods=['GET', 'POST'])
def edytuj_polaczenie(connection_id):
    if 'role' not in session or session['role'] != 'przewoznik':
        flash('Brak dostępu')
        return redirect(url_for('przewoznik.login')) 
      

    conn = get_db_connection('przewoznik')
    cursor = conn.cursor()


    cursor.execute("""
        SELECT * FROM polaczenia WHERE id_połączenia = %s
    """, (connection_id,))
    connection = cursor.fetchone()

    if request.method == 'POST':
        id_linii = request.form.get('id_linii')
        id_stacji_poczatkowej = request.form.get('id_stacji_początkowej')
        id_stacji_koncowej = request.form.get('id_stacji_końcowej')
        id_pociagu = request.form.get('id_pociągu')
        czas_przejazdu = request.form.get('czas_przejazdu')
        godzina_odjazdu = request.form.get('godzina_odjazdu')
        dni_tygodnia = ','.join(request.form.getlist('dni_tygodnia'))  

        cursor.execute("""
            UPDATE polaczenia SET
                id_lini = %s,
                id_stacji_początkowej = %s,
                id_stacji_końcowej = %s,
                id_pociągu = %s,
                czas_przejazdu = %s,
                godzina_odjazdu = %s,
                dni_tygodnia = %s
            WHERE id_połączenia = %s
        """, (id_linii, id_stacji_poczatkowej, id_stacji_koncowej, id_pociagu, czas_przejazdu,
              godzina_odjazdu, dni_tygodnia, connection_id))
        conn.commit()
        cursor.close()
        return redirect(url_for('przewoznik.przewoznik_polaczenia'))

    id_przewoznika = session.get('user_id')

    cursor.execute("SELECT id_stacji, nazwa_stacji FROM stacje_kolejowe ORDER BY nazwa_stacji")
    stacje = cursor.fetchall()

    cursor.execute("SELECT id_pociągu FROM pociagi WHERE id_przewoźnika = %s ORDER BY id_pociągu ", (id_przewoznika,))
    pociagi = cursor.fetchall()

    cursor.execute("SELECT id_linii, nazwa_linii FROM linie_kolejowe ORDER BY nazwa_linii")
    linie = cursor.fetchall()

    cursor.close()
    return render_template('przewoznik/edytuj_polaczenie.html',
                           connection=connection,
                           stacje=stacje,
                           pociagi=pociagi,
                           linie=linie)



@przewoznik_bp.route('/polaczenia/dodaj', methods=['GET', 'POST'])
def dodaj_polaczenie():
    if 'role' not in session or session['role'] != 'przewoznik':
        flash('Brak dostępu')
        return redirect(url_for('przewoznik.login')) 
      

    conn = get_db_connection('admin')
    cursor = conn.cursor()

    if request.method == 'POST':
        id_linii = request.form.get('id_linii')
        id_stacji_poczatkowej = request.form.get('id_stacji_początkowej')
        id_stacji_koncowej = request.form.get('id_stacji_końcowej')
        id_pociagu = request.form.get('id_pociągu')
        czas_przejazdu = request.form.get('czas_przejazdu')
        godzina_odjazdu = request.form.get('godzina_odjazdu')
        dni_tygodnia = ','.join(request.form.getlist('dni_tygodnia'))

        cursor.execute("""
            INSERT INTO polaczenia (
                id_lini, id_stacji_początkowej, id_stacji_końcowej,
                id_pociągu, czas_przejazdu, godzina_odjazdu,
                dni_tygodnia 
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (id_linii, id_stacji_poczatkowej, id_stacji_koncowej, id_pociagu,
              czas_przejazdu, godzina_odjazdu,  dni_tygodnia))
        conn.commit()
        cursor.close()
        return redirect(url_for('przewoznik.przewoznik_polaczenia'))

    id_przewoznika = session.get('user_id')

    cursor.execute("SELECT id_stacji, nazwa_stacji FROM stacje_kolejowe ORDER BY nazwa_stacji")
    stacje = cursor.fetchall()

    cursor.execute("SELECT id_pociągu FROM pociagi WHERE id_przewoźnika = %s ORDER BY id_pociągu", (id_przewoznika,))
    pociagi = cursor.fetchall()

    cursor.execute("SELECT id_linii, nazwa_linii FROM linie_kolejowe ORDER BY nazwa_linii")
    linie = cursor.fetchall()

    cursor.close()

    return render_template('przewoznik/dodaj_polaczenie.html',
                           stacje=stacje,
                           pociagi=pociagi,
                           linie=linie)





@przewoznik_bp.route('/polaczenia/usun/<int:connection_id>', methods=['POST'])
def usun_polaczenie(connection_id):
    if 'role' not in session or session['role'] != 'przewoznik':
        flash('Brak dostępu')
        return redirect(url_for('przewoznik.login')) 
         
    
    conn = get_db_connection('przewoznik')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM polaczenia WHERE id_połączenia = %s", (connection_id,))
    conn.commit()
    cursor.close()

    return redirect(url_for('przewoznik.przewoznik_polaczenia'))
