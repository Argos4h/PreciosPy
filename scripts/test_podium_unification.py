# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/verified_products_clean.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Default cart: 0: 2, 1: 6, 3: 1
cart = {0: 2, 1: 6, 3: 1}
# Saturday (selectedDay = 6), ueno enabled N4 (35% Biggie, 20% Superseis/Stock)

biggie_total = 0
superseis_total = 0
stock_total = 0

for k, qty in cart.items():
    p = products[k]
    is_alcohol = 'cerveza' in p['name'].lower() or 'michelob' in p['name'].lower()
    
    # Biggie
    p_biggie_base = p.get('stores', {}).get('Biggie Express', p['regularPrice'])
    p_biggie_final = p_biggie_base if is_alcohol else round(p_biggie_base * 0.65)
    biggie_total += p_biggie_final * qty

    # Superseis (Saturday with ueno Finde 20%)
    p_super_base = p.get('stores', {}).get('Superseis', p['regularPrice'])
    p_super_final = round(p_super_base * 0.80)
    superseis_total += p_super_final * qty

    # Stock (Saturday with ueno Finde 20%)
    p_stock_base = p.get('stores', {}).get('Supermercados Stock', p['regularPrice'])
    p_stock_final = round(p_stock_base * 0.80)
    stock_total += p_stock_final * qty

    print(f"{p['name']} (x{qty}):")
    print(f"  Biggie: Gs. {p_biggie_final * qty:,}")
    print(f"  Superseis: Gs. {p_super_final * qty:,}")
    print(f"  Stock: Gs. {p_stock_final * qty:,}")

print("\n=== TOTALES COMPRA 100% EN CADA SÚPER ===")
print(f"Superseis Total: Gs. {superseis_total:,}")
print(f"Biggie Total: Gs. {biggie_total:,}")
print(f"Stock Total: Gs. {stock_total:,}")

split_total = (11375 * 2) + (4063 * 6) + (38400 * 1)
print(f"\nTotal Dividido (Split 2 Kurupí Biggie + 6 Lactolanda Biggie + 1 Michelob Superseis): Gs. {split_total:,}")
print(f"Ahorro extra dividiendo vs mejor súper único (Superseis {superseis_total:,}): Gs. {superseis_total - split_total:,}")

