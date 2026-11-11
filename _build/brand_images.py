"""Regenerates assets/og-default.png (1200x630) and assets/apple-touch-icon.png (180x180) in the amber theme."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets"))
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BG = (10, 15, 20); ACC = "#ffb020"; ACC_L = (255, 201, 102); ACC_D = (232, 137, 12)

def fridge(dr, x, y, w, h, grad_img=None):
    r = int(w * .22)
    dr.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=ACC)
    dr.rectangle([x, y + int(h * .36), x + w, y + int(h * .36) + max(3, int(h * .045))], fill=BG)
    hw = max(4, int(w * .1))
    dr.rounded_rectangle([x + int(w * .15), y + int(h * .1), x + int(w * .15) + hw, y + int(h * .28)], radius=hw // 2, fill=BG)
    dr.rounded_rectangle([x + int(w * .15), y + int(h * .48), x + int(w * .15) + hw, y + int(h * .76)], radius=hw // 2, fill=BG)

def gradient_fridge(size, box):
    """amber vertical gradient fridge body as an RGBA layer"""
    x, y, w, h = box
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    grad = Image.new("RGBA", (w, h))
    gd = ImageDraw.Draw(grad)
    for i in range(h):
        t = i / max(1, h - 1)
        c = tuple(int(ACC_L[k] + (ACC_D[k] - ACC_L[k]) * t) for k in range(3)) + (255,)
        gd.line([(0, i), (w, i)], fill=c)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=int(w * .22), fill=255)
    layer.paste(grad, (x, y), mask)
    d = ImageDraw.Draw(layer)
    d.rectangle([x, y + int(h * .36), x + w, y + int(h * .36) + max(3, int(h * .045))], fill=BG + (255,))
    hw = max(4, int(w * .1))
    d.rounded_rectangle([x + int(w * .15), y + int(h * .1), x + int(w * .15) + hw, y + int(h * .28)], radius=hw // 2, fill=BG + (255,))
    d.rounded_rectangle([x + int(w * .15), y + int(h * .48), x + int(w * .15) + hw, y + int(h * .76)], radius=hw // 2, fill=BG + (255,))
    return layer

# OG image
W, H = 1200, 630
im = Image.new("RGBA", (W, H), BG + (255,))
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
gd.ellipse([-500, -700, 700, 520], fill=(255, 150, 20, 70))
glow = glow.filter(ImageFilter.GaussianBlur(140))
im = Image.alpha_composite(im, glow)
im = Image.alpha_composite(im, gradient_fridge((W, H), (110, 165, 200, 300)))
dr = ImageDraw.Draw(im)
dr.text((375, 185), "FRIDGE", font=ImageFont.truetype(F, 124), fill=ACC)
dr.text((378, 335), "Roblox Codes & Guides", font=ImageFont.truetype(F, 46), fill=(230, 238, 245))
dr.text((378, 405), "Codes · Guides · Events · Tips", font=ImageFont.truetype(F, 30), fill=(159, 179, 196))
im.convert("RGB").save(os.path.join(OUT, "og-default.png"), optimize=True)

# Apple touch icon
S = 180
ic = Image.new("RGBA", (S, S), BG + (255,))
ic = Image.alpha_composite(ic, gradient_fridge((S, S), (48, 14, 84, 152)))
ic.convert("RGB").save(os.path.join(OUT, "apple-touch-icon.png"), optimize=True)
print("ok")
