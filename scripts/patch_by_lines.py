# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = None
end_idx = None
for i, line in enumerate(lines):
    if '// Precio Biggie Express' in line:
        start_idx = i
    if 'const itemObj = {' in line and start_idx is not None:
        end_idx = i
        break

print(f"Found block: {start_idx} to {end_idx}")

new_block = """        // Precio Biggie Express
        const isAlcohol = prod.name.toLowerCase().includes('cerveza') || prod.name.toLowerCase().includes('michelob') || prod.name.toLowerCase().includes('vino');
        let pBiggieBase = (prod.stores && prod.stores['Biggie Express']) ? prod.stores['Biggie Express'] : prod.regularPrice;
        let offerBiggie = isAlcohol 
          ? { finalPrice: pBiggieBase, discountPct: 0, bankTag: 'Precio Góndola (Excluye reintegro alcohol)' }
          : calculateStoreOffer('Biggie Express', pBiggieBase, selectedDay);
        let pBiggieFinal = offerBiggie.finalPrice;

        // Precio Superseis
        let pSuperseisBase = (prod.stores && prod.stores['Superseis']) ? prod.stores['Superseis'] : prod.regularPrice;
        let offerSuperseis = calculateStoreOffer('Superseis', pSuperseisBase, selectedDay);
        let pSuperseisFinal = offerSuperseis.finalPrice;

        // Precio Stock
        let pStockBase = (prod.stores && prod.stores['Supermercados Stock']) ? prod.stores['Supermercados Stock'] : prod.regularPrice;
        let offerStock = calculateStoreOffer('Supermercados Stock', pStockBase, selectedDay);
        let pStockFinal = offerStock.finalPrice;

        totalBiggie += pBiggieFinal * qty;
        totalSuperseis += pSuperseisFinal * qty;
        totalStock += pStockFinal * qty;

        // Asignacion optima entre Biggie Express y Superseis
        let assignedStore = 'Biggie Express';
        let winnerPrice = pBiggieFinal;
        let winnerOffer = offerBiggie;
        let otherStore = 'Superseis';
        let otherPrice = pSuperseisFinal;
        let otherOffer = offerSuperseis;

        if (pSuperseisFinal < pBiggieFinal) {
          assignedStore = 'Superseis';
          winnerPrice = pSuperseisFinal;
          winnerOffer = offerSuperseis;
          otherStore = 'Biggie Express';
          otherPrice = pBiggieFinal;
          otherOffer = offerBiggie;
        } else {
          assignedStore = 'Biggie Express';
          winnerPrice = pBiggieFinal;
          winnerOffer = offerBiggie;
          otherStore = 'Superseis';
          otherPrice = pSuperseisFinal;
          otherOffer = offerSuperseis;
        }

        const diffPerUnit = Math.max(0, otherPrice - winnerPrice);
        const diffTotal = diffPerUnit * qty;

        // Explicacion explicita de la diferencia del porque
        let whyExplanation = '';
        if (assignedStore === 'Biggie Express') {
          if (winnerOffer.discountPct > 0) {
            whyExplanation = 'En Biggie pagas <strong>Gs. ' + winnerPrice.toLocaleString('es-PY') + '</strong> (' + winnerOffer.bankTag + ') en vez de <strong>Gs. ' + otherPrice.toLocaleString('es-PY') + '</strong> en Superseis. ¡Ahorras <strong>Gs. ' + diffPerUnit.toLocaleString('es-PY') + '</strong> por unidad' + (qty > 1 ? ' (Gs. ' + diffTotal.toLocaleString('es-PY') + ' en tus ' + qty + ' u.)' : '') + '!';
          } else if (diffPerUnit > 0) {
            whyExplanation = 'Precio regular más barato en Biggie (Gs. ' + winnerPrice.toLocaleString('es-PY') + ' vs Gs. ' + otherPrice.toLocaleString('es-PY') + ' en Superseis). Ahorras <strong>Gs. ' + diffPerUnit.toLocaleString('es-PY') + '</strong> por unidad.';
          } else {
            whyExplanation = 'Mismo precio en ambos súper (Gs. ' + winnerPrice.toLocaleString('es-PY') + '). Asignado a Biggie para conveniencia y cercanía.';
          }
        } else {
          if (isAlcohol) {
            whyExplanation = 'En Superseis el pack cuesta <strong>Gs. ' + winnerPrice.toLocaleString('es-PY') + '</strong> vs <strong>Gs. ' + otherPrice.toLocaleString('es-PY') + '</strong> en Biggie (las cervezas están excluidas del reintegro bancario en Biggie). ¡Ahorras <strong>Gs. ' + diffPerUnit.toLocaleString('es-PY') + '</strong> por pack!';
          } else if (winnerOffer.discountPct > 0) {
            whyExplanation = 'En Superseis pagas <strong>Gs. ' + winnerPrice.toLocaleString('es-PY') + '</strong> (' + winnerOffer.bankTag + ') en vez de <strong>Gs. ' + otherPrice.toLocaleString('es-PY') + '</strong> en Biggie. ¡Ahorras <strong>Gs. ' + diffPerUnit.toLocaleString('es-PY') + '</strong> por unidad' + (qty > 1 ? ' (Gs. ' + diffTotal.toLocaleString('es-PY') + ' en tus ' + qty + ' u.)' : '') + '!';
          } else if (diffPerUnit > 0) {
            whyExplanation = 'Precio de góndola menor en Superseis (Gs. ' + winnerPrice.toLocaleString('es-PY') + ' vs Gs. ' + otherPrice.toLocaleString('es-PY') + ' en Biggie). Ahorras <strong>Gs. ' + diffPerUnit.toLocaleString('es-PY') + '</strong> por pack/unidad.';
          } else {
            whyExplanation = 'Mejor disponibilidad y precio mayorista en Superseis (Gs. ' + winnerPrice.toLocaleString('es-PY') + ').';
          }
        }

"""

lines[start_idx:end_idx] = [new_block]

with open('scripts/build_html.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Patch applied successfully!")

