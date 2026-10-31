import re

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace button ueno
old_ueno = '<button id="btn-ueno" onclick="toggleBankProfile(\'ueno\')" class="px-3 py-1 rounded-xl bg-emerald-500/20 text-emerald-400 font-bold text-xs border border-emerald-500/30 active:scale-95 transition">Activa</button>'
new_ueno = '<button id="btn-ueno" onclick="toggleBankProfile(\'ueno\')" aria-label="Alternar ueno" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-emerald-500 shadow-md shadow-emerald-500/20 flex items-center focus:outline-none active:scale-95">\n                <div id="thumb-ueno" class="w-4 h-4 rounded-full bg-white shadow-md transition-transform duration-200 translate-x-6 pointer-events-none"></div>\n              </button>'
assert old_ueno in content, "old_ueno not found"
content = content.replace(old_ueno, new_ueno)

# 2. Replace button itau
old_itau = '<button id="btn-itau" onclick="toggleBankProfile(\'itau\')" class="px-3 py-1 rounded-xl bg-emerald-500/20 text-emerald-400 font-bold text-xs border border-emerald-500/30 active:scale-95 transition">Activa</button>'
new_itau = '<button id="btn-itau" onclick="toggleBankProfile(\'itau\')" aria-label="Alternar Itaú" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-emerald-500 shadow-md shadow-emerald-500/20 flex items-center focus:outline-none active:scale-95">\n                <div id="thumb-itau" class="w-4 h-4 rounded-full bg-white shadow-md transition-transform duration-200 translate-x-6 pointer-events-none"></div>\n              </button>'
assert old_itau in content, "old_itau not found"
content = content.replace(old_itau, new_itau)

# 3. Replace button continental
old_conti = '<button id="btn-continental" onclick="toggleBankProfile(\'continental\')" class="px-3 py-1 rounded-xl bg-slate-800 text-slate-400 font-bold text-xs border border-slate-700 active:scale-95 transition">+ Activar</button>'
new_conti = '<button id="btn-continental" onclick="toggleBankProfile(\'continental\')" aria-label="Alternar Continental" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-slate-800 border border-slate-700 flex items-center focus:outline-none active:scale-95">\n                <div id="thumb-continental" class="w-4 h-4 rounded-full bg-slate-400 shadow-md transition-transform duration-200 translate-x-0 pointer-events-none"></div>\n              </button>'
assert old_conti in content, "old_conti not found"
content = content.replace(old_conti, new_conti)

# 4. Replace button zeta
old_zeta = '<button id="btn-zeta" onclick="toggleBankProfile(\'zeta\')" class="px-3 py-1 rounded-xl bg-emerald-500/20 text-emerald-400 font-bold text-xs border border-emerald-500/30 active:scale-95 transition">Activa</button>'
new_zeta = '<button id="btn-zeta" onclick="toggleBankProfile(\'zeta\')" aria-label="Alternar Zeta" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-emerald-500 shadow-md shadow-emerald-500/20 flex items-center focus:outline-none active:scale-95">\n              <div id="thumb-zeta" class="w-4 h-4 rounded-full bg-white shadow-md transition-transform duration-200 translate-x-6 pointer-events-none"></div>\n            </button>'
assert old_zeta in content, "old_zeta not found"
content = content.replace(old_zeta, new_zeta)

# 5. Replace button familiar
old_familiar = '<button id="btn-familiar" onclick="toggleBankProfile(\'familiar\')" class="px-3 py-1 rounded-xl bg-slate-800 text-slate-400 font-bold text-xs border border-slate-700 active:scale-95 transition">+ Activar</button>'
new_familiar = '<button id="btn-familiar" onclick="toggleBankProfile(\'familiar\')" aria-label="Alternar Familiar" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-slate-800 border border-slate-700 flex items-center focus:outline-none active:scale-95">\n              <div id="thumb-familiar" class="w-4 h-4 rounded-full bg-slate-400 shadow-md transition-transform duration-200 translate-x-0 pointer-events-none"></div>\n            </button>'
assert old_familiar in content, "old_familiar not found"
content = content.replace(old_familiar, new_familiar)

# 6. Replace button atlas
old_atlas = '<button id="btn-atlas" onclick="toggleBankProfile(\'atlas\')" class="px-3 py-1 rounded-xl bg-slate-800 text-slate-400 font-bold text-xs border border-slate-700 active:scale-95 transition">+ Activar</button>'
new_atlas = '<button id="btn-atlas" onclick="toggleBankProfile(\'atlas\')" aria-label="Alternar Atlas" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-slate-800 border border-slate-700 flex items-center focus:outline-none active:scale-95">\n              <div id="thumb-atlas" class="w-4 h-4 rounded-full bg-slate-400 shadow-md transition-transform duration-200 translate-x-0 pointer-events-none"></div>\n            </button>'
assert old_atlas in content, "old_atlas not found"
content = content.replace(old_atlas, new_atlas)

# 7. Replace button sudameris
old_sudameris = '<button id="btn-sudameris" onclick="toggleBankProfile(\'sudameris\')" class="px-3 py-1 rounded-xl bg-slate-800 text-slate-400 font-bold text-xs border border-slate-700 active:scale-95 transition">+ Activar</button>'
new_sudameris = '<button id="btn-sudameris" onclick="toggleBankProfile(\'sudameris\')" aria-label="Alternar Sudameris" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-slate-800 border border-slate-700 flex items-center focus:outline-none active:scale-95">\n              <div id="thumb-sudameris" class="w-4 h-4 rounded-full bg-slate-400 shadow-md transition-transform duration-200 translate-x-0 pointer-events-none"></div>\n            </button>'
assert old_sudameris in content, "old_sudameris not found"
content = content.replace(old_sudameris, new_sudameris)

# 8. Replace button gnb
old_gnb = '<button id="btn-gnb" onclick="toggleBankProfile(\'gnb\')" class="px-3 py-1 rounded-xl bg-slate-800 text-slate-400 font-bold text-xs border border-slate-700 active:scale-95 transition">+ Activar</button>'
new_gnb = '<button id="btn-gnb" onclick="toggleBankProfile(\'gnb\')" aria-label="Alternar GNB" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-slate-800 border border-slate-700 flex items-center focus:outline-none active:scale-95">\n              <div id="thumb-gnb" class="w-4 h-4 rounded-full bg-slate-400 shadow-md transition-transform duration-200 translate-x-0 pointer-events-none"></div>\n            </button>'
assert old_gnb in content, "old_gnb not found"
content = content.replace(old_gnb, new_gnb)

# 9. Replace button basa
old_basa = '<button id="btn-basa" onclick="toggleBankProfile(\'basa\')" class="px-3 py-1 rounded-xl bg-slate-800 text-slate-400 font-bold text-xs border border-slate-700 active:scale-95 transition">+ Activar</button>'
new_basa = '<button id="btn-basa" onclick="toggleBankProfile(\'basa\')" aria-label="Alternar Basa" class="w-12 h-6 rounded-full p-1 transition-colors duration-200 bg-slate-800 border border-slate-700 flex items-center focus:outline-none active:scale-95">\n              <div id="thumb-basa" class="w-4 h-4 rounded-full bg-slate-400 shadow-md transition-transform duration-200 translate-x-0 pointer-events-none"></div>\n            </button>'
assert old_basa in content, "old_basa not found"
content = content.replace(old_basa, new_basa)

# 10. Update updateProfileButtons logic
old_update = """      // 4. Update all toggle buttons
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
      });"""

new_update = """      // 4. Update all toggle buttons (switches con círculo deslizante)
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
      });"""

assert old_update in content, "old_update not found"
content = content.replace(old_update, new_update)

with open('scripts/build_html.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully patched build_html.py with circle toggle switch!")

