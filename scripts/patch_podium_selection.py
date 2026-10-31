# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Podium HTML block
old_podium_html = """          <!-- Tarjetas del Podium -->
          <div class="grid grid-cols-3 gap-2 pt-1">
            
            <!-- 2° Lugar (Plata) -->
            <div class="p-2.5 rounded-2xl bg-slate-900/80 border border-slate-800 text-center flex flex-col justify-between">
              <span class="text-base">🥈</span>
              <div>
                <p class="text-[11px] font-black text-slate-200 mt-1">Superseis</p>
                <p id="podium2Price" class="text-xs font-black text-slate-300 mt-0.5">Gs. 72.800</p>
              </div>
              <span class="text-[9px] text-slate-500 mt-1 font-bold">+ Gs. 5.200</span>
            </div>

            <!-- 1° Lugar (Oro - Ganador) -->
            <div class="p-2.5 rounded-2xl bg-emerald-500/20 border-2 border-emerald-500 text-center flex flex-col justify-between relative shadow-lg shadow-emerald-500/20 scale-105">
              <span class="text-lg">👑</span>
              <div>
                <span class="text-[9px] font-black uppercase px-1.5 py-0.5 rounded-full bg-emerald-500 text-white">Más Barato</span>
                <p class="text-xs font-black text-white mt-1">Biggie Express</p>
                <p id="podium1Price" class="text-xs font-black text-emerald-400 mt-0.5">Gs. 67.600</p>
              </div>
              <span id="podium1Badge" class="text-[9px] text-emerald-300 mt-1 font-bold">con ueno/Zeta</span>
            </div>

            <!-- 3° Lugar (Bronce) -->
            <div class="p-2.5 rounded-2xl bg-slate-900/80 border border-slate-800 text-center flex flex-col justify-between">
              <span class="text-base">🥉</span>
              <div>
                <p class="text-[11px] font-black text-slate-200 mt-1">Stock</p>
                <p id="podium3Price" class="text-xs font-black text-slate-300 mt-0.5">Gs. 78.400</p>
              </div>
              <span class="text-[9px] text-slate-500 mt-1 font-bold">+ Gs. 10.800</span>
            </div>

          </div>"""

new_podium_html = """          <div class="flex items-center justify-between">
            <div>
              <span class="text-xs font-black uppercase tracking-wider text-emerald-400">Podium de Supermercados</span>
              <p class="text-[10px] text-slate-400 font-medium">Toca un súper para cotizar toda tu lista ahí:</p>
            </div>
            <span id="podiumModeBadge" class="text-[9px] font-black uppercase px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">100% Biggie</span>
          </div>

          <!-- Tarjetas del Podium (Clickables e Interactivas) -->
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

# 2. Update Header of Podium in HTML
old_podium_header = """          <div class="flex items-center justify-between">
            <span class="text-xs font-black uppercase tracking-wider text-emerald-400">Podium de Ahorro en tu Carrito</span>
            <span class="text-[10px] text-slate-400 font-bold">Misma lista, 3 súper</span>
          </div>"""

# 3. Add cartFinalStoreLabel in Total Summary
old_total_summary = """            <div class="pt-2 border-t border-slate-800 flex justify-between items-baseline">
              <span class="text-sm font-black text-white">Total a Pagar Hoy:</span>
              <span id="cartFinalTotal" class="text-lg font-black text-emerald-400">Gs. 67.600</span>
            </div>"""

new_total_summary = """            <div class="pt-2 border-t border-slate-800 flex justify-between items-baseline">
              <div>
                <span class="text-sm font-black text-white">Total a Pagar Hoy:</span>
                <span id="cartFinalStoreLabel" class="text-[10px] text-emerald-400 font-bold block">100% en Biggie Express</span>
              </div>
              <span id="cartFinalTotal" class="text-lg font-black text-emerald-400">Gs. 67.600</span>
            </div>"""

html_norm = html.replace('\r\n', '\n')
old_podium_header_norm = old_podium_header.replace('\r\n', '\n')
old_podium_html_norm = old_podium_html.replace('\r\n', '\n')
old_total_summary_norm = old_total_summary.replace('\r\n', '\n')

if old_podium_header_norm in html_norm and old_podium_html_norm in html_norm:
    # replace both header and podium cards
    combined_old = old_podium_header_norm + "\n\n" + old_podium_html_norm
    combined_new = new_podium_html.replace('\r\n', '\n')
    html_norm = html_norm.replace(combined_old, combined_new)
    print("SUCCESS: Replaced podium HTML")
else:
    print("WARNING: Exact podium HTML match failed, trying separate replacement")
    if old_podium_html_norm in html_norm:
        html_norm = html_norm.replace(old_podium_html_norm, new_podium_html.replace('\r\n', '\n'))
        print("SUCCESS: Replaced podium cards HTML")

if old_total_summary_norm in html_norm:
    html_norm = html_norm.replace(old_total_summary_norm, new_total_summary.replace('\r\n', '\n'))
    print("SUCCESS: Replaced total summary HTML")

with open('scripts/build_html.py', 'w', encoding='utf-8') as f:
    f.write(html_norm)

print("HTML template patched.")

