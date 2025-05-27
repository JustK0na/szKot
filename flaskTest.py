from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import  random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'szkot'

mysql = MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        imie = request.form['imie']
        nazwisko = request.form['nazwisko']
        email = request.form['email']
        telefon = request.form['telefon']
        password = request.form['password']
        password_hash = str(abs(hash(password)))[:10]

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id_pasażera FROM pasazerowie WHERE mail = %s", (email,))
        if cursor.fetchone():
            flash("Ten emali ma już przypisane konto.")
            return redirect(url_for('register'))

        query = """
                INSERT INTO pasazerowie (imie, nazwisko, mail, telefon, haslo_plain, haslo)
                VALUES (%s, %s, %s, %s, %s, %s) \
                """
        cursor.execute(query, (imie, nazwisko, email, telefon, password, password_hash))
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
    return render_template('search.html', cities=cities, results=results, all_connections=all_connections)


@app.route('/buy_ticket/<int:connection_id>', methods=['POST'])
def buy_ticket(connection_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()

    cena = random.randint(50, 300)
    ulgi = random.choice(["None", "Student", "Senior", "Weteran", "Dziecko"])

    cursor.execute("""
                   INSERT INTO bilety (id_pasażera, id_połączenia, cena, ulgi)
                   VALUES (%s, %s, %s, %s)
                   """, (session['user_id'], connection_id, cena, ulgi))

    mysql.connection.commit()
    cursor.close()
    flash("Bilet zakupiony!")
    return redirect(url_for('bilety'))

@app.route('/bilety')
def bilety():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    query = """
            SELECT b.id_biletu, p.data, p.czas_przejazdu, p.opóźnienie, b.cena, b.ulgi
            FROM bilety b
                     JOIN polaczenia p ON b.id_połączenia = p.id_połączenia
            WHERE b.id_pasażera = %s \
            """
    cursor.execute(query, (session['user_id'],))
    tickets = cursor.fetchall()
    cursor.close()

    return render_template('bilety.html', tickets=tickets)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM pasazerowie WHERE mail=%s AND haslo_plain=%s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('welcome'))
        else:
            flash('Niepoprawny login lub hasło')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('welcome.html', name=session['user_name'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
