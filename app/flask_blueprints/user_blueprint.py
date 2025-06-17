from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from common import random,hash_password,get_db_connection,MySQLdb

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection('auth')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM pasazerowie WHERE mail=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        if user and user[5] == hash_password(password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('user.welcome'))
        else:
            flash('Niepoprawny login lub hasło')
            return redirect(url_for('user.login'))
        
    return render_template('login.html')


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        imie = request.form['imie']
        nazwisko = request.form['nazwisko']
        email = request.form['email']
        telefon = request.form['telefon']
        password = request.form['password']

        password_hash = hash_password(password)

        conn = get_db_connection('auth')
        cursor = conn.cursor()

        cursor.execute("SELECT id_pasażera FROM pasazerowie WHERE mail = %s", (email,))
        if cursor.fetchone():
            flash("Ten emali ma już przypisane konto.")
            return redirect(url_for('user.register'))
        

        try:
            query = """
                    INSERT INTO pasazerowie (imie, nazwisko, mail, telefon, haslo)
                    VALUES (%s, %s, %s, %s, %s) \
                    """
            cursor.execute(query, (imie, nazwisko, email, telefon, password_hash))
            conn.commit()
            cursor.close()
            ("Rejestracja zakończona. Zaloguj się.")
            return redirect(url_for('user.login'))
        except MySQLdb.Error as e:
            conn.rollback()
            flash(f"Błąd MySQL: {e.args[1]}")


        cursor.close()
        
    return render_template('register.html')





@user_bp.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))

    conn = get_db_connection('pasazer')
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT miasto FROM stacje_kolejowe ORDER BY miasto ASC")
    cities = [row[0] for row in cursor.fetchall()]

    results = []
    all_connections = []

    cursor.execute("""
        SELECT id_przejazdu, nazwa_stacji_początkowej, nazwa_stacji_końcowej, godzina_odjazdu,data , czas_przejazdu, cena
        FROM przejazd_szczeg WHERE stan = "Zaplanowany"
        ORDER BY data ASC, godzina_odjazdu ASC
    """)
    all_connections = cursor.fetchall()

    cursor.close()
    return render_template('user/search.html', cities=cities, results=results, all_connections=all_connections)


@user_bp.route('/buy_ticket/<int:connection_id>', methods=['GET', 'POST'])
def buy_ticket(connection_id):
    if 'user_id' not in session:
        return redirect(url_for('user.login'))

    conn = get_db_connection('pasazer')
    cursor = conn.cursor()

    if request.method == 'POST':
        selected_discount = request.form['ulga']


        cursor.execute("""
        SELECT cena
        FROM przejazd_szczeg
        WHERE id_przejazdu = %s
    """, (connection_id,))
        cena = cursor.fetchone()


        cursor.execute("""
            INSERT INTO bilety (id_pasażera, id_przejazdu, cena, ulgi)
            VALUES (%s, %s, %s, %s)
        """, (session['user_id'], connection_id, cena, selected_discount))

        conn.commit()
        cursor.close()
        flash("Bilet zakupiony!")
        return redirect(url_for('user.bilety'))

    cursor.execute("""
        SELECT id_przejazdu, nazwa_stacji_początkowej, nazwa_stacji_końcowej, czas_przejazdu, godzina_odjazdu, data,
               nazwa_modelu, nazwa_przewoznika, id_pociągu,cena
        FROM przejazd_szczeg
        WHERE id_przejazdu = %s
    """, (connection_id,))

    connection = cursor.fetchone()
    cursor.close()

    ulgi = ["Brak", "Student", "Senior", "Weteran", "Dziecko"]
    return render_template('user/kupBilet.html', connection=connection, ulgi=ulgi)




@user_bp.route('/bilety')
def bilety():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))

    conn = get_db_connection('pasazer')
    cursor = conn.cursor()

    query = """
            SELECT
            p.nazwa_stacji_początkowej, 
            p.nazwa_stacji_końcowej,
            b.id_biletu,          
            p.godzina_odjazdu, 
            p.data, 
            p.czas_przejazdu, 
            b.cena, 
            b.ulgi
            FROM bilety b
            JOIN przejazd_szczeg p ON b.id_przejazdu = p.id_przejazdu
            WHERE b.id_pasażera = %s AND p.stan ="Zaplanowany" \
            ORDER BY data ASC, godzina_odjazdu ASC
            """
    cursor.execute(query, (session['user_id'],))
    tickets_planned = cursor.fetchall()

    query = """
            SELECT
            p.nazwa_stacji_początkowej, 
            p.nazwa_stacji_końcowej,
            b.id_biletu,             
            p.godzina_odjazdu, 
            p.data, 
            p.czas_przejazdu, 
            b.cena, 
            b.ulgi
            FROM bilety b
            JOIN przejazd_szczeg p ON b.id_przejazdu = p.id_przejazdu
            WHERE b.id_pasażera = %s AND p.stan !="Zaplanowany" \
            ORDER BY data ASC, godzina_odjazdu ASC
            """
    cursor.execute(query, (session['user_id'],))
    tickets_done = cursor.fetchall()


    cursor.close()

    return render_template('user/bilety.html', tickets_planned=tickets_planned,tickets_done=tickets_done)

@user_bp.route('/bilety/<int:bilet_id>')
def bilety_szczegol(bilet_id):
    if 'user_id' not in session:
        return redirect(url_for('user.login'))

    conn = get_db_connection('pasazer')
    cursor = conn.cursor()

    query = """
            SELECT
            b.id_biletu,
            b.cena,
            b.ulgi,
            p.czas_przejazdu,
            p.godzina_odjazdu, 
            p.data,
            p.nazwa_stacji_początkowej, 
            p.nazwa_stacji_końcowej,
            p.nazwa_modelu, 
            p.id_pociągu,
            p.nazwa_przewoznika
            FROM bilety b
            JOIN przejazd_szczeg p ON b.id_przejazdu = p.id_przejazdu
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

