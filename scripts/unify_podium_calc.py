# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_calc = """        biggieTotal += Math.round(prod.regularPrice * (bankProfiles.ueno.enabled ? (1 - (uenoPcts[bankProfiles.ueno.level] || 35) / 100) : 1)) * qty;
        superseisTotal += Math.round(prod.regularPrice * ((selectedDay === 5 || selectedDay === 6) && bankProfiles.ueno.enabled ? 0.8 : 0.95)) * qty;
        stockTotal += Math.round(prod.regularPrice * (selectedDay === 2 && bankProfiles.itau.enabled ? 0.8 : 0.98)) * qty;"""

new_calc = """        const isAlcohol = prod.name.toLowerCase().includes('cerveza') || prod.name.toLowerCase().includes('michelob') || prod.name.toLowerCase().includes('vino');
        
        // Biggie Express (compra monomarca 100% en Biggie)
        const pBiggieBase = (prod.stores && prod.stores['Biggie Express']) ? prod.stores['Biggie Express'] : prod.regularPrice;
        const offerBiggie = isAlcohol 
          ? { finalPrice: pBiggieBase } 
          : calculateStoreOffer('Biggie Express', pBiggieBase, selectedDay);
        biggieTotal += offerBiggie.finalPrice * qty;

        // Superseis (compra monomarca 100% en Superseis)
        const pSuperBase = (prod.stores && prod.stores['Superseis']) ? prod.stores['Superseis'] : prod.regularPrice;
        const offerSuper = calculateStoreOffer('Superseis', pSuperBase, selectedDay);
        superseisTotal += offerSuper.finalPrice * qty;

        // Stock (compra monomarca 100% en Stock)
        const pStockBase = (prod.stores && prod.stores['Supermercados Stock']) ? prod.stores['Supermercados Stock'] : prod.regularPrice;
        const offerStock = calculateStoreOffer('Supermercados Stock', pStockBase, selectedDay);
        stockTotal += offerStock.finalPrice * qty;"""

old_calc_norm = old_calc.replace('\r\n', '\n')
text_norm = text.replace('\r\n', '\n')

if old_calc_norm in text_norm:
    updated = text_norm.replace(old_calc_norm, new_calc.replace('\r\n', '\n'))
    with open('scripts/build_html.py', 'w', encoding='utf-8') as f:
        f.write(updated)
    print("SUCCESS: Unified podium calculation in build_html.py")
else:
    print("ERROR: old_calc NOT found")

