from faker import Faker
import mysql.connector
import random
import hashlib


# Połączenie z MySQL

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()[:16]

def insert_przewoznicy():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="szkot"
    )

    cursor = conn.cursor()
    fake = Faker('pl_PL')


    nazwy_przewoznikow = [
        'PKP Intercity',
        'Koleje Mazowieckie',
        'Polregio',
        'Koleje Dolnośląskie',
        'Koleje Wielkopolskie',
        'Koleje Małopolskie',
        'SKM Trójmiasto',
        'Łódzka Kolej Aglomeracyjna',
        'Koleje Śląskie'
    ]

    def utworz_login(nazwa, idx):
        slug = ''.join(c.lower() for c in nazwa if c.isalnum())
        return slug[:12]

    # haslo do kazdego przewoznika do 123
    for i, nazwa in enumerate(nazwy_przewoznikow, start=1):
        username = utworz_login(nazwa, i)
        haslo_zahashowane = hash_password('123')

        query = """
                INSERT INTO przewoznicy (nazwa, username, haslo) 
                VALUES (%s, %s, %s) \
                """
        cursor.execute(query, (nazwa,username,haslo_zahashowane))



    conn.commit()
    cursor.close()
    conn.close()
    print("Przewoznicy inserted")