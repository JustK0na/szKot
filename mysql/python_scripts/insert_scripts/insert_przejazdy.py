import mysql.connector
import random
from datetime import datetime, timedelta
import numpy as np

# Mapowanie nazw dni tygodnia na ich numery
dni_map = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6
}

# Funkcja generująca losowe daty przypadające na dany dzień tygodnia
def generuj_daty_dla_dnia_tygodnia(dzien_tygodnia, ile):
    today = datetime.today()
    dzien_num = dni_map[dzien_tygodnia]
    daty = []

    # Szukamy dat w promieniu +/-14 dni od dziś
    for i in range(-14,-1):
        kandydat = today + timedelta(days=i)
        if kandydat.weekday() == dzien_num:
            daty.append(kandydat.date())

    return random.sample(daty, min(ile, len(daty)))

def insert_przejazdy():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="szkot"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT id_połączenia, dni_tygodnia, id_przewoznika FROM polaczenia;")
    polaczenia = cursor.fetchall()

    for id_polaczenia, dni, id_przewoznika in polaczenia:
        number_of_przejazds = random.randint(1, 12)

        if isinstance(dni, str):
            dni_lista = dni.split(',')
        else:
            dni_lista = list(dni) if isinstance(dni, set) else [str(dni)]

        for dzien in dni_lista:
            dzien = dzien.strip()
            daty = generuj_daty_dla_dnia_tygodnia(dzien, number_of_przejazds)

            for data in daty:
                # Wybierz losowy pociąg danego przewoźnika
                cursor.execute(
                    "SELECT id_pociągu FROM pociagi WHERE id_przewoźnika = %s ORDER BY RAND() LIMIT 1",
                    (id_przewoznika,)
                )
                wynik = cursor.fetchone()
                if not wynik:
                    continue  
                id_pociagu = wynik[0]

                if data > datetime.today().date():
                    stan = 'Zaplanowany'
                    opoznienie = None
                else:
                    stan = random.choices(
                        ['Zakończony', 'Opóźniony', 'Anulowany'],
                        weights=[0.6, 0.3, 0.1]
                    )[0]

                    if stan == 'Opóźniony':
                        opoznienie_minuty = int(max(0, np.random.normal(15, 10)))  # opóźnienie ~N(15, 10)
                        godziny = opoznienie_minuty // 60
                        minuty = opoznienie_minuty % 60
                        opoznienie = f"{godziny:02d}:{minuty:02d}:00"
                    else:
                        opoznienie = None

                # Wstaw do tabeli przejazdy
                query = """
                    INSERT INTO przejazdy (id_połączenia, id_pociągu, data, stan, opoznienie)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (id_polaczenia, id_pociagu, data, stan, opoznienie))

    # Zatwierdź zmiany
    conn.commit()
    cursor.close()
    conn.close()
    print("Przejazdy inserted")
