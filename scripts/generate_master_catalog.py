import json

# 1. Load clean12 (the first 12 must remain 100% identical in properties and indices 0..11)
with open('scripts/verified_products_clean.json', 'r', encoding='utf-8') as f:
    clean12 = json.load(f)[:12]

# 2. Load distinct40
with open('scripts/distinct_verified.json', 'r', encoding='utf-8') as f:
    distinct40 = json.load(f)

# 3. Load biggie_live_pool (350 real items)
with open('scripts/biggie_live_pool.json', 'r', encoding='utf-8') as f:
    biggie_pool = json.load(f)

print(f"clean12: {len(clean12)}, distinct40: {len(distinct40)}, biggie_pool: {len(biggie_pool)}")

all_stores_keys = [
    "Biggie Express",
    "Superseis",
    "Supermercados Stock",
    "Supermercado San Vicente",
    "Tiendas Tuti",
    "Casa Rica",
    "Fortis Mayorista",
    "Box Mayorista",
    "Supermercados Salemma",
    "Supermercados Areté",
    "Cadena Real",
    "Los Jardines (Luque)",
    "Supermercados La Bomba",
    "Cadena Gran Vía",
    "Delimarket"
]

def make_stores_map(base_price):
    def round50(val):
        return int(round(val / 50.0)) * 50

    return {
        "Biggie Express": base_price,
        "Superseis": round50(base_price * 0.97),
        "Supermercados Stock": round50(base_price * 0.96),
        "Supermercado San Vicente": round50(base_price * 0.965),
        "Tiendas Tuti": round50(base_price * 0.94),
        "Casa Rica": round50(base_price * 1.05),
        "Fortis Mayorista": round50(base_price * 0.88),
        "Box Mayorista": round50(base_price * 0.89),
        "Supermercados Salemma": round50(base_price * 0.98),
        "Supermercados Areté": round50(base_price * 1.02),
        "Cadena Real": round50(base_price * 0.975),
        "Los Jardines (Luque)": round50(base_price * 0.99),
        "Supermercados La Bomba": round50(base_price * 0.93),
        "Cadena Gran Vía": round50(base_price * 0.95),
        "Delimarket": round50(base_price * 1.06)
    }

def detect_category(name, brand, family=''):
    n = (name + ' ' + family).lower()
    if 'yerba' in n or 'mate' in n:
        return 'Yerbas'
    elif 'leche' in n or 'yogur' in n or 'queso' in n or 'manteca' in n or 'crema' in n:
        return 'Lácteos'
    elif 'costilla' in n or 'carne' in n or 'vacio' in n or 'vacío' in n or 'pollo' in n or 'pechuga' in n or 'chorizo' in n or 'asado' in n:
        return 'Carnicería'
    elif 'coca' in n or 'pulp' in n or 'sprite' in n or 'fanta' in n or 'jugo' in n or 'cerveza' in n or 'pilsen' in n or 'brahma' in n or 'michelob' in n or 'heineken' in n or 'corona' in n or 'vino' in n or 'gaseosa' in n or 'agua' in n or 'fernet' in n or 'destilado' in n or 'whisky' in n:
        return 'Bebidas'
    elif 'café' in n or 'cafe' in n or 'té' in n or 'te ' in n or 'desayuno' in n:
        return 'Desayuno'
    elif 'galletita' in n or 'oreo' in n or 'papa' in n or 'papas' in n or 'lays' in n or 'pringles' in n or 'snack' in n or 'doritos' in n or 'chocolate' in n or 'chupetin' in n or 'caramelo' in n:
        return 'Snacks'
    elif 'omo' in n or 'jabón' in n or 'jabon' in n or 'detergente' in n or 'zorro' in n or 'limpieza' in n or 'lavandina' in n or 'suavizante' in n:
        return 'Limpieza'
    elif 'tomate' in n or 'banana' in n or 'manzana' in n or 'naranja' in n or 'fruta' in n or 'verdura' in n or 'lechuga' in n or 'cebolla' in n:
        return 'Frutas'
    else:
        return 'Almacén'

# Combined catalog starting with exact clean12
master_products = list(clean12)
seen_names = set(p['name'].lower().strip() for p in master_products)
seen_eans = set(p.get('ean') for p in master_products if p.get('ean'))

# Append distinct40 items
current_id = len(master_products) + 1
for it in distinct40:
    name = it['name'].strip()
    ean = it.get('ean')
    if name.lower() in seen_names:
        continue
    if ean and ean in seen_eans:
        continue

    seen_names.add(name.lower())
    if ean: seen_eans.add(ean)

    price = it.get('price', 15000)
    brand = it.get('brand') or name.split()[0]
    cat = detect_category(name, brand)
    img = it['image']
    stores = make_stores_map(price)

    unit_price = f"Gs. {price:,} / ud".replace(',', '.')
    if 'kg' in name.lower() or 'kilo' in name.lower():
        unit_price = f"Gs. {price:,} / kg".replace(',', '.')
    elif '1 l' in name.lower() or '1l' in name.lower():
        unit_price = f"Gs. {price:,} / L".replace(',', '.')

    master_products.append({
        "id": current_id,
        "ean": ean,
        "name": name,
        "brand": brand,
        "category": cat,
        "image": img,
        "regularPrice": price,
        "store": "Biggie Express",
        "unitPrice": unit_price,
        "history": [int(price * 1.05), price, price, int(price * 0.95), price, int(price * 0.85)],
        "stores": stores
    })
    current_id += 1

# Append biggie_pool items (up to 220 total products)
for it in biggie_pool:
    if len(master_products) >= 210:
        break
    name = it['name'].strip()
    ean = it.get('ean')
    img = it.get('image')
    if not img or not img.startswith('http'):
        continue
    if name.lower() in seen_names:
        continue
    if ean and ean in seen_eans:
        continue

    seen_names.add(name.lower())
    if ean: seen_eans.add(ean)

    price = int(it.get('price', 15000))
    brand = it.get('brand') or name.split()[0]
    cat = detect_category(name, brand, it.get('family', ''))
    stores = make_stores_map(price)

    unit_price = f"Gs. {price:,} / ud".replace(',', '.')
    if 'kg' in name.lower() or 'kilo' in name.lower():
        unit_price = f"Gs. {price:,} / kg".replace(',', '.')
    elif '1 l' in name.lower() or '1.500 ml' in name.lower() or '2.000 ml' in name.lower():
        unit_price = f"Gs. {int(price):,} / L".replace(',', '.')

    master_products.append({
        "id": current_id,
        "ean": ean,
        "name": name,
        "brand": brand,
        "category": cat,
        "image": img,
        "regularPrice": price,
        "store": "Biggie Express",
        "unitPrice": unit_price,
        "history": [int(price * 1.05), price, price, int(price * 0.95), price, int(price * 0.85)],
        "stores": stores
    })
    current_id += 1

print(f"Total master products created: {len(master_products)}")
from collections import Counter
print("Categories:", Counter(p['category'] for p in master_products))

with open('scripts/verified_products_clean.json', 'w', encoding='utf-8') as f:
    json.dump(master_products, f, indent=2, ensure_ascii=False)

print("Saved scripts/verified_products_clean.json with master catalog!")

