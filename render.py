# render.py — draws entry.png for make.fun bounty news-image-20261120.
#
# "The World in One Picture — Friday 20 November 2026": a flat vector
# newspaper front page, drawn from scratch with Pillow at 2x and
# downscaled to 1024x1024. No network, no photos, no external assets:
# every pixel is computed here, so no headline can come out garbled.
#
# Stories (researched 20 Nov 2026 ~00:30 UTC, checked against Reuters
# wire copy, IMD bulletins, Sensor Tower via Reuters, Space and the BBC):
#   1. Cyclone Akvan makes landfall near Gopalpur, Odisha, around noon
#      IST — 300,000 evacuated, 423 rescue teams, gusts to 110 km/h.
#   2. Trump pushes any Iran decision to 2027: "We'll see what happens
#      after January 1" / "I'm not rushing" (Reuters interviews, reported
#      in the 20 Nov morning editions).
#   3. GTA VI: an estimated $1.84bn by launch day, 19.05m copies —
#      already past The Odyssey's $1.805bn lifetime box office
#      (Sensor Tower estimate, reported 20 Nov).
#   4. Japan's Hayabusa2 abandons its asteroid landing after engine
#      trouble (reported 20 Nov).
#   5. Europe says it is ready for talks with Russia on ending the war
#      in Ukraine (BBC, reported 20 Nov).
# Ticker: Voyager 1 a full light-day from Earth; Fiji declares a national
# disaster over drought; Nicholls 113* in the Wellington Test.
#
# Deliberately NOT used: the ICJ Myanmar ruling, the Kyiv embassy strikes
# and the Riyadh PIF Tower strike — all happened on 19 Nov, so they belong
# to yesterday's front page, not this one.
#
# Run:  python3 render.py   (writes entry.png next to this file)

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

S = 2                      # supersample factor
W, H = 1024, 1024          # final size
CW, CH = W * S, H * S      # canvas size

# --- palette -------------------------------------------------------------
PAPER   = (246, 241, 231)  # warm newsprint
INK     = (26, 26, 26)
SOFTINK = (64, 60, 54)
RED     = (178, 34, 34)
GOLD    = (176, 124, 22)
SEA     = (24, 68, 99)     # Bay of Bengal
SEA_DK  = (16, 50, 76)
SEA_LT  = (46, 104, 138)
LAND    = (222, 199, 156)  # Odisha coast
LAND_DK = (190, 162, 112)
SPIRAL  = (226, 238, 244)
TEAL    = (32, 96, 110)
DARKPANEL = (24, 26, 34)
SUNSET  = [(255, 176, 102), (255, 120, 110), (196, 84, 138), (96, 66, 130)]

# --- fonts ---------------------------------------------------------------
def font(name, size):
    path = "/usr/share/fonts/truetype/liberation/" + name
    return ImageFont.truetype(path, size * S)

SERIF_B  = lambda s: font("LiberationSerif-Bold.ttf", s)
SERIF    = lambda s: font("LiberationSerif-Regular.ttf", s)
SERIF_I  = lambda s: font("LiberationSerif-Italic.ttf", s)
SANS_B   = lambda s: font("LiberationSans-Bold.ttf", s)
SANS     = lambda s: font("LiberationSans-Regular.ttf", s)

img = Image.new("RGB", (CW, CH), PAPER)
d = ImageDraw.Draw(img, "RGBA")

# --- helpers -------------------------------------------------------------
def X(v):
    return int(v * S)

def rect(x0, y0, x1, y1, fill=None, outline=None, width=1):
    d.rectangle([X(x0), X(y0), X(x1), X(y1)], fill=fill,
                outline=outline, width=max(1, int(width * S)))

def line(x0, y0, x1, y1, fill=INK, width=1):
    d.line([X(x0), X(y0), X(x1), X(y1)], fill=fill, width=max(1, int(width * S)))

def text(x, y, s, f, fill=INK, anchor="la"):
    d.text((X(x), X(y)), s, font=f, fill=fill, anchor=anchor)

def tw(f, s):
    """Text width in 1024-space."""
    return d.textlength(s, font=f) / S

def wrap(s, f, max_w):
    """Greedy word wrap to a max width (1024-space)."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tw(f, trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(x, y, s, f, max_w, leading, fill=INK, align="left"):
    """Draw a wrapped paragraph; return y after the last line."""
    for ln in wrap(s, f, max_w):
        if align == "center":
            text(x + max_w / 2, y, ln, f, fill=fill, anchor="ma")
        else:
            text(x, y, ln, f, fill=fill)
        y += leading
    return y

def kicker(x, y, s, fill=RED):
    text(x, y, s, SANS_B(13), fill=fill)

def star(cx, cy, r, fill):
    """Five-point star centred at (cx, cy), radius r (1024-space)."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((X(cx + rr * math.cos(ang)), X(cy + rr * math.sin(ang))))
    d.polygon(pts, fill=fill)

def rule_double(y, x0=40, x1=984):
    line(x0, y, x1, y, fill=INK, width=2.5)
    line(x0, y + 5, x1, y + 5, fill=INK, width=1)

# --- frame ---------------------------------------------------------------
rect(14, 14, 1010, 1010, outline=INK, width=2)
line(20, 20, 1004, 20, fill=INK, width=1)
line(20, 1004, 1004, 1004, fill=INK, width=1)
line(20, 20, 20, 1004, fill=INK, width=1)
line(1004, 20, 1004, 1004, fill=INK, width=1)

# --- masthead ------------------------------------------------------------
text(512, 34, "FRIDAY 20 NOVEMBER 2026", SANS_B(15), fill=RED, anchor="ma")
text(512, 52, "THE WORLD IN ONE PICTURE", SERIF_B(52), anchor="ma")
text(512, 106, "ONE DAY  ·  ONE IMAGE  ·  THE NEWS THAT MATTERED",
     SANS(12), fill=SOFTINK, anchor="ma")
rule_double(126)

# --- LEAD: Cyclone Akvan -------------------------------------------------
kicker(40, 140, "LANDFALL  •  INDIA'S EAST COAST")
text(40, 158, "AKVAN SLAMS INTO ODISHA", SERIF_B(56))
para(40, 222,
     "300,000 people moved to safety as the cyclone comes ashore near "
     "Gopalpur — gusts of 110 km/h and red alerts across Odisha and "
     "Andhra Pradesh.",
     SERIF(20), 944, 26, fill=SOFTINK)

# hero panel: Bay of Bengal + spiral + coast  (y 272..470)
HX0, HY0, HX1, HY1 = 40, 272, 984, 470
rect(HX0, HY0, HX1, HY1, fill=SEA)
# subtle depth bands in the sea
for i, col in enumerate([(20, 58, 86), (24, 68, 99), (28, 78, 110)]):
    rect(HX0, HY0 + i * 66, HX1, HY0 + (i + 1) * 66, fill=col)
# landmass: India's east coast on the right
coast = [(788, 272), (984, 272), (984, 470), (838, 470), (812, 420),
         (796, 372), (782, 330), (788, 272)]
d.polygon([(X(x), X(y)) for x, y in coast], fill=LAND)
d.line([(X(x), X(y)) for x, y in coast], fill=LAND_DK, width=3 * S, joint="curve")
# spiral arms over the sea, centred left of the coast
cx, cy = 430, 372
for arm in range(3):
    phase = arm * 2.094
    pts = []
    for t in range(0, 190):
        th = phase + t * 0.055
        r = 8 + t * 0.62
        pts.append((X(cx + r * math.cos(th)), X(cy + r * math.sin(th) * 0.82)))
    d.line(pts, fill=SPIRAL, width=7 * S, joint="curve")
    pts2 = []
    for t in range(0, 150):
        th = phase + 0.35 + t * 0.055
        r = 16 + t * 0.62
        pts2.append((X(cx + r * math.cos(th)), X(cy + r * math.sin(th) * 0.82)))
    d.line(pts2, fill=(168, 200, 216), width=4 * S, joint="curve")
# calm eye
d.ellipse([X(cx - 17), X(cy - 15), X(cx + 17), X(cy + 15)], fill=(250, 248, 240),
          outline=SPIRAL, width=2 * S)
# rain streaks
for i in range(26):
    rx = 90 + (i * 53) % 560
    ry = 288 + (i * 37) % 160
    line(rx, ry, rx - 7, ry + 16, fill=(150, 190, 208), width=2)
# labels on the map
text(120, 292, "BAY OF BENGAL", SANS_B(15), fill=(168, 200, 216))
text(120, 312, "Severe Cyclonic Storm", SANS(13), fill=(168, 200, 216))
text(862, 300, "ODISHA", SANS_B(16), fill=(90, 70, 40))
text(858, 322, "Gopalpur", SANS(13), fill=(90, 70, 40))
d.ellipse([X(838), X(424), X(850), X(436)], fill=RED, outline=(255, 255, 255), width=2 * S)
text(856, 424, "LANDFALL", SANS_B(12), fill=RED)
text(880, 452, "noon IST", SANS(12), fill=(90, 70, 40))
text(60, 436, "AKVAN", SERIF_B(30), fill=(255, 255, 255))

# stat strip under the hero
SY = 482
for i, (num, lab) in enumerate([("300,000", "EVACUATED"),
                                ("423", "RESCUE TEAMS"),
                                ("110 km/h", "GUSTS")]):
    x0 = 40 + i * 320
    rect(x0, SY, x0 + 304, SY + 46, outline=INK, width=1.5)
    text(x0 + 152, SY + 5, num, SERIF_B(22), fill=RED, anchor="ma")
    text(x0 + 152, SY + 29, lab, SANS_B(11), fill=SOFTINK, anchor="ma")

rule_double(548)

# --- ROW 2: Trump / Iran  |  GTA VI --------------------------------------
# left column: Trump
kicker(40, 566, "WASHINGTON  •  THE IRAN QUESTION")
text(40, 584, "TRUMP: IRAN CAN WAIT", SERIF_B(33))
text(40, 620, "UNTIL 2027", SERIF_B(33))
# calendar card art
rect(40, 664, 190, 748, fill=(255, 255, 255), outline=INK, width=2)
rect(40, 664, 190, 692, fill=RED)
text(115, 668, "JANUARY", SANS_B(13), fill=(255, 255, 255), anchor="ma")
text(115, 694, "2027", SERIF_B(40), fill=INK, anchor="ma")
text(115, 734, "JAN 1", SANS_B(12), fill=SOFTINK, anchor="ma")
para(206, 664,
     "\u201cWe\u2019ll see what happens after January 1.\u201d "
     "\u201cI\u2019m not rushing to make any decisions.\u201d",
     SERIF_I(18), 278, 24, fill=INK)
para(40, 758,
     "The president pushes any decision on new strikes against Iran into "
     "next year — \u201cWe\u2019ve got time.\u201d",
     SERIF(16), 444, 21, fill=SOFTINK)

# right column: GTA VI
GX = 540
line(GX - 16, 566, GX - 16, 800, fill=INK, width=1)
kicker(GX, 566, "ENTERTAINMENT  •  A RECORD LAUNCH")
text(GX, 584, "GTA VI: $1.84BN IN A DAY", SERIF_B(33))
# sunset skyline art
AX0, AY0, AX1, AY1 = GX, 640, 984, 724
for i, col in enumerate(SUNSET):
    rect(AX0, AY0 + i * 21, AX1, AY0 + (i + 1) * 21, fill=col)
# sun
d.ellipse([X(AX0 + 330), X(AY0 + 8), X(AX0 + 380), X(AY0 + 58)],
          fill=(255, 236, 170))
# skyline silhouette
heights = [34, 52, 28, 62, 44, 70, 38, 56, 30, 66, 42, 58, 36]
bx = AX0
for j, hh in enumerate(heights):
    bw = (AX1 - AX0) / len(heights)
    rect(bx, AY1 - hh, bx + bw - 3, AY1, fill=(24, 20, 32))
    bx += bw
para(GX, 734,
     "19 million copies by launch day — already past The Odyssey\u2019s "
     "$1.8bn lifetime box office. (Sensor Tower estimate)",
     SERIF(16), 444, 21, fill=SOFTINK)

rule_double(812)

# --- ROW 3: Hayabusa2  |  Europe talks -----------------------------------
# left: Hayabusa2
kicker(40, 830, "SPACE  •  JAPAN")
text(40, 848, "HAYABUSA2 GIVES UP", SERIF_B(27))
text(40, 878, "ITS ASTEROID LANDING", SERIF_B(27))
para(40, 912,
     "Engine trouble forces JAXA\u2019s probe to change plans — no more "
     "touchdown on the asteroid.",
     SERIF(15), 444, 20, fill=SOFTINK)
# small space art: asteroid + probe, right of the text block is tight;
# draw a slim strip instead: dashed diverted path under the text
d.ellipse([X(404), X(846), X(470), X(912)], fill=(150, 148, 140),
          outline=(110, 108, 100), width=2 * S)
d.ellipse([X(420), X(860), X(436), X(876)], fill=(120, 118, 110))
d.ellipse([X(444), X(884), X(460), X(900)], fill=(120, 118, 110))
# probe: gold body + blue panels
rect(392, 926, 414, 942, fill=(212, 175, 55), outline=INK, width=1)
rect(368, 930, 392, 938, fill=(52, 90, 150))
rect(414, 930, 438, 938, fill=(52, 90, 150))
# dashed path from probe toward asteroid, veering off
for t in range(0, 12):
    px = 404 + t * 5
    py = 920 - t * 6
    d.ellipse([X(px), X(py), X(px + 3), X(py + 3)], fill=RED)

# right: Europe / Ukraine talks
RX = 540
line(RX - 16, 830, RX - 16, 956, fill=INK, width=1)
kicker(RX, 830, "EUROPE  •  UKRAINE")
text(RX, 848, "EUROPE READY FOR", SERIF_B(27))
text(RX, 878, "TALKS WITH RUSSIA", SERIF_B(27))
para(RX, 912,
     "Leaders say they are ready to discuss ending the war in Ukraine.",
     SERIF(15), 444, 20, fill=SOFTINK)
# EU star circle
ccx, ccy = RX + 396, 876
d.ellipse([X(ccx - 34), X(ccy - 34), X(ccx + 34), X(ccy + 34)],
          fill=(28, 62, 130), outline=INK, width=1)
for k in range(12):
    ang = -math.pi / 2 + k * math.pi / 6
    star(ccx + 23 * math.cos(ang), ccy + 23 * math.sin(ang), 4.5,
         fill=(255, 214, 64))

# --- footer ticker -------------------------------------------------------
rect(28, 966, 996, 998, fill=INK)
ticker = ("ALSO TODAY:  Voyager 1 now a light-day from Earth  •  "
          "Fiji declares a drought disaster  •  Nicholls 113* in Wellington")
tf = SANS_B(13)
assert tw(tf, ticker) <= 940, tw(tf, ticker)
text(44, 976, ticker, tf, fill=(255, 255, 255))

out_img = img.resize((W, H), Image.LANCZOS)
out_img.save(OUT, optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
