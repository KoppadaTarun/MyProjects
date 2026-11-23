
import sqlite3

connection = sqlite3.connect("data/enterprise_rag.db")

cursor = connection.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name;
""")

tables = cursor.fetchall()

print("Tables created in SQLite:")

for table in tables:
    print(table[0])

connection.close()
