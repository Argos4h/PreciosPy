import os

for root, dirs, files in os.walk('scraper'):
    for f in files:
        p = os.path.join(root, f)
        print(f"{p} ({os.path.getsize(p)} bytes)")

