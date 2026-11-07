"""Single source of truth for the 365-day calendar (16 Nov 2026 - 15 Nov 2027)."""
import datetime, itertools
import kb
START = datetime.date(2026, 11, 16)
d = datetime.date
FEST = {d(2026,11,20): "Devutthana Ekadashi", d(2026,11,21): "Tulsi Vivah", d(2026,11,24): "Guru Nanak Jayanti & Dev Deepawali", d(2026,12,20): "Gita Jayanti",
 d(2026,12,23): "Datta Jayanti", d(2026,12,25): "Christmas", d(2026,12,31): "New Year's Eve", d(2027,1,1): "New Year 2027", d(2027,1,13): "Lohri",
 d(2027,1,14): "Makar Sankranti & Pongal"}
Y = {n: (v["fam"], v["c"]) for n, v in kb.Y.items()}
F27 = {d(2027,1,26):"Republic Day", d(2027,2,11):"Vasant Panchami", d(2027,3,6):"Maha Shivratri", d(2027,3,8):"Women's Day",
 d(2027,3,10):"Eid al-Fitr (moon, confirm)", d(2027,3,21):"Holika Dahan", d(2027,3,22):"Holi", d(2027,4,1):"New Financial Year",
 d(2027,4,7):"Gudi Padwa / Ugadi", d(2027,4,14):"Baisakhi & Ambedkar Jayanti", d(2027,4,15):"Ram Navami", d(2027,4,20):"Hanuman Jayanti",
 d(2027,5,1):"Maharashtra Day & Labour Day", d(2027,5,9):"Akshaya Tritiya & Mother's Day", d(2027,5,17):"Eid al-Adha (moon, confirm)",
 d(2027,6,5):"World Environment Day", d(2027,6,20):"Father's Day", d(2027,6,21):"International Yoga Day", d(2027,7,5):"Rath Yatra",
 d(2027,7,18):"Guru Purnima", d(2027,8,7):"National Handloom Day", d(2027,8,15):"Independence Day", d(2027,8,17):"Raksha Bandhan",
 d(2027,8,25):"Janmashtami", d(2027,9,4):"Ganesh Chaturthi", d(2027,9,5):"Teachers' Day", d(2027,9,14):"Anant Chaturdashi",
 d(2027,9,15):"Engineers' Day", d(2027,9,30):"Navratri begins", d(2027,10,2):"Gandhi Jayanti", d(2027,10,7):"World Cotton Day",
 d(2027,10,9):"Dussehra", d(2027,10,16):"1 year of our Instagram", d(2027,10,18):"Karwa Chauth", d(2027,10,27):"Dhanteras",
 d(2027,10,28):"Choti Diwali", d(2027,10,29):"Diwali + Yarns AI turns 1", d(2027,10,30):"Govardhan Puja / New Year (Gujarati)",
 d(2027,10,31):"Bhai Dooj", d(2027,11,2):"Labh Pancham (confirm)", d(2027,11,4):"Chhath Puja", d(2027,11,14):"Guru Nanak Jayanti (confirm)"}
for i in range(1, 9): F27.setdefault(d(2027,9,30) + datetime.timedelta(days=i), f"Navratri Day {i+1}")
FALL = {**FEST, **F27}
# monthly yarn focus (Jan 15 onward) -> yarn names
MF = {(2027,1):["Acrylic","Wool & Wool Blends","Melange","P/V 2-ply Suiting","Polyester Ring Spun","P/V 65/35","Polyester OE"],
 (2027,2):["Combed Cotton","Compact Cotton","Carded Cotton","100% Flax (Linen)","Linen-Cotton & Linen-Viscose","Viscose Ring Spun","Tencel / Lyocell","Modal"],
 (2027,3):["Single & Double Dyed","Dope Dyed Colours","Dope Dyed Black","Melange","Space Dyed","Jaspe Yarn","Indigo Ring Dyed"],
 (2027,4):["FDY Bright","FDY Semi & Full Dull","DTY SD vs FD","Intermingled DTY (HIM/NIM/SIM)","POY","ATY","PTY","Hollow Yarn"],
 (2027,5):["Compact Cotton","Siro / Eli Twist","Polyester Vortex","Viscose Vortex","OE Cotton","Viscose Compact","Viscose OE"],
 (2027,6):["Recycled rPET","GRS Certified Yarns","Tencel / Lyocell","EcoVero / Livaeco","Hemp & Hemp Blends","Bamboo","100% Flax (Linen)"],
 (2027,7):["Polyester Ring Spun","Viscose Ring Spun","Combed Cotton","Nylon 6 vs Nylon 6,6","BCF Carpet Yarn","P/C 65/35","C/P & CVC"],
 (2027,8):["Neppy Yarn","Multi-count Slub","Injection & Core-spun Slub","TFO Twisted Polyester","SNZ Mono Covered (S & Z)","Mono Filament","Mother Yarn"],
 (2027,9):["Viscose Ring Spun","Modal","Micro Modal","Polyester Lycra","Viscose Lycra","Superstretch","Micro Modal-Cotton","Cotton-Viscose"],
 (2027,10):["DTY SD vs FD","Viscose Ring Spun","P/V 65/35","Polyester Ring Spun","Combed Cotton","Dope Dyed Colours","Melange","Viscose Lycra"],
 (2027,11):["Polyester Ring Spun","DTY SD vs FD","Viscose Ring Spun","Combed Cotton","P/V 65/35"]}
ANG = ["counts & uses","the fabric it makes","how to check quality","vs its closest rival","buying guide","end uses","dyeing & finishing"]
THEME = {(2027,1):"New year, new looms",(2027,2):"Summer prep",(2027,3):"Colour & finish",(2027,4):"New financial year",(2027,5):"Quality month",
 (2027,6):"Sustainable June",(2027,7):"Hub tour",(2027,8):"Made in India",(2027,9):"Festive fabrics",(2027,10):"Diwali peak",(2027,11):"Year in review"}







_R2 = ["Motivation line (animated)","Myth vs Fact","Hub montage","Yarns AI demo","Fabric showcase","Behind the scenes (real video)","Week recap"]

MOT = list(kb.MOT); KNOW = list(kb.KNOW); AI = list(kb.AIK); FAB = list(kb.FABK); BTS = list(kb.BTSK)
HUB = ["Ichalkaranji - Manchester of Maharashtra","Surat - India's MMF capital","Bhiwandi - the powerloom belt","Bhilwara - textile city of India",
 "Tirupur - knitwear capital","Ludhiana - hosiery & woollens","Panipat - home furnishing","Varanasi - weaving heritage","Malegaon - grey cloth",
 "Ahmedabad - cotton & denim","Mumbai - where we began","Coimbatore, Erode & Salem","Kolkata - jute & hosiery","Rajkot","Bharuch","Delhi",
 "Indore","Nagpur","Raipur","Burhanpur","Ichalkaranji by numbers","Ichalkaranji - next 10 years","Our mill partners (names as text only)","22 hubs we serve"]
VAL = ["S: Sustainable Solutions","Hari Prasad Chandak, Co-founder & Director","H: Heritage of Trust","Jagdish Prasad Chandak, Co-founder & Director",
 "I: Innovation","Pratik Chandak, Head of Sales & Marketing","V: Versatility","Manmohan Chandak, Finance, Legal & Compliance","P: Pan-India Network",
 "Vishnu Chandak, Operations & Administration","R: Reliability","Keshav Chandak, Technology & IT","I: Integrity","Yogesh Chandak, Online Sales & Marketing",
 "Y: Yarn Excellence","Pankaj Rathi, Sales Head - Filament","A: Alliance with Leaders","Prakash Godhara, Sales Head - Spun","Founder quote: ship without a compass",
 "Manoj Jhabak, Head of Accounts","Since 1996 - our journey","Yarn Expo Ichalkaranji 2025","2,500+ customers across India","Mission, Vision, Values, Growth"]
for L, D in ((HUB, kb.HUBK), (VAL, kb.VALK)):
    for x in L: assert x in D, x

WEEKS = [("Polyester Ring Spun","Polyester Vortex"),("Polyester OE","SHT Yarn"),("FDY Bright","FDY Semi & Full Dull"),
 ("DTY SD vs FD","Intermingled DTY (HIM/NIM/SIM)"),("POY","ATY"),("Dope Dyed Black","Dope Dyed Colours"),("TFO Twisted Polyester","PTY"),
 ("Acrylic","Wool & Wool Blends"),("P/V 65/35","P/V 2-ply Suiting"),("Melange","PSF - the fibre"),("Nylon 6 vs Nylon 6,6","Nylon Textured"),
 ("Carded Cotton","Combed Cotton"),("Compact Cotton","Siro / Eli Twist"),("100% Flax (Linen)","Linen-Cotton & Linen-Viscose"),
 ("Viscose Ring Spun","Viscose OE"),("Single & Double Dyed","Space Dyed"),("Jaspe Yarn","Indigo Ring Dyed"),("Viscose Compact","Viscose Vortex"),
 ("Dope Dyed Colours","Single & Double Dyed"),("FDY Bright","DTY SD vs FD"),("Hollow Yarn","Mono Filament"),("SNZ Mono Covered (S & Z)","Mother Yarn"),
 ("POY","Intermingled DTY (HIM/NIM/SIM)"),("Modal","Micro Modal"),("OE Cotton","Polyester OE"),("Compact Cotton","Polyester Ring Spun"),
 ("Polyester Vortex","Viscose Vortex"),("C/P & CVC","P/C 65/35"),("Cotton-Viscose","Micro Modal-Cotton"),("Recycled rPET","GRS Certified Yarns"),
 ("Tencel / Lyocell","EcoVero / Livaeco"),("Hemp & Hemp Blends","Bamboo"),("100% Flax (Linen)","Linen-Cotton & Linen-Viscose"),
 ("BCF Carpet Yarn","Acrylic"),("Combed Cotton","Polyester Lycra"),("DTY SD vs FD","FDY Bright"),("P/V 65/35","Polyester Ring Spun"),
 ("Neppy Yarn","Multi-count Slub"),("Injection & Core-spun Slub","TFO Twisted Polyester"),("SNZ Mono Covered (S & Z)","Mono Filament"),
 ("Polyester Lycra","Viscose Lycra"),("Superstretch","Nylon Textured"),("Viscose Ring Spun","Modal"),("Dope Dyed Colours","Single & Double Dyed"),
 ("FDY Bright","Viscose Compact"),("Melange","Space Dyed"),("DTY SD vs FD","Polyester Ring Spun"),("Combed Cotton","C/P & CVC"),
 ("Viscose Lycra","P/V 65/35"),("Dope Dyed Colours","Melange"),("Polyester Ring Spun","DTY SD vs FD"),("Viscose Ring Spun","Combed Cotton")]
WNOTE = {49:"Diwali best-sellers", 50:"Year-1 top 10 (part 1)", 51:"Year-1 top 10 (part 2)", 33:"Panipat home furnishing", 34:"Tirupur knitting",
 35:"Surat saree yarns", 36:"Bhiwandi weaving", 18:"Holi colour week", 29:"Sustainable June"}
TH26 = {(2026,11):"Every yarn, deeper",(2026,12):"Every yarn, deeper"}
def cnt(n): return Y[n][1] if n in Y else ""
PLAN = [  # (pillar label, pillar source key, sub-topic slot, sub-topic angle, reel 2)
 ("Motivation","M","A","counts & uses","H · Quote of the week"),
 ("Knowledge","K","A","how to check quality","A · Yarn 101"),
 ("Textile city","H","A","the fabric it makes","D · Textile cities"),
 ("Yarns AI & buyer tips","A","B","counts & uses","G · Buyer tips / Yarns AI"),
 ("Fabric","F","B","buying guide","B · Yarn to fabric"),
 ("Our floor","B","AB","A vs B: which one, when","E · Behind our floor / C · Looms"),
 ("Shivpriya story","V","AB","week recap","F · The Shivpriya story")]
SRC = {"M":MOT,"K":KNOW,"H":HUB,"A":AI,"F":FAB,"B":BTS,"V":VAL}
def rows():
    out, cyc = [], {k: itertools.count() for k in SRC}
    for i in range(365):
        dt = START + datetime.timedelta(days=i); w = i // 7; wd = dt.weekday()
        a, b = WEEKS[min(w, len(WEEKS) - 1)]
        lab, k, slot, ang, r2 = PLAN[wd]
        key = SRC[k][next(cyc[k]) % len(SRC[k])]; top = key + (" - which yarn" if k == "F" else "")
        c1 = f"<font color='#1F4E9C'><b>{lab}</b></font> · {top}"
        if slot == "A": c2, rr = f"<b>{a}</b> · {ang} ({cnt(a)})", a
        elif slot == "B": c2, rr = f"<b>{b}</b> · {ang} ({cnt(b)})", b
        elif ang == "week recap": c2, rr = f"<b>{a} + {b}</b> · week recap", "week recap"
        else: c2, rr = f"<b>{a} vs {b}</b> · which one, when", f"{a} vs {b}"
        th = TH26.get((dt.year, dt.month)) or THEME[(dt.year, dt.month)]
        out.append(dict(pk=k, pkey=key, plab=lab, slot=slot, ang=ang, n=i+1, dt=dt, th=th, week=w+1, wa=a, wb=b, wnote=WNOTE.get(w, ""), c1=c1, c2=c2, r1=f"Sub-topic reel: {rr}", r2=r2, fe=FALL.get(dt, "")))
    return out
