import sqlite3
import urllib.request

conn = sqlite3.connect('dist/catalog_latest.db')
c = conn.cursor()
c.execute("""
    SELECT id, name, ean, image_url, regular_price, category 
    FROM products 
    WHERE image_url LIKE 'https://static.app.biggie.com.py%'
    LIMIT 25
""")
rows = c.fetchall()

verified = []
req_headers = {'User-Agent': 'Mozilla/5.0'}

for r in rows:
    url = r[3]
    try:
        req = urllib.request.Request(url, headers=req_headers)
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status == 200:
                print(f"VERIFIED [200]: {r[1]} -> {url}")
                verified.append({
                    "id": r[0],
                    "name": r[1],
                    "ean": r[2],
                    "image": url,
                    "price": r[4],
                    "category": r[5]
                })
                if len(verified) >= 12:
                    break
    except Exception as e:
        pass

print(f"\nTotal verified: {len(verified)}")
for v in verified:
    print(v)

