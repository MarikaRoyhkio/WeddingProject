import sqlite3

connection = sqlite3.connect('guests.sql')

with open('guests.sql', ecoding='utf-8') as f:
    connection.executescript(f.read())

    connection.comit()
    connection.close()