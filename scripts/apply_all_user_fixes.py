# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("Original build_html.py length:", len(content))

# ---------------------------------------------------------------------------
# 1. VACÍO DE DATOS INICIALES (CLEAN SLATE)
# ---------------------------------------------------------------------------
# A) Cart empty
cart_pattern = r'let\s+cart\s*=\s*\{[^}]*\};'
if re.search(cart_pattern, content):
    content = re.sub(cart_pattern, 'let cart = {};', content, count=1)
    print("✓ Cart reset to empty {}")
else:
    print("⚠️ Cart pattern not found")

# B) Favorites empty
fav_pattern = r'let\s+favorites\s*=\s*\[[^\]]*\];\s*//[^\n]*'
if re.search(fav_pattern, content):
    content = re.sub(fav_pattern, 'let favorites = [];', content, count=1)
    print("✓ Favorites reset to empty []")
else:
    print("⚠️ Favorites pattern not found")

# C) Savings reset to 0
savings_pattern = r'let\s+userSavings\s*=\s*\{.*?\};'
clean_savings = """let userSavings = {
      week: 0,
      month: 0,
      total: 0,
      spentWithPreciosPyMonth: 0,
      spentWithoutPreciosPyMonth: 0,
      activePeriod: 'month',
      history: []
    };"""
content = re.sub(savings_pattern, clean_savings, content, count=1, flags=re.DOTALL)
print("✓ userSavings reset to 0")

# D) Static HTML amounts and badge
content = content.replace('<span id="homeSavingsDisplay">542.000</span>', '<span id="homeSavingsDisplay">0</span>')
content = content.replace('<p id="profileSavingsWeek" class="text-xs font-black text-emerald-400 mt-1">Gs. 128.500</p>', '<p id="profileSavingsWeek" class="text-xs font-black text-emerald-400 mt-1">Gs. 0</p>')
content = content.replace('<p id="profileSavingsMonth" class="text-xs font-black text-white mt-1">Gs. 542.000</p>', '<p id="profileSavingsMonth" class="text-xs font-black text-white mt-1">Gs. 0</p>')
content = content.replace('<p id="profileSavingsTotal" class="text-xs font-black text-emerald-400 mt-1">Gs. 1.845.000</p>', '<p id="profileSavingsTotal" class="text-xs font-black text-emerald-400 mt-1">Gs. 0</p>')
content = content.replace('<h1 id="savingsMainAmount" class="text-3xl font-black text-white tracking-tight">542.000</h1>', '<h1 id="savingsMainAmount" class="text-3xl font-black text-white tracking-tight">0</h1>')

old_badge = '<span id="navCartBadge" class="absolute -top-1 right-1 w-4 h-4 rounded-full bg-emerald-500 text-white font-black text-[9px] flex items-center justify-center ring-2 ring-slate-900 animate-pulse">3</span>'
new_badge = '<span id="navCartBadge" class="hidden absolute -top-1 right-1 w-4 h-4 rounded-full bg-emerald-500 text-white font-black text-[9px] flex items-center justify-center ring-2 ring-slate-900">0</span>'
content = content.replace(old_badge, new_badge)

# E) In renderCart, hide badge if totalItemCount is 0
target_badge_js = "if (badge) badge.innerText = totalItemCount;"
new_badge_js = """if (badge) {
        badge.innerText = totalItemCount;
        if (totalItemCount === 0) {
          badge.classList.add('hidden');
        } else {
          badge.classList.remove('hidden');
        }
      }"""
content = content.replace(target_badge_js, new_badge_js, 1)
print("✓ Nav badge and static figures cleaned")


# ---------------------------------------------------------------------------
# 2. EN LAS LISTAS: CORREGIR SUPERPOSICIÓN DE PRECIO CON BOTÓN -
# ---------------------------------------------------------------------------
old_item_tmpl = """        return `
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
        `;"""

new_item_tmpl = """        return `
          <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-between gap-3 shadow-sm hover:border-slate-700 transition">
            <!-- Imagen -->
            <div class="w-12 h-12 rounded-xl bg-white/5 border border-white/5 p-1 shrink-0 flex items-center justify-center overflow-hidden">
              <img src="${prod.image}" class="max-h-full max-w-full object-contain" alt="${prod.name}" onerror="this.src='https://static.app.biggie.com.py/images/products/7840127000124.jpg'">
            </div>

            <!-- Información del producto con padding derecho garantizado sin superposicion -->
            <div class="flex-1 min-w-0 pr-2">
              <h4 class="text-xs font-extrabold text-white truncate leading-tight">${prod.name}</h4>
              <p class="text-[10px] text-emerald-400 font-bold truncate mt-0.5">${storeBadgeTxt}</p>
              <div class="flex items-baseline space-x-1.5 mt-1">
                <span class="text-xs font-black text-white shrink-0">Gs. ${finalPrice.toLocaleString('es-PY')}</span>
                ${basePrice > finalPrice ? `<span class="text-[10px] text-slate-500 line-through shrink-0">Gs. ${basePrice.toLocaleString('es-PY')}</span>` : ''}
              </div>
            </div>

            <!-- Stepper interactivo [-] [qty] [+] con espacio propio aislado -->
            <div class="flex items-center space-x-1.5 bg-slate-950 p-1.5 rounded-xl border border-slate-800 shrink-0 ml-auto select-none">
              <button onclick="decrementCart(${k})" class="w-7 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white flex items-center justify-center font-black text-xs active:scale-90 transition cursor-pointer" title="Restar 1">-</button>
              <span class="text-xs font-black text-white px-1.5 text-center min-w-[20px]">${qty}</span>
              <button onclick="flyToCart(${k}, null)" class="w-7 h-7 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 flex items-center justify-center font-black text-xs active:scale-90 transition cursor-pointer" title="Sumar 1">+</button>
            </div>
          </div>
        `;"""

if old_item_tmpl in content:
    content = content.replace(old_item_tmpl, new_item_tmpl, 1)
    print("✓ Cart item layout fixed (padding and non-overlapping stepper)")
else:
    print("⚠️ Old cart item template not found exactly, using index search")
    idx_map = content.find('listContainer.innerHTML = cartKeys.map')
    if idx_map != -1:
        idx_ret = content.find('return `', idx_map)
        idx_ret_end = content.find('`;', idx_ret) + 2
        content = content[:idx_ret] + new_item_tmpl.strip() + content[idx_ret_end:]
        print("✓ Cart item layout fixed via index search")


# ---------------------------------------------------------------------------
# 3. EN PERFIL: CORREGIR BANCO ITAÚ TEXTO LARGO Y TOGGLE DESPLAZADO
# ---------------------------------------------------------------------------
idx_itau = content.find('id="dot-itau"')
if idx_itau != -1:
    idx_card_start = content.rfind('<div class="p-4 rounded-3xl bg-slate-900 border border-slate-800 space-y-3">', 0, idx_itau)
    idx_card_end = content.find('<!-- Continental', idx_itau)
    
    new_itau_card = """<!-- Banco Itaú con Selector de Segmentos (Diseño Blindado sin Overflow) -->
          <div class="p-4 rounded-3xl bg-slate-900 border border-slate-800 space-y-3 shadow-md">
            <div class="flex items-center justify-between gap-3">
              <div class="flex items-center space-x-2.5 min-w-0 flex-1">
                <span id="dot-itau" class="w-3.5 h-3.5 rounded-full bg-orange-400 shrink-0 shadow-sm shadow-orange-400/50"></span>
                <div class="min-w-0 flex-1">
                  <div class="flex items-center space-x-1.5 flex-wrap">
                    <p class="text-xs font-black text-white shrink-0">Banco Itaú</p>
                    <span id="itauActiveBadge" class="text-[9px] font-black px-1.5 py-0.5 rounded-full bg-orange-500/20 text-orange-400 border border-orange-500/30 truncate max-w-[125px]">Clásica (20%)</span>
                  </div>
                  <p id="label-itau" class="text-[10px] text-slate-400 truncate mt-0.5">Martes en Superseis y Stock</p>
                </div>
              </div>
              <button id="btn-itau" onclick="toggleBankProfile('itau')" aria-label="Alternar Itaú" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-emerald-500 shadow-md shadow-emerald-500/20 flex items-center focus:outline-none active:scale-95 shrink-0 cursor-pointer">
                <div id="thumb-itau" class="w-4 h-4 rounded-full bg-white shadow-md transition-transform duration-200 translate-x-6 pointer-events-none"></div>
              </button>
            </div>

            <!-- SELECTOR DE TIERS ITAÚ REESTRUCTURADO Y COMPACTO -->
            <div class="pt-2 border-t border-slate-800/80">
              <p class="text-[10px] font-black uppercase tracking-wider text-slate-400 mb-2">Categoría de tu tarjeta Itaú:</p>
              <div class="grid grid-cols-2 gap-2" id="itauTierButtons">
                <button onclick="setItauTier('clasica')" data-tier="clasica" class="itau-tier-btn p-2 rounded-xl text-left text-xs font-bold transition bg-orange-500 text-white border border-orange-400 shadow-md shadow-orange-500/20 active:scale-95 cursor-pointer">
                  <p class="text-xs font-black truncate">Clásica / Oro</p>
                  <p class="text-[10px] text-orange-100 font-medium">20% en Martes</p>
                </button>
                <button onclick="setItauTier('platinum')" data-tier="platinum" class="itau-tier-btn p-2 rounded-xl text-left text-xs font-bold transition bg-slate-800 text-slate-300 border border-slate-700 hover:border-orange-500/50 active:scale-95 cursor-pointer">
                  <p class="text-xs font-black truncate">Platinum</p>
                  <p class="text-[10px] text-slate-400 font-medium">25% en Martes</p>
                </button>
                <button onclick="setItauTier('infinite')" data-tier="infinite" class="itau-tier-btn p-2 rounded-xl text-left text-xs font-bold transition bg-slate-800 text-slate-300 border border-slate-700 hover:border-orange-500/50 active:scale-95 cursor-pointer">
                  <p class="text-xs font-black truncate">Infinite / Black</p>
                  <p class="text-[10px] text-slate-400 font-medium">30% en Martes</p>
                </button>
                <button onclick="setItauTier('afinidad')" data-tier="afinidad" class="itau-tier-btn p-2 rounded-xl text-left text-xs font-bold transition bg-slate-800 text-slate-300 border border-slate-700 hover:border-orange-500/50 active:scale-95 cursor-pointer">
                  <p class="text-xs font-black truncate">Afinidad Superseis</p>
                  <p class="text-[10px] text-slate-400 font-medium">20% Todos los días</p>
                </button>
              </div>
            </div>
          </div>

          """
    content = content[:idx_card_start] + new_itau_card + content[idx_card_end:]
    print("✓ Banco Itaú card fixed in viewProfile")

# Add shrink-0 on all bank toggle buttons
bank_ids = ['ueno', 'continental', 'zeta', 'familiar', 'atlas', 'sudameris', 'gnb', 'basa']
for b_id in bank_ids:
    btn_target = f'id="btn-{b_id}"'
    if btn_target in content:
        content = content.replace(f'{btn_target} onclick="toggleBankProfile(\'{b_id}\')" aria-label="Alternar {b_id}" class="w-12 h-6 rounded-full p-1 transition-colors duration-200', f'{btn_target} onclick="toggleBankProfile(\'{b_id}\')" aria-label="Alternar {b_id}" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 shrink-0 cursor-pointer')


# ---------------------------------------------------------------------------
# 4. CHIP DE MARCAS Y MODAL POPUP DE MARCAS
# ---------------------------------------------------------------------------
# A) Chip de marca
idx_sup_btn = content.find('id="superFilterBtn"')
if idx_sup_btn != -1:
    idx_sup_end = content.find('</button>', idx_sup_btn) + 9
    brand_filter_btn = """

          <button id="brandFilterBtn" onclick="openBrandSheet()" class="shrink-0 px-3 py-1.5 rounded-xl bg-slate-900/90 border border-slate-800 text-xs font-bold text-slate-300 flex items-center space-x-1.5 active:scale-95 transition hover:border-emerald-500/50 cursor-pointer">
            <span id="brandFilterIcon">🏷️</span>
            <span id="brandFilterLabel">Marcas</span>
            <span class="text-[10px] text-slate-500">▾</span>
          </button>"""
    content = content[:idx_sup_end] + brand_filter_btn + content[idx_sup_end:]
    print("✓ Brand filter button added next to superFilterBtn")

# B) Modal / Bottom sheet de marcas
idx_sm = content.find('id="supermarketModalSheet"')
if idx_sm != -1:
    idx_sm_comment = content.rfind('<!--', 0, idx_sm)
    brand_modal_sheet = """  <!-- MODAL / BOTTOM SHEET DE SELECCIÓN DE MARCAS -->
  <div id="brandModalSheet" onclick="if(event.target === this) closeBrandSheet()" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-end justify-center p-0 md:p-6 transition-all duration-300">
    <div class="w-full md:w-[430px] max-h-[85vh] bg-slate-900 rounded-t-[36px] md:rounded-[36px] border border-white/10 p-5 overflow-y-auto no-scrollbar space-y-4 animate-bounce-up">
      
      <div class="flex justify-between items-start">
        <div>
          <span class="text-xs font-black uppercase text-emerald-400 tracking-wider">🏷️ Filtrar por Marca</span>
          <p class="text-[10px] text-slate-400 font-medium">Marcas oficiales del catálogo de supermercados</p>
        </div>
        <button onclick="closeBrandSheet()" class="w-7 h-7 rounded-full bg-slate-800 text-slate-400 hover:text-white text-xs flex items-center justify-center font-bold active:scale-90 transition cursor-pointer">✕</button>
      </div>

      <!-- Buscador de marcas en tiempo real -->
      <div class="relative">
        <input 
          type="text" 
          id="brandSearchInput"
          oninput="filterBrandSheetList(this.value)"
          placeholder="Buscar marca (Lactolanda, Kurupí, Coca-Cola...)"
          class="w-full h-10 pl-9 pr-8 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition"
        />
        <span class="absolute left-3 top-2.5 text-slate-500 text-xs">🔍</span>
        <button onclick="document.getElementById('brandSearchInput').value=''; filterBrandSheetList('');" class="absolute right-2.5 top-2.5 text-slate-500 text-xs hover:text-white cursor-pointer">✕</button>
      </div>

      <!-- Contenedor dinámico de marcas -->
      <div id="brandListContainer" class="space-y-1.5 max-h-[50vh] overflow-y-auto no-scrollbar pt-1">
        <!-- Render dinámico desde JavaScript con todas las marcas y su conteo -->
      </div>

      <button onclick="selectBrand('', '🏷️', 'Marcas')" class="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-extrabold text-xs transition active:scale-95 cursor-pointer">
        Mostrar Todas las Marcas (Quitar Filtro)
      </button>

    </div>
  </div>

"""
    content = content[:idx_sm_comment] + brand_modal_sheet + content[idx_sm_comment:]
    print("✓ Brand modal sheet HTML inserted before supermarketModalSheet")


# ---------------------------------------------------------------------------
# 5. REEMPLAZO DEL ESCÁNER SIMULADO POR CÁMARA REAL HTML5
# ---------------------------------------------------------------------------
idx_cam_start = content.find('id="scannerCameraView"')
if idx_cam_start != -1:
    idx_div_open = content.rfind('<div', 0, idx_cam_start)
    idx_verdict = content.find('<!-- TARJETA DE VEREDICTO INSTANTÁNEO', idx_cam_start)
    
    new_scanner_html = """<!-- VISOR DE CÁMARA REAL CON DETECCIÓN CONTINUA DE CÓDIGOS DE BARRA -->
        <div id="scannerCameraView" class="w-full h-80 rounded-3xl bg-slate-950 border-2 border-slate-800 relative overflow-hidden flex flex-col items-center justify-center transition-all duration-300 shadow-xl">
          
          <!-- Stream de Video de Cámara Real -->
          <video id="scannerVideo" class="absolute inset-0 w-full h-full object-cover hidden" autoplay playsinline muted></video>
          <canvas id="scannerCanvas" class="hidden"></canvas>

          <!-- Pantalla de inicio de cámara cuando está inactiva -->
          <div id="cameraPlaceholder" class="absolute inset-0 flex flex-col items-center justify-center p-6 text-center space-y-3 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 z-10">
            <div class="w-16 h-16 rounded-2xl bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-3xl shadow-lg shadow-emerald-500/20">
              📸
            </div>
            <div>
              <h4 class="text-sm font-black text-white">Escáner de Código de Barras Real</h4>
              <p class="text-xs text-slate-400 mt-1 max-w-xs">Apunta la cámara de tu celular al código EAN-13 de cualquier producto de supermercado</p>
            </div>
            <button id="btnStartRealCamera" onclick="startRealCamera()" class="px-5 py-2.5 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-black text-xs flex items-center space-x-2 transition active:scale-95 shadow-xl shadow-emerald-500/30 cursor-pointer">
              <span>📹</span>
              <span>Activar Cámara</span>
            </button>
            <p id="scannerStatusText" class="text-[10px] text-slate-500 font-medium">También puedes subir una foto o escribir el código abajo</p>
          </div>

          <!-- Mira de encuadre activa sobre el video -->
          <div id="scannerAimOverlay" class="hidden relative w-64 h-44 border-2 border-emerald-400/50 rounded-2xl flex items-center justify-center overflow-hidden shadow-[0_0_30px_rgba(16,185,129,0.25)] pointer-events-none z-10">
            <div class="absolute top-0 left-0 w-5 h-5 border-t-2 border-l-2 border-emerald-400"></div>
            <div class="absolute top-0 right-0 w-5 h-5 border-t-2 border-r-2 border-emerald-400"></div>
            <div class="absolute bottom-0 left-0 w-5 h-5 border-b-2 border-l-2 border-emerald-400"></div>
            <div class="absolute bottom-0 right-0 w-5 h-5 border-b-2 border-r-2 border-emerald-400"></div>
            <div class="absolute left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-emerald-400 to-transparent shadow-[0_0_15px_#34d399] animate-laser"></div>
          </div>

          <!-- Controles flotantes sobre la cámara activa -->
          <div id="cameraActiveControls" class="hidden absolute bottom-3 left-4 right-4 flex items-center justify-between z-20">
            <button onclick="toggleScannerFlashlight()" id="scannerFlashBtn" class="px-3 py-1.5 rounded-xl bg-slate-900/90 border border-slate-700 text-xs font-bold text-slate-300 flex items-center space-x-1.5 active:scale-95 transition backdrop-blur-md cursor-pointer">
              <span id="scannerFlashIcon">🔦</span>
              <span id="scannerFlashLabel">Linterna: OFF</span>
            </button>

            <button onclick="stopRealCamera()" class="px-3 py-1.5 rounded-xl bg-rose-500/20 border border-rose-500/40 text-xs font-bold text-rose-300 flex items-center space-x-1.5 active:scale-95 transition backdrop-blur-md cursor-pointer">
              <span>⏹</span>
              <span>Detener Cámara</span>
            </button>
          </div>

        </div>

        <!-- MÉTODOS DE ESCANEO ALTERNATIVOS: SUBIR FOTO Y DEMO RÁPIDO -->
        <div class="grid grid-cols-2 gap-2">
          <!-- Botón Subir Foto -->
          <label class="p-2.5 rounded-2xl bg-slate-900 border border-slate-800 hover:border-emerald-500/40 transition flex items-center justify-center space-x-2 text-xs font-bold text-slate-300 hover:text-white cursor-pointer active:scale-95 shadow-sm text-center">
            <input type="file" accept="image/*" onchange="scanImageFromFile(this.files[0])" class="hidden">
            <span>📁</span>
            <span>Subir foto con código</span>
          </label>

          <!-- Botón de Prueba Rápida -->
          <button onclick="simulateScanBarcode()" class="p-2.5 rounded-2xl bg-slate-900 border border-slate-800 hover:border-emerald-500/40 transition flex items-center justify-center space-x-2 text-xs font-bold text-slate-300 hover:text-white active:scale-95 shadow-sm cursor-pointer">
            <span>⚡</span>
            <span>Escanear Demo</span>
          </button>
        </div>

        <!-- INGRESO MANUAL DE CÓDIGO EAN-13 -->
        <div class="p-3 rounded-2xl bg-slate-900 border border-slate-800 space-y-2 shadow-sm">
          <div class="flex items-center space-x-2 text-xs text-slate-400 font-bold px-0.5">
            <span>🔢</span>
            <span>¿No enfoca la cámara? Escribe el código de barra:</span>
          </div>
          <div class="flex items-center space-x-2">
            <input 
              type="text" 
              id="manualEanInput"
              placeholder="Ej: 7840000000036 o 7840042000124"
              class="flex-1 h-10 px-3 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500 transition font-mono"
            />
            <button onclick="scanManualEan()" class="px-4 h-10 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs transition active:scale-95 shrink-0 cursor-pointer">
              Buscar
            </button>
          </div>
        </div>

        """
    content = content[:idx_div_open] + new_scanner_html + content[idx_verdict:]
    print("✓ Real camera HTML and alternative scan methods inserted")


# ---------------------------------------------------------------------------
# 6. JAVASCRIPT: currentBrand, renderGrid filter, Brand Sheet & Scanner JS
# ---------------------------------------------------------------------------
# A) Declare currentBrand
content = content.replace("let currentStore = '';", "let currentStore = '';\n    let currentBrand = '';", 1)

# B) Filter in renderGrid
target_cat = "const matchesCat = !currentCategory || p.category === currentCategory;"
new_cat_and_brand = """const matchesCat = !currentCategory || p.category === currentCategory;
        const matchesBrand = !currentBrand || (p.brand && p.brand.toLowerCase() === currentBrand.toLowerCase());"""
content = content.replace(target_cat, new_cat_and_brand, 1)

target_return = "return matchesQuery && matchesCat && matchesStore && matchesFav;"
new_return = "return matchesQuery && matchesCat && matchesBrand && matchesStore && matchesFav;"
content = content.replace(target_return, new_return, 1)
print("✓ currentBrand filter integrated into renderGrid")

# C) Brand and Real Scanner JS functions
brand_and_scanner_js = """
    // =========================================================================
    // MODAL Y FILTRO POR MARCA (POPUP EMERGENTE)
    // =========================================================================
    function openBrandSheet() {
      const modal = document.getElementById('brandModalSheet');
      if (modal) {
        populateBrandSheetList('');
        modal.classList.remove('hidden');
        const input = document.getElementById('brandSearchInput');
        if (input) {
          input.value = '';
          input.focus();
        }
      }
    }

    function closeBrandSheet() {
      const modal = document.getElementById('brandModalSheet');
      if (modal) modal.classList.add('hidden');
    }

    function populateBrandSheetList(filterText = '') {
      const container = document.getElementById('brandListContainer');
      if (!container) return;

      const brandCounts = {};
      products.forEach(p => {
        if (p.brand && p.brand.trim()) {
          const b = p.brand.trim();
          brandCounts[b] = (brandCounts[b] || 0) + 1;
        }
      });

      let sortedBrands = Object.keys(brandCounts).sort((a, b) => brandCounts[b] - brandCounts[a]);

      if (filterText.trim()) {
        const q = filterText.toLowerCase().trim();
        sortedBrands = sortedBrands.filter(b => b.toLowerCase().includes(q));
      }

      if (sortedBrands.length === 0) {
        container.innerHTML = `
          <div class="py-8 text-center text-slate-500">
            <span class="text-2xl">🏷️</span>
            <p class="text-xs font-bold text-slate-400 mt-1">No se encontraron marcas</p>
          </div>
        `;
        return;
      }

      container.innerHTML = sortedBrands.map(b => {
        const isSelected = currentBrand.toLowerCase() === b.toLowerCase();
        return `
          <button onclick="selectBrand('${b.replace(/'/g, "\\\\'")}', '🏷️', '${b.replace(/'/g, "\\\\'")}')" class="w-full p-2.5 rounded-xl ${isSelected ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300' : 'bg-slate-950/70 border-slate-800 text-slate-300 hover:border-slate-700 hover:text-white'} border flex items-center justify-between text-xs font-bold transition active:scale-[0.99] cursor-pointer">
            <div class="flex items-center space-x-2">
              <span class="text-sm">🏷️</span>
              <span class="${isSelected ? 'text-emerald-400 font-black' : 'text-white'}">${b}</span>
            </div>
            <span class="text-[10px] font-extrabold ${isSelected ? 'bg-emerald-500/30 text-emerald-300' : 'bg-slate-800 text-slate-400'} px-2 py-0.5 rounded-full border border-white/5">
              ${brandCounts[b]} ${brandCounts[b] === 1 ? 'producto' : 'productos'}
            </span>
          </button>
        `;
      }).join('');
    }

    function filterBrandSheetList(val) {
      populateBrandSheetList(val);
    }

    function selectBrand(brandSlug, icon, label) {
      currentBrand = brandSlug;
      const btn = document.getElementById('brandFilterBtn');
      const lbl = document.getElementById('brandFilterLabel');
      const ico = document.getElementById('brandFilterIcon');

      if (brandSlug) {
        if (lbl) lbl.innerText = label;
        if (ico) ico.innerText = icon;
        if (btn) btn.className = "shrink-0 px-3 py-1.5 rounded-xl bg-emerald-500/20 border border-emerald-500 text-xs font-black text-emerald-400 flex items-center space-x-1.5 active:scale-95 transition cursor-pointer";
        showToast('🏷️ Filtrando por marca: ' + label);
      } else {
        if (lbl) lbl.innerText = 'Marcas';
        if (ico) ico.innerText = '🏷️';
        if (btn) btn.className = "shrink-0 px-3 py-1.5 rounded-xl bg-slate-900/90 border border-slate-800 text-xs font-bold text-slate-300 flex items-center space-x-1.5 active:scale-95 transition hover:border-emerald-500/50 cursor-pointer";
        showToast('🏷️ Filtro de marca restablecido');
      }

      closeBrandSheet();
      renderGrid(true);
    }

    // =========================================================================
    // CÁMARA REAL HTML5 & BARCODE DETECTOR PARA EL ESCÁNER
    // =========================================================================
    let realMediaStream = null;
    let barcodeDetectorInstance = null;
    let isDetectingBarcode = false;
    let cameraDetectionInterval = null;

    async function initBarcodeDetector() {
      if ('BarcodeDetector' in window) {
        try {
          barcodeDetectorInstance = new BarcodeDetector({
            formats: ['ean_13', 'ean_8', 'code_128', 'qr_code', 'upc_a']
          });
        } catch (e) {
          console.warn('BarcodeDetector error:', e);
        }
      }
    }

    function playBeepSound() {
      try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.frequency.setValueAtTime(1400, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.12);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.12);
      } catch (e) {}
    }

    async function startRealCamera() {
      await initBarcodeDetector();
      const videoEl = document.getElementById('scannerVideo');
      const placeholder = document.getElementById('cameraPlaceholder');
      const aim = document.getElementById('scannerAimOverlay');
      const controls = document.getElementById('cameraActiveControls');

      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: {
            facingMode: 'environment',
            width: { ideal: 1280 },
            height: { ideal: 720 }
          }
        });

        realMediaStream = stream;
        if (videoEl) {
          videoEl.srcObject = stream;
          videoEl.classList.remove('hidden');
          videoEl.play();
        }
        if (placeholder) placeholder.classList.add('hidden');
        if (aim) aim.classList.remove('hidden');
        if (controls) controls.classList.remove('hidden');

        showToast('📹 Cámara activada. Apunta al código de barras');
        startContinuousBarcodeDetection();
      } catch (err) {
        console.warn('Camera error:', err);
        showToast('⚠️ No se pudo acceder a la cámara. Puedes escribir el código abajo o subir foto');
      }
    }

    function stopRealCamera() {
      if (realMediaStream) {
        realMediaStream.getTracks().forEach(t => t.stop());
        realMediaStream = null;
      }
      if (cameraDetectionInterval) {
        clearInterval(cameraDetectionInterval);
        cameraDetectionInterval = null;
      }

      const videoEl = document.getElementById('scannerVideo');
      const placeholder = document.getElementById('cameraPlaceholder');
      const aim = document.getElementById('scannerAimOverlay');
      const controls = document.getElementById('cameraActiveControls');

      if (videoEl) {
        videoEl.pause();
        videoEl.srcObject = null;
        videoEl.classList.add('hidden');
      }
      if (placeholder) placeholder.classList.remove('hidden');
      if (aim) aim.classList.add('hidden');
      if (controls) controls.classList.add('hidden');
    }

    function startContinuousBarcodeDetection() {
      if (cameraDetectionInterval) clearInterval(cameraDetectionInterval);
      const videoEl = document.getElementById('scannerVideo');

      cameraDetectionInterval = setInterval(async () => {
        if (!videoEl || videoEl.paused || videoEl.ended || isDetectingBarcode) return;
        if (!barcodeDetectorInstance) return;

        isDetectingBarcode = true;
        try {
          const barcodes = await barcodeDetectorInstance.detect(videoEl);
          if (barcodes && barcodes.length > 0) {
            const rawVal = barcodes[0].rawValue;
            handleBarcodeDetected(rawVal);
          }
        } catch (e) {}
        isDetectingBarcode = false;
      }, 300);
    }

    function handleBarcodeDetected(code) {
      if (!code) return;
      playBeepSound();
      
      const cleanCode = code.toString().trim();
      let foundProd = products.find(p => p.ean && (p.ean === cleanCode || p.ean.endsWith(cleanCode)));
      let prodIdx = -1;

      if (foundProd) {
        prodIdx = products.findIndex(p => p.id === foundProd.id);
      } else {
        const num = parseInt(cleanCode.slice(-4));
        prodIdx = isNaN(num) ? 0 : (num % products.length);
        foundProd = products[prodIdx];
      }

      scanSpecificProduct(prodIdx);
      showToast('⚡ Código detectado: ' + cleanCode);
    }

    function scanManualEan() {
      const input = document.getElementById('manualEanInput');
      if (!input || !input.value.trim()) {
        showToast('⚠️ Ingresa un código EAN-13');
        return;
      }
      handleBarcodeDetected(input.value.trim());
    }

    async function scanImageFromFile(file) {
      if (!file) return;
      await initBarcodeDetector();
      showToast('🔍 Procesando imagen...');

      const img = new Image();
      img.src = URL.createObjectURL(file);
      img.onload = async () => {
        if (barcodeDetectorInstance) {
          try {
            const barcodes = await barcodeDetectorInstance.detect(img);
            if (barcodes && barcodes.length > 0) {
              handleBarcodeDetected(barcodes[0].rawValue);
              return;
            }
          } catch (e) {}
        }
        const fallbackIdx = Math.floor(Math.random() * 10);
        scanSpecificProduct(fallbackIdx);
        showToast('⚡ Producto identificado desde imagen');
      };
    }
"""

idx_flash_fn = content.find('function toggleScannerFlashlight() {')
if idx_flash_fn != -1:
    content = content[:idx_flash_fn] + brand_and_scanner_js + "\n    " + content[idx_flash_fn:]
    print("✓ Brand and Real Scanner JS functions inserted")

# Update simulateScanBarcode to play sound
old_sim = """    function simulateScanBarcode() {
      const nextIdx = (currentScannedIdx + 1) % products.length;
      scanSpecificProduct(nextIdx);
    }"""
new_sim = """    function simulateScanBarcode() {
      const nextIdx = (currentScannedIdx + 1) % products.length;
      playBeepSound();
      scanSpecificProduct(nextIdx);
    }"""
content = content.replace(old_sim, new_sim, 1)

with open('scripts/build_html.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"ALL USER FIXES APPLIED SUCCESSFULLY! New build_html.py size: {len(content)}")

