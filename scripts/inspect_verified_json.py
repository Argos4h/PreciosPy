import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/verified_products_clean.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(json.dumps(data[0], indent=2, ensure_ascii=False))
