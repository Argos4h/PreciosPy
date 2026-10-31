# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update Podium Container in HTML
old_podium_container = """          <!-- Tarjetas del Podium (Clickables e Interactivas) -->
          <div class="grid grid-cols-3 gap-2 pt-1">
            
            <!-- 2° Lugar: Superseis -->
            <div id="podiumCardSuperseis" onclick="selectPodiumStore('Superseis')" class="p-2.5 rounded-2xl bg-slate-900/80 border border-slate-800 text-center flex flex-col justify-between cursor-pointer hover:border-slate-700 active:scale-95 transition-all duration-200">
              <span class="text-base">🥈</span>
              <div>
                <p class="text-[11px] font-black text-slate-200 mt-1">Superseis</p>
                <p id="podium2Price" class="text-xs font-black text-slate-300 mt-0.5">Gs. 94.720</p>
              </div>
              <span id="podiumSuperseisStatus" class="text-[9px] text-slate-500 mt-1 font-bold">Tocar para ver</span>
            </div>

            <!-- 1° Lugar: Biggie Express -->
            <div id="podiumCardBiggie" onclick="selectPodiumStore('Biggie Express')" class="p-2.5 rounded-2xl bg-emerald-500/20 border-2 border-emerald-500 text-center flex flex-col justify-between relative shadow-lg shadow-emerald-500/20 scale-105 cursor-pointer ring-2 ring-emerald-400/50 hover:border-emerald-400 active:scale-95 transition-all duration-200">
              <span class="text-lg">👑</span>
              <div>
                <span id="podium1Badge" class="text-[9px] font-black uppercase px-1.5 py-0.5 rounded-full bg-emerald-500 text-white">Más Rápido</span>
                <p class="text-xs font-black text-white mt-1">Biggie Express</p>
                <p id="podium1Price" class="text-xs font-black text-emerald-400 mt-0.5">Gs. 98.628</p>
              </div>
              <span id="podiumBiggieStatus" class="text-[9px] text-emerald-300 mt-1 font-bold">✓ Viendo aquí</span>
            </div>

            <!-- 3° Lugar: Stock -->
            <div id="podiumCardStock" onclick="selectPodiumStore('Supermercados Stock')" class="p-2.5 rounded-2xl bg-slate-900/80 border border-slate-800 text-center flex flex-col justify-between cursor-pointer hover:border-slate-700 active:scale-95 transition-all duration-200">
              <span class="text-base">🥉</span>
              <div>
                <p class="text-[11px] font-black text-slate-200 mt-1">Stock</p>
                <p id="podium3Price" class="text-xs font-black text-slate-300 mt-0.5">Gs. 93.360</p>
              </div>
              <span id="podiumStockStatus" class="text-[9px] text-slate-500 mt-1 font-bold">Tocar para ver</span>
            </div>

          </div>"""

new_podium_container = """          <!-- Tarjetas del Podium (Dinámicas ordenadas por donde se gasta menos) -->
          <div id="podiumCardsGrid" class="grid grid-cols-3 gap-2 pt-1 items-end">
            <!-- Render dinámico desde renderCart(): 2° Lugar (Izq), 1° TOP (Centro), 3° Lugar (Der) -->
          </div>"""

old_norm = old_podium_container.replace('\r\n', '\n')
new_norm = new_podium_container.replace('\r\n', '\n')
code_norm = code.replace('\r\n', '\n')

if old_norm in code_norm:
    code_norm = code_norm.replace(old_norm, new_norm)
    print("Replaced podium HTML with dynamic podiumCardsGrid.")
else:
    print("WARNING: old_podium_container not found, checking...")

# 2. Update renderCart() with dynamic ranking logic
old_calc_block = """      // Actualizar precios en las 3 tarjetas del Podium
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
      }"""

new_calc_block = """      // 2. Ranking Dinámico: Ordenar los 3 súper por menor gasto (EL TOP ES DONDE MENOS GASTAS)
      const storeRanks = [
        {
          key: 'Biggie Express',
          name: 'Biggie Express',
          shortName: 'Biggie',
          icon: '🏪',
          total: biggieTotal,
          cardId: 'podiumCardBiggie',
          statusId: 'podiumBiggieStatus',
          colorBorder: 'border-emerald-500',
          bgActive: 'bg-emerald-500/20',
          ringColor: 'ring-emerald-400/50',
          textAccent: 'text-emerald-400'
        },
        {
          key: 'Superseis',
          name: 'Superseis',
          shortName: 'Superseis',
          icon: '🏬',
          total: superseisTotal,
          cardId: 'podiumCardSuperseis',
          statusId: 'podiumSuperseisStatus',
          colorBorder: 'border-amber-500',
          bgActive: 'bg-amber-500/20',
          ringColor: 'ring-amber-400/50',
          textAccent: 'text-amber-400'
        },
        {
          key: 'Supermercados Stock',
          name: 'Supermercados Stock',
          shortName: 'Stock',
          icon: '🛒',
          total: stockTotal,
          cardId: 'podiumCardStock',
          statusId: 'podiumStockStatus',
          colorBorder: 'border-blue-500',
          bgActive: 'bg-blue-500/20',
          ringColor: 'ring-blue-400/50',
          textAccent: 'text-blue-400'
        }
      ];

      // Ordenar ascendentemente por total: el índice 0 es EL TOP (donde menos se gasta)
      storeRanks.sort((a, b) => a.total - b.total);

      const rank1 = storeRanks[0]; // 🥇 1° LUGAR — TOP DONDE SE GASTA MENOS
      const rank2 = storeRanks[1]; // 🥈 2° Lugar
      const rank3 = storeRanks[2]; // 🥉 3° Lugar

      // Si no hay súper seleccionado previamente, seleccionar el TOP por defecto
      if (!selectedCartStore) {
        selectedCartStore = rank1.key;
      }

      const isSplitActive = (selectedCartStore === 'split');

      // 3. Renderizado del Podium: 2° Lugar (Izq), 1° TOP (Centro más alto con corona), 3° Lugar (Der)
      const podiumGrid = document.getElementById('podiumCardsGrid');
      if (podiumGrid) {
        const createCardHtml = (store, place) => {
          const isSelected = (selectedCartStore === store.key);
          const isTop = (place === 1);
          const medal = isTop ? '👑' : (place === 2 ? '🥈' : '🥉');
          const badgeText = isTop ? 'TOP 1° AHORRO' : (place === 2 ? '2° Lugar' : '3° Lugar');
          const badgeClass = isTop 
            ? 'bg-emerald-500 text-slate-950 shadow-sm animate-pulse' 
            : 'bg-slate-800 text-slate-300 border border-slate-700';

          const diffText = isTop 
            ? '<span class="text-[8.5px] font-extrabold text-emerald-300 block">Menor gasto total</span>'
            : `<span class="text-[8.5px] font-bold text-rose-400 block">+ Gs. ${(store.total - rank1.total).toLocaleString('es-PY')}</span>`;

          const cardBase = isTop
            ? `p-2.5 rounded-2xl ${isSelected ? store.bgActive + ' border-2 ' + store.colorBorder + ' ring-2 ' + store.ringColor + ' shadow-lg shadow-emerald-500/20' : 'bg-emerald-500/15 border-2 border-emerald-500/60 shadow-md'} text-center flex flex-col justify-between relative scale-105 cursor-pointer active:scale-95 transition-all z-10`
            : `p-2.5 rounded-2xl ${isSelected ? store.bgActive + ' border-2 ' + store.colorBorder + ' ring-2 ' + store.ringColor + ' shadow-lg' : 'bg-slate-900/80 border border-slate-800'} text-center flex flex-col justify-between cursor-pointer hover:border-slate-700 active:scale-95 transition-all`;

          let statusHtml = '';
          if (isSplitActive) {
            if (store.key === 'Biggie Express') statusHtml = '<span class="text-[9px] text-emerald-400 font-black">2 prod. en split</span>';
            else if (store.key === 'Superseis') statusHtml = '<span class="text-[9px] text-amber-400 font-black">1 prod. en split</span>';
            else statusHtml = '<span class="text-[9px] text-slate-500 font-semibold">Tocar para ver</span>';
          } else {
            statusHtml = isSelected 
              ? `<span class="text-[9px] ${store.textAccent} font-black">✓ Viendo aquí</span>` 
              : '<span class="text-[9px] text-slate-500 font-semibold">Tocar para ver</span>';
          }

          const priceId = isTop ? 'podium1Price' : (place === 2 ? 'podium2Price' : 'podium3Price');

          return `
            <div id="${store.cardId}" onclick="selectPodiumStore('${store.key}')" class="${cardBase}">
              <div class="flex items-center justify-center space-x-1">
                <span class="${isTop ? 'text-lg drop-shadow' : 'text-base'}">${medal}</span>
                <span class="text-[8.5px] font-black uppercase px-1.5 py-0.5 rounded-full ${badgeClass}">${badgeText}</span>
              </div>
              <div class="my-1">
                <p class="${isTop ? 'text-xs font-black text-white' : 'text-[11px] font-black text-slate-200'} mt-0.5">${store.name}</p>
                <p id="${priceId}" class="${isTop ? 'text-sm font-black text-emerald-400' : 'text-xs font-black text-slate-300'} mt-0.5">Gs. ${store.total.toLocaleString('es-PY')}</p>
                ${diffText}
              </div>
              <div class="pt-1 border-t border-white/5">
                <span id="${store.statusId}">${statusHtml}</span>
              </div>
            </div>
          `;
        };

        podiumGrid.innerHTML = createCardHtml(rank2, 2) + createCardHtml(rank1, 1) + createCardHtml(rank3, 3);
      }

      // Actualizar badge superior del modo
      const modeBadge = document.getElementById('podiumModeBadge');
      if (modeBadge) {
        if (isSplitActive) {
          modeBadge.innerText = '✂️ Ahorro Dividido';
          modeBadge.className = 'text-[9px] font-black uppercase px-2 py-0.5 rounded-full bg-emerald-500 text-slate-950 shadow-sm animate-pulse';
        } else {
          const activeStoreObj = storeRanks.find(s => s.key === selectedCartStore) || rank1;
          modeBadge.innerText = '100% ' + activeStoreObj.shortName;
          modeBadge.className = 'text-[9px] font-black uppercase px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700';
        }
      }"""

old_calc_norm = old_calc_block.replace('\r\n', '\n')
new_calc_norm = new_calc_block.replace('\r\n', '\n')

if old_calc_norm in code_norm:
    code_norm = code_norm.replace(old_calc_norm, new_calc_norm)
    print("Replaced renderCart podium ranking logic.")
else:
    print("ERROR: old_calc_block not found in code_norm")

with open('scripts/build_html.py', 'w', encoding='utf-8') as f:
    f.write(code_norm)

print("Patching complete.")

