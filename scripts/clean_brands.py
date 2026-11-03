import sqlite3

db = sqlite3.connect('mobile/assets/db/catalog_latest.db')
db.execute("UPDATE local_products SET brand = TRIM(brand) WHERE brand IS NOT NULL")
db.commit()

res = [r[0] for r in db.execute("SELECT DISTINCT brand FROM local_products WHERE brand IS NOT NULL AND TRIM(brand) != '' ORDER BY brand COLLATE NOCASE").fetchall()]
print(f"Total clean brands: {len(res)}")
print("Sample:", res[:15])
db.close()

