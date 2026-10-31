# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Definición del Directorio Maestro de Cobertura de Supermercados por Ciudad
city_map_definition = """    // DIRECTORIO MAESTRO DE COBERTURA DE SUPERMERCADOS POR CIUDAD EN PARAGUAY
    const CITY_SUPERMARKETS_MAP = {
      'Caacupé': [
        { name: 'Supermercados Stock', icon: '🏬', desc: 'Sucursal Km 54 • Caacupé', isLocal: false },
        { name: 'Superseis', icon: '🏪', desc: 'Sucursal Caacupé Centro', isLocal: false },
        { name: 'Biggie Express', icon: '⚡', desc: 'Abierto 24 Horas Caacupé', isLocal: false },
        { name: 'Supermercado San Vicente', icon: '🏷️', desc: 'Local Caacupé • Verificado en Tienda', isLocal: true, verifiedBadge: 'Local Caacupé' },
        { name: 'Tiendas Tuti', icon: '🏪', desc: 'Tienda de Conveniencia Caacupé', isLocal: false }
      ],
      'Asunción': [
        { name: 'Biggie Express', icon: '⚡', desc: '200+ sucursales 24hs Capital', isLocal: false },
        { name: 'Superseis', icon: '🏪', desc: 'Cadena líder nacional • Itaú y ueno', isLocal: false },
        { name: 'Supermercados Stock', icon: '🏬', desc: 'Gran cobertura barrial Asunción', isLocal: false },
        { name: 'Casa Rica', icon: '👑', desc: 'Gourmet Molas López & España', isLocal: false },
        { name: 'Supermercados Areté', icon: '🛒', desc: 'Primer Presidente & Denis Roa', isLocal: false },
        { name: 'Cadena Real', icon: '🏬', desc: 'Real Villa Morra & Acceso Sur', isLocal: false },
        { name: 'Delimarket', icon: '✨', desc: 'Delimarket Shopping del Sol', isLocal: false }
      ],
      'San Lorenzo': [
        { name: 'Supermercados Stock', icon: '🏬', desc: 'Stock San Lorenzo & Ruta 2', isLocal: false },
        { name: 'Superseis', icon: '🏪', desc: 'Superseis San Lorenzo', isLocal: false },
        { name: 'Biggie Express', icon: '⚡', desc: 'Sucursales San Lorenzo', isLocal: false },
        { name: 'Supermercados Salemma', icon: '🏬', desc: 'Salemma Super Center Km 9.5', isLocal: false },
        { name: 'Fortis Mayorista', icon: '📦', desc: 'Fortis San Lorenzo', isLocal: false },
        { name: 'Cadena Real', icon: '🏬', desc: 'Real San Lorenzo', isLocal: false }
      ],
      'Luque': [
        { name: 'Supermercados Stock', icon: '🏬', desc: 'Stock Luque Centro', isLocal: false },
        { name: 'Superseis', icon: '🏪', desc: 'Superseis Luque', isLocal: false },
        { name: 'Biggie Express', icon: '⚡', desc: 'Biggie Luque', isLocal: false },
        { name: 'Los Jardines (Luque)', icon: '🌺', desc: 'Supermercado tradicional de Luque', isLocal: true, verifiedBadge: 'Local Luque' },
        { name: 'Supermercados Areté', icon: '🛒', desc: 'Areté Luque', isLocal: false }
      ],
      'Ciudad del Este': [
        { name: 'Fortis Mayorista', icon: '📦', desc: 'Fortis CDE Km 4', isLocal: false },
        { name: 'Box Mayorista', icon: '📦', desc: 'Box Mayorista CDE', isLocal: false },
        { name: 'Cadena Gran Vía', icon: '🛒', desc: 'Gran Vía Km 4 & Hernandarias', isLocal: false },
        { name: 'Supermercados Stock', icon: '🏬', desc: 'Stock CDE', isLocal: false },
        { name: 'Superseis', icon: '🏪', desc: 'Superseis Plaza Jesuítica', isLocal: false }
      ],
      'Encarnación': [
        { name: 'Supermercados Stock', icon: '🏬', desc: 'Stock Encarnación Costanera', isLocal: false },
        { name: 'Superseis', icon: '🏪', desc: 'Superseis Encarnación', isLocal: false },
        { name: 'Biggie Express', icon: '⚡', desc: 'Biggie Costanera', isLocal: false },
        { name: 'Supermercados La Bomba', icon: '💣', desc: 'La Bomba Circuito Comercial', isLocal: false }
      ],
      'Todo Paraguay': [
        { name: 'Biggie Express', icon: '⚡', desc: '200+ sucursales 24hs', isLocal: false },
        { name: 'Superseis', icon: '🏪', desc: 'Cadena líder nacional', isLocal: false },
        { name: 'Supermercados Stock', icon: '🏬', desc: 'Gran cobertura nacional', isLocal: false },
        { name: 'Casa Rica', icon: '👑', desc: 'Gourmet & Delicatessen', isLocal: false },
        { name: 'Fortis Mayorista', icon: '📦', desc: 'Precios mayoristas y minoristas', isLocal: false },
        { name: 'Supermercado San Vicente', icon: '🏷️', desc: 'Local Caacupé • Verificado en Tienda', isLocal: true, verifiedBadge: 'Local Caacupé' },
        { name: 'Supermercados Salemma', icon: '🏬', desc: 'Salemma Super Center', isLocal: false },
        { name: 'Supermercados Areté', icon: '🛒', desc: 'Supermercados Areté', isLocal: false },
        { name: 'Los Jardines (Luque)', icon: '🌺', desc: 'Supermercado Los Jardines', isLocal: true },
        { name: 'Box Mayorista', icon: '📦', desc: 'Box Mayorista CDE & San Lorenzo', isLocal: false },
        { name: 'Cadena Real', icon: '🏬', desc: 'Cadena Real', isLocal: false },
        { name: 'Cadena Gran Vía', icon: '🛒', desc: 'Gran Vía CDE', isLocal: false },
        { name: 'Supermercados La Bomba', icon: '💣', desc: 'La Bomba Encarnación', isLocal: false },
        { name: 'Delimarket', icon: '✨', desc: 'Delimarket Shopping del Sol', isLocal: false },
        { name: 'Tiendas Tuti', icon: '🏪', desc: 'Tiendas Tuti', isLocal: false }
      ]
    };

    function getStoresForCurrentCity() {
      return CITY_SUPERMARKETS_MAP[selectedCity] || CITY_SUPERMARKETS_MAP['Caacupé'];
    }"""

old_target_vars = """    let selectedCity = 'Caacupé';"""
new_target_vars = """    let selectedCity = 'Caacupé';\n\n""" + city_map_definition

# 2. Reemplazar el contenedor estático de supermercados en el HTML por un contenedor dinámico
old_sheet_html = """  <!-- MODAL SHEET: FILTRAR POR SUPERMERCADO -->
  <div id="supermarketModalSheet" onclick="if(event.target === this) closeSupermarketSheet()" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-end justify-center p-0 md:p-6 transition-all">
    <div class="w-full md:w-[430px] max-h-[75vh] bg-slate-900 rounded-t-[36px] md:rounded-[36px] border border-white/10 p-5 overflow-y-auto no-scrollbar space-y-3 animate-bounce-up">
      <div class="flex justify-between items-center pb-2 border-b border-slate-800">
        <span class="text-xs font-black text-white uppercase tracking-wider">Filtrar por Supermercado</span>
        <button onclick="closeSupermarketSheet()" class="w-7 h-7 rounded-full bg-slate-800 text-slate-400 hover:text-white text-xs flex items-center justify-center font-bold">✕</button>
      </div>
      <div class="space-y-2 pt-1">
        <button onclick="selectStore('', '🏬', 'Supermercados')" class="w-full p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center justify-between text-left transition">
          <div>
            <p class="text-xs font-extrabold text-white">Todos los Supermercados</p>
            <p class="text-[10px] text-slate-400">Ver góndola combinada de todas las cadenas</p>
          </div>
          <span class="text-xs">🌐</span>
        </button>
        <button onclick="selectStore('Biggie Express', '🏪', 'Biggie Express')" class="w-full p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center justify-between text-left transition">
          <div>
            <p class="text-xs font-extrabold text-white">Biggie Express</p>
            <p class="text-[10px] text-slate-400">200+ sucursales abiertas las 24 horas</p>
          </div>
          <span class="text-xs">⚡</span>
        </button>
        <button onclick="selectStore('Superseis', '🏪', 'Superseis')" class="w-full p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center justify-between text-left transition">
          <div>
            <p class="text-xs font-extrabold text-white">Superseis</p>
            <p class="text-[10px] text-slate-400">Cadena líder nacional • Itaú y ueno</p>
          </div>
          <span class="text-xs">🏬</span>
        </button>
        <button onclick="selectStore('Stock', '🏪', 'Stock')" class="w-full p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center justify-between text-left transition">
          <div>
            <p class="text-xs font-extrabold text-white">Supermercados Stock</p>
            <p class="text-[10px] text-slate-400">Gran cobertura nacional • Atlas y Familiar</p>
          </div>
          <span class="text-xs">🏬</span>
        </button>
        <button onclick="selectStore('Casa Rica', '👑', 'Casa Rica')" class="w-full p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center justify-between text-left transition">
          <div>
            <p class="text-xs font-extrabold text-white">Casa Rica</p>
            <p class="text-[10px] text-slate-400">Gourmet & Delicatessen • Sudameris</p>
          </div>
          <span class="text-xs">👑</span>
        </button>
        <button onclick="selectStore('Fortis', '📦', 'Fortis Mayorista')" class="w-full p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center justify-between text-left transition">
          <div>
            <p class="text-xs font-extrabold text-white">Fortis Mayorista</p>
            <p class="text-[10px] text-slate-400">Precios por mayor y menor en todo el país</p>
          </div>
          <span class="text-xs">📦</span>
        </button>
      </div>
    </div>
  </div>"""

new_sheet_html = """  <!-- MODAL SHEET: FILTRAR POR SUPERMERCADO (DINÁMICO SEGÚN LA CIUDAD ACTIVA) -->
  <div id="supermarketModalSheet" onclick="if(event.target === this) closeSupermarketSheet()" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-end justify-center p-0 md:p-6 transition-all">
    <div class="w-full md:w-[430px] max-h-[75vh] bg-slate-900 rounded-t-[36px] md:rounded-[36px] border border-white/10 p-5 overflow-y-auto no-scrollbar space-y-3 animate-bounce-up">
      <div class="flex justify-between items-center pb-2 border-b border-slate-800">
        <div>
          <span class="text-xs font-black text-white uppercase tracking-wider">Supermercados en tu Ciudad</span>
          <p id="supermarketCitySubtitle" class="text-[10px] text-emerald-400 font-bold mt-0.5">Mostrando solo comercios de Caacupé</p>
        </div>
        <button onclick="closeSupermarketSheet()" class="w-7 h-7 rounded-full bg-slate-800 text-slate-400 hover:text-white text-xs flex items-center justify-center font-bold">✕</button>
      </div>
      <div id="supermarketListContainer" class="space-y-2 pt-1">
        <!-- Generado dinámicamente según la ciudad activa por renderSupermarketSheet() -->
      </div>
    </div>
  </div>"""

# 3. Funciones renderSupermarketSheet y selectCity
old_city_funcs = """    function selectCity(cityName) {
      selectedCity = cityName;
      document.getElementById('currentCityLabel').innerText = cityName;
      closeCitySheet();
      saveLocalData();
      showToast('📍 Ciudad cambiada a: ' + cityName);
    }"""

new_city_funcs = """    function renderSupermarketSheet() {
      const container = document.getElementById('supermarketListContainer');
      const subtitle = document.getElementById('supermarketCitySubtitle');
      if (subtitle) subtitle.innerText = 'Mostrando solo comercios disponibles en ' + selectedCity;
      if (!container) return;

      const stores = getStoresForCurrentCity();
      let html = `
        <button onclick="selectStore('', '🏬', 'Supermercados')" class="w-full p-3 rounded-2xl ${!currentStore ? 'bg-emerald-500/20 border-emerald-500/50' : 'bg-slate-800/80'} hover:bg-emerald-500/20 border border-slate-700 flex items-center justify-between text-left transition">
          <div>
            <p class="text-xs font-extrabold text-white">Todos los de ${selectedCity}</p>
            <p class="text-[10px] text-slate-400">Ver góndola de los ${stores.length} comercios locales</p>
          </div>
          <span class="text-xs">📍</span>
        </button>
      `;

      stores.forEach(st => {
        const isSelected = (currentStore === st.name || (currentStore === 'Stock' && st.name === 'Supermercados Stock'));
        const localTag = st.isLocal 
          ? '<span class="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Local • En Tienda</span>'
          : '';

        html += `
          <button onclick="selectStore('${st.name}', '${st.icon}', '${st.name}')" class="w-full p-3 rounded-2xl ${isSelected ? 'bg-emerald-500/20 border-emerald-500/50' : 'bg-slate-800/80'} hover:bg-emerald-500/20 border border-slate-700 flex items-center justify-between text-left transition">
            <div class="min-w-0 pr-2">
              <div class="flex items-center space-x-1.5">
                <p class="text-xs font-extrabold text-white truncate">${st.name}</p>
                ${localTag}
              </div>
              <p class="text-[10px] text-slate-400 truncate mt-0.5">${st.desc}</p>
            </div>
            <span class="text-base shrink-0">${st.icon}</span>
          </button>
        `;
      });

      container.innerHTML = html;
    }

    function selectCity(cityName) {
      selectedCity = cityName;
      document.getElementById('currentCityLabel').innerText = cityName;
      closeCitySheet();
      saveLocalData();

      // Si el súper seleccionado no existe en la nueva ciudad, reiniciar a "Todos"
      const availableStores = getStoresForCurrentCity().map(s => s.name);
      if (currentStore && !availableStores.includes(currentStore) && !(currentStore === 'Stock' && availableStores.includes('Supermercados Stock'))) {
        currentStore = '';
        const iconEl = document.getElementById('superFilterIcon');
        const labelEl = document.getElementById('superFilterLabel');
        if (iconEl) iconEl.innerText = '🏬';
        if (labelEl) labelEl.innerText = 'Supermercados';
      }

      renderSupermarketSheet();
      renderGrid();
      renderCart();
      showToast('📍 Ciudad: ' + cityName + ' (' + availableStores.length + ' supermercados disponibles)');
    }"""

# 4. Actualizar openProductDetail para que en la comparativa Knasta solo salgan supermercados de la ciudad activa
old_detail_stores = """      // Catálogo de cadenas con sus precios específicos
      const storesCatalog = [
        { name: 'Biggie Express', icon: '⚡', desc: 'Abierto 24 Horas' },
        { name: 'Superseis', icon: '🏪', desc: 'Cadena Líder Nacional' },
        { name: 'Supermercados Stock', icon: '🏬', desc: 'Precios Bajos Siempre' },
        { name: 'Casa Rica', icon: '👑', desc: 'Gourmet & Delicatessen' },
        { name: 'Fortis Mayorista', icon: '📦', desc: 'Venta Mayorista y Minorista' }
      ];

      const comparisons = storesCatalog.map(st => {"""

new_detail_stores = """      // Supermercados presentes estrictamente en la ciudad activa (${selectedCity})
      const localCatalog = getStoresForCurrentCity();
      const comparisons = localCatalog.map(st => {"""

# 5. Agregar badge 'Local / Verificado en Tienda' en la comparativa Knasta
old_detail_card = """                        <div class="flex items-center space-x-1.5">
                          <p class="text-xs font-black text-white truncate">${st.name}</p>
                          ${winnerBadge}
                        </div>"""

new_detail_card = """                        <div class="flex items-center space-x-1.5">
                          <p class="text-xs font-black text-white truncate">${st.name}</p>
                          ${st.isLocal ? '<span class="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Local • En Tienda</span>' : ''}
                          ${winnerBadge}
                        </div>"""

# 6. Actualizar el header de "5 cadenas" a dinámico "${comparisons.length} comercios en ${selectedCity}"
old_detail_header = """<span class="text-[10px] text-emerald-400 font-extrabold bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">5 cadenas</span>"""
new_detail_header = """<span class="text-[10px] text-emerald-400 font-extrabold bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">${comparisons.length} comercios en ${selectedCity}</span>"""

# 7. Ejecutar renderSupermarketSheet() en init()
old_init = """    // INICIALIZACIÓN
    window.addEventListener('DOMContentLoaded', () => {
      loadSavedData();
      updateStatusBarClock();
      setInterval(updateStatusBarClock, 30000);
      renderGrid();
      renderCart();
      renderDayChips();
      updateProfileButtons();
      renderPromos();"""

new_init = """    // INICIALIZACIÓN
    window.addEventListener('DOMContentLoaded', () => {
      loadSavedData();
      updateStatusBarClock();
      setInterval(updateStatusBarClock, 30000);
      renderSupermarketSheet();
      renderGrid();
      renderCart();
      renderDayChips();
      updateProfileButtons();
      renderPromos();"""

code_norm = code.replace('\r\n', '\n')
err = False

for name, old_b, new_b in [
    ("CITY_SUPERMARKETS_MAP vars", old_target_vars, new_target_vars),
    ("supermarketModalSheet HTML", old_sheet_html, new_sheet_html),
    ("city functions", old_city_funcs, new_city_funcs),
    ("openProductDetail stores", old_detail_stores, new_detail_stores),
    ("openProductDetail card badge", old_detail_card, new_detail_card),
    ("openProductDetail header count", old_detail_header, new_detail_header),
    ("init call", old_init, new_init)
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
    print("SUCCESS: scripts/build_html.py updated with location-based supermarket filtering and Supermercado San Vicente!")
else:
    print("FAILED TO APPLY PATCH")
