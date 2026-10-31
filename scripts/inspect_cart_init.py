import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('let cart =')
if idx != -1:
    print(text[idx:idx+500])

