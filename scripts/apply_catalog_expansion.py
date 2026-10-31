import json

# 1. Copy expanded_products_clean.json to verified_products_clean.json
with open('scripts/expanded_products_clean.json', 'r', encoding='utf-8') as f:
    products_data = json.load(f)

with open('scripts/verified_products_clean.json', 'w', encoding='utf-8') as f:
    json.dump(products_data, f, indent=2, ensure_ascii=False)

print(f"Updated verified_products_clean.json with {len(products_data)} products!")

# 2. Patch build_html.py
with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace matchesStore in renderGrid
old_grid_filter = """      const q = currentSearch.toLowerCase().trim();
      const filtered = products.filter(p => {
        const matchesQuery = !q || 
          p.name.toLowerCase().includes(q) || 
          p.brand.toLowerCase().includes(q) || 
          (p.image && p.image.includes(q)) || 
          (p.category && p.category.toLowerCase().includes(q));
        const matchesCat = !currentCategory || p.category === currentCategory;
        const matchesStore = !currentStore || p.store.toLowerCase().includes(currentStore.toLowerCase());
        const matchesFav = !showOnlyFavorites || favorites.includes(p.id);
        return matchesQuery && matchesCat && matchesStore && matchesFav;
      });"""

new_grid_filter = """      const q = currentSearch.toLowerCase().trim();
      const filtered = products.filter(p => {
        const matchesQuery = !q || 
          p.name.toLowerCase().includes(q) || 
          p.brand.toLowerCase().includes(q) || 
          (p.image && p.image.includes(q)) || 
          (p.category && p.category.toLowerCase().includes(q));
        const matchesCat = !currentCategory || p.category === currentCategory;
        const matchesStore = !currentStore || 
          (p.stores && (p.stores[currentStore] !== undefined || Object.keys(p.stores).some(k => k.toLowerCase().includes(currentStore.toLowerCase())))) ||
          (p.store && p.store.toLowerCase().includes(currentStore.toLowerCase()));
        const matchesFav = !showOnlyFavorites || favorites.includes(p.id);
        return matchesQuery && matchesCat && matchesStore && matchesFav;
      });"""

assert old_grid_filter in code, "old_grid_filter not found in build_html.py"
code = code.replace(old_grid_filter, new_grid_filter)

old_card_calc = """      container.innerHTML = filtered.map((prod, idx) => {
        const realIdx = products.findIndex(p => p.id === prod.id && p.name === prod.name);
        const offer = calculateProductOffer(prod, selectedDay);
        const displayBestPrice = offer.finalPrice;
        const cardTag = '💳 ' + offer.bankTag;
        const discountBadge = offer.discountPct > 0 ? `<span class="text-[9px] font-black uppercase px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center space-x-1"><span>🔥</span><span>-${offer.discountPct}%</span></span>` : '<span></span>';
        const isFav = favorites.includes(prod.id);"""

new_card_calc = """      container.innerHTML = filtered.map((prod, idx) => {
        const realIdx = products.findIndex(p => p.id === prod.id && p.name === prod.name);
        
        // Si hay un filtro de supermercado activo, mostrar precio y nombre de ese supermercado
        let storeForCard = prod.store;
        let regularPriceForCard = prod.regularPrice;
        if (currentStore && prod.stores) {
          const matchingKey = Object.keys(prod.stores).find(k => k.toLowerCase().includes(currentStore.toLowerCase()));
          if (matchingKey && prod.stores[matchingKey]) {
            storeForCard = matchingKey;
            regularPriceForCard = prod.stores[matchingKey];
          }
        }
        
        const offer = calculateStoreOffer(storeForCard, regularPriceForCard, selectedDay);
        const displayBestPrice = offer.finalPrice;
        const cardTag = '💳 ' + offer.bankTag;
        const discountBadge = offer.discountPct > 0 ? `<span class="text-[9px] font-black uppercase px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center space-x-1"><span>🔥</span><span>-${offer.discountPct}%</span></span>` : '<span></span>';
        const isFav = favorites.includes(prod.id);"""

assert old_card_calc in code, "old_card_calc not found in build_html.py"
code = code.replace(old_card_calc, new_card_calc)

old_card_markup = """            <div class="mt-2.5">
              <p class="text-[10px] font-extrabold text-slate-400 truncate">${prod.brand} • ${prod.store}</p>
              <h3 class="text-xs font-black text-white line-clamp-2 leading-tight mt-0.5">${prod.name}</h3>
              <div class="mt-1 flex items-center space-x-1 text-[10px] text-emerald-400 font-bold">
                <span class="text-xs">🏬</span>
                <span>Toca para ver en 5 súper ▾</span>
              </div>
            </div>

            <div class="mt-2.5 pt-2 border-t border-white/5 space-y-1.5">
              <div class="flex items-baseline justify-between">
                <span class="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider">Precio real:</span>
                <span class="text-xs font-black text-slate-200">Gs. ${prod.regularPrice.toLocaleString('es-PY')}</span>
              </div>"""

new_card_markup = """            <div class="mt-2.5">
              <p class="text-[10px] font-extrabold text-slate-400 truncate">${prod.brand} • ${storeForCard}</p>
              <h3 class="text-xs font-black text-white line-clamp-2 leading-tight mt-0.5">${prod.name}</h3>
              <div class="mt-1 flex items-center space-x-1 text-[10px] text-emerald-400 font-bold">
                <span class="text-xs">🏬</span>
                <span>Toca para ver en 5 súper ▾</span>
              </div>
            </div>

            <div class="mt-2.5 pt-2 border-t border-white/5 space-y-1.5">
              <div class="flex items-baseline justify-between">
                <span class="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider">Precio real:</span>
                <span class="text-xs font-black text-slate-200">Gs. ${regularPriceForCard.toLocaleString('es-PY')}</span>
              </div>"""

assert old_card_markup in code, "old_card_markup not found in build_html.py"
code = code.replace(old_card_markup, new_card_markup)

# Add Limpieza and Frutas to categoryModalSheet
old_cat_buttons = """        <button onclick="selectCategory('Snacks', '🍟', 'Snacks')" class="p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center space-x-2 text-left transition">
          <span class="text-base">🍟</span>
          <span class="text-xs font-extrabold text-white">Snacks & Papas</span>
        </button>
      </div>"""

new_cat_buttons = """        <button onclick="selectCategory('Snacks', '🍟', 'Snacks')" class="p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center space-x-2 text-left transition">
          <span class="text-base">🍟</span>
          <span class="text-xs font-extrabold text-white">Snacks & Papas</span>
        </button>
        <button onclick="selectCategory('Limpieza', '🧼', 'Limpieza')" class="p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center space-x-2 text-left transition">
          <span class="text-base">🧼</span>
          <span class="text-xs font-extrabold text-white">Limpieza & Hogar</span>
        </button>
        <button onclick="selectCategory('Frutas', '🍎', 'Frutas y Verduras')" class="p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center space-x-2 text-left transition">
          <span class="text-base">🍎</span>
          <span class="text-xs font-extrabold text-white">Frutas & Verduras</span>
        </button>
      </div>"""

assert old_cat_buttons in code, "old_cat_buttons not found in build_html.py"
code = code.replace(old_cat_buttons, new_cat_buttons)

with open('scripts/build_html.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("build_html.py patched successfully with expanded catalog and multi-store filtering!")
