"""SQLite による価格データの保存・集計。"""
import sqlite3
from contextlib import contextmanager
from datetime import date, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / "prices.db"


@contextmanager
def conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    try:
        yield c
        c.commit()
    finally:
        c.close()


def init():
    with conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                date        TEXT NOT NULL,
                item_id     TEXT NOT NULL,
                source      TEXT NOT NULL,
                name        TEXT NOT NULL,
                price       INTEGER NOT NULL,
                count       INTEGER NOT NULL,
                per_unit    REAL NOT NULL,
                url         TEXT,
                seller      TEXT,
                image       TEXT,
                created_at  TEXT DEFAULT (datetime('now','localtime'))
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_date_item ON prices(date, item_id)")


def save_prices(today: str, item_id: str, rows: list[dict]):
    # 同じ日・同じ item_id は洗い替え
    with conn() as c:
        c.execute("DELETE FROM prices WHERE date=? AND item_id=?", (today, item_id))
        c.executemany(
            """INSERT INTO prices (date, item_id, source, name, price, count, per_unit, url, seller, image)
               VALUES (:date, :item_id, :source, :name, :price, :count, :per_unit, :url, :seller, :image)""",
            [{"date": today, "item_id": item_id, **r} for r in rows],
        )


def get_percentile(item_id: str, pct: float, days: int = 30) -> float | None:
    """過去 days 日の per_unit の下から pct% 目の値を返す（安い基準の計算に使う）。"""
    since = (date.today() - timedelta(days=days)).isoformat()
    with conn() as c:
        rows = c.execute(
            "SELECT per_unit FROM prices WHERE item_id=? AND date>=? ORDER BY per_unit",
            (item_id, since),
        ).fetchall()
    if not rows:
        return None
    idx = max(0, int(len(rows) * pct / 100) - 1)
    return rows[idx]["per_unit"]


def get_today_best(today: str, item_id: str) -> dict | None:
    """今日の最安値1件を返す。"""
    with conn() as c:
        row = c.execute(
            "SELECT * FROM prices WHERE date=? AND item_id=? ORDER BY per_unit LIMIT 1",
            (today, item_id),
        ).fetchone()
    return dict(row) if row else None


def get_30day_median(item_id: str) -> float | None:
    """過去30日の1枚あたり中央値。"""
    return get_percentile(item_id, 50, days=30)
