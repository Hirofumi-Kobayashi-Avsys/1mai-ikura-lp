"""LINE Messaging API でブロードキャスト通知を送る。"""
import os
import requests

LINE_API = "https://api.line.me/v2/bot/message"
TOKEN = os.environ.get("LINE_CHANNEL_TOKEN", "")


def _headers():
    return {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}


def send_price_alert(item_label: str, per_unit: float, discount_pct: float, url: str):
    """価格下落を友だち全員に通知する。"""
    if not TOKEN:
        raise EnvironmentError("LINE_CHANNEL_TOKEN が設定されていません")

    text = (
        f"🏷️ {item_label} が安くなりました\n"
        f"\n"
        f"1枚 {per_unit:.1f}円\n"
        f"いつもより約{discount_pct:.0f}%安い\n"
        f"\n"
        f"{url}"
    )

    resp = requests.post(
        f"{LINE_API}/broadcast",
        headers=_headers(),
        json={"messages": [{"type": "text", "text": text}]},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.status_code
