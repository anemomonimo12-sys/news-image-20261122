#!/usr/bin/env python3
"""Render entry.png: the world news of Sunday 22 November 2026 in one picture.

Drawn programmatically with PIL (flat newspaper-front-page style): a masthead
naming the day, six story panels across regions and beats, and an "also
today" strip. Stories as reported on 22 Nov 2026 by the day's news services:
COP31 overtime in Antalya, Iran's strike on Bahrain, Kryvyi Rih bombed and a
Russian ship struck, the capture of 'El Chapo Isidro' in Sinaloa, the
Trump-Xi-Putin meeting in Shenzhen, and the AI sell-off on Wall Street.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 246, 238)
INK = (20, 30, 52)
GRAY = (74, 80, 92)
RED = (178, 34, 44)
WHITE = (255, 255, 255)
BORDER = (20, 30, 52)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF_I = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def centered(draw, y, text, fnt, fill):
    w_ = draw.textlength(text, font=fnt)
    draw.text(((W - w_) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


# ---------- icons (drawn in a 96x96 box at x, y) ----------

def icon_sun_factory(d, x, y):
    d.ellipse([x + 52, y + 4, x + 88, y + 40], fill=(243, 156, 18))
    for a in range(0, 360, 45):
        cx, cy = x + 70, y + 22
        x1, y1 = cx + 22 * math.cos(math.radians(a)), cy + 22 * math.sin(math.radians(a))
        x2, y2 = cx + 28 * math.cos(math.radians(a)), cy + 28 * math.sin(math.radians(a))
        d.line([x1, y1, x2, y2], fill=(243, 156, 18), width=3)
    d.rectangle([x + 6, y + 62, x + 62, y + 90], fill=INK)
    d.rectangle([x + 14, y + 44, x + 24, y + 62], fill=INK)
    d.rectangle([x + 34, y + 38, x + 44, y + 62], fill=INK)
    for (sx, sy, r) in [(19, 34, 6), (24, 26, 8), (39, 28, 7), (45, 20, 9)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r], fill=(160, 166, 178))


def icon_flame(d, x, y):
    d.polygon([(x + 48, y + 6), (x + 66, y + 38), (x + 78, y + 56),
               (x + 72, y + 80), (x + 56, y + 90), (x + 38, y + 90),
               (x + 24, y + 78), (x + 20, y + 54), (x + 32, y + 34)],
              fill=(211, 84, 0))
    d.polygon([(x + 48, y + 34), (x + 60, y + 54), (x + 62, y + 70),
               (x + 52, y + 84), (x + 40, y + 82), (x + 32, y + 68),
               (x + 38, y + 50)], fill=(243, 156, 18))
    d.ellipse([x + 40, y + 62, x + 56, y + 86], fill=(250, 220, 130))


def icon_ship(d, x, y):
    d.polygon([(x + 12, y + 52), (x + 84, y + 52), (x + 74, y + 72), (x + 24, y + 72)], fill=INK)
    d.rectangle([x + 40, y + 34, x + 62, y + 52], fill=INK)
    d.rectangle([x + 46, y + 24, x + 54, y + 34], fill=INK)
    d.line([x + 20, y + 20, x + 32, y + 30], fill=RED, width=4)
    d.line([x + 32, y + 20, x + 20, y + 30], fill=RED, width=4)
    for i, wy in enumerate((80, 88)):
        pts = []
        for px in range(8, 90, 4):
            pts.append((x + px, y + wy + 3 * math.sin((px + i * 9) / 7.0)))
        d.line(pts, fill=(41, 128, 185), width=3)


def icon_badge(d, x, y):
    d.ellipse([x + 14, y + 8, x + 82, y + 88], fill=(212, 172, 13), outline=INK, width=3)
    cx, cy, r1, r2 = x + 48, y + 48, 26, 11
    pts = []
    for i in range(10):
        r = r1 if i % 2 == 0 else r2
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=WHITE)


def icon_atom(d, x, y):
    layer = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse([8, 34, 88, 62], outline=(26, 82, 118, 255), width=4)
    for ang in (60, 120):
        rot = layer.rotate(ang, resample=Image.BICUBIC, center=(48, 48))
        d.bitmap((x, y), rot.split()[3], fill=(26, 82, 118))
    d.bitmap((x, y), layer.split()[3], fill=(26, 82, 118))
    d.ellipse([x + 41, y + 41, x + 55, y + 55], fill=RED)


def icon_chart(d, x, y):
    d.line([x + 14, y + 10, x + 14, y + 78], fill=INK, width=3)
    d.line([x + 14, y + 78, x + 88, y + 78], fill=INK, width=3)
    pts = [(x + 18, y + 24), (x + 36, y + 34), (x + 50, y + 28), (x + 66, y + 50), (x + 84, y + 66)]
    d.line(pts, fill=RED, width=5, joint="curve")
    d.polygon([(x + 84, y + 66), (x + 70, y + 64), (x + 82, y + 52)], fill=RED)


# ---------- page ----------

PANELS = [
    ("CLIMATE · ANTALYA, TÜRKIYE", (46, 125, 50),
     "COP31 deadlocked on fossil fuels",
     "UN climate summit runs into a second day of overtime.",
     icon_sun_factory),
    ("MIDDLE EAST · BAHRAIN", (178, 34, 44),
     "Iran strikes site in Bahrain",
     "Missiles hit Bahrain as Gulf tensions flare once more.",
     icon_flame),
    ("EUROPE · UKRAINE", (26, 82, 118),
     "Missiles hit Kryvyi Rih",
     "Zelensky's hometown; a Russian ship ablaze.",
     icon_ship),
    ("AMERICAS · SINALOA, MEXICO", (110, 44, 145),
     "Cartel boss 'Chapo Isidro' captured",
     "FBI Most Wanted fugitive seized; 11 die in violence.",
     icon_badge),
    ("DIPLOMACY · SHENZHEN, CHINA", (146, 108, 0),
     "Trump, Xi, Putin meet in Shenzhen",
     "The leaders agree to open nuclear risk-reduction talks.",
     icon_atom),
    ("ECONOMY · NEW YORK", (14, 102, 85),
     "US stocks fall into correction",
     "AI shares slide, dragging the Dow and S&P 500 lower.",
     icon_chart),
]

ALSO = ("ALSO TODAY: EU–Indonesia trade deal signed · M6.9 quake hits Peru · "
        "UN moves on autonomous weapons · Swimmer crosses the Strait of Hormuz")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead (date auto-fitted to the content width)
    centered(d, 34, "S U N D A Y", font(SANS_B, 30), RED)
    size = 110
    while d.textlength("22 NOVEMBER 2026", font=font(SERIF_B, size)) > W - 80:
        size -= 2
    centered(d, 76, "22 NOVEMBER 2026", font(SERIF_B, size), INK)
    centered(d, 196, "The world's news of the day, in one picture", font(SERIF_I, 31), GRAY)
    d.rectangle([40, 240, W - 40, 246], fill=INK)
    d.rectangle([40, 250, W - 40, 252], fill=INK)

    # panels: 2 cols x 3 rows; text column left, icon column right
    px0, py0, pw, ph, gap = 40, 268, 462, 196, 20
    text_w = pw - 150
    f_kick, f_head, f_sum = font(SANS_B, 19), font(SANS_B, 29), font(SANS, 21)
    for i, (kicker, color, head, summ, icon) in enumerate(PANELS):
        x = px0 + (i % 2) * (pw + gap)
        y = py0 + (i // 2) * (ph + 14)
        d.rectangle([x, y, x + pw, y + ph], fill=WHITE, outline=BORDER, width=2)
        # kicker chip
        kw = d.textlength(kicker, font=f_kick) + 22
        d.rectangle([x + 16, y + 14, x + 16 + kw, y + 46], fill=color)
        d.text((x + 27, y + 20), kicker, font=f_kick, fill=WHITE)
        # icon, vertically centred in the right column
        icon(d, x + pw - 118, y + (ph - 96) // 2)
        # headline + summary
        lines = wrap(d, head, f_head, text_w)
        ty = y + 56
        for ln in lines[:2]:
            d.text((x + 16, ty), ln, font=f_head, fill=INK)
            ty += 36
        for ln in wrap(d, summ, f_sum, text_w)[:2]:
            d.text((x + 16, ty + 4), ln, font=f_sum, fill=GRAY)
            ty += 28

    # also-today strip
    sy = 896
    d.rectangle([40, sy, W - 40, sy + 3], fill=RED)
    f_also = font(SANS, 22)
    lines = wrap(d, ALSO, f_also, W - 80)
    ty = sy + 12
    for ln in lines[:2]:
        centered(d, ty, ln, f_also, INK)
        ty += 29
    centered(d, 986, "Stories as reported on Sunday 22 November 2026",
             font(SANS, 17), GRAY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
