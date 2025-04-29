from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'szkot'

mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from bilety limit 10')
    bilety = cursor.fetchall()
    cursor.close()
    return render_template('index.html', biletyhtml=bilety)

if __name__ == '__main__':
    app.run(debug=True)