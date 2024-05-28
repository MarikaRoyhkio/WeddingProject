import sqlite3

connection = sqlite3.connect('guests.sql')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

guests = [
    ('Marika Röyhkiö',),
    ('Susanna Kyrö',),
    ('Clara Luja',),
    ('Pia Varmola',),
    ('Riikka Röyhkiö',),
    ('Satu Varmola',),
    ('Essi Akselin',),
    ('Helena Varmola',),
    ('Kari Varmola',)

]

for guest in guests:
    cur.execute("INSERT OR IGNORE INTO guests (name) VALUES (?)", guest)

cur.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', 'adminpassword'))    



connection.commit()
connection.close()