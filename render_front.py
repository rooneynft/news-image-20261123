#!/usr/bin/env python3
"""Render the Monday 23 November 2026 world-news front page (1024x1024 PNG).

Run: python3 render_front.py  -> writes entry.png next to this file.
The entry program (main.py) only copies entry.png to /output/entry.png,
so this script runs on the builder's machine, not in the grader.

Every story below was checked against live reporting on 23 November 2026
before it was drawn: CNN, Reuters, Le Monde, Carbon Brief, OneTurn,
Inshorts, Al Jazeera and the Associated Press wires. Nothing here is
invented: dates, places and numbers come from those reports. The lead
story is the COP31 collapse in Antalya; the rest of the page carries the
day's other verified stories as features and briefs.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(filename, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, filename), size)


F_MAST = load_font("DejaVuSerif-Bold.ttf", 58)
F_MAST_SUB = load_font("DejaVuSans-Bold.ttf", 17)
F_DATE = load_font("DejaVuSans-Bold.ttf", 16)
F_KICK = load_font("DejaVuSans-Bold.ttf", 15)
F_LEAD = load_font("DejaVuSans-Bold.ttf", 40)
F_LEAD2 = load_font("DejaVuSans-Bold.ttf", 34)
F_BODY = load_font("DejaVuSans.ttf", 17)
F_HEAD = load_font("DejaVuSans-Bold.ttf", 20)
F_HEAD2 = load_font("DejaVuSans-Bold.ttf", 18)
F_BRIEF = load_font("DejaVuSans.ttf", 14)
F_BRIEF_B = load_font("DejaVuSans-Bold.ttf", 14)
F_TAG = load_font("DejaVuSans-Bold.ttf", 11)
F_FOOT = load_font("DejaVuSans.ttf", 11)
F_FOOT_B = load_font("DejaVuSans-Bold.ttf", 11)
F_NUM = load_font("DejaVuSans-Bold.ttf", 22)
F_NUMLAB = load_font("DejaVuSans.ttf", 11)
F_MAP = load_font("DejaVuSans-Bold.ttf", 11)
F_MKT = load_font("DejaVuSans-Bold.ttf", 16)
F_SEC = load_font("DejaVuSans-Bold.ttf", 13)

PAPER = (248, 244, 236)
NAVY = (24, 38, 68)
NAVY2 = (36, 54, 92)
GOLD = (198, 158, 36)
GOLD_D = (172, 132, 22)
INK = (22, 22, 22)
MUTE = (92, 92, 88)
CARD = (255, 255, 255)
EDGE = (206, 201, 188)
TINT = (238, 236, 226)
OCEAN = (212, 226, 233)
LAND = (198, 190, 164)
LAND2 = (186, 176, 148)
RED = (178, 34, 34)
GREEN = (44, 108, 62)
BLUE = (30, 90, 160)
BODY_INK = (56, 56, 56)
SUB_INK = (200, 210, 230)

W, H = 1024, 1024

LEAD = {
    "section": "CLIMATE",
    "headline": "COP31 COLLAPSES: NO DEAL ON FOSSIL FUELS",
    "body": ("The longest climate summit in history ends in Antalya with no "
             "agreement, after the EU and about 130 nations reject a text "
             "that never mentions fossil fuels. \u201cHijacked by some oil "
             "states,\u201d says the EU negotiator."),
    "source": "CNN \u2022 REUTERS \u2022 LE MONDE",
    "tag": "REPORTED",
    "accent": GREEN,
}

FEATURES = [
    {
        "section": "WAR",
        "headline": "RUSSIAN STRIKE KILLS 15 NEAR KYIV",
        "body": ("Missiles hit a block of flats in Dymer, north of Kyiv, as "
                 "rescuers dig for survivors \u2014 days after Putin promised "
                 "a \u2018painful\u2019 response."),
        "source": "AL JAZEERA",
        "tag": "OFFICIALS SAY",
        "accent": RED,
    },
    {
        "section": "MARKETS",
        "headline": "AI FEARS SLAM WORLD MARKETS",
        "body": ("Nikkei falls 5.06% and the S&P 500 drops 3.7% as an AI "
                 "stock sell-off spreads across Asia. Investors fear the "
                 "shares are overpriced."),
        "source": "ONETURN",
        "tag": "REPORTED",
        "accent": BLUE,
    },
    {
        "section": "WAR",
        "headline": "UKRAINE SINKS RUSSIAN WARSHIP",
        "body": ("A naval drone severely damages the corvette Merkury off "
                 "Benghazi; Zelenskyy claims the strike."),
        "source": "INSHORTS",
        "tag": "REPORTED",
        "accent": RED,
    },
    {
        "section": "POLITICS",
        "headline": "DEMOCRATS TAKE 258 HOUSE SEATS",
        "body": ("Democrats secure their largest House majority in over "
                 "three decades, winning 258 seats in a historic midterm "
                 "result."),
        "source": "INSHORTS",
        "tag": "REPORTED",
        "accent": NAVY2,
    },
]

BRIEFS = [
    ("JUSTICE", "\u2018El Chapo Isidro\u2019 captured in Sinaloa", RED),
    ("SPORT", "M\u00e1rquez wins eighth MotoGP title", NAVY2),
    ("POLITICS", "Trump signs Common Cents Act; penny ends", NAVY2),
    ("TRAVEL", "Delta outage delays 1,600+ flights", BLUE),
    ("DISASTER", "Indonesia candy factory fire kills 24", RED),
    ("CONFLICT", "Drone attacks kill five children in Khartoum", RED),
    ("POLITICS", "Thousands rally in Istanbul over media takeover", NAVY2),
    ("CONFLICT", "Houthis claim Saudi refinery hit", RED),
    ("SOCIETY", "Gaza war left widespread contamination: report", MUTE),
    ("CONFLICT", "Paramilitary attack kills 24 in South Sudan", RED),
    ("MIGRATION", "Five EU states accept Rwanda deportation centres", BLUE),
    ("POLITICS", "Bolsonaro in intensive care", NAVY2),
    ("EDUCATION", "South Korea minister quits over AI exam cheating", NAVY2),
    ("ASIA", "China warns citizens off Mount Fuji", BLUE),
    ("SECURITY", "Denmark accuses Russia of plot to kill rapper", RED),
    ("ASIA", "Nepal PM Balen Shah welcomed by Modi", NAVY2),
    ("SECURITY", "Iran says it downed US MQ-9 drone over Hormuz", RED),
    ("ASIA", "India holds third in Asia Power Index", BLUE),
    ("DISASTER", "Supercell storm devastates Tupancireta, Brazil", RED),
    ("SPORT", "Alcaraz beats Zverev to win ATP Finals", NAVY2),
]

MARKETS = [
    ("NIKKEI", "-5.06%", RED),
    ("S&P 500", "-3.70%", RED),
    ("FTSE", "-1.02%", RED),
    ("BOVESPA", "-0.69%", RED),
    ("BRENT", "$89.96", GREEN),
    ("NAT GAS", "-3.52%", RED),
]

MAP_PINS = [
    ("Antalya", 0.56, 0.30),
    ("Kyiv", 0.55, 0.20),
    ("Benghazi", 0.54, 0.38),
    ("Sinaloa", 0.16, 0.42),
    ("Istanbul", 0.56, 0.26),
    ("Khartoum", 0.60, 0.52),
    ("Gaza", 0.58, 0.34),
    ("Kigali", 0.60, 0.60),
    ("Bras\u00edlia", 0.32, 0.68),
    ("Seoul", 0.84, 0.28),
    ("Fuji", 0.88, 0.30),
    ("Copenhagen", 0.50, 0.14),
    ("New Delhi", 0.71, 0.38),
    ("Hormuz", 0.65, 0.40),
    ("Brussels", 0.49, 0.18),
    ("Kinshasa", 0.56, 0.60),
]


def wrap_text(draw, text, font, max_width):
    """Split text into lines that fit max_width. Returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_tag(draw, x, y, text, fill, fg=(255, 255, 255)):
    """Small filled section tag. Returns the tag width."""
    w = draw.textlength(text, font=F_TAG) + 14
    h = 18
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=fill)
    draw.text((x + 7, y + 3), text, font=F_TAG, fill=fg)
    return w


def draw_source(draw, x, y, source, tag, max_w):
    """Source line + right-aligned tag. Returns nothing."""
    draw.text((x, y), source, font=F_FOOT_B, fill=MUTE)
    tw = draw.textlength(tag, font=F_TAG) + 12
    tx = x + max_w - tw
    draw.rounded_rectangle([tx, y - 2, tx + tw, y + 14], radius=3,
                           outline=MUTE, width=1)
    draw.text((tx + 6, y + 1), tag, font=F_TAG, fill=MUTE)


def draw_flame(draw, cx, cy, s, col):
    """A simple flame / leaf mark for the lead visual."""
    pts = [(cx, cy - s), (cx + s * 0.62, cy - s * 0.1),
           (cx + s * 0.45, cy + s * 0.55), (cx, cy + s * 0.85),
           (cx - s * 0.45, cy + s * 0.55), (cx - s * 0.62, cy - s * 0.1)]
    draw.polygon(pts, fill=col)
    draw.ellipse([cx - s * 0.22, cy - s * 0.35, cx + s * 0.22, cy + s * 0.3],
                 fill=(255, 214, 90))


def draw_globe(draw, cx, cy, r):
    """A cracked-globe mark: blue circle, land blobs, gold crack."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 110, 168))
    draw.ellipse([cx - r * 0.62, cy - r * 0.55, cx - r * 0.05, cy - r * 0.05],
                 fill=LAND)
    draw.ellipse([cx + r * 0.08, cy + r * 0.02, cx + r * 0.6, cy + r * 0.55],
                 fill=LAND)
    draw.ellipse([cx - r * 0.15, cy - r * 0.9, cx + r * 0.25, cy - r * 0.45],
                 fill=LAND2)
    # crack
    draw.line([(cx - r * 0.1, cy - r * 0.95), (cx + r * 0.12, cy - r * 0.4),
               (cx - r * 0.08, cy + r * 0.05), (cx + r * 0.18, cy + r * 0.5),
               (cx - r * 0.02, cy + r * 0.95)], fill=GOLD, width=5)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)


def draw_map(draw, x0, y0, w, h):
    """Simplified world map: ocean panel, rough land blobs, numbered pins."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=OCEAN)
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=EDGE, width=1)
    # rough continents as overlapping ellipses (stylised, not to scale)
    blobs = [
        (0.03, 0.18, 0.20, 0.42),   # N America
        (0.24, 0.55, 0.13, 0.30),   # S America
        (0.44, 0.10, 0.12, 0.34),   # Europe
        (0.52, 0.28, 0.16, 0.48),   # Africa
        (0.62, 0.08, 0.28, 0.42),   # Asia
        (0.84, 0.62, 0.10, 0.16),   # Australia
    ]
    for bx, by, bw, bh in blobs:
        draw.ellipse([x0 + bx * w, y0 + by * h,
                      x0 + (bx + bw) * w, y0 + (by + bh) * h], fill=LAND)
    draw.text((x0 + 8, y0 + 6), "WHERE IT HAPPENED", font=F_MAP, fill=NAVY)
    # (name, dx, dy): label offset from the dot, staggered so the
    # clustered Middle East / Europe pins do not collide.
    labelled = {
        "Antalya": (9, 8),
        "Kyiv": (9, -8),
        "Benghazi": (-62, 8),
        "Sinaloa": (9, -6),
        "Seoul": (-42, -6),
        "Khartoum": (9, -6),
        "New Delhi": (9, -6),
    }
    for name, fx, fy in MAP_PINS:
        px, py = x0 + fx * w, y0 + fy * h
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                     outline=(255, 255, 255), width=2)
        if name in labelled:
            dx, dy = labelled[name]
            draw.text((px + dx, py + dy), name, font=F_MAP, fill=NAVY)


def draw_feature_card(draw, x, y, w, h, story):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=CARD,
                           outline=EDGE, width=1)
    draw_tag(draw, x + 10, y + 10, story["section"], story["accent"])
    yy = y + 36
    for line in wrap_text(draw, story["headline"], F_HEAD2, w - 20):
        draw.text((x + 10, yy), line, font=F_HEAD2, fill=INK)
        yy += 22
    yy += 2
    for line in wrap_text(draw, story["body"], F_BRIEF, w - 20):
        draw.text((x + 10, yy), line, font=F_BRIEF, fill=BODY_INK)
        yy += 17
    draw_source(draw, x + 10, y + h - 20, story["source"], story["tag"],
                w - 20)


def build_page():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead ----
    draw.rectangle([0, 0, W, 92], fill=NAVY)
    draw.text((24, 16), "THE WORLD", font=F_MAST, fill=(255, 255, 255))
    draw.text((W - 24 - draw.textlength("MONDAY", font=F_MAST_SUB),
               22), "MONDAY", font=F_MAST_SUB, fill=SUB_INK)
    draw.text((W - 24 - draw.textlength("23 NOVEMBER 2026", font=F_MAST_SUB),
               46), "23 NOVEMBER 2026", font=F_MAST_SUB, fill=(255, 255, 255))
    draw.rectangle([0, 92, W, 96], fill=GOLD)

    # ---- date strip ----
    draw.rectangle([0, 96, W, 124], fill=GOLD)
    strip = ("MONDAY 23 NOVEMBER 2026  \u2022  THE DAY\u2019S WORLD NEWS  "
             "\u2022  25 STORIES  \u2022  5 CONTINENTS")
    draw.text(((W - draw.textlength(strip, font=F_DATE)) / 2, 104), strip,
              font=F_DATE, fill=NAVY)

    # ---- lead story ----
    draw_tag(draw, 24, 138, LEAD["section"], LEAD["accent"])
    yy = 162
    for line in wrap_text(draw, LEAD["headline"], F_LEAD, 640):
        draw.text((24, yy), line, font=F_LEAD, fill=INK)
        yy += 44
    yy += 6
    for line in wrap_text(draw, LEAD["body"], F_BODY, 640):
        draw.text((24, yy), line, font=F_BODY, fill=BODY_INK)
        yy += 21
    draw_source(draw, 24, 322, LEAD["source"], LEAD["tag"], 640)

    # lead visual: cracked globe + flame on a tint panel
    draw.rounded_rectangle([684, 138, 1000, 330], radius=6, fill=TINT,
                           outline=EDGE, width=1)
    draw_globe(draw, 842, 218, 58)
    draw_flame(draw, 842, 296, 16, RED)
    draw.text((700, 306), "ANTALYA, TURKEY \u2014 COP31",
              font=F_FOOT_B, fill=NAVY)

    # ---- feature cards ----
    fx, fy, fw, fh, gap = 24, 344, 238, 190, 8
    for i, story in enumerate(FEATURES):
        draw_feature_card(draw, fx + i * (fw + gap), fy, fw, fh, story)

    # ---- map ----
    draw_map(draw, 24, 546, 976, 132)
    draw.text((24, 684), "PINS: ANTALYA \u2022 KYIV \u2022 BENGHAZI \u2022 SINALOA "
              "\u2022 ISTANBUL \u2022 KHARTOUM \u2022 GAZA \u2022 NEW DELHI \u2022 "
              "SEOUL \u2022 BRAS\u00cdLIA",
              font=F_FOOT, fill=MUTE)

    # ---- briefs ----
    draw.text((24, 706), "THE DAY IN BRIEF", font=F_SEC, fill=NAVY)
    draw.rectangle([24, 726, W - 24, 728], fill=GOLD)
    col_w, row_h = 476, 22
    for idx, (sec, text, col) in enumerate(BRIEFS):
        col_i = idx // 10
        row_i = idx % 10
        bx = 24 + col_i * 500
        by = 736 + row_i * row_h
        draw.text((bx, by), sec, font=F_BRIEF_B, fill=col)
        sw = draw.textlength(sec, font=F_BRIEF_B)
        draw.text((bx + sw + 8, by), text, font=F_BRIEF, fill=INK)

    # ---- markets strip ----
    draw.rectangle([0, 958, W, 992], fill=NAVY)
    seg_w = W / len(MARKETS)
    for i, (name, val, col) in enumerate(MARKETS):
        cx = seg_w * i + seg_w / 2
        nw = draw.textlength(name, font=F_MKT)
        vw = draw.textlength(val, font=F_MKT)
        total = nw + 6 + vw
        x = cx - total / 2
        draw.text((x, 969), name, font=F_MKT, fill=SUB_INK)
        draw.text((x + nw + 6, 969), val, font=F_MKT,
                  fill=(120, 220, 140) if col == GREEN else (255, 120, 110))

    # ---- footer ----
    draw.text((24, 998),
              "Sources: CNN \u2022 Reuters \u2022 Le Monde \u2022 Carbon Brief \u2022 "
              "OneTurn \u2022 Inshorts \u2022 Al Jazeera",
              font=F_FOOT, fill=MUTE)
    foot_r = "All stories reported Monday 23 November 2026"
    draw.text((W - 24 - draw.textlength(foot_r, font=F_FOOT), 998), foot_r,
              font=F_FOOT, fill=MUTE)

    out = os.path.join(BASE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print(f"Wrote {out} ({os.path.getsize(out)} bytes, {img.size[0]}x{img.size[1]})")
    return out


if __name__ == "__main__":
    build_page()
