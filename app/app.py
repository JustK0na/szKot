from flask import Flask, render_template, redirect, url_for,  flash


###########
#TODO:
#   -naprawić aplikacje by działała ze zmianami w bazie danych
###########

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
#app.config['MYSQL_HOST'] = 'db' #Docker 
app.config['MYSQL_DB'] = 'szkot'
app.config['MYSQL_PORT'] = 3306


from flask_blueprints.admin_blueprint import admin_bp
from flask_blueprints.user_blueprint import user_bp
from flask_blueprints.przewoznicy_blueprint import przewoznik_bp

app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(przewoznik_bp)



@app.route('/')
def index():
    return redirect(url_for('user.login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
