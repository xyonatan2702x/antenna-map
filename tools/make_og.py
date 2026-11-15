"""Build og-image.png (1200x630) for einklita.co.il. Run from the repo root: python3 tools/make_og.py"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG, CYAN, WHITE, LIGHT = '#1a1a2e', '#00B4CC', '#ffffff', '#cfe8ee'
B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
R = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
im = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(im)

def center(text, y, font, fill):
    w = d.textlength(text, font=font, direction='rtl')
    d.text(((W - w) / 2, y), text, font=font, fill=fill, direction='rtl')

center('אין קליטה  ·  einklita.co.il', 36, ImageFont.truetype(B, 30), CYAN)
center('אין קליטה בבית?', 100, ImageFont.truetype(B, 92), WHITE)
center('בדקו אילו אנטנות יש ליד הכתובת שלכם', 222, ImageFont.truetype(R, 44), LIGHT)

lf = ImageFont.truetype(B, 30)
items = [('פרטנר', '#00B4CC'), ('פלאפון', '#3B8FE0'), ('סלקום', '#C05BD6')]
x = 880
for name, col in items:  # right to left
    d.ellipse((x - 13, 313, x + 13, 339), fill=col)
    w = d.textlength(name, font=lf, direction='rtl')
    d.text((x - 24 - w, 306), name, font=lf, fill=WHITE, direction='rtl')
    x -= 215

cx, cy = 600, 600
for r in (75, 135, 195):
    d.arc((cx - r, cy - r, cx + r, cy + r), 210, 330, fill=CYAN, width=7)
d.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=CYAN)
# "no signal": a slash across the arcs
d.line((cx - 150, cy - 230, cx + 150, cy - 10), fill='#ff5a6e', width=10)
im.save('og-image.png', optimize=True)
