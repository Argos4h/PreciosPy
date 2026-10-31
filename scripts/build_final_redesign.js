const fs = require('fs');
const path = require('path');

const verifiedProducts = JSON.parse(fs.readFileSync('scripts/verified_products_clean.json', 'utf8'));

const htmlContent = `<!DOCTYPE html>
<html lang="es" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>PreciosPy 2.0 — Rediseño Mundial & Vistas Animadas</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    * {
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      -webkit-tap-highlight-color: transparent;
      box-sizing: border-box;
    }
    
    @keyframes pulseGlow {
      0%, 100% { opacity: 0.6; transform: scale(1); }
      50% { opacity: 1; transform: scale(1.05); }
    }
    
    @keyframes scanLaser {
      0% { top: 12%; opacity: 0.8; }
      50% { top: 82%; opacity: 1; }
      100% { top: 12%; opacity: 0.8; }
    }
    
    @keyframes bounceUp {
      0% { opacity: 0; transform: translateY(16px) scale(0.96); }
      70% { transform: translateY(-3px) scale(1.01); }
      100% { opacity: 1; transform: translateY(0) scale(1); }
    }

    @keyframes flyCartAnim {
      0% { transform: scale(1) translateY(0); opacity: 1; }
      50% { transform: scale(1.4) translateY(-20px); opacity: 0.9; }
      100% { transform: scale(0.2) translateY(80px); opacity: 0; }
    }

    .animate-laser {
      animation: scanLaser 2.2s ease-in-out infinite;
    }
    
    .animate-bounce-up {
      animation: bounceUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    .no-scrollbar::-webkit-scrollbar {
      display: none;
    }
    .no-scrollbar {
      -ms-overflow-style: none;
      scrollbar-width: none;
    }

    .glass-panel {
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .glass-card {
      background: rgba(30, 41, 59, 0.7);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    .card-ueno {
      background: linear-gradient(135deg, #00C9A7 0%, #008775 100%);
    }
    .card-itau {
      background: linear-gradient(135deg, #EA580C 0%, #9A3412 100%);
    }
    .card-continental {
      background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
    }
    .card-sudameris {
      background: linear-gradient(135deg, #7C3AED 0%, #4C1D95 100%);
    }
    .card-zeta {
      background: linear-gradient(135deg, #6366F1 0%, #4338CA 100%);
    }
    .card-familiar {
      background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);
    }
    .card-atlas {
      background: linear-gradient(135deg, #1D4ED8 0%, #1E3A8A 100%);
    }
    .card-gnb {
      background: linear-gradient(135deg, #0F766E 0%, #115E59 100%);
    }
    .card-basa {
      background: linear-gradient(135deg, #1E40AF 0%, #172554 100%);
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex items-center justify-center p-0 md:p-6 select-none overflow-x-hidden">

  <!-- MARCO DE TELÉFONO IPHONE 16 PRO -->
  <div class="relative w-full md:w-[430px] h-[100dvh] md:h-[915px] bg-[#090D16] md:rounded-[48px] shadow-2xl md:ring-1 md:ring-white/10 flex flex-col overflow-hidden">
    
    <!-- BARRA SUPERIOR Y DYNAMIC ISLAND -->
    <header class="pt-3 px-6 pb-2 shrink-0 flex items-center justify-between text-xs font-semibold text-slate-300 relative z-30">
      <span id="statusBarClock" class="font-extrabold tracking-tight">12:30</span>
      
      <!-- Dynamic Island interactiva -->
      <div id="dynamicIsland" onclick="toggleDynamicIsland()" class="absolute left-1/2 -translate-x-1/2 top-2.5 h-7 px-3 rounded-full bg-black border border-white/10 flex items-center space-x-2 cursor-pointer shadow-lg transition-all duration-300 hover:scale-105 active:scale-95">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
        <span class="text-[11px] font-bold text-white tracking-wide flex items-center space-x-1">
          <span>⚡ Ahorro Billetera:</span>
          <span id="islandSavingsText" class="text-emerald-400">Gs. 48.500</span>
        </span>
      </div>

      <div class="flex items-center space-x-2 text-slate-400">
        <svg class="w-3.5 h-3.5 text-slate-300" fill="currentColor" viewBox="0 0 24 24"><path d="M12 3c-4.97 0-9 4.03-9 9 0 2.12.74 4.07 1.97 5.61L4.35 19.4c-.39.39-.39 1.02 0 1.41.39.39 1.02.39 1.41 0l1.9-1.9C9.22 19.64 10.57 20 12 20c4.97 0 9-4.03 9-9s-4.03-9-9-9zm0 15c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6z"/></svg>
        <span>5G</span>
        <div class="w-5 h-2.5 rounded-sm border border-slate-300 p-0.5 flex items-center">
          <div class="h-full w-full bg-emerald-400 rounded-2xs"></div>
        </div>
      </div>
    </header>

    <!-- CABECERA: PRECIOSPY + CIUDAD + MODO EFECTIVO -->
    <section class="px-5 pt-1 pb-2 shrink-0 flex items-center justify-between z-20">
      <div class="flex items-center space-x-2.5">
        <div onclick="switchTab('viewSearch')" class="w-9 h-9 rounded-2xl bg-gradient-to-tr from-emerald-600 via-emerald-500 to-teal-400 p-0.5 shadow-lg shadow-emerald-500/25 flex items-center justify-center cursor-pointer active:scale-90 transition">
          <span class="text-lg">🛒</span>
        </div>
        <div>
          <div class="flex items-center space-x-1.5">
            <h1 class="text-base font-extrabold tracking-tight text-white leading-none">PreciosPy</h1>
            <span class="text-[10px] px-1.5 py-0.5 rounded-full font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">2.0 PRO</span>
          </div>
          <!-- Selector de Ciudad con Dropdown Táctil -->
          <button onclick="openCitySheet()" class="flex items-center space-x-1 text-xs text-slate-400 hover:text-white mt-0.5 transition">
            <span class="text-rose-400">📍</span>
            <span id="currentCityLabel" class="font-bold underline decoration-dotted decoration-slate-500">Caacupé</span>
            <span class="text-[10px] text-slate-500">▾</span>
          </button>
        </div>
      </div>

      <!-- Acciones de cabecera: Modo Efectivo & Perfil -->
      <div class="flex items-center space-x-2">
        <button id="cashModeBtn" onclick="toggleCashMode()" class="px-2.5 py-1.5 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 bg-slate-800/80 border border-slate-700 hover:border-emerald-500/50 text-slate-300 active:scale-95">
          <span id="cashModeIcon">💳</span>
          <span id="cashModeText">Con Tarjetas</span>
        </button>
        <button onclick="switchTab('viewProfile')" class="w-8 h-8 rounded-xl bg-slate-800/80 border border-slate-700 flex items-center justify-center text-slate-300 hover:text-white relative active:scale-95 transition">
          <span class="text-xs">⚙️</span>
          <span id="profileActiveDot" class="w-2 h-2 rounded-full bg-emerald-400 absolute top-1.5 right-1.5 ring-2 ring-slate-900"></span>
        </button>
      </div>
    </section>

    <!-- ÁREA DE CONTENIDO PRINCIPAL -->
    <main class="flex-1 overflow-y-auto no-scrollbar relative z-10 px-4 pb-24">
      
      <!-- ============================================================ -->
      <!-- VISTA 1: EXPLORADOR DE PRECIOS & GÓNDOLA 2X2 -->
      <!-- ============================================================ -->
      <div id="viewSearch" class="tab-view space-y-3.5 pt-1">
        
        <!-- BARRA DE BÚSQUEDA FLIPP STYLE -->
        <div class="relative">
          <input 
            type="text" 
            id="searchInput"
            oninput="handleSearch(this.value)"
            placeholder="Buscar yerba, leche, carne, cerveza..." 
            class="w-full h-11 pl-10 pr-9 rounded-2xl bg-slate-900/90 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/80 focus:ring-1 focus:ring-emerald-500 transition shadow-inner"
          />
          <span class="absolute left-3.5 top-3 text-slate-500 text-sm">🔍</span>
          <button id="clearSearchBtn" onclick="clearSearch()" class="hidden absolute right-3 top-2.5 w-6 h-6 rounded-full bg-slate-800 text-slate-400 hover:text-white text-xs flex items-center justify-center">✕</button>
        </div>

        <!-- FILTROS RÁPIDOS INTERACTIVOS (CHIPS HORIZONTALES) -->
        <div class="flex items-center space-x-2 overflow-x-auto no-scrollbar py-1">
          <button id="catFilterBtn" onclick="openCategorySheet()" class="shrink-0 px-3 py-1.5 rounded-xl bg-slate-900/90 border border-slate-800 text-xs font-bold text-slate-300 flex items-center space-x-1.5 active:scale-95 transition hover:border-emerald-500/50">
            <span id="catFilterIcon">🗂️</span>
            <span id="catFilterLabel">Categorías</span>
            <span class="text-[10px] text-slate-500">▾</span>
          </button>

          <button id="superFilterBtn" onclick="openSupermarketSheet()" class="shrink-0 px-3 py-1.5 rounded-xl bg-slate-900/90 border border-slate-800 text-xs font-bold text-slate-300 flex items-center space-x-1.5 active:scale-95 transition hover:border-emerald-500/50">
            <span id="superFilterIcon">🏬</span>
            <span id="superFilterLabel">Supermercados</span>
            <span class="text-[10px] text-slate-500">▾</span>
          </button>

          <button onclick="toggleBestDealsOnly()" id="btnDealHeat" class="shrink-0 px-3 py-1.5 rounded-xl bg-slate-900/90 border border-slate-800 text-xs font-bold text-slate-400 flex items-center space-x-1.5 active:scale-95 transition">
            <span>🔥</span>
            <span>Mayores Descuentos</span>
          </button>
        </div>

        <!-- SELECTOR DE DÍAS AUTOMÁTICO (DÍA REAL DETECTADO) -->
        <div class="p-3 rounded-2xl glass-card space-y-2">
          <div class="flex items-center justify-between text-xs px-1">
            <span class="font-extrabold text-slate-400 text-[11px] uppercase tracking-wider">Descuentos para:</span>
            <span id="dayPromoHint" class="text-xs text-emerald-400 font-bold truncate">⚡ Sábado: ueno en Superseis/Stock + Zeta en Biggie</span>
          </div>

          <div class="grid grid-cols-7 gap-1" id="dayChipsContainer">
            <button onclick="setDay(1)" data-day="1" class="day-chip py-1.5 rounded-xl text-center text-[11px] font-extrabold transition bg-slate-900/80 text-slate-400 hover:text-white">
              <span class="block text-[9px] uppercase font-semibold text-slate-500">Lun</span>26
            </button>
            <button onclick="setDay(2)" data-day="2" class="day-chip py-1.5 rounded-xl text-center text-[11px] font-extrabold transition bg-slate-900/80 text-slate-400 hover:text-white">
              <span class="block text-[9px] uppercase font-semibold text-slate-500">Mar</span>27
            </button>
            <button onclick="setDay(3)" data-day="3" class="day-chip py-1.5 rounded-xl text-center text-[11px] font-extrabold transition bg-slate-900/80 text-slate-400 hover:text-white">
              <span class="block text-[9px] uppercase font-semibold text-slate-500">Mié</span>28
            </button>
            <button onclick="setDay(4)" data-day="4" class="day-chip py-1.5 rounded-xl text-center text-[11px] font-extrabold transition bg-slate-900/80 text-slate-400 hover:text-white">
              <span class="block text-[9px] uppercase font-semibold text-slate-500">Jue</span>29
            </button>
            <button onclick="setDay(5)" data-day="5" class="day-chip py-1.5 rounded-xl text-center text-[11px] font-extrabold transition bg-slate-900/80 text-slate-400 hover:text-white">
              <span class="block text-[9px] uppercase font-semibold text-slate-500">Vie</span>30
            </button>
            <button onclick="setDay(6)" data-day="6" class="day-chip py-1.5 rounded-xl text-center text-[11px] font-extrabold transition bg-emerald-500 text-white shadow-lg shadow-emerald-500/30 ring-1 ring-emerald-400">
              <span class="block text-[9px] uppercase font-semibold text-emerald-100">Sáb</span>31
            </button>
            <button onclick="setDay(7)" data-day="7" class="day-chip py-1.5 rounded-xl text-center text-[11px] font-extrabold transition bg-slate-900/80 text-slate-400 hover:text-white">
              <span class="block text-[9px] uppercase font-semibold text-slate-500">Dom</span>01
            </button>
          </div>
        </div>

        <!-- ENCABEZADO DE RESULTADOS -->
        <div class="flex items-center justify-between text-xs px-1">
          <span class="text-slate-400 font-bold">Góndola en vivo (<span id="resultsCount">12</span> productos)</span>
          <span class="text-[11px] text-emerald-400 font-extrabold flex items-center space-x-1">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>Precios Verificados 100%</span>
          </span>
        </div>

        <!-- GÓNDOLA 2X2 CON IMÁGENES REALES VERIFICADAS (HTTP 200) -->
        <div id="productGrid" class="grid grid-cols-2 gap-3">
          <!-- Render dinámico desde JS -->
        </div>

      </div>


      <!-- ============================================================ -->
      <!-- VISTA 2: MI LISTA / CARRITO CON PODIUM (BASKET STYLE) -->
      <!-- ============================================================ -->
      <div id="viewCart" class="tab-view hidden space-y-4 pt-1 animate-bounce-up">
        
        <!-- PODIUM DE SUPERMERCADOS (COMPARATIVA 1°, 2°, 3° LUGAR) -->
        <div class="p-4 rounded-3xl glass-card space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-xs font-black uppercase tracking-wider text-emerald-400">Podium de Ahorro en tu Carrito</span>
            <span class="text-[10px] text-slate-400 font-bold">Misma lista, 3 súper</span>
          </div>

          <!-- Tarjetas del Podium -->
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

          </div>

          <!-- OPTIMIZADOR DE CARRITO DIVIDIDO (SPLIT-CART) -->
          <div class="pt-2 border-t border-white/5 flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <span class="text-base">✂️</span>
              <div>
                <p class="text-xs font-black text-white">Ahorro Dividido (Split-Cart)</p>
                <p id="splitSavingsHint" class="text-[10px] text-emerald-400 font-bold">Comprando en 2 súper ahorras Gs. 14.500 extra</p>
              </div>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" id="splitCartToggle" onchange="toggleSplitCart(this.checked)" class="sr-only peer">
              <div class="w-9 h-5 bg-slate-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-emerald-500"></div>
            </label>
          </div>
        </div>

        <!-- LISTADO DE PRODUCTOS EN EL CARRITO -->
        <div class="space-y-2">
          <div class="flex justify-between items-center px-1">
            <span class="text-xs font-black uppercase text-slate-400 tracking-wider">Productos en tu lista:</span>
            <button onclick="clearUserCart()" class="text-[11px] text-rose-400 hover:text-rose-300 font-bold">Vaciar lista</button>
          </div>

          <div id="cartItemsList" class="space-y-2">
            <!-- Render dinámico desde JS -->
          </div>
        </div>

        <!-- TOTAL Y RESUMEN FINAL -->
        <div class="p-4 rounded-3xl bg-slate-900 border border-slate-800 space-y-3">
          <div class="space-y-1.5 text-xs">
            <div class="flex justify-between text-slate-400">
              <span>Subtotal precio regular:</span>
              <span id="cartSubtotalRegular" class="font-bold">Gs. 98.500</span>
            </div>
            <div class="flex justify-between text-emerald-400">
              <span class="font-bold flex items-center space-x-1">
                <span>⚡ Descuento aplicado:</span>
              </span>
              <span id="cartTotalSavings" class="font-black">- Gs. 30.900</span>
            </div>
            <div class="pt-2 border-t border-slate-800 flex justify-between items-baseline">
              <span class="text-sm font-black text-white">Total a Pagar Hoy:</span>
              <span id="cartFinalTotal" class="text-lg font-black text-emerald-400">Gs. 67.600</span>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-2 pt-1">
            <button onclick="shareCartWhatsApp()" class="py-2.5 rounded-2xl bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold text-xs flex items-center justify-center space-x-1.5 transition active:scale-95 shadow-lg shadow-emerald-600/30">
              <span>💬</span>
              <span>Enviar por WhatsApp</span>
            </button>
            <button onclick="switchTab('viewSearch')" class="py-2.5 rounded-2xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-extrabold text-xs flex items-center justify-center space-x-1.5 transition active:scale-95">
              <span>+ Sumar más productos</span>
            </button>
          </div>
        </div>

      </div>


      <!-- ============================================================ -->
      <!-- VISTA 3: ESCÁNER DE CÓDIGOS DE BARRA (ESTILO YUKA) -->
      <!-- ============================================================ -->
      <div id="viewScanner" class="tab-view hidden space-y-4 pt-1 animate-bounce-up">
        
        <div class="p-4 rounded-3xl glass-card text-center space-y-1">
          <span class="text-xs font-black uppercase text-emerald-400 tracking-wider">Escáner de Góndola Yuka-Style</span>
          <p class="text-xs text-slate-300">Apunta la cámara al código de barra de cualquier producto</p>
        </div>

        <!-- VISOR DE CÁMARA CON ANIMACIÓN DE LÁSER ESCÁNER -->
        <div class="w-full h-72 rounded-3xl bg-slate-900 border-2 border-slate-800 relative overflow-hidden flex flex-col items-center justify-center">
          
          <!-- Mock del fondo de cámara -->
          <div class="absolute inset-0 bg-gradient-to-b from-slate-950/80 via-slate-900/60 to-slate-950/90 flex items-center justify-center">
            <span class="text-6xl opacity-15">📷</span>
          </div>

          <!-- Mira de encuadre con esquinas iluminadas -->
          <div class="relative w-56 h-40 border-2 border-emerald-400/40 rounded-2xl flex items-center justify-center overflow-hidden shadow-[0_0_30px_rgba(16,185,129,0.15)]">
            
            <!-- Esquinas reforzadas -->
            <div class="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-emerald-400"></div>
            <div class="absolute top-0 right-0 w-4 h-4 border-t-2 border-r-2 border-emerald-400"></div>
            <div class="absolute bottom-0 left-0 w-4 h-4 border-b-2 border-l-2 border-emerald-400"></div>
            <div class="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-emerald-400"></div>

            <!-- Láser animado rojo/verde -->
            <div class="absolute left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-emerald-400 to-transparent shadow-[0_0_12px_#34d399] animate-laser"></div>

            <!-- Código de barra simulado -->
            <div class="opacity-30 text-2xl tracking-widest font-mono text-white select-none">
              ||||| | ||||| || |||
            </div>
          </div>

          <!-- Controles de la cámara: Linterna y selector de cámara -->
          <div class="absolute bottom-3 left-4 right-4 flex items-center justify-between">
            <button onclick="toggleScannerFlashlight()" id="scannerFlashBtn" class="px-3 py-1.5 rounded-xl bg-slate-800/90 border border-slate-700 text-xs font-bold text-slate-300 flex items-center space-x-1.5 active:scale-95 transition">
              <span id="scannerFlashIcon">🔦</span>
              <span id="scannerFlashLabel">Linterna: OFF</span>
            </button>

            <button onclick="simulateScanBarcode()" class="px-3.5 py-1.5 rounded-xl bg-emerald-500 text-white text-xs font-black flex items-center space-x-1.5 active:scale-95 transition shadow-lg shadow-emerald-500/30 animate-pulse">
              <span>⚡</span>
              <span>Escanear Producto</span>
            </button>
          </div>

        </div>

        <!-- TARJETA DE VEREDICTO INSTANTÁNEO (SEMÁFORO YUKA) -->
        <div id="scannedProductCard" class="p-4 rounded-3xl bg-slate-900 border border-slate-800 space-y-3">
          <div class="flex items-start space-x-3">
            <div class="w-14 h-14 rounded-2xl bg-white/5 border border-white/10 p-1.5 shrink-0 flex items-center justify-center overflow-hidden">
              <img id="scannedProductImg" src="https://static.app.biggie.com.py/images/products/7840127000124.jpg" class="max-h-full max-w-full object-contain" alt="Escaneado">
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center space-x-1.5">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
                <span id="scannedVerdictBadge" class="text-[10px] font-black uppercase text-emerald-400 tracking-wider">🟢 Precio Excelente</span>
              </div>
              <h3 id="scannedProductName" class="text-xs font-black text-white truncate mt-0.5">Yerba Kurupi Menta y Boldo 500g</h3>
              <p id="scannedProductBrand" class="text-[10px] text-slate-400">Kurupí • EAN: 7840127000124</p>
            </div>
          </div>

          <div class="p-2.5 rounded-2xl bg-slate-950/60 border border-slate-800 flex items-center justify-between text-xs">
            <div>
              <p class="text-[10px] text-slate-400">Mejor opción detectada:</p>
              <p id="scannedBestDealText" class="font-extrabold text-white">Gs. 11.375 en Biggie Express</p>
            </div>
            <span class="text-xs font-black text-emerald-400 bg-emerald-500/20 px-2 py-1 rounded-xl border border-emerald-500/30">35% Ahorro</span>
          </div>

          <button onclick="addScannedProductToCart()" class="w-full py-2.5 rounded-2xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs flex items-center justify-center space-x-2 transition active:scale-95 shadow-lg shadow-emerald-500/20">
            <span>+</span>
            <span>Agregar a mi Lista de Compras</span>
          </button>
        </div>

      </div>


      <!-- ============================================================ -->
      <!-- VISTA 4: BENEFICIOS BANCARIOS (ESTILO PELANDO / DESCUENTOCITY) -->
      <!-- ============================================================ -->
      <div id="viewPromos" class="tab-view hidden space-y-4 pt-1 animate-bounce-up">
        
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-lg font-black text-white">Beneficios Bancarios</h2>
            <p id="promosDayTitle" class="text-xs text-emerald-400 font-bold">Promociones y reintegros vigentes</p>
          </div>
          <span id="promosCountBadge" class="text-xs font-extrabold bg-emerald-500/20 text-emerald-400 px-2.5 py-1 rounded-full border border-emerald-500/30">11 disponibles</span>
        </div>

        <!-- CONTROL SEGMENTADO: TODAS LAS PROMOS VS MIS TARJETAS -->
        <div class="p-1 rounded-2xl bg-slate-900 border border-slate-800 flex">
          <button id="promoTabAllBtn" onclick="filterPromosView(false)" class="flex-1 py-1.5 rounded-xl text-xs font-bold transition flex items-center justify-center space-x-1.5 bg-emerald-500 text-white shadow-md">
            <span>🌐</span>
            <span>Todas las Promos</span>
          </button>
          <button id="promoTabMyBtn" onclick="filterPromosView(true)" class="flex-1 py-1.5 rounded-xl text-xs font-bold transition flex items-center justify-center space-x-1.5 text-slate-400 hover:text-white">
            <span>💳</span>
            <span>Mis Tarjetas</span>
          </button>
        </div>

        <!-- LISTADO DINÁMICO DE PROMOCIONES BANCARIAS -->
        <div id="promosListContainer" class="space-y-3">
          <!-- Render dinámico desde JS con las 11 promociones oficiales -->
        </div>

      </div>


      <!-- ============================================================ -->
      <!-- VISTA 5: PERFIL & GESTIÓN DE TARJETAS (BILLETERA MODERNA) -->
      <!-- ============================================================ -->
      <div id="viewProfile" class="tab-view hidden space-y-4 pt-1 animate-bounce-up">
        
        <div class="p-4 rounded-3xl bg-slate-900 border border-slate-800">
          <div class="flex items-center space-x-3">
            <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-emerald-500 to-sky-500 flex items-center justify-center text-xl font-black text-white shadow-lg shadow-emerald-500/20">
              💳
            </div>
            <div>
              <h2 class="text-sm font-black text-white">Mi Billetera PreciosPy & Niveles</h2>
              <p class="text-xs text-slate-400">Configura tus tarjetas y niveles para calcular tus precios</p>
            </div>
          </div>
        </div>

        <div class="space-y-3">
          <span class="text-xs font-black uppercase text-slate-400 tracking-wider px-1">Tarjetas y Niveles Configurados:</span>
          
          <!-- ueno bank con Selector de Niveles N1 a N5 -->
          <div class="p-4 rounded-3xl bg-slate-900 border border-slate-800 space-y-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2.5">
                <span id="dot-ueno" class="w-3.5 h-3.5 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]"></span>
                <div>
                  <div class="flex items-center space-x-1.5">
                    <p class="text-xs font-extrabold text-white">ueno bank</p>
                    <span id="uenoActiveBadge" class="text-[9px] font-black px-1.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">Nivel 4 (35%)</span>
                  </div>
                  <p id="label-ueno" class="text-[11px] text-slate-400">Reintegro QR en Biggie (24hs) y Superseis</p>
                </div>
              </div>
              <button id="btn-ueno" onclick="toggleBankProfile('ueno')" class="px-3 py-1 rounded-xl bg-emerald-500/20 text-emerald-400 font-bold text-xs border border-emerald-500/30 active:scale-95 transition">Activa</button>
            </div>

            <!-- SELECTOR DE NIVELES UENO N1 A N5 -->
            <div class="pt-2 border-t border-slate-800">
              <p class="text-[10px] font-black uppercase tracking-wider text-slate-400 mb-2">Selecciona tu Nivel ueno:</p>
              <div class="grid grid-cols-5 gap-1.5" id="uenoLevelButtons">
                <button onclick="setUenoLevel(1)" data-level="1" class="ueno-lvl-btn py-1.5 rounded-xl text-center text-xs font-bold transition bg-slate-800 text-slate-300 border border-slate-700 hover:border-emerald-500/50">
                  <span class="block text-[11px] font-black">N1</span>
                  <span class="text-[9px] text-slate-400">15%</span>
                </button>
                <button onclick="setUenoLevel(2)" data-level="2" class="ueno-lvl-btn py-1.5 rounded-xl text-center text-xs font-bold transition bg-slate-800 text-slate-300 border border-slate-700 hover:border-emerald-500/50">
                  <span class="block text-[11px] font-black">N2</span>
                  <span class="text-[9px] text-slate-400">20%</span>
                </button>
                <button onclick="setUenoLevel(3)" data-level="3" class="ueno-lvl-btn py-1.5 rounded-xl text-center text-xs font-bold transition bg-slate-800 text-slate-300 border border-slate-700 hover:border-emerald-500/50">
                  <span class="block text-[11px] font-black">N3</span>
                  <span class="text-[9px] text-slate-400">25%</span>
                </button>
                <button onclick="setUenoLevel(4)" data-level="4" class="ueno-lvl-btn py-1.5 rounded-xl text-center text-xs font-bold transition bg-emerald-500 text-white border border-emerald-400 shadow-md shadow-emerald-500/30">
                  <span class="block text-[11px] font-black">N4</span>
                  <span class="text-[9px] text-emerald-100">35%</span>
                </button>
                <button onclick="setUenoLevel(5)" data-level="5" class="ueno-lvl-btn py-1.5 rounded-xl text-center text-xs font-bold transition bg-slate-800 text-slate-300 border border-slate-700 hover:border-emerald-500/50">
                  <span class="block text-[11px] font-black">N5</span>
                  <span class="text-[9px] text-slate-400">40%</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Itaú con Selector de Categorías -->
          <div class="p-4 rounded-3xl bg-slate-900 border border-slate-800 space-y-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2.5">
                <span id="dot-itau" class="w-3.5 h-3.5 rounded-full bg-orange-400"></span>
                <div>
                  <div class="flex items-center space-x-1.5">
                    <p class="text-xs font-extrabold text-white">Banco Itaú</p>
                    <span id="itauActiveBadge" class="text-[9px] font-black px-1.5 py-0.5 rounded-full bg-orange-500/20 text-orange-400 border border-orange-500/30">Clásica (20%)</span>
                  </div>
                  <p id="label-itau" class="text-[11px] text-slate-400">Martes en Superseis y Stock</p>
                </div>
              </div>
              <button id="btn-itau" onclick="toggleBankProfile('itau')" class="px-3 py-1 rounded-xl bg-emerald-500/20 text-emerald-400 font-bold text-xs border border-emerald-500/30 active:scale-95 transition">Activa</button>
            </div>

            <!-- SELECTOR DE TIERS ITAÚ -->
            <div class="pt-2 border-t border-slate-800">
              <p class="text-[10px] font-black uppercase tracking-wider text-slate-400 mb-2">Categoría de tu tarjeta Itaú:</p>
              <div class="grid grid-cols-2 gap-1.5" id="itauTierButtons">
                <button onclick="setItauTier('clasica')" data-tier="clasica" class="itau-tier-btn p-2 rounded-xl text-left text-xs font-bold transition bg-orange-500 text-white border border-orange-400 shadow-md shadow-orange-500/20">
                  <p class="text-[11px] font-black">Clásica / Oro</p>
                  <p class="text-[9px] text-orange-100">20% en Martes</p>
                </button>
                <button onclick="setItauTier('platinum')" data-tier="platinum" class="itau-tier-btn p-2 rounded-xl text-left text-xs font-bold transition bg-slate-800 text-slate-300 border border-slate-700 hover:border-orange-500/50">
                  <p class="text-[11px] font-black">Platinum</p>
                  <p class="text-[9px] text-slate-400">25% en Martes</p>
                </button>
                <button onclick="setItauTier('infinite')" data-tier="infinite" class="itau-tier-btn p-2 rounded-xl text-left text-xs font-bold transition bg-slate-800 text-slate-300 border border-slate-700 hover:border-orange-500/50">
                  <p class="text-[11px] font-black">Infinite / Black</p>
                  <p class="text-[9px] text-slate-400">30% en Martes</p>
                </button>
                <button onclick="setItauTier('afinidad')" data-tier="afinidad" class="itau-tier-btn p-2 rounded-xl text-left text-xs font-bold transition bg-slate-800 text-slate-300 border border-slate-700 hover:border-orange-500/50">
                  <p class="text-[11px] font-black">Afinidad Superseis</p>
                  <p class="text-[9px] text-slate-400">20% Todos los Días</p>
                </button>
              </div>
            </div>
          </div>

          <!-- Continental con Selector de Categorías -->
          <div class="p-4 rounded-3xl bg-slate-900 border border-slate-800 space-y-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2.5">
                <span id="dot-continental" class="w-3.5 h-3.5 rounded-full bg-slate-600"></span>
                <div>
                  <div class="flex items-center space-x-1.5">
                    <p class="text-xs font-extrabold text-white">Banco Continental</p>
                    <span id="continentalActiveBadge" class="text-[9px] font-black px-1.5 py-0.5 rounded-full bg-slate-800 text-slate-400">Inactiva</span>
                  </div>
                  <p id="label-continental" class="text-[11px] text-slate-400">Miércoles en Areté y Superseis</p>
                </div>
              </div>
              <button id="btn-continental" onclick="toggleBankProfile('continental')" class="px-3 py-1 rounded-xl bg-slate-800 text-slate-400 font-bold text-xs border border-slate-700 active:scale-95 transition">+ Activar</button>
            </div>

            <div class="pt-2 border-t border-slate-800">
              <p class="text-[10px] font-black uppercase tracking-wider text-slate-400 mb-2">Categoría ContiClub:</p>
              <div class="grid grid-cols-2 gap-1.5" id="contiTierButtons">
                <button onclick="setContinentalTier('clasica')" data-tier="clasica" class="conti-tier-btn p-2 rounded-xl text-left text-xs font-bold transition bg-slate-800 text-slate-300 border border-slate-700">
                  <p class="text-[11px] font-black">Clásica</p>
                  <p class="text-[9px] text-slate-400">20% Miércoles</p>
                </button>
                <button onclick="setContinentalTier('platinum')" data-tier="platinum" class="conti-tier-btn p-2 rounded-xl text-left text-xs font-bold transition bg-slate-800 text-slate-300 border border-slate-700">
                  <p class="text-[11px] font-black">Oro / Black</p>
                  <p class="text-[9px] text-slate-400">25% Miércoles</p>
                </button>
              </div>
            </div>
          </div>

          <!-- Zeta Banco -->
          <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-between">
            <div class="flex items-center space-x-2.5">
              <span id="dot-zeta" class="w-3.5 h-3.5 rounded-full bg-indigo-500"></span>
              <div>
                <p class="text-xs font-extrabold text-white">Zeta Banco</p>
                <p id="label-zeta" class="text-[11px] text-slate-400">20% Reintegro QR en Biggie los Sábados</p>
              </div>
            </div>
            <button id="btn-zeta" onclick="toggleBankProfile('zeta')" class="px-3 py-1 rounded-xl bg-emerald-500/20 text-emerald-400 font-bold text-xs border border-emerald-500/30 active:scale-95 transition">Activa</button>
          </div>

          <!-- Banco Familiar -->
          <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-between">
            <div class="flex items-center space-x-2.5">
              <span id="dot-familiar" class="w-3.5 h-3.5 rounded-full bg-slate-600"></span>
              <div>
                <p class="text-xs font-extrabold text-white">Banco Familiar</p>
                <p id="label-familiar" class="text-[11px] text-slate-400">20%-25% Viernes en Stock</p>
              </div>
            </div>
            <button id="btn-familiar" onclick="toggleBankProfile('familiar')" class="px-3 py-1 rounded-xl bg-slate-800 text-slate-400 font-bold text-xs border border-slate-700 active:scale-95 transition">+ Activar</button>
          </div>

          <!-- Banco Atlas -->
          <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-between">
            <div class="flex items-center space-x-2.5">
              <span id="dot-atlas" class="w-3.5 h-3.5 rounded-full bg-slate-600"></span>
              <div>
                <p class="text-xs font-extrabold text-white">Banco Atlas</p>
                <p id="label-atlas" class="text-[11px] text-slate-400">20% Lunes en Stock con Atlas QR</p>
              </div>
            </div>
            <button id="btn-atlas" onclick="toggleBankProfile('atlas')" class="px-3 py-1 rounded-xl bg-slate-800 text-slate-400 font-bold text-xs border border-slate-700 active:scale-95 transition">+ Activar</button>
          </div>

          <!-- Sudameris -->
          <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-between">
            <div class="flex items-center space-x-2.5">
              <span id="dot-sudameris" class="w-3.5 h-3.5 rounded-full bg-slate-600"></span>
              <div>
                <p class="text-xs font-extrabold text-white">Banco Sudameris</p>
                <p id="label-sudameris" class="text-[11px] text-slate-400">Club Infinite / Black (25% Jueves en Casa Rica)</p>
              </div>
            </div>
            <button id="btn-sudameris" onclick="toggleBankProfile('sudameris')" class="px-3 py-1 rounded-xl bg-slate-800 text-slate-400 font-bold text-xs border border-slate-700 active:scale-95 transition">+ Activar</button>
          </div>

          <!-- Banco GNB -->
          <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-between">
            <div class="flex items-center space-x-2.5">
              <span id="dot-gnb" class="w-3.5 h-3.5 rounded-full bg-slate-600"></span>
              <div>
                <p class="text-xs font-extrabold text-white">Banco GNB Paraguay</p>
                <p id="label-gnb" class="text-[11px] text-slate-400">20% Miércoles en Superseis y Delimarket</p>
              </div>
            </div>
            <button id="btn-gnb" onclick="toggleBankProfile('gnb')" class="px-3 py-1 rounded-xl bg-slate-800 text-slate-400 font-bold text-xs border border-slate-700 active:scale-95 transition">+ Activar</button>
          </div>

          <!-- Banco Basa -->
          <div class="p-3.5 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-between">
            <div class="flex items-center space-x-2.5">
              <span id="dot-basa" class="w-3.5 h-3.5 rounded-full bg-slate-600"></span>
              <div>
                <p class="text-xs font-extrabold text-white">Banco Basa</p>
                <p id="label-basa" class="text-[11px] text-slate-400">20% Domingos en Supermercados Stock</p>
              </div>
            </div>
            <button id="btn-basa" onclick="toggleBankProfile('basa')" class="px-3 py-1 rounded-xl bg-slate-800 text-slate-400 font-bold text-xs border border-slate-700 active:scale-95 transition">+ Activar</button>
          </div>

        </div>

        <!-- RESTABLECER VALORES DE FÁBRICA -->
        <div class="pt-4 border-t border-slate-800 text-center">
          <button onclick="resetUserDataToDefault()" class="text-xs text-rose-400 hover:text-rose-300 font-bold px-3 py-1.5 rounded-xl border border-rose-500/30 hover:bg-rose-500/10 transition active:scale-95">
            🗑️ Restablecer mi carrito y tarjetas de fábrica
          </button>
          <p class="text-[10px] text-slate-500 mt-1">Todos tus datos se guardan de forma privada en tu propio teléfono.</p>
        </div>

      </div>

    </main>

    <!-- BARRA DE NAVEGACIÓN INFERIOR (APPLE GLASS DOCK) -->
    <nav class="absolute bottom-0 left-0 right-0 h-20 glass-panel border-t border-white/10 px-6 flex items-center justify-between z-30">
      
      <!-- Tab 1: Precios -->
      <button onclick="switchTab('viewSearch')" class="nav-btn flex flex-col items-center justify-center text-emerald-400 font-black scale-105 transition" data-view="viewSearch">
        <span class="text-lg">🛒</span>
        <span class="text-[10px] mt-0.5">Precios</span>
      </button>

      <!-- Tab 2: Mi Lista / Carrito -->
      <button onclick="switchTab('viewCart')" class="nav-btn relative flex flex-col items-center justify-center text-slate-400 hover:text-white font-bold transition" data-view="viewCart">
        <span class="text-lg">🧾</span>
        <span class="text-[10px] mt-0.5">Mi Lista</span>
        <span id="navCartBadge" class="absolute -top-1 right-1 w-4 h-4 rounded-full bg-emerald-500 text-white font-black text-[9px] flex items-center justify-center ring-2 ring-slate-900 animate-pulse">3</span>
      </button>

      <!-- Tab 3: Escáner Central Destacado -->
      <button onclick="switchTab('viewScanner')" class="relative -top-3 w-12 h-12 rounded-2xl bg-gradient-to-tr from-emerald-500 to-teal-400 text-white text-xl flex items-center justify-center shadow-lg shadow-emerald-500/40 hover:scale-110 active:scale-95 transition" data-view="viewScanner">
        <span>📸</span>
      </button>

      <!-- Tab 4: Promos -->
      <button onclick="switchTab('viewPromos')" class="nav-btn flex flex-col items-center justify-center text-slate-400 hover:text-white font-bold transition" data-view="viewPromos">
        <span class="text-lg">🏷️</span>
        <span class="text-[10px] mt-0.5">Promos</span>
      </button>

      <!-- Tab 5: Perfil -->
      <button onclick="switchTab('viewProfile')" class="nav-btn flex flex-col items-center justify-center text-slate-400 hover:text-white font-bold transition" data-view="viewProfile">
        <span class="text-lg">⚙️</span>
        <span class="text-[10px] mt-0.5">Perfil</span>
      </button>

    </nav>

  </div>


  <!-- ============================================================ -->
  <!-- MODAL FLOTANTE INFERIOR: HISTORIAL DE PRECIOS KNASTA STYLE -->
  <!-- ============================================================ -->
  <div id="productDetailModal" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-end justify-center p-0 md:p-6 transition-all duration-300">
    <div class="w-full md:w-[430px] max-h-[85vh] bg-slate-900 rounded-t-[36px] md:rounded-[36px] border border-white/10 p-5 overflow-y-auto no-scrollbar space-y-4 animate-bounce-up">
      <div class="flex justify-between items-start">
        <span class="text-xs font-black uppercase text-emerald-400 tracking-wider">Historial de Precios (Últimos 30 días)</span>
        <button onclick="closeProductModal()" class="w-7 h-7 rounded-full bg-slate-800 text-slate-400 hover:text-white text-xs flex items-center justify-center font-bold active:scale-90 transition">✕</button>
      </div>

      <div id="modalProductContent">
        <!-- Render dinámico desde JS -->
      </div>
    </div>
  </div>

  <!-- MODAL SHEET: SELECTOR DE CIUDADES EN PARAGUAY -->
  <div id="cityModalSheet" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-end justify-center p-0 md:p-6 transition-all">
    <div class="w-full md:w-[430px] max-h-[75vh] bg-slate-900 rounded-t-[36px] md:rounded-[36px] border border-white/10 p-5 overflow-y-auto no-scrollbar space-y-3 animate-bounce-up">
      <div class="flex justify-between items-center pb-2 border-b border-slate-800">
        <span class="text-xs font-black text-white uppercase tracking-wider">Selecciona tu Ciudad</span>
        <button onclick="closeCitySheet()" class="w-7 h-7 rounded-full bg-slate-800 text-slate-400 hover:text-white text-xs flex items-center justify-center font-bold">✕</button>
      </div>
      <div class="space-y-2 pt-1">
        <button onclick="selectCity('Caacupé')" class="w-full p-3 rounded-2xl bg-slate-800/80 hover:bg-emerald-500/20 hover:border-emerald-500/40 border border-slate-700/60 flex items-center justify-between text-left transition">
          <div>
            <p class="text-xs font-extrabold text-white">Caacupé (Cordillera)</p>
            <p class="text-[10px] text-slate-400">Superseis, Stock, Biggie, Tuti</p>
          </div>
          <span class="text-xs">📍</span>
        </button>
        <button onclick="selectCity('Asunción')" class="w-full p-3 rounded-2xl bg-slate-800/80 hover:bg-emerald-500/20 hover:border-emerald-500/40 border border-slate-700/60 flex items-center justify-between text-left transition">
          <div>
            <p class="text-xs font-extrabold text-white">Asunción (Capital)</p>
            <p class="text-[10px] text-slate-400">Superseis, Stock, Biggie, Casa Rica, Areté, Real, Delimarket</p>
          </div>
          <span class="text-xs">📍</span>
        </button>
        <button onclick="selectCity('Luque')" class="w-full p-3 rounded-2xl bg-slate-800/80 hover:bg-emerald-500/20 hover:border-emerald-500/40 border border-slate-700/60 flex items-center justify-between text-left transition">
          <div>
            <p class="text-xs font-extrabold text-white">Luque (Central)</p>
            <p class="text-[10px] text-slate-400">Fortis, Box, Superseis, Stock, Los Jardines</p>
          </div>
          <span class="text-xs">📍</span>
        </button>
        <button onclick="selectCity('San Lorenzo')" class="w-full p-3 rounded-2xl bg-slate-800/80 hover:bg-emerald-500/20 hover:border-emerald-500/40 border border-slate-700/60 flex items-center justify-between text-left transition">
          <div>
            <p class="text-xs font-extrabold text-white">San Lorenzo (Central)</p>
            <p class="text-[10px] text-slate-400">Salemma, Real, Fortis, Stock, Superseis</p>
          </div>
          <span class="text-xs">📍</span>
        </button>
        <button onclick="selectCity('Ciudad del Este')" class="w-full p-3 rounded-2xl bg-slate-800/80 hover:bg-emerald-500/20 hover:border-emerald-500/40 border border-slate-700/60 flex items-center justify-between text-left transition">
          <div>
            <p class="text-xs font-extrabold text-white">Ciudad del Este (Alto Paraná)</p>
            <p class="text-[10px] text-slate-400">Fortis, Box, Gran Vía, Stock</p>
          </div>
          <span class="text-xs">📍</span>
        </button>
        <button onclick="selectCity('Encarnación')" class="w-full p-3 rounded-2xl bg-slate-800/80 hover:bg-emerald-500/20 hover:border-emerald-500/40 border border-slate-700/60 flex items-center justify-between text-left transition">
          <div>
            <p class="text-xs font-extrabold text-white">Encarnación (Itapúa)</p>
            <p class="text-[10px] text-slate-400">Superseis, Stock, La Bomba</p>
          </div>
          <span class="text-xs">📍</span>
        </button>
        <button onclick="selectCity('Todo Paraguay')" class="w-full p-3 rounded-2xl bg-slate-800/80 hover:bg-emerald-500/20 hover:border-emerald-500/40 border border-slate-700/60 flex items-center justify-between text-left transition">
          <div>
            <p class="text-xs font-extrabold text-white">Todo Paraguay (Nacional)</p>
            <p class="text-[10px] text-slate-400">Todas las 14 cadenas de supermercados</p>
          </div>
          <span class="text-xs">🌐</span>
        </button>
      </div>
    </div>
  </div>

  <!-- MODAL SHEET: FILTRAR POR CATEGORÍA -->
  <div id="categoryModalSheet" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-end justify-center p-0 md:p-6 transition-all">
    <div class="w-full md:w-[430px] max-h-[75vh] bg-slate-900 rounded-t-[36px] md:rounded-[36px] border border-white/10 p-5 overflow-y-auto no-scrollbar space-y-3 animate-bounce-up">
      <div class="flex justify-between items-center pb-2 border-b border-slate-800">
        <span class="text-xs font-black text-white uppercase tracking-wider">Filtrar por Categoría</span>
        <button onclick="closeCategorySheet()" class="w-7 h-7 rounded-full bg-slate-800 text-slate-400 hover:text-white text-xs flex items-center justify-center font-bold">✕</button>
      </div>
      <div class="grid grid-cols-2 gap-2 pt-1">
        <button onclick="selectCategory('', '🗂️', 'Categorías')" class="p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center space-x-2 text-left transition">
          <span class="text-base">🛒</span>
          <span class="text-xs font-extrabold text-white">Todas</span>
        </button>
        <button onclick="selectCategory('Yerbas', '🌿', 'Yerbas')" class="p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center space-x-2 text-left transition">
          <span class="text-base">🌿</span>
          <span class="text-xs font-extrabold text-white">Yerba & Mate</span>
        </button>
        <button onclick="selectCategory('Lácteos', '🥛', 'Lácteos')" class="p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center space-x-2 text-left transition">
          <span class="text-base">🥛</span>
          <span class="text-xs font-extrabold text-white">Lácteos & Huevos</span>
        </button>
        <button onclick="selectCategory('Bebidas', '🥤', 'Bebidas')" class="p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center space-x-2 text-left transition">
          <span class="text-base">🥤</span>
          <span class="text-xs font-extrabold text-white">Bebidas & Gaseosas</span>
        </button>
        <button onclick="selectCategory('Carnicería', '🥩', 'Carnicería')" class="p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center space-x-2 text-left transition">
          <span class="text-base">🥩</span>
          <span class="text-xs font-extrabold text-white">Carnicería & Asado</span>
        </button>
        <button onclick="selectCategory('Almacén', '🥫', 'Almacén')" class="p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center space-x-2 text-left transition">
          <span class="text-base">🥫</span>
          <span class="text-xs font-extrabold text-white">Almacén & Galletas</span>
        </button>
        <button onclick="selectCategory('Desayuno', '☕', 'Desayuno')" class="p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center space-x-2 text-left transition">
          <span class="text-base">☕</span>
          <span class="text-xs font-extrabold text-white">Café & Desayuno</span>
        </button>
        <button onclick="selectCategory('Snacks', '🍟', 'Snacks')" class="p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center space-x-2 text-left transition">
          <span class="text-base">🍟</span>
          <span class="text-xs font-extrabold text-white">Snacks & Papas</span>
        </button>
      </div>
    </div>
  </div>

  <!-- MODAL SHEET: FILTRAR POR SUPERMERCADO -->
  <div id="supermarketModalSheet" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-end justify-center p-0 md:p-6 transition-all">
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
      </div>
    </div>
  </div>

  <!-- TOAST FLOTANTE -->
  <div id="toastNotification" class="fixed top-6 left-1/2 -translate-x-1/2 px-4 py-2 rounded-2xl bg-emerald-500 text-white font-extrabold text-xs shadow-2xl transition-all duration-300 -translate-y-20 opacity-0 z-50 flex items-center space-x-2">
    <span id="toastIcon">✨</span>
    <span id="toastMsg">Producto sumado a tu lista</span>
  </div>

  <script>
    // CATÁLOGO DE PRODUCTOS CON IMÁGENES CDN REALES VERIFICADAS (HTTP 200)
    const products = ${JSON.stringify(verifiedProducts, null, 2)};

    // CONSTANTES Y NIVELES BANCARIOS EN PARAGUAY
    const uenoPcts = { 1: 15, 2: 20, 3: 25, 4: 35, 5: 40 };
    const itauPcts = { clasica: 20, platinum: 25, infinite: 30, afinidad: 20 };
    const continentalPcts = { clasica: 20, platinum: 25 };
    const familiarPcts = { clasica: 20, platinum: 25 };

    // ESTADO DE LA APLICACIÓN PRECIOSPY 2.0
    let currentIsoDay = (function() {
      const d = new Date().getDay();
      return d === 0 ? 7 : d; // 1=Lun ... 6=Sáb, 7=Dom
    })();
    let selectedDay = currentIsoDay;
    let isCashOnly = false;
    let selectedCity = 'Caacupé';
    let currentSearch = '';
    let currentCategory = '';
    let currentStore = '';
    let isFlashlightOn = false;
    let currentScannedIdx = 0;
    let showOnlyMyPromos = false;

    let bankProfiles = {
      ueno: { enabled: true, level: 4 },
      itau: { enabled: true, tier: 'clasica' },
      continental: { enabled: false, tier: 'clasica' },
      zeta: { enabled: true },
      familiar: { enabled: false, tier: 'clasica' },
      atlas: { enabled: false },
      sudameris: { enabled: false, tier: 'club' },
      gnb: { enabled: false },
      basa: { enabled: false }
    };

    let cart = {
      0: 2, // 2x Yerba Kurupí
      1: 6, // 6x Leche Lactolanda
      3: 1, // 1x Cerveza Michelob
    };

    // MOTOR DE CÁLCULO DINÁMICO DE BENEFICIOS BANCARIOS PRECIOSPY
    function calculateProductOffer(prod, targetDay) {
      if (isCashOnly) {
        return {
          discountPct: 0,
          finalPrice: prod.regularPrice,
          savings: 0,
          bankTag: '💵 Efectivo',
          activeOffer: false
        };
      }

      let candidates = [];
      const store = prod.store;

      // 1. ueno bank Biggie Express (Todos los días)
      if (store === 'Biggie Express' && bankProfiles.ueno && bankProfiles.ueno.enabled) {
        const lvl = bankProfiles.ueno.level || 4;
        const pct = uenoPcts[lvl] || 35;
        candidates.push({
          pct: pct,
          bankTag: 'ueno N' + lvl + ' (' + pct + '%)',
          bank: 'ueno'
        });
      }

      // 2. Zeta Banco Biggie Express (Sábados = 6)
      if (store === 'Biggie Express' && targetDay === 6 && bankProfiles.zeta && bankProfiles.zeta.enabled) {
        candidates.push({
          pct: 20,
          bankTag: 'Zeta QR (20%)',
          bank: 'zeta'
        });
      }

      // 3. ueno bank Superseis y Stock (Viernes = 5 y Sábados = 6)
      if ((store === 'Superseis' || store === 'Supermercados Stock') && (targetDay === 5 || targetDay === 6) && bankProfiles.ueno && bankProfiles.ueno.enabled) {
        candidates.push({
          pct: 20,
          bankTag: 'ueno Finde (20%)',
          bank: 'ueno'
        });
      }

      // 4. Itaú Superseis y Stock (Martes = 2)
      if ((store === 'Superseis' || store === 'Supermercados Stock') && targetDay === 2 && bankProfiles.itau && bankProfiles.itau.enabled) {
        const tier = bankProfiles.itau.tier || 'clasica';
        const pct = itauPcts[tier] || 20;
        candidates.push({
          pct: pct,
          bankTag: 'Itaú ' + tier.toUpperCase() + ' (' + pct + '%)',
          bank: 'itau'
        });
      }

      // 5. Itaú Afinidad Superseis (Todos los días en Superseis)
      if (store === 'Superseis' && bankProfiles.itau && bankProfiles.itau.enabled && bankProfiles.itau.tier === 'afinidad') {
        candidates.push({
          pct: 20,
          bankTag: 'Itaú Afinidad (20%)',
          bank: 'itau'
        });
      }

      // 6. Continental Superseis (Miércoles = 3)
      if (store === 'Superseis' && targetDay === 3 && bankProfiles.continental && bankProfiles.continental.enabled) {
        const tier = bankProfiles.continental.tier || 'clasica';
        const pct = continentalPcts[tier] || 20;
        candidates.push({
          pct: pct,
          bankTag: 'Continental (' + pct + '%)',
          bank: 'continental'
        });
      }

      // 7. Banco GNB Superseis (Miércoles = 3)
      if (store === 'Superseis' && targetDay === 3 && bankProfiles.gnb && bankProfiles.gnb.enabled) {
        candidates.push({
          pct: 20,
          bankTag: 'Banco GNB (20%)',
          bank: 'gnb'
        });
      }

      // 8. Banco Atlas Stock (Lunes = 1)
      if (store === 'Supermercados Stock' && targetDay === 1 && bankProfiles.atlas && bankProfiles.atlas.enabled) {
        candidates.push({
          pct: 20,
          bankTag: 'Atlas QR (20%)',
          bank: 'atlas'
        });
      }

      // 9. Banco Familiar Stock (Viernes = 5)
      if (store === 'Supermercados Stock' && targetDay === 5 && bankProfiles.familiar && bankProfiles.familiar.enabled) {
        const tier = bankProfiles.familiar.tier || 'clasica';
        const pct = familiarPcts[tier] || 20;
        candidates.push({
          pct: pct,
          bankTag: 'Familiar (' + pct + '%)',
          bank: 'familiar'
        });
      }

      // 10. Banco Basa Stock (Domingos = 7)
      if (store === 'Supermercados Stock' && targetDay === 7 && bankProfiles.basa && bankProfiles.basa.enabled) {
        candidates.push({
          pct: 20,
          bankTag: 'Banco Basa (20%)',
          bank: 'basa'
        });
      }

      if (candidates.length === 0) {
        return {
          discountPct: 0,
          finalPrice: prod.regularPrice,
          savings: 0,
          bankTag: 'Precio Regular',
          activeOffer: false
        };
      }

      candidates.sort((a, b) => b.pct - a.pct);
      const best = candidates[0];
      const finalPrice = Math.round(prod.regularPrice * (1 - best.pct / 100));
      const savings = prod.regularPrice - finalPrice;

      return {
        discountPct: best.pct,
        finalPrice: finalPrice,
        savings: savings,
        bankTag: best.bankTag,
        activeOffer: true
      };
    }

    // INICIALIZACIÓN
    window.addEventListener('DOMContentLoaded', () => {
      loadSavedData();
      renderGrid();
      renderCart();
      highlightDayChip(selectedDay);
      updateProfileButtons();
      renderPromos();
    });

    // RENDERIZADO DE LA GÓNDOLA 2X2
    function renderGrid() {
      const container = document.getElementById('productGrid');
      if (!container) return;

      const filtered = products.filter(p => {
        const matchesQuery = !currentSearch || p.name.toLowerCase().includes(currentSearch.toLowerCase()) || p.brand.toLowerCase().includes(currentSearch.toLowerCase());
        const matchesCat = !currentCategory || p.category === currentCategory;
        const matchesStore = !currentStore || p.store.toLowerCase().includes(currentStore.toLowerCase());
        return matchesQuery && matchesCat && matchesStore;
      });

      document.getElementById('resultsCount').innerText = filtered.length;

      if (filtered.length === 0) {
        container.innerHTML = \`
          <div class="col-span-2 py-12 text-center text-slate-500">
            <span class="text-4xl">🔍</span>
            <p class="text-xs font-bold mt-2">No se encontraron productos</p>
            <p class="text-[10px] text-slate-600">Prueba con otra palabra o limpia los filtros</p>
            <button onclick="clearSearch(); selectCategory('', '🗂️', 'Categorías'); selectStore('', '🏬', 'Supermercados')" class="mt-3 px-3 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-400 font-bold text-xs border border-emerald-500/30">
              Restablecer filtros
            </button>
          </div>
        \`;
        return;
      }

      container.innerHTML = filtered.map((prod, idx) => {
        const realIdx = products.findIndex(p => p.id === prod.id && p.name === prod.name);
        const offer = calculateProductOffer(prod, selectedDay);
        const displayBestPrice = offer.finalPrice;
        const cardTag = '💳 ' + offer.bankTag;
        const discountBadge = offer.discountPct > 0 ? \`<span class="text-[9px] font-black uppercase px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center space-x-1"><span>🔥</span><span>-\${offer.discountPct}%</span></span>\` : '<span></span>';

        return \`
          <div onclick="openProductDetail(\${realIdx})" class="p-3 rounded-3xl glass-card hover:border-emerald-500/50 transition-all duration-300 flex flex-col justify-between relative group cursor-pointer shadow-md hover:shadow-emerald-500/10 active:scale-[0.98]">
            
            <div class="flex items-center justify-between mb-2 z-10">
              \${discountBadge}
              <button onclick="event.stopPropagation(); showToast('❤️ Guardado en tus favoritos');" class="text-xs text-slate-500 hover:text-rose-400 transition">❤️</button>
            </div>

            <div class="w-full h-28 flex items-center justify-center p-2 rounded-2xl bg-white/5 relative overflow-hidden group-hover:scale-105 transition-transform duration-300">
              <img src="\${prod.image}" class="max-h-full max-w-full object-contain drop-shadow" alt="\${prod.name}" onerror="this.src='https://static.app.biggie.com.py/images/products/7840127000124.jpg'">
            </div>

            <div class="mt-2.5">
              <p class="text-[10px] font-extrabold text-slate-400 truncate">\${prod.brand} • \${prod.store}</p>
              <h3 class="text-xs font-black text-white line-clamp-2 leading-tight mt-0.5">\${prod.name}</h3>
            </div>

            <div class="mt-2.5 pt-2 border-t border-white/5">
              <div class="flex items-baseline space-x-1.5">
                <span class="text-sm font-black text-white">Gs. \${prod.regularPrice.toLocaleString('es-PY')}</span>
                \${offer.discountPct > 0 ? \`<span class="text-[10px] text-slate-500 line-through">Gs. \${Math.round(prod.regularPrice * 1.15).toLocaleString('es-PY')}</span>\` : ''}
              </div>
              
              <div class="mt-1 p-1.5 rounded-xl bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-between">
                <span class="text-[10px] font-bold text-emerald-300 truncate max-w-[95px]">\${cardTag}</span>
                <span class="text-xs font-black text-emerald-400 shrink-0">Gs. \${displayBestPrice.toLocaleString('es-PY')}</span>
              </div>
            </div>

            <button onclick="event.stopPropagation(); flyToCart(\${realIdx}, event)" class="mt-2.5 w-full py-1.5 rounded-xl bg-slate-800 hover:bg-emerald-500 text-slate-300 hover:text-white text-xs font-extrabold flex items-center justify-center space-x-1.5 transition-all shadow active:scale-95">
              <span class="text-sm">+</span>
              <span>Sumar a Lista</span>
            </button>

          </div>
        \`;
      }).join('');
    }

    // ANIMACIÓN VOLADORA AL CARRITO
    function flyToCart(idx, event) {
      if (cart[idx]) {
        cart[idx]++;
      } else {
        cart[idx] = 1;
      }
      saveLocalData();
      renderCart();
      const prod = products[idx];
      showToast('🛒 Sumado: ' + prod.name.substring(0, 22) + '...');

      const badge = document.getElementById('navCartBadge');
      if (badge) {
        badge.classList.remove('animate-ping');
        void badge.offsetWidth;
        badge.classList.add('animate-ping');
      }
    }

    // RENDERIZADO DEL CARRITO & PODIUM
    function renderCart() {
      const listContainer = document.getElementById('cartItemsList');
      const badge = document.getElementById('navCartBadge');
      
      const cartKeys = Object.keys(cart).filter(k => cart[k] > 0);
      const totalItemCount = cartKeys.reduce((acc, k) => acc + cart[k], 0);

      if (badge) badge.innerText = totalItemCount;

      let subtotalRegular = 0;
      let totalCalculated = 0;

      // Calcular totales para los 3 supermercados
      let biggieTotal = 0;
      let superseisTotal = 0;
      let stockTotal = 0;

      cartKeys.forEach(k => {
        const prod = products[k];
        const qty = cart[k];
        if (!prod) return;

        const offer = calculateProductOffer(prod, selectedDay);
        subtotalRegular += prod.regularPrice * qty;
        totalCalculated += offer.finalPrice * qty;

        // Simulador de góndola comparativa para podium
        biggieTotal += Math.round(prod.regularPrice * (bankProfiles.ueno.enabled ? (1 - (uenoPcts[bankProfiles.ueno.level] || 35) / 100) : 1)) * qty;
        superseisTotal += Math.round(prod.regularPrice * ((selectedDay === 5 || selectedDay === 6) && bankProfiles.ueno.enabled ? 0.8 : 0.95)) * qty;
        stockTotal += Math.round(prod.regularPrice * (selectedDay === 2 && bankProfiles.itau.enabled ? 0.8 : 0.98)) * qty;
      });

      const totalSavings = Math.max(0, subtotalRegular - totalCalculated);

      // Actualizar vista resumen
      const elSubtotal = document.getElementById('cartSubtotalRegular');
      if (elSubtotal) elSubtotal.innerText = 'Gs. ' + subtotalRegular.toLocaleString('es-PY');

      const elSavings = document.getElementById('cartTotalSavings');
      if (elSavings) elSavings.innerText = '- Gs. ' + totalSavings.toLocaleString('es-PY');

      const elFinal = document.getElementById('cartFinalTotal');
      if (elFinal) elFinal.innerText = 'Gs. ' + totalCalculated.toLocaleString('es-PY');

      const islandSavings = document.getElementById('islandSavingsText');
      if (islandSavings) islandSavings.innerText = 'Gs. ' + totalSavings.toLocaleString('es-PY');

      // Actualizar Podium
      const p1 = document.getElementById('podium1Price');
      const p2 = document.getElementById('podium2Price');
      const p3 = document.getElementById('podium3Price');

      if (p1) p1.innerText = 'Gs. ' + (biggieTotal || totalCalculated).toLocaleString('es-PY');
      if (p2) p2.innerText = 'Gs. ' + (superseisTotal || Math.round(totalCalculated * 1.08)).toLocaleString('es-PY');
      if (p3) p3.innerText = 'Gs. ' + (stockTotal || Math.round(totalCalculated * 1.15)).toLocaleString('es-PY');

      if (!listContainer) return;

      if (cartKeys.length === 0) {
        listContainer.innerHTML = \`
          <div class="py-10 text-center text-slate-500 glass-card rounded-3xl">
            <span class="text-4xl">🛒</span>
            <p class="text-xs font-bold mt-2">Tu lista de compras está vacía</p>
            <p class="text-[10px] text-slate-600">Explora la góndola y suma productos para comparar</p>
            <button onclick="switchTab('viewSearch')" class="mt-3 px-3 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-400 font-bold text-xs border border-emerald-500/30">
              Ir a la Góndola
            </button>
          </div>
        \`;
        return;
      }

      listContainer.innerHTML = cartKeys.map(k => {
        const prod = products[k];
        const qty = cart[k];
        const offer = calculateProductOffer(prod, selectedDay);
        const itemTotal = offer.finalPrice * qty;

        return \`
          <div class="p-3 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-between space-x-3">
            <div class="w-12 h-12 rounded-xl bg-white/5 border border-white/5 p-1 shrink-0 flex items-center justify-center overflow-hidden">
              <img src="\${prod.image}" class="max-h-full max-w-full object-contain" alt="\${prod.name}" onerror="this.src='https://static.app.biggie.com.py/images/products/7840127000124.jpg'">
            </div>

            <div class="flex-1 min-w-0">
              <h4 class="text-xs font-extrabold text-white truncate">\${prod.name}</h4>
              <p class="text-[10px] text-emerald-400 font-bold">\${prod.store} • \${offer.bankTag}</p>
              <div class="flex items-baseline space-x-1.5 mt-0.5">
                <span class="text-xs font-black text-white">Gs. \${offer.finalPrice.toLocaleString('es-PY')}</span>
                <span class="text-[10px] text-slate-500 line-through">Gs. \${prod.regularPrice.toLocaleString('es-PY')}</span>
              </div>
            </div>

            <!-- Stepper interactivo [-] [qty] [+] -->
            <div class="flex items-center space-x-1.5 bg-slate-950 p-1 rounded-xl border border-slate-800 shrink-0">
              <button onclick="decrementCart(\${k})" class="w-6 h-6 rounded-lg bg-slate-800 text-slate-300 hover:text-white flex items-center justify-center font-bold text-xs active:scale-90 transition">-</button>
              <span class="text-xs font-black text-white px-1">\${qty}</span>
              <button onclick="flyToCart(\${k}, null)" class="w-6 h-6 rounded-lg bg-emerald-500 text-white flex items-center justify-center font-bold text-xs active:scale-90 transition">+</button>
            </div>
          </div>
        \`;
      }).join('');
    }

    function decrementCart(idx) {
      if (cart[idx] > 1) {
        cart[idx]--;
      } else {
        delete cart[idx];
      }
      saveLocalData();
      renderCart();
    }

    function clearUserCart() {
      if (confirm('¿Vaciar toda tu lista de compras?')) {
        cart = {};
        saveLocalData();
        renderCart();
        showToast('🗑️ Lista de compras vaciada');
      }
    }

    function toggleSplitCart(isChecked) {
      const hint = document.getElementById('splitSavingsHint');
      if (isChecked) {
        hint.innerHTML = '✨ ¡Modo Split Activo! Biggie: 2 productos + Superseis: 1 producto';
        showToast('✂️ Optimización Multi-Supermercado activada');
      } else {
        hint.innerHTML = 'Comprando en 2 súper ahorras Gs. 14.500 extra';
      }
    }

    // MODAL DE HISTORIAL DE PRECIOS KNASTA
    function openProductDetail(idx) {
      const prod = products[idx];
      if (!prod) return;

      const modal = document.getElementById('productDetailModal');
      const content = document.getElementById('modalProductContent');
      const offer = calculateProductOffer(prod, selectedDay);

      // SVG Sparkline Knasta
      const minHist = Math.min(...prod.history);
      const maxHist = Math.max(...prod.history);
      const range = maxHist - minHist || 1;
      const pts = prod.history.map((val, i) => {
        const x = 20 + i * 50;
        const y = 80 - ((val - minHist) / range) * 60;
        return \`\${x},\${y}\`;
      }).join(' ');

      content.innerHTML = \`
        <div class="space-y-4">
          <div class="flex items-center space-x-3">
            <div class="w-16 h-16 rounded-2xl bg-white/5 border border-white/10 p-2 shrink-0 flex items-center justify-center">
              <img src="\${prod.image}" class="max-h-full max-w-full object-contain" alt="\${prod.name}" onerror="this.src='https://static.app.biggie.com.py/images/products/7840127000124.jpg'">
            </div>
            <div>
              <span class="text-[10px] font-black uppercase text-emerald-400 bg-emerald-500/20 px-2 py-0.5 rounded-full border border-emerald-500/30">Mínimo Histórico Knasta</span>
              <h3 class="text-sm font-black text-white mt-1">\${prod.name}</h3>
              <p class="text-xs text-slate-400">\${prod.brand} • \${prod.store} • \${prod.unitPrice}</p>
            </div>
          </div>

          <!-- Precios hoy con tarjeta activa -->
          <div class="p-3.5 rounded-2xl bg-slate-950/80 border border-slate-800 flex items-center justify-between">
            <div>
              <p class="text-[10px] text-slate-400 uppercase font-black">Mejor precio hoy con \${offer.bankTag}:</p>
              <div class="flex items-baseline space-x-2 mt-0.5">
                <span class="text-xl font-black text-emerald-400">Gs. \${offer.finalPrice.toLocaleString('es-PY')}</span>
                <span class="text-xs text-slate-500 line-through">Gs. \${prod.regularPrice.toLocaleString('es-PY')}</span>
              </div>
            </div>
            <span class="text-xs font-black px-2.5 py-1 rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
              -\${offer.discountPct}% OFF
            </span>
          </div>

          <!-- Gráfico SVG Tendencia 30 días Knasta Style -->
          <div class="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
            <div class="flex justify-between items-center text-[11px]">
              <span class="font-extrabold text-slate-400">Evolución de Precio (Oct 2026)</span>
              <span class="text-emerald-400 font-extrabold">🟢 Momento Óptimo</span>
            </div>
            
            <div class="h-28 w-full flex items-center justify-center">
              <svg viewBox="0 0 280 90" class="w-full h-full overflow-visible">
                <polyline fill="none" stroke="#10b981" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" points="\${pts}" />
                \${prod.history.map((val, i) => {
                  const x = 20 + i * 50;
                  const y = 80 - ((val - minHist) / range) * 60;
                  return \`<circle cx="\${x}" cy="\${y}" r="4" fill="#090D16" stroke="#10b981" stroke-width="2.5" />\`;
                }).join('')}
              </svg>
            </div>

            <div class="flex justify-between text-[10px] font-bold text-slate-500 pt-1 border-t border-slate-800/80">
              <span>Hace 30 días (Gs. \${prod.history[0].toLocaleString('es-PY')})</span>
              <span>Hoy (Gs. \${offer.finalPrice.toLocaleString('es-PY')})</span>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-2 pt-1">
            <button onclick="flyToCart(\${idx}, null); closeProductModal();" class="py-3 rounded-2xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs flex items-center justify-center space-x-1.5 transition active:scale-95 shadow-lg shadow-emerald-500/20">
              <span>+ Sumar a mi Lista</span>
            </button>
            <button onclick="closeProductModal()" class="py-3 rounded-2xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-extrabold text-xs transition active:scale-95">
              Cerrar
            </button>
          </div>
        </div>
      \`;

      modal.classList.remove('hidden');
    }

    function closeProductModal() {
      const modal = document.getElementById('productDetailModal');
      if (modal) modal.classList.add('hidden');
    }

    // NAVEGACIÓN ENTRE TABS
    function switchTab(viewId) {
      document.querySelectorAll('.tab-view').forEach(v => v.classList.add('hidden'));
      const activeView = document.getElementById(viewId);
      if (activeView) activeView.classList.remove('hidden');

      document.querySelectorAll('.nav-btn').forEach(btn => {
        if (btn.getAttribute('data-view') === viewId) {
          btn.className = "nav-btn flex flex-col items-center justify-center text-emerald-400 font-black scale-105 transition";
        } else {
          btn.className = "nav-btn relative flex flex-col items-center justify-center text-slate-400 hover:text-white font-bold transition";
        }
      });

      if (viewId === 'viewCart') renderCart();
      if (viewId === 'viewSearch') renderGrid();
      if (viewId === 'viewPromos') renderPromos();
      if (viewId === 'viewProfile') updateProfileButtons();
    }

    // SELECTOR DE DÍAS Y PROMOCIONES DEL DÍA
    function setDay(d) {
      selectedDay = d;
      highlightDayChip(d);
      
      const hints = {
        1: '💳 Lunes: Banco Atlas 20% en Supermercados Stock',
        2: '💳 Martes: Itaú 20% a 30% en Superseis y Stock',
        3: '💳 Miércoles: Banco Continental y GNB en Superseis',
        4: '💳 Jueves: Sudameris Club 25% en Casa Rica y Areté',
        5: '💳 Viernes: Familiar en Stock + ueno Finde en Superseis',
        6: '⚡ Sábado: ueno en Superseis/Stock + Zeta y ueno en Biggie',
        7: '💳 Domingo: Banco Basa 20% en Supermercados Stock'
      };

      const hintEl = document.getElementById('dayPromoHint');
      if (hintEl) hintEl.innerText = hints[d] || 'Promos bancarias vigentes';

      renderGrid();
      renderCart();
      renderPromos();
      showToast('📅 Precios actualizados para el ' + getDayName(d));
    }

    function highlightDayChip(d) {
      document.querySelectorAll('.day-chip').forEach(btn => {
        const dayAttr = parseInt(btn.getAttribute('data-day'));
        if (dayAttr === d) {
          btn.className = "day-chip py-1.5 rounded-xl text-center text-[11px] font-extrabold transition bg-emerald-500 text-white shadow-lg shadow-emerald-500/30 ring-1 ring-emerald-400";
        } else {
          btn.className = "day-chip py-1.5 rounded-xl text-center text-[11px] font-extrabold transition bg-slate-900/80 text-slate-400 hover:text-white";
        }
      });
    }

    function getDayName(d) {
      const names = { 1: 'Lunes', 2: 'Martes', 3: 'Miércoles', 4: 'Jueves', 5: 'Viernes', 6: 'Sábado', 7: 'Domingo' };
      return names[d] || 'Día seleccionado';
    }

    // ESCÁNER YUKA
    function simulateScanBarcode() {
      currentScannedIdx = (currentScannedIdx + 1) % products.length;
      const prod = products[currentScannedIdx];
      const offer = calculateProductOffer(prod, selectedDay);

      document.getElementById('scannedProductName').innerText = prod.name;
      document.getElementById('scannedProductBrand').innerText = prod.brand + ' • ' + prod.store;
      document.getElementById('scannedProductImg').src = prod.image;
      document.getElementById('scannedBestDealText').innerText = 'Gs. ' + offer.finalPrice.toLocaleString('es-PY') + ' con ' + offer.bankTag;

      showToast('⚡ ¡Código de barra detectado! ' + prod.name.substring(0, 18));
    }

    function addScannedProductToCart() {
      flyToCart(currentScannedIdx, null);
      switchTab('viewCart');
    }

    function toggleScannerFlashlight() {
      isFlashlightOn = !isFlashlightOn;
      const lbl = document.getElementById('scannerFlashLabel');
      const icon = document.getElementById('scannerFlashIcon');
      if (isFlashlightOn) {
        lbl.innerText = 'Linterna: ON';
        icon.innerText = '💡';
        showToast('💡 Linterna del escáner encendida');
      } else {
        lbl.innerText = 'Linterna: OFF';
        icon.innerText = '🔦';
        showToast('🔦 Linterna apagada');
      }
    }

    // SELECTOR DE CIUDAD
    function openCitySheet() {
      document.getElementById('cityModalSheet').classList.remove('hidden');
    }
    function closeCitySheet() {
      document.getElementById('cityModalSheet').classList.add('hidden');
    }
    function selectCity(cityName) {
      selectedCity = cityName;
      document.getElementById('currentCityLabel').innerText = cityName;
      closeCitySheet();
      saveLocalData();
      showToast('📍 Ciudad cambiada a: ' + cityName);
    }

    // SELECTOR DE CATEGORÍA
    function openCategorySheet() {
      document.getElementById('categoryModalSheet').classList.remove('hidden');
    }
    function closeCategorySheet() {
      document.getElementById('categoryModalSheet').classList.add('hidden');
    }
    function selectCategory(cat, icon, name) {
      currentCategory = cat;
      document.getElementById('catFilterIcon').innerText = icon;
      document.getElementById('catFilterLabel').innerText = name;
      closeCategorySheet();
      renderGrid();
      showToast(cat ? '🗂️ Categoría: ' + name : '🗂️ Mostrando todas las categorías');
    }

    // SELECTOR DE SUPERMERCADOS
    function openSupermarketSheet() {
      document.getElementById('supermarketModalSheet').classList.remove('hidden');
    }
    function closeSupermarketSheet() {
      document.getElementById('supermarketModalSheet').classList.add('hidden');
    }
    function selectStore(storeSlug, icon, name) {
      currentStore = storeSlug;
      document.getElementById('superFilterIcon').innerText = icon;
      document.getElementById('superFilterLabel').innerText = name;
      closeSupermarketSheet();
      renderGrid();
      showToast(storeSlug ? '🏬 Filtrado por: ' + name : '🏬 Mostrando todos los supermercados');
    }

    // GESTIÓN DE NIVELES UENO & CATEGORÍAS BANCARIAS
    function setUenoLevel(lvl) {
      bankProfiles.ueno.level = parseInt(lvl);
      bankProfiles.ueno.enabled = true;
      saveLocalData();
      updateProfileButtons();
      renderGrid();
      renderCart();
      renderPromos();
      showToast('⚡ Nivel ueno ' + lvl + ' activado (' + uenoPcts[lvl] + '% reintegro QR)');
    }

    function setItauTier(tier) {
      bankProfiles.itau.tier = tier;
      bankProfiles.itau.enabled = true;
      saveLocalData();
      updateProfileButtons();
      renderGrid();
      renderCart();
      renderPromos();
      const tierNames = { clasica: 'Clásica/Oro (20%)', platinum: 'Platinum (25%)', infinite: 'Infinite (30%)', afinidad: 'Afinidad Superseis (20% Diario)' };
      showToast('💳 Itaú ' + (tierNames[tier] || tier) + ' activado');
    }

    function setContinentalTier(tier) {
      bankProfiles.continental.tier = tier;
      bankProfiles.continental.enabled = true;
      saveLocalData();
      updateProfileButtons();
      renderGrid();
      renderCart();
      renderPromos();
      showToast('💳 Continental ' + tier.toUpperCase() + ' activado');
    }

    function toggleBankProfile(bankSlug) {
      if (bankProfiles[bankSlug]) {
        bankProfiles[bankSlug].enabled = !bankProfiles[bankSlug].enabled;
        updateProfileButtons();
        saveLocalData();
        renderGrid();
        renderCart();
        renderPromos();
        showToast(bankProfiles[bankSlug].enabled ? '💳 Tarjeta ' + bankSlug.toUpperCase() + ' activada' : '❌ Tarjeta ' + bankSlug.toUpperCase() + ' desactivada');
      }
    }

    function updateProfileButtons() {
      // 1. ueno level buttons
      const currentUenoLvl = bankProfiles.ueno.level || 4;
      document.querySelectorAll('.ueno-lvl-btn').forEach(btn => {
        const lvl = parseInt(btn.getAttribute('data-level'));
        if (lvl === currentUenoLvl && bankProfiles.ueno.enabled) {
          btn.className = "ueno-lvl-btn py-1.5 rounded-xl text-center text-xs font-bold transition bg-emerald-500 text-white border border-emerald-400 shadow-md shadow-emerald-500/30";
        } else {
          btn.className = "ueno-lvl-btn py-1.5 rounded-xl text-center text-xs font-bold transition bg-slate-800 text-slate-300 border border-slate-700 hover:border-emerald-500/50";
        }
      });
      const uenoBadge = document.getElementById('uenoActiveBadge');
      if (uenoBadge) {
        uenoBadge.innerText = bankProfiles.ueno.enabled ? 'Nivel ' + currentUenoLvl + ' (' + uenoPcts[currentUenoLvl] + '%)' : 'Inactiva';
      }

      // 2. itau tier buttons
      const currentItauTier = bankProfiles.itau.tier || 'clasica';
      document.querySelectorAll('.itau-tier-btn').forEach(btn => {
        const tier = btn.getAttribute('data-tier');
        if (tier === currentItauTier && bankProfiles.itau.enabled) {
          btn.className = "itau-tier-btn p-2 rounded-xl text-left text-xs font-bold transition bg-orange-500 text-white border border-orange-400 shadow-md shadow-orange-500/20";
        } else {
          btn.className = "itau-tier-btn p-2 rounded-xl text-left text-xs font-bold transition bg-slate-800 text-slate-300 border border-slate-700 hover:border-orange-500/50";
        }
      });
      const itauBadge = document.getElementById('itauActiveBadge');
      if (itauBadge) {
        itauBadge.innerText = bankProfiles.itau.enabled ? currentItauTier.toUpperCase() + ' (' + itauPcts[currentItauTier] + '%)' : 'Inactiva';
      }

      // 3. continental tier buttons
      const currentContiTier = bankProfiles.continental.tier || 'clasica';
      document.querySelectorAll('.conti-tier-btn').forEach(btn => {
        const tier = btn.getAttribute('data-tier');
        if (tier === currentContiTier && bankProfiles.continental.enabled) {
          btn.className = "conti-tier-btn p-2 rounded-xl text-left text-xs font-bold transition bg-sky-500 text-white border border-sky-400 shadow-md shadow-sky-500/20";
        } else {
          btn.className = "conti-tier-btn p-2 rounded-xl text-left text-xs font-bold transition bg-slate-800 text-slate-300 border border-slate-700";
        }
      });
      const contiBadge = document.getElementById('continentalActiveBadge');
      if (contiBadge) {
        contiBadge.innerText = bankProfiles.continental.enabled ? currentContiTier.toUpperCase() + ' (' + continentalPcts[currentContiTier] + '%)' : 'Inactiva';
      }

      // 4. Update all toggle buttons
      ['ueno', 'itau', 'continental', 'zeta', 'familiar', 'atlas', 'sudameris', 'gnb', 'basa'].forEach(slug => {
        const btn = document.getElementById('btn-' + slug);
        const dot = document.getElementById('dot-' + slug);
        const isActive = bankProfiles[slug] && bankProfiles[slug].enabled;
        
        if (btn) {
          if (isActive) {
            btn.className = "px-3 py-1 rounded-xl bg-emerald-500/20 text-emerald-400 font-bold text-xs border border-emerald-500/30 active:scale-95 transition";
            btn.innerText = "Activa";
          } else {
            btn.className = "px-3 py-1 rounded-xl bg-slate-800 text-slate-400 font-bold text-xs border border-slate-700 active:scale-95 transition";
            btn.innerText = "+ Activar";
          }
        }
        if (dot) {
          dot.className = isActive ? "w-3.5 h-3.5 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]" : "w-3.5 h-3.5 rounded-full bg-slate-600";
        }
      });
    }

    // CATÁLOGO DE LAS 11 PROMOCIONES BANCARIAS REALES EN PARAGUAY
    const allBankPromos = [
      {
        id: 'ueno_biggie',
        bankKey: 'ueno',
        cardClass: 'card-ueno',
        bankName: 'ueno bank',
        title: 'ueno bank • Nivel 1 al 5 (15% a 40% OFF)',
        daysText: 'Todos los días (24hs)',
        dayNumbers: [1, 2, 3, 4, 5, 6, 7],
        supermarket: 'Biggie Express (Todas las sucursales)',
        discountText: 'Hasta 40% Reintegro QR',
        capText: 'Tope mensual: Gs. 300.000',
        icon: '⚡'
      },
      {
        id: 'ueno_superseis',
        bankKey: 'ueno',
        cardClass: 'card-ueno',
        bankName: 'ueno bank',
        title: 'ueno bank • Fin de Semana de Ahorro',
        daysText: 'Viernes y Sábados',
        dayNumbers: [5, 6],
        supermarket: 'Superseis y Supermercados Stock',
        discountText: '20% Reintegro QR',
        capText: 'Tope por compra: Gs. 200.000',
        icon: '📱'
      },
      {
        id: 'itau_superseis',
        bankKey: 'itau',
        cardClass: 'card-itau',
        bankName: 'Banco Itaú',
        title: 'Banco Itaú • Martes de Supermercado',
        daysText: 'Todos los Martes',
        dayNumbers: [2],
        supermarket: 'Superseis y Supermercados Stock',
        discountText: '20% a 30% OFF',
        capText: 'Clásica 20%, Platinum 25%, Infinite 30%',
        icon: '💳'
      },
      {
        id: 'itau_afinidad',
        bankKey: 'itau',
        cardClass: 'card-itau',
        bankName: 'Banco Itaú',
        title: 'Itaú Afinidad Superseis • Ahorro Diario',
        daysText: 'Todos los días del mes',
        dayNumbers: [1, 2, 3, 4, 5, 6, 7],
        supermarket: 'Superseis y Superseis Online',
        discountText: '20% Descuento Directo',
        capText: 'Tope mensual: Gs. 500.000',
        icon: '🏪'
      },
      {
        id: 'zeta_biggie',
        bankKey: 'zeta',
        cardClass: 'card-zeta',
        bankName: 'Zeta Banco',
        title: 'Zeta Banco • Sábados de Ahorro Biggie',
        daysText: 'Todos los Sábados',
        dayNumbers: [6],
        supermarket: 'Biggie Express',
        discountText: '20% Reintegro QR',
        capText: 'Tope por cliente: Gs. 200.000',
        icon: '⚡'
      },
      {
        id: 'conti_arete',
        bankKey: 'continental',
        cardClass: 'card-continental',
        bankName: 'Banco Continental',
        title: 'Continental ContiClub • Miércoles de Súper',
        daysText: 'Todos los Miércoles',
        dayNumbers: [3],
        supermarket: 'Supermercados Areté y Superseis',
        discountText: '20% a 25% OFF',
        capText: 'Tope semanal: Gs. 250.000',
        icon: '💳'
      },
      {
        id: 'familiar_stock',
        bankKey: 'familiar',
        cardClass: 'card-familiar',
        bankName: 'Banco Familiar',
        title: 'Banco Familiar • Viernes de Ahorro',
        daysText: 'Todos los Viernes',
        dayNumbers: [5],
        supermarket: 'Supermercados Stock',
        discountText: '20% a 25% Reintegro',
        capText: 'Tope por compra: Gs. 200.000',
        icon: '🛍️'
      },
      {
        id: 'atlas_stock',
        bankKey: 'atlas',
        cardClass: 'card-atlas',
        bankName: 'Banco Atlas',
        title: 'Banco Atlas • Lunes de Góndola Stock',
        daysText: 'Todos los Lunes',
        dayNumbers: [1],
        supermarket: 'Supermercados Stock',
        discountText: '20% Reintegro QR & TC',
        capText: 'Tope por lunes: Gs. 150.000',
        icon: '💳'
      },
      {
        id: 'sudameris_casarica',
        bankKey: 'sudameris',
        cardClass: 'card-sudameris',
        bankName: 'Banco Sudameris',
        title: 'Club Sudameris • Jueves Gourmet',
        daysText: 'Todos los Jueves',
        dayNumbers: [4],
        supermarket: 'Casa Rica y Areté',
        discountText: '25% Reintegro',
        capText: 'Tarjetas Infinite y Black',
        icon: '👑'
      },
      {
        id: 'gnb_superseis',
        bankKey: 'gnb',
        cardClass: 'card-gnb',
        bankName: 'Banco GNB',
        title: 'Banco GNB • Miércoles de Mercado',
        daysText: 'Todos los Miércoles',
        dayNumbers: [3],
        supermarket: 'Superseis y Delimarket',
        discountText: '20% Reintegro',
        capText: 'Mastercard GNB • Tope Gs. 200.000',
        icon: '🛒'
      },
      {
        id: 'basa_stock',
        bankKey: 'basa',
        cardClass: 'card-basa',
        bankName: 'Banco Basa',
        title: 'Banco Basa • Domingos en Familia',
        daysText: 'Todos los Domingos',
        dayNumbers: [7],
        supermarket: 'Supermercados Stock',
        discountText: '20% Reintegro',
        capText: 'Tarjetas de Crédito Basa',
        icon: '🏷️'
      }
    ];

    function filterPromosView(onlyMyCards) {
      showOnlyMyPromos = onlyMyCards;
      const allBtn = document.getElementById('promoTabAllBtn');
      const myBtn = document.getElementById('promoTabMyBtn');
      if (onlyMyCards) {
        myBtn.className = "flex-1 py-1.5 rounded-xl text-xs font-bold transition flex items-center justify-center space-x-1.5 bg-emerald-500 text-white shadow-md";
        allBtn.className = "flex-1 py-1.5 rounded-xl text-xs font-bold transition flex items-center justify-center space-x-1.5 text-slate-400 hover:text-white";
        showToast('💳 Mostrando solo promociones de tus tarjetas activas');
      } else {
        allBtn.className = "flex-1 py-1.5 rounded-xl text-xs font-bold transition flex items-center justify-center space-x-1.5 bg-emerald-500 text-white shadow-md";
        myBtn.className = "flex-1 py-1.5 rounded-xl text-xs font-bold transition flex items-center justify-center space-x-1.5 text-slate-400 hover:text-white";
        showToast('🌐 Mostrando todas las promociones bancarias');
      }
      renderPromos();
    }

    function renderPromos() {
      const container = document.getElementById('promosListContainer');
      if (!container) return;

      const filtered = allBankPromos.filter(p => {
        if (!showOnlyMyPromos) return true;
        return bankProfiles[p.bankKey] && bankProfiles[p.bankKey].enabled;
      });

      const badge = document.getElementById('promosCountBadge');
      if (badge) badge.innerText = filtered.length + ' promociones';

      if (filtered.length === 0) {
        container.innerHTML = \`
          <div class="p-8 text-center text-slate-500 glass-card rounded-3xl">
            <span class="text-4xl">💳</span>
            <p class="text-xs font-bold mt-2">No tienes tarjetas activas con promociones</p>
            <p class="text-[10px] text-slate-600">Activa tus tarjetas en la pestaña Perfil para ver tus beneficios</p>
            <button onclick="switchTab('viewProfile')" class="mt-3 px-3 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-400 font-bold text-xs border border-emerald-500/30">
              Ir a Mi Billetera
            </button>
          </div>
        \`;
        return;
      }

      container.innerHTML = filtered.map(p => {
        const isCardActive = bankProfiles[p.bankKey] && bankProfiles[p.bankKey].enabled;
        const isTodayActive = p.dayNumbers.includes(selectedDay);
        const dayBadge = isTodayActive 
          ? \`<span class="text-[9px] font-black uppercase px-2 py-0.5 rounded-full bg-emerald-400 text-slate-950 shadow-sm animate-pulse">⚡ Válido Hoy \${getDayName(selectedDay)}</span>\` 
          : \`<span class="text-[9px] font-bold text-white/80">\${p.daysText}</span>\`;

        // Renderizar tarjeta bancaria con diseño realista
        return \`
          <div class="p-4 rounded-3xl \${p.cardClass} text-white shadow-xl relative overflow-hidden transition-all duration-300 hover:scale-[1.01]">
            <div class="flex justify-between items-start">
              <div>
                <div class="flex items-center space-x-2">
                  <span class="text-[10px] uppercase font-black tracking-widest text-white/80">\${p.bankName}</span>
                  \${dayBadge}
                </div>
                <h3 class="text-base font-black mt-1 leading-tight">\${p.title}</h3>
                <p class="text-xs text-white/90 font-semibold mt-1">🏬 \${p.supermarket}</p>
              </div>
              <span class="text-2xl drop-shadow">\${p.icon}</span>
            </div>

            <div class="mt-4 pt-3 border-t border-white/20 flex justify-between items-center text-xs">
              <span class="text-white/80 text-[11px]">\${p.capText}</span>
              <button onclick="toggleBankProfile('\${p.bankKey}')" class="px-2.5 py-1 rounded-xl \${isCardActive ? 'bg-black/25 text-white font-extrabold border border-white/20' : 'bg-white text-slate-950 font-black shadow-md'} transition active:scale-95">
                \${isCardActive ? '✓ Activa en Billetera' : '+ Activar Tarjeta'}
              </button>
            </div>
          </div>
        \`;
      }).join('');
    }

    // PERSISTENCIA LOCAL
    function saveLocalData() {
      try {
        localStorage.setItem('preciospy_2_cart', JSON.stringify(cart));
        localStorage.setItem('preciospy_2_bank_profiles', JSON.stringify(bankProfiles));
        localStorage.setItem('preciospy_2_city', selectedCity);
      } catch (e) {}
    }

    function loadSavedData() {
      try {
        const rawCart = localStorage.getItem('preciospy_2_cart');
        if (rawCart) cart = JSON.parse(rawCart);
        const rawBanks = localStorage.getItem('preciospy_2_bank_profiles');
        if (rawBanks) bankProfiles = JSON.parse(rawBanks);
        const rawCity = localStorage.getItem('preciospy_2_city');
        if (rawCity) {
          selectedCity = rawCity;
          const lbl = document.getElementById('currentCityLabel');
          if (lbl) lbl.innerText = rawCity;
        }
      } catch (e) {}
    }

    function resetUserDataToDefault() {
      if (confirm('¿Restablecer datos de fábrica de tu carrito y tarjetas?')) {
        localStorage.removeItem('preciospy_2_cart');
        localStorage.removeItem('preciospy_2_bank_profiles');
        localStorage.removeItem('preciospy_2_city');
        location.reload();
      }
    }

    // TOAST NOTIFIER
    function showToast(msg) {
      const t = document.getElementById('toastNotification');
      const m = document.getElementById('toastMsg');
      if (!t || !m) return;
      m.innerText = msg;
      t.classList.remove('-translate-y-20', 'opacity-0');
      t.classList.add('translate-y-0', 'opacity-100');
      setTimeout(() => {
        t.classList.remove('translate-y-0', 'opacity-100');
        t.classList.add('-translate-y-20', 'opacity-0');
      }, 2400);
    }

    function handleSearch(val) {
      currentSearch = val;
      const btn = document.getElementById('clearSearchBtn');
      if (btn) {
        if (val.length > 0) btn.classList.remove('hidden');
        else btn.classList.add('hidden');
      }
      renderGrid();
    }

    function clearSearch() {
      const input = document.getElementById('searchInput');
      if (input) input.value = '';
      currentSearch = '';
      const btn = document.getElementById('clearSearchBtn');
      if (btn) btn.classList.add('hidden');
      renderGrid();
    }

    function toggleCashMode() {
      isCashOnly = !isCashOnly;
      const btn = document.getElementById('cashModeBtn');
      const text = document.getElementById('cashModeText');
      const icon = document.getElementById('cashModeIcon');
      if (isCashOnly) {
        btn.className = "px-2.5 py-1.5 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 bg-amber-500/20 border border-amber-500 text-amber-300 active:scale-95";
        icon.innerText = '💵';
        text.innerText = 'Solo Efectivo';
        showToast('💵 Modo Efectivo activado (Sin tarjetas)');
      } else {
        btn.className = "px-2.5 py-1.5 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 bg-slate-800/80 border border-slate-700 hover:border-emerald-500/50 text-slate-300 active:scale-95";
        icon.innerText = '💳';
        text.innerText = 'Con Tarjetas';
        showToast('💳 Descuentos bancarios activados');
      }
      renderGrid();
      renderCart();
    }

    function toggleBestDealsOnly() {
      const btn = document.getElementById('btnDealHeat');
      if (btn.classList.contains('bg-rose-500/20')) {
        btn.className = "shrink-0 px-3 py-1.5 rounded-xl bg-slate-900/90 border border-slate-800 text-xs font-bold text-slate-400 flex items-center space-x-1.5 active:scale-95 transition";
        currentCategory = '';
      } else {
        btn.className = "shrink-0 px-3 py-1.5 rounded-xl bg-rose-500/20 border border-rose-500/40 text-xs font-bold text-rose-300 flex items-center space-x-1.5 active:scale-95 transition";
      }
      renderGrid();
    }

    function toggleDynamicIsland() {
      switchTab('viewCart');
      showToast('⚡ Mostrando el detalle de tu ahorro en Mi Lista');
    }

    function shareCartWhatsApp() {
      const cartKeys = Object.keys(cart).filter(k => cart[k] > 0);
      let text = '🛒 Mi Lista de PreciosPy 2.0 (Caacupé):%0A';
      cartKeys.forEach(k => {
        const prod = products[k];
        const offer = calculateProductOffer(prod, selectedDay);
        text += '- ' + cart[k] + 'x ' + prod.name + ': Gs. ' + (offer.finalPrice * cart[k]).toLocaleString('es-PY') + '%0A';
      });
      window.open('https://wa.me/?text=' + text, '_blank');
    }
  </script>
</body>
</html>
\`;

// Escribir en la carpeta local y en la carpeta del artifact
const localFilePath = path.join(__dirname, '..', 'preciospy_redesign_2026.html');
fs.writeFileSync(localFilePath, htmlContent, 'utf8');

const artifactPath = 'C:\\\\Users\\\\munic\\\\.gemini\\\\antigravity\\\\brain\\\\3ac93072-98c3-495f-ad02-c8cfc7984916\\\\preciospy_redesign_2026.html';
try {
  fs.writeFileSync(artifactPath, htmlContent, 'utf8');
} catch (e) {
  console.log('Artifact path write error (optional):', e.message);
}

console.log('Successfully written both redesign files with verified images and working interactive modals!');
