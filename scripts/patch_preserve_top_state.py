# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update initial state variables
old_vars = "let selectedCartStore = 'Biggie Express'; // 'Biggie Express', 'Superseis', 'Supermercados Stock', or 'split'"
new_vars = "let selectedCartStore = null; // Inicializa con el TOP 1 (menor gasto)\n    let lastSingleStore = null; // Recuerda el súper monomarca activo antes de activar Split"

content = content.replace(old_vars, new_vars)

# 2. Update selectPodiumStore
old_select = """    function selectPodiumStore(storeName) {
      selectedCartStore = storeName;
      const toggle = document.getElementById('splitCartToggle');"""

new_select = """    function selectPodiumStore(storeName) {
      selectedCartStore = storeName;
      lastSingleStore = storeName;
      const toggle = document.getElementById('splitCartToggle');"""

content = content.replace(old_select, new_select)

# 3. Update renderCart default assignment
old_rend_default = """      // Si no hay súper seleccionado previamente, seleccionar el TOP por defecto
      if (!selectedCartStore) {
        selectedCartStore = rank1.key;
      }"""

new_rend_default = """      // Si no hay súper seleccionado previamente, seleccionar el TOP por defecto
      if (!selectedCartStore) {
        selectedCartStore = rank1.key;
        lastSingleStore = rank1.key;
      }"""

content = content.replace(old_rend_default, new_rend_default)

# 4. Update toggleSplitCart to restore lastSingleStore
old_toggle = """    function toggleSplitCart(isChecked) {
      const hint = document.getElementById('splitSavingsHint');
      const container = document.getElementById('splitCartBreakdownContainer');
      const plan = getSplitPlan();
      if (isChecked) {
        selectedCartStore = 'split';
        hint.innerHTML = '✨ ¡Modo Split Activo! Biggie: 2 productos + Superseis: 1 producto';
        if (container) {
          renderSplitBreakdown();
          container.classList.remove('hidden');
        }
        renderCart();
        showToast('✂️ Optimización Multi-Supermercado activada');
      } else {
        selectedCartStore = 'Biggie Express';
        hint.innerHTML = 'Comprando en ' + (plan.storesCount || 2) + ' súper ahorras Gs. ' + (plan.extraSavings || 14500).toLocaleString('es-PY') + ' extra';
        if (container) {
          container.classList.add('hidden');
        }
        renderCart();
        showToast('🛒 Mostrando toda tu lista en Biggie Express');
      }
    }"""

new_toggle = """    function toggleSplitCart(isChecked) {
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

content = content.replace(old_toggle.replace('\r\n', '\n'), new_toggle.replace('\r\n', '\n'))

with open('scripts/build_html.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied successfully to build_html.py!")

