"""Minimal line-art textile illustrations + fabric swatch textures, brand colours only.
Every icon is drawn in a 1000x1000 box at 2x and scaled down (smooth lines)."""
import math
from PIL import Image, ImageDraw
import brand
SKY, WHITE, BLUE, NAVY = brand.SKY, brand.WHITE, brand.BLUE, brand.NAVY
LW = 14

def _c(d, box, **k): d.ellipse(box, **k)

def cone(d):
    d.polygon([(330, 860), (670, 860), (585, 160), (415, 160)], outline=WHITE, width=LW)
    for y in range(240, 840, 70):
        t = (y - 160) / 700; xl = 415 - 85 * t; xr = 585 + 85 * t
        d.line([(xl + 18, y), (xr - 18, y + 30)], fill=SKY, width=6)
    d.rectangle([460, 110, 540, 160], outline=SKY, width=LW)

def cheese(d):
    for x in (300, 700):
        _c(d, [x - 170, 300, x + 170, 700], outline=WHITE, width=LW); _c(d, [x - 50, 450, x + 50, 550], outline=SKY, width=LW)
    d.line([(300, 300), (700, 300)], fill=WHITE, width=LW); d.line([(300, 700), (700, 700)], fill=WHITE, width=LW)

def loom(d):
    d.rectangle([140, 300, 860, 800], outline=WHITE, width=LW)
    d.line([(140, 470), (860, 470)], fill=SKY, width=LW)
    for x in range(200, 820, 40): d.line([(x, 300), (x, 470)], fill=SKY, width=5)
    _c(d, [420, 520, 580, 680], outline=WHITE, width=LW); d.line([(500, 520), (500, 300)], fill=WHITE, width=8)
    d.line([(140, 800), (100, 900)], fill=WHITE, width=LW); d.line([(860, 800), (900, 900)], fill=WHITE, width=LW)
    _c(d, [200, 180, 300, 280], outline=SKY, width=10); _c(d, [700, 180, 800, 280], outline=SKY, width=10)
    d.line([(250, 280), (250, 300)], fill=SKY, width=8); d.line([(750, 280), (750, 300)], fill=SKY, width=8)

def knitting(d):  # circular knitting machine
    _c(d, [200, 380, 800, 520], outline=WHITE, width=LW)
    d.line([(200, 450), (230, 760)], fill=WHITE, width=LW); d.line([(800, 450), (770, 760)], fill=WHITE, width=LW)
    d.arc([230, 690, 770, 830], 0, 180, fill=WHITE, width=LW)
    for k in range(6):
        a = math.pi * 2 * k / 6; x = 500 + math.cos(a) * 250; y = 230 + math.sin(a) * 50
        d.polygon([(x - 28, y + 40), (x + 28, y + 40), (x + 16, y - 50), (x - 16, y - 50)], outline=SKY, width=6)
        d.line([(x, y + 40), (500 + math.cos(a) * 120, 430)], fill=SKY, width=4)
    for x in range(260, 760, 60): d.line([(x, 520), (x + 6, 690)], fill=SKY, width=5)

def sock(d):
    return "sock"

def _sock_img():
    from PIL import ImageFilter
    m = Image.new("L", (1000, 1000), 0); md = ImageDraw.Draw(m)
    md.rounded_rectangle([400, 130, 620, 640], radius=30, fill=255)
    md.rounded_rectangle([400, 540, 860, 800], radius=130, fill=255)
    inner = m.filter(ImageFilter.MinFilter(15))
    edge = Image.eval(Image.merge("L", [m]), lambda v: v)
    from PIL import ImageChops
    edge = ImageChops.subtract(m, inner)
    im = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0)); im.paste(WHITE + (255,), (0, 0), edge)
    d = ImageDraw.Draw(im)
    for y in range(180, 300, 32): d.line([(420, y), (600, y)], fill=SKY, width=6)
    d.arc([660, 560, 860, 800], 300, 60, fill=SKY, width=8)
    d.arc([400, 600, 560, 800], 90, 180, fill=SKY, width=8)
    return im

def _old_sock(d):
    d.line([(420, 140), (420, 560)], fill=WHITE, width=LW); d.line([(620, 140), (620, 600)], fill=WHITE, width=LW)
    d.arc([300, 480, 620, 800], 90, 180, fill=WHITE, width=LW)
    d.line([(460, 800), (780, 800)], fill=WHITE, width=LW); d.arc([620, 600, 860, 800], 270, 90, fill=WHITE, width=LW)
    d.line([(420, 140), (620, 140)], fill=WHITE, width=LW)
    for y in range(180, 300, 30): d.line([(430, y), (610, y)], fill=SKY, width=6)
    d.arc([300, 640, 460, 800], 90, 180, fill=SKY, width=8)

def cap(d):
    d.chord([200, 260, 800, 860], 180, 360, outline=WHITE, width=LW)
    d.rectangle([180, 560, 820, 700], outline=WHITE, width=LW)
    for x in range(230, 800, 50): d.line([(x, 575), (x, 685)], fill=SKY, width=6)
    _c(d, [445, 160, 555, 270], outline=SKY, width=LW)

def glove(d):
    d.rounded_rectangle([300, 420, 700, 760], radius=60, outline=WHITE, width=LW)
    for i, (x, top) in enumerate([(340, 220), (430, 170), (520, 180), (610, 240)]):
        d.rounded_rectangle([x, top, x + 70, 450], radius=35, outline=WHITE, width=LW)
    d.rounded_rectangle([170, 470, 330, 560], radius=45, outline=WHITE, width=LW)
    d.rectangle([310, 760, 690, 860], outline=SKY, width=LW)
    for x in range(340, 680, 40): d.line([(x, 770), (x, 850)], fill=SKY, width=5)

def net(d):
    for k in range(-6, 7):
        d.line([(200 + k * 80, 200), (200 + k * 80 + 600, 800)], fill=SKY, width=7)
        d.line([(800 + k * 80, 200), (800 + k * 80 - 600, 800)], fill=SKY, width=7)
    d.rectangle([200, 200, 800, 800], outline=NAVY, width=0)
    m = Image.new("L", (1000, 1000), 0)
    return "mask"

def bedsheet(d):
    for i, c in enumerate((WHITE, SKY, WHITE)):
        y = 300 + i * 150
        d.rounded_rectangle([200 + i * 20, y, 800 - i * 20, y + 120], radius=20, outline=c, width=LW)
    d.line([(240, 360), (760, 360)], fill=SKY, width=5)
    d.line([(260, 660), (740, 660)], fill=SKY, width=5)

def towel(d):
    d.rectangle([330, 150, 670, 850], outline=WHITE, width=LW)
    for y in (260, 740): d.line([(330, y), (670, y)], fill=SKY, width=10)
    for x in range(360, 660, 30): d.line([(x, 850), (x, 900)], fill=SKY, width=5)

def tshirt(d):
    d.polygon([(380, 170), (440, 210), (560, 210), (620, 170), (840, 290), (770, 420), (690, 380), (690, 850), (310, 850), (310, 380), (230, 420), (160, 290)], outline=WHITE, width=LW)
    d.arc([430, 160, 570, 260], 0, 180, fill=SKY, width=LW)

def jeans(d):
    d.polygon([(300, 150), (700, 150), (760, 860), (560, 860), (500, 380), (440, 860), (240, 860)], outline=WHITE, width=LW)
    d.line([(300, 230), (700, 230)], fill=SKY, width=10)
    d.line([(500, 230), (500, 380)], fill=SKY, width=8)

def saree(d):
    d.arc([180, 180, 820, 820], 200, 340, fill=WHITE, width=LW)
    d.polygon([(250, 520), (750, 520), (680, 860), (320, 860)], outline=WHITE, width=LW)
    for y in (560, 600): d.line([(260, y), (740, y)], fill=SKY, width=8)
    for x in range(340, 680, 60): _c(d, [x, 700, x + 24, 724], outline=SKY, width=5)

def carpet(d):
    d.rectangle([180, 260, 820, 740], outline=WHITE, width=LW)
    d.rectangle([260, 340, 740, 660], outline=SKY, width=8)
    d.polygon([(500, 400), (620, 500), (500, 600), (380, 500)], outline=WHITE, width=8)
    for x in range(200, 820, 40): d.line([(x, 740), (x, 790)], fill=SKY, width=5); d.line([(x, 210), (x, 260)], fill=SKY, width=5)

def swatch_icon(d):
    for i, c in enumerate((SKY, WHITE, SKY)):
        o = i * 70; d.rounded_rectangle([220 + o, 220 + o, 640 + o, 640 + o], radius=30, outline=c, width=LW, fill=NAVY)
    for k in range(6): d.line([(380, 400 + k * 40), (760, 400 + k * 40)], fill=SKY, width=5)

ICONS = dict(cone=cone, cheese=cheese, loom=loom, knitting=knitting, sock=sock, cap=cap, glove=glove, net=net,
             bedsheet=bedsheet, towel=towel, tshirt=tshirt, jeans=jeans, saree=saree, carpet=carpet, swatch=swatch_icon)
LABEL = dict(cone="Yarn Cone", cheese="Cheese / Bobbin", loom="Weaving Loom", knitting="Knitting Machine", sock="Socks", cap="Caps",
             glove="Gloves", net="Nets & Mesh", bedsheet="Bedsheets", towel="Towels", tshirt="T-Shirts", jeans="Denim",
             saree="Sarees", carpet="Carpets", swatch="Fabric Swatches")

def icon(name, size):
    im = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if name == "sock":
        return _sock_img().resize((size, size), Image.LANCZOS)
    if name == "net":
        tmp = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0)); td = ImageDraw.Draw(tmp)
        for k in range(-8, 9):
            td.line([(200 + k * 75, 200), (200 + k * 75 + 600, 800)], fill=SKY, width=7)
            td.line([(800 + k * 75, 200), (800 + k * 75 - 600, 800)], fill=SKY, width=7)
        m = Image.new("L", (1000, 1000), 0); ImageDraw.Draw(m).ellipse([200, 200, 800, 800], fill=255)
        im.paste(tmp, (0, 0), m); d.ellipse([200, 200, 800, 800], outline=WHITE, width=LW)
    else:
        ICONS[name](d)
    return im.resize((size, size), Image.LANCZOS)

# ---------- fabric swatch textures ----------
def swatch(kind, size, base=BLUE, hi=SKY, lo=NAVY):
    S = size * 2; im = Image.new("RGB", (S, S), lo); d = ImageDraw.Draw(im); u = S // 24
    if kind == "plain":
        for r in range(24):
            for c in range(24):
                d.rectangle([c * u + 2, r * u + 2, c * u + u - 2, r * u + u - 2], fill=hi if (r + c) % 2 else base)
    elif kind == "twill":
        for r in range(24):
            for c in range(24):
                d.rectangle([c * u + 1, r * u + 1, c * u + u - 1, r * u + u - 1], fill=hi if (c - r) % 4 < 2 else base)
    elif kind == "knit":
        w = S // 12
        for r in range(26):
            for c in range(13):
                x, y = c * w, r * w // 2
                d.line([(x + 4, y), (x + w // 2, y + w * .7)], fill=hi if r % 2 else base, width=max(3, w // 6))
                d.line([(x + w - 4, y), (x + w // 2, y + w * .7)], fill=hi if r % 2 else base, width=max(3, w // 6))
    elif kind == "mesh":
        for k in range(-24, 48, 2):
            d.line([(k * u, 0), (k * u + S, S)], fill=hi, width=max(3, u // 5))
            d.line([(k * u + S, 0), (k * u, S)], fill=base, width=max(3, u // 5))
    elif kind == "slub":
        import random; random.seed(3)
        for y in range(0, S, max(4, u // 2)):
            x = 0
            while x < S:
                L = random.randint(u, u * 5); t = random.choice([3, 4, 5, 9])
                d.line([(x, y), (x + L, y)], fill=hi if t > 5 else base, width=t); x += L
    elif kind == "melange":
        import random; random.seed(7)
        d.rectangle([0, 0, S, S], fill=base)
        for _ in range(S * 6):
            x, y = random.randrange(S), random.randrange(S)
            d.line([(x, y), (x + random.randint(4, 14), y)], fill=random.choice([hi, lo, WHITE, base]), width=2)
    return im.resize((size, size), Image.LANCZOS)
