with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    content = f.read()

target_start = '    // RENDERIZADO DE LA GÓNDOLA 2X2\n    function renderGrid() {'
target_end = '        `;\n      }).join(\'\');\n    }'

idx1 = content.find(target_start)
assert idx1 != -1, "target_start not found"
idx2 = content.find(target_end, idx1)
assert idx2 != -1, "target_end not found"
idx2 += len(target_end)

new_block = """    // RENDERIZADO DE LA GÓNDOLA 2X2 CON SCROLL INFINITO DINÁMICO
    let currentGridPage = 1;
    const GRID_PAGE_SIZE = 20;
    let currentFilteredList = [];
    let isInfiniteScrollLoading = false;

    function renderProductCardHtml(prod) {
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
      const isFav = favorites.includes(prod.id);
      const starBtn = `
        <button onclick="event.stopPropagation(); toggleFavorite(${prod.id}, event);" class="w-7 h-7 rounded-full ${isFav ? 'bg-amber-400/20 text-amber-400 border border-amber-400/40 shadow-sm shadow-amber-400/20 font-black' : 'bg-slate-800/80 text-slate-400 hover:text-amber-400 border border-slate-700/60 font-medium'} text-xs flex items-center justify-center transition-all hover:scale-110 active:scale-90" title="${isFav ? 'Quitar de favoritos' : 'Guardar en favoritos'}">
          <span>${isFav ? '★' : '☆'}</span>
        </button>
      `;

      return `
        <div onclick="openProductDetail(${realIdx})" class="p-3 rounded-3xl glass-card hover:border-emerald-500/50 transition-all duration-300 flex flex-col justify-between relative group cursor-pointer shadow-md hover:shadow-emerald-500/10 active:scale-[0.98]">
          
          <div class="flex items-center justify-between mb-2 z-10">
            ${discountBadge}
            ${starBtn}
          </div>

          <div class="w-full h-28 flex items-center justify-center p-2 rounded-2xl bg-white/5 relative overflow-hidden group-hover:scale-105 transition-transform duration-300">
            <img src="${prod.image}" class="max-h-full max-w-full object-contain drop-shadow" alt="${prod.name}" onerror="this.src='https://static.app.biggie.com.py/images/products/7840127000124.jpg'">
          </div>

          <div class="mt-2.5">
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
            </div>
            
            <div class="p-1.5 rounded-xl ${offer.discountPct > 0 ? 'bg-emerald-500/15 border border-emerald-500/30' : 'bg-slate-900 border border-slate-800'} flex items-center justify-between">
              <span class="text-[10px] font-bold ${offer.discountPct > 0 ? 'text-emerald-300' : 'text-slate-400'} truncate max-w-[95px]">${cardTag}</span>
              <span class="text-xs font-black ${offer.discountPct > 0 ? 'text-emerald-400' : 'text-white'} shrink-0">Gs. ${displayBestPrice.toLocaleString('es-PY')}</span>
            </div>
          </div>

          <button onclick="event.stopPropagation(); flyToCart(${realIdx}, event)" class="mt-2.5 w-full py-1.5 rounded-xl bg-slate-800 hover:bg-emerald-500 text-slate-300 hover:text-white text-xs font-extrabold flex items-center justify-center space-x-1.5 transition-all shadow active:scale-95">
            <span class="text-sm">+</span>
            <span>Sumar a Lista</span>
          </button>

        </div>
      `;
    }

    function renderGrid(resetPage = true) {
      const container = document.getElementById('productGrid');
      if (!container) return;

      if (resetPage) {
        currentGridPage = 1;
      }

      const q = currentSearch.toLowerCase().trim();
      currentFilteredList = products.filter(p => {
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
      });

      const countEl = document.getElementById('resultsCount');
      if (countEl) countEl.innerText = currentFilteredList.length;

      // Actualizar contador del chip de favoritos
      const favBadge = document.getElementById('favCountBadge');
      if (favBadge) {
        if (favorites.length > 0) {
          favBadge.innerText = favorites.length;
          favBadge.classList.remove('hidden');
        } else {
          favBadge.classList.add('hidden');
        }
      }

      if (currentFilteredList.length === 0) {
        if (showOnlyFavorites) {
          container.innerHTML = `
            <div class="col-span-2 py-12 text-center text-slate-500 glass-card rounded-3xl p-6">
              <span class="text-4xl">⭐</span>
              <p class="text-xs font-black text-white mt-2">No tienes productos favoritos aún</p>
              <p class="text-[10px] text-slate-400 mt-1">Toca la estrella en los productos de la góndola para verlos aquí rápidamente</p>
              <button onclick="toggleFavoritesOnly()" class="mt-3 px-3 py-1.5 rounded-xl bg-amber-500/20 text-amber-300 font-bold text-xs border border-amber-500/30">
                Ver toda la Góndola
              </button>
            </div>
          `;
          return;
        }

        container.innerHTML = `
          <div class="col-span-2 py-12 text-center text-slate-500">
            <span class="text-4xl">🔍</span>
            <p class="text-xs font-bold mt-2">No se encontraron productos</p>
            <p class="text-[10px] text-slate-600">Prueba con otra palabra o limpia los filtros</p>
            <button onclick="clearSearch(); selectCategory('', '🗂️', 'Categorías'); selectStore('', '🏬', 'Supermercados')" class="mt-3 px-3 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-400 font-bold text-xs border border-emerald-500/30">
              Restablecer filtros
            </button>
          </div>
        `;
        return;
      }

      const initialBatch = currentFilteredList.slice(0, currentGridPage * GRID_PAGE_SIZE);
      let html = initialBatch.map(renderProductCardHtml).join('');

      if (initialBatch.length < currentFilteredList.length) {
        html += `
          <div id="infiniteScrollSentinel" class="col-span-2 py-6 flex flex-col items-center justify-center space-y-1.5 text-center">
            <div class="flex items-center space-x-2 text-xs font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-4 py-2 rounded-2xl shadow-sm">
              <span class="w-3.5 h-3.5 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin"></span>
              <span>Cargando más productos en ${currentStore || 'góndola'}...</span>
            </div>
            <p id="infiniteScrollProgress" class="text-[10px] text-slate-500">Mostrando ${initialBatch.length} de ${currentFilteredList.length} productos verificados</p>
          </div>
        `;
      }

      container.innerHTML = html;
      initInfiniteScrollListener();
    }

    function loadMoreProducts() {
      if (isInfiniteScrollLoading) return;
      if (!currentFilteredList || currentFilteredList.length === 0) return;
      
      const currentRendered = currentGridPage * GRID_PAGE_SIZE;
      if (currentRendered >= currentFilteredList.length) return;

      isInfiniteScrollLoading = true;
      const nextBatch = currentFilteredList.slice(currentRendered, currentRendered + GRID_PAGE_SIZE);
      currentGridPage++;

      const container = document.getElementById('productGrid');
      const sentinel = document.getElementById('infiniteScrollSentinel');
      if (sentinel) sentinel.remove();

      if (container && nextBatch.length > 0) {
        const nextHtml = nextBatch.map(renderProductCardHtml).join('');
        container.insertAdjacentHTML('beforeend', nextHtml);

        const newTotalRendered = Math.min(currentGridPage * GRID_PAGE_SIZE, currentFilteredList.length);
        if (newTotalRendered < currentFilteredList.length) {
          const newSentinelHtml = `
            <div id="infiniteScrollSentinel" class="col-span-2 py-6 flex flex-col items-center justify-center space-y-1.5 text-center">
              <div class="flex items-center space-x-2 text-xs font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-4 py-2 rounded-2xl shadow-sm">
                <span class="w-3.5 h-3.5 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin"></span>
                <span>Cargando más productos en ${currentStore || 'góndola'}...</span>
              </div>
              <p id="infiniteScrollProgress" class="text-[10px] text-slate-500">Mostrando ${newTotalRendered} de ${currentFilteredList.length} productos verificados</p>
            </div>
          `;
          container.insertAdjacentHTML('beforeend', newSentinelHtml);
        }
      }

      setTimeout(() => {
        isInfiniteScrollLoading = false;
      }, 100);
    }

    function initInfiniteScrollListener() {
      const mainEl = document.querySelector('main');
      if (mainEl && !window._hasInfiniteScrollHandler) {
        window._hasInfiniteScrollHandler = true;
        mainEl.addEventListener('scroll', () => {
          if (mainEl.scrollTop + mainEl.clientHeight >= mainEl.scrollHeight - 500) {
            loadMoreProducts();
          }
        });
      }
    }"""

patched_content = content[:idx1] + new_block + content[idx2:]

with open('scripts/build_html.py', 'w', encoding='utf-8') as f:
    f.write(patched_content)

print("Infinite scroll patched into scripts/build_html.py successfully!")

