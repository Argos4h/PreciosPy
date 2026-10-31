# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/verified_products_clean.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

for idx, p in enumerate(products):
    stores = p.get('stores', {})
    print(f"[{idx}] {p['name'][:30]}: Biggie={stores.get('Biggie Express', p['regularPrice'])}, Superseis={stores.get('Superseis')}, Stock={stores.get('Supermercados Stock')}")

