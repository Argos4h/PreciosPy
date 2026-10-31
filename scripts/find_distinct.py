import sqlite3
import urllib.request
import json

conn = sqlite3.connect('dist/catalog_latest.db')
c = conn.cursor()
c.execute("""
    SELECT DISTINCT p.id, p.ean, p.normalized_name, p.brand, p.image_url, o.regular_price
    FROM local_products p
    JOIN local_offers o ON p.id = o.product_id
    WHERE p.image_url LIKE 'https://static.app.biggie.com.py%'
    GROUP BY p.id
    LIMIT 40
""")
rows = c.fetchall()

distinct_verified = []
req_headers = {'User-Agent': 'Mozilla/5.0'}

for r in rows:
    p_id, ean, name, brand, image_url, regular_price = r
    try:
        req = urllib.request.Request(image_url, headers=req_headers)
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status == 200:
                print(f"VERIFIED 200: id={p_id} {name} -> {image_url}")
                distinct_verified.append({
                    "id": p_id,
                    "ean": ean,
                    "name": name,
                    "brand": brand or name.split()[0],
                    "image": image_url,
                    "price": regular_price
                })
    except Exception as e:
        pass

print(f"Distinct verified count: {len(distinct_verified)}")
with open('scripts/distinct_verified.json', 'w', encoding='utf-8') as f:
    json.dump(distinct_verified, f, indent=2, ensure_ascii=False)

