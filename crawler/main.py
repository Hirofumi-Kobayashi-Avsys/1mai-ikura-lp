"""
毎日1回実行するバッチ。
  1. 全対象商品を Yahoo! Shopping API で検索
  2. 1枚あたりの値段を計算してDBに保存
  3. 過去30日の中央値より安ければ通知候補としてログに出力（通知は後で実装）
"""
import logging
import os
from datetime import date

from dotenv import load_dotenv
load_dotenv()

import db
import yahoo_client
from items import ITEMS

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# 中央値より何%安ければ通知するか
NOTIFY_THRESHOLD = float(os.environ.get("NOTIFY_THRESHOLD", "0.90"))  # デフォルト10%安


def run():
    db.init()
    today = date.today().isoformat()
    log.info("クロール開始: %s", today)

    notify_candidates = []

    for item in ITEMS:
        log.info("[%s] 検索中...", item["label"])
        try:
            rows = yahoo_client.search(item["query_yahoo"])
        except Exception as e:
            log.error("[%s] Yahoo! API エラー: %s", item["label"], e)
            continue

        # 枚数の範囲フィルタ（異サイズ除外）
        rows = [r for r in rows if item["count_min"] <= r["count"] <= item["count_max"]]

        if not rows:
            log.warning("[%s] 該当商品なし", item["label"])
            continue

        db.save_prices(today, item["id"], rows)

        best = min(rows, key=lambda r: r["per_unit"])
        median = db.get_30day_median(item["id"])
        log.info(
            "[%s] 最安値 %.1f円/枚（%s）| 30日中央値 %s",
            item["label"],
            best["per_unit"],
            best["seller"],
            f"{median:.1f}円" if median else "データなし",
        )

        if median and best["per_unit"] <= median * NOTIFY_THRESHOLD:
            notify_candidates.append({
                "item": item,
                "best": best,
                "median": median,
                "discount_pct": round((1 - best["per_unit"] / median) * 100, 1),
            })

    if notify_candidates:
        log.info("=== 通知候補 %d件 ===", len(notify_candidates))
        for c in notify_candidates:
            log.info(
                "  %s: %.1f円/枚（中央値より%.1f%%安）%s",
                c["item"]["label"],
                c["best"]["per_unit"],
                c["discount_pct"],
                c["best"]["url"],
            )
    else:
        log.info("通知候補なし（全品目、閾値以下の安値なし）")

    log.info("クロール完了")


if __name__ == "__main__":
    run()
