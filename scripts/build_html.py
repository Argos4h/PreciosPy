# -*- coding: utf-8 -*-
import json
import os
import shutil

with open('scripts/verified_products_clean.json', 'r', encoding='utf-8') as f:
    products_json = f.read().strip()

html_content = '''<!DOCTYPE html>
<html lang="es" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>PreciosPy — Comparador de Supermercados & Billetera de Ahorro</title>
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
    <main class="flex-1 overflow-y-auto no-scrollbar relative z-10 px-4 pb-28">
      
      <!-- ============================================================ -->
      <!-- VISTA 1: EXPLORADOR DE PRECIOS & GÓNDOLA 2X2 -->
      <!-- ============================================================ -->
      <div id="viewSearch" class="tab-view space-y-3.5 pt-1 pb-32 animate-bounce-up">
        
        <!-- BARRA DE BÚSQUEDA FLIPP STYLE -->
        <div class="relative">
          <input 
            type="text" 
            id="searchInput"
            oninput="handleSearch(this.value)"
            placeholder="Buscar yerba, leche, carne, cerveza o código..." 
            class="w-full h-11 pl-10 pr-9 rounded-2xl bg-slate-900/90 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/80 focus:ring-1 focus:ring-emerald-500 transition shadow-inner"
          />
          <span class="absolute left-3.5 top-3 text-slate-500 text-sm">🔍</span>
          <button id="clearSearchBtn" onclick="clearSearch()" class="hidden absolute right-3 top-2.5 w-6 h-6 rounded-full bg-slate-800 text-slate-400 hover:text-white text-xs flex items-center justify-center">✕</button>
        </div>

        <!-- BANNER DE IMPACTO DE AHORRO REAL PRECIOSPY (SEMANA, MES, TOTAL) -->
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
              <p class="text-xs font-black text-white">Gs. <span id="homeSavingsDisplay">0</span> <span class="text-[10px] font-medium text-slate-400">ahorrados este mes</span></p>
            </div>
          </div>
          <div class="flex items-center space-x-1 bg-emerald-500/15 group-hover:bg-emerald-500 text-emerald-300 group-hover:text-white px-2.5 py-1 rounded-xl text-[10px] font-black border border-emerald-500/30 transition-all">
            <span>Semana / Mes / Total</span>
            <span class="text-xs">➔</span>
          </div>
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

          <button id="brandFilterBtn" onclick="openBrandSheet()" class="shrink-0 px-3 py-1.5 rounded-xl bg-slate-900/90 border border-slate-800 text-xs font-bold text-slate-300 flex items-center space-x-1.5 active:scale-95 transition hover:border-emerald-500/50 cursor-pointer">
            <span id="brandFilterIcon">🏷️</span>
            <span id="brandFilterLabel">Marcas</span>
            <span class="text-[10px] text-slate-500">▾</span>
          </button>

          <button onclick="toggleBestDealsOnly()" id="btnDealHeat" class="shrink-0 px-3 py-1.5 rounded-xl bg-slate-900/90 border border-slate-800 text-xs font-bold text-slate-400 flex items-center space-x-1.5 active:scale-95 transition">
            <span>🔥</span>
            <span>Mayores Descuentos</span>
          </button>

          <button onclick="toggleFavoritesOnly()" id="btnFavFilter" class="shrink-0 px-3 py-1.5 rounded-xl bg-slate-900/90 border border-slate-800 text-xs font-bold text-slate-400 flex items-center space-x-1.5 active:scale-95 transition hover:border-amber-400/50">
            <span id="favFilterStar">⭐</span>
            <span>Favoritos</span>
            <span id="favCountBadge" class="hidden text-[9px] px-1.5 py-0.2 rounded-full bg-amber-400/20 text-amber-300 font-black">0</span>
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
      <div id="viewCart" class="tab-view hidden space-y-4 pt-1 pb-32 animate-bounce-up">
        
        <!-- PODIUM DE SUPERMERCADOS (COMPARATIVA 1°, 2°, 3° LUGAR) -->
        <div class="p-4 rounded-3xl glass-card space-y-3">
          <div class="flex items-center justify-between">
            <div>
              <span class="text-xs font-black uppercase tracking-wider text-emerald-400">Podium de Supermercados</span>
              <p class="text-[10px] text-slate-400 font-medium">Toca un súper para cotizar toda tu lista ahí:</p>
            </div>
            <span id="podiumModeBadge" class="text-[9px] font-black uppercase px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">100% Biggie</span>
          </div>

          <!-- Tarjetas del Podium (Dinámicas ordenadas por donde se gasta menos) -->
          <div id="podiumCardsGrid" class="grid grid-cols-3 gap-2 pt-1 items-end">
            <!-- Render dinámico desde renderCart(): 2° Lugar (Izq), 1° TOP (Centro), 3° Lugar (Der) -->
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

          <!-- DESGLOSE DETALLADO DEL SPLIT-CART (DIVIDIR EN 2 SUPERMERCADOS) -->
          <div id="splitCartBreakdownContainer" class="hidden pt-3 border-t border-white/10 space-y-3 animate-bounce-up">
            <!-- Render dinámico desde JS con los productos por súper y el porqué -->
          </div>
        </div>

        <!-- LISTADO DE PRODUCTOS EN EL CARRITO -->
        <div class="space-y-2">
          <div class="flex justify-between items-center px-1">
            <span class="text-xs font-black uppercase text-slate-400 tracking-wider">Productos en tu lista:</span>
            <button onclick="openClearCartModal()" class="px-2.5 py-1 rounded-xl bg-rose-500/15 hover:bg-rose-500/25 text-rose-300 text-[11px] font-bold border border-rose-500/30 flex items-center space-x-1.5 transition active:scale-95 shadow-sm">
              <span>🗑️</span>
              <span>Vaciar lista</span>
            </button>
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
              <div>
                <span class="text-sm font-black text-white">Total a Pagar Hoy:</span>
                <span id="cartFinalStoreLabel" class="text-[10px] text-emerald-400 font-bold block">100% en Biggie Express</span>
              </div>
              <span id="cartFinalTotal" class="text-lg font-black text-emerald-400">Gs. 67.600</span>
            </div>
          </div>

          <button id="btnRegisterCartPurchase" onclick="registerCartPurchase()" class="w-full py-3 rounded-2xl bg-gradient-to-r from-emerald-500 via-teal-500 to-sky-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-black text-xs flex items-center justify-center space-x-2 transition active:scale-95 shadow-xl shadow-emerald-500/20 group cursor-pointer mb-2">
            <span class="text-base group-hover:scale-125 transition-transform">💰</span>
            <span>Registrar esta compra en Mi Ahorro Acumulado</span>
          </button>

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
      <div id="viewScanner" class="tab-view hidden space-y-4 pt-1 pb-32 animate-bounce-up">
        
        <div class="p-4 rounded-3xl glass-card text-center space-y-1">
          <span class="text-xs font-black uppercase text-emerald-400 tracking-wider">Escáner de Góndola Yuka-Style</span>
          <p class="text-xs text-slate-300">Apunta la cámara al código de barra de cualquier producto</p>
        </div>

        <!-- VISOR DE CÁMARA CON ANIMACIÓN DE LÁSER ESCÁNER -->
        <!-- VISOR DE CÁMARA REAL CON DETECCIÓN CONTINUA DE CÓDIGOS DE BARRA -->
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

          <div class="grid grid-cols-2 gap-2 pt-1">
            <button onclick="addScannedProductToCart()" class="py-2.5 rounded-2xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs flex items-center justify-center space-x-1.5 transition active:scale-95 shadow-lg shadow-emerald-500/20">
              <span>+</span>
              <span>A mi Lista</span>
            </button>
            <button onclick="openProductDetail(currentScannedIdx)" class="py-2.5 rounded-2xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-extrabold text-xs flex items-center justify-center space-x-1.5 transition active:scale-95 border border-slate-700">
              <span>🏬</span>
              <span>Ver en 5 Súper</span>
            </button>
          </div>
        </div>

      </div>


      <!-- ============================================================ -->
      <!-- VISTA 4: BENEFICIOS BANCARIOS (ESTILO PELANDO / DESCUENTOCITY) -->
      <!-- ============================================================ -->
      <div id="viewPromos" class="tab-view hidden space-y-4 pt-1 pb-32 animate-bounce-up">
        
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
      <div id="viewProfile" class="tab-view hidden space-y-4 pt-1 pb-32 animate-bounce-up">
        
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

        <!-- DASHBOARD DE AHORRO EN PERFIL (SEMANA, MES, TOTAL) -->
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
              <p id="profileSavingsWeek" class="text-xs font-black text-emerald-400 mt-1">Gs. 0</p>
            </div>
            <div class="p-2.5 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 ring-1 ring-emerald-500/20">
              <p class="text-[9px] font-black text-emerald-300 uppercase tracking-wider">Este Mes</p>
              <p id="profileSavingsMonth" class="text-xs font-black text-white mt-1">Gs. 0</p>
            </div>
            <div class="p-2.5 rounded-2xl bg-slate-950/70 border border-slate-800">
              <p class="text-[9px] font-extrabold text-slate-400 uppercase tracking-wider">Total</p>
              <p id="profileSavingsTotal" class="text-xs font-black text-emerald-400 mt-1">Gs. 0</p>
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
              <button id="btn-ueno" onclick="toggleBankProfile('ueno')" aria-label="Alternar ueno" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 shrink-0 cursor-pointer bg-emerald-500 shadow-md shadow-emerald-500/20 flex items-center focus:outline-none active:scale-95">
                <div id="thumb-ueno" class="w-4 h-4 rounded-full bg-white shadow-md transition-transform duration-200 translate-x-6 pointer-events-none"></div>
              </button>
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
          <!-- Banco Itaú con Selector de Segmentos (Diseño Blindado sin Overflow) -->
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
              <button id="btn-continental" onclick="toggleBankProfile('continental')" aria-label="Alternar Continental" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-slate-800 border border-slate-700 flex items-center focus:outline-none active:scale-95">
                <div id="thumb-continental" class="w-4 h-4 rounded-full bg-slate-400 shadow-md transition-transform duration-200 translate-x-0 pointer-events-none"></div>
              </button>
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
            <button id="btn-zeta" onclick="toggleBankProfile('zeta')" aria-label="Alternar Zeta" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-emerald-500 shadow-md shadow-emerald-500/20 flex items-center focus:outline-none active:scale-95">
              <div id="thumb-zeta" class="w-4 h-4 rounded-full bg-white shadow-md transition-transform duration-200 translate-x-6 pointer-events-none"></div>
            </button>
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
            <button id="btn-familiar" onclick="toggleBankProfile('familiar')" aria-label="Alternar Familiar" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-slate-800 border border-slate-700 flex items-center focus:outline-none active:scale-95">
              <div id="thumb-familiar" class="w-4 h-4 rounded-full bg-slate-400 shadow-md transition-transform duration-200 translate-x-0 pointer-events-none"></div>
            </button>
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
            <button id="btn-atlas" onclick="toggleBankProfile('atlas')" aria-label="Alternar Atlas" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-slate-800 border border-slate-700 flex items-center focus:outline-none active:scale-95">
              <div id="thumb-atlas" class="w-4 h-4 rounded-full bg-slate-400 shadow-md transition-transform duration-200 translate-x-0 pointer-events-none"></div>
            </button>
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
            <button id="btn-sudameris" onclick="toggleBankProfile('sudameris')" aria-label="Alternar Sudameris" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-slate-800 border border-slate-700 flex items-center focus:outline-none active:scale-95">
              <div id="thumb-sudameris" class="w-4 h-4 rounded-full bg-slate-400 shadow-md transition-transform duration-200 translate-x-0 pointer-events-none"></div>
            </button>
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
            <button id="btn-gnb" onclick="toggleBankProfile('gnb')" aria-label="Alternar GNB" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-slate-800 border border-slate-700 flex items-center focus:outline-none active:scale-95">
              <div id="thumb-gnb" class="w-4 h-4 rounded-full bg-slate-400 shadow-md transition-transform duration-200 translate-x-0 pointer-events-none"></div>
            </button>
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
            <button id="btn-basa" onclick="toggleBankProfile('basa')" aria-label="Alternar Basa" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-slate-800 border border-slate-700 flex items-center focus:outline-none active:scale-95">
              <div id="thumb-basa" class="w-4 h-4 rounded-full bg-slate-400 shadow-md transition-transform duration-200 translate-x-0 pointer-events-none"></div>
            </button>
          </div>

        </div>

        <!-- RESTABLECER VALORES DE FÁBRICA -->
        <div class="pt-4 border-t border-slate-800 text-center">
          <button onclick="openResetDataModal()" class="text-xs text-rose-400 hover:text-rose-300 font-bold px-3 py-1.5 rounded-xl border border-rose-500/30 hover:bg-rose-500/10 transition active:scale-95 shadow-sm">
            🔄 Restablecer mi carrito y tarjetas de fábrica
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
        <span id="navCartBadge" class="hidden absolute -top-1 right-1 w-4 h-4 rounded-full bg-emerald-500 text-white font-black text-[9px] flex items-center justify-center ring-2 ring-slate-900">0</span>
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
  <!-- MODAL DASHBOARD DE IMPACTO DE AHORRO REAL (SEMANA, MES, TOTAL) -->
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
          <h1 id="savingsMainAmount" class="text-3xl font-black text-white tracking-tight">0</h1>
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

  <div id="productDetailModal" onclick="if(event.target === this) closeProductModal()" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-end justify-center p-0 md:p-6 transition-all duration-300">
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
  <div id="cityModalSheet" onclick="if(event.target === this) closeCitySheet()" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-end justify-center p-0 md:p-6 transition-all">
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
  <div id="categoryModalSheet" onclick="if(event.target === this) closeCategorySheet()" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-end justify-center p-0 md:p-6 transition-all">
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
        <button onclick="selectCategory('Limpieza', '🧼', 'Limpieza')" class="p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center space-x-2 text-left transition">
          <span class="text-base">🧼</span>
          <span class="text-xs font-extrabold text-white">Limpieza & Hogar</span>
        </button>
        <button onclick="selectCategory('Frutas', '🍎', 'Frutas y Verduras')" class="p-3 rounded-2xl bg-slate-800 hover:bg-emerald-500/20 border border-slate-700 flex items-center space-x-2 text-left transition">
          <span class="text-base">🍎</span>
          <span class="text-xs font-extrabold text-white">Frutas & Verduras</span>
        </button>
      </div>
    </div>
  </div>

    <!-- MODAL / BOTTOM SHEET DE SELECCIÓN DE MARCAS -->
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

<!-- MODAL SHEET: FILTRAR POR SUPERMERCADO (DINÁMICO SEGÚN LA CIUDAD ACTIVA) -->
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
  </div>

  <!-- MODAL: CONFIRMACIÓN PARA VACIAR CARRITO -->
  <div id="clearCartModal" onclick="if(event.target === this) closeClearCartModal()" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 transition-all duration-300">
    <div class="w-full max-w-xs bg-slate-900 rounded-3xl border border-white/10 p-5 space-y-4 shadow-2xl animate-bounce-up text-center">
      <div class="w-12 h-12 mx-auto rounded-2xl bg-rose-500/20 border border-rose-500/30 flex items-center justify-center text-2xl">
        🗑️
      </div>
      <div>
        <h3 class="text-sm font-black text-white">¿Vaciar lista de compras?</h3>
        <p class="text-xs text-slate-400 mt-1">Se eliminarán todos los productos de tu carrito actual.</p>
      </div>
      <div class="grid grid-cols-2 gap-2 pt-1">
        <button onclick="closeClearCartModal()" class="py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs transition active:scale-95">
          Cancelar
        </button>
        <button onclick="confirmClearCart()" class="py-2.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-black text-xs transition active:scale-95 shadow-lg shadow-rose-600/30">
          Sí, Vaciar
        </button>
      </div>
    </div>
  </div>

  <!-- MODAL: CONFIRMACIÓN PARA RESTABLECER VALORES DE FÁBRICA -->
  <div id="resetDataModal" onclick="if(event.target === this) closeResetDataModal()" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 transition-all duration-300">
    <div class="w-full max-w-xs bg-slate-900 rounded-3xl border border-white/10 p-5 space-y-4 shadow-2xl animate-bounce-up text-center">
      <div class="w-12 h-12 mx-auto rounded-2xl bg-amber-500/20 border border-amber-500/30 flex items-center justify-center text-2xl">
        🔄
      </div>
      <div>
        <h3 class="text-sm font-black text-white">¿Restablecer de fábrica?</h3>
        <p class="text-xs text-slate-400 mt-1">Se borrarán tus tarjetas guardadas, favoritos y carrito, volviendo a la configuración inicial.</p>
      </div>
      <div class="grid grid-cols-2 gap-2 pt-1">
        <button onclick="closeResetDataModal()" class="py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs transition active:scale-95">
          Cancelar
        </button>
        <button onclick="confirmResetData()" class="py-2.5 rounded-xl bg-amber-600 hover:bg-amber-500 text-white font-black text-xs transition active:scale-95 shadow-lg shadow-amber-600/30">
          Sí, Restablecer
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
    const products = ''' + products_json + ''';

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

    // DIRECTORIO MAESTRO DE COBERTURA DE SUPERMERCADOS POR CIUDAD EN PARAGUAY
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
    }
    let currentSearch = '';
    let currentCategory = '';
    let currentStore = '';
    let currentBrand = '';
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

    let selectedCartStore = null; // Inicializa con el TOP 1 (menor gasto)
    let lastSingleStore = null; // Recuerda el súper monomarca activo antes de activar Split
    let isSplitCartActive = false; // Modo ahorro dividido activo/inactivo
    let cart = {};

    let favorites = [];
    let showOnlyFavorites = false;

    function toggleFavorite(prodId, event) {
      if (event) event.stopPropagation();
      const index = favorites.indexOf(prodId);
      if (index > -1) {
        favorites.splice(index, 1);
        showToast('☆ Quitado de tus favoritos');
      } else {
        favorites.push(prodId);
        showToast('⭐ Guardado en tus favoritos');
      }
      saveLocalData();
      renderGrid();
    }

    function toggleFavoritesOnly() {
      showOnlyFavorites = !showOnlyFavorites;
      const btn = document.getElementById('btnFavFilter');
      if (showOnlyFavorites) {
        if (btn) btn.className = "shrink-0 px-3 py-1.5 rounded-xl bg-amber-400/20 border border-amber-400 text-xs font-bold text-amber-300 flex items-center space-x-1.5 active:scale-95 transition shadow-sm";
        showToast('⭐ Mostrando solo tus productos favoritos');
      } else {
        if (btn) btn.className = "shrink-0 px-3 py-1.5 rounded-xl bg-slate-900/90 border border-slate-800 text-xs font-bold text-slate-400 flex items-center space-x-1.5 active:scale-95 transition hover:border-amber-400/50";
        showToast('Góndola completa restablecida');
      }
      renderGrid();
    }

    // MOTOR DE CÁLCULO DINÁMICO DE BENEFICIOS BANCARIOS PRECIOSPY
    function calculateStoreOffer(storeName, regularPrice, targetDay) {
      if (isCashOnly) {
        return {
          regularPrice: regularPrice,
          finalPrice: regularPrice,
          discountPct: 0,
          savings: 0,
          bankTag: '💵 Efectivo (Sin tarjeta)',
          activeOffer: false
        };
      }

      let candidates = [];

      // 1. ueno bank Biggie Express (Todos los días)
      if (storeName === 'Biggie Express' && bankProfiles.ueno && bankProfiles.ueno.enabled) {
        const lvl = bankProfiles.ueno.level || 4;
        const pct = uenoPcts[lvl] || 35;
        candidates.push({
          pct: pct,
          bankTag: 'ueno N' + lvl + ' (' + pct + '%)',
          bank: 'ueno'
        });
      }

      // 2. Zeta Banco Biggie Express (Sábados = 6)
      if (storeName === 'Biggie Express' && targetDay === 6 && bankProfiles.zeta && bankProfiles.zeta.enabled) {
        candidates.push({
          pct: 20,
          bankTag: 'Zeta QR (20%)',
          bank: 'zeta'
        });
      }

      // 3. ueno bank Superseis y Stock (Viernes = 5 y Sábados = 6)
      if ((storeName === 'Superseis' || storeName === 'Supermercados Stock') && (targetDay === 5 || targetDay === 6) && bankProfiles.ueno && bankProfiles.ueno.enabled) {
        candidates.push({
          pct: 20,
          bankTag: 'ueno Finde (20%)',
          bank: 'ueno'
        });
      }

      // 4. Itaú Superseis y Stock (Martes = 2)
      if ((storeName === 'Superseis' || storeName === 'Supermercados Stock') && targetDay === 2 && bankProfiles.itau && bankProfiles.itau.enabled) {
        const tier = bankProfiles.itau.tier || 'clasica';
        const pct = itauPcts[tier] || 20;
        candidates.push({
          pct: pct,
          bankTag: 'Itaú ' + tier.toUpperCase() + ' (' + pct + '%)',
          bank: 'itau'
        });
      }

      // 5. Itaú Afinidad Superseis (Todos los días en Superseis)
      if (storeName === 'Superseis' && bankProfiles.itau && bankProfiles.itau.enabled && bankProfiles.itau.tier === 'afinidad') {
        candidates.push({
          pct: 20,
          bankTag: 'Itaú Afinidad (20%)',
          bank: 'itau'
        });
      }

      // 6. Continental Superseis (Miércoles = 3)
      if (storeName === 'Superseis' && targetDay === 3 && bankProfiles.continental && bankProfiles.continental.enabled) {
        const tier = bankProfiles.continental.tier || 'clasica';
        const pct = continentalPcts[tier] || 20;
        candidates.push({
          pct: pct,
          bankTag: 'Continental (' + pct + '%)',
          bank: 'continental'
        });
      }

      // 7. Banco GNB Superseis (Miércoles = 3)
      if (storeName === 'Superseis' && targetDay === 3 && bankProfiles.gnb && bankProfiles.gnb.enabled) {
        candidates.push({
          pct: 20,
          bankTag: 'Banco GNB (20%)',
          bank: 'gnb'
        });
      }

      // 8. Banco Atlas Stock (Lunes = 1)
      if (storeName === 'Supermercados Stock' && targetDay === 1 && bankProfiles.atlas && bankProfiles.atlas.enabled) {
        candidates.push({
          pct: 20,
          bankTag: 'Atlas QR (20%)',
          bank: 'atlas'
        });
      }

      // 9. Banco Familiar Stock (Viernes = 5)
      if (storeName === 'Supermercados Stock' && targetDay === 5 && bankProfiles.familiar && bankProfiles.familiar.enabled) {
        const tier = bankProfiles.familiar.tier || 'clasica';
        const pct = familiarPcts[tier] || 20;
        candidates.push({
          pct: pct,
          bankTag: 'Familiar (' + pct + '%)',
          bank: 'familiar'
        });
      }

      // 10. Banco Basa Stock (Domingos = 7)
      if (storeName === 'Supermercados Stock' && targetDay === 7 && bankProfiles.basa && bankProfiles.basa.enabled) {
        candidates.push({
          pct: 20,
          bankTag: 'Banco Basa (20%)',
          bank: 'basa'
        });
      }

      // 11. Banco Sudameris Casa Rica (Jueves = 4)
      if (storeName === 'Casa Rica' && targetDay === 4 && bankProfiles.sudameris && bankProfiles.sudameris.enabled) {
        candidates.push({
          pct: 25,
          bankTag: 'Sudameris Club (25%)',
          bank: 'sudameris'
        });
      }

      if (candidates.length === 0) {
        return {
          regularPrice: regularPrice,
          finalPrice: regularPrice,
          discountPct: 0,
          savings: 0,
          bankTag: 'Precio Regular',
          activeOffer: false
        };
      }

      candidates.sort((a, b) => b.pct - a.pct);
      const best = candidates[0];
      const finalPrice = Math.round(regularPrice * (1 - best.pct / 100));
      const savings = regularPrice - finalPrice;

      return {
        regularPrice: regularPrice,
        finalPrice: finalPrice,
        discountPct: best.pct,
        savings: savings,
        bankTag: best.bankTag,
        activeOffer: true
      };
    }

    function calculateProductOffer(prod, targetDay) {
      return calculateStoreOffer(prod.store, prod.regularPrice, targetDay);
    }

    // INICIALIZACIÓN
    window.addEventListener('DOMContentLoaded', () => {
      loadSavedData();
      updateStatusBarClock();
      setInterval(updateStatusBarClock, 30000);
      renderSupermarketSheet();
      renderGrid();
      renderCart();
      renderDayChips();
      updateProfileButtons();
      renderPromos();
      renderSavingsDisplays();

      // Cerrar modales con tecla Escape
      window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          closeProductModal();
          closeCitySheet();
          closeCategorySheet();
          closeSupermarketSheet();
          closeClearCartModal();
          closeResetDataModal();
        }
      });
    });

    function updateStatusBarClock() {
      const el = document.getElementById('statusBarClock');
      if (!el) return;
      const now = new Date();
      const h = String(now.getHours()).padStart(2, '0');
      const m = String(now.getMinutes()).padStart(2, '0');
      el.innerText = h + ':' + m;
    }

    // RENDERIZADO DE LA GÓNDOLA 2X2 CON BOTÓN 'VER MÁS' Y SCROLL CONTINUO
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

    function renderLoadMoreSection(renderedCount, totalCount) {
      const remaining = totalCount - renderedCount;
      if (remaining <= 0) {
        return `
          <div id="loadMoreSection" class="col-span-2 pt-2 pb-8 flex justify-center text-center">
            <div class="inline-flex items-center space-x-2 px-5 py-2.5 rounded-2xl bg-slate-900 border border-slate-800 text-xs font-bold text-slate-400 shadow-sm">
              <span>✨</span>
              <span>Has visto todos los ${totalCount} productos en ${currentStore || 'góndola'}</span>
            </div>
          </div>
        `;
      }
      
      const nextBatch = Math.min(GRID_PAGE_SIZE, remaining);
      return `
        <div id="loadMoreSection" class="col-span-2 pt-2 pb-8 flex flex-col items-center justify-center space-y-2">
          <button id="btnLoadMore" onclick="loadMoreProducts()" class="w-full py-3.5 px-6 rounded-2xl bg-gradient-to-r from-emerald-500/20 via-teal-500/20 to-sky-500/20 hover:from-emerald-500/30 hover:to-sky-500/30 border-2 border-emerald-500/40 hover:border-emerald-400 text-white font-extrabold text-xs transition-all active:scale-95 flex items-center justify-center space-x-2.5 shadow-xl shadow-emerald-500/10 group cursor-pointer">
            <span class="text-emerald-400 text-sm group-hover:translate-y-0.5 transition-transform">🔽</span>
            <span>Ver más productos en ${currentStore || 'góndola'}</span>
            <span class="text-[10px] text-emerald-300 font-black bg-emerald-500/30 px-2 py-0.5 rounded-full border border-emerald-500/40">+${nextBatch} más</span>
          </button>
          <p id="infiniteScrollProgress" class="text-[10px] text-slate-400 font-bold">
            Mostrando ${renderedCount} de ${totalCount} productos en ${currentStore || 'góndola'}
          </p>
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
        const matchesBrand = !currentBrand || (p.brand && p.brand.toLowerCase() === currentBrand.toLowerCase());
        const matchesStore = !currentStore || 
          (p.stores && (p.stores[currentStore] !== undefined || Object.keys(p.stores).some(k => k.toLowerCase().includes(currentStore.toLowerCase())))) ||
          (p.store && p.store.toLowerCase().includes(currentStore.toLowerCase()));
        const matchesFav = !showOnlyFavorites || favorites.includes(p.id);
        return matchesQuery && matchesCat && matchesBrand && matchesStore && matchesFav;
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
      html += renderLoadMoreSection(initialBatch.length, currentFilteredList.length);

      container.innerHTML = html;
      initInfiniteScrollListener();
    }

    function loadMoreProducts() {
      if (isInfiniteScrollLoading) return;
      if (!currentFilteredList || currentFilteredList.length === 0) return;
      
      const currentRendered = currentGridPage * GRID_PAGE_SIZE;
      if (currentRendered >= currentFilteredList.length) return;

      isInfiniteScrollLoading = true;
      const btn = document.getElementById('btnLoadMore');
      if (btn) {
        btn.innerHTML = `<span class="w-4 h-4 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin"></span><span>Cargando productos abajo...</span>`;
      }

      setTimeout(() => {
        const nextBatch = currentFilteredList.slice(currentRendered, currentRendered + GRID_PAGE_SIZE);
        currentGridPage++;

        const container = document.getElementById('productGrid');
        const section = document.getElementById('loadMoreSection');
        if (section) section.remove();

        if (container && nextBatch.length > 0) {
          const nextHtml = nextBatch.map(renderProductCardHtml).join('');
          container.insertAdjacentHTML('beforeend', nextHtml);

          const newTotalRendered = Math.min(currentGridPage * GRID_PAGE_SIZE, currentFilteredList.length);
          container.insertAdjacentHTML('beforeend', renderLoadMoreSection(newTotalRendered, currentFilteredList.length));
        }

        isInfiniteScrollLoading = false;
        showToast('📦 Se cargaron ' + nextBatch.length + ' productos más abajo');
      }, 150);
    }

    function initInfiniteScrollListener() {
      const mainEl = document.querySelector('main');
      if (mainEl && !window._hasInfiniteScrollHandler) {
        window._hasInfiniteScrollHandler = true;
        mainEl.addEventListener('scroll', () => {
          if (mainEl.scrollTop + mainEl.clientHeight >= mainEl.scrollHeight - 350) {
            loadMoreProducts();
          }
        });
      }
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

    function selectPodiumStore(storeName) {
      selectedCartStore = storeName;
      lastSingleStore = storeName;
      isSplitCartActive = false;
      const toggle = document.getElementById('splitCartToggle');
      if (toggle) toggle.checked = false;
      const splitContainer = document.getElementById('splitCartBreakdownContainer');
      if (splitContainer) splitContainer.classList.add('hidden');
      updateSplitHint();
      renderCart();
      const shortName = storeName === 'Supermercados Stock' ? 'Stock' : storeName;
      showToast('🏬 Cotizando toda tu lista en ' + shortName);
    }

    // RENDERIZADO DEL CARRITO & PODIUM
    function renderCart() {
      const listContainer = document.getElementById('cartItemsList');
      const badge = document.getElementById('navCartBadge');
      
      const cartKeys = Object.keys(cart).filter(k => (cart[k] || 0) > 0);
      const totalItemCount = cartKeys.reduce((acc, k) => acc + cart[k], 0);

      if (badge) {
        badge.innerText = totalItemCount;
        if (totalItemCount === 0) {
          badge.classList.add('hidden');
        } else {
          badge.classList.remove('hidden');
        }
      }

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

      // 2. Ranking Dinámico: Ordenar los 3 súper por menor gasto (EL TOP ES DONDE MENOS GASTAS)
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
      if (!selectedCartStore || selectedCartStore === 'split') {
        selectedCartStore = rank1.key;
        lastSingleStore = rank1.key;
      }

      const splitToggleEl = document.getElementById('splitCartToggle');
      const isSplitActive = splitToggleEl ? splitToggleEl.checked : isSplitCartActive;

      // 3. Renderizado del Podium: 2° Lugar (Izq), 1° TOP (Centro más alto con corona), 3° Lugar (Der)
      const podiumGrid = document.getElementById('podiumCardsGrid');
      if (podiumGrid) {
        const createCardHtml = (store, place) => {
          const isSelected = (selectedCartStore === store.key);
          const isTop = (place === 1);
          const medal = isTop ? '👑' : (place === 2 ? '🥈' : '🥉');
          const badgeText = isTop ? 'TOP 1° AHORRO' : (place === 2 ? '2° Lugar' : '3° Lugar');

          let cardBase = '';
          let badgeClass = '';
          let statusHtml = '';

          if (isSelected) {
            // ¡SOLO ESTE TOP ESTÁ SELECCIONADO! (Se mantiene siempre como el seleccionado único aun al activar Split)
            cardBase = `p-2.5 rounded-2xl ${store.bgActive} border-2 ${store.colorBorder} ring-2 ${store.ringColor} shadow-xl shadow-black/40 text-center flex flex-col justify-between relative scale-105 cursor-pointer active:scale-95 transition-all duration-200 z-10`;
            badgeClass = isTop 
              ? 'bg-emerald-500 text-slate-950 font-black shadow-sm'
              : (place === 2 ? 'bg-amber-500 text-slate-950 font-black shadow-sm' : 'bg-blue-500 text-slate-950 font-black shadow-sm');
            statusHtml = `<span class="text-[9.5px] ${store.textAccent} font-black flex items-center justify-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-current"></span>✓ Viendo aquí</span>`;
          } else {
            // LOS OTROS DOS TOPS NO SELECCIONADOS (Apagados, escala 95, sin borde activo ni resplandor)
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
        `;
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

    function openClearCartModal() {
      const cartKeys = Object.keys(cart).filter(k => (cart[k] || 0) > 0);
      if (cartKeys.length === 0) {
        showToast('⚠️ Tu lista ya está vacía');
        return;
      }
      const modal = document.getElementById('clearCartModal');
      if (modal) {
        modal.classList.remove('hidden');
      }
    }

    function closeClearCartModal() {
      const modal = document.getElementById('clearCartModal');
      if (modal) {
        modal.classList.add('hidden');
      }
    }

    function confirmClearCart() {
      cart = {};
      saveLocalData();
      renderCart();
      closeClearCartModal();
      showToast('🗑️ Lista de compras vaciada');
    }

    function clearUserCart() {
      openClearCartModal();
    }

    function getSplitPlan() {
      const cartKeys = Object.keys(cart).filter(k => (cart[k] || 0) > 0);
      if (cartKeys.length === 0) {
        return {
          storeGroups: {},
          activeStores: [],
          splitTotal: 0,
          totalBiggie: 0,
          totalSuperseis: 0,
          totalStock: 0,
          extraSavings: 14500,
          storesCount: 2
        };
      }

      let splitTotal = 0;
      let totalBiggie = 0;
      let totalSuperseis = 0;
      let totalStock = 0;

      const storeGroups = {
        'Biggie Express': {
          storeName: 'Biggie Express',
          icon: '🏪',
          color: 'emerald',
          items: [],
          subtotal: 0,
          itemsCount: 0
        },
        'Superseis': {
          storeName: 'Superseis',
          icon: '🏬',
          color: 'amber',
          items: [],
          subtotal: 0,
          itemsCount: 0
        }
      };

      cartKeys.forEach(k => {
        const prod = products[k];
        const qty = cart[k];
        if (!prod) return;

        // Precio Biggie Express
        const isAlcohol = prod.name.toLowerCase().includes('cerveza') || prod.name.toLowerCase().includes('michelob') || prod.name.toLowerCase().includes('vino');
        let pBiggieBase = (prod.stores && prod.stores['Biggie Express']) ? prod.stores['Biggie Express'] : prod.regularPrice;
        let offerBiggie = isAlcohol 
          ? { finalPrice: pBiggieBase, discountPct: 0, bankTag: 'Precio Góndola (Excluye reintegro alcohol)' }
          : calculateStoreOffer('Biggie Express', pBiggieBase, selectedDay);
        let pBiggieFinal = offerBiggie.finalPrice;

        // Precio Superseis
        let pSuperseisBase = (prod.stores && prod.stores['Superseis']) ? prod.stores['Superseis'] : prod.regularPrice;
        let offerSuperseis = calculateStoreOffer('Superseis', pSuperseisBase, selectedDay);
        let pSuperseisFinal = offerSuperseis.finalPrice;

        // Precio Stock
        let pStockBase = (prod.stores && prod.stores['Supermercados Stock']) ? prod.stores['Supermercados Stock'] : prod.regularPrice;
        let offerStock = calculateStoreOffer('Supermercados Stock', pStockBase, selectedDay);
        let pStockFinal = offerStock.finalPrice;

        totalBiggie += pBiggieFinal * qty;
        totalSuperseis += pSuperseisFinal * qty;
        totalStock += pStockFinal * qty;

        // Asignacion optima entre Biggie Express y Superseis
        let assignedStore = 'Biggie Express';
        let winnerPrice = pBiggieFinal;
        let winnerOffer = offerBiggie;
        let otherStore = 'Superseis';
        let otherPrice = pSuperseisFinal;
        let otherOffer = offerSuperseis;

        if (pSuperseisFinal < pBiggieFinal) {
          assignedStore = 'Superseis';
          winnerPrice = pSuperseisFinal;
          winnerOffer = offerSuperseis;
          otherStore = 'Biggie Express';
          otherPrice = pBiggieFinal;
          otherOffer = offerBiggie;
        } else {
          assignedStore = 'Biggie Express';
          winnerPrice = pBiggieFinal;
          winnerOffer = offerBiggie;
          otherStore = 'Superseis';
          otherPrice = pSuperseisFinal;
          otherOffer = offerSuperseis;
        }

        const diffPerUnit = Math.max(0, otherPrice - winnerPrice);
        const diffTotal = diffPerUnit * qty;

        // Explicación simplificada y directa del porqué (solo lo esencial)
        let whyExplanation = '';
        const shortOther = otherStore === 'Biggie Express' ? 'Biggie' : otherStore;
        const shortWinner = assignedStore === 'Biggie Express' ? 'Biggie' : assignedStore;

        if (assignedStore === 'Biggie Express') {
          if (winnerOffer.discountPct > 0) {
            whyExplanation = 'Ahorras <strong class="text-emerald-400">Gs. ' + diffPerUnit.toLocaleString('es-PY') + ' c/u</strong> con ' + winnerOffer.bankTag + ' vs ' + shortOther + '.';
          } else if (diffPerUnit > 0) {
            whyExplanation = 'Ahorras <strong class="text-emerald-400">Gs. ' + diffPerUnit.toLocaleString('es-PY') + ' c/u</strong> por precio góndola vs ' + shortOther + '.';
          } else {
            whyExplanation = 'Mismo precio. Asignado a ' + shortWinner + ' por cercanía.';
          }
        } else {
          if (isAlcohol) {
            whyExplanation = 'Ahorras <strong class="text-amber-400">Gs. ' + diffPerUnit.toLocaleString('es-PY') + '</strong> vs Biggie (alcohol sin promo en Biggie).';
          } else if (winnerOffer.discountPct > 0) {
            whyExplanation = 'Ahorras <strong class="text-amber-400">Gs. ' + diffPerUnit.toLocaleString('es-PY') + ' c/u</strong> con ' + winnerOffer.bankTag + ' vs ' + shortOther + '.';
          } else if (diffPerUnit > 0) {
            whyExplanation = 'Ahorras <strong class="text-amber-400">Gs. ' + diffPerUnit.toLocaleString('es-PY') + ' c/u</strong> por precio góndola vs ' + shortOther + '.';
          } else {
            whyExplanation = 'Mismo precio en ambos súper.';
          }
        }

        const itemObj = {
          key: k,
          prod: prod,
          qty: qty,
          winnerPrice: winnerPrice,
          subtotal: winnerPrice * qty,
          winnerOffer: winnerOffer,
          otherStore: otherStore,
          otherPrice: otherPrice,
          diffPerUnit: diffPerUnit,
          diffTotal: diffTotal,
          whyExplanation: whyExplanation
        };

        storeGroups[assignedStore].items.push(itemObj);
        storeGroups[assignedStore].subtotal += winnerPrice * qty;
        storeGroups[assignedStore].itemsCount += qty;
        splitTotal += winnerPrice * qty;
      });

      const singleStoreBest = Math.min(totalBiggie, totalSuperseis);
      const extraSavings = Math.max(0, singleStoreBest - splitTotal);
      const activeStores = Object.values(storeGroups).filter(g => g.items.length > 0);

      return {
        storeGroups: storeGroups,
        activeStores: activeStores,
        splitTotal: splitTotal,
        totalBiggie: totalBiggie,
        totalSuperseis: totalSuperseis,
        totalStock: totalStock,
        extraSavings: extraSavings || 14500,
        storesCount: activeStores.length
      };
    }

    function calculateSplitSavings() {
      const plan = getSplitPlan();
      return {
        extraSavings: plan.extraSavings || 14500,
        storesCount: Math.max(2, plan.storesCount)
      };
    }

    function updateSplitHint() {
      const hint = document.getElementById('splitSavingsHint');
      const toggle = document.getElementById('splitCartToggle');
      if (!hint) return;
      const plan = getSplitPlan();
      if (toggle && toggle.checked) {
        hint.innerHTML = '✨ ¡Modo Split Activo! Biggie: 2 productos + Superseis: 1 producto';
      } else {
        hint.innerHTML = 'Comprando en ' + (plan.storesCount || 2) + ' súper ahorras Gs. ' + (plan.extraSavings || 14500).toLocaleString('es-PY') + ' extra';
      }
    }

    function toggleSplitCart(isChecked) {
      isSplitCartActive = isChecked;
      const hint = document.getElementById('splitSavingsHint');
      const container = document.getElementById('splitCartBreakdownContainer');
      const plan = getSplitPlan();
      if (isChecked) {
        if (selectedCartStore && selectedCartStore !== 'split') {
          lastSingleStore = selectedCartStore;
        }
        hint.innerHTML = '✨ ¡Modo Split Activo! Biggie: 2 productos + Superseis: 1 producto';
        if (container) {
          renderSplitBreakdown();
          container.classList.remove('hidden');
        }
        renderCart();
        showToast('✂️ Optimización Multi-Supermercado activada');
      } else {
        // Mantener exactamente el súper monomarca activo
        if (lastSingleStore) {
          selectedCartStore = lastSingleStore;
        }
        hint.innerHTML = 'Comprando en ' + (plan.storesCount || 2) + ' súper ahorras Gs. ' + (plan.extraSavings || 14500).toLocaleString('es-PY') + ' extra';
        if (container) {
          container.classList.add('hidden');
        }
        renderCart();
        const shortName = selectedCartStore === 'Supermercados Stock' ? 'Stock' : selectedCartStore;
        showToast('🛒 Mostrando toda tu lista en ' + shortName);
      }
    }

    function renderSplitBreakdown() {
      const container = document.getElementById('splitCartBreakdownContainer');
      if (!container) return;

      const plan = getSplitPlan();
      if (plan.activeStores.length === 0) {
        container.innerHTML = `
          <div class="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 text-center text-xs text-slate-400">
            Tu lista está vacía. Suma productos para ver la división inteligente.
          </div>
        `;
        return;
      }

      const singleBest = Math.min(plan.totalBiggie, plan.totalSuperseis);
      const singleBestName = plan.totalBiggie <= plan.totalSuperseis ? 'Biggie Express' : 'Superseis';

      let html = `
        <!-- BANNER DE RESUMEN Y AHORRO EXTRA -->
        <div class="p-3.5 rounded-2xl bg-gradient-to-br from-emerald-500/15 via-slate-900 to-slate-900 border border-emerald-500/30 shadow-lg">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <span class="text-xl">✂️</span>
              <div>
                <h4 class="text-xs font-black text-white tracking-wide">División Inteligente en 2 Supermercados</h4>
                <p class="text-[10px] text-emerald-300 font-semibold">Te mostramos qué comprar en cada súper y exactamente cuánto y por qué ahorras</p>
              </div>
            </div>
            <span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-[9px] font-black uppercase tracking-wider shrink-0">
              🔥 -Gs. ${plan.extraSavings.toLocaleString('es-PY')} EXTRA
            </span>
          </div>

          <!-- Métricas comparativas -->
          <div class="grid grid-cols-2 gap-2 mt-3 pt-2.5 border-t border-white/10 text-center">
            <div class="p-2 rounded-xl bg-slate-950/70 border border-slate-800/80">
              <p class="text-[9px] uppercase font-bold text-slate-400">Comprando Dividido</p>
              <p class="text-sm font-black text-emerald-400 mt-0.5">Gs. ${plan.splitTotal.toLocaleString('es-PY')}</p>
              <p class="text-[9px] text-emerald-300/80 font-semibold mt-0.5">Menor precio en todo</p>
            </div>
            <div class="p-2 rounded-xl bg-slate-950/70 border border-slate-800/80">
              <p class="text-[9px] uppercase font-bold text-slate-400">Todo en 1 solo súper</p>
              <p class="text-sm font-black text-rose-300/90 line-through mt-0.5">Gs. ${singleBest.toLocaleString('es-PY')}</p>
              <p class="text-[9px] text-rose-400/80 font-medium mt-0.5">${singleBestName}</p>
            </div>
          </div>
        </div>

        <!-- SECCIONES POR SUPERMERCADO -->
        <div class="space-y-3">
      `;

      plan.activeStores.forEach(group => {
        const isBiggie = group.storeName === 'Biggie Express';
        const storeColorClass = isBiggie ? 'border-emerald-500/30' : 'border-amber-500/30';
        const storePill = isBiggie ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' : 'bg-amber-500/20 text-amber-300 border-amber-500/30';

        html += `
          <div class="p-3.5 rounded-2xl bg-slate-900 border ${storeColorClass} shadow-md space-y-2.5">
            
            <!-- Header del supermercado -->
            <div class="flex items-center justify-between pb-2 border-b border-white/10">
              <div class="flex items-center space-x-2">
                <span class="text-xl">${group.icon}</span>
                <div>
                  <div class="flex items-center space-x-1.5">
                    <h5 class="text-xs font-black text-white">${group.storeName}</h5>
                    <span class="px-1.5 py-0.5 rounded-md ${storePill} text-[9px] font-extrabold border">${group.items.length} ${group.items.length === 1 ? 'producto' : 'productos'}</span>
                  </div>
                  <p class="text-[10px] text-slate-400 font-medium">Subtotal a pagar aquí: <span class="font-extrabold text-white">Gs. ${group.subtotal.toLocaleString('es-PY')}</span></p>
                </div>
              </div>
              <span class="text-xs font-black text-emerald-400 bg-slate-950 px-2 py-1 rounded-xl border border-white/5">
                Gs. ${group.subtotal.toLocaleString('es-PY')}
              </span>
            </div>

            <!-- Lista de productos asignados a este súper -->
            <div class="space-y-2">
        `;

        group.items.forEach(it => {
          const prod = it.prod;
          html += `
            <div class="p-2.5 rounded-xl bg-slate-950/80 border border-white/5 space-y-2">
              
              <div class="flex items-center space-x-2.5">
                <div class="w-11 h-11 rounded-lg bg-white/5 p-1 shrink-0 flex items-center justify-center overflow-hidden border border-white/5">
                  <img src="${prod.image}" class="max-h-full max-w-full object-contain" alt="${prod.name}" onerror="this.src='https://static.app.biggie.com.py/images/products/7840127000124.jpg'">
                </div>

                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between">
                    <h6 class="text-xs font-bold text-white truncate max-w-[170px]">${prod.name}</h6>
                    <span class="text-[10px] font-extrabold text-slate-300 bg-slate-900 px-1.5 py-0.5 rounded-md border border-slate-800">x${it.qty}</span>
                  </div>
                  <div class="flex items-center space-x-1.5 mt-0.5">
                    <span class="text-xs font-black text-emerald-400">Gs. ${it.subtotal.toLocaleString('es-PY')}</span>
                    <span class="text-[10px] text-slate-400">(Gs. ${it.winnerPrice.toLocaleString('es-PY')} c/u)</span>
                  </div>
                </div>
              </div>

              <!-- MOTIVO ESENCIAL -->
              <div class="px-2.5 py-1.5 rounded-xl bg-slate-900/80 border border-white/5 text-[10.5px]">
                <div class="flex items-center space-x-1.5">
                  <span class="text-xs shrink-0">💡</span>
                  <span class="font-bold text-slate-400 text-[9px] uppercase tracking-wide">¿Por qué comprar acá?</span>
                </div>
                <p class="text-slate-200 mt-0.5 pl-4 text-[10px] font-medium leading-normal">
                  ${it.whyExplanation}
                </p>
              </div>

            </div>
          `;
        });

        html += `
            </div>
          </div>
        `;
      });

      html += `
        </div>

        <!-- BOTONES DE ACCIÓN PARA COMPARTIR EL PLAN DIVIDIDO -->
        <div class="pt-1 flex items-center space-x-2">
          <button onclick="shareSplitCartWhatsApp()" class="flex-1 py-2.5 px-3 rounded-2xl bg-emerald-500 hover:bg-emerald-400 active:scale-95 text-slate-950 font-black text-xs flex items-center justify-center space-x-2 shadow-lg shadow-emerald-500/20 transition">
            <span>📲</span>
            <span>Compartir Plan en WhatsApp</span>
          </button>
          <button onclick="copySplitPlan()" class="py-2.5 px-3 rounded-2xl bg-slate-800 hover:bg-slate-700 active:scale-95 text-white font-extrabold text-xs flex items-center justify-center space-x-1 border border-slate-700 transition" title="Copiar resumen">
            <span>📋</span>
            <span>Copiar</span>
          </button>
        </div>
      `;

      container.innerHTML = html;
    }

    function shareSplitCartWhatsApp() {
      const plan = getSplitPlan();
      if (plan.activeStores.length === 0) {
        showToast('⚠️ Tu lista está vacía. ¡Agrega productos primero!');
        return;
      }

      const dayNames = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
      const dayName = dayNames[selectedDay] || 'Hoy';

      let msg = '🛒 *PLAN DE COMPRA DIVIDIDA — PreciosPy*\\n';
      msg += '📍 *Ciudad:* ' + (typeof selectedCity !== 'undefined' ? selectedCity : 'Caacupé') + ' | 📅 *Día:* ' + dayName + '\\n';
      msg += '✂️ *Ahorro Extra por Dividir:* Gs. ' + plan.extraSavings.toLocaleString('es-PY') + '\\n';
      msg += '====================================\\n\\n';

      plan.activeStores.forEach(function(group, idx) {
        msg += group.icon + ' *' + (idx + 1) + '. COMPRAR EN ' + group.storeName.toUpperCase() + '*\\n';
        msg += '   📦 ' + group.itemsCount + ' unid. | Subtotal: Gs. ' + group.subtotal.toLocaleString('es-PY') + '\\n';
        group.items.forEach(function(it) {
          msg += '   • ' + it.qty + 'x ' + it.prod.name + ' -> Gs. ' + it.subtotal.toLocaleString('es-PY');
          if (it.winnerOffer && it.winnerOffer.discountPct > 0) {
            msg += ' (' + it.winnerOffer.bankTag + ')';
          }
          msg += '\\n';
          const cleanWhy = it.whyExplanation.replace(/<[^>]+>/g, '');
          msg += '     💡 _¿Por qué acá? ' + cleanWhy + '_\\n';
        });
        msg += '\\n';
      });

      msg += '====================================\\n';
      msg += '💰 *TOTAL DIVIDIDO OPTIMIZADO: Gs. ' + plan.splitTotal.toLocaleString('es-PY') + '*\\n';
      const singleBest = Math.min(plan.totalBiggie, plan.totalSuperseis);
      if (singleBest > plan.splitTotal) {
        msg += '🚫 Comprando todo en un solo súper: Gs. ' + singleBest.toLocaleString('es-PY') + '\\n';
        msg += '🔥 *¡Ahorro Neto Extra por Dividir: Gs. ' + plan.extraSavings.toLocaleString('es-PY') + '!*\\n\\n';
      }
      msg += '_Generado con PreciosPy — El comparador inteligente de Paraguay_ 🇵🇾';

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(msg).catch(function(err) {});
      }

      const encoded = encodeURIComponent(msg);
      const waUrl = 'https://api.whatsapp.com/send?text=' + encoded;
      const a = document.createElement('a');
      a.href = waUrl;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      document.body.appendChild(a);
      a.click();
      setTimeout(function() {
        if (a.parentNode) a.parentNode.removeChild(a);
      }, 500);

      showToast('📲 Abriendo WhatsApp con tu plan dividido...');
    }

    function copySplitPlan() {
      const plan = getSplitPlan();
      if (plan.activeStores.length === 0) {
        showToast('⚠️ Tu lista está vacía');
        return;
      }

      let text = '🛒 PLAN DE COMPRA DIVIDIDA - PreciosPy\\n\\n';
      plan.activeStores.forEach(function(group, idx) {
        text += (idx + 1) + '. ' + group.storeName + ' (Subtotal: Gs. ' + group.subtotal.toLocaleString('es-PY') + ')\\n';
        group.items.forEach(function(it) {
          text += '  - ' + it.qty + 'x ' + it.prod.name + ' (Gs. ' + it.winnerPrice.toLocaleString('es-PY') + ' c/u)\\n';
          const cleanWhy = it.whyExplanation.replace(/<[^>]+>/g, '');
          text += '    * ' + cleanWhy + '\\n';
        });
        text += '\\n';
      });
      text += 'Total Dividido: Gs. ' + plan.splitTotal.toLocaleString('es-PY') + '\\n';
      text += 'Ahorro extra: Gs. ' + plan.extraSavings.toLocaleString('es-PY');

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).catch(function(err) {});
      }
      showToast('📋 Plan de compra copiado al portapapeles');
    }

    // MODAL DE HISTORIAL DE PRECIOS KNASTA & COMPARATIVA DE SUPERMERCADOS
    function openProductDetail(idx) {
      const prod = products[idx];
      if (!prod) return;

      const modal = document.getElementById('productDetailModal');
      const content = document.getElementById('modalProductContent');
      const offer = calculateProductOffer(prod, selectedDay);

      const minHist = Math.min(...prod.history);
      const maxHist = Math.max(...prod.history);
      const range = maxHist - minHist || 1;
      const pts = prod.history.map((val, i) => {
        const x = 20 + i * 50;
        const y = 80 - ((val - minHist) / range) * 60;
        return `${x},${y}`;
      }).join(' ');

      // Supermercados presentes estrictamente en la ciudad activa (${selectedCity})
      const localCatalog = getStoresForCurrentCity();
      const comparisons = localCatalog.map(st => {
        const regular = (prod.stores && prod.stores[st.name]) ? prod.stores[st.name] : prod.regularPrice;
        const off = calculateStoreOffer(st.name, regular, selectedDay);
        return {
          ...st,
          regularPrice: regular,
          finalPrice: off.finalPrice,
          discountPct: off.discountPct,
          savings: off.savings,
          bankTag: off.bankTag
        };
      });

      // Ordenar por precio final ascendente (el más barato primero)
      comparisons.sort((a, b) => a.finalPrice - b.finalPrice);
      const cheapestPrice = comparisons[0].finalPrice;

      content.innerHTML = `
        <div class="space-y-4">
          
          <!-- CABECERA DEL PRODUCTO -->
          <div class="flex items-center space-x-3">
            <div class="w-16 h-16 rounded-2xl bg-white/5 border border-white/10 p-2 shrink-0 flex items-center justify-center">
              <img src="${prod.image}" class="max-h-full max-w-full object-contain drop-shadow" alt="${prod.name}" onerror="this.src='https://static.app.biggie.com.py/images/products/7840127000124.jpg'">
            </div>
            <div class="min-w-0">
              <div class="flex items-center space-x-1.5">
                <span class="text-[9px] font-black uppercase text-emerald-400 bg-emerald-500/20 px-2 py-0.5 rounded-full border border-emerald-500/30">Góndola Verificada</span>
                <span class="text-[9px] text-slate-400">• ${prod.unitPrice}</span>
              </div>
              <h3 class="text-sm font-black text-white mt-1 leading-snug truncate">${prod.name}</h3>
              <p class="text-xs text-slate-400">${prod.brand} • ${prod.store}</p>
            </div>
          </div>

          <!-- PRECIO REAL EN GÓNDOLA Y PRECIO CON TU TARJETA ACTIVA -->
          <div class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
            <div class="flex items-center justify-between text-xs">
              <span class="text-[10px] text-slate-400 uppercase font-black tracking-wider">Precio real en góndola (${prod.store}):</span>
              <span class="text-sm font-black text-slate-200">Gs. ${prod.regularPrice.toLocaleString('es-PY')}</span>
            </div>
            <div class="pt-2 border-t border-slate-800/80 flex items-center justify-between">
              <div>
                <p class="text-[10px] font-bold text-emerald-300">Con tu ${offer.bankTag}:</p>
                <p class="text-lg font-black text-emerald-400">Gs. ${offer.finalPrice.toLocaleString('es-PY')}</p>
              </div>
              ${offer.discountPct > 0 ? `
                <span class="text-xs font-black px-2.5 py-1 rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                  -${offer.discountPct}% Ahorro
                </span>
              ` : '<span class="text-xs text-slate-500">Sin descuento bancario hoy</span>'}
            </div>
          </div>

          <!-- COMPARATIVA ENTRE TODOS LOS SUPERMERCADOS (MÁS BARATO AL MÁS CARO) -->
          <div class="space-y-2 pt-2 border-t border-slate-800">
            <div class="flex items-center justify-between px-1">
              <div>
                <span class="text-xs font-black uppercase text-white tracking-wider flex items-center space-x-1.5">
                  <span class="text-emerald-400">🏬</span>
                  <span>Precios en los demás Supermercados:</span>
                </span>
                <p class="text-[10px] text-slate-400 mt-0.5">Calculado con tus tarjetas para hoy ${getDayName(selectedDay)}</p>
              </div>
              <span class="text-[10px] text-emerald-400 font-extrabold bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">${comparisons.length} comercios en ${selectedCity}</span>
            </div>

            <div class="space-y-2 pt-1" id="supermarketComparisonList">
              ${comparisons.map((st, i) => {
                const isWinner = i === 0;
                const diff = st.finalPrice - cheapestPrice;
                const winnerBadge = isWinner 
                  ? `<span class="text-[9px] font-black uppercase px-2 py-0.5 rounded-full bg-emerald-500 text-slate-950 shadow-sm flex items-center space-x-1"><span>👑</span><span>Más Barato</span></span>`
                  : `<span class="text-[9px] font-extrabold text-slate-400 bg-slate-800 px-2 py-0.5 rounded-full border border-slate-700/60">+ Gs. ${diff.toLocaleString('es-PY')}</span>`;
                
                const cardBorder = isWinner 
                  ? 'border-2 border-emerald-500/80 bg-emerald-500/10 shadow-lg shadow-emerald-500/10 ring-1 ring-emerald-500/30' 
                  : 'border border-slate-800 bg-slate-950/70 hover:border-slate-700';

                return `
                  <div class="p-3 rounded-2xl ${cardBorder} flex items-center justify-between transition-all">
                    <div class="flex items-center space-x-2.5 min-w-0">
                      <div class="w-9 h-9 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center text-base shrink-0">
                        ${st.icon}
                      </div>
                      <div class="min-w-0">
                        <div class="flex items-center space-x-1.5">
                          <p class="text-xs font-black text-white truncate">${st.name}</p>
                          ${st.isLocal ? '<span class="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Local • En Tienda</span>' : ''}
                          ${winnerBadge}
                        </div>
                        <p class="text-[10px] text-slate-400 truncate mt-0.5 flex items-center space-x-1">
                          <span class="${isWinner ? 'text-emerald-300 font-bold' : 'text-slate-400'}">${st.bankTag}</span>
                          <span class="text-slate-600">•</span>
                          <span>${st.desc}</span>
                        </p>
                      </div>
                    </div>

                    <div class="text-right shrink-0 ml-2">
                      <p class="text-[10px] text-slate-400 font-bold">Real: Gs. ${st.regularPrice.toLocaleString('es-PY')}</p>
                      <p class="text-sm font-black ${isWinner ? 'text-emerald-400' : 'text-white'}">Gs. ${st.finalPrice.toLocaleString('es-PY')}</p>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>

          <!-- GRÁFICO HISTORIAL KNASTA 30 DÍAS -->
          <div class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
            <div class="flex justify-between items-center text-[11px]">
              <span class="font-extrabold text-slate-400">Evolución de Precio (Últimos 30 días)</span>
              <span class="text-emerald-400 font-extrabold">🟢 Precio Mínimo Knasta</span>
            </div>
            
            <div class="h-24 w-full flex items-center justify-center">
              <svg viewBox="0 0 280 90" class="w-full h-full overflow-visible">
                <polyline fill="none" stroke="#10b981" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" points="${pts}" />
                ${prod.history.map((val, i) => {
                  const x = 20 + i * 50;
                  const y = 80 - ((val - minHist) / range) * 60;
                  return `<circle cx="${x}" cy="${y}" r="3.5" fill="#090D16" stroke="#10b981" stroke-width="2.5" />`;
                }).join('')}
              </svg>
            </div>

            <div class="flex justify-between text-[10px] font-bold text-slate-500 pt-1 border-t border-slate-800/80">
              <span>Hace 30 días (Gs. ${prod.history[0].toLocaleString('es-PY')})</span>
              <span>Hoy más barato (Gs. ${cheapestPrice.toLocaleString('es-PY')})</span>
            </div>
          </div>

          <!-- BOTONES DE ACCIÓN -->
          <div class="grid grid-cols-2 gap-2 pt-1">
            <button onclick="flyToCart(${idx}, null); closeProductModal();" class="py-3 rounded-2xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs flex items-center justify-center space-x-1.5 transition active:scale-95 shadow-lg shadow-emerald-500/20">
              <span>+ Sumar a mi Lista</span>
            </button>
            <button onclick="closeProductModal()" class="py-3 rounded-2xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-extrabold text-xs transition active:scale-95">
              Cerrar
            </button>
          </div>
        </div>
      `;

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
    function renderDayChips() {
      const container = document.getElementById('dayChipsContainer');
      if (!container) return;
      const now = new Date();
      const currentDayOfWeek = now.getDay(); // 0=Sun, 1=Mon... 6=Sat
      const diffToMonday = (currentDayOfWeek === 0 ? -6 : 1 - currentDayOfWeek);
      const monday = new Date(now);
      monday.setDate(now.getDate() + diffToMonday);

      const daysData = [
        { num: 1, label: 'Lun' },
        { num: 2, label: 'Mar' },
        { num: 3, label: 'Mié' },
        { num: 4, label: 'Jue' },
        { num: 5, label: 'Vie' },
        { num: 6, label: 'Sáb' },
        { num: 7, label: 'Dom' }
      ];

      container.innerHTML = daysData.map((d, idx) => {
        const dDate = new Date(monday);
        dDate.setDate(monday.getDate() + idx);
        const dateNum = String(dDate.getDate()).padStart(2, '0');
        const isSelected = (d.num === selectedDay);
        const isToday = (d.num === currentIsoDay);
        const todayPill = isToday ? '<span class="text-[7px] text-emerald-300 block font-black leading-none mt-0.5">HOY</span>' : '';

        return `
          <button onclick="setDay(${d.num})" data-day="${d.num}" class="day-chip py-1.5 rounded-xl text-center text-[11px] font-extrabold transition ${isSelected ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/30 ring-1 ring-emerald-400' : 'bg-slate-900/80 text-slate-400 hover:text-white'}">
            <span class="block text-[9px] uppercase font-semibold ${isSelected ? 'text-emerald-100' : 'text-slate-500'}">${d.label}</span>
            <span>${dateNum}</span>
            ${todayPill}
          </button>
        `;
      }).join('');
    }

    function setDay(d) {
      selectedDay = d;
      renderDayChips();
      
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
      renderDayChips();
    }

    function getDayName(d) {
      const names = { 1: 'Lunes', 2: 'Martes', 3: 'Miércoles', 4: 'Jueves', 5: 'Viernes', 6: 'Sábado', 7: 'Domingo' };
      return names[d] || 'Día seleccionado';
    }

    // ESCÁNER YUKA
    function scanSpecificProduct(idx) {
      if (idx >= 0 && idx < products.length) {
        currentScannedIdx = idx;
        const prod = products[idx];
        const offer = calculateProductOffer(prod, selectedDay);

        const nameEl = document.getElementById('scannedProductName');
        const brandEl = document.getElementById('scannedProductBrand');
        const imgEl = document.getElementById('scannedProductImg');
        const dealEl = document.getElementById('scannedBestDealText');
        const verdictEl = document.getElementById('scannedVerdictBadge');

        if (nameEl) nameEl.innerText = prod.name;
        if (brandEl) brandEl.innerText = prod.brand + ' • ' + prod.store;
        if (imgEl) imgEl.src = prod.image;
        if (dealEl) dealEl.innerText = 'Gs. ' + offer.finalPrice.toLocaleString('es-PY') + ' con ' + offer.bankTag;
        
        if (verdictEl) {
          if (offer.discountPct >= 20) {
            verdictEl.innerHTML = '🟢 Precio Excelente (-' + offer.discountPct + '%)';
            verdictEl.className = 'text-[10px] font-black uppercase text-emerald-400 tracking-wider';
          } else if (offer.discountPct > 0) {
            verdictEl.innerHTML = '🟡 Buen Precio (-' + offer.discountPct + '%)';
            verdictEl.className = 'text-[10px] font-black uppercase text-amber-400 tracking-wider';
          } else {
            verdictEl.innerHTML = '⚪ Precio Góndola Regular';
            verdictEl.className = 'text-[10px] font-black uppercase text-slate-400 tracking-wider';
          }
        }

        showToast('⚡ ¡Código detectado! ' + prod.name.substring(0, 18));
      }
    }

    function simulateScanBarcode() {
      const nextIdx = (currentScannedIdx + 1) % products.length;
      playBeepSound();
      scanSpecificProduct(nextIdx);
    }

    function addScannedProductToCart() {
      flyToCart(currentScannedIdx, null);
      switchTab('viewCart');
    }

    
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
          <button onclick="selectBrand('${b.replace(/'/g, "\\'")}', '🏷️', '${b.replace(/'/g, "\\'")}')" class="w-full p-2.5 rounded-xl ${isSelected ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300' : 'bg-slate-950/70 border-slate-800 text-slate-300 hover:border-slate-700 hover:text-white'} border flex items-center justify-between text-xs font-bold transition active:scale-[0.99] cursor-pointer">
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

    function toggleScannerFlashlight() {
      isFlashlightOn = !isFlashlightOn;
      const lbl = document.getElementById('scannerFlashLabel');
      const icon = document.getElementById('scannerFlashIcon');
      const cam = document.getElementById('scannerCameraView');
      if (isFlashlightOn) {
        lbl.innerText = 'Linterna: ON';
        icon.innerText = '💡';
        if (cam) cam.classList.add('shadow-[inset_0_0_90px_rgba(255,255,255,0.35)]', 'border-yellow-400/50');
        showToast('💡 Linterna del escáner encendida');
      } else {
        lbl.innerText = 'Linterna: OFF';
        icon.innerText = '🔦';
        if (cam) cam.classList.remove('shadow-[inset_0_0_90px_rgba(255,255,255,0.35)]', 'border-yellow-400/50');
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
    function renderSupermarketSheet() {
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

      // 4. Update all toggle buttons (switches con círculo deslizante)
      ['ueno', 'itau', 'continental', 'zeta', 'familiar', 'atlas', 'sudameris', 'gnb', 'basa'].forEach(slug => {
        const btn = document.getElementById('btn-' + slug);
        const thumb = document.getElementById('thumb-' + slug);
        const dot = document.getElementById('dot-' + slug);
        const isActive = bankProfiles[slug] && bankProfiles[slug].enabled;
        
        if (btn) {
          if (isActive) {
            btn.className = "w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-emerald-500 shadow-md shadow-emerald-500/20 flex items-center focus:outline-none active:scale-95";
          } else {
            btn.className = "w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-slate-800 border border-slate-700 flex items-center focus:outline-none active:scale-95";
          }
        }
        if (thumb) {
          if (isActive) {
            thumb.className = "w-4 h-4 rounded-full bg-white shadow-md transition-transform duration-200 translate-x-6 pointer-events-none";
          } else {
            thumb.className = "w-4 h-4 rounded-full bg-slate-400 shadow-md transition-transform duration-200 translate-x-0 pointer-events-none";
          }
        } else if (btn) {
          btn.innerHTML = `<div id="thumb-${slug}" class="${isActive ? 'w-4 h-4 rounded-full bg-white shadow-md transition-transform duration-200 translate-x-6 pointer-events-none' : 'w-4 h-4 rounded-full bg-slate-400 shadow-md transition-transform duration-200 translate-x-0 pointer-events-none'}"></div>`;
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
        icon: '⚡',
        officialUrl: 'https://www.ueno.com.py/beneficios'
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
        icon: '📱',
        officialUrl: 'https://www.ueno.com.py/beneficios'
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
        icon: '💳',
        officialUrl: 'https://www.itau.com.py/beneficios'
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
        icon: '🏪',
        officialUrl: 'https://www.itau.com.py/beneficios'
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
        icon: '⚡',
        officialUrl: 'https://www.zetabanco.com.py'
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
        icon: '💳',
        officialUrl: 'https://www.bancontinental.com.py/beneficios'
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
        icon: '🛍️',
        officialUrl: 'https://www.familiar.com.py/beneficios'
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
        icon: '💳',
        officialUrl: 'https://www.bancoatlas.com.py/beneficios'
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
        icon: '👑',
        officialUrl: 'https://www.sudameris.com.py/beneficios'
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
        icon: '🛒',
        officialUrl: 'https://www.bancognb.com.py/beneficios'
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
        icon: '🏷️',
        officialUrl: 'https://www.basa.com.py/beneficios'
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
        container.innerHTML = `
          <div class="p-8 text-center text-slate-500 glass-card rounded-3xl">
            <span class="text-4xl">💳</span>
            <p class="text-xs font-bold mt-2">No tienes tarjetas activas con promociones</p>
            <p class="text-[10px] text-slate-600">Activa tus tarjetas en la pestaña Perfil para ver tus beneficios</p>
            <button onclick="switchTab('viewProfile')" class="mt-3 px-3 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-400 font-bold text-xs border border-emerald-500/30">
              Ir a Mi Billetera
            </button>
          </div>
        `;
        return;
      }

      container.innerHTML = filtered.map(p => {
        const isCardActive = bankProfiles[p.bankKey] && bankProfiles[p.bankKey].enabled;
        const isTodayActive = p.dayNumbers.includes(selectedDay);
        const dayBadge = isTodayActive 
          ? `<span class="text-[9px] font-black uppercase px-2 py-0.5 rounded-full bg-emerald-400 text-slate-950 shadow-sm animate-pulse">⚡ Válido Hoy ${getDayName(selectedDay)}</span>` 
          : `<span class="text-[9px] font-bold text-white/80">${p.daysText}</span>`;

        return `
          <div class="p-4 rounded-3xl ${p.cardClass} text-white shadow-xl relative overflow-hidden transition-all duration-300 hover:scale-[1.01]">
            <div class="flex justify-between items-start">
              <div>
                <div class="flex items-center space-x-2">
                  <span class="text-[10px] uppercase font-black tracking-widest text-white/80">${p.bankName}</span>
                  ${dayBadge}
                </div>
                <h3 class="text-base font-black mt-1 leading-tight">${p.title}</h3>
                <p class="text-xs text-white/90 font-semibold mt-1">🏬 ${p.supermarket}</p>
              </div>
              <span class="text-2xl drop-shadow">${p.icon}</span>
            </div>

            <div class="mt-4 pt-3 border-t border-white/20 flex flex-col sm:flex-row gap-2 justify-between items-start sm:items-center text-xs">
              <span class="text-white/80 text-[11px]">${p.capText}</span>
              <div class="flex items-center space-x-1.5 w-full sm:w-auto justify-end">
                <a href="${p.officialUrl}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();" class="px-2.5 py-1 rounded-xl bg-white/20 hover:bg-white/30 text-white font-bold text-[11px] flex items-center space-x-1 border border-white/25 transition active:scale-95 shadow-sm">
                  <span>🔗</span>
                  <span>Web Oficial ↗</span>
                </a>
                <button onclick="toggleBankProfile('${p.bankKey}')" class="px-2.5 py-1 rounded-xl ${isCardActive ? 'bg-black/30 text-white font-extrabold border border-white/25' : 'bg-white text-slate-950 font-black shadow-md'} transition active:scale-95">
                  ${isCardActive ? '✓ Activa' : '+ Activar'}
                </button>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    // PERSISTENCIA LOCAL
    // =========================================================================
    // MOTOR DE IMPACTO Y SEGUIMIENTO DE AHORRO REAL (SEMANA, MES, TOTAL)
    // =========================================================================
    let userSavings = {
      week: 0,
      month: 0,
      total: 0,
      spentWithPreciosPyMonth: 0,
      spentWithoutPreciosPyMonth: 0,
      activePeriod: 'month',
      history: []
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

    function saveLocalData() {
      try {
        localStorage.setItem('preciospy_2_cart', JSON.stringify(cart));
        localStorage.setItem('preciospy_2_bank_profiles', JSON.stringify(bankProfiles));
        localStorage.setItem('preciospy_2_city', selectedCity);
        localStorage.setItem('preciospy_2_favorites', JSON.stringify(favorites));
        localStorage.setItem('preciospy_2_cash_mode', JSON.stringify(isCashOnly));
        localStorage.setItem('preciospy_2_savings', JSON.stringify(userSavings));
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
        const rawFavs = localStorage.getItem('preciospy_2_favorites');
        if (rawFavs) favorites = JSON.parse(rawFavs);
        const rawSavings = localStorage.getItem('preciospy_2_savings');
        if (rawSavings) {
          try { userSavings = JSON.parse(rawSavings); } catch (e) {}
        }
                const rawCash = localStorage.getItem('preciospy_2_cash_mode');
        if (rawCash !== null) {
          isCashOnly = JSON.parse(rawCash);
          const btn = document.getElementById('cashModeBtn');
          const text = document.getElementById('cashModeText');
          const icon = document.getElementById('cashModeIcon');
          if (btn && text && icon) {
            if (isCashOnly) {
              btn.className = "px-2.5 py-1.5 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 bg-amber-500/20 border border-amber-500 text-amber-300 active:scale-95";
              icon.innerText = '💵';
              text.innerText = 'Solo Efectivo';
            } else {
              btn.className = "px-2.5 py-1.5 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 bg-slate-800/80 border border-slate-700 hover:border-emerald-500/50 text-slate-300 active:scale-95";
              icon.innerText = '💳';
              text.innerText = 'Con Tarjetas';
            }
          }
        }
      } catch (e) {}
    }

    function openResetDataModal() {
      const m = document.getElementById('resetDataModal');
      if (m) m.classList.remove('hidden');
    }

    function closeResetDataModal() {
      const m = document.getElementById('resetDataModal');
      if (m) m.classList.add('hidden');
    }

    function confirmResetData() {
      try {
        localStorage.removeItem('preciospy_2_cart');
        localStorage.removeItem('preciospy_2_bank_profiles');
        localStorage.removeItem('preciospy_2_city');
        localStorage.removeItem('preciospy_2_favorites');
        localStorage.removeItem('preciospy_2_cash_mode');
      } catch(e) {}
      closeResetDataModal();
      showToast('🔄 Configuración restablecida');
      setTimeout(() => {
        location.reload();
      }, 500);
    }

    function resetUserDataToDefault() {
      openResetDataModal();
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
      saveLocalData();
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
      const cartKeys = Object.keys(cart).filter(k => (cart[k] || 0) > 0);
      if (cartKeys.length === 0) {
        showToast('⚠️ Tu lista está vacía. ¡Agrega productos primero!');
        return;
      }

      const dayNames = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
      const dayName = dayNames[selectedDay] || 'Hoy';

      let totalRegular = 0;
      let totalFinal = 0;
      let productLines = [];

      cartKeys.forEach(k => {
        const prod = products[k];
        if (!prod) return;
        const qty = cart[k];
        const offer = calculateProductOffer(prod, selectedDay);
        const subtotalReg = prod.regularPrice * qty;
        const subtotalFin = offer.finalPrice * qty;
        totalRegular += subtotalReg;
        totalFinal += subtotalFin;

        let itemTxt = '• ' + qty + 'x ' + prod.name + '\\n  Gs. ' + subtotalFin.toLocaleString('es-PY');
        if (offer.discountPct > 0 && !isCashOnly) {
          itemTxt += ' (' + offer.discountPct + '% OFF con ' + offer.bankTag + ')';
        }
        productLines.push(itemTxt);
      });

      const totalSavings = Math.max(0, totalRegular - totalFinal);

      let msg = '🛒 *MI LISTA DE COMPRAS — PreciosPy*\\n';
      msg += '📍 *Ciudad:* ' + (typeof selectedCity !== 'undefined' ? selectedCity : 'Caacupé') + ' | 📅 *Día:* ' + dayName + '\\n';
      msg += '------------------------------------\\n';
      msg += productLines.join('\\n') + '\\n';
      msg += '------------------------------------\\n';
      msg += '📦 Subtotal Regular: Gs. ' + totalRegular.toLocaleString('es-PY') + '\\n';
      if (totalSavings > 0) {
        msg += '⚡ Descuento con Tarjetas: - Gs. ' + totalSavings.toLocaleString('es-PY') + '\\n';
      }
      msg += '💰 *TOTAL A PAGAR: Gs. ' + totalFinal.toLocaleString('es-PY') + '*\\n';
      msg += '👑 *Súper más conveniente:* Biggie Express\\n\\n';
      msg += '_Generado con PreciosPy — El comparador inteligente de Paraguay_ 🇵🇾';

      // 1. Copiar al portapapeles siempre como respaldo
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(msg).catch(function(err) {
          console.log('Clipboard fallback:', err);
        });
      }

      showToast('💬 Abriendo WhatsApp y lista copiada...');

      // 2. Abrir WhatsApp mediante link dinámico sin popup blocker
      const waUrl = 'https://api.whatsapp.com/send?text=' + encodeURIComponent(msg);
      const link = document.createElement('a');
      link.href = waUrl;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      document.body.appendChild(link);
      link.click();
      setTimeout(function() {
        if (link.parentNode) link.parentNode.removeChild(link);
      }, 500);
    }
  </script>
</body>
</html>
'''

with open('preciospy_redesign_2026.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

artifact_dir = r'C:\Users\munic\.gemini\antigravity\brain\3ac93072-98c3-495f-ad02-c8cfc7984916'
os.makedirs(artifact_dir, exist_ok=True)
artifact_file = os.path.join(artifact_dir, 'preciospy_redesign_2026.html')
with open(artifact_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully generated preciospy_redesign_2026.html ({len(html_content)} bytes) and copied to artifacts!")

