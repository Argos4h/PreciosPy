with open('scripts/build_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = list(re.finditer(r'toggleBankProfile', text))
print(f'Total occurrences in scripts/build_html.py: {len(matches)}')
for i, m in enumerate(matches):
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 100)
    print(f'=== OCCURRENCE {i+1} ===')
    print(repr(text[start:end]))

