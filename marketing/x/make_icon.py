from PIL import Image, ImageDraw, ImageFont
S = 800
img = Image.new("RGB", (S, S), "#ffd84d")
d = ImageDraw.Draw(img)
ink = "#3a2e00"
big = ImageFont.truetype("C:/Windows/Fonts/BIZ-UDGothicB.ttc", 300)
small = ImageFont.truetype("C:/Windows/Fonts/BIZ-UDGothicB.ttc", 150)
d.text((S/2, S*0.40), "1枚", font=big, fill=ink, anchor="mm")
d.text((S/2, S*0.71), "いくら", font=small, fill=ink, anchor="mm")
import os; img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "x_avatar.png"))
