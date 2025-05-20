from faker import Faker
import mysql.connector
import random

# Połączenie z MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="szkot"
)

cursor = conn.cursor()
fake = Faker('pl_PL')

# Clean all tables before inserting new data
cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
cursor.execute("TRUNCATE TABLE bilety;")
cursor.execute("TRUNCATE TABLE polaczenia;")
cursor.execute("TRUNCATE TABLE pociagi;")
cursor.execute("TRUNCATE TABLE wagony;")
cursor.execute("TRUNCATE TABLE linie_kolejowe;")
cursor.execute("TRUNCATE TABLE przewoznicy;")
cursor.execute("TRUNCATE TABLE stacje_kolejowe;")
cursor.execute("TRUNCATE TABLE pasazerowie;")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

# Ensure columns for passwords exist
cursor.execute("SHOW COLUMNS FROM pasazerowie LIKE 'haslo_plain'")
if not cursor.fetchone():
    cursor.execute("ALTER TABLE pasazerowie ADD COLUMN haslo_plain VARCHAR(100)")

cursor.execute("SHOW COLUMNS FROM pasazerowie LIKE 'haslo'")
if not cursor.fetchone():
    cursor.execute("ALTER TABLE pasazerowie ADD COLUMN haslo VARCHAR(100)")

#########################
#pasazerowie
#########################

for _ in range(10000):
    first = fake.first_name()
    last = fake.last_name()
    email = fake.email()
    phone = fake.phone_number()
    password_plain = fake.password(length=8)
    password_hash = str(abs(hash(password_plain)))[:10]  # simple numeric hash

    query = """
            INSERT INTO pasazerowie (imie, nazwisko, mail, telefon, haslo_plain, haslo)
            VALUES (%s, %s, %s, %s, %s, %s) \
            """
    cursor.execute(query, (first, last, email, phone, password_plain, password_hash))

print("Pasazerowie have been filled")

# ... [rest of the script remains unchanged] ...
#########################
#miasta
#########################

for _ in range(1000):
    city = fake.city()
    station_name = city + ' Główny'

    cursor.execute("""
                   SELECT COUNT(*) FROM stacje_kolejowe
                   WHERE nazwa_stacji = %s AND miasto = %s
                   """, (station_name, city))

    if cursor.fetchone()[0] == 0:
        query = """
                INSERT INTO stacje_kolejowe (nazwa_stacji, miasto)
                VALUES (%s, %s) \
                """
        cursor.execute(query, (station_name, city))

print("Stacje kolejowe have been filled")

carrier_names = [
    "PKP Intercity", "Arriva", "Koleje Mazowieckie", "Koleje Śląskie",
    "Łódzka Kolej Aglomeracyjna", "Przewozy Regionalne",
    "Warszawska Kolej Dojazdowa", "Koleje Wielkopolskie", "Koleje Dolnośląskie"
]

for name in carrier_names:
    cursor.execute("INSERT INTO przewoznicy (nazwa) VALUES (%s)", (name,))

print("Przewoznicy have been filled")

cursor.execute("SELECT id_przewoznika FROM przewoznicy")
przewoznicy_ids = [row[0] for row in cursor.fetchall()]

#########################
#linie
#########################

for _ in range(100):
    cursor.execute("SELECT id_stacji, miasto FROM stacje_kolejowe ORDER BY RAND() LIMIT 2;")
    two_cities = cursor.fetchall()

    for city in two_cities:
        city_id = city[0]
        city_name = "Linia " + city[1]
        przewoznik_id = random.choice(przewoznicy_ids)

        query = """
                INSERT INTO linie_kolejowe (nazwa_linii, id_stacji,id_przewoznika)
                VALUES (%s, %s, %s) \
                """
        cursor.execute(query, (city_name, city_id, przewoznik_id))

print("Linie have been filled")

#########################
# Wagony
#########################

wagon_capacity = [30, 50, 70, 100]

for _ in range(100):
    capacity = random.choice(wagon_capacity)
    query = """
            INSERT INTO wagony (liczba_miejsc)
            VALUES (%s) \
            """
    cursor.execute(query, (capacity,))

print("Wagony have been filled")

#########################
# linie
#########################
cursor.execute("SELECT id_przewoznika FROM przewoznicy")
przewoznicy_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id_stacji FROM stacje_kolejowe")
stacje_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id_wagonu FROM wagony")
wagony_ids = [row[0] for row in cursor.fetchall()]

train_models = ["Pendolino", "Pesa Elf", "Flirt", "IC NGT", "EIP", "Intercity", "Desiro"]

for i in range(50):
    model = random.choice(train_models)
    przewoznik_id = random.choice(przewoznicy_ids)
    station_id = random.choice(stacje_ids)
    wagon_id = wagony_ids[i]

    query = """
            INSERT INTO pociagi (model_pociągu, id_przewoźnika, id_aktualna_stacja, stan, id_wagonu)
            VALUES (%s, %s, %s, %s, %s) \
            """

    train_state = "Operational"

    cursor.execute(query, (model, przewoznik_id, station_id, train_state, wagon_id))

print("Pociagi have been filled")

#########################
#Połączenia
#########################
cursor.execute("SELECT id_linii, id_stacji, id_przewoznika FROM linie_kolejowe")
linie_data = cursor.fetchall()

cursor.execute("SELECT id_pociągu, id_przewoźnika FROM pociagi")
pociagi_data = cursor.fetchall()

cursor.execute("SELECT id_stacji FROM stacje_kolejowe")
stacje_ids = [row[0] for row in cursor.fetchall()]

for _ in range(100):
    line = random.choice(linie_data)
    id_linii = line[0]
    id_stacji_poczatkowej = line[1]
    id_przewoznika_from_line = line[2]

    id_stacji_koncowej = random.choice(stacje_ids)
    while id_stacji_poczatkowej == id_stacji_koncowej:
        id_stacji_koncowej = random.choice(stacje_ids)

    available_trains = [train for train in pociagi_data if train[1] == id_przewoznika_from_line]
    if available_trains:
        id_pociagu = random.choice(available_trains)[0]
    else:
        continue

    travel_time = f"{random.randint(0, 5)}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"
    delay = f"{random.randint(0, 2)}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"
    connection_date = f"2025-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"

    query = """
            INSERT INTO polaczenia (id_lini, id_stacji_początkowej, id_stacji_końcowej, id_pociągu, czas_przejazdu, data, opóźnienie)
            VALUES (%s, %s, %s, %s, %s, %s, %s) \
            """

    cursor.execute(query, (id_linii, id_stacji_poczatkowej, id_stacji_koncowej, id_pociagu, travel_time, connection_date, delay))

print("Polaczenia have been filled")

########################
#Bilety
########################

cursor.execute("SELECT id_pasażera FROM pasazerowie")
pasazerowie_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id_połączenia FROM polaczenia")
polaczenia_ids = [row[0] for row in cursor.fetchall()]

for _ in range(100):
    pasazer_id = random.choice(pasazerowie_ids)
    polaczenie_id = random.choice(polaczenia_ids)
    cena = random.randint(50, 300)
    ulgi = random.choice(["None", "Student", "Senior", "Weteran", "Dziecko"])

    query = """
            INSERT INTO bilety (id_pasażera, id_połączenia, cena, ulgi)
            VALUES (%s, %s, %s, %s) \
            """

    cursor.execute(query, (pasazer_id, polaczenie_id, cena, ulgi))

print("Bilety have been filled")

conn.commit()
cursor.close()
conn.close()