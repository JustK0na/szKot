from flask import Flask, render_template, request, redirect, url_for, session, flash
from common import hash_password
from flask_mysqldb import MySQL 


###########
#TODO:
#    -add pociagi and wagony to admin powers
#    -add some admin powers to panel przewoznika
#    -make admin access to admin powers secure
###########

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
#app.config['MYSQL_HOST'] = 'db' #Docker 
app.config['MYSQL_USER'] = 'root' #host
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'szkot'
app.config['MYSQL_PORT'] = 3306


mysql = MySQL(app)

from flask_blueprints.admin_blueprint import admin_bp
from flask_blueprints.user_blueprint import user_bp

app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)



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
            return redirect(url_for('user.welcome'))
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



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
