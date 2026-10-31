import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

vc_idx = text.find('id="viewCart"')
print(text[vc_idx:vc_idx + 1800])

