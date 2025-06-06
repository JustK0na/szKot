from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL

import hashlib
import  random


###########
#TODO:
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
app.config['MYSQL_USER'] = 'root'
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


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('admin/admin.html')


@app.route('/admin/pasazerowie')
def admin_pasazerowie():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_pasażera, imie, nazwisko, mail, telefon, haslo FROM pasazerowie")
    passengers = cursor.fetchall()
    cursor.close()
    return render_template('admin/pasazerowie.html', passengers=passengers)


@app.route('/admin/pasazerowie/<int:id_pasazer>/bilety')
def pokaz_bilety_pasazera(id_pasazer):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_biletu, id_pasażera, id_połączenia, cena, ulgi FROM bilety WHERE id_pasażera = %s", (id_pasazer,))
    tickets = cursor.fetchall()

    cursor.execute("SELECT imie, nazwisko FROM pasazerowie WHERE id_pasażera = %s", (id_pasazer,))
    passenger = cursor.fetchone()

    cursor.close()
    return render_template('admin/bilety_pasazera.html', tickets=tickets, passenger=passenger, id_pasazer=id_pasazer)


@app.route('/admin/pasazerowie/<int:id_pasazer>/bilety/<int:bilet_id>/usun', methods=['POST'])
def usun_bilet(id_pasazer, bilet_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM bilety WHERE id_biletu = %s", (bilet_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('pokaz_bilety_pasazera', id_pasazer=id_pasazer))



@app.route('/admin/pasazerowie/<int:id_pasazer>/bilety/<int:bilet_id>/edytuj', methods=['POST'])
def edytuj_bilet(id_pasazer, bilet_id):
    cena = request.form.get('cena')
    ulga = request.form.get('ulga')  # teraz string, np. "Student"

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE bilety SET cena = %s, ulgi = %s WHERE id_biletu = %s
    """, (cena, ulga, bilet_id))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('pokaz_bilety_pasazera', id_pasazer=id_pasazer))




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
