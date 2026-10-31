import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'renderGrid|selectedSupermarket|filterSupermarket|selectSupermarket', text):
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 250)
    print('---')
    print(text[start:end])

