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

#########################
#pasazerowie
#########################

for _ in range(10000):
    first = fake.first_name()
    last = fake.last_name()
    email = fake.email()
    phone = fake.phone_number()

    query = """
        INSERT INTO pasazerowie (imie, nazwisko, mail, telefon)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (first, last, email, phone))

print("Pasazerowie have been filled")

#########################
#miasta
#########################

for _ in range(1000):
    city = fake.city()
    station_name = city + ' Główny'

    # Sprawdzanie, czy stacja już istnieje
    cursor.execute("""
        SELECT COUNT(*) FROM stacje_kolejowe
        WHERE nazwa_stacji = %s AND miasto = %s
    """, (station_name, city))
    
    if cursor.fetchone()[0] == 0:  # Jeśli stacja nie istnieje
        query = """
            INSERT INTO `stacje_kolejowe` (nazwa_stacji, miasto)
            VALUES (%s, %s)
        """
        cursor.execute(query, (station_name, city))

print("Stacje kolejowe have been filled")

carrier_names = [
    "PKP Intercity", "Arriva", "Koleje Mazowieckie", "Koleje Śląskie",
    "Łódzka Kolej Aglomeracyjna", "Przewozy Regionalne",
    "Warszawska Kolej Dojazdowa", "Koleje Wielkopolskie", "Koleje Dolnośląskie"
]

# Wstaw przewoźników do bazy
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
    two_cities = cursor.fetchall()  # Fetch the results first

    # Now perform the insertion
    for city in two_cities:
        city_id = city[0]
        city_name = "Linia " + city[1]
        przewoznik_id = random.choice(przewoznicy_ids)

        query = """
            INSERT INTO linie_kolejowe (nazwa_linii, id_stacji,id_przewoznika)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (city_name, city_id,przewoznik_id))


print("Linie have been filled")



#########################
# Wagony
#########################

wagon_capacity = [30, 50, 70, 100] 


for _ in range(100):  
    capacity = random.choice(wagon_capacity)  
    query = """
        INSERT INTO wagony (liczba_miejsc)
        VALUES (%s)
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

cursor.execute("SELECT id_wagonu FROM wagony")  # Fetch all wagons
wagony_ids = [row[0] for row in cursor.fetchall()]

train_models = ["Pendolino", "Pesa Elf", "Flirt", "IC NGT", "EIP", "Intercity", "Desiro"]

for i in range(50):  
    model = random.choice(train_models) 
    przewoznik_id = random.choice(przewoznicy_ids)  
    station_id = random.choice(stacje_ids)  
    wagon_id = wagony_ids[i]  

    query = """
        INSERT INTO pociagi (model_pociągu, id_przewoźnika, id_aktualna_stacja, stan, id_wagonu)
        VALUES (%s, %s, %s, %s, %s)
    """

    train_state = "Operational"
    
    cursor.execute(query, (model, przewoznik_id, station_id, train_state, wagon_id))

print("Pociagi have been filled")
#########################
#Połączenia
########################
cursor.execute("SELECT id_linii, id_stacji, id_przewoznika FROM linie_kolejowe")
linie_data = cursor.fetchall()  # Fetch id_linii, id_stacji, and id_przewoznika

cursor.execute("SELECT id_pociągu, id_przewoźnika FROM pociagi")
pociagi_data = cursor.fetchall()  # Fetch id_pociągu and id_przewoźnika

cursor.execute("SELECT id_stacji FROM stacje_kolejowe")
stacje_ids = [row[0] for row in cursor.fetchall()]

# Generate random connections (połączenia)
for _ in range(100):  # Generating 100 connections (połączenia)
    # Randomly select a line and get corresponding station and carrier
    line = random.choice(linie_data)
    id_linii = line[0]
    id_stacji_początkowej = line[1]  # id_stacji is assigned from id_linii
    id_przewoznika_from_line = line[2]  # id_przewoznika is assigned from id_linii

    # Ensure the destination station is different from the starting station
    id_stacji_końcowej = random.choice(stacje_ids)
    while id_stacji_początkowej == id_stacji_końcowej:
        id_stacji_końcowej = random.choice(stacje_ids)

    # Find a pociąg (train) that has the same przewoznik as the one from id_linii
    available_trains = [train for train in pociagi_data if train[1] == id_przewoznika_from_line]
    if available_trains:
        id_pociągu = random.choice(available_trains)[0]  # Randomly select a train that matches the carrier
    else:
        continue  # If no trains are available, skip this iteration

    # Randomly generate a travel time (czas_przejazdu) and delay (opóźnienie)
    travel_time = f"{random.randint(0, 5)}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"  # HH:MM:SS format
    delay = f"{random.randint(0, 2)}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"  # HH:MM:SS format
    
    # Randomly generate a date for the connection (date)
    connection_date = f"2025-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"

    query = """
        INSERT INTO polaczenia (id_lini, id_stacji_początkowej, id_stacji_końcowej, id_pociągu, czas_przejazdu, data, opóźnienie)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    # Execute the insert query
    cursor.execute(query, (id_linii, id_stacji_początkowej, id_stacji_końcowej, id_pociągu, travel_time, connection_date, delay))


print("Polaczenia have been filled")


########################
#Bilety
########################

cursor.execute("SELECT id_pasażera FROM pasazerowie")
pasazerowie_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id_połączenia FROM polaczenia")
polaczenia_ids = [row[0] for row in cursor.fetchall()]

# Generate random tickets
for _ in range(100):  # Generating 100 random tickets
    pasazer_id = random.choice(pasazerowie_ids)  # Randomly select a passenger
    polaczenie_id = random.choice(polaczenia_ids)  # Randomly select a connection
    cena = random.randint(50, 300)  # Random ticket price between 50 and 300
    ulgi = random.choice(["None", "Student", "Senior", "Weteran", "Dziecko"])  # Random discount
    
    query = """
        INSERT INTO bilety (id_pasażera, id_połączenia, cena, ulgi)
        VALUES (%s, %s, %s, %s)
    """
    
    cursor.execute(query, (pasazer_id, polaczenie_id, cena, ulgi))

print("Bilety have been filled")

conn.commit()
cursor.close()
conn.close()
