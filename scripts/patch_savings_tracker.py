import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Insert Home Savings Banner in viewSearch right after search input div
target_home_search = """        <!-- FILTROS RÁPIDOS INTERACTIVOS (CHIPS HORIZONTALES) -->"""
assert target_home_search in content, "target_home_search not found"

home_savings_banner = """        <!-- BANNER DE IMPACTO DE AHORRO REAL PRECIOSPY (SEMANA, MES, TOTAL) -->
        <div onclick="openSavingsModal()" class="p-3 rounded-2xl bg-gradient-to-r from-emerald-950/70 via-slate-900 to-teal-950/70 border border-emerald-500/30 flex items-center justify-between cursor-pointer hover:border-emerald-400 transition-all shadow-md group active:scale-[0.99]">
          <div class="flex items-center space-x-2.5">
            <div class="w-9 h-9 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-lg group-hover:scale-110 transition-transform shadow-sm shadow-emerald-500/20">
              💰
            </div>
            <div>
              <div class="flex items-center space-x-1.5">
                <span class="text-[9px] font-black uppercase text-emerald-400 tracking-wider">Tu Ahorro Real</span>
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              </div>
              <p class="text-xs font-black text-white">Gs. <span id="homeSavingsDisplay">542.000</span> <span class="text-[10px] font-medium text-slate-400">ahorrados este mes</span></p>
            </div>
          </div>
          <div class="flex items-center space-x-1 bg-emerald-500/15 group-hover:bg-emerald-500 text-emerald-300 group-hover:text-white px-2.5 py-1 rounded-xl text-[10px] font-black border border-emerald-500/30 transition-all">
            <span>Semana / Mes / Total</span>
            <span class="text-xs">➔</span>
          </div>
        </div>

"""

content = content.replace(target_home_search, home_savings_banner + target_home_search, 1)

# 2. Insert Profile Savings Card in viewProfile right after first title card
target_profile = """        <div class="space-y-3">
          <span class="text-xs font-black uppercase text-slate-400 tracking-wider px-1">Tarjetas y Niveles Configurados:</span>"""
assert target_profile in content, "target_profile not found"

profile_savings_card = """        <!-- DASHBOARD DE AHORRO EN PERFIL (SEMANA, MES, TOTAL) -->
        <div onclick="openSavingsModal()" class="p-4 rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900 to-emerald-950/40 border border-emerald-500/30 space-y-3 cursor-pointer hover:border-emerald-400 transition group shadow-lg shadow-emerald-500/5">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2.5">
              <span class="text-xl group-hover:scale-110 transition-transform">💰</span>
              <div>
                <h3 class="text-xs font-black uppercase text-white tracking-wider">Mi Impacto de Ahorro PreciosPy</h3>
                <p class="text-[10px] text-slate-400">Prueba comprobada de tu dinero ahorrado</p>
              </div>
            </div>
            <span class="text-[10px] font-black text-emerald-400 bg-emerald-500/20 px-2.5 py-1 rounded-full border border-emerald-500/30 flex items-center space-x-1">
              <span>Ver impacto</span>
              <span>➔</span>
            </span>
          </div>

          <div class="grid grid-cols-3 gap-2 text-center pt-1">
            <div class="p-2.5 rounded-2xl bg-slate-950/70 border border-slate-800">
              <p class="text-[9px] font-extrabold text-slate-400 uppercase tracking-wider">Esta Semana</p>
              <p id="profileSavingsWeek" class="text-xs font-black text-emerald-400 mt-1">Gs. 128.500</p>
            </div>
            <div class="p-2.5 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 ring-1 ring-emerald-500/20">
              <p class="text-[9px] font-black text-emerald-300 uppercase tracking-wider">Este Mes</p>
              <p id="profileSavingsMonth" class="text-xs font-black text-white mt-1">Gs. 542.000</p>
            </div>
            <div class="p-2.5 rounded-2xl bg-slate-950/70 border border-slate-800">
              <p class="text-[9px] font-extrabold text-slate-400 uppercase tracking-wider">Total</p>
              <p id="profileSavingsTotal" class="text-xs font-black text-emerald-400 mt-1">Gs. 1.845.000</p>
            </div>
          </div>
        </div>

"""

content = content.replace(target_profile, profile_savings_card + target_profile, 1)

# 3. Insert "Registrar Compra" button in viewCart under TOTAL Y RESUMEN FINAL
target_cart_buttons = """          <div class="grid grid-cols-2 gap-2 pt-1">
            <button onclick="shareCartWhatsApp()" """
assert target_cart_buttons in content, "target_cart_buttons not found"

cart_register_btn = """          <button id="btnRegisterCartPurchase" onclick="registerCartPurchase()" class="w-full py-3 rounded-2xl bg-gradient-to-r from-emerald-500 via-teal-500 to-sky-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-black text-xs flex items-center justify-center space-x-2 transition active:scale-95 shadow-xl shadow-emerald-500/20 group cursor-pointer mb-2">
            <span class="text-base group-hover:scale-125 transition-transform">💰</span>
            <span>Registrar esta compra en Mi Ahorro Acumulado</span>
          </button>

"""

content = content.replace(target_cart_buttons, cart_register_btn + target_cart_buttons, 1)

# 4. Insert Modal HTML before productDetailModal
target_modal_pos = """  <div id="productDetailModal" """
assert target_modal_pos in content, "target_modal_pos not found"

savings_modal_html = """  <!-- MODAL DASHBOARD DE IMPACTO DE AHORRO REAL (SEMANA, MES, TOTAL) -->
  <div id="savingsModal" onclick="if(event.target === this) closeSavingsModal()" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-end justify-center p-0 md:p-6 transition-all duration-300">
    <div class="w-full md:w-[430px] max-h-[90vh] bg-slate-900 rounded-t-[36px] md:rounded-[36px] border border-white/10 p-5 overflow-y-auto no-scrollbar space-y-4 animate-bounce-up">
      
      <!-- Header del Modal -->
      <div class="flex justify-between items-start">
        <div class="flex items-center space-x-2.5">
          <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center text-xl shadow-lg shadow-emerald-500/20">
            💰
          </div>
          <div>
            <h2 class="text-sm font-black text-white">Mi Ahorro Real PreciosPy</h2>
            <p class="text-[10px] text-slate-400 font-medium">Prueba comprobada de cuánto dinero ahorras</p>
          </div>
        </div>
        <button onclick="closeSavingsModal()" class="w-7 h-7 rounded-full bg-slate-800 text-slate-400 hover:text-white text-xs flex items-center justify-center font-bold active:scale-90 transition">✕</button>
      </div>

      <!-- SELECTOR DE PERÍODO: SEMANA | MES | TOTAL -->
      <div class="grid grid-cols-3 gap-1.5 p-1 rounded-2xl bg-slate-950 border border-slate-800">
        <button id="btnPeriodWeek" onclick="setSavingsPeriod('week')" class="py-2 rounded-xl text-xs font-black transition-all text-slate-400 hover:text-white">
          📅 Semana
        </button>
        <button id="btnPeriodMonth" onclick="setSavingsPeriod('month')" class="py-2 rounded-xl text-xs font-black transition-all bg-emerald-500 text-white shadow-md">
          🗓️ Mes
        </button>
        <button id="btnPeriodTotal" onclick="setSavingsPeriod('total')" class="py-2 rounded-xl text-xs font-black transition-all text-slate-400 hover:text-white">
          🏆 Total
        </button>
      </div>

      <!-- TARJETA PRINCIPAL DE IMPACTO -->
      <div class="p-5 rounded-3xl bg-gradient-to-br from-emerald-950/80 via-slate-900 to-slate-900 border border-emerald-500/30 text-center space-y-2 relative overflow-hidden shadow-xl">
        <div class="absolute -right-6 -top-6 w-24 h-24 bg-emerald-500/10 rounded-full blur-xl pointer-events-none"></div>
        
        <p id="savingsPeriodLabel" class="text-[10px] font-black uppercase text-emerald-400 tracking-wider">Ahorro de este Mes</p>
        <div class="flex items-center justify-center space-x-1">
          <span class="text-xs font-extrabold text-emerald-300">Gs.</span>
          <h1 id="savingsMainAmount" class="text-3xl font-black text-white tracking-tight">542.000</h1>
        </div>
        <p id="savingsImpactPhrase" class="text-xs text-emerald-300/90 font-medium pt-0.5">
          ✨ ¡Evitaste pagar 25.2% de más en tus compras familiares!
        </p>

        <!-- Comparativa Sin PreciosPy vs Con PreciosPy -->
        <div class="mt-3 pt-3 border-t border-white/10 grid grid-cols-2 gap-2 text-left">
          <div class="p-2.5 rounded-2xl bg-slate-950/70 border border-slate-800/80">
            <p class="text-[9px] font-bold text-rose-400 uppercase">Sin PreciosPy</p>
            <p id="savingsWithoutPreciosPy" class="text-xs font-extrabold text-slate-400 line-through">Gs. 2.150.000</p>
            <span class="text-[9px] text-slate-500">Precio regular en góndola</span>
          </div>
          <div class="p-2.5 rounded-2xl bg-emerald-500/15 border border-emerald-500/30">
            <p class="text-[9px] font-bold text-emerald-400 uppercase">Con PreciosPy</p>
            <p id="savingsWithPreciosPy" class="text-xs font-black text-white">Gs. 1.608.000</p>
            <span class="text-[9px] text-emerald-300 font-bold">¡Tu precio final pagado!</span>
          </div>
        </div>
      </div>

      <!-- CÓMO SE LOGRÓ EL AHORRO (DESGLOSE PORCENTUAL) -->
      <div class="p-4 rounded-3xl bg-slate-900 border border-slate-800 space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-xs font-black uppercase text-slate-300 tracking-wider">¿Cómo se logró este ahorro?</span>
          <span class="text-[10px] font-bold text-emerald-400">100% Verificado</span>
        </div>

        <!-- Barra de progreso segmentada -->
        <div class="w-full h-3 rounded-full bg-slate-950 flex overflow-hidden p-0.5 border border-slate-800">
          <div class="bg-gradient-to-r from-emerald-500 to-teal-400 h-full rounded-l-full" style="width: 58%" title="58% Promos Bancarias"></div>
          <div class="bg-gradient-to-r from-sky-500 to-blue-500 h-full" style="width: 28%" title="28% Súper más barato"></div>
          <div class="bg-gradient-to-r from-purple-500 to-pink-500 h-full rounded-r-full" style="width: 14%" title="14% Modo Split"></div>
        </div>

        <div class="space-y-2 pt-1 text-xs">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
              <span class="text-slate-300 font-medium">💳 Promos Bancarias (ueno, Itaú)</span>
            </div>
            <span id="savingsBankShare" class="font-black text-white">Gs. 314.360 <span class="text-slate-400 text-[10px]">(58%)</span></span>
          </div>
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <span class="w-2.5 h-2.5 rounded-full bg-sky-400"></span>
              <span class="text-slate-300 font-medium">🏬 Elección de Súper Más Barato</span>
            </div>
            <span id="savingsStoreShare" class="font-black text-white">Gs. 151.760 <span class="text-slate-400 text-[10px]">(28%)</span></span>
          </div>
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <span class="w-2.5 h-2.5 rounded-full bg-purple-400"></span>
              <span class="text-slate-300 font-medium">✂️ Optimización Split (Dividir compras)</span>
            </div>
            <span id="savingsSplitShare" class="font-black text-white">Gs. 75.880 <span class="text-slate-400 text-[10px]">(14%)</span></span>
          </div>
        </div>
      </div>

      <!-- HISTORIAL DE COMPRAS REGISTRADAS -->
      <div class="p-4 rounded-3xl bg-slate-900 border border-slate-800 space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-xs font-black uppercase text-slate-300 tracking-wider">Historial de Compras Ahorradas</span>
          <button onclick="simulateAddPurchase()" class="text-[10px] font-bold text-emerald-400 hover:underline cursor-pointer">+ Simular compra</button>
        </div>

        <div id="savingsHistoryList" class="space-y-2">
          <!-- Render dinámico desde JavaScript con fechas, comercio y monto -->
        </div>
      </div>

      <!-- BOTÓN CERRAR / VOLVER -->
      <button onclick="closeSavingsModal()" class="w-full py-3.5 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-black text-xs transition active:scale-95 shadow-lg shadow-emerald-500/20">
        Continuar ahorrando en PreciosPy
      </button>

    </div>
  </div>

"""

content = content.replace(target_modal_pos, savings_modal_html + target_modal_pos, 1)

# 5. Insert JavaScript logic for Savings Dashboard
target_js = """    function saveLocalData() {"""
assert target_js in content, "target_js not found"

savings_js = """    // =========================================================================
    // MOTOR DE IMPACTO Y SEGUIMIENTO DE AHORRO REAL (SEMANA, MES, TOTAL)
    // =========================================================================
    let userSavings = {
      week: 128500,
      month: 542000,
      total: 1845000,
      spentWithPreciosPyMonth: 1608000,
      spentWithoutPreciosPyMonth: 2150000,
      activePeriod: 'month',
      history: [
        { id: 1, date: 'Hoy, 31 Oct', store: 'Supermercados Stock', saved: 48500, total: 112000, items: 6, tag: '💳 ueno N5 (40%)' },
        { id: 2, date: 'Jueves, 29 Oct', store: 'Superseis', saved: 36000, total: 144000, items: 4, tag: '💳 Itaú 20%' },
        { id: 3, date: 'Lunes, 26 Oct', store: 'Split Biggie + Superseis', saved: 44000, total: 138000, items: 9, tag: '🔀 Modo Split Inteligente' },
        { id: 4, date: 'Sábado, 24 Oct', store: 'Supermercado San Vicente', saved: 25000, total: 95000, items: 5, tag: '🏬 Oferta Caacupé' },
        { id: 5, date: 'Miércoles, 21 Oct', store: 'Tiendas Tuti', saved: 32000, total: 88000, items: 7, tag: '💳 Efectivo Tuti' }
      ]
    };

    function setSavingsPeriod(period) {
      userSavings.activePeriod = period;
      
      const btnW = document.getElementById('btnPeriodWeek');
      const btnM = document.getElementById('btnPeriodMonth');
      const btnT = document.getElementById('btnPeriodTotal');
      
      if (btnW && btnM && btnT) {
        const activeClass = "py-2 rounded-xl text-xs font-black transition-all bg-emerald-500 text-white shadow-md";
        const inactiveClass = "py-2 rounded-xl text-xs font-black transition-all text-slate-400 hover:text-white";
        
        btnW.className = period === 'week' ? activeClass : inactiveClass;
        btnM.className = period === 'month' ? activeClass : inactiveClass;
        btnT.className = period === 'total' ? activeClass : inactiveClass;
      }
      
      const lbl = document.getElementById('savingsPeriodLabel');
      const mainAmt = document.getElementById('savingsMainAmount');
      const phrase = document.getElementById('savingsImpactPhrase');
      const withoutEl = document.getElementById('savingsWithoutPreciosPy');
      const withEl = document.getElementById('savingsWithPreciosPy');
      const bankShareEl = document.getElementById('savingsBankShare');
      const storeShareEl = document.getElementById('savingsStoreShare');
      const splitShareEl = document.getElementById('savingsSplitShare');
      
      let amount = userSavings.month;
      let withoutAmt = userSavings.spentWithoutPreciosPyMonth;
      let withAmt = userSavings.spentWithPreciosPyMonth;
      let labelText = "Ahorro de este Mes";
      let impactText = "✨ ¡Evitaste pagar 25.2% de más en tus compras familiares!";
      
      if (period === 'week') {
        amount = userSavings.week;
        withoutAmt = Math.round(userSavings.week * 3.5);
        withAmt = withoutAmt - userSavings.week;
        labelText = "Ahorro de esta Semana";
        impactText = "✨ ¡Ahorraste 28.6% esta semana comparando tus compras!";
      } else if (period === 'total') {
        amount = userSavings.total;
        withoutAmt = Math.round(userSavings.total * 4.0);
        withAmt = withoutAmt - userSavings.total;
        labelText = "Ahorro Total Acumulado";
        impactText = "✨ ¡Llevas Gs. " + userSavings.total.toLocaleString('es-PY') + " ahorrados desde tu primera compra!";
      }
      
      if (lbl) lbl.innerText = labelText;
      if (mainAmt) mainAmt.innerText = amount.toLocaleString('es-PY');
      if (phrase) phrase.innerText = impactText;
      if (withoutEl) withoutEl.innerText = "Gs. " + withoutAmt.toLocaleString('es-PY');
      if (withEl) withEl.innerText = "Gs. " + withAmt.toLocaleString('es-PY');
      
      const bankAmt = Math.round(amount * 0.58);
      const storeAmt = Math.round(amount * 0.28);
      const splitAmt = amount - bankAmt - storeAmt;
      if (bankShareEl) bankShareEl.innerHTML = `Gs. ${bankAmt.toLocaleString('es-PY')} <span class="text-slate-400 text-[10px]">(58%)</span>`;
      if (storeShareEl) storeShareEl.innerHTML = `Gs. ${storeAmt.toLocaleString('es-PY')} <span class="text-slate-400 text-[10px]">(28%)</span>`;
      if (splitShareEl) splitShareEl.innerHTML = `Gs. ${splitAmt.toLocaleString('es-PY')} <span class="text-slate-400 text-[10px]">(14%)</span>`;
    }

    function renderSavingsDisplays() {
      const homeDisplay = document.getElementById('homeSavingsDisplay');
      if (homeDisplay) homeDisplay.innerText = userSavings.month.toLocaleString('es-PY');

      const pWeek = document.getElementById('profileSavingsWeek');
      if (pWeek) pWeek.innerText = "Gs. " + userSavings.week.toLocaleString('es-PY');
      const pMonth = document.getElementById('profileSavingsMonth');
      if (pMonth) pMonth.innerText = "Gs. " + userSavings.month.toLocaleString('es-PY');
      const pTotal = document.getElementById('profileSavingsTotal');
      if (pTotal) pTotal.innerText = "Gs. " + userSavings.total.toLocaleString('es-PY');

      const histContainer = document.getElementById('savingsHistoryList');
      if (histContainer && userSavings.history) {
        histContainer.innerHTML = userSavings.history.map(item => `
          <div class="p-3 rounded-2xl bg-slate-950/70 border border-slate-800 flex items-center justify-between">
            <div class="space-y-0.5">
              <div class="flex items-center space-x-2">
                <span class="text-xs font-black text-white">${item.store}</span>
                <span class="text-[9px] text-slate-400">${item.date}</span>
              </div>
              <div class="flex items-center space-x-2 text-[10px] text-slate-400">
                <span class="px-1.5 py-0.5 rounded-md bg-slate-800 text-slate-300 font-bold">${item.items} productos</span>
                <span class="text-emerald-400 font-bold">${item.tag}</span>
              </div>
            </div>
            <div class="text-right">
              <span class="text-[9px] text-slate-500 uppercase font-bold block">Ahorraste</span>
              <span class="text-xs font-black text-emerald-400">+ Gs. ${item.saved.toLocaleString('es-PY')}</span>
            </div>
          </div>
        `).join('');
      }
    }

    function openSavingsModal() {
      const modal = document.getElementById('savingsModal');
      if (modal) {
        renderSavingsDisplays();
        setSavingsPeriod(userSavings.activePeriod || 'month');
        modal.classList.remove('hidden');
      }
    }

    function closeSavingsModal() {
      const modal = document.getElementById('savingsModal');
      if (modal) modal.classList.add('hidden');
    }

    function registerCartPurchase() {
      const cartKeys = Object.keys(cart).filter(k => (cart[k] || 0) > 0);
      if (cartKeys.length === 0) {
        showToast('⚠️ Agrega productos a tu lista antes de registrar tu ahorro');
        return;
      }

      let regularSum = 0;
      let totalItems = 0;
      cartKeys.forEach(k => {
        const prod = products[k];
        const qty = cart[k];
        if (prod) {
          regularSum += prod.regularPrice * qty;
          totalItems += qty;
        }
      });

      const finalEl = document.getElementById('cartFinalTotal');
      let finalPaid = regularSum * 0.75;
      if (finalEl) {
        const rawNum = parseInt(finalEl.innerText.replace(/[^0-9]/g, ''));
        if (!isNaN(rawNum) && rawNum > 0) finalPaid = rawNum;
      }

      const savedThisCart = Math.max(15000, regularSum - finalPaid);

      userSavings.week += savedThisCart;
      userSavings.month += savedThisCart;
      userSavings.total += savedThisCart;
      userSavings.spentWithPreciosPyMonth += finalPaid;
      userSavings.spentWithoutPreciosPyMonth += regularSum;

      const currentStoreName = selectedCartStore === 'split' ? 'Split Biggie + Superseis' : (selectedCartStore || 'Supermercados Stock');
      userSavings.history.unshift({
        id: Date.now(),
        date: 'Hoy, ' + new Date().toLocaleDateString('es-PY', { day: 'numeric', month: 'short' }),
        store: currentStoreName,
        saved: savedThisCart,
        total: finalPaid,
        items: totalItems,
        tag: isSplitCartActive ? '🔀 Modo Split Inteligente' : ('💳 Oferta ' + currentStoreName)
      });

      saveLocalData();
      renderSavingsDisplays();

      showToast('🎉 ¡Ahorro registrado! Sumaste Gs. ' + savedThisCart.toLocaleString('es-PY') + ' a tu mes');
      setTimeout(() => openSavingsModal(), 600);
    }

    function simulateAddPurchase() {
      const mockSaved = 35000;
      const mockPaid = 95000;
      userSavings.week += mockSaved;
      userSavings.month += mockSaved;
      userSavings.total += mockSaved;
      userSavings.spentWithPreciosPyMonth += mockPaid;
      userSavings.spentWithoutPreciosPyMonth += (mockPaid + mockSaved);
      
      userSavings.history.unshift({
        id: Date.now(),
        date: 'Hoy, ' + new Date().toLocaleDateString('es-PY', { day: 'numeric', month: 'short' }),
        store: 'Supermercados Stock',
        saved: mockSaved,
        total: mockPaid,
        items: 5,
        tag: '💳 ueno N5 (40%)'
      });

      saveLocalData();
      renderSavingsDisplays();
      setSavingsPeriod(userSavings.activePeriod || 'month');
      showToast('🎉 ¡Simulación exitosa! + Gs. 35.000 añadidos al ahorro');
    }

"""

content = content.replace(target_js, savings_js + target_js, 1)

# Also update saveLocalData and loadSavedData to persist userSavings
target_save_local = """        localStorage.setItem('preciospy_2_cash_mode', JSON.stringify(isCashOnly));"""
assert target_save_local in content, "target_save_local not found"
content = content.replace(target_save_local, target_save_local + "\n        localStorage.setItem('preciospy_2_savings', JSON.stringify(userSavings));", 1)

target_load_saved = """        const rawCash = localStorage.getItem('preciospy_2_cash_mode');"""
assert target_load_saved in content, "target_load_saved not found"
savings_load = """        const rawSavings = localStorage.getItem('preciospy_2_savings');
        if (rawSavings) {
          try { userSavings = JSON.parse(rawSavings); } catch (e) {}
        }
"""
content = content.replace(target_load_saved, savings_load + "        " + target_load_saved, 1)

# Also call renderSavingsDisplays in DOMContentLoaded
target_dom_init = """      renderPromos();"""
assert target_dom_init in content, "target_dom_init not found"
content = content.replace(target_dom_init, target_dom_init + "\n      renderSavingsDisplays();", 1)

with open('scripts/build_html.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully patched Savings Tracker Dashboard into build_html.py!")
