import sys, sqlite3
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('dist/catalog_latest.db')
c = conn.cursor()
c.execute("SELECT id, ean, normalized_name, brand, category, image_url, base_unit FROM local_products;")
rows = c.fetchall()
print(f"Total local_products in SQLite: {len(rows)}")
for r in rows:
    print(r)
conn.close()

