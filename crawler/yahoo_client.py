"""Yahoo! Shopping Item Search API クライアント。"""
import os
import time
import requests
from parser import extract_count

ENDPOINT = "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"
APP_ID = os.environ.get("YAHOO_APP_ID", "")


def search(query: str, hits: int = 100) -> list[dict]:
    """
    商品を検索して価格・枚数・URLのリストを返す。
    1リクエスト最大100件、ページネーションで最大500件取得。
    """
    if not APP_ID:
        raise EnvironmentError("YAHOO_APP_ID が設定されていません")

    results = []
    start = 1

    while start <= 201:  # 最大200件（2ページ）
        params = {
            "appid": APP_ID,
            "query": query,
            "hits": hits,
            "start": start,
            "sort": "-price",
        }
        resp = requests.get(ENDPOINT, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        batch = data.get("hits", [])
        if not batch:
            break

        for item in batch:
            count = extract_count(item.get("name", ""))
            if count is None:
                continue
            price = item.get("price")
            if not price:
                continue
            results.append({
                "name": item["name"],
                "price": int(price),
                "count": count,
                "per_unit": round(int(price) / count, 2),
                "url": item.get("url", ""),
                "seller": item.get("seller", {}).get("name", ""),
                "image": item.get("image", {}).get("small", ""),
                "source": "yahoo",
            })

        total = data.get("totalResultsAvailable", 0)
        if start + hits > min(total, 500):
            break
        start += hits
        time.sleep(2)  # API レートリミット対策

    return results
