# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/verified_products_clean.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

def rank_stores_for_cart(cart):
    biggie_total = 0
    super_total = 0
    stock_total = 0

    for k, qty in cart.items():
        p = products[k]
        is_alc = 'cerveza' in p['name'].lower() or 'michelob' in p['name'].lower()
        
        # Biggie
        p_biggie = p.get('stores', {}).get('Biggie Express', p['regularPrice'])
        biggie_total += (p_biggie if is_alc else round(p_biggie * 0.65)) * qty

        # Superseis (Saturday ueno 20%)
        p_super = p.get('stores', {}).get('Superseis', p['regularPrice'])
        super_total += round(p_super * 0.80) * qty

        # Stock (Saturday ueno 20%)
        p_stock = p.get('stores', {}).get('Supermercados Stock', p['regularPrice'])
        stock_total += round(p_stock * 0.80) * qty

    stores = [
        {'name': 'Biggie Express', 'total': biggie_total},
        {'name': 'Superseis', 'total': super_total},
        {'name': 'Supermercados Stock', 'total': stock_total}
    ]
    stores.sort(key=lambda x: x['total'])
    return stores

# Case 1: Default cart (with beer Michelob)
cart1 = {0: 2, 1: 6, 3: 1}
ranked1 = rank_stores_for_cart(cart1)
print("=== CASO 1: CARRITO CON CERVEZA MICHELOB ===")
for i, s in enumerate(ranked1):
    print(f"  {i+1}° Lugar: {s['name']} -> Gs. {s['total']:,}")
print(f"  👑 EL TOP (donde se gasta menos) es: {ranked1[0]['name']} (Gs. {ranked1[0]['total']:,})")

# Case 2: Cart without beer (only Yerba Kurupí + Lactolanda)
cart2 = {0: 2, 1: 6}
ranked2 = rank_stores_for_cart(cart2)
print("\n=== CASO 2: CARRITO DE ALMACÉN (YERBA + LECHE) ===")
for i, s in enumerate(ranked2):
    print(f"  {i+1}° Lugar: {s['name']} -> Gs. {s['total']:,}")
print(f"  👑 EL TOP (donde se gasta menos) es: {ranked2[0]['name']} (Gs. {ranked2[0]['total']:,})")

