# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_why_code = """        // Explicacion explicita de la diferencia del porque
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
        }"""

new_why_code = """        // Explicación simplificada y directa del porqué (solo lo esencial)
        let whyExplanation = '';
        const shortOther = otherStore === 'Biggie Express' ? 'Biggie' : otherStore;
        const shortWinner = assignedStore === 'Biggie Express' ? 'Biggie' : assignedStore;

        if (assignedStore === 'Biggie Express') {
          if (winnerOffer.discountPct > 0) {
            whyExplanation = 'Ahorras <strong class="text-emerald-400">Gs. ' + diffPerUnit.toLocaleString('es-PY') + ' c/u</strong> con ' + winnerOffer.bankTag + ' vs ' + shortOther + '.';
          } else if (diffPerUnit > 0) {
            whyExplanation = 'Ahorras <strong class="text-emerald-400">Gs. ' + diffPerUnit.toLocaleString('es-PY') + ' c/u</strong> por precio góndola vs ' + shortOther + '.';
          } else {
            whyExplanation = 'Mismo precio. Asignado a ' + shortWinner + ' por cercanía.';
          }
        } else {
          if (isAlcohol) {
            whyExplanation = 'Ahorras <strong class="text-amber-400">Gs. ' + diffPerUnit.toLocaleString('es-PY') + '</strong> vs Biggie (alcohol sin promo en Biggie).';
          } else if (winnerOffer.discountPct > 0) {
            whyExplanation = 'Ahorras <strong class="text-amber-400">Gs. ' + diffPerUnit.toLocaleString('es-PY') + ' c/u</strong> con ' + winnerOffer.bankTag + ' vs ' + shortOther + '.';
          } else if (diffPerUnit > 0) {
            whyExplanation = 'Ahorras <strong class="text-amber-400">Gs. ' + diffPerUnit.toLocaleString('es-PY') + ' c/u</strong> por precio góndola vs ' + shortOther + '.';
          } else {
            whyExplanation = 'Mismo precio en ambos súper.';
          }
        }"""

old_html_why = """              <!-- LA DIFERENCIA DEL PORQUÉ (EXPLICACIÓN EXPLÍCITA) -->
              <div class="p-2 rounded-xl bg-slate-900/90 border border-emerald-500/20 text-[10.5px] leading-relaxed">
                <div class="flex items-start space-x-1.5">
                  <span class="text-xs shrink-0">💡</span>
                  <div class="flex-1 min-w-0">
                    <span class="font-extrabold text-white block">¿Por qué comprar acá?</span>
                    <p class="text-slate-300 mt-0.5 text-[10px]">
                      ${it.whyExplanation}
                    </p>
                  </div>
                </div>
              </div>"""

new_html_why = """              <!-- MOTIVO ESENCIAL -->
              <div class="px-2.5 py-1.5 rounded-xl bg-slate-900/80 border border-white/5 text-[10.5px]">
                <div class="flex items-center space-x-1.5">
                  <span class="text-xs shrink-0">💡</span>
                  <span class="font-bold text-slate-400 text-[9px] uppercase tracking-wide">¿Por qué comprar acá?</span>
                </div>
                <p class="text-slate-200 mt-0.5 pl-4 text-[10px] font-medium leading-normal">
                  ${it.whyExplanation}
                </p>
              </div>"""

code_norm = code.replace('\r\n', '\n')
old_why_norm = old_why_code.replace('\r\n', '\n')
new_why_norm = new_why_code.replace('\r\n', '\n')
old_html_norm = old_html_why.replace('\r\n', '\n')
new_html_norm = new_html_why.replace('\r\n', '\n')

err = False
if old_why_norm in code_norm:
    code_norm = code_norm.replace(old_why_norm, new_why_norm)
    print("✓ Replaced whyExplanation logic with simplified essential text.")
else:
    print("ERROR: old_why_norm not found")
    err = True

if old_html_norm in code_norm:
    code_norm = code_norm.replace(old_html_norm, new_html_norm)
    print("✓ Replaced HTML why block with compact essential style.")
else:
    print("ERROR: old_html_norm not found")
    err = True

if not err:
    with open('scripts/build_html.py', 'w', encoding='utf-8') as f:
        f.write(code_norm)
    print("SUCCESS: scripts/build_html.py updated successfully!")

