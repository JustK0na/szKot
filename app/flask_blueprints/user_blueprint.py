from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import mysql

user_bp = Blueprint('user', __name__)

@user_bp.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT DISTINCT miasto FROM stacje_kolejowe ORDER BY miasto ASC")
    cities = [row[0] for row in cursor.fetchall()]

    results = []
    all_connections = []

    if request.method == 'POST':
        from_city = request.form['from_city']
        to_city = request.form['to_city']

        query = """
                SELECT p.id_połączenia, s1.miasto, s2.miasto, p.data, p.czas_przejazdu, p.opóźnienie
                FROM polaczenia p
                         JOIN stacje_kolejowe s1 ON p.id_stacji_początkowej = s1.id_stacji
                         JOIN stacje_kolejowe s2 ON p.id_stacji_końcowej = s2.id_stacji
                WHERE s1.miasto = %s AND s2.miasto = %s
                """
        cursor.execute(query, (from_city, to_city))
        results = cursor.fetchall()

    # Fetch all connections (for the scrollable list)
    cursor.execute("""
        SELECT p.id_połączenia, s1.miasto, s2.miasto, p.data, p.czas_przejazdu, p.opóźnienie
        FROM polaczenia p
                 JOIN stacje_kolejowe s1 ON p.id_stacji_początkowej = s1.id_stacji
                 JOIN stacje_kolejowe s2 ON p.id_stacji_końcowej = s2.id_stacji
        ORDER BY p.data ASC
    """)
    all_connections = cursor.fetchall()

    cursor.close()
    return render_template('user/search.html', cities=cities, results=results, all_connections=all_connections)


@user_bp.route('/buy_ticket/<int:connection_id>', methods=['GET', 'POST'])
def buy_ticket(connection_id):
    if 'user_id' not in session:
        return redirect(url_for('user.login'))

    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        selected_discount = request.form['ulga']
        cena = random.randint(50, 300)

        cursor.execute("""
            INSERT INTO bilety (id_pasażera, id_połączenia, cena, ulgi)
            VALUES (%s, %s, %s, %s)
        """, (session['user_id'], connection_id, cena, selected_discount))

        mysql.connection.commit()
        cursor.close()
        flash("Bilet zakupiony!")
        return redirect(url_for('user.bilety'))

    # jeśli GET — wyświetl stronę z danymi
    cursor.execute("""
        SELECT p.id_połączenia, s1.miasto, s2.miasto, p.data, p.czas_przejazdu, p.opóźnienie,
               poc.model_pociągu, prz.nazwa, poc.id_pociągu
        FROM polaczenia p
        JOIN stacje_kolejowe s1 ON p.id_stacji_początkowej = s1.id_stacji
        JOIN stacje_kolejowe s2 ON p.id_stacji_końcowej = s2.id_stacji
        JOIN pociagi poc ON p.id_pociągu = poc.id_pociągu
        JOIN przewoznicy prz ON poc.id_przewoźnika = prz.id_przewoznika
        WHERE p.id_połączenia = %s
    """, (connection_id,))
    connection = cursor.fetchone()
    cursor.close()

    ulgi = ["Brak", "Student", "Senior", "Dziecko", "Weteran"]
    return render_template('user/kupBilet.html', connection=connection, ulgi=ulgi)


@user_bp.route('/bilety')
def bilety():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))

    cursor = mysql.connection.cursor()
    query = """
            SELECT s1.miasto AS stacja_początkowa, s2. miasto AS stacja_docelowa ,b.id_biletu, p.data, p.czas_przejazdu, p.opóźnienie, b.cena, b.ulgi
            FROM bilety b
                     JOIN polaczenia p ON b.id_połączenia = p.id_połączenia
                     JOIN stacje_kolejowe s1 ON p.id_stacji_początkowej = s1.id_stacji
                     JOIN stacje_kolejowe s2 ON p.id_stacji_końcowej = s2.id_stacji
            WHERE b.id_pasażera = %s \
            ORDER BY p.data DESC
            """
    cursor.execute(query, (session['user_id'],))
    tickets = cursor.fetchall()
    cursor.close()

    return render_template('user/bilety.html', tickets=tickets)

@user_bp.route('/bilety/<int:bilet_id>')
def bilety_szczegol(bilet_id):
    if 'user_id' not in session:
        return redirect(url_for('user.login'))

    cursor = mysql.connection.cursor()
    query = """
            SELECT b.id_biletu, b.cena, b.ulgi, p.data, p.czas_przejazdu, p.opóźnienie, 
            s1.nazwa_stacji AS stacja_początkowa, 
            s2.nazwa_stacji AS stacja_docelowa,
            po.model_pociągu, po.id_pociągu,
            prz.nazwa AS przewoznik
            FROM bilety b
            JOIN polaczenia p ON b.id_połączenia = p.id_połączenia
            JOIN stacje_kolejowe s1 ON p.id_stacji_początkowej = s1.id_stacji
            JOIN stacje_kolejowe s2 ON p.id_stacji_końcowej = s2.id_stacji
            JOIN pociagi po ON p.id_pociągu = po.id_pociągu
            JOIN przewoznicy prz ON po.id_przewoźnika = prz.id_przewoznika
            WHERE b.id_biletu = %s AND b.id_pasażera = %s
            """
    cursor.execute(query, (bilet_id, session['user_id']))
    ticket = cursor.fetchone()
    cursor.close()
    if not ticket:
        flash("Bilet nie istnieje lub nie jest przypisany do Twojego konta.")
        return redirect(url_for('user.bilety'))
    return render_template('user/biletSzczegoly.html', bilet=ticket)
    


@user_bp.route('/welcome')
def welcome():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    return render_template('user/welcome.html', name=session['user_name'])

@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.login'))

