import sqlite3

conn = sqlite3.connect('dist/catalog_latest.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

for t in tables:
    name = t[0]
    cursor.execute(f"SELECT COUNT(*) FROM {name};")
    count = cursor.fetchone()[0]
    print(f"Table {name}: {count} rows")

cursor.execute("SELECT * FROM products LIMIT 5;")
cols = [d[0] for d in cursor.description]
print("Products columns:", cols)
for row in cursor.fetchall():
    print(row)

conn.close()

