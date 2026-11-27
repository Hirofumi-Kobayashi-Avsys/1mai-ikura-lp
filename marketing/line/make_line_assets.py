"""LINE 公式アカウント用の画像を作る（リッチメニュー・友だち追加QR）。"""
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
paper, ink, muted, tag, tagink, good, rule = "#fbfaf6", "#1d2433", "#5d6576", "#ffd84d", "#3a2e00", "#1f8a5b", "#e3e1d8"
B = "C:/Windows/Fonts/BIZ-UDGothicB.ttc"
R = "C:/Windows/Fonts/BIZ-UDGothicR.ttc"
f = lambda p, s: ImageFont.truetype(p, s)
ADD_URL = "https://line.me/R/ti/p/@667eogtp"


def richmenu():
    # LINE のリッチメニュー（小）: 2500×843 を3分割
    W, H = 2500, 843
    img = Image.new("RGB", (W, H), paper)
    d = ImageDraw.Draw(img)
    cols = [
        ("しくみを見る", "1枚いくら？の計算", tag, tagink),
        ("お知らせの見本", "どんな通知が届く？", "#ffffff", ink),
        ("友だちに教える", "LINEで紹介する", good, "#ffffff"),
    ]
    w = W / 3
    for i, (title, sub, bg, fg) in enumerate(cols):
        x0, x1 = int(i * w), int((i + 1) * w)
        d.rectangle([x0, 0, x1, H], fill=bg)
        if i:
            d.line([x0, 60, x0, H - 60], fill=rule, width=6)
        cx = (x0 + x1) / 2
        d.text((cx, H * 0.42), title, font=f(B, 100), fill=fg, anchor="mm")
        d.text((cx, H * 0.66), sub, font=f(R, 64), fill=fg, anchor="mm")
    d.rectangle([0, 0, W, 14], fill=tag)
    img.save(os.path.join(HERE, "richmenu.png"), optimize=True)


def qr():
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=20, border=2)
    q.add_data(ADD_URL)
    q.make(fit=True)
    code = q.make_image(fill_color=ink, back_color="white").convert("RGB")
    W = code.width + 120
    H = code.height + 260
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 16], fill=tag)
    d.text((W / 2, 90), "「1枚いくら」をLINEで友だち追加", font=f(B, 46), fill=ink, anchor="mm")
    img.paste(code, (60, 150))
    d.text((W / 2, H - 55), "スマホのカメラで読み取ってください", font=f(R, 36), fill=muted, anchor="mm")
    img.save(os.path.join(HERE, "line_qr.png"), optimize=True)
    # LP 用：文字なしのQRだけ
    q2 = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=2)
    q2.add_data(ADD_URL)
    q2.make(fit=True)
    q2.make_image(fill_color=ink, back_color="white").save(os.path.join(HERE, "line_qr_plain.png"), optimize=True)


if __name__ == "__main__":
    richmenu()
    qr()
