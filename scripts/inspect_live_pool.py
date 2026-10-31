import json

with open('scripts/biggie_live_pool.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total items in biggie_live_pool: {len(items)}")
for i, it in enumerate(items[:20]):
    print(f"{i+1}. {it['name']} | Gs. {it['price']} | Family: {it.get('family')} | Img: {bool(it.get('image'))}")

