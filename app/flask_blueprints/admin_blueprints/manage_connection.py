from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import mysql
from flask_blueprints.admin_blueprint import admin_bp


@admin_bp.route('/polaczenia')
def admin_polaczenia():
    cursor = mysql.connection.cursor()
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
        p.data,
        p.opóźnienie
    FROM polaczenia p
    JOIN linie_kolejowe l ON p.id_lini = l.id_linii
    JOIN stacje_kolejowe sp ON p.id_stacji_początkowej = sp.id_stacji
    JOIN stacje_kolejowe sk ON p.id_stacji_końcowej = sk.id_stacji
    JOIN pociagi po ON p.id_pociągu = po.id_pociągu
    JOIN przewoznicy pr ON po.id_przewoźnika = pr.id_przewoznika;
    """)
    connections = cursor.fetchall()

    cursor.close()
    return render_template('admin/polaczenia.html', connections=connections)



@admin_bp.route('/polaczenia/<int:connection_id>/edytuj', methods=['GET', 'POST'])
def edytuj_polaczenie(connection_id):
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        cursor.execute("""
            SELECT id_lini FROM polaczenia WHERE id_połączenia = %s
        """, (connection_id,))
        

        id_linii = request.form.get('id_linii')
        id_stacji_poczatkowej = request.form.get('id_stacji_początkowej')
        id_stacji_koncowej = request.form.get('id_stacji_końcowej')
        id_pociagu = request.form.get('id_pociągu')
        czas_przejazdu = request.form.get('czas_przejazdu')
        data = request.form.get('data')
        opoznienie = request.form.get('opóźnienie')

        cursor.execute("""
            UPDATE polaczenia SET
                id_lini = %s,
                id_stacji_początkowej = %s,
                id_stacji_końcowej = %s,
                id_pociągu = %s,
                czas_przejazdu = %s,
                data = %s,
                opóźnienie = %s
            WHERE id_połączenia = %s
        """, (id_linii, id_stacji_poczatkowej, id_stacji_koncowej, id_pociagu, czas_przejazdu, data, opoznienie, connection_id))
        
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('admin.admin_polaczenia'))

    cursor.execute("""
        SELECT id_połączenia, id_lini, id_stacji_początkowej, id_stacji_końcowej, id_pociągu, czas_przejazdu, data, opóźnienie 
        FROM polaczenia WHERE id_połączenia = %s
    """, (connection_id,))
    connection = cursor.fetchone()


    cursor.execute("SELECT id_stacji, nazwa_stacji FROM stacje_kolejowe ORDER BY nazwa_stacji")
    stacje = cursor.fetchall()


    cursor.execute("SELECT id_pociągu FROM pociagi ORDER BY id_pociągu")
    pociagi = cursor.fetchall()


    cursor.execute("SELECT id_linii, nazwa_linii FROM linie_kolejowe ORDER BY nazwa_linii")
    linie = cursor.fetchall()

    cursor.close()

    return render_template('admin/edytuj_polaczenie.html',
                           connection=connection,
                           stacje=stacje,
                           pociagi=pociagi,
                           linie=linie)



@admin_bp.route('/polaczenia/dodaj', methods=['GET', 'POST'])
def dodaj_polaczenie():
    cursor = mysql.connection.cursor()

    if request.method == 'POST':

        id_linii = request.form.get('id_linii')
        id_stacji_poczatkowej = request.form.get('id_stacji_początkowej')
        id_stacji_koncowej = request.form.get('id_stacji_końcowej')
        id_pociagu = request.form.get('id_pociągu')
        czas_przejazdu = request.form.get('czas_przejazdu')
        data = request.form.get('data')
        opoznienie = request.form.get('opóźnienie')

        cursor.execute("""
            INSERT INTO polaczenia (
                id_lini, id_stacji_początkowej, id_stacji_końcowej,
                id_pociągu, czas_przejazdu, data, opóźnienie
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (id_linii, id_stacji_poczatkowej, id_stacji_koncowej, id_pociagu, czas_przejazdu, data, opoznienie))
        
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('admin.admin_polaczenia'))

    cursor.execute("SELECT id_stacji, nazwa_stacji FROM stacje_kolejowe ORDER BY nazwa_stacji")
    stacje = cursor.fetchall()


    cursor.execute("SELECT id_pociągu FROM pociagi ORDER BY id_pociągu")
    pociagi = cursor.fetchall()


    cursor.execute("SELECT id_linii, nazwa_linii FROM linie_kolejowe ORDER BY nazwa_linii")
    linie = cursor.fetchall()

    cursor.close()

    return render_template('admin/dodaj_polaczenie.html',
                           stacje=stacje,
                           pociagi=pociagi,
                           linie=linie)





@admin_bp.route('/polaczenia/usun/<int:connection_id>', methods=['POST'])
def usun_polaczenie(connection_id):   
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM polaczenia WHERE id_połączenia = %s", (connection_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('admin.admin_polaczenia'))
