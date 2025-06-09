from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL

import hashlib
import  random


###########
#TODO:
#    - podzielić na pałe plików bo kongo sie robi w tym pliku
#    -add edytuj użytkownika
#    -add all admin powers to panel admina
#    -add some admin powers to panel przewoznika
###########
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()[:16] 


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
#app.config['MYSQL_HOST'] = 'db' #Docker 
app.config['MYSQL_USER'] = 'root' #host
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'szkot'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM pasazerowie WHERE mail=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        if user and user[5] == hash_password(password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('welcome'))
        else:
            flash('Niepoprawny login lub hasło')
            return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        imie = request.form['imie']
        nazwisko = request.form['nazwisko']
        email = request.form['email']
        telefon = request.form['telefon']
        password = request.form['password']

        password_hash = hash_password(password)

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id_pasażera FROM pasazerowie WHERE mail = %s", (email,))
        if cursor.fetchone():
            flash("Ten emali ma już przypisane konto.")
            return redirect(url_for('register'))

        query = """
                INSERT INTO pasazerowie (imie, nazwisko, mail, telefon, haslo)
                VALUES (%s, %s, %s, %s, %s) \
                """
        cursor.execute(query, (imie, nazwisko, email, telefon, password_hash))
        mysql.connection.commit()
        cursor.close()
        flash("Rejestracja zakończona. Zaloguj się.")
        return redirect(url_for('login'))
    return render_template('register.html')



@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))

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


@app.route('/buy_ticket/<int:connection_id>', methods=['GET', 'POST'])
def buy_ticket(connection_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

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
        return redirect(url_for('bilety'))

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


@app.route('/bilety')
def bilety():
    if 'user_id' not in session:
        return redirect(url_for('login'))

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

@app.route('/bilety/<int:bilet_id>')
def bilety_szczegol(bilet_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

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
        return redirect(url_for('bilety'))
    return render_template('user/biletSzczegoly.html', bilet=ticket)
    


@app.route('/welcome')
def welcome():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('user/welcome.html', name=session['user_name'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


######
#ADMIN
######


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('admin/admin.html')


@app.route('/admin/pasazerowie')
def admin_pasazerowie():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_pasażera, imie, nazwisko, mail, telefon, haslo FROM pasazerowie")
    users = cursor.fetchall()
    cursor.close()
    return render_template('admin/pasazerowie.html', users=users)


@app.route('/admin/pasazerowie/<int:user_id>/bilety')
def pokaz_bilety_pasazera(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_biletu, id_pasażera, id_połączenia, cena, ulgi FROM bilety WHERE id_pasażera = %s", (user_id,))
    tickets = cursor.fetchall()

    cursor.execute("SELECT imie, nazwisko FROM pasazerowie WHERE id_pasażera = %s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    return render_template('admin/bilety_pasazera.html', tickets=tickets, user=user, user_id=user_id)


@app.route('/admin/pasazerowie/<int:user_id>/bilety/<int:ticket_id>/usun', methods=['POST'])
def usun_bilet(user_id, ticket_id):   
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM bilety WHERE id_biletu = %s", (ticket_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('pokaz_bilety_pasazera', user_id=user_id))

@app.route('/admin/pasazerowie/<int:user_id>/bilety/<int:ticket_id>/edytuj', methods=['POST'])
def edytuj_bilet(user_id, ticket_id):
    cena = request.form.get('cena')
    ulga = request.form.get('ulga') 

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE bilety SET cena = %s, ulgi = %s WHERE id_biletu = %s
    """, (cena, ulga, ticket_id))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('pokaz_bilety_pasazera', user_id=user_id))

@app.route('/admin/pasazerowie/<int:user_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('admin_pasazerowie'))


    cursor.close()

    return render_template('admin/edytuj_pasazera.html',
                           user=user,)




@app.route('/admin/polaczenia')
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


@app.route('/admin/polaczenia/<int:connection_id>/edytuj', methods=['GET', 'POST'])
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
        return redirect(url_for('admin_polaczenia'))

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


@app.route('/admin/polaczenia/dodaj', methods=['GET', 'POST'])
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
        return redirect(url_for('admin_polaczenia'))

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







if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
