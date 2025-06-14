from faker import Faker
import mysql.connector


def insert_stacje(amount):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="szkot"
    )

    cursor = conn.cursor()
    fake = Faker('pl_PL')




    for _ in range(amount):
        city = fake.city()
        station_name = city + ' Główny'

        cursor.execute("""
            SELECT COUNT(*) FROM stacje_kolejowe
            WHERE nazwa_stacji = %s AND miasto = %s
        """, (station_name, city))

        if cursor.fetchone()[0] == 0:
            query = """
                INSERT INTO `stacje_kolejowe` (nazwa_stacji, miasto)
                VALUES (%s, %s)
            """
            cursor.execute(query, (station_name, city))

    conn.commit()
    cursor.close()
    conn.close()
    print("Stacje kolejowe inserted")