import os, time
from dotenv import load_dotenv
load_dotenv()
import requests
from parser import extract_count

time.sleep(60)

r = requests.get(
    'https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch',
    params={'appid': os.environ['YAHOO_APP_ID'], 'query': 'グーン パンツ M', 'hits': 10, 'start': 1, 'sort': '-price'},
    timeout=15
)
print('Status:', r.status_code)
if r.status_code == 200:
    hits = r.json().get('hits', [])
    print(f'件数: {len(hits)}')
    for item in hits[:5]:
        name = item.get('name', '')
        price = item.get('price', 0)
        count = extract_count(name)
        if count:
            print(f'{price}円/{count}枚={price/count:.1f}円/枚  {name[:40]}')
else:
    print(r.text[:500])
