import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove 2.0 PRO badge in header
old_badge = '<span class="text-[10px] px-1.5 py-0.5 rounded-full font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">2.0 PRO</span>'
assert old_badge in content, "old_badge not found"
content = content.replace(old_badge, '')

# 2. Update title: PreciosPy 2.0 -> PreciosPy
content = content.replace('<title>PreciosPy 2.0 — Rediseño Mundial & Billetera de Tarjetas</title>', '<title>PreciosPy — Comparador de Supermercados & Billetera de Ahorro</title>')

# 3. Clean any WhatsApp messages or titles saying "PreciosPy 2.0" -> "PreciosPy"
content = content.replace('PreciosPy 2.0', 'PreciosPy')

with open('scripts/build_html.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed '2.0 PRO' and updated titles in build_html.py!")
