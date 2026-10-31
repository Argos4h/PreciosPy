import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('function renderGrid')
end = text.find('function openProductDetail', start)
print(text[start:end])

