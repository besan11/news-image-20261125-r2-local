# render.py — draws the 1024x1024 newspaper front page for news-image-20261125.
# Run: python3 render.py  -> writes entry.png next to this file.
# All text, dates and numbers come from the verified news brief for
# Wednesday 25 November 2026 (see NOTES.md). Fonts are Liberation
# TTF files shipped in fonts/ — no base64 fonts, no network.
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (246, 239, 219)
PAPER2 = (250, 244, 228)
INK = (20, 20, 20)
GREY = (90, 86, 76)
RED = (176, 30, 30)
DRED = (143, 22, 22)
BLUE = (31, 78, 121)
LAND = (216, 201, 163)
SEA = (168, 197, 218)
LIGHT = (232, 222, 196)

REGION = {
    "EUROPE": (31, 78, 121),
    "NORTH AMERICA": (176, 30, 30),
    "MIDDLE EAST": (159, 110, 20),
    "ASIA": (46, 125, 50),
    "AFRICA": (192, 86, 33),
    "LATIN AMERICA": (107, 70, 193),
    "PACIFIC": (14, 116, 144),
}

def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", name), size)

SERIF_B = lambda s: font("LiberationSerif-Bold.ttf", s)
SERIF_R = lambda s: font("LiberationSerif-Regular.ttf", s)
SERIF_I = lambda s: font("LiberationSerif-Italic.ttf", s)
SANS_B = lambda s: font("LiberationSans-Bold.ttf", s)
SANS_R = lambda s: font("LiberationSans-Regular.ttf", s)
SANS_I = lambda s: font("LiberationSans-Italic.ttf", s)

def tw(draw, text, f):
    b = draw.textbbox((0, 0), text, font=f)
    return b[2] - b[0]

def th(draw, text, f):
    b = draw.textbbox((0, 0), text, font=f)
    return b[3] - b[1]

def wrap(draw, text, f, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(draw, t, f) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(draw, x, y, text, f, width, fill=INK, leading=None, max_lines=None):
    lines = wrap(draw, text, f, width)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(f.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y

def centre(draw, cx, y, text, f, fill=INK):
    draw.text((cx - tw(draw, text, f) // 2, y), text, font=f, fill=fill)

def pill(draw, x, y, label, fill):
    f = SANS_B(8)
    w = tw(draw, label, f) + 10
    draw.rounded_rectangle([x, y, x + w, y + 13], radius=6, fill=fill)
    draw.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w

def hline(draw, x0, x1, y, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)

def section_bar(draw, y, text):
    draw.rectangle([14, y, 1010, y + 20], fill=INK)
    draw.text((22, y + 4), text, font=SANS_B(11), fill=(255, 255, 255))
    return y + 20

# ---------------------------------------------------------------- data
TRIO = [
    {
        "n": 1, "region": "MIDDLE EAST", "pill": ("CLAIM", (159, 110, 20)),
        "head": "Two tankers hit mines and burn in the Strait of Hormuz",
        "body": "Iran's IRGC Navy says two tankers exploded and caught fire in their engine rooms after hitting mines on an \u201cunauthorised\u201d route; a 3rd was claimed later the same day. No ships, flags or casualties named. Iranian claim only \u2014 no independent confirmation.",
        "src": "Reuters \u2022 IRNA / IRGC \u2022 Just Security",
        "art": "hormuz",
    },
    {
        "n": 2, "region": "NORTH AMERICA", "pill": ("OFFICIAL", BLUE),
        "head": "US proposes sweeping tariffs on 14 trading partners",
        "body": "USTR Jamieson Greer proposes Section 301 duties over \u201cexcess\u201d factory capacity: China 20% (40% if the truce unravels), EU 15%, Vietnam 20%* (35% if talks fail), India 17\u201325%. About 60% of US imports covered. Duties only after a hearing on 25 Jan 2027.",
        "src": "Reuters \u2022 AP 20:00 UTC \u2022 BBC \u2022 Le Monde",
        "art": "tariffs",
    },
    {
        "n": 3, "region": "ASIA", "pill": ("CONFIRMED", (46, 125, 50)),
        "head": "AI sell-off rolls through Asia as chip stocks plunge",
        "body": "KOSPI \u22126.16% to 4,697.51 \u2014 Korea Exchange triggered a 5-minute sell-side halt. Nikkei \u22122.78%, Taiex \u22124.8%. Samsung \u22129.9%, SK Hynix \u221211.1%, SoftBank \u221214.8%. Nasdaq \u22120.62% on Wednesday; chip index \u22120.7% after an 8% morning plunge.",
        "src": "Reuters \u2022 AP 20:19 UTC \u2022 BBC 17:48 UTC",
        "art": "rout",
    },
]

SMALL = [
    (4, "ASIA", "CONFIRMED", "Shenzhou-24 launches \u2014 Pakistan's first astronaut in orbit",
     "Long March-2F from Jiuquan 00:18 UTC; docking 03:56 UTC. Pakistan's Zeeshan Ali \u2014 first foreigner at China's station.",
     "AP \u2022 Xinhua"),
    (5, "MIDDLE EAST", "CLAIM", "Houthis claim strike on Saudi Arabia's biggest refinery",
     "Ras Tanura claimed hit (strike 24 Nov; claim 25 Nov). Coalition: 4 drones destroyed. Smoke over ~600 km\u00b2.",
     "Reuters \u2022 ISW"),
    (6, "AFRICA", "OFFICIAL", "Fuel tanker explodes on Cairo Ring Road \u2014 31 killed",
     "Health Ministry: 31 dead, 21 injured; 27 vehicles destroyed, 39 ambulances sent. Evening, Wednesday (AP 19:33 UTC).",
     "AP \u2022 Reuters \u2022 CNN"),
    (7, "EUROPE", "REPORTED", "Ukraine hits two Rosneft refineries in Samara region",
     "Overnight drone attack 24\u201325 Nov on Syzran + Kuibyshev (~15.5m tonnes/yr). Russia confirms: 1 killed, 145 drones downed.",
     "Reuters \u2022 Kyiv Independent"),
    (8, "MIDDLE EAST", "REPORTED", "Israeli strike kills Hamas security chief in Gaza",
     "Col. Abuelouf (47), wife Noura (41), daughters 15 and 13 killed in Shati camp; a second strike in Karama kills 1 more.",
     "Reuters \u2022 BBC"),
    (9, "PACIFIC", "OFFICIAL", "Solomons signs treaty with Australia \u2014 no foreign base",
     "Australia becomes \u201cprimary security partner\u201d; A$740m (~$490m) over 10 years. Ends the 2022 China pact.",
     "AP \u2022 Reuters"),
    (10, "AFRICA", "REPORTED", "RSF drone strikes kill 19 civilians in Sudan's Blue Nile",
     "Damazin + Roseires hit; hospital count 14. Strikes were Tuesday night 24 Nov \u2014 reported Wednesday 25 Nov.",
     "Reuters \u2022 Al Jazeera"),
    (11, "NORTH AMERICA", "OFFICIAL", "US economy booms but inflation stays hot",
     "Q3 GDP 4.3% (vs 3.5% expected, fastest in 3 years); Oct PCE 3.8% y/y, core 3.3%. Released 13:30 UTC (08:30 ET).",
     "BEA \u2022 AP \u2022 Reuters"),
    (12, "LATIN AMERICA", "CONFIRMED", "All 76 hostages freed as Colombian forces storm market",
     "Troops storm the \u00c9xito in Cartagena after a ~17-hour siege. 1 captor killed, 4 arrested, 0 hostages killed.",
     "Reuters \u2022 AFP \u2022 BBC"),
    (13, "ASIA", "REPORTED", "Nine dead, 17 trapped as flood swamps Indonesian gold mine",
     "Pongkor, Bogor, West Java: bodies recovered Wednesday; 11 escaped; 325 rescuers at the site.",
     "AP \u2022 Reuters"),
]

ALSO = [
    (14, "Leaked Russian data: at least 490,334 soldiers dead in Ukraine (BBC; up to ~700,000 incl. missing)", "EUROPE"),
    (15, "Poland to create no-fly zone on Ukraine border after drone incursion", "EUROPE"),
    (16, "Israeli judges urge dropping most serious charges against Netanyahu", "MIDDLE EAST"),
    (17, "Pope Leo XIV laments COP31 failure \u2014 the 25 Nov news is the Pope's intervention", "EUROPE"),
    (18, "Venice Biennale visitors award first-ever prizes to Nick Cave and India", "EUROPE"),
    (19, "Axios: Anthropic and OpenAI staff fear unreleased models too powerful to release", "NORTH AMERICA"),
    (20, "Six dead, incl. two boys 8 and 10, in plane crash off Mississippi (crash Tue 24 Nov)", "NORTH AMERICA"),
    (21, "US Army blows up entire 5-ton lead-azide stockpile in Iowa", "NORTH AMERICA"),
    (22, "Macy's 100th Thanksgiving Day Parade postponed to Saturday by storm", "NORTH AMERICA"),
    (23, "Steelers bench Aaron Rodgers; Mason Rudolph to start vs Broncos", "NORTH AMERICA"),
    (24, "Jennifer Barreto of Puerto Rico wins Miss Universe 2026", "LATIN AMERICA"),
    (25, "Veteran Nollywood star Pete Edochie dies aged 79", "AFRICA"),
    (26, "Duran Duran guitarist Andy Taylor dies aged 65 \u2014 announced today (died Mon 23 Nov)", "EUROPE"),
    (27, "North Korea expels Swiss diplomat, orders Pyongyang office shut", "ASIA"),
    (28, "UN evacuates 10 Ebola workers trapped by fighting in DR Congo (11,955 cases, 5,867 dead)", "AFRICA"),
    (29, "Islamic State attack kills 2 Syrian security personnel in Hasaka", "MIDDLE EAST"),
    (30, "Ukraine says it hit 5 Russian jets at Savasleyka airfield (3 MiG-31s, 2 Su-34s) \u2014 Ukrainian claim only", "EUROPE"),
    (31, "Gordon Ramsay to lead BBC's revived Top Gear", "EUROPE"),
    (32, "Poundland collapses, putting 11,000 jobs at risk", "EUROPE"),
    (33, "First close-ups of asteroid Dimorphos released by ESA's Hera", "EUROPE"),
    (34, "Australia passes online safety law; Big Tech faces multibillion-dollar fines", "PACIFIC"),
    (35, "King tides could break decades-old records on both US coasts on Thanksgiving week", "NORTH AMERICA"),
]

TIMELINE = [
    ("00:18", "Shenzhou-24 launches from Jiuquan"),
    ("03:56", "Shenzhou-24 docks at Tiangong"),
    ("~06:30", "Cartagena supermarket stormed; 76 freed"),
    ("early hrs", "Hormuz tankers hit mines (IRGC ~09:46 UTC)"),
    ("13:30", "US PCE 3.8% + GDP 4.3% released"),
    ("afternoon", "Ras Tanura claim; Brent $90.82, \u22120.6%"),
    ("18:23", "UN evacuates Ebola workers in DR Congo"),
    ("evening", "Cairo toll 31 dead; Indonesia mine toll 9 dead"),
]

BIG = [
    ("2", "tankers hit mines in Hormuz (3rd claimed)"),
    ("$90.82", "Brent crude, \u22120.6% on the day"),
    ("\u22126.16%", "KOSPI \u2014 Korea halted selling for 5 min"),
    ("14", "partners face US tariffs; ~60% of imports"),
    ("490,334", "Russian soldiers dead \u2014 leaked data (BBC)"),
    ("76", "hostages freed in Cartagena, 0 killed"),
]

REGIONS = [("EUROPE", 10), ("NORTH AMERICA", 8), ("MIDDLE EAST", 5),
           ("ASIA", 4), ("AFRICA", 4), ("LATIN AMERICA", 2), ("PACIFIC", 2)]

# ---------------------------------------------------------------- art
def art_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=GREY)
    d.polygon([(x, y), (x + w, y), (x + w, y + 11), (x + w * 0.62, y + 15),
               (x + w * 0.55, y + 11), (x, y + 13)], fill=LAND)
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + h - 11),
               (x + w * 0.45, y + h - 14), (x, y + h - 11)], fill=LAND)
    d.text((x + 5, y + 2), "IRAN", font=SANS_B(7), fill=GREY)
    lab = "STRAIT OF HORMUZ"
    d.text((x + w - tw(d, lab, SANS_B(7)) - 5, y + 2), lab, font=SANS_B(7), fill=GREY)
    for tx, ty in ((x + 48, y + 36), (x + 182, y + 44)):
        d.rectangle([tx, ty, tx + 66, ty + 12], fill=(25, 35, 55))
        d.rectangle([tx + 10, ty - 8, tx + 28, ty], fill=(25, 35, 55))
        d.rectangle([tx + 40, ty - 5, tx + 52, ty], fill=(25, 35, 55))
        d.polygon([(tx + 16, ty - 8), (tx + 24, ty - 24), (tx + 32, ty - 8)], fill=(230, 120, 20))
        d.polygon([(tx + 28, ty - 8), (tx + 38, ty - 28), (tx + 48, ty - 8)], fill=(240, 170, 30))
        d.ellipse([tx + 42, ty - 22, tx + 60, ty - 8], fill=(110, 110, 110))
        d.ellipse([tx + 54, ty - 30, tx + 68, ty - 16], fill=(140, 140, 140))
    for mx, my in ((x + 140, y + 32), (x + 152, y + 58), (x + 262, y + 34)):
        d.ellipse([mx - 3, my - 3, mx + 3, my + 3], fill=INK)
        d.line([(mx - 6, my), (mx + 6, my)], fill=INK, width=1)
        d.line([(mx, my - 6), (mx, my + 6)], fill=INK, width=1)
    d.text((x + 5, y + h - 11), "2 tankers burning  \u2022  mines in the water", font=SANS_B(7), fill=INK)

def art_tariffs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PAPER2, outline=GREY)
    bars = [("CHINA", 20, "20%"), ("EU", 15, "15%"), ("VIETNAM", 20, "20%*"), ("INDIA", 21, "17\u201325%")]
    base = y + h - 16
    bw = 44
    gap = (w - 4 * bw - 24) // 3
    cx = x + 14
    for name, val, lab in bars:
        bh = int((h - 34) * val / 25.0)
        d.rectangle([cx, base - bh, cx + bw, base], fill=RED)
        d.text((cx + bw // 2 - tw(d, lab, SANS_B(9)) // 2, base - bh - 12), lab, font=SANS_B(9), fill=RED)
        d.text((cx + bw // 2 - tw(d, name, SANS_B(8)) // 2, base + 3), name, font=SANS_B(8), fill=INK)
        cx += bw + gap
    d.text((x + 6, y + 3), "PROPOSED SECTION 301 DUTIES \u2014 % on imports", font=SANS_B(7), fill=GREY)

def art_rout(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PAPER2, outline=GREY)
    for gy in (y + 16, y + 34, y + 52):
        d.line([(x + 8, gy), (x + w - 8, gy)], fill=(210, 200, 175), width=1)
    pts = [(x + 14, y + 22), (x + 70, y + 28), (x + 120, y + 26), (x + 170, y + 40),
           (x + 220, y + 48), (x + 268, y + 60), (x + w - 12, y + 62)]
    d.line(pts, fill=RED, width=3)
    for px, py in pts[::2]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    d.text((x + 8, y + 3), "KOSPI \u22126.16%  \u2022  NIKKEI \u22122.78%  \u2022  TAIEX \u22124.8%", font=SANS_B(8), fill=RED)
    d.text((x + 8, y + h - 13), "Samsung \u22129.9% \u2022 SK Hynix \u221211.1% \u2022 SoftBank \u221214.8%", font=SANS_B(8), fill=INK)

ART = {"hormuz": art_hormuz, "tariffs": art_tariffs, "rout": art_rout}

# ---------------------------------------------------------------- map
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66), (-80, 73), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35), (-80, 26), (-85, 30), (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-60, 0), (-50, 0), (-35, -8), (-40, -20), (-50, -30), (-60, -35), (-70, -40), (-73, -50), (-70, -55), (-75, -40), (-80, -20), (-80, -5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 70), (15, 70), (5, 60), (-5, 58), (-10, 50)],
    [(-6, 35), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15), (43, 11), (48, 11), (51, 10), (44, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -30), (12, -18), (9, -2), (9, 4), (-8, 4), (-15, 10), (-17, 15), (-15, 25), (-10, 30)],
    [(30, 62), (40, 68), (55, 70), (70, 72), (90, 75), (110, 76), (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (162, 58), (158, 52), (150, 45), (140, 40), (135, 35), (130, 33), (127, 35), (122, 38), (120, 30), (115, 22), (108, 18), (105, 10), (100, 8), (97, 15), (92, 21), (88, 22), (80, 15), (75, 10), (72, 20), (66, 25), (60, 25), (55, 26), (50, 29), (48, 30), (43, 28), (40, 32), (36, 36), (33, 40), (30, 45)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (130, -32), (135, -35), (140, -38), (145, -38), (150, -37), (153, -27), (150, -22), (146, -19), (142, -11), (136, -12), (132, -11), (126, -14), (122, -17), (118, -20)],
]
PINS = [(1, 56, 26), (2, -77, 39), (3, 127, 37), (4, 100, 40), (5, 50, 26),
        (6, 31, 30), (7, 50, 53), (8, 34, 31), (9, 160, -9), (10, 34, 11),
        (11, -77, 39), (12, -75, 10), (13, 107, -6)]

def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 238), outline=GREY)
    def px(lon):
        return x + (lon + 180) / 360.0 * w
    def py(lat):
        return y + (75 - lat) / 135.0 * h
    for poly in CONTINENTS:
        d.polygon([(px(lon), py(lat)) for lon, lat in poly], fill=LAND, outline=(120, 105, 70))
    # nudge pin 11 (Washington GDP) slightly below pin 2 so both show
    off = {2: (0, -7), 11: (0, 7), 1: (10, -8), 5: (0, 6), 7: (0, -8), 8: (14, 2), 6: (-12, -6), 10: (0, 12)}
    for n, lon, lat in PINS:
        dx, dy = off.get(n, (0, 0))
        cx, cy = px(lon) + dx, py(lat) + dy
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED, outline=(255, 255, 255), width=1)
        f = SANS_B(8 if n < 10 else 7)
        d.text((cx - tw(d, str(n), f) // 2, cy - 5), str(n), font=f, fill=(255, 255, 255))
    d.text((x + 5, y + h - 11), "Schematic \u2014 pins 1\u201313 = the drawn stories", font=SANS_B(7), fill=GREY)

# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top red kicker bar
    d.rectangle([0, 0, W, 26], fill=RED)
    d.text((14, 7), "THE WORLD IN ONE PAGE", font=SANS_B(11), fill=(255, 255, 255))
    t = "WEDNESDAY 25 NOVEMBER 2026"
    d.text((W - 14 - tw(d, t, SANS_B(11)), 7), t, font=SANS_B(11), fill=(255, 255, 255))

    # masthead
    centre(d, W // 2, 28, "THE WORLD TODAY", SERIF_B(50), INK)
    hline(d, 14, 380, 96, INK, 2)
    hline(d, 644, 1010, 96, INK, 2)
    centre(d, W // 2, 72, "WEDNESDAY 25 NOVEMBER 2026  \u2022  No. 25", SANS_B(13), INK)
    centre(d, W // 2, 100, "Hormuz mined, US tariffs hit 14 partners, Asia's AI rout \u2014 35 stories from 7 regions in one page.",
           SERIF_I(15), INK)

    # count proof + region bar
    centre(d, W // 2, 118, "35 STORIES  \u2022  7 REGIONS  \u2022  13 DRAWN  \u2022  22 ALSO LISTED", SANS_B(11), RED)
    bx, bw_bar, by = 14, 996, 136
    x = bx
    for name, n in REGIONS:
        seg = bw_bar * n // 35
        d.rectangle([x, by, x + seg - 1, by + 13], fill=REGION[name])
        x += seg
    lx = bx
    for name, n in REGIONS:
        c = REGION[name]
        d.rectangle([lx, 153, lx + 8, 153 + 8], fill=c)
        lab = f"{name} {n}"
        d.text((lx + 11, 153), lab, font=SANS_B(8), fill=INK)
        lx += 11 + tw(d, lab, SANS_B(8)) + 12

    # big numbers
    section_bar(d, 166, "THE DAY IN NUMBERS")
    cw = (996 - 5 * 6) // 6
    for i, (num, lab) in enumerate(BIG):
        cx = 14 + i * (cw + 6)
        d.rectangle([cx, 190, cx + cw, 190 + 44], fill=PAPER2, outline=GREY)
        centre(d, cx + cw // 2, 193, num, SERIF_B(17), RED)
        para(d, cx + 6, 214, lab, SANS_R(8), cw - 12, GREY, leading=10, max_lines=2)

    # trio
    section_bar(d, 240, "THE TOP THREE \u2014 WEDNESDAY'S MOST CONSEQUENTIAL STORIES")
    tw3 = 326
    for i, s in enumerate(TRIO):
        px = 14 + i * (tw3 + 9)
        py = 264
        ph = 198
        d.rectangle([px, py, px + tw3, py + ph], fill=(255, 255, 255), outline=INK, width=1)
        d.rectangle([px, py, px + tw3, py + 18], fill=REGION[s["region"]])
        d.text((px + 6, py + 4), f"{s['n']}  \u2022  {s['region']}", font=SANS_B(9), fill=(255, 255, 255))
        pw = pill(d, px + tw3 - 62, py + 3, s["pill"][0], s["pill"][1])
        y = py + 24
        y = para(d, px + 8, y, s["head"], SERIF_B(17), tw3 - 16, INK, leading=19, max_lines=2)
        ART[s["art"]](d, px + 8, y + 2, tw3 - 16, 66)
        y = para(d, px + 8, y + 72, s["body"], SANS_R(10), tw3 - 16, INK, leading=12, max_lines=4)
        d.text((px + 8, py + ph - 13), s["src"], font=SANS_I(8), fill=GREY)

    # timeline
    section_bar(d, 468, "THE DAY IN UTC")
    for i, (t, txt) in enumerate(TIMELINE):
        row, col = divmod(i, 4)
        cx = 14 + col * 251
        cy = 492 + row * 22
        d.rectangle([cx, cy, cx + 243, cy + 19], fill=PAPER2, outline=GREY)
        d.text((cx + 5, cy + 4), t, font=SANS_B(9), fill=RED)
        d.text((cx + 5 + tw(d, t, SANS_B(9)) + 12, cy + 4), txt, font=SANS_R(9), fill=INK)

    # stories 4-13
    section_bar(d, 540, "MORE OF THE DAY \u2014 STORIES 4\u201313")
    cw5 = 194
    for i, (n, reg, pill_lab, head, body, src) in enumerate(SMALL):
        row, col = divmod(i, 5)
        cx = 14 + col * (cw5 + 6)
        cy = 564 + row * 108
        d.rectangle([cx, cy, cx + cw5, cy + 102], fill=(255, 255, 255), outline=GREY)
        d.rectangle([cx, cy, cx + cw5, cy + 4], fill=REGION[reg])
        d.text((cx + 6, cy + 8), f"{n} \u2022 {reg}", font=SANS_B(8), fill=REGION[reg])
        pill(d, cx + cw5 - 58, cy + 7, pill_lab, {"CONFIRMED": (46, 125, 50), "OFFICIAL": BLUE, "REPORTED": (90, 86, 76), "CLAIM": (159, 110, 20)}[pill_lab])
        y = para(d, cx + 6, cy + 24, head, SERIF_B(11), cw5 - 12, INK, leading=13, max_lines=2)
        y = para(d, cx + 6, y + 1, body, SANS_R(8), cw5 - 12, (60, 58, 50), leading=10, max_lines=3)
        d.text((cx + 6, cy + 102 - 11), src, font=SANS_I(7), fill=GREY)

    # also list
    section_bar(d, 780, "ALSO ON WEDNESDAY 25 NOVEMBER \u2014 14\u201335")
    for i, (n, head, reg) in enumerate(ALSO):
        col, row = divmod(i, 11)
        cx = 14 + col * 503
        cy = 804 + row * 10
        d.text((cx, cy), f"{n}.", font=SANS_B(9), fill=RED)
        rw = tw(d, reg, SANS_B(7))
        avail = 503 - 22 - rw - 12
        f9 = SANS_R(9)
        while tw(d, head, f9) > avail and len(head) > 10:
            head = head[:-1]
        if tw(d, head + "\u2026", f9) <= avail and head != ALSO[i][1]:
            head = head.rstrip() + "\u2026"
        d.text((cx + 22, cy), head, font=f9, fill=INK)
        d.text((cx + 503 - rw - 4, cy + 1), reg, font=SANS_B(7), fill=REGION[reg])

    # map + date check
    d.text((14, 922), "WHERE IT HAPPENED", font=SANS_B(11), fill=INK)
    d.text((530, 922), "DATE CHECK \u2014 NOT 25 NOVEMBER", font=SANS_B(11), fill=RED)
    hline(d, 14, 510, 936, INK, 1)
    hline(d, 530, 1010, 936, RED, 1)
    draw_map(d, 14, 940, 496, 66)
    # date-check box (red frame)
    d.rectangle([530, 940, 1010, 1006], outline=RED, width=2)
    dc = ("EXCLUDED: Kyiv bridges smashed (20 Nov) \u2022 Cyclone Akvan (20 Nov) \u2022 Iran strikes Bahrain (21 Nov) \u2022 "
          "Huawei guilty (Tue 24 Nov) \u2022 Houthi strike on Riyadh tower, 11 hurt (24 Nov) \u2022 Dell record quarter (Tue 24 Nov) \u2022 "
          "Anthropic below $83 IPO / Nasdaq \u22121.48% Tue close (24 Nov) \u2022 US consumer confidence 103.3 (Tue 24 Nov) \u2022 "
          "Kilmar \u00c1brego Garc\u00eda leaves US for Spain (night of 24 Nov) \u2022 Hormuz incidents Mon 23 + Tue 24 Nov \u2022 "
          "COP31 collapse itself (~20\u201323 Nov) \u2022 Mississippi crash itself (Tue 24 Nov) \u2022 Sudan Damazin strikes (Tue night 24 Nov) \u2022 "
          "Andy Taylor's death (Mon 23 Nov).  NOT YET: Thanksgiving Thu 26 Nov \u2022 Macy's parade Sat 28 Nov \u2022 "
          "tariffs only after 25 Jan 2027 hearing \u2022 Fed decision 8\u20139 Dec \u2022 Steelers vs Broncos Sat 28 Nov.")
    para(d, 536, 943, dc, SANS_R(8), 468, INK, leading=10, max_lines=7)

    # footer legend
    hline(d, 14, 1010, 1010, INK, 1)
    d.text((14, 1013), "HOW SURE: CONFIRMED = multiple sources \u2022 OFFICIAL = government / institution \u2022 REPORTED = reported 25 Nov \u2022 CLAIM = single-source, unverified \u2014 Sources: Reuters \u2022 AP \u2022 BBC \u2022 BEA \u2022 Xinhua \u2022 Al Jazeera \u2022 AFP \u2022 ISW \u2022 Just Security",
           font=SANS_B(7), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")

if __name__ == "__main__":
    main()
