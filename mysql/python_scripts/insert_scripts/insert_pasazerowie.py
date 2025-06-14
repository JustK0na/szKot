from faker import Faker
import mysql.connector
import random
import hashlib

# Połączenie z MySQL



def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()[:16]

def insert_pasazerowie(amount):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="szkot"
    )

    cursor = conn.cursor()
    fake = Faker('pl_PL')


    for _ in range(amount):
        first = fake.first_name()
        last = fake.last_name()
        email = fake.unique.email()
        phone = fake.phone_number()
        password_hash = hash_password("123")

        query = """
                INSERT INTO pasazerowie (imie, nazwisko, mail, telefon, haslo)
                VALUES (%s, %s, %s, %s, %s) \
                """
        cursor.execute(query, (first, last, email, phone, password_hash))


    conn.commit()
    cursor.close()
    conn.close()
    print("Pasażerowie inserted")