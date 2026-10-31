import urllib.request
import json

queries = ['yerba', 'leche', 'coca cola', 'cerveza', 'costilla', 'oreo', 'cafe', 'papas']
products = []

req_headers = {'User-Agent': 'Mozilla/5.0'}

for q in queries:
    url = f"https://api.app.biggie.com.py/api/articles?take=8&query={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers=req_headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            for item in data.get('items', []):
                imgs = item.get('images', [])
                if imgs and len(imgs) > 0 and imgs[0].get('src'):
                    src = imgs[0]['src']
                    # Verify 200
                    try:
                        img_req = urllib.request.Request(src, headers=req_headers)
                        with urllib.request.urlopen(img_req, timeout=3) as img_resp:
                            if img_resp.status == 200:
                                name = item.get('name')
                                price = item.get('price', 10000)
                                print(f"MATCH: {name} -> {src}")
                                products.append({
                                    'name': name,
                                    'price': price,
                                    'image': src,
                                    'family': item.get('family', {}).get('name', '').strip()
                                })
                                break
                    except Exception:
                        pass
    except Exception as e:
        print("Query failed:", q, e)

print(f"\nFound {len(products)} perfect products:")
for p in products:
    print(p)

with open('scripts/perfect_matched_products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

