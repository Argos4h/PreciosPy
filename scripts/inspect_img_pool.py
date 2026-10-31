import json, re

with open('scripts/distinct_verified.json', 'r', encoding='utf-8') as f:
    d40 = json.load(f)

img_pool = [it['image'] for it in d40 if it.get('image')]
print(f"Distinct verified images: {len(img_pool)}")
for img in img_pool[:10]:
    print(" ", img)

