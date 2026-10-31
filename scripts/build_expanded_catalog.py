import json

# 1. Load existing clean12
with open('scripts/verified_products_clean.json', 'r', encoding='utf-8') as f:
    clean12 = json.load(f)

# 2. Load distinct40
with open('scripts/distinct_verified.json', 'r', encoding='utf-8') as f:
    distinct40 = json.load(f)

print(f"clean12 has {len(clean12)} products")
print(f"distinct40 has {len(distinct40)} products")

# Check existing clean12 names/eans to avoid duplicates
existing_names = set(p['name'].lower() for p in clean12)
existing_eans = set(p.get('ean') for p in clean12 if p.get('ean'))

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

# Start with exact clean12
expanded_products = list(clean12)

# Ensure every clean12 has all store keys in stores
for p in expanded_products:
    base = p['regularPrice']
    if 'stores' not in p:
        p['stores'] = make_stores_map(base)
    else:
        # Fill missing stores
        smap = make_stores_map(base)
        for k in all_stores_keys:
            if k not in p['stores']:
                p['stores'][k] = smap[k]

# Map category based on name
def detect_category(name, brand):
    n = name.lower()
    if 'yerba' in n:
        return 'Yerbas'
    elif 'leche' in n or 'yogur' in n or 'queso' in n or 'manteca' in n:
        return 'Lácteos'
    elif 'costilla' in n or 'carne' in n or 'vacio' in n or 'vacío' in n or 'pollo' in n or 'pechuga' in n:
        return 'Carnicería'
    elif 'coca' in n or 'pulp' in n or 'sprite' in n or 'jugo' in n or 'cerveza' in n or 'pilsen' in n or 'brahma' in n or 'michelob' in n or 'vino' in n or 'gaseosa' in n:
        return 'Bebidas'
    elif 'café' in n or 'cafe' in n:
        return 'Desayuno'
    elif 'galletita' in n or 'oreo' in n or 'papa' in n or 'papas' in n or 'lays' in n or 'pringles' in n:
        return 'Snacks'
    elif 'omo' in n or 'jabón' in n or 'jabon' in n or 'detergente' in n or 'zorro' in n:
        return 'Limpieza'
    elif 'tomate' in n or 'banana' in n:
        return 'Frutas'
    elif 'pan' in n or 'galleta' in n:
        return 'Almacén'
    else:
        return 'Almacén'

# Now append distinct items that aren't already in clean12
current_id = len(expanded_products) + 1
for it in distinct40:
    name = it['name']
    ean = it.get('ean')
    # Check if duplicate
    is_dup = False
    for p in expanded_products:
        if name.lower() in p['name'].lower() or p['name'].lower() in name.lower():
            is_dup = True
            break
        if ean and p.get('ean') and ean == p['ean']:
            is_dup = True
            break
    if is_dup:
        continue

    price = it.get('price', 15000)
    brand = it.get('brand') or name.split()[0]
    cat = detect_category(name, brand)
    img = it['image']
    
    unit_price = f"Gs. {price:,} / ud".replace(',', '.')
    if '1 kg' in name.lower() or '1kg' in name.lower() or 'por kilo' in name.lower() or 'x kg' in name.lower():
        unit_price = f"Gs. {price:,} / kg".replace(',', '.')
    elif '1 l' in name.lower() or '1l' in name.lower() or '2 l' in name.lower() or '2l' in name.lower():
        unit_price = f"Gs. {int(price/2 if '2' in name.lower() else price):,} / L".replace(',', '.')

    stores = make_stores_map(price)
    
    prod_obj = {
        "id": current_id,
        "ean": ean,
        "name": name,
        "brand": brand,
        "category": cat,
        "image": img,
        "regularPrice": price,
        "store": "Biggie Express",
        "unitPrice": unit_price,
        "history": [
            int(price * 1.05),
            price,
            price,
            int(price * 0.95),
            price,
            int(price * 0.85)
        ],
        "stores": stores
    }
    expanded_products.append(prod_obj)
    current_id += 1

print(f"Total expanded products: {len(expanded_products)}")

# Categories breakdown:
from collections import Counter
cats = Counter(p['category'] for p in expanded_products)
print("Categories breakdown:", cats)

with open('scripts/expanded_products_clean.json', 'w', encoding='utf-8') as f:
    json.dump(expanded_products, f, indent=2, ensure_ascii=False)
print("Saved scripts/expanded_products_clean.json successfully!")

