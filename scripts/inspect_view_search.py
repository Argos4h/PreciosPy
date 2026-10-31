import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

vs_idx = text.find('id="viewSearch"')
print(text[vs_idx:vs_idx + 1200])

