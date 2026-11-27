"""商品名から1セットの枚数を抽出する。"""
import re


def extract_count(name: str) -> int | None:
    """
    商品名から合計枚数を返す。解析できない場合は None。

    対応パターン例:
      "54枚×3パック"  → 162
      "44枚入り×4個"  → 176
      "176枚"         → 176
      "54枚(3パック)" → 162
    """
    name = name.replace("×", "x").replace("✕", "x").replace("ｘ", "x").replace("*", "x").replace("＊", "x")

    # "N枚 x M パック/個/袋/セット"
    m = re.search(r"(\d+)\s*枚\s*[xX]\s*(\d+)\s*(?:パック|個|袋|セット|P)", name)
    if m:
        return int(m.group(1)) * int(m.group(2))

    # "N枚入り x M個" / "N枚入×M"
    m = re.search(r"(\d+)\s*枚入[りリ]?\s*[xX]\s*(\d+)", name)
    if m:
        return int(m.group(1)) * int(m.group(2))

    # "(N枚 x M)" など括弧内
    m = re.search(r"[（(](\d+)\s*枚\s*[xX]\s*(\d+)[)）]", name)
    if m:
        return int(m.group(1)) * int(m.group(2))

    # 単体: "176枚" "176枚入" — セットなしの大袋
    m = re.search(r"(\d+)\s*枚(?:入[りリ]?)?(?:\s|$|[^x×✕])", name)
    if m:
        return int(m.group(1))

    return None
