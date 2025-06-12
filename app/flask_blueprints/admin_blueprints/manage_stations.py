from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_blueprints.admin_blueprint import admin_bp,get_db_connection

@admin_bp.route('/stacje')
def admin_stacje():
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))

    conn = get_db_connection('admin')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM stacje_kolejowe
    """)
    stations = cursor.fetchall()
    cursor.close()
    return render_template('admin/stacje.html', stations=stations)


@admin_bp.route('/stacje/<int:station_id>/usun', methods=['POST'])
def usun_stacje(station_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))   
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM stacje_kolejowe WHERE id_stacji = %s", (station_id,))
    
    conn.commit()
    cursor.close()
    return redirect(url_for('admin.admin_stacje'))


@admin_bp.route('/stacje/<int:station_id>/edytuj', methods=['GET', 'POST'])
def edytuj_stacje(station_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))   
    
    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM stacje_kolejowe WHERE id_stacji=%s""", (station_id,))
    station = cursor.fetchone()

    if request.method == 'POST':
        nazwa_stacji = request.form.get('nazwa_stacji')
        miasto = request.form.get('miasto')
        
        cursor.execute("""
            UPDATE stacje_kolejowe SET
                nazwa_stacji = %s,
                miasto = %s
            WHERE id_stacji = %s
        """, (nazwa_stacji, miasto, station_id))
        
        conn.commit()
        cursor.close()
        return redirect(url_for('admin.admin_stacje'))

    cursor.close()

    return render_template('admin/edytuj_stacje.html',
                           station=station)




@admin_bp.route('/stacje/dodaj', methods=['GET', 'POST'])
def dodaj_stacje():
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login'))

    conn = get_db_connection('admin')
    cursor = conn.cursor()


    if request.method == 'POST':
        nazwa_stacji = request.form.get('nazwa_stacji')
        miasto = request.form.get('miasto')
        
        cursor.execute("""
            INSERT INTO stacje_kolejowe (
                nazwa_stacji,miasto
            ) VALUES (%s, %s)
        """, (nazwa_stacji, miasto))
        
        conn.commit()
        cursor.close()
        return redirect(url_for('admin.admin_stacje'))

    cursor.close()

    return render_template('admin/dodaj_stacje.html')


