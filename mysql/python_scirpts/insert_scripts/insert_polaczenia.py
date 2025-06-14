import mysql.connector
import random


def insert_polaczenia(amount):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="szkot"
    )
    cursor = conn.cursor()


    cursor.execute("SELECT id_przewoznika FROM przewoznicy;")
    przewoznicy = cursor.fetchall()

    dni_tygodnia = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    weekday_order = {day: i for i, day in enumerate(dni_tygodnia)}

    for _ in range(amount):
        cursor.execute("SELECT id_stacji, miasto FROM stacje_kolejowe ORDER BY RAND() LIMIT 2;")
        two_cities = cursor.fetchall()

        travel_time = f"{random.randint(0, 5)}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"  # HH:MM:SS format

        departure_time = f"{random.randint(0, 23)}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"  # HH:MM:SS format

        price = random.randint(10, 100)

        num_days = random.randint(1, 7)
        days = random.sample(dni_tygodnia, num_days)
        days_sorted = sorted(days, key=lambda d: weekday_order[d])
        days_str = ",".join(days_sorted)

        id_przewoznika = random.choice(przewoznicy)[0]

        query = """
                INSERT INTO polaczenia (id_stacji_początkowej, id_stacji_końcowej,id_przewoznika,czas_przejazdu,godzina_odjazdu,cena , dni_tygodnia)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """
        cursor.execute(query, (two_cities[0][0],two_cities[1][0],id_przewoznika,travel_time,departure_time,price,days_str,))

        conn.commit()

    cursor.close()
    conn.close()
    print("Połaczenia inserted")