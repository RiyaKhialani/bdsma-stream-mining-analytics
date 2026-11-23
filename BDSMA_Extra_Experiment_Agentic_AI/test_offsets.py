import urllib.request
import json

for offset in [0, 20, 50, 80, 100, 150, 200, 500, 1000]:
    url = f"https://datasets-server.huggingface.co/rows?dataset=mb7419%2Fcareer-guidance-reddit&config=default&split=train&offset={offset}&limit=10"
    req = urllib.request.Request(url, headers={"User-Agent": "BDSMA-Agent/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode("utf-8"))
            print(f"Offset {offset}: SUCCESS, {len(data['rows'])} rows")
    except Exception as e:
        print(f"Offset {offset}: FAILED ({e})")
