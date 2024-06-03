import os
import sqlite3

if not os.path.exists('guestlist.sql'):
    connection = sqlite3.connect('guestlist.sql')

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
    print("Tämä tietokanta on luotu ja alustettu onnistuneesti.")

else:
    print("Tietokanta on jo olemassa. Ei tarvitse alustaa uudelleen")