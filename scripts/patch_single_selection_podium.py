# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Buscamos la definición de createCardHtml en scripts/build_html.py
old_create_card = """        const createCardHtml = (store, place) => {
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
        };"""

new_create_card = """        const createCardHtml = (store, place) => {
          const isSelected = (selectedCartStore === store.key);
          const isTop = (place === 1);
          const medal = isTop ? '👑' : (place === 2 ? '🥈' : '🥉');
          const badgeText = isTop ? 'TOP 1° AHORRO' : (place === 2 ? '2° Lugar' : '3° Lugar');

          let cardBase = '';
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
          }

          const diffText = isTop 
            ? `<span class="text-[8.5px] font-bold ${isSelected ? 'text-emerald-300' : 'text-slate-400'} block">Menor gasto total</span>`
            : `<span class="text-[8.5px] font-bold ${isSelected ? 'text-rose-300' : 'text-slate-500'} block">+ Gs. ${(store.total - rank1.total).toLocaleString('es-PY')}</span>`;

          const priceId = isTop ? 'podium1Price' : (place === 2 ? 'podium2Price' : 'podium3Price');
          const nameClass = isSelected ? 'text-xs font-black text-white' : 'text-[11px] font-bold text-slate-300';
          const priceClass = isSelected ? `text-sm font-black ${store.textAccent}` : 'text-xs font-bold text-slate-300';

          return `
            <div id="${store.cardId}" onclick="selectPodiumStore('${store.key}')" class="${cardBase}">
              <div class="flex items-center justify-center space-x-1">
                <span class="${isSelected ? 'text-lg drop-shadow' : 'text-base opacity-80'}">${medal}</span>
                <span class="text-[8.5px] uppercase px-1.5 py-0.5 rounded-full ${badgeClass}">${badgeText}</span>
              </div>
              <div class="my-1">
                <p class="${nameClass} mt-0.5">${store.name}</p>
                <p id="${priceId}" class="${priceClass} mt-0.5">Gs. ${store.total.toLocaleString('es-PY')}</p>
                ${diffText}
              </div>
              <div class="pt-1 border-t border-white/5">
                <span id="${store.statusId}">${statusHtml}</span>
              </div>
            </div>
          `;
        };"""

code_norm = code.replace('\r\n', '\n')
old_norm = old_create_card.replace('\r\n', '\n')
new_norm = new_create_card.replace('\r\n', '\n')

if old_norm in code_norm:
    code_norm = code_norm.replace(old_norm, new_norm)
    with open('scripts/build_html.py', 'w', encoding='utf-8') as f:
        f.write(code_norm)
    print("SUCCESS: scripts/build_html.py updated so ONLY the selected top looks selected!")
else:
    print("ERROR: old_create_card block not matched.")

