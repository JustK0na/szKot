import pymysql
import time
import random
from datetime import datetime, timedelta, time as dt_time
import calendar



DB_CONFIG = {
    'host': 'db',  
    'user': 'root',
    'password': 'root',
    'database': 'szkot',
    'cursorclass': pymysql.cursors.DictCursor # te kursory strasznie ułatwiają życie z mysqldictionary 
}                                              # trzeba bylo ich używać w projeckie bo to oszcedza kilkanascie godzin roboty :d

CHECK_INTERVAL = 300  # 5 minut

def get_connection():
    return pymysql.connect(**DB_CONFIG)

def timedelta_to_time(td):
    total_seconds = int(td.total_seconds())
    hours = (total_seconds // 3600) % 24
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return dt_time(hour=hours, minute=minutes, second=seconds)


def update_przejazdy():
    print(f"[{datetime.now()}] Checking and updating przejazdy")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.id_przejazdu, p.data, p.godzina_odjazdu, pol.czas_przejazdu, p.stan
        FROM przejazd_szczeg p
        JOIN polaczenia pol ON p.id_połączenia = pol.id_połączenia
        WHERE p.stan IN ('Zaplanowany')
    """)
    przejazdy = cursor.fetchall()

    now = datetime.now()

    for p in przejazdy:
        godzina_odjazdu = p['godzina_odjazdu']
        if isinstance(godzina_odjazdu, timedelta):
            godzina_odjazdu = timedelta_to_time(godzina_odjazdu)

        datagodzina_odjazdu = datetime.combine(p['data'], godzina_odjazdu)

        czas_przejazdu = p['czas_przejazdu']

        if not isinstance(czas_przejazdu, timedelta):
            czas_przejazdu = timedelta()

        datagodzina_przyjazdu = datagodzina_odjazdu + czas_przejazdu

        if now >= datagodzina_przyjazdu:
            if random.choice([True, False]):
                cursor.execute("""
                    UPDATE przejazdy SET stan = 'Zakończony', opoznienie = NULL WHERE id_przejazdu = %s
                """, (p['id_przejazdu'],))
                print(f"Przejazd {p['id_przejazdu']} zakończony.")
            else:
                delay_minuty = random.randint(5, 60)
                delay = timedelta(minutes=delay_minuty)
                cursor.execute("""
                    UPDATE przejazdy SET stan = 'Opóźniony', opoznienie = %s WHERE id_przejazdu = %s
                """, (str(delay), p['id_przejazdu']))
                print(f"Przejazd {p['id_przejazdu']} opóźniony o {delay_minuty} minut.")

    conn.commit()
    cursor.close()
    conn.close()


def insert_przejazdy():
    print(f"[{datetime.now()}] Inserting new przejazdy")
    for i in range(30):
        date = datetime.today().date() + timedelta(days=i)
        date_name = calendar.day_name[date.weekday()]  

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM polaczenia")
        polaczenia = cursor.fetchall()

        for pol in polaczenia:
            dni = pol['dni_tygodnia']
            if dni is None:
                continue

            dni_lista = [d.strip() for d in dni.split(',')]

            if date_name not in dni_lista:
                continue

            cursor.execute("""
                SELECT COUNT(*) AS count FROM przejazdy
                WHERE id_połączenia = %s AND data = %s
            """, (pol['id_połączenia'], date))
            count = cursor.fetchone()['count']

            if count == 0:
                cursor.execute("""
                    SELECT id_pociągu FROM pociagi WHERE id_przewoźnika = %s ORDER BY RAND() LIMIT 1
                """, (pol['id_przewoznika'],))
                pociag = cursor.fetchone()
                if pociag:
                    cursor.execute("""
                        INSERT INTO przejazdy (id_połączenia, id_pociągu, data, stan)
                        VALUES (%s, %s, %s, 'Zaplanowany')
                    """, (pol['id_połączenia'], pociag['id_pociągu'], date))
                    print(f"Dodano nowy przejazd dla połączenia {pol['id_połączenia']}.")

        conn.commit()
        cursor.close()
        conn.close()


print("Update script running")
while True:
    try:
        update_przejazdy()
        insert_przejazdy()
        update_przejazdy()
        
    except Exception as e:
       print(f"Błąd: {e}")
    
    print(f"[{datetime.now()}] Update script done. Next update in 5 minutes.")
    time.sleep(CHECK_INTERVAL)