import sqlite3
import os


GENERATOR = "./PP2I1/src/backend/db/generator_tables.txt"
DB = "./PP2I1/src/backend/db/main.db"

f = open(GENERATOR, "r")
requests = f.readlines()

try:
    os.remove(DB)
except FileNotFoundError:
    pass
finally:
    print("Generating database...")
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    for request in requests:
        cursor.execute(request)
        conn.commit()
    print("Database generated !")
    conn.close()
