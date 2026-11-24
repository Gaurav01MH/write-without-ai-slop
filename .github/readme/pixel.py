"""Pixel-art sprites and helpers for the README scenes.

A sprite is a list of equal-length strings. Each character is a colour key from a palette and '.' is empty.
sprite() turns it into SVG rects (runs of the same colour merge into one rect), so a character costs a few hundred bytes.
"""
import math
import random
from artlib import esc, stops, run, svg, MONO, SANS, SERIF, REDUCE, PEN, MARK

SKY, SKY2, STAR = "#0f1628", "#1b2440", "#cfd6f0"
CREAM, PAPER2, DIM, GREEN, GOLD = "#f3ecdc", "#fbf7ee", "#8d95b3", "#4fd18b", "#ffcf4a"
SLOP, SLOP_L, SLOP_D = "#8ac24a", "#bfe685", "#4d7a24"

HIDE = []   # classes that only appear during the animation; hidden when the viewer prefers reduced motion

# ------------------------------------------------------------------ sprites
EDITOR = ["...RRRRR....", "..RRRRRRR...", ".RRRRRRRRR..", "..HSSSSSSH..", "..HSKSSKSH..", "..HSSSSSSH..",
          "...SSSSSS...", "....SSSS....", "..TTCCCCTT..", ".TTTCCCCTTT.", ".STTTCCTTTS.", "..TTTTTTTT..",
          "..TTTTTTTT..", "..TTTTTTTT.."]
LEGS_A = ["..TTT..TTT..", "..TTT..TTT..", ".BBBB..BBBB."]
LEGS_B = ["...TTTTTT...", "...TTTTTT...", "..BBBBBBBB.."]
EDITOR_PAL = {"R": PEN, "H": "#5a3a22", "S": "#f0c9a0", "K": "#1d1d26", "C": CREAM, "T": "#2f8fa8", "B": "#3a2a20"}

BLOB = ["....GGGG....", "..GGGGGGGG..", ".GLLGGGGGGG.", ".GGKGGGGKGG.", ".GGWKGGWKGG.", "GGGGGGGGGGGG",
        "GGGKKKKKKGGG", "GGGGGGGGGGGG", "DGGDGGGGDGGD"]
BLOB_PAL = {"G": SLOP, "L": SLOP_L, "D": SLOP_D, "K": "#16202a", "W": "#ffffff"}

ROBOT = [".....KK.....", ".....KK.....", "..MMMMMMMM..", ".MMWWMMWWMM.", ".MMWKMMWKMM.", ".MMMMMMMMMM.",
         ".MMKKKKKKMM.", "..MMMMMMMM..", ".MMMMMMMMMM.", "MMMMLLLLMMMM", "MMMMLLLLMMMM", ".MMMMMMMMMM.",
         "..KK....KK..", ".KKK....KKK."]

SHEET = ["CCCCCCCCCC", "CIIIIIIIIC", "CCCCCCCCCC", "CIIIIIIIIC", "CCCCCCCCCC", "CIIIIIICCC", "CCCCCCCCCC",
         "CIIIIIIIIC", "CCCCCCCCCC", "CIIIICCCCC", "CCCCCCCCCC"]
SHEET_PAL = {"C": PAPER2, "I": "#b9ad8f"}

EXCL = ["XX", "XX", "XX", "XX", "..", "XX"]
QMARK = [".XXX.", "X...X", "....X", "..XX.", "..X..", ".....", "..X.."]
HEART = [".X.X.", "XXXXX", "XXXXX", ".XXX.", "..X.."]
CHECK = ["......X", ".....XX", "X...XX.", "XX.XX..", ".XXX...", "..X...."]
STARP = ["..X..", ".XXX.", "XXXXX", ".XXX.", "..X.."]
BOLT = ["..XX", ".XX.", "XXXX", "..XX", ".XX.", "X..."]
DROP = ["..X..", "..X..", ".XXX.", "XXXXX", "XXXXX", ".XXX."]
NOTE = ["..XXX", "..X.X", "..X..", "XXX..", "XXX.."]
DOTS = ["X.X.X"]

assert len({len(r) for r in EDITOR + LEGS_A + LEGS_B}) == 1
assert len({len(r) for r in BLOB}) == 1 and len({len(r) for r in ROBOT}) == 1 and len({len(r) for r in SHEET}) == 1


def sprite(grid, pal, s, x=0, y=0):
    """SVG for a pixel sprite at (x, y), s user units per pixel."""
    rects = []
    for r, row in enumerate(grid):
        c = 0
        while c < len(row):
            ch = row[c]
            if ch == ".":
                c += 1
                continue
            e = c
            while e < len(row) and row[e] == ch:
                e += 1
            rects.append(f'<rect x="{c*s}" y="{r*s}" width="{(e-c)*s}" height="{s}" fill="{pal[ch]}"/>')
            c = e
    return f'<g transform="translate({x} {y})" shape-rendering="crispEdges">{"".join(rects)}</g>'


def icon(grid, color, s, x=0, y=0):
    return sprite(grid, {"X": color}, s, x, y)


def monster(i, s):
    """A seeded invader: the same i always gives the same creature."""
    r = random.Random(1000 + i)
    rows = []
    for y in range(7):
        half = [r.random() < .6 for _ in range(4)]
        if y in (1, 2, 3, 4, 5):
            half[1] = half[2] = half[3] = True
        if y == 0:
            half = [False, False, r.random() < .5, True]
        if y == 6:
            half = [r.random() < .6, False, r.random() < .6, False]
        full = half + half[:3][::-1]
        rows.append(["M" if v else "." for v in full])
    rows[2][2] = rows[2][4] = "W"
    rows[3][2] = rows[3][4] = "K"
    rows[4][2:5] = ["K", "K", "K"]
    return ["".join(r) for r in rows]


MONSTER_COLORS = ["#7e8cf0", "#c08af0", "#5fc4d8", "#e08aa8", "#8fd18a", "#f0b45a"]


def monster_pal(i, color=None):
    return {"M": color or MONSTER_COLORS[i % len(MONSTER_COLORS)], "W": "#ffffff", "K": "#1a1f33"}


# ------------------------------------------------------------------ scene helpers
def stars(w, h, count, seed, ymax=None):
    r = random.Random(seed)
    out = []
    for _ in range(count):
        x, y = r.randrange(8, w - 8), r.randrange(8, int(ymax or h * .7))
        sz = r.choice((2, 2, 3))
        out.append(f'<rect x="{x}" y="{y}" width="{sz}" height="{sz}" fill="{STAR}" opacity="{r.choice((.35, .5, .8))}"/>')
    return "".join(out)


def night(w, h, label, body, css, rest="", scale=1):
    bg = (f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SKY}"/>'
          f'<stop offset="1" stop-color="{SKY2}"/></linearGradient><clipPath id="frame"><rect x="0" y="0" width="{w}" height="{h}" rx="18"/></clipPath></defs>'
          f'<g clip-path="url(#frame)"><rect width="{w}" height="{h}" fill="url(#sky)"/>')
    tail = f'</g><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="none" stroke="#2a3558" stroke-width="2"/>'
    base = (f"text{{font-family:{MONO};white-space:pre;fill:{CREAM}}}.sans{{font-family:{SANS}}}.serif{{font-family:{SERIF};font-style:italic;fill:{PEN}}}"
            f".tw{{animation:tw 3.2s steps(1) infinite}}@keyframes tw{{0%,60%{{opacity:1}}61%,100%{{opacity:.15}}}}")
    hide = (",".join(f".{c}" for c in HIDE) + "{opacity:0}") if HIDE else ""
    HIDE.clear()
    reduce = f"@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}{hide}{rest}}}"
    return svg(w, h, label, bg + body + tail, base + css + reduce, scale)


def poof(name, loop, t, cx, cy, color, size=5, reach=2.4):
    """A ring of pixels that bursts out at second t. Returns (svg, css)."""
    bits = ""
    for k in range(8):
        a = k * math.pi / 4
        c = color if k % 2 == 0 else "#ffffff"
        bits += f'<rect x="{math.cos(a)*14-size/2:.1f}" y="{math.sin(a)*14-size/2:.1f}" width="{size}" height="{size}" fill="{c}"/>'
    css = stops(name, loop, [(0, "opacity:0;transform:scale(.3)"), (max(t - .01, 0), "opacity:0;transform:scale(.3)"), (t, "opacity:1;transform:scale(.5)"),
                             (t + .5, f"opacity:0;transform:scale({reach})"), (loop, f"opacity:0;transform:scale({reach})")]) + run(name, loop)
    HIDE.append(name)
    return f'<g transform="translate({cx} {cy})"><g class="{name}">{bits}</g></g>', css


def window(name, loop, a, b, fade=.08, hold=1.0):
    """Keyframes for an element visible only between a and b seconds."""
    HIDE.append(name)
    return stops(name, loop, [(0, "opacity:0"), (a, "opacity:0"), (a + fade, "opacity:1"), (b, "opacity:1"), (b + fade, "opacity:0"), (loop, "opacity:0")]) + run(name, loop)


def digits(name, loop, x, y, times, size, fill, anchor="start"):
    """A counter: shows 0, then 1 at times[0], then 2 at times[1] and so on. Returns (svg, css)."""
    edges = [0] + list(times) + [loop + 1]
    out, css = "", ""
    for n in range(len(times) + 1):
        a, b = edges[n], edges[n + 1]
        pts = [(0, f"opacity:{1 if n == 0 else 0}")]
        if n:
            pts += [(a - .01, "opacity:0"), (a, "opacity:1")]
        if b < loop:
            pts += [(b - .01, "opacity:1"), (b, "opacity:0")]
        pts.append((loop, f"opacity:{0 if b < loop else 1}"))
        if n:
            HIDE.append(f"{name}{n}")
        css += stops(f"{name}{n}", loop, pts) + run(f"{name}{n}", loop)
        out += f'<text class="{name}{n}" x="{x}" y="{y}" style="font-size:{size}px;font-weight:700;fill:{fill};text-anchor:{anchor}">{n}</text>'
    return out, css
