import mysql.connector
import random

ulga_procent = {
    'Brak': 0.0,
    'Student': 0.5,
    'Senior': 0.4,
    'Weteran': 0.3,
    'Dziecko': 0.6
}


def insert_bilety():
    print("Bilety insertion stared. This takes a while")
    ulgi_lista = list(ulga_procent.keys())

    # Połączenie z MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="szkot"
    )
    cursor = conn.cursor()

    # Pobierz wszystkich pasażerów
    cursor.execute("SELECT id_pasażera FROM pasazerowie;")
    pasazerowie = [row[0] for row in cursor.fetchall()]

    # Pobierz wszystkie przejazdy wraz z id_połączenia
    cursor.execute("SELECT id_przejazdu, id_połączenia FROM przejazdy;")
    przejazdy = cursor.fetchall()

    for id_przejazdu, id_polaczenia in przejazdy:
        number_of_pasazers = random.randint(5, 50)
        for _ in range(number_of_pasazers):
            id_pasazera = random.choice(pasazerowie)

            # Pobierz bazową cenę z połączenia
            cursor.execute("SELECT cena FROM polaczenia WHERE id_połączenia = %s", (id_polaczenia,))
            wynik = cursor.fetchone()
            if not wynik:
                continue
            cena_bazowa = float(wynik[0])

            # Losuj ulgę i wylicz cenę
            ulga = random.choice(ulgi_lista)
            znizka = ulga_procent[ulga]
            cena_koncowa = round(cena_bazowa * (1 - znizka), 2)

            # Wstaw do tabeli bilety
            query = """
                INSERT INTO bilety (id_pasażera, id_przejazdu, cena, ulgi)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (id_pasazera, id_przejazdu, cena_koncowa, ulga))

    # Zatwierdzenie zmian
    conn.commit()
    cursor.close()
    conn.close()
    print("Bilety inserted")
