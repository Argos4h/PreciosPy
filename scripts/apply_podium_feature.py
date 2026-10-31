# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add let selectedCartStore = 'Biggie Express';
if "let selectedCartStore =" not in code:
    code = code.replace(
        "let cart = {",
        "let selectedCartStore = 'Biggie Express'; // 'Biggie Express', 'Superseis', 'Supermercados Stock', or 'split'\n    let cart = {"
    )
    print("Added selectedCartStore variable.")

# 2. Add selectPodiumStore function
select_func = """    function selectPodiumStore(storeName) {
      selectedCartStore = storeName;
      const toggle = document.getElementById('splitCartToggle');
      if (toggle) toggle.checked = false;
      const splitContainer = document.getElementById('splitCartBreakdownContainer');
      if (splitContainer) splitContainer.classList.add('hidden');
      updateSplitHint();
      renderCart();
      const shortName = storeName === 'Supermercados Stock' ? 'Stock' : storeName;
      showToast('🏬 Cotizando toda tu lista en ' + shortName);
    }

"""

if "function selectPodiumStore" not in code:
    code = code.replace(
        "    // RENDERIZADO DEL CARRITO & PODIUM\n    function renderCart() {",
        select_func + "    // RENDERIZADO DEL CARRITO & PODIUM\n    function renderCart() {"
    )
    print("Added selectPodiumStore function.")

# 3. Replace renderCart() implementation
old_render_cart_start = "    // RENDERIZADO DEL CARRITO & PODIUM\n    function renderCart() {"
old_render_cart_end = "    function decrementCart(idx) {"

start_pos = code.find(old_render_cart_start)
end_pos = code.find(old_render_cart_end)

if start_pos != -1 and end_pos != -1:
    new_render_cart = """    // RENDERIZADO DEL CARRITO & PODIUM
    function renderCart() {
      const listContainer = document.getElementById('cartItemsList');
      const badge = document.getElementById('navCartBadge');
      
      const cartKeys = Object.keys(cart).filter(k => (cart[k] || 0) > 0);
      const totalItemCount = cartKeys.reduce((acc, k) => acc + cart[k], 0);

      if (badge) badge.innerText = totalItemCount;

      let biggieTotal = 0;
      let superseisTotal = 0;
      let stockTotal = 0;

      // 1. Calcular totales Monomarca para cada uno de los 3 supermercados
      cartKeys.forEach(k => {
        const prod = products[k];
        const qty = cart[k];
        if (!prod) return;

        const isAlcohol = prod.name.toLowerCase().includes('cerveza') || prod.name.toLowerCase().includes('michelob') || prod.name.toLowerCase().includes('vino');
        
        // Biggie Express
        const pBiggieBase = (prod.stores && prod.stores['Biggie Express']) ? prod.stores['Biggie Express'] : prod.regularPrice;
        const offerBiggie = isAlcohol 
          ? { finalPrice: pBiggieBase } 
          : calculateStoreOffer('Biggie Express', pBiggieBase, selectedDay);
        biggieTotal += offerBiggie.finalPrice * qty;

        // Superseis
        const pSuperBase = (prod.stores && prod.stores['Superseis']) ? prod.stores['Superseis'] : prod.regularPrice;
        const offerSuper = calculateStoreOffer('Superseis', pSuperBase, selectedDay);
        superseisTotal += offerSuper.finalPrice * qty;

        // Stock
        const pStockBase = (prod.stores && prod.stores['Supermercados Stock']) ? prod.stores['Supermercados Stock'] : prod.regularPrice;
        const offerStock = calculateStoreOffer('Supermercados Stock', pStockBase, selectedDay);
        stockTotal += offerStock.finalPrice * qty;
      });

      // Actualizar precios en las 3 tarjetas del Podium
      const p1 = document.getElementById('podium1Price');
      const p2 = document.getElementById('podium2Price');
      const p3 = document.getElementById('podium3Price');

      if (p1) p1.innerText = 'Gs. ' + biggieTotal.toLocaleString('es-PY');
      if (p2) p2.innerText = 'Gs. ' + superseisTotal.toLocaleString('es-PY');
      if (p3) p3.innerText = 'Gs. ' + stockTotal.toLocaleString('es-PY');

      // Actualizar estilo visual activo de las 3 tarjetas del Podium
      const cardBiggie = document.getElementById('podiumCardBiggie');
      const cardSuper = document.getElementById('podiumCardSuperseis');
      const cardStock = document.getElementById('podiumCardStock');
      const statusBiggie = document.getElementById('podiumBiggieStatus');
      const statusSuper = document.getElementById('podiumSuperseisStatus');
      const statusStock = document.getElementById('podiumStockStatus');
      const modeBadge = document.getElementById('podiumModeBadge');

      const isSplitActive = (selectedCartStore === 'split');

      if (cardBiggie && cardSuper && cardStock) {
        if (isSplitActive) {
          cardBiggie.className = "p-2.5 rounded-2xl bg-emerald-500/10 border border-emerald-500/40 text-center flex flex-col justify-between cursor-pointer hover:scale-[1.02] transition-all";
          cardSuper.className = "p-2.5 rounded-2xl bg-amber-500/10 border border-amber-500/40 text-center flex flex-col justify-between cursor-pointer hover:scale-[1.02] transition-all";
          cardStock.className = "p-2.5 rounded-2xl bg-slate-900/80 border border-slate-800 text-center flex flex-col justify-between cursor-pointer opacity-70 hover:opacity-100 transition-all";
          if (statusBiggie) statusBiggie.innerHTML = '<span class="text-[9px] text-emerald-400 font-black">2 prod. en split</span>';
          if (statusSuper) statusSuper.innerHTML = '<span class="text-[9px] text-amber-400 font-black">1 prod. en split</span>';
          if (statusStock) statusStock.innerHTML = '<span class="text-[9px] text-slate-500">Tocar para ver</span>';
          if (modeBadge) {
            modeBadge.innerText = '✂️ Ahorro Dividido';
            modeBadge.className = 'text-[9px] font-black uppercase px-2 py-0.5 rounded-full bg-emerald-500 text-slate-950 shadow-sm animate-pulse';
          }
        } else if (selectedCartStore === 'Superseis') {
          cardSuper.className = "p-2.5 rounded-2xl bg-amber-500/20 border-2 border-amber-500 text-center flex flex-col justify-between relative shadow-lg shadow-amber-500/20 scale-105 cursor-pointer ring-2 ring-amber-400/50 transition-all";
          cardBiggie.className = "p-2.5 rounded-2xl bg-slate-900/80 border border-slate-800 text-center flex flex-col justify-between cursor-pointer hover:border-slate-700 opacity-80 hover:opacity-100 transition-all";
          cardStock.className = "p-2.5 rounded-2xl bg-slate-900/80 border border-slate-800 text-center flex flex-col justify-between cursor-pointer hover:border-slate-700 opacity-80 hover:opacity-100 transition-all";
          if (statusSuper) statusSuper.innerHTML = '<span class="text-[9px] text-amber-300 font-black">✓ Viendo aquí</span>';
          if (statusBiggie) statusBiggie.innerHTML = '<span class="text-[9px] text-slate-500 font-semibold">Tocar para ver</span>';
          if (statusStock) statusStock.innerHTML = '<span class="text-[9px] text-slate-500 font-semibold">Tocar para ver</span>';
          if (modeBadge) {
            modeBadge.innerText = '100% Superseis';
            modeBadge.className = 'text-[9px] font-black uppercase px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30';
          }
        } else if (selectedCartStore === 'Supermercados Stock') {
          cardStock.className = "p-2.5 rounded-2xl bg-blue-500/20 border-2 border-blue-500 text-center flex flex-col justify-between relative shadow-lg shadow-blue-500/20 scale-105 cursor-pointer ring-2 ring-blue-400/50 transition-all";
          cardBiggie.className = "p-2.5 rounded-2xl bg-slate-900/80 border border-slate-800 text-center flex flex-col justify-between cursor-pointer hover:border-slate-700 opacity-80 hover:opacity-100 transition-all";
          cardSuper.className = "p-2.5 rounded-2xl bg-slate-900/80 border border-slate-800 text-center flex flex-col justify-between cursor-pointer hover:border-slate-700 opacity-80 hover:opacity-100 transition-all";
          if (statusStock) statusStock.innerHTML = '<span class="text-[9px] text-blue-300 font-black">✓ Viendo aquí</span>';
          if (statusBiggie) statusBiggie.innerHTML = '<span class="text-[9px] text-slate-500 font-semibold">Tocar para ver</span>';
          if (statusSuper) statusSuper.innerHTML = '<span class="text-[9px] text-slate-500 font-semibold">Tocar para ver</span>';
          if (modeBadge) {
            modeBadge.innerText = '100% Stock';
            modeBadge.className = 'text-[9px] font-black uppercase px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-300 border border-blue-500/30';
          }
        } else {
          // Biggie Express por defecto
          cardBiggie.className = "p-2.5 rounded-2xl bg-emerald-500/20 border-2 border-emerald-500 text-center flex flex-col justify-between relative shadow-lg shadow-emerald-500/20 scale-105 cursor-pointer ring-2 ring-emerald-400/50 transition-all";
          cardSuper.className = "p-2.5 rounded-2xl bg-slate-900/80 border border-slate-800 text-center flex flex-col justify-between cursor-pointer hover:border-slate-700 opacity-80 hover:opacity-100 transition-all";
          cardStock.className = "p-2.5 rounded-2xl bg-slate-900/80 border border-slate-800 text-center flex flex-col justify-between cursor-pointer hover:border-slate-700 opacity-80 hover:opacity-100 transition-all";
          if (statusBiggie) statusBiggie.innerHTML = '<span class="text-[9px] text-emerald-300 font-black">✓ Viendo aquí</span>';
          if (statusSuper) statusSuper.innerHTML = '<span class="text-[9px] text-slate-500 font-semibold">Tocar para ver</span>';
          if (statusStock) statusStock.innerHTML = '<span class="text-[9px] text-slate-500 font-semibold">Tocar para ver</span>';
          if (modeBadge) {
            modeBadge.innerText = '100% Biggie Express';
            modeBadge.className = 'text-[9px] font-black uppercase px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
          }
        }
      }

      // 2. Calcular subtotal y total calculado según el modo activo
      let subtotalRegular = 0;
      let totalCalculated = 0;

      cartKeys.forEach(k => {
        const prod = products[k];
        const qty = cart[k];
        if (!prod) return;

        let basePrice = prod.regularPrice;
        let finalPrice = prod.regularPrice;

        if (isSplitActive) {
          const isBeerOrMeat = prod.name.includes('Michelob') || prod.name.includes('Cerveza');
          if (isBeerOrMeat) {
            basePrice = (prod.stores && prod.stores['Superseis']) ? prod.stores['Superseis'] : prod.regularPrice;
            const offer = calculateStoreOffer('Superseis', basePrice, selectedDay);
            finalPrice = offer.finalPrice;
          } else {
            basePrice = (prod.stores && prod.stores['Biggie Express']) ? prod.stores['Biggie Express'] : prod.regularPrice;
            const offer = calculateStoreOffer('Biggie Express', basePrice, selectedDay);
            finalPrice = offer.finalPrice;
          }
        } else if (selectedCartStore === 'Superseis') {
          basePrice = (prod.stores && prod.stores['Superseis']) ? prod.stores['Superseis'] : prod.regularPrice;
          const offer = calculateStoreOffer('Superseis', basePrice, selectedDay);
          finalPrice = offer.finalPrice;
        } else if (selectedCartStore === 'Supermercados Stock') {
          basePrice = (prod.stores && prod.stores['Supermercados Stock']) ? prod.stores['Supermercados Stock'] : prod.regularPrice;
          const offer = calculateStoreOffer('Supermercados Stock', basePrice, selectedDay);
          finalPrice = offer.finalPrice;
        } else {
          basePrice = (prod.stores && prod.stores['Biggie Express']) ? prod.stores['Biggie Express'] : prod.regularPrice;
          const isAlcohol = prod.name.toLowerCase().includes('cerveza') || prod.name.toLowerCase().includes('michelob') || prod.name.toLowerCase().includes('vino');
          const offer = isAlcohol ? { finalPrice: basePrice } : calculateStoreOffer('Biggie Express', basePrice, selectedDay);
          finalPrice = offer.finalPrice;
        }

        subtotalRegular += basePrice * qty;
        totalCalculated += finalPrice * qty;
      });

      const totalSavings = Math.max(0, subtotalRegular - totalCalculated);

      const elSubtotal = document.getElementById('cartSubtotalRegular');
      if (elSubtotal) elSubtotal.innerText = 'Gs. ' + subtotalRegular.toLocaleString('es-PY');

      const elSavings = document.getElementById('cartTotalSavings');
      if (elSavings) elSavings.innerText = '- Gs. ' + totalSavings.toLocaleString('es-PY');

      const elFinal = document.getElementById('cartFinalTotal');
      if (elFinal) elFinal.innerText = 'Gs. ' + totalCalculated.toLocaleString('es-PY');

      const elStoreLabel = document.getElementById('cartFinalStoreLabel');
      if (elStoreLabel) {
        if (isSplitActive) {
          elStoreLabel.innerText = '✂️ Total con Ahorro Dividido (2 Súper)';
          elStoreLabel.className = 'text-[10px] text-emerald-400 font-black block';
        } else if (selectedCartStore === 'Superseis') {
          elStoreLabel.innerText = '🏬 Total comprando todo en Superseis';
          elStoreLabel.className = 'text-[10px] text-amber-400 font-black block';
        } else if (selectedCartStore === 'Supermercados Stock') {
          elStoreLabel.innerText = '🛒 Total comprando todo en Stock';
          elStoreLabel.className = 'text-[10px] text-blue-400 font-black block';
        } else {
          elStoreLabel.innerText = '🏪 Total comprando todo en Biggie Express';
          elStoreLabel.className = 'text-[10px] text-emerald-400 font-black block';
        }
      }

      const islandSavings = document.getElementById('islandSavingsText');
      if (islandSavings) islandSavings.innerText = 'Gs. ' + totalSavings.toLocaleString('es-PY');

      updateSplitHint();
      const splitToggle = document.getElementById('splitCartToggle');
      const splitContainer = document.getElementById('splitCartBreakdownContainer');
      if (splitToggle && splitToggle.checked) {
        renderSplitBreakdown();
        if (splitContainer) splitContainer.classList.remove('hidden');
      } else {
        if (splitContainer) splitContainer.classList.add('hidden');
      }

      if (!listContainer) return;

      if (cartKeys.length === 0) {
        listContainer.innerHTML = `
          <div class="py-10 text-center text-slate-500 glass-card rounded-3xl">
            <span class="text-4xl">🛒</span>
            <p class="text-xs font-bold mt-2">Tu lista de compras está vacía</p>
            <p class="text-[10px] text-slate-600">Explora la góndola y suma productos para comparar</p>
            <button onclick="switchTab('viewSearch')" class="mt-3 px-3 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-400 font-bold text-xs border border-emerald-500/30">
              Ir a la Góndola
            </button>
          </div>
        `;
        return;
      }

      // Renderizar productos de la lista con los precios del súper seleccionado
      listContainer.innerHTML = cartKeys.map(k => {
        const prod = products[k];
        const qty = cart[k];

        let basePrice = prod.regularPrice;
        let finalPrice = prod.regularPrice;
        let storeBadgeTxt = '';

        if (isSplitActive) {
          const isBeerOrMeat = prod.name.includes('Michelob') || prod.name.includes('Cerveza');
          if (isBeerOrMeat) {
            basePrice = (prod.stores && prod.stores['Superseis']) ? prod.stores['Superseis'] : prod.regularPrice;
            const offer = calculateStoreOffer('Superseis', basePrice, selectedDay);
            finalPrice = offer.finalPrice;
            storeBadgeTxt = '🏬 Superseis (Mejor opción) • ' + offer.bankTag;
          } else {
            basePrice = (prod.stores && prod.stores['Biggie Express']) ? prod.stores['Biggie Express'] : prod.regularPrice;
            const offer = calculateStoreOffer('Biggie Express', basePrice, selectedDay);
            finalPrice = offer.finalPrice;
            storeBadgeTxt = '🏪 Biggie Express (Mejor opción) • ' + offer.bankTag;
          }
        } else if (selectedCartStore === 'Superseis') {
          basePrice = (prod.stores && prod.stores['Superseis']) ? prod.stores['Superseis'] : prod.regularPrice;
          const offer = calculateStoreOffer('Superseis', basePrice, selectedDay);
          finalPrice = offer.finalPrice;
          storeBadgeTxt = '🏬 Superseis • ' + offer.bankTag;
        } else if (selectedCartStore === 'Supermercados Stock') {
          basePrice = (prod.stores && prod.stores['Supermercados Stock']) ? prod.stores['Supermercados Stock'] : prod.regularPrice;
          const offer = calculateStoreOffer('Supermercados Stock', basePrice, selectedDay);
          finalPrice = offer.finalPrice;
          storeBadgeTxt = '🛒 Supermercados Stock • ' + offer.bankTag;
        } else {
          basePrice = (prod.stores && prod.stores['Biggie Express']) ? prod.stores['Biggie Express'] : prod.regularPrice;
          const isAlcohol = prod.name.toLowerCase().includes('cerveza') || prod.name.toLowerCase().includes('michelob') || prod.name.toLowerCase().includes('vino');
          const offer = isAlcohol 
            ? { finalPrice: basePrice, bankTag: 'Precio Góndola' } 
            : calculateStoreOffer('Biggie Express', basePrice, selectedDay);
          finalPrice = offer.finalPrice;
          storeBadgeTxt = '🏪 Biggie Express • ' + offer.bankTag;
        }

        return `
          <div class="p-3 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-between space-x-3">
            <div class="w-12 h-12 rounded-xl bg-white/5 border border-white/5 p-1 shrink-0 flex items-center justify-center overflow-hidden">
              <img src="${prod.image}" class="max-h-full max-w-full object-contain" alt="${prod.name}" onerror="this.src='https://static.app.biggie.com.py/images/products/7840127000124.jpg'">
            </div>

            <div class="flex-1 min-w-0">
              <h4 class="text-xs font-extrabold text-white truncate">${prod.name}</h4>
              <p class="text-[10px] text-emerald-400 font-bold truncate">${storeBadgeTxt}</p>
              <div class="flex items-baseline space-x-1.5 mt-0.5">
                <span class="text-xs font-black text-white">Gs. ${finalPrice.toLocaleString('es-PY')}</span>
                ${basePrice > finalPrice ? `<span class="text-[10px] text-slate-500 line-through">Gs. ${basePrice.toLocaleString('es-PY')}</span>` : ''}
              </div>
            </div>

            <!-- Stepper interactivo [-] [qty] [+] -->
            <div class="flex items-center space-x-1.5 bg-slate-950 p-1 rounded-xl border border-slate-800 shrink-0">
              <button onclick="decrementCart(${k})" class="w-6 h-6 rounded-lg bg-slate-800 text-slate-300 hover:text-white flex items-center justify-center font-bold text-xs active:scale-90 transition">-</button>
              <span class="text-xs font-black text-white px-1">${qty}</span>
              <button onclick="flyToCart(${k}, null)" class="w-6 h-6 rounded-lg bg-emerald-500 text-white flex items-center justify-center font-bold text-xs active:scale-90 transition">+</button>
            </div>
          </div>
        `;
      }).join('');
    }
"""
    code = code[:start_pos] + new_render_cart + "\n" + code[end_pos:]
    print("Replaced renderCart function.")
else:
    print("ERROR: could not find renderCart bounds")

# 4. Update toggleSplitCart to sync selectedCartStore
old_toggle_split = """    function toggleSplitCart(isChecked) {
      const hint = document.getElementById('splitSavingsHint');
      const container = document.getElementById('splitCartBreakdownContainer');
      const plan = getSplitPlan();
      if (isChecked) {
        hint.innerHTML = '✨ ¡Modo Split Activo! Biggie: 2 productos + Superseis: 1 producto';
        if (container) {
          renderSplitBreakdown();
          container.classList.remove('hidden');
        }
        showToast('✂️ Optimización Multi-Supermercado activada');
      } else {
        hint.innerHTML = 'Comprando en ' + (plan.storesCount || 2) + ' súper ahorras Gs. ' + (plan.extraSavings || 14500).toLocaleString('es-PY') + ' extra';
        if (container) {
          container.classList.add('hidden');
        }
      }
    }"""

new_toggle_split = """    function toggleSplitCart(isChecked) {
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

old_toggle_split_norm = old_toggle_split.replace('\r\n', '\n')
new_toggle_split_norm = new_toggle_split.replace('\r\n', '\n')
code_norm = code.replace('\r\n', '\n')

if old_toggle_split_norm in code_norm:
    code_norm = code_norm.replace(old_toggle_split_norm, new_toggle_split_norm)
    print("Replaced toggleSplitCart.")

with open('scripts/build_html.py', 'w', encoding='utf-8') as f:
    f.write(code_norm)

print("build_html.py fully patched.")

