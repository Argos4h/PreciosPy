import sqlite3
conn = sqlite3.connect('dist/catalog_latest.db')
c = conn.cursor()
c.execute("PRAGMA table_info(local_products);")
print("local_products columns:", [r[1] for r in c.fetchall()])
c.execute("PRAGMA table_info(local_offers);")
print("local_offers columns:", [r[1] for r in c.fetchall()])
conn.close()

