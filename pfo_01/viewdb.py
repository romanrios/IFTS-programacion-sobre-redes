import sqlite3

conn = sqlite3.connect("mensajes.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM mensajes")

for fila in cursor.fetchall():
    print(fila)

conn.close()