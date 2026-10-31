# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('preciospy_redesign_2026.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check if '\${' exists in generated html
print("Count of '\\${' in html:", html.count('\\${'))
print("Count of '${' in html:", html.count('${'))
print("Contains renderSplitBreakdown:", 'renderSplitBreakdown' in html)
print("Contains officialUrl:", 'officialUrl' in html)

