"""note のヘッダー画像（1920×1006）。X のヘッダーと同じデザイン。
note はスマホで左右が切れるので、文字は中央寄せにしている。"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1006
paper, ink, muted, tag, tagink = "#fbfaf6", "#1d2433", "#5d6576", "#ffd84d", "#3a2e00"
B = "C:/Windows/Fonts/BIZ-UDGothicB.ttc"
R = "C:/Windows/Fonts/BIZ-UDGothicR.ttc"
f = lambda p, s: ImageFont.truetype(p, s)

img = Image.new("RGB", (W, H), paper)
d = ImageDraw.Draw(img)
d.rectangle([0, 0, W, 20], fill=tag)
cx = W / 2
d.text((cx, 300), "58枚×3パックと64枚×4パック、", font=f(R, 52), fill=muted, anchor="mm")
d.text((cx, 410), "どっちが安い？", font=f(B, 120), fill=ink, anchor="mm")
ans, af = "1枚あたりの値段で比べます", f(B, 76)
bx = d.textbbox((cx, 560), ans, font=af, anchor="mm")
d.rectangle([bx[0] - 6, bx[1] + (bx[3] - bx[1]) * 0.55, bx[2] + 6, bx[3] + 10], fill=tag)
d.text((cx, 560), ans, font=af, fill=ink, anchor="mm")
d.text((cx, 690), "楽天・Yahoo!ショッピングを毎日チェック。安い日にLINEでお知らせ（無料）", font=f(R, 38), fill=muted, anchor="mm")
img.save(os.path.join(HERE, "note_header.png"), optimize=True)
