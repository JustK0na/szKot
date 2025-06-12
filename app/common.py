from flask import Flask, render_template, request, redirect, url_for, session, flash,current_app
from flask_mysqldb import MySQL
import MySQLdb

import hashlib
import  random


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()[:16] 



#function to get db connection by some user
#it makes it so we don't have to use root on everything
def get_db_connection(role):
    config = {
        'admin': {
            'user': 'admin_user',
            'password': 'admin_pass'
        },
        'carrier': {
            'user': 'przewoznik_user',
            'password': 'przewoznik_pass'
        },
        'pasazer': {
            'user': 'pasazer_user',
            'password': 'pasazer_pass'
        },
        'auth': {
            'user': 'auth_user',
            'password': 'auth_pass'
        }
    }

    creds = config[role]
    return MySQLdb.connect(
        host=current_app.config['MYSQL_HOST'],
        user=creds['user'],
        password=creds['password'],
        db=current_app.config['MYSQL_DB'],
        port=current_app.config['MYSQL_PORT'],
        charset='utf8mb4'
    )
