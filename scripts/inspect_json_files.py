import sys, json
sys.stdout.reconfigure(encoding='utf-8')

for fname in ['scripts/distinct_verified.json', 'scripts/perfect_matched_products.json']:
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            d = json.load(f)
            print(f"{fname}: {len(d)} items")
            if len(d) > 0:
                print("First item keys:", list(d[0].keys()))
                print("Sample name:", d[0].get('name') or d[0].get('raw_title'))
    except Exception as e:
        print(f"{fname} error: {e}")

