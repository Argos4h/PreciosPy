import sys
sys.stdout.reconfigure(encoding='utf-8')

for fname in ['scripts/test_location_based_supermarkets.py', 'scripts/test_split_keeps_selected_top.py', 'scripts/test_split_breakdown.py']:
    with open(fname, 'r', encoding='utf-8') as f:
        text = f.read()
    import re
    asserts = [m.start() for m in re.finditer(r'assert ', text)]
    print(f"{fname}: {len(asserts)} asserts")
    for a in asserts:
        print("  ", text[a:a+100].replace('\n', ' '))

