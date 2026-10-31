import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/distinct_verified.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total items in distinct_verified.json: {len(items)}")
for i, item in enumerate(items):
    print(f"{i+1}. {item.get('name')} | Brand: {item.get('brand')} | EAN: {item.get('ean')} | Price: {item.get('price')} | Image: {item.get('image')[:60]}...")

