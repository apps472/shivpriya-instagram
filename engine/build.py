"""Render one day of the 1-year plan (6 stories, 2 carousels, 2 reels, festival wishes) and return its queue items.
Usage: python engine/build.py OUT_DIR YYYY-MM-DD [YYYY-MM-DD ...]   -> writes OUT_DIR/<date>/* and OUT_DIR/<date>/items.json"""
import os, sys, json, datetime, subprocess, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand, icons, kb, cal
from PIL import Image, ImageDraw
WA = brand.WA
USE_RACK_PHOTOS = True   # set False to follow the brief strictly (no office/godown cone or shelf photos)
PRODUCT = ["polyester-yarn.jpg", "blue-cone.jpg"]
RACKS = {"grey": ["grey-melange-rack.jpg", "grey-rack-2.jpg", "grey-rack-4.jpg", "grey-rack-5.jpg", "grey-rack-6.jpg", "cone-shelf.jpg"],
         "colour": ["colour-rack.jpg", "colour-rack-2.jpg", "colour-rack-3.jpg", "blue-cone.jpg"]}
ICON = [("weav", "loom"), ("warp", "loom"), ("knit", "knitting"), ("hosiery", "sock"), ("sock", "sock"), ("saree", "saree"), ("denim", "jeans"), ("jeans", "jeans"),
        ("towel", "towel"), ("bed", "bedsheet"), ("home textile", "bedsheet"), ("carpet", "carpet"), ("rug", "carpet"), ("mesh", "net"), ("net", "net"),
        ("t-shirt", "tshirt"), ("apparel", "tshirt"), ("sportswear", "tshirt"), ("innerwear", "tshirt"), ("legging", "tshirt"), ("swimwear", "tshirt"),
        ("athleisure", "tshirt"), ("casual", "jeans"), ("winter", "cap"), ("sweater", "cap"), ("cap", "cap"), ("glove", "glove"), ("industrial", "glove"),
        ("uniform", "tshirt"), ("technical", "net"), ("narrow fabric", "swatch"), ("upholstery", "swatch"), ("suiting", "swatch"), ("shirting", "swatch"), ("embroidery", "saree")]
FILAMENT = {"filament", "dyed", "technical", "stretch"}

def photo(name, seed):
    v = kb.Y.get(name, {}); fam = v.get("fam", "spun")
    pool = PRODUCT[:]
    if USE_RACK_PHOTOS: pool += RACKS["colour"] if (fam in ("dyed", "filament") or "Dyed" in name) else RACKS["grey"]
    return brand.PHOTO(pool[seed % len(pool)])

def title2(name):
    n = name.split(" (")[0].replace(" - ", " ")
    w = n.split(); k = max(1, (len(w) + 1) // 2)
    return " ".join(w[:k]) + ("|" + " ".join(w[k:]) if w[k:] else "") + "."

def stop(t): t = t.strip(); return t if t.endswith((".", "?", "!")) else t + "."

def half(t):
    w = t.rstrip(".").split(); k = max(1, (len(w) + 1) // 2)
    return " ".join(w[:k]) + ("|" + " ".join(w[k:]) if w[k:] else "") + "."

def icons_for(uses):
    out = []
    for u in uses:
        for k, v in ICON:
            if k == u and v not in out: out.append(v)
    for v in ("loom", "knitting", "swatch", "tshirt", "bedsheet", "sock"):
        if len(out) < 6 and v not in out: out.append(v)
    return out[:6]

def swatches_for(name, v):
    n = (name + " " + " ".join(v["u"])).lower()
    if "slub" in n or "neppy" in n or v["fam"] == "fancy": return ["slub", "plain", "twill", "knit"]
    if "denim" in n or "indigo" in n: return ["twill", "plain", "slub", "knit"]
    if "melange" in n or v["fam"] == "dyed": return ["melange", "knit", "plain", "twill"]
    if v["fam"] in ("technical",) or "net" in n: return ["mesh", "knit", "plain", "twill"]
    if v["fam"] == "stretch": return ["knit", "mesh", "twill", "plain"]
    return ["plain", "twill", "knit", "melange"]
SWL = dict(plain="Plain", twill="Twill", knit="Knit", mesh="Mesh", slub="Slub", melange="Melange")

class Deck:
    def __init__(s, out, prefix): s.out, s.prefix, s.files = out, prefix, []
    def nxt(s):
        p = os.path.join(s.out, f"{s.prefix}-{len(s.files) + 1:02d}.jpg"); s.files.append(p); return p
    def pg(s, total): return lambda i: f"{i:02d} / {total:02d}"

def cta(dk, page):
    brand.post(dk.nxt(), "Need a rate?", "Let's Talk|Yarn.", [f"WhatsApp {WA}", "Indicative rate within 24 hours", "Follow for one textile lesson a day"], page=page)

def why(dk, page, seed):
    brand.post(dk.nxt(), "Why Shivpriya", "Three Decades.|One Standard.", ["Authorised agent for India's leading mills", "2,500+ customers · 22 textile hubs",
               "We don't just trade it. We make it: TFO & SNZ"], photo=brand.PHOTO(PRODUCT[seed % 2]), page=page)

# ---------------- carousel 2: week sub-topic ----------------
def yarn_deck(out, r, seed):
    dk = Deck(out, "c2"); A, B, ang = r["wa"], r["wb"], r["ang"]
    if r["slot"] == "B": A = B
    v = kb.Y[A]; T = title2(A); N = 10; pg = lambda i: f"{i:02d}"
    fil = v["fam"] in FILAMENT
    if ang == "counts & uses":
        brand.post(dk.nxt(), "Week sub-topic · Counts & uses", T, [v["hook"], "Swipe to learn"], photo=photo(A, seed), page=pg(1))
        brand.post_hero(dk.nxt(), "What is it?", T, "cheese" if fil else "cone", [v["what"]], page=pg(2))
        brand.post(dk.nxt(), "Counts we supply", "Counts.|=" + v["c"], [" · ".join(v["t"]), "Counts outside the list built to requirement"], page=pg(3))
        brand.post(dk.nxt(), "Types & variants", "Types.|Variants.", v["t"], page=pg(4))
        brand.post(dk.nxt(), "Key features", "Built To|Perform.", v["f"], page=pg(5))
        brand.post_icons(dk.nxt(), "Where it's used", "From Loom|To Market.", icons_for(v["u"]), page=pg(6))
        sw = swatches_for(A, v); brand.post_swatches(dk.nxt(), "Fabrics it makes", "Woven &|Knitted.", sw, [SWL[x] for x in sw], page=pg(7))
        brand.post(dk.nxt(), "Did you know?", "Fact.|Not Fiction.", [v["fact"]], photo=photo(A, seed + 1), page=pg(8))
        why(dk, pg(9), seed); cta(dk, pg(10))
    elif ang == "how to check quality":
        brand.post(dk.nxt(), "Week sub-topic · Quality check", T, ["5 checks before you run a new lot", "Swipe to learn"], photo=photo(A, seed), page=pg(1))
        brand.post_hero(dk.nxt(), "What is it?", T, "cheese" if fil else "cone", [v["what"]], page=pg(2))
        chk = kb.CHECK[v["fam"]]
        for i, c in enumerate(chk):
            h, dtl = c.split(": ", 1); brand.post(dk.nxt(), f"Check {i + 1:02d} of 05", stop(h) + "|", [dtl[0].upper() + dtl[1:]], page=pg(3 + i))
        brand.post(dk.nxt(), "Save this checklist", "Quality Is|Woven In.", [c.split(":")[0] for c in chk], page=pg(8))
        brand.post(dk.nxt(), "Our promise", "Every Cone|Traced.", ["Every cone tracked to the lot, the mill and the run", "Consistent quality on the first order and the four-hundredth"], page=pg(9))
        cta(dk, pg(10))
    elif ang == "the fabric it makes":
        brand.post(dk.nxt(), "Week sub-topic · Yarn to fabric", T, ["From fibre to fabric", "Swipe to see where it goes"], photo=photo(A, seed), page=pg(1))
        brand.post_hero(dk.nxt(), "What is it?", T, "cheese" if fil else "cone", [v["what"]], page=pg(2))
        brand.post_icons(dk.nxt(), "Where it's used", "From Loom|To Market.", icons_for(v["u"]), page=pg(3))
        sw = swatches_for(A, v); brand.post_swatches(dk.nxt(), "Fabrics it makes", "Woven &|Knitted.", sw, [SWL[x] for x in sw], page=pg(4))
        for i, u in enumerate(v["u"][:4]):
            h, dtl = kb.USE_LINE[u].split(": ", 1)
            brand.post(dk.nxt(), f"End use {i + 1:02d}", stop(h) + "|", [dtl[0].upper() + dtl[1:], f"Why it works: {v['f'][i % 4].lower()}"], page=pg(5 + i))
        brand.post(dk.nxt(), "Did you know?", "Fact.|Not Fiction.", [v["fact"]], page=pg(9))
        cta(dk, pg(10))
    elif ang == "buying guide":
        brand.post(dk.nxt(), "Week sub-topic · Buying guide", T, ["Buy it right, the first time", "Swipe to learn"], photo=photo(A, seed), page=pg(1))
        brand.post_hero(dk.nxt(), "What is it?", T, "cheese" if fil else "cone", [v["what"]], page=pg(2))
        brand.post(dk.nxt(), "Counts we supply", "Counts.|=" + v["c"], [" · ".join(v["t"])], page=pg(3))
        for i, (t, b) in enumerate((("Send 4 Things.|", kb.BUY[0]), ("Sample Cone|First.", kb.BUY[1]), ("Mill-Direct Or|Stock-Lot?", kb.BUY[2]))):
            brand.post(dk.nxt(), f"Buying tip {i + 1:02d}", t, [b.split(": ", 1)[-1][0].upper() + b.split(": ", 1)[-1][1:]], page=pg(4 + i))
        brand.post(dk.nxt(), "Quality check", "Check Before|You Run.", [c.split(":")[0] for c in kb.CHECK[v["fam"]]], page=pg(7))
        brand.post(dk.nxt(), "Key features", "What You|Should Get.", v["f"], page=pg(8))
        why(dk, pg(9), seed); cta(dk, pg(10))
    elif ang.startswith("A vs B"):
        a, b = kb.Y[r["wa"]], kb.Y[r["wb"]]
        brand.post(dk.nxt(), "Week sub-topic · Which one, when", f"={r['wa']}|vs {r['wb']}.", ["Same family, different jobs", "Swipe to compare"], photo=photo(r["wa"], seed), page=pg(1))
        brand.post_hero(dk.nxt(), "Option A", title2(r["wa"]), "cheese" if a["fam"] in FILAMENT else "cone", [a["what"]], page=pg(2))
        brand.post_hero(dk.nxt(), "Option B", title2(r["wb"]), "cheese" if b["fam"] in FILAMENT else "cone", [b["what"]], page=pg(3))
        brand.post(dk.nxt(), "Counts", "Side By|Side.", [f"A: {a['c']}", f"B: {b['c']}"], page=pg(4))
        brand.post(dk.nxt(), "Strengths of A", title2(r["wa"]), a["f"], page=pg(5))
        brand.post(dk.nxt(), "Strengths of B", title2(r["wb"]), b["f"], page=pg(6))
        brand.post(dk.nxt(), "Pick A when", "Choose|A For.", [kb.USE_LINE[u].split(":")[0] for u in a["u"][:4]], page=pg(7))
        brand.post(dk.nxt(), "Pick B when", "Choose|B For.", [kb.USE_LINE[u].split(":")[0] for u in b["u"][:4]], page=pg(8))
        brand.post(dk.nxt(), "Still not sure?", "Ask Us.|We Advise.", ["Technical support on count, blend, construction and end use", "Share your fabric and loom"], page=pg(9))
        cta(dk, pg(10))
    else:  # week recap
        a, b = kb.Y[r["wa"]], kb.Y[r["wb"]]
        brand.post(dk.nxt(), f"Week {r['week']} recap", "This Week|We Learned.", [r["wa"], r["wb"]], photo=photo(r["wa"], seed), page=pg(1))
        for j, (nm, x) in enumerate(((r["wa"], a), (r["wb"], b))):
            brand.post(dk.nxt(), "In one slide", title2(nm), [x["what"], f"Counts: {x['c']}", " · ".join(x["f"][:3])], page=pg(2 + j))
        q, ans = kb.QUIZ[r["week"] % len(kb.QUIZ)]
        brand.post(dk.nxt(), "Quick quiz", stop(q) + "|", ["Answer on the next slide"], page=pg(4))
        brand.post(dk.nxt(), "Answer", stop(ans) + "|", ["Save this post for later"], page=pg(5))
        brand.post(dk.nxt(), "Free guides", "84 Knowledge|Guides.", ["Counts, blends, looms and more", "shivpriyatexchem.com/knowledge"], page=pg(6))
        cta(dk, pg(7))
    return dk.files

# ---------------- carousel 1: pillar of the day ----------------
PCOVER = {"M": "Motivation Monday", "K": "Knowledge Tuesday", "H": "Textile cities", "A": "Yarns AI & buyer tips", "F": "Yarn to fabric", "B": "Behind our floor", "V": "The Shivpriya story"}
def pillar_deck(out, r, seed):
    dk = Deck(out, "c1"); k, key = r["pk"], r["pkey"]
    pts = {"M": kb.MOT, "K": kb.KNOW, "H": kb.HUBK, "A": kb.AIK, "F": kb.FABK, "B": kb.BTSK, "V": kb.VALK}[k][key]
    n = len(pts) + 2; pg = lambda i: f"{i:02d}"
    ttl = half(key) if k == "M" else (f"Which Yarn For|{key}?" if k == "F" else half(key.split(" - ")[0].split(" (")[0]) if len(key) < 40 else half(key.split(":")[0].split(" - ")[0]))
    sub = {"M": ["Words from our office walls", "Swipe"], "H": [key.split(" - ")[-1] if " - " in key else "One of the 22 hubs we serve", "Swipe"]}.get(k, ["Swipe to learn"])
    ph = brand.PHOTO("office-team.jpg") if (k == "V" and "," in key) else (brand.PHOTO("expo-booth.jpg") if "Expo" in key else None)
    brand.post(dk.nxt(), PCOVER[k], ttl, sub, photo=ph, page=pg(1))
    for i, p in enumerate(pts):
        if ": " in p: h, dtl = p.split(": ", 1); brand.post(dk.nxt(), f"{PCOVER[k]} · {i + 1:02d}", stop(h) + "|", [dtl[0].upper() + dtl[1:]], page=pg(i + 2))
        else: brand.post(dk.nxt(), f"{PCOVER[k]} · {i + 1:02d}", "=" + stop(p) if len(p) > 28 else stop(p) + "|", [], page=pg(i + 2))
    cta(dk, pg(n)); return dk.files

# ---------------- stories ----------------
def stories(out, r, seed):
    S = lambda nm: os.path.join(out, nm); A = r["wb"] if r["slot"] == "B" else r["wa"]; v = kb.Y[A]
    q, ans = kb.QUIZ[(r["n"]) % len(kb.QUIZ)]; f = []
    brand.story(S("s1.jpg"), "Good morning", half(kb.MORNING[r["n"] % len(kb.MORNING)]), ["Team Shivpriya Texchem"]); f.append(("08:30", "s1.jpg"))
    brand.story(S("s2.jpg"), "Yarn of the day", title2(A), [v["what"]], photo=photo(A, seed + 2)); f.append(("10:00", "s2.jpg"))
    brand.story(S("s3.jpg"), "Counts we supply", "Counts.|=" + v["c"], v["t"][:3] + ["Indicative rate within 24 hours"]); f.append(("13:00", "s3.jpg"))
    brand.story(S("s4.jpg"), "Quick quiz", stop(q) + "|", ["Answer in tonight's story", "Or reply to us on WhatsApp"]); f.append(("15:30", "s4.jpg"))
    brand.story(S("s5.jpg"), "Where it's used", "From Loom|To Market.", [kb.USE_LINE[u].split(":")[0] for u in v["u"][:4]]); f.append(("18:00", "s5.jpg"))
    brand.story(S("s6.jpg"), "Quiz answer", stop(ans) + "|", [kb.NIGHT[r["n"] % len(kb.NIGHT)], "Follow for one textile lesson a day"]); f.append(("21:00", "s6.jpg"))
    return f

# ---------------- reels ----------------
def endcard(path):
    W, H = 1080, 1920; sc = Image.new("RGB", (W, H), brand.NAVY); d = ImageDraw.Draw(sc)
    lg = Image.open(os.path.join(brand.ROOT, "assets", "logo-white.png")).convert("RGBA"); lg = lg.resize((640, int(lg.height * 640 / lg.width)), Image.LANCZOS)
    sc.paste(lg, (220, 600), lg); d.text((540, 900), "YARN MADE FOR YOU.", font=brand.F("Bold", 64), fill=brand.WHITE, anchor="mm")
    d.rounded_rectangle([80, 990, 1000, 1110], radius=60, fill=brand.WHITE)
    d.text((540, 1050), f"WhatsApp  {WA}", font=brand.F("Bold", 44), fill=brand.NAVY, anchor="mm")
    d.text((540, 1190), "www.shivpriyatexchem.com", font=brand.F("Regular", 34), fill=brand.GREY, anchor="mm")
    d.text((540, 1250), "Mumbai · Bhiwandi · Surat · Ichalkaranji", font=brand.F("Regular", 30), fill=brand.GREY, anchor="mm"); sc.save(path, quality=92)

def scene(slide, path, i):
    W, H = 1080, 1920; sc = Image.new("RGB", (W, H), brand.NAVY); sl = Image.open(slide); sc.paste(sl, (0, 420))
    d = ImageDraw.Draw(sc); d.text((540, 1640), "www.shivpriyatexchem.com", font=brand.F("Regular", 32), fill=brand.GREY, anchor="mm"); sc.save(path, quality=92)

def reel(slides, out, name):
    pick = (slides[:5] + slides[-2:-1] * 5)[:5]; sp = []
    for i, s in enumerate(pick):
        p = os.path.join(out, f"_{name}{i}.jpg"); scene(s, p, i); sp.append(p)
    p = os.path.join(out, f"_{name}end.jpg"); endcard(p); sp.append(p)
    dur, fade = 5.6, 0.6; inp, flt = [], []
    for i, s in enumerate(sp, 1):
        inp += ["-loop", "1", "-t", str(dur), "-i", s]
        flt.append(f"[{i-1}:v]scale=792:1408,zoompan=z='min(zoom+0.0006,1.06)':d={int(dur*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=720x1280:fps=30,format=yuv420p,setsar=1[v{i}]")
    chain, off = "[v1]", dur - fade
    for i in range(2, 7):
        flt.append(f"{chain}[v{i}]xfade=transition=fade:duration={fade}:offset={off:.2f}[x{i}]"); chain = f"[x{i}]"; off += dur - fade
    mp4 = os.path.join(out, f"{name}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inp + ["-f", "lavfi", "-t", "30", "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex", ";".join(flt),
        "-map", chain, "-map", "6:a", "-t", "30", "-c:v", "libx264", "-preset", "fast", "-crf", "26", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", mp4], check=True)
    for s in sp: os.remove(s)
    return os.path.basename(mp4)

# ---------------- captions ----------------
def caption(hook, lines, tags):
    return "\n".join([stop(hook), ""] + lines + ["", "We supply spun, filament and fancy yarns from India's leading mills - and make TFO & SNZ yarn on our own floor.",
           f"📩 WhatsApp {WA} for an indicative rate within 24 hours.", "🌐 www.shivpriyatexchem.com", "", " ".join(kb.TAGS["core"] + tags)])

def festival(out, name, f):
    mot = next((m for k, m in kb.FEST_MOTIF.items() if k in name), "mandala")
    wish = next((w for k, w in kb.WISH.items() if k == name), kb.WISH_DEFAULT)
    nm = name.split(" (")[0]
    brand.festival(os.path.join(out, "w-story.jpg"), stop(nm), wish, mot, square=False, kicker="Warm wishes")
    brand.festival(os.path.join(out, "w-1.jpg"), stop(nm), wish, mot, square=True, kicker="Warm wishes")
    brand.post(os.path.join(out, "w-2.jpg"), "From our family to yours", "Yarn Made|For You.", ["Shivpriya Texchem Pvt. Ltd. & G S & Sons", "Mumbai · Bhiwandi · Surat · Ichalkaranji"])
    return nm, wish

def build(outroot, day):
    rows = {r["dt"]: r for r in cal.rows()}; r = rows[day]; ds = day.isoformat(); out = os.path.join(outroot, ds); os.makedirs(out, exist_ok=True)
    seed = r["n"]; items = []; at = lambda t: f"{ds} {t}"; F = lambda fn: f"{ds}/{fn}"
    A = r["wb"] if r["slot"] == "B" else r["wa"]; v = kb.Y[A]
    if r["fe"]:
        nm, wish = festival(out, r["fe"], None)
        items += [dict(id=f"y{ds}-wish-story", type="story", files=[F("w-story.jpg")], at=at("07:30")),
                  dict(id=f"y{ds}-wish", type="carousel", files=[F("w-1.jpg"), F("w-2.jpg")], at=at("09:00"),
                       caption=f"{wish}\n\nTeam Shivpriya Texchem & G S & Sons.\n\n" + " ".join(kb.TAGS["core"] + kb.TAGS["fest"]))]
    for t, fn in stories(out, r, seed): items.append(dict(id=f"y{ds}-{fn[:-4]}", type="story", files=[F(fn)], at=at(t)))
    c2 = yarn_deck(out, r, seed); c1 = pillar_deck(out, r, seed)
    fam_tags = kb.TAGS.get(v["fam"], kb.TAGS["spun"])
    cap2 = caption(v["hook"], [v["what"], "Counts: " + v["c"], " · ".join(v["f"][:3])], fam_tags)
    pts = {"M": kb.MOT, "K": kb.KNOW, "H": kb.HUBK, "A": kb.AIK, "F": kb.FABK, "B": kb.BTSK, "V": kb.VALK}[r["pk"]][r["pkey"]]
    cap1 = caption(r["pkey"] + (" - which yarn?" if r["pk"] == "F" else ""), ["• " + p for p in pts[:4]], kb.TAGS[r["pk"]])
    items.append(dict(id=f"y{ds}-c2", type="carousel", files=[F(os.path.basename(x)) for x in c2], at=at("11:00"), caption=cap2))
    items.append(dict(id=f"y{ds}-c1", type="carousel", files=[F(os.path.basename(x)) for x in c1], at=at("17:00"), caption=cap1))
    items.append(dict(id=f"y{ds}-r1", type="reel", files=[F(reel(c2, out, "r1"))], at=at("13:30"), caption=cap2))
    items.append(dict(id=f"y{ds}-r2", type="reel", files=[F(reel(c1, out, "r2"))], at=at("19:30"), caption=cap1))
    for it in items: it.update(branch="media", posted=False)
    items.sort(key=lambda x: x["at"]); json.dump(items, open(os.path.join(out, "items.json"), "w"), indent=1, ensure_ascii=False)
    return items

if __name__ == "__main__":
    o = sys.argv[1]
    for s in sys.argv[2:]: its = build(o, datetime.date.fromisoformat(s)); print(s, len(its), "items", flush=True)
