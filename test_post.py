import requests, json, time
time.sleep(2)
try:
    r = requests.post('http://localhost:5000/ask', json={'query':'Meri wheat pe rust aa gaya hai','language':'auto'}, timeout=10)
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))
except Exception as e:
    print('ERROR', e)
