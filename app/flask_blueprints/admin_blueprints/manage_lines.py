from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import mysql
from flask_blueprints.admin_blueprint import admin_bp

@admin_bp.route('/linie')
def admin_linie():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT
            l.id_linii,
            l.nazwa_linii,
            s.nazwa_stacji,
            p.nazwa
        FROM linie_kolejowe l
        JOIN stacje_kolejowe s ON l.id_stacji = s.id_stacji
        JOIN przewoznicy p ON l.id_przewoznika = p.id_przewoznika
    """)
    lines = cursor.fetchall()
    cursor.close()
    return render_template('admin/linie.html', lines=lines)


@admin_bp.route('/linie/<int:line_id>/polaczenia')
def pokaz_polaczenia_linii(line_id):
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
        JOIN przewoznicy pr ON po.id_przewoźnika = pr.id_przewoznika
        WHERE p.id_lini = %s
    """, (line_id,))
    connections = cursor.fetchall()
    cursor.close()

    return render_template('admin/polaczenia.html', connections=connections)


@admin_bp.route('/linie/<int:line_id>/usun', methods=['POST'])
def usun_linie(line_id):   
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM polaczenia WHERE id_lini = %s", (line_id,))

    cursor.execute("DELETE FROM linie_kolejowe WHERE id_linii = %s", (line_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('admin.admin_linie'))


@admin_bp.route('/linie/<int:line_id>/edytuj', methods=['GET', 'POST'])
def edytuj_linie(line_id):   
    cursor = mysql.connection.cursor()

    cursor.execute("""SELECT * FROM linie_kolejowe WHERE id_linii=%s""", (line_id,))
    line = cursor.fetchone()

    if request.method == 'POST':
        nazwa_linii = request.form.get('nazwa_linii')
        id_stacji = request.form.get('id_stacji')
        id_przewoznika = request.form.get('id_przewoznika')
        
        cursor.execute("""
            UPDATE linie_kolejowe SET
                nazwa_linii = %s,
                id_stacji = %s,
                id_przewoznika = %s
            WHERE id_linii = %s
        """, (nazwa_linii, id_stacji, id_przewoznika, line_id))
        
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('admin.admin_linie'))

    cursor.execute("SELECT id_stacji, nazwa_stacji FROM stacje_kolejowe ORDER BY nazwa_stacji")
    stacje = cursor.fetchall()

    cursor.execute("SELECT id_przewoznika, nazwa FROM przewoznicy ORDER BY nazwa")
    przewoznicy = cursor.fetchall()

    cursor.close()

    return render_template('admin/edytuj_linie.html',
                           line=line,
                           stacje=stacje,
                           przewoznicy=przewoznicy)




@admin_bp.route('/linie/dodaj', methods=['GET', 'POST'])
def dodaj_linie():   
    cursor = mysql.connection.cursor()


    if request.method == 'POST':
        nazwa_linii = request.form.get('nazwa_linii')
        id_stacji = request.form.get('id_stacji')
        id_przewoznika = request.form.get('id_przewoznika')
        
        cursor.execute("""
            INSERT INTO linie_kolejowe (
                nazwa_linii,id_stacji, id_przewoznika
            ) VALUES (%s, %s, %s)
        """, (nazwa_linii, id_stacji, id_przewoznika))
        
        mysql.connection.commit()
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


