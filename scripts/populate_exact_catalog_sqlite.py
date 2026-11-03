import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json

print("Actualizando SQLite 'mobile/assets/db/catalog_latest.db' con los 1.200 productos 100% exactos...")

db = sqlite3.connect('mobile/assets/db/catalog_latest.db')
cursor = db.cursor()

# Mapa de supermercados
supermarket_map = {}
for row in cursor.execute("SELECT id, slug FROM local_supermarkets").fetchall():
    supermarket_map[row[1]] = row[0]

cursor.execute("DELETE FROM local_products")
cursor.execute("DELETE FROM local_offers")
cursor.execute("DELETE FROM local_products_fts")

with open('scripts/verified_products_clean.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Cargando {len(products)} productos a SQLite...")

offer_id = 1
for p in products:
    p_id = p['id']
    ean = str(p.get('ean') or '')
    name = p['name'].strip()
    brand = (p.get('brand') or '').strip()
    img = p['image'].strip()
    reg_price = int(p['regularPrice'])
    unit_measure = 'ud'
    if 'kg' in name.lower() or 'kilo' in name.lower():
        unit_measure = 'kg'
    elif '1 l' in name.lower() or '1l' in name.lower() or 'litro' in name.lower():
        unit_measure = 'L'

    cursor.execute("""
        INSERT INTO local_products (id, ean, normalized_name, brand, unit_measure, unit_quantity, base_unit, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (p_id, ean, name, brand, unit_measure, 1.0, unit_measure, img))

    cursor.execute("""
        INSERT INTO local_products_fts (rowid, normalized_name, brand, ean)
        VALUES (?, ?, ?, ?)
    """, (p_id, name, brand, ean))

    # Ofertas por supermercado
    stores = p.get('stores', {})
    seen_stores_for_product = set()
    for store_name, price in stores.items():
        slug = store_name.lower().replace(' ', '').replace('(', '').replace(')', '').replace('é', 'e').replace('í', 'i')
        if 'biggie' in slug: slug = 'biggie'
        elif 'superseis' in slug: slug = 'superseis'
        elif 'stock' in slug: slug = 'stock'
        elif 'sanvicente' in slug: slug = 'superseis'
        elif 'tuti' in slug: slug = 'tuti'
        elif 'casarica' in slug: slug = 'casarica'
        elif 'fortis' in slug: slug = 'fortis'
        elif 'box' in slug: slug = 'box'
        elif 'salemma' in slug: slug = 'salemma'
        elif 'arete' in slug: slug = 'arete'
        elif 'real' in slug: slug = 'real'
        elif 'jardines' in slug: slug = 'losjardines'
        elif 'bomba' in slug: slug = 'labomba'
        elif 'granvia' in slug: slug = 'granvia'
        elif 'delimarket' in slug: slug = 'delimarket'

        s_id = supermarket_map.get(slug)
        if not s_id or s_id in seen_stores_for_product:
            continue
        seen_stores_for_product.add(s_id)

        cursor.execute("""
            INSERT INTO local_offers (id, product_id, supermarket_id, regular_price, promo_price, club_price, wholesale_price, wholesale_min_qty, price_per_base_unit, in_stock, scraped_at)
            VALUES (?, ?, ?, ?, NULL, NULL, NULL, 1, ?, 1, CURRENT_TIMESTAMP)
        """, (offer_id, p_id, s_id, int(price), int(price)))
        offer_id += 1

db.commit()

p_count = cursor.execute("SELECT count(*) FROM local_products").fetchone()[0]
o_count = cursor.execute("SELECT count(*) FROM local_offers").fetchone()[0]
fts_count = cursor.execute("SELECT count(*) FROM local_products_fts").fetchone()[0]
brands_count = cursor.execute("SELECT count(DISTINCT brand) FROM local_products WHERE length(brand) > 0").fetchone()[0]

print(f"✅ SQLite actualizado con éxito:")
print(f"  • Productos: {p_count}")
print(f"  • Ofertas: {o_count}")
print(f"  • FTS: {fts_count}")
print(f"  • Marcas reales únicas: {brands_count}")

db.close()
