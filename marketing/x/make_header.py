from PIL import Image, ImageDraw, ImageFont
W, H = 1500, 500
paper, ink, muted, tag, tagink, good, rule = "#fbfaf6", "#1d2433", "#5d6576", "#ffd84d", "#3a2e00", "#1f8a5b", "#e3e1d8"
B = "C:/Windows/Fonts/BIZ-UDGothicB.ttc"; R = "C:/Windows/Fonts/BIZ-UDGothicR.ttc"
f = lambda p, s: ImageFont.truetype(p, s)
img = Image.new("RGB", (W, H), paper)
d = ImageDraw.Draw(img)
d.rectangle([0, 0, W, 12], fill=tag)

# 左〜中央：キャッチ（X のアイコンが左下に重なるので、左端は上寄せ）
x0 = 380
d.text((x0, 110), "58枚×3パックと64枚×4パック、", font=f(R, 34), fill=muted)
d.text((x0, 160), "どっちが安い？", font=f(B, 72), fill=ink)
# 黄色マーカー付きの答え
ans = "1枚あたりの値段で比べます"
af = f(B, 46)
bx = d.textbbox((x0, 270), ans, font=af)
d.rectangle([bx[0]-4, bx[1]+(bx[3]-bx[1])*0.55, bx[2]+4, bx[3]+6], fill=tag)
d.text((x0, 270), ans, font=af, fill=ink)
d.text((x0, 350), "楽天・Yahoo!ショッピングを毎日チェック。安い日にLINEでお知らせ（無料）", font=f(R, 24), fill=muted)

# 右：値札
cx, cy = 1350, 230
tagbox = [cx-100, cy-110, cx+100, cy+110]
d.rounded_rectangle(tagbox, radius=28, fill=tag)
d.ellipse([cx-12, cy-92, cx+12, cy-68], fill=paper)
d.text((cx, cy+5), "1枚", font=f(B, 84), fill=tagink, anchor="mm")
d.text((cx, cy+75), "いくら？", font=f(B, 34), fill=tagink, anchor="mm")
import os; img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "x_header.png"))
