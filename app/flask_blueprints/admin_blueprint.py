from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import mysql

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('admin/admin.html')


@admin_bp.route('/pasazerowie')
def admin_pasazerowie():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_pasażera, imie, nazwisko, mail, telefon, haslo FROM pasazerowie")
    users = cursor.fetchall()
    cursor.close()
    return render_template('admin/pasazerowie.html', users=users)


@admin_bp.route('/pasazerowie/<int:user_id>/bilety')
def pokaz_bilety_pasazera(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_biletu, id_pasażera, id_połączenia, cena, ulgi FROM bilety WHERE id_pasażera = %s", (user_id,))
    tickets = cursor.fetchall()

    cursor.execute("SELECT imie, nazwisko FROM pasazerowie WHERE id_pasażera = %s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    return render_template('admin/bilety_pasazera.html', tickets=tickets, user=user, user_id=user_id)


@admin_bp.route('/pasazerowie/<int:user_id>/bilety/<int:ticket_id>/usun', methods=['POST'])
def usun_bilet(user_id, ticket_id):   
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM bilety WHERE id_biletu = %s", (ticket_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('admin.pokaz_bilety_pasazera', user_id=user_id))

@admin_bp.route('/pasazerowie/<int:user_id>/bilety/<int:ticket_id>/edytuj', methods=['POST'])
def edytuj_bilet(user_id, ticket_id):
    cena = request.form.get('cena')
    ulga = request.form.get('ulga') 

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE bilety SET cena = %s, ulgi = %s WHERE id_biletu = %s
    """, (cena, ulga, ticket_id))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('admin.pokaz_bilety_pasazera', user_id=user_id))

@admin_bp.route('/pasazerowie/<int:user_id>', methods=['GET', 'POST'])
def edytuj_pasazera(user_id):   
    cursor = mysql.connection.cursor()

    cursor.execute("""SELECT * FROM pasazerowie WHERE id_pasażera=%s""", (user_id,))
    user = cursor.fetchall()

    if request.method == 'POST':
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
        
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('admin.admin_pasazerowie'))


    cursor.close()

    return render_template('admin/edytuj_pasazera.html',
                           user=user,)




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





