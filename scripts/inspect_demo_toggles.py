with open('precios_py_demo.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = list(re.finditer(r'toggleBankProfile', text))
print(f'Total occurrences of toggleBankProfile: {len(matches)}')
for i, m in enumerate(matches):
    start = max(0, m.start() - 200)
    end = min(len(text), m.end() + 200)
    print(f'=== OCCURRENCE {i+1} ===')
    print(text[start:end])

