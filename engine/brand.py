"""Shivpriya Texchem Instagram brand system (matches E-Catalogue 2026).
Feed posts & carousel slides: 1080x1080 square. Stories: 1080x1920.
Colours: navy, blue, sky, white, grey only. Logo: white, top-left, same size/position everywhere.
Titles: UPPERCASE Poppins Bold; text after '|' goes on a sky-blue second line (catalogue style)."""
import os, math
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.abspath(__file__))
NAVY, BLUE, SKY, WHITE, GREY, MIST = (22, 38, 74), (43, 93, 184), (140, 196, 255), (255, 255, 255), (111, 120, 144), (238, 242, 249)  # Company Brief Nov 2026
F = lambda w, s: ImageFont.truetype(os.path.join(ROOT, "fonts", f"Poppins-{w}.ttf"), s)
WA = "+91 87672 50274"
FOOT = f"shivpriyatexchem.com   ·   WhatsApp {WA}"
PHOTO = lambda n: os.path.join(ROOT, "assets", "photos", n)

def _logo(h=84):
    lg = Image.open(os.path.join(ROOT, "assets", "logo-white.png")).convert("RGBA")
    return lg.resize((int(lg.width * h / lg.height), h), Image.LANCZOS)

def _wrap(d, text, font, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: out.append(cur); cur = w
    out.append(cur); return out

def _kick(d, xy, text, size, center=False):
    f = F("Medium", size); sp = size * 0.2
    wid = sum(d.textlength(c, font=f) + sp for c in text.upper()) - sp
    x, y = xy
    if center: x -= wid / 2
    for ch in text.upper():
        d.text((x, y), ch, font=f, fill=SKY); x += d.textlength(ch, font=f) + sp

def _title(d, x, y, title, tf, maxw, center=False):
    for i, part in enumerate(title.split("|")):
        txt = part.strip(); txt = txt[1:] if txt.startswith("=") else txt.upper()
        for ln in _wrap(d, txt, tf, maxw):
            d.text((x, y), ln, font=tf, fill=SKY if i else WHITE, anchor="ma" if center else "la")
            y += int(tf.size * 1.12)
    return y

def _base(size, logo_y):
    im = Image.new("RGB", size, NAVY)
    return im, ImageDraw.Draw(im)

def _put_logo(im, y): lg = _logo(); im.paste(lg, (80, y), lg)

def _footer(d, W, H):
    d.line([(80, H - 110), (W - 80, H - 110)], fill=BLUE, width=2)
    d.text((W // 2, H - 66), FOOT, font=F("Regular", 27), fill=GREY, anchor="mm")

def _photo(im, photo, box):
    if not photo or not os.path.exists(photo): return False
    x0, y0, x1, y1 = box; bw, bh = x1 - x0, y1 - y0
    p = Image.open(photo).convert("RGB")
    s = max(bw / p.width, bh / p.height); p = p.resize((int(p.width * s) + 1, int(p.height * s) + 1), Image.LANCZOS)
    p = p.crop(((p.width - bw) // 2, (p.height - bh) // 2, (p.width - bw) // 2 + bw, (p.height - bh) // 2 + bh))
    im.paste(p, (x0, y0))
    g = Image.new("L", (1, bh))
    for y in range(bh):
        t = y / (bh - 1)
        a = max((0.97 * (1 - t / 0.42)) if t < 0.42 else 0, ((t - 0.50) / 0.50) if t > 0.50 else 0)
        g.putpixel((0, y), int(255 * min(1, a) ** 0.9))
    im.paste(Image.new("RGB", (bw, bh), NAVY), (x0, y0), g.resize((bw, bh)))
    return True

def _points(d, y, points, size, maxw, gap):
    pf = F("Regular", size)
    for p in points:
        d.ellipse([82, y + size * .47, 82 + size * .38, y + size * .85], fill=SKY)
        for ln in _wrap(d, p, pf, maxw):
            d.text((120, y), ln, font=pf, fill=MIST); y += gap
        y += gap * .25
    return y

def post(path, kicker, title, points=(), photo=None, page=None):
    """Square feed post / carousel slide (1080x1080)."""
    W = H = 1080
    im, d = _base((W, H), 70); y = 250
    hasp = _photo(im, photo, (0, 0, W, 500))
    if hasp: y = 430
    _put_logo(im, 70)
    if page: d.text((W - 80, 112), page, font=F("Medium", 26), fill=WHITE if hasp else GREY, anchor="rm")
    _kick(d, (80, y), kicker, 25); y += 54
    y = _title(d, 80, y, title, F("Bold", 62 if len(title) < 30 else 54), W - 160)
    y += 22; d.rectangle([80, y, 200, y + 6], fill=SKY); y += 44
    _points(d, y, points, 35, W - 220, 48)
    _footer(d, W, H); im.save(path, quality=93)

def story(path, kicker, title, points=(), photo=None, cta=f"WhatsApp  {WA}"):
    W, H = 1080, 1920
    im, d = _base((W, H), 230); y = 520
    if _photo(im, photo, (0, 0, W, 1080)): y = 960
    _put_logo(im, 230)
    _kick(d, (80, y), kicker, 30); y += 66
    y = _title(d, 80, y, title, F("Bold", 80 if len(title) < 24 else 68), W - 160)
    y += 30; d.rectangle([80, y, 220, y + 7], fill=SKY); y += 54
    _points(d, y, points, 42, W - 220, 58)
    if cta:
        d.rounded_rectangle([80, H - 330, W - 80, H - 214], radius=58, fill=WHITE)
        d.text((W // 2, H - 272), cta, font=F("Bold", 42), fill=NAVY, anchor="mm")
    d.text((W // 2, H - 130), "shivpriyatexchem.com", font=F("Regular", 30), fill=GREY, anchor="mm")
    im.save(path, quality=93)

def _motif(d, kind, cx, cy, r):
    c, w = SKY, 6
    if kind == "diya":
        d.arc([cx - r, cy - r * .2, cx + r, cy + r * .9], 0, 180, fill=c, width=w)
        d.line([(cx - r, cy + r * .35), (cx + r, cy + r * .35)], fill=c, width=w)
        d.ellipse([cx - r * .16, cy - r * .75, cx + r * .16, cy + r * .1], outline=WHITE, width=w)
        d.ellipse([cx - r * .06, cy - r * .35, cx + r * .06, cy - r * .05], fill=WHITE)
    elif kind == "moon":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=w)
        d.ellipse([cx - r * .7, cy - r * .7, cx + r * .7, cy + r * .7], outline=WHITE, width=3)
    elif kind == "sun":
        d.ellipse([cx - r * .5, cy - r * .5, cx + r * .5, cy + r * .5], outline=WHITE, width=w)
        for k in range(12):
            a = k * math.pi / 6
            d.line([(cx + math.cos(a) * r * .68, cy + math.sin(a) * r * .68), (cx + math.cos(a) * r, cy + math.sin(a) * r)], fill=c, width=w)
    elif kind == "bow":
        d.arc([cx - r, cy - r, cx + r * .2, cy + r], -70, 70, fill=c, width=w)
        d.line([(cx - r * .64, cy - r * .94), (cx - r * .64, cy + r * .94)], fill=WHITE, width=3)
        d.line([(cx - r * .9, cy), (cx + r * .9, cy)], fill=WHITE, width=w)
        d.polygon([(cx + r * .9, cy), (cx + r * .72, cy - r * .1), (cx + r * .72, cy + r * .1)], fill=WHITE)
    elif kind == "lotus":
        for k in (-2, -1, 0, 1, 2):
            a = math.radians(-90 + k * 28); px, py = cx + math.cos(a) * r * .55, cy + math.sin(a) * r * .55
            d.ellipse([px - r * .22, py - r * .42, px + r * .22, py + r * .42], outline=c if k else WHITE, width=5)
        d.line([(cx - r, cy + r * .45), (cx + r, cy + r * .45)], fill=c, width=w)
    elif kind == "spark":  # Yarns AI: cone + spark, like the catalogue AI page
        d.polygon([(cx - r * .45, cy + r * .9), (cx + r * .45, cy + r * .9), (cx + r * .22, cy - r * .5), (cx - r * .22, cy - r * .5)], outline=WHITE, width=w)
        for k in range(-1, 3): d.line([(cx - r * (.4 - k * .04), cy + r * (.55 - k * .35)), (cx + r * (.4 - k * .04), cy + r * (.55 - k * .35))], fill=c, width=3)
        sx, sy, sr = cx + r * .6, cy - r * .75, r * .28
        d.polygon([(sx, sy - sr), (sx + sr * .22, sy - sr * .22), (sx + sr, sy), (sx + sr * .22, sy + sr * .22), (sx, sy + sr), (sx - sr * .22, sy + sr * .22), (sx - sr, sy), (sx - sr * .22, sy - sr * .22)], fill=WHITE)
    else:
        for k, col in ((1, c), (.72, WHITE), (.44, c)):
            d.ellipse([cx - r * k, cy - r * k, cx + r * k, cy + r * k], outline=col, width=4)

def festival(path, name, wish, motif, square=True, kicker="Warm Wishes", sign="Team Shivpriya Texchem"):
    W, H = (1080, 1080) if square else (1080, 1920)
    im, d = _base((W, H), 0); _put_logo(im, 70 if square else 230)
    cy = 390 if square else 760
    _motif(d, motif, W // 2, cy, 150 if square else 200)
    y = cy + (210 if square else 290)
    _kick(d, (W // 2, y - 18), kicker, 28 if square else 34, center=True); y += 50 if square else 70
    y = _title(d, W // 2, y, name, F("Bold", 66 if square else 86), W - 160, center=True) + (28 if square else 40)
    wf = F("Regular", 31 if square else 40)
    for ln in _wrap(d, wish, wf, W - 240):
        d.text((W // 2, y), ln, font=wf, fill=MIST, anchor="ma"); y += 46 if square else 58
    if square: _footer(d, W, H)
    else: d.text((W // 2, H - 130), sign, font=F("Medium", 34), fill=GREY, anchor="mm")
    im.save(path, quality=93)


# ---------- layouts with illustrations / swatches ----------
def post_icons(path, kicker, title, names, page=None):
    """Applications slide: up to 6 line icons in a grid with labels."""
    import icons
    W = H = 1080; im, d = _base((W, H), 70); _put_logo(im, 70)
    if page: d.text((W - 80, 112), page, font=F("Medium", 26), fill=GREY, anchor="rm")
    y = 230; _kick(d, (80, y), kicker, 25); y += 54
    y = _title(d, 80, y, title, F("Bold", 56), W - 160) + 30
    cols = 3; cw = (W - 160) // cols; sz = 190
    for i, n in enumerate(names[:6]):
        cx = 80 + (i % cols) * cw + cw // 2; cy = y + (i // cols) * 290
        ic = icons.icon(n, sz); im.paste(ic, (cx - sz // 2, cy), ic)
        d.text((cx, cy + sz + 28), icons.LABEL[n], font=F("Regular", 30), fill=MIST, anchor="mm")
    _footer(d, W, H); im.save(path, quality=93)

def post_hero(path, kicker, title, icon_name, points=(), page=None):
    """Process slide: big illustration on the right, text on the left."""
    import icons
    W = H = 1080; im, d = _base((W, H), 70); _put_logo(im, 70)
    if page: d.text((W - 80, 112), page, font=F("Medium", 26), fill=GREY, anchor="rm")
    ic = icons.icon(icon_name, 420); im.paste(ic, (W - 470, 300), ic)
    y = 250; _kick(d, (80, y), kicker, 25); y += 54
    y = _title(d, 80, y, title, F("Bold", 54), 540) + 22
    d.rectangle([80, y, 200, y + 6], fill=SKY); y += 44
    pf = F("Regular", 33)
    for p in points:
        d.ellipse([82, y + 16, 95, y + 29], fill=SKY)
        for ln in _wrap(d, p, pf, 470): d.text((118, y), ln, font=pf, fill=MIST); y += 46
        y += 12
    _footer(d, W, H); im.save(path, quality=93)

def post_swatches(path, kicker, title, kinds, labels, page=None):
    """Fabric swatch slide: 2x2 swatch tiles with labels."""
    import icons
    W = H = 1080; im, d = _base((W, H), 70); _put_logo(im, 70)
    if page: d.text((W - 80, 112), page, font=F("Medium", 26), fill=GREY, anchor="rm")
    y = 230; _kick(d, (80, y), kicker, 25); y += 54
    y = _title(d, 80, y, title, F("Bold", 56), W - 160) + 30
    sz = 300; gap = (W - 160 - 2 * sz)
    for i, (k, lb) in enumerate(zip(kinds[:4], labels[:4])):
        x = 80 + (i % 2) * (sz + gap) if len(kinds) > 2 else 80 + i * (sz + gap)
        x = 80 + (i % 2) * (W - 160 - sz) if False else [140, 140 + sz + 140][i % 2]
        yy = y + (i // 2) * (sz // 2 + 140) if False else y + (i // 2) * 0
        pass
    n = len(kinds[:4]); sz = 200 if n > 3 else 250; tot = n * sz + (n - 1) * 30; x0 = (W - tot) // 2
    for i, (k, lb) in enumerate(zip(kinds[:4], labels[:4])):
        x = x0 + i * (sz + 30); sw = icons.swatch(k, sz)
        mask = Image.new("L", (sz, sz), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, sz - 1, sz - 1], radius=24, fill=255)
        im.paste(sw, (x, y + 20), mask)
        d.text((x + sz // 2, y + sz + 60), lb, font=F("Regular", 28), fill=MIST, anchor="mm")
    _footer(d, W, H); im.save(path, quality=93)
