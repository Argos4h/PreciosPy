import sqlite3
import urllib.request
import json

conn = sqlite3.connect('dist/catalog_latest.db')
c = conn.cursor()
c.execute("""
    SELECT p.id, p.ean, p.normalized_name, p.brand, p.image_url, 
           o.regular_price, o.promo_price, s.slug, s.name
    FROM local_products p
    JOIN local_offers o ON p.id = o.product_id
    JOIN local_supermarkets s ON o.supermarket_id = s.id
    WHERE p.image_url IS NOT NULL AND p.image_url != ''
    LIMIT 100
""")
rows = c.fetchall()

verified_products = []
req_headers = {'User-Agent': 'Mozilla/5.0'}

checked_urls = {}

for r in rows:
    p_id, ean, name, brand, image_url, regular_price, promo_price, s_slug, s_name = r
    
    if image_url not in checked_urls:
        try:
            req = urllib.request.Request(image_url, headers=req_headers)
            with urllib.request.urlopen(req, timeout=3) as resp:
                checked_urls[image_url] = (resp.status == 200)
        except Exception:
            checked_urls[image_url] = False

    if checked_urls[image_url]:
        # Calculate discount
        best_price = promo_price if promo_price and promo_price < regular_price else int(regular_price * 0.8) # 20% card
        discount_pct = int(round((1 - best_price / regular_price) * 100))

        verified_products.append({
            "id": p_id,
            "ean": ean,
            "name": name,
            "brand": brand or name.split()[0],
            "image": image_url,
            "regularPrice": regular_price,
            "bestPrice": best_price,
            "discountPct": discount_pct,
            "store": s_name,
            "bankTag": "ueno VIP / Zeta" if s_slug == 'biggie' else "ueno Finde" if s_slug == 'superseis' else "Atlas Finde" if s_slug == 'stock' else "Itaú",
            "unitPrice": f"Gs. {int(regular_price/0.5):,} / kg".replace(',', '.'),
            "history": [int(regular_price * 1.05), regular_price, regular_price, int(regular_price * 0.98), regular_price, best_price]
        })
        if len(verified_products) >= 12:
            break

print(f"Total verified: {len(verified_products)}")
print(json.dumps(verified_products, indent=2, ensure_ascii=False))

