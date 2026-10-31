import urllib.request, json

all_items = []
headers = {'User-Agent': 'Mozilla/5.0'}

for skip in [0, 50, 100, 150, 200, 250, 300]:
    url = f"https://api.app.biggie.com.py/api/articles?take=50&skip={skip}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8', errors='ignore'))
            items = data.get('items', [])
            print(f"Fetched {len(items)} items at skip={skip}")
            all_items.extend(items)
    except Exception as e:
        print(f"Error at skip={skip}: {e}")

print(f"Total raw items fetched: {len(all_items)}")

valid_products = []
seen_names = set()

for it in all_items:
    name = it.get('name')
    price = it.get('price')
    if not name or not price or price <= 0:
        continue
    if name.lower() in seen_names:
        continue
    seen_names.add(name.lower())
    
    images = it.get('images', [])
    img_url = images[0].get('src') if images and len(images) > 0 and isinstance(images[0], dict) else None
    
    ean = it.get('cbaCode') or it.get('code')
    brand = it.get('brand', {}).get('name') if isinstance(it.get('brand'), dict) else (it.get('brand') or name.split()[0])
    family = it.get('family', {}).get('name') if isinstance(it.get('family'), dict) else ''

    valid_products.append({
        'name': name,
        'price': price,
        'ean': ean,
        'brand': brand,
        'family': family,
        'image': img_url
    })

print(f"Valid distinct products: {len(valid_products)}")
with open('scripts/biggie_live_pool.json', 'w', encoding='utf-8') as f:
    json.dump(valid_products, f, indent=2, ensure_ascii=False)
