# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/verified_products_clean.json', 'r', encoding='utf-8') as f:
    prods = json.load(f)

p_beer = prods[3] # Cerveza Michelob
print(f"Product: {p_beer['name']}")
print(f"  regularPrice: {p_beer['regularPrice']}")
print(f"  stores: {p_beer.get('stores', {})}")
