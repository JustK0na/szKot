from faker import Faker
import mysql.connector
import random


def insert_pociagi(amount):
    conn = mysql.connector.connect(host="localhost",user="root",password="root",database="szkot")

    cursor = conn.cursor()
    fake = Faker('pl_PL')



    cursor.execute("SELECT id_modelu FROM modele_pociagow;")
    modele_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id_przewoznika, nazwa FROM przewoznicy;")
    przewoznicy = cursor.fetchall()


    for _ in range(amount):
        id_modelu = random.choice(modele_ids)
        id_przewoznika, nazwa_przewoznika = random.choice(przewoznicy)

        query = """
                INSERT INTO pociagi (id_modelu, id_przewoźnika)
                VALUES (%s, %s)
                """
        cursor.execute(query, (id_modelu, id_przewoznika))

    conn.commit()
    cursor.close()
    conn.close()
    print("Pociagi inserted")