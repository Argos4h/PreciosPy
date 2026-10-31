const fs = require('fs');
const path = require('path');

const files = [
  path.resolve(__dirname, '../precios_py_demo.html'),
  path.resolve('C:/Users/munic/.gemini/antigravity/brain/3ac93072-98c3-495f-ad02-c8cfc7984916/precios_py_interactive_demo.html')
];

files.forEach(f => {
  if (!fs.existsSync(f)) {
    console.error('File not found:', f);
    return;
  }
  let content = fs.readFileSync(f, 'utf8');

  // Persistence helpers
  const persistenceCode = [
    '    // ==========================================',
    '    // PERSISTENCIA LOCAL AUTOMÁTICA (localStorage)',
    '    // Cada persona / dispositivo guarda su propia configuración y carrito',
    '    // ==========================================',
    '    const STORAGE_KEY = "preciospy_user_data_v1";',
    '',
    '    function saveUserData() {',
    '      try {',
    '        const payload = {',
    '          bankProfiles,',
    '          cart,',
    '          userFavorites,',
    '          selectedCity,',
    '          isDarkMode,',
    '          isCashOnly',
    '        };',
    '        localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));',
    '      } catch (e) {',
    '        console.warn("No se pudo guardar en localStorage:", e);',
    '      }',
    '    }',
    '',
    '    function loadUserData() {',
    '      try {',
    '        const raw = localStorage.getItem(STORAGE_KEY);',
    '        if (!raw) return;',
    '        const data = JSON.parse(raw);',
    '        if (data.bankProfiles && typeof data.bankProfiles === "object") {',
    '          bankProfiles = { ...bankProfiles, ...data.bankProfiles };',
    '        }',
    '        if (data.cart && typeof data.cart === "object") {',
    '          cart = data.cart;',
    '        }',
    '        if (Array.isArray(data.userFavorites)) {',
    '          userFavorites = data.userFavorites;',
    '        }',
    '        if (data.selectedCity && citySupermarkets[data.selectedCity]) {',
    '          selectedCity = data.selectedCity;',
    '        }',
    '        if (typeof data.isDarkMode === "boolean") {',
    '          isDarkMode = data.isDarkMode;',
    '        }',
    '        if (typeof data.isCashOnly === "boolean") {',
    '          isCashOnly = data.isCashOnly;',
    '        }',
    '      } catch (e) {',
    '        console.warn("No se pudo cargar desde localStorage:", e);',
    '      }',
    '    }',
    '',
    '    function resetUserDataToDefault() {',
    '      if (confirm("¿Deseas restablecer tus tarjetas, carrito y favoritos a los valores predeterminados?")) {',
    '        localStorage.removeItem(STORAGE_KEY);',
    '        location.reload();',
    '      }',
    '    }',
    ''
  ].join('\n');

  // Insert persistenceCode right before catalog declaration
  if (!content.includes('const STORAGE_KEY = "preciospy_user_data_v1";')) {
    content = content.replace('    // BASE DE DATOS LOCAL CON FOTOS Y CATEGORÍAS', persistenceCode + '\n    // BASE DE DATOS LOCAL CON FOTOS Y CATEGORÍAS');
  }

  // Hook saveUserData into state changes:
  if (!content.includes('renderScannerView();\n        saveUserData();') && !content.includes('renderScannerView();\r\n        saveUserData();')) {
    content = content.replace(
      '        renderScannerView();\r\n      }\r\n    }',
      '        renderScannerView();\r\n        saveUserData();\r\n      }\r\n    }'
    );
    content = content.replace(
      '        renderScannerView();\n      }\n    }',
      '        renderScannerView();\n        saveUserData();\n      }\n    }'
    );
  }

  // setUenoLevel
  content = content.replace(
    'showToast(`ueno configurado en Nivel ${lvl}`);',
    'showToast(`ueno configurado en Nivel ${lvl}`);\n      saveUserData();'
  );

  // setBankTier
  content = content.replace(
    'showToast(`${slug.toUpperCase()}: ${tier.toUpperCase()}`);',
    'showToast(`${slug.toUpperCase()}: ${tier.toUpperCase()}`);\n        saveUserData();'
  );

  // setBankQr
  content = content.replace(
    'renderPromosView();\r\n      }\r\n    }',
    'renderPromosView();\r\n        saveUserData();\r\n      }\r\n    }'
  );
  content = content.replace(
    'renderPromosView();\n      }\n    }',
    'renderPromosView();\n        saveUserData();\n      }\n    }'
  );

  // quickAddToCart
  content = content.replace(
    'updateCartBadge();\r\n    }',
    'updateCartBadge();\r\n      saveUserData();\r\n    }'
  );
  content = content.replace(
    'updateCartBadge();\n    }',
    'updateCartBadge();\n      saveUserData();\n    }'
  );

  // decrementCartItem
  content = content.replace(
    'if (cart[prodIdx] <= 0) delete cart[prodIdx];\r\n      renderCartView();\r\n      updateCartBadge();',
    'if (cart[prodIdx] <= 0) delete cart[prodIdx];\r\n      renderCartView();\r\n      updateCartBadge();\r\n      saveUserData();'
  );
  content = content.replace(
    'if (cart[prodIdx] <= 0) delete cart[prodIdx];\n      renderCartView();\n      updateCartBadge();',
    'if (cart[prodIdx] <= 0) delete cart[prodIdx];\n      renderCartView();\n      updateCartBadge();\n      saveUserData();'
  );

  // clearCart
  content = content.replace(
    'cart = {};\r\n      renderCartView();\r\n      updateCartBadge();',
    'cart = {};\r\n      renderCartView();\r\n      updateCartBadge();\r\n      saveUserData();'
  );
  content = content.replace(
    'cart = {};\n      renderCartView();\n      updateCartBadge();',
    'cart = {};\n      renderCartView();\n      updateCartBadge();\n      saveUserData();'
  );

  // toggleFavorite
  content = content.replace(
    'renderProfileView();\r\n    }\r\n\r\n    function shareCart()',
    'renderProfileView();\r\n      saveUserData();\r\n    }\r\n\r\n    function shareCart()'
  );
  content = content.replace(
    'renderProfileView();\n    }\n\n    function shareCart()',
    'renderProfileView();\n      saveUserData();\n    }\n\n    function shareCart()'
  );

  // selectCity
  content = content.replace(
    'renderScannerView();\r\n    }',
    'renderScannerView();\r\n      saveUserData();\r\n    }'
  );
  content = content.replace(
    'renderScannerView();\n    }',
    'renderScannerView();\n      saveUserData();\n    }'
  );

  // toggleCashOnly
  content = content.replace(
    'isCashOnly = !isCashOnly;\r\n      }',
    'isCashOnly = !isCashOnly;\r\n      }\r\n      saveUserData();'
  );
  content = content.replace(
    'isCashOnly = !isCashOnly;\n      }',
    'isCashOnly = !isCashOnly;\n      }\n      saveUserData();'
  );

  // toggleTheme
  content = content.replace(
    'applyTheme();\r\n    }\r\n\r\n    function setThemeMode',
    'applyTheme();\r\n      saveUserData();\r\n    }\r\n\r\n    function setThemeMode'
  );
  content = content.replace(
    'applyTheme();\n    }\n\n    function setThemeMode',
    'applyTheme();\n      saveUserData();\n    }\n\n    function setThemeMode'
  );

  // Improved shareCart function
  const improvedShareCart = [
    '    function shareCart() {',
    '      const items = Object.entries(cart).filter(([_, qty]) => qty > 0);',
    '      if (items.length === 0) {',
    '        showToast("Tu lista de compras está vacía");',
    '        return;',
    '      }',
    '      let text = "🛒 *Mi Lista de Compras en PreciosPy:*\\n";',
    '      items.forEach(([idx, qty]) => {',
    '        const prod = catalog[idx];',
    '        if (prod) text += "• " + qty + "x " + prod.name + "\\n";',
    '      });',
    '      text += "\\n📍 Ciudad: " + selectedCity + "\\n💡 Precios comparados con ofertas y tarjetas bancarias en PreciosPy\\n🔗 https://preciospy.com.py";',
    '      if (navigator.clipboard && navigator.clipboard.writeText) {',
    '        navigator.clipboard.writeText(text).then(() => {',
    '          showToast("📋 ¡Lista copiada para enviar por WhatsApp!");',
    '        }).catch(() => {',
    '          showToast("📋 Lista preparada");',
    '        });',
    '      } else {',
    '        showToast("📋 Lista preparada");',
    '      }',
    '      if (navigator.share) {',
    '        navigator.share({ title: "Mi Lista PreciosPy", text: text }).catch(() => {});',
    '      }',
    '    }'
  ].join('\n');

  content = content.replace(/function shareCart\(\) \{[\s\S]*?function switchTab/, improvedShareCart + '\n\n    function switchTab');

  // Call loadUserData() on DOMContentLoaded
  if (!content.includes('loadUserData();')) {
    content = content.replace(
      'window.addEventListener(\'DOMContentLoaded\', () => {',
      'window.addEventListener(\'DOMContentLoaded\', () => {\r\n      loadUserData();'
    );
  }

  // Add "Restablecer mis datos" button in Perfil tab
  const resetBtnHtml = [
    '          <!-- Botón Restablecer Datos de Usuario -->',
    '          <div class="pt-4 border-t border-slate-700/50 mt-4 text-center">',
    '            <button onclick="resetUserDataToDefault()" class="text-xs text-rose-400 hover:text-rose-300 font-bold px-3 py-1.5 rounded-xl border border-rose-500/30 hover:bg-rose-500/10 transition">',
    '              🗑️ Restablecer mis tarjetas y carrito por defecto',
    '            </button>',
    '            <p class="text-[10px] text-slate-500 mt-1">Tus datos se guardan de forma privada en tu propio dispositivo.</p>',
    '          </div>'
  ].join('\n');

  if (!content.includes('resetUserDataToDefault()')) {
    content = content.replace('          <!-- Botón Tutorial Guiado -->', resetBtnHtml + '\n          <!-- Botón Tutorial Guiado -->');
  }

  fs.writeFileSync(f, content, 'utf8');
  console.log('Persistence added to:', f);
});
