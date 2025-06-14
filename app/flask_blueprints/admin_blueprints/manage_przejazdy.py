from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_blueprints.admin_blueprint import admin_bp,get_db_connection,MySQLdb

@admin_bp.route('/przejazdy')
def admin_przejazdy():
    if 'role' not in session or session['role'] != 'admin':
        flash('Brak dostępu')
        return redirect(url_for('admin.login')) 

    conn = get_db_connection('admin')
    cursor = conn.cursor()

    cursor.execute("""SELECT id_przejazdu,
                   data,
                   godzina_odjazdu,
                   czas_przejazdu,
                   cena,
                   opoznienie,
                   nazwa_stacji_początkowej,
                   nazwa_stacji_końcowej,
                   nazwa_przewoznika,
                   nazwa_modelu,
                   id_pociągu,
                   stan
                FROM przejazd_szczeg """)

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


#jak na razie nie robie edycji id_polaczenia
# nie ma to sensu, latwiej usunac przejazd i zrobic nowy jak sie ktos pomyli
# dlatego dodwanie przejazdu da sie rowniez przy polaczeniach dla wiekszej klarownosci
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
        id_pociagu = request.form.get('id_pociagu')
        data = request.form.get('data_przejazdu')
        stan = request.form.get('stan')
        opoznienie = request.form.get('opoznienie')

        try:
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
            return redirect(url_for('admin.admin_przejazdy'))
        except MySQLdb.Error as e:
                conn.rollback()
                flash(f"Błąd MySQL: {e.args[1]}")


    cursor.execute("SELECT id_pociągu, nazwa_modelu,nazwa_przewoznika FROM pociag_szczeg")
    pociagi = cursor.fetchall()

    cursor.close()

    return render_template('admin/edytuj_przejazd.html',
                           przejazd=przejazd,
                           pociagi=pociagi)






