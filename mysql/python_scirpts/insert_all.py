from insert_scripts.insert_bilety import insert_bilety
from insert_scripts.insert_pasazerowie import insert_pasazerowie
from insert_scripts.insert_pociagi import insert_pociagi
from insert_scripts.insert_przejazdy import insert_przejazdy
from insert_scripts.insert_przewoznicy import insert_przewoznicy
from insert_scripts.insert_stacje import insert_stacje
from insert_scripts.insert_wagony import insert_wagony
from insert_scripts.insert_polaczenia import insert_polaczenia

import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="szkot"
)


cursor = conn.cursor()

cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
cursor.execute("TRUNCATE TABLE przewoznicy;")
cursor.execute("TRUNCATE TABLE przejazdy;")
cursor.execute("TRUNCATE TABLE bilety;")
cursor.execute("TRUNCATE TABLE pociagi;")
cursor.execute("TRUNCATE TABLE polaczenia;")
cursor.execute("TRUNCATE TABLE wagony;")
cursor.execute("TRUNCATE TABLE stacje_kolejowe;")
cursor.execute("TRUNCATE TABLE pasazerowie;")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
print("All tables truncated")

conn.commit()
cursor.close()
conn.close()

insert_przewoznicy()
insert_pociagi(100)
insert_wagony()
insert_stacje(200)
insert_pasazerowie(1000)
insert_polaczenia(300)
insert_przejazdy()
insert_bilety()

print("All inserts done succesfully(at least I hope)")