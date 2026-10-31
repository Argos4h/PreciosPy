import urllib.request, json

url = 'https://api.app.biggie.com.py/api/articles?take=5&skip=0'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = json.loads(resp.read().decode())
        print('Total items reported by Biggie API:', data.get('total') or len(data.get('items', [])))
        for it in data.get('items', [])[:3]:
            print(f"- {it.get('name')} | Gs. {it.get('price')} | EAN: {it.get('cbaCode')}")
except Exception as e:
    print('Error connecting:', e)

