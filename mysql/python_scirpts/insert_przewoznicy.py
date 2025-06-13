import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()[:16]

nazwy_przewoznikow = [
    'PKP Intercity',
    'Koleje Mazowieckie',
    'Polregio',
    'Koleje Dolnośląskie',
    'Koleje Wielkopolskie',
    'Koleje Małopolskie',
    'SKM Trójmiasto',
    'Łódzka Kolej Aglomeracyjna',
    'Koleje Śląskie'
]

def utworz_login(nazwa, idx):
    slug = ''.join(c.lower() for c in nazwa if c.isalnum())
    return slug[:12]

# haslo do kazdego przewoznika do 123

print("INSERT INTO przewoznicy (id_przewoznika, nazwa, username, haslo) VALUES")
for i, nazwa in enumerate(nazwy_przewoznikow, start=1):
    username = utworz_login(nazwa, i)
    haslo_zahashowane = hash_password('123')
    print(f"({i}, '{nazwa}', '{username}', '{haslo_zahashowane}'){',' if i < len(nazwy_przewoznikow) else ';'}")