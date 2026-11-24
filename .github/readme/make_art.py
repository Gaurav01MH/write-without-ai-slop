#!/usr/bin/env python3
"""Build the README art for write-without-ai-slop: paper and a red pen.

Usage:
    python3 .github/readme/make_art.py            write banner.svg, demo.svg, modes.svg next to this file
    python3 .github/readme/make_art.py --check    exit 1 if the files on disk differ from a fresh build

Standard library only. The output is deterministic, so --check can run in CI.
The art holds no version or test counts, so it never goes stale when those change.
The text and the pen strokes are positioned with textLength, so they line up in any font.
"""
import random, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER, EDGE, INK, PEN, MARK = "#fbf7ee", "#e4dcc8", "#2a2a2a", "#d6342b", "#ffe27a"
MONO = 'ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono","Courier New",monospace'
SANS = '-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif'
SERIF = 'Georgia,"Times New Roman",serif'
CW, FS, X0 = 10.8, 18, 28   # monospace cell width at 18px, left margin
LOOP = 20.0                 # seconds

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def line(x, y, s, cls="d"):
    return f'<text class="{cls}" x="{x}" y="{y}" textLength="{len(s)*CW:.1f}" lengthAdjust="spacingAndGlyphs">{esc(s)}</text>'

def pen(x0, x1, y, seed):
    """A hand-drawn strike: gentle wobble, same result every build."""
    r = random.Random(seed)
    pts, x = [], x0
    while x < x1:
        pts.append(x); x += r.uniform(22, 34)
    pts.append(x1)
    d = f"M{x0:.1f},{y + r.uniform(-1, 1):.1f}"
    for a, b in zip(pts, pts[1:]):
        d += f" Q{(a+b)/2:.1f},{y + r.uniform(-3, 3):.1f} {b:.1f},{y + r.uniform(-1.4, 1.4):.1f}"
    return d

def anim(name, start, dur, kind):
    """Keyframes for one element in a LOOP-second cycle: hidden until start, then shown until the end."""
    s, e = start / LOOP * 100, (start + dur) / LOOP * 100
    if kind == "draw":   # pen stroke drawn along its path
        kf = f"0%,{s:.2f}%{{stroke-dashoffset:1;opacity:0}}{s+.01:.2f}%{{opacity:1}}{e:.2f}%,100%{{stroke-dashoffset:0;opacity:1}}"
    else:                # fade in
        kf = f"0%,{s:.2f}%{{opacity:0}}{e:.2f}%,100%{{opacity:1}}"
    return f"@keyframes {name}{{{kf}}}"

def svg(w, h, label, body, css):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-label="{esc(label)}"><title>{esc(label)}</title><style>{css}</style>{body}</svg>\n')

BASE_CSS = (f"text{{font-family:{MONO};font-size:{FS}px;fill:{INK};white-space:pre}}"
            f".lab{{font-family:{SANS};font-size:12px;letter-spacing:.14em;fill:#8a8068}}"
            f".note{{font-family:{SANS};font-size:14px;fill:#6b6350}}"
            f".pen{{fill:none;stroke:{PEN};stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}}"
            f".num{{font-family:{SANS};font-size:12px;font-weight:700;fill:{PEN};text-anchor:middle}}"
            f".ring{{fill:none;stroke:{PEN};stroke-width:1.6}}"
            f".ok{{fill:#1d6b3a}}"
            f".foot2{{font-family:{SERIF};font-style:italic;font-size:16px;fill:#6b6350}}")

# ---------------------------------------------------------------- demo
def demo():
    before = ["Here's the thing: shipping fast isn't just about",
              "speed, it's about trust.", "",
              "Last month our team cut the checkout bug backlog",
              "from 42 to 9 in two weeks. Not just a win for",
              "engineering, but a win for customers, for the",
              "business, and for the future.", "",
              "Agree? What's your biggest lesson?"]
    after = ["Shipping fast builds trust.", "",
             "Last month our team cut the checkout bug backlog",
             "from 42 to 9 in two weeks."]
    y0, step = 76, 28
    ys = [y0 + i * step for i in range(len(before))]
    # (line index, first char, last char, group id)
    strikes = [(0, 0, 17, 1), (0, 32, 48, 2), (1, 0, 17, 2),
               (4, 27, 45, 3), (5, 0, 45, 3), (6, 0, 29, 3), (8, 0, 34, 4)]
    timing = {1: 1.6, 2: 3.4, 3: 5.2, 4: 7.4}      # start second of each pattern
    marks = {1: (0, 580), 2: (0, 606), 3: (6, 368), 4: (8, 424)}  # ringed number: (line, x of centre)
    css, body = [BASE_CSS], []
    body.append(f'<rect x="1" y="1" width="638" height="{622}" rx="14" fill="{PAPER}" stroke="{EDGE}" stroke-width="2"/>')
    body.append('<text class="lab" x="28" y="40">BEFORE</text>')
    # number highlights behind the numbers, before and after
    def hl(line_y, idx, n): return f'<rect x="{X0 + idx*CW - 2:.1f}" y="{line_y - 16}" width="{n*CW + 4:.1f}" height="22" rx="3" fill="{MARK}" opacity=".75"/>'
    body.append(hl(ys[4], 5, 2) + hl(ys[4], 11, 1))
    for i, s in enumerate(before):
        if s: body.append(line(X0, ys[i], s))
    css.append(f".grp{{opacity:1}}")
    for g in (1, 2, 3, 4):
        css.append(anim(f"d{g}", timing[g], .7, "draw") + anim(f"f{g}", timing[g] + .5, .5, "fade"))
        css.append(f".d{g}{{stroke-dasharray:1;stroke-dashoffset:0;animation:d{g} {LOOP}s linear infinite}}.f{g}{{animation:f{g} {LOOP}s linear infinite}}")
    for k, (li, a, b, g) in enumerate(strikes):
        x0, x1 = X0 + a * CW - 3, X0 + b * CW + 3
        body.append(f'<path class="pen d{g}" pathLength="1" d="{pen(x0, x1, ys[li] - 6, 100 + k)}"/>')
    for g, (li, cx) in marks.items():
        cy = ys[li] - 6
        body.append(f'<g class="f{g}"><circle class="ring" cx="{cx:.1f}" cy="{cy}" r="10"/><text class="num" x="{cx:.1f}" y="{cy+4}" textLength="7" lengthAdjust="spacingAndGlyphs">{g}</text></g>')
    ly = ys[-1] + 40
    legend = [(1, "setup before the point"), (2, "“not just X” contrast"), (3, "group of three"), (4, "bait question")]
    # two rows keep every label inside the 640 px sheet
    lx = [28, 330, 28, 330]; ly_list = [ly, ly, ly + 24, ly + 24]
    for (g, t), x, y in zip(legend, lx, ly_list):
        body.append(f'<g class="f{g}"><circle class="ring" cx="{x+9}" cy="{y-4}" r="9"/><text class="num" x="{x+9}" y="{y}">{g}</text>'
                    f'<text class="note" x="{x+26}" y="{y}">{esc(t)}</text></g>')
    ydiv = ly + 52
    body.append(f'<line x1="28" y1="{ydiv}" x2="612" y2="{ydiv}" stroke="{EDGE}" stroke-width="2"/>')
    # after block
    ya = ydiv + 36
    css.append(anim("aft", 9.8, .8, "fade") + f".aft{{animation:aft {LOOP}s linear infinite}}")
    css.append(anim("foot", 11.0, .8, "fade") + f".foot{{animation:foot {LOOP}s linear infinite}}")
    body.append(f'<g class="aft"><text class="lab" x="28" y="{ya}">AFTER</text>')
    ay = [ya + 36 + i * step for i in range(len(after))]
    body.append(hl(ay[3], 5, 2) + hl(ay[3], 11, 1))
    for i, s in enumerate(after):
        if s: body.append(line(X0, ay[i], s, "d ok"))
    body.append('</g>')
    yf = ay[-1] + 44
    body.append(f'<g class="foot"><text class="foot2" x="28" y="{yf}">The numbers stayed. Four patterns went.</text>'
                f'<text x="28" y="{yf+30}" style="font-size:14px;fill:#6b6350" textLength="{len("npx skills add nocodeanish/write-without-ai-slop")*8.4:.1f}" lengthAdjust="spacingAndGlyphs">npx skills add nocodeanish/write-without-ai-slop</text></g>')
    h = yf + 56
    body[0] = body[0].replace('height="622"', f'height="{h-2}"')
    css.append(f"@keyframes all{{0%,93%{{opacity:1}}97%,100%{{opacity:0}}}}.all{{animation:all {LOOP}s linear infinite}}")
    css.append("@media (prefers-reduced-motion:reduce){*{animation:none!important}}")
    inner = "".join(body)
    return svg(640, h, "A short draft marked up with a red pen. Four patterns are struck through and numbered: a setup before the point, a “not just X” contrast, a group of three and a bait question. Below, the same draft after the edit. The numbers 42 and 9 stay.",
               f'<g class="all">{inner}</g>', "".join(css))

# ---------------------------------------------------------------- banner
def banner():
    css = BASE_CSS + f".word{{font-family:{SANS};font-weight:800;font-size:66px;fill:{INK}}}.serif{{font-family:{SERIF};font-style:italic;font-size:30px;fill:{PEN}}}"
    body = [f'<rect x="1" y="1" width="1198" height="198" rx="16" fill="{PAPER}" stroke="{EDGE}" stroke-width="2"/>',
            f'<text class="word" x="48" y="122" textLength="740" lengthAdjust="spacingAndGlyphs">write-without-ai-slop</text>']
    # a small proof sheet, slightly tilted: one phrase struck, one line marked stet
    sheet = (f'<g transform="translate(830 18) rotate(-2.2)">'
             f'<rect x="0" y="0" width="350" height="150" rx="10" fill="#fffdf7" stroke="{EDGE}" stroke-width="2"/>'
             f'<text x="20" y="40" style="font-size:17px" textLength="{len("Here\'s the thing: shipping fast")*10.2:.0f}" lengthAdjust="spacingAndGlyphs">Here\'s the thing: shipping fast</text>'
             f'<path class="pen" d="{pen(17, 17+17*10.2, 34, 7)}"/>'
             f'<text x="20" y="74" style="font-size:17px" textLength="{len("builds trust.")*10.2:.0f}" lengthAdjust="spacingAndGlyphs">builds trust.</text>'
             f'<rect x="18" y="94" width="{len("Backlog: 42 to 9.")*10.2+4:.0f}" height="26" rx="3" fill="{MARK}" opacity=".7"/>'
             f'<text x="20" y="113" style="font-size:17px" textLength="{len("Backlog: 42 to 9.")*10.2:.0f}" lengthAdjust="spacingAndGlyphs">Backlog: 42 to 9.</text>'
             f'<path d="M18,126 q6,5 12,0 t12,0 t12,0 t12,0 t12,0 t12,0 t12,0 t12,0 t12,0 t12,0 t12,0 t12,0 t12,0 t12,0" fill="none" stroke="{PEN}" stroke-width="1.6" stroke-dasharray="2 4" stroke-linecap="round" transform="translate(0 3)"/>'
             f'<text class="serif" x="250" y="114">stet</text></g>')
    body.append(sheet)
    return svg(1200, 200, "write-without-ai-slop", "".join(body), css)


# ---------------------------------------------------------------- modes
def modes():
    css = BASE_CSS + f".h{{font-family:{SANS};font-weight:700;font-size:21px;fill:{INK}}}.s{{font-family:{SANS};font-size:16px;fill:#4a4535}}" \
          f".c{{font-family:{MONO};font-size:15px;fill:{INK}}}"
    cards = [
        ("Check", "Ask it to check a draft.", "Nothing is rewritten. Each finding quotes the line, names the pattern and gives a short fix.",
         ["\u201cHere's the thing:\u201d \u00b7 setup before the point \u00b7 cut it"]),
        ("Rewrite", "Give it a draft.", "The smallest edit that removes the problems, then a short Changed list. Say \u201cpaste as is\u201d and only the text comes back.",
         ["Changed:", "- Cut \u201cHere's the thing:\u201d and the contrast."]),
        ("Write", "Ask your agent to write.", "It follows the rules while it writes and runs the final check on its own draft. Only the text comes back.",
         ["Shipping fast builds trust."]),
    ]
    body, y = [], 10
    for t, say, desc, sample in cards:
        words, lines_, cur = desc.split(), [], ""
        for w in words:
            if len(cur) + len(w) + 1 > 68: lines_.append(cur); cur = w
            else: cur = (cur + " " + w).strip()
        lines_.append(cur)
        box_h = len(sample) * 24 + 14
        card_h = 64 + len(lines_) * 22 + 12 + box_h + 18
        body.append(f'<rect x="1" y="{y}" width="638" height="{card_h}" rx="12" fill="{PAPER}" stroke="{EDGE}" stroke-width="2"/>')
        body.append(f'<text class="h" x="24" y="{y+36}">{t}</text><text class="s" x="140" y="{y+36}">{esc(say)}</text>')
        for j, l in enumerate(lines_):
            body.append(f'<text class="s" x="24" y="{y+66+j*22}">{esc(l)}</text>')
        by = y + 66 + len(lines_) * 22 - 6
        body.append(f'<rect x="24" y="{by}" width="592" height="{box_h}" rx="6" fill="#fffdf7" stroke="{EDGE}"/>')
        for j, l in enumerate(sample):
            body.append(f'<text class="c" x="38" y="{by+24+j*24}">{esc(l)}</text>')
        y += card_h + 12
    return svg(640, y - 2, "The three ways to use it. Check lists problems with the quoted line and a short fix. Rewrite returns the smallest edit and a Changed list. Write follows the rules while the agent writes and returns only the text.",
               "".join(body), css)

ART = (("banner", banner), ("demo", demo), ("modes", modes))


def main(argv):
    built = {f"{name}.svg": fn() for name, fn in ART}
    if "--check" in argv:
        stale = [n for n, text in built.items() if not (HERE / n).exists() or (HERE / n).read_text(encoding="utf-8") != text]
        for n in stale:
            print(f"{n} differs from a fresh build; run make_art.py")
        return 1 if stale else 0
    for n, text in built.items():
        (HERE / n).write_text(text, encoding="utf-8")
        print(n, len(text.encode("utf-8")), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
