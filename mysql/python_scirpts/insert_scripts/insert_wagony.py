import mysql.connector
import random


def insert_wagony():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="szkot"
    )

    cursor = conn.cursor()



    wagon_capacity = [30, 50, 70, 100]

    cursor.execute("SELECT id_pociągu FROM pociagi;")
    id_pociagow = [row[0] for row in cursor.fetchall()]

    for id_pociagu in id_pociagow:
        number_of_wagons = random.randint(5, 12)

        for i in range(1,number_of_wagons):
            capacity = random.choice(wagon_capacity)
            query = """
                INSERT INTO wagony (id_pociągu,liczba_miejsc)
                VALUES (%s,%s)
            """
            cursor.execute(query, (id_pociagu,capacity,))

    conn.commit()
    cursor.close()
    conn.close()
    print("Wagony inserted")
