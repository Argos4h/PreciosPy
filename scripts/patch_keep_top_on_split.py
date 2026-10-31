# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. En renderCart(): isSplitActive debe consultar el toggle o la variable
old_is_split = """      // Si no hay súper seleccionado previamente, seleccionar el TOP por defecto
      if (!selectedCartStore) {
        selectedCartStore = rank1.key;
        lastSingleStore = rank1.key;
      }

      const isSplitActive = (selectedCartStore === 'split');"""

new_is_split = """      // Si no hay súper seleccionado previamente, seleccionar el TOP por defecto
      if (!selectedCartStore || selectedCartStore === 'split') {
        selectedCartStore = rank1.key;
        lastSingleStore = rank1.key;
      }

      const splitToggleEl = document.getElementById('splitCartToggle');
      const isSplitActive = splitToggleEl ? splitToggleEl.checked : isSplitCartActive;"""

# 2. En createCardHtml(): Eliminar el bloque if (isSplitActive) para que el podio NUNCA cambie ni deseleccione el top activo
old_card_logic = """          let cardBase = '';
          let badgeClass = '';
          let statusHtml = '';

          if (isSplitActive) {
            // En modo Split: vista neutra donde ninguno está seleccionado individualmente
            if (store.key === 'Biggie Express') {
              cardBase = 'p-2.5 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-center flex flex-col justify-between cursor-pointer hover:border-emerald-500/60 transition-all z-0';
              statusHtml = '<span class="text-[9px] text-emerald-400 font-black">2 prod. en split</span>';
            } else if (store.key === 'Superseis') {
              cardBase = 'p-2.5 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-center flex flex-col justify-between cursor-pointer hover:border-amber-500/60 transition-all z-0';
              statusHtml = '<span class="text-[9px] text-amber-400 font-black">1 prod. en split</span>';
            } else {
              cardBase = 'p-2.5 rounded-2xl bg-slate-900/60 border border-slate-800/80 text-center flex flex-col justify-between cursor-pointer opacity-70 hover:opacity-100 transition-all z-0';
              statusHtml = '<span class="text-[9px] text-slate-500 font-semibold">Tocar para ver</span>';
            }
            badgeClass = isTop
              ? 'bg-slate-800 text-amber-300 border border-amber-500/30 font-bold'
              : 'bg-slate-800 text-slate-400 border border-slate-700/60 font-medium';
          } else if (isSelected) {
            // ¡SOLO ESTE TOP ESTÁ SELECCIONADO! (Borde 2px destacado, anillo de foco, escala 105, sombra activa)
            cardBase = `p-2.5 rounded-2xl ${store.bgActive} border-2 ${store.colorBorder} ring-2 ${store.ringColor} shadow-xl shadow-black/40 text-center flex flex-col justify-between relative scale-105 cursor-pointer active:scale-95 transition-all duration-200 z-10`;
            badgeClass = isTop 
              ? 'bg-emerald-500 text-slate-950 font-black shadow-sm'
              : (place === 2 ? 'bg-amber-500 text-slate-950 font-black shadow-sm' : 'bg-blue-500 text-slate-950 font-black shadow-sm');
            statusHtml = `<span class="text-[9.5px] ${store.textAccent} font-black flex items-center justify-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-current"></span>✓ Viendo aquí</span>`;
          } else {
            // LOS OTROS DOS TOPS NO SELECCIONADOS (Apagados, opacidad reducida, escala 95, sin borde activo ni resplandor)
            cardBase = 'p-2.5 rounded-2xl bg-slate-900/60 border border-slate-800/80 text-center flex flex-col justify-between cursor-pointer opacity-65 hover:opacity-95 hover:border-slate-700 scale-95 transition-all duration-200 z-0';
            badgeClass = isTop 
              ? 'bg-slate-800/90 text-amber-300 border border-amber-500/30 font-bold' 
              : 'bg-slate-800/90 text-slate-400 border border-slate-700/60 font-medium';
            statusHtml = '<span class="text-[9px] text-slate-500 font-semibold">Tocar para ver</span>';
          }"""

new_card_logic = """          let cardBase = '';
          let badgeClass = '';
          let statusHtml = '';

          if (isSelected) {
            // ¡SOLO ESTE TOP ESTÁ SELECCIONADO! (Se mantiene siempre como el seleccionado único aun al activar Split)
            cardBase = `p-2.5 rounded-2xl ${store.bgActive} border-2 ${store.colorBorder} ring-2 ${store.ringColor} shadow-xl shadow-black/40 text-center flex flex-col justify-between relative scale-105 cursor-pointer active:scale-95 transition-all duration-200 z-10`;
            badgeClass = isTop 
              ? 'bg-emerald-500 text-slate-950 font-black shadow-sm'
              : (place === 2 ? 'bg-amber-500 text-slate-950 font-black shadow-sm' : 'bg-blue-500 text-slate-950 font-black shadow-sm');
            statusHtml = `<span class="text-[9.5px] ${store.textAccent} font-black flex items-center justify-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-current"></span>✓ Viendo aquí</span>`;
          } else {
            // LOS OTROS DOS TOPS NO SELECCIONADOS (Apagados, escala 95, sin borde activo ni resplandor)
            cardBase = 'p-2.5 rounded-2xl bg-slate-900/60 border border-slate-800/80 text-center flex flex-col justify-between cursor-pointer opacity-65 hover:opacity-95 hover:border-slate-700 scale-95 transition-all duration-200 z-0';
            badgeClass = isTop 
              ? 'bg-slate-800/90 text-amber-300 border border-amber-500/30 font-bold' 
              : 'bg-slate-800/90 text-slate-400 border border-slate-700/60 font-medium';
            statusHtml = '<span class="text-[9px] text-slate-500 font-semibold">Tocar para ver</span>';
          }"""

# 3. En toggleSplitCart(): No pisar selectedCartStore con 'split'
old_toggle_split = """    function toggleSplitCart(isChecked) {
      const hint = document.getElementById('splitSavingsHint');
      const container = document.getElementById('splitCartBreakdownContainer');
      const plan = getSplitPlan();
      if (isChecked) {
        if (selectedCartStore && selectedCartStore !== 'split') {
          lastSingleStore = selectedCartStore;
        }
        selectedCartStore = 'split';
        hint.innerHTML = '✨ ¡Modo Split Activo! Biggie: 2 productos + Superseis: 1 producto';
        if (container) {
          renderSplitBreakdown();
          container.classList.remove('hidden');
        }
        renderCart();
        showToast('✂️ Optimización Multi-Supermercado activada');
      } else {
        // Restaurar exactamente el súper monomarca que estaba activo antes de entrar a Split
        selectedCartStore = lastSingleStore || 'Supermercados Stock';
        hint.innerHTML = 'Comprando en ' + (plan.storesCount || 2) + ' súper ahorras Gs. ' + (plan.extraSavings || 14500).toLocaleString('es-PY') + ' extra';
        if (container) {
          container.classList.add('hidden');
        }
        renderCart();
        const shortName = selectedCartStore === 'Supermercados Stock' ? 'Stock' : selectedCartStore;
        showToast('🛒 Mostrando toda tu lista en ' + shortName);
      }
    }"""

new_toggle_split = """    function toggleSplitCart(isChecked) {
      isSplitCartActive = isChecked;
      const hint = document.getElementById('splitSavingsHint');
      const container = document.getElementById('splitCartBreakdownContainer');
      const plan = getSplitPlan();
      if (isChecked) {
        if (selectedCartStore && selectedCartStore !== 'split') {
          lastSingleStore = selectedCartStore;
        }
        hint.innerHTML = '✨ ¡Modo Split Activo! Biggie: 2 productos + Superseis: 1 producto';
        if (container) {
          renderSplitBreakdown();
          container.classList.remove('hidden');
        }
        renderCart();
        showToast('✂️ Optimización Multi-Supermercado activada');
      } else {
        // Mantener exactamente el súper monomarca activo
        if (lastSingleStore) {
          selectedCartStore = lastSingleStore;
        }
        hint.innerHTML = 'Comprando en ' + (plan.storesCount || 2) + ' súper ahorras Gs. ' + (plan.extraSavings || 14500).toLocaleString('es-PY') + ' extra';
        if (container) {
          container.classList.add('hidden');
        }
        renderCart();
        const shortName = selectedCartStore === 'Supermercados Stock' ? 'Stock' : selectedCartStore;
        showToast('🛒 Mostrando toda tu lista en ' + shortName);
      }
    }"""

# 4. En selectPodiumStore(): desactivar isSplitCartActive
old_select_podium = """    function selectPodiumStore(storeName) {
      selectedCartStore = storeName;
      lastSingleStore = storeName;
      const toggle = document.getElementById('splitCartToggle');
      if (toggle) toggle.checked = false;
      const splitContainer = document.getElementById('splitCartBreakdownContainer');
      if (splitContainer) splitContainer.classList.add('hidden');
      updateSplitHint();
      renderCart();
      const shortName = storeName === 'Supermercados Stock' ? 'Stock' : storeName;
      showToast('🏬 Cotizando toda tu lista en ' + shortName);
    }"""

new_select_podium = """    function selectPodiumStore(storeName) {
      selectedCartStore = storeName;
      lastSingleStore = storeName;
      isSplitCartActive = false;
      const toggle = document.getElementById('splitCartToggle');
      if (toggle) toggle.checked = false;
      const splitContainer = document.getElementById('splitCartBreakdownContainer');
      if (splitContainer) splitContainer.classList.add('hidden');
      updateSplitHint();
      renderCart();
      const shortName = storeName === 'Supermercados Stock' ? 'Stock' : storeName;
      showToast('🏬 Cotizando toda tu lista en ' + shortName);
    }"""

code_norm = code.replace('\r\n', '\n')
err = False

for name, old_b, new_b in [
    ("is_split in renderCart", old_is_split, new_is_split),
    ("card logic", old_card_logic, new_card_logic),
    ("toggleSplitCart", old_toggle_split, new_toggle_split),
    ("selectPodiumStore", old_select_podium, new_select_podium)
]:
    old_b_norm = old_b.replace('\r\n', '\n')
    new_b_norm = new_b.replace('\r\n', '\n')
    if old_b_norm in code_norm:
        code_norm = code_norm.replace(old_b_norm, new_b_norm)
        print(f"✓ Replaced {name} successfully.")
    else:
        print(f"ERROR: {name} not found!")
        err = True

if not err:
    with open('scripts/build_html.py', 'w', encoding='utf-8') as f:
        f.write(code_norm)
    print("SUCCESS: scripts/build_html.py patched successfully!")
else:
    print("FAILED TO APPLY PATCH")
