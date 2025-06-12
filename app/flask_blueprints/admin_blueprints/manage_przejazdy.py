from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_blueprints.admin_blueprint import admin_bp,get_db_connection

@admin_bp.route('/przejazdy')
def admin_przejazdy():
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login')) 

    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            pr.id_przejazdu,
            pr.data,
            spocz.nazwa_stacji AS stacja_początkowa,
            skonc.nazwa_stacji AS stacja_końcowa,
            pz.nazwa AS nazwa_przewoznika,
            pz.czas_przejazdu,
            pz.godzina_odjazdu,
            pr.opoznienie
        FROM przejazdy pr
        JOIN polaczenia_przewoznikiem pz ON pr.id_połączenia = pz.id_połączenia
        JOIN stacje_kolejowe spocz ON pz.id_stacji_początkowej = spocz.id_stacji
        JOIN stacje_kolejowe skonc ON pz.id_stacji_końcowej = skonc.id_stacji
        JOIN przewoznicy pzv ON pz.id_przewoznika = pzv.id_przewoznika
    """)

    przejazdy = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin/przejazdy.html', przejazdy=przejazdy)


@admin_bp.route('/przejazdy/<int:przejazd_id>/usun', methods=['POST'])
def usun_przejazd(przejazd_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login')) 
         
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM przejazdy WHERE id_przejazdu = %s", (przejazd_id,))
    conn.commit()
    cursor.close()
    return redirect(url_for('admin.admin_przejazdy'))


@admin_bp.route('/przejazdy/<int:przejazd_id>/edytuj', methods=['GET', 'POST'])
def edytuj_przejazd(przejazd_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login')) 
      
    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM przejazdy WHERE id_przejazdu=%s""", (przejazd_id,))
    przejazd = cursor.fetchone()

    if request.method == 'POST':
        id_polaczenia = request.form.get('id_polaczenia')
        data_przejazdu = request.form.get('data_przejazdu')
        stan = request.form.get('stan')
        opoznienie = request.form.get('opoznienie')

        cursor.execute("""
            UPDATE przejazdy SET
                id_połączenia = %s,
                data_przejazdu = %s,
                stan = %s,
                opoznienie = %s
            WHERE id_przejazdu = %s
        """, (id_polaczenia, data_przejazdu, stan, opoznienie,przejazd_id))
        
        conn.commit()
        cursor.close()
        return redirect(url_for('admin.admin_przejazdy'))


    cursor.execute("SELECT id_przewoznika, nazwa FROM przewoznicy ORDER BY nazwa")
    polaczenia = cursor.fetchall()

    cursor.close()

    return render_template('admin/edytuj_przejazd.html',
                           przejazd=przejazd,
                           polaczenia=polaczenia)




@admin_bp.route('/linie/dodaj', methods=['GET', 'POST'])
def dodaj_linie():

    conn = get_db_connection('admin')
    cursor = conn.cursor()


    if request.method == 'POST':
        nazwa_linii = request.form.get('nazwa_linii')
        id_stacji = request.form.get('id_stacji')
        id_przewoznika = request.form.get('id_przewoznika')
        
        cursor.execute("""
            INSERT INTO linie_kolejowe (
                nazwa_linii,id_stacji, id_przewoznika
            ) VALUES (%s, %s, %s)
        """, (nazwa_linii, id_stacji, id_przewoznika))
        
        conn.commit()
        cursor.close()
        return redirect(url_for('admin.admin_linie'))

    cursor.execute("SELECT id_stacji, nazwa_stacji FROM stacje_kolejowe ORDER BY nazwa_stacji")
    stacje = cursor.fetchall()

    cursor.execute("SELECT id_przewoznika, nazwa FROM przewoznicy ORDER BY nazwa")
    przewoznicy = cursor.fetchall()

    cursor.close()

    return render_template('admin/dodaj_linie.html',
                           stacje=stacje,
                           przewoznicy=przewoznicy)


