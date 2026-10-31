import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/verified_products_clean.json', 'r', encoding='utf-8') as f:
    clean12 = json.load(f)

with open('scripts/distinct_verified.json', 'r', encoding='utf-8') as f:
    distinct40 = json.load(f)

print(f"clean12 has {len(clean12)} items")
for i, p in enumerate(clean12):
    print(f"clean[{i}]: id={p['id']}, name={p['name']}, price={p['regularPrice']}, store={p['store']}")

