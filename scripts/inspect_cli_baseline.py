import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scraper/src/precios_py/cli.py', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('baseline_offers =')
if idx != -1:
    print(text[idx:idx+3000])

