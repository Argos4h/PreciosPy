# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/verified_products_clean.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

cart = {0: 2, 1: 6, 3: 1} # 2 Kurupí, 6 Lactolanda, 1 Michelob
selected_day = 6 # Saturday (ueno active)

def calc_mode(mode_name):
    total_reg = 0
    total_final = 0
    items_out = []
    
    for k, qty in cart.items():
        p = products[k]
        is_alc = 'cerveza' in p['name'].lower() or 'michelob' in p['name'].lower()
        
        if mode_name == 'Biggie Express':
            base_p = p.get('stores', {}).get('Biggie Express', p['regularPrice'])
            final_p = base_p if is_alc else round(base_p * 0.65) # ueno N4 35%
            store_label = 'Biggie Express'
        elif mode_name == 'Superseis':
            base_p = p.get('stores', {}).get('Superseis', p['regularPrice'])
            final_p = round(base_p * 0.80) # Saturday ueno 20%
            store_label = 'Superseis'
        elif mode_name == 'Supermercados Stock':
            base_p = p.get('stores', {}).get('Supermercados Stock', p['regularPrice'])
            final_p = round(base_p * 0.80) # Saturday ueno 20%
            store_label = 'Stock'
        elif mode_name == 'split':
            if is_alc:
                # Michelob goes to Superseis
                base_p = p.get('stores', {}).get('Superseis', p['regularPrice'])
                final_p = round(base_p * 0.80)
                store_label = 'Superseis (Mejor opción)'
            else:
                # Kurupí and Lactolanda go to Biggie
                base_p = p.get('stores', {}).get('Biggie Express', p['regularPrice'])
                final_p = round(base_p * 0.65)
                store_label = 'Biggie Express (Mejor opción)'

        sub_reg = base_p * qty
        sub_fin = final_p * qty
        total_reg += sub_reg
        total_final += sub_fin
        items_out.append(f"  • {p['name'][:22]} (x{qty}): Gs. {final_p:,} c/u [{store_label}] -> Gs. {sub_fin:,}")

    return total_reg, total_final, items_out

for mode in ['Biggie Express', 'Superseis', 'Supermercados Stock', 'split']:
    reg, fin, items = calc_mode(mode)
    print(f"\n=== MODO: {mode.upper()} ===")
    print(f"Total a Pagar: Gs. {fin:,} (Ahorro: Gs. {reg - fin:,})")
    for it in items:
        print(it)

