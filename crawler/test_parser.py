"""枚数パーサーの動作確認。"""
from parser import extract_count

cases = [
    ("パンパース パンツ Lサイズ 44枚×4パック", 176),
    ("グーン パンツ M 54枚×3パック", 162),
    ("メリーズ パンツL 58枚入り×4個", 232),
    ("ムーニー テープ Lサイズ(76枚×2パック)", 152),
    ("ムーニー パンツ Mサイズ 176枚", 176),
    ("パンパース パンツ ビッグ 44枚入×4P", 176),
    ("おむつ", None),
]

for name, expected in cases:
    result = extract_count(name)
    status = "OK" if result == expected else "NG"
    print(f"{status}  {str(result):>5}  {name}")
