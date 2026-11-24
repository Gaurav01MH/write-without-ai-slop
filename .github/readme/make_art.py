#!/usr/bin/env python3
"""Build the README art for write-without-ai-slop: paper and a red pen.

Usage:
    python3 .github/readme/make_art.py            write every SVG in this folder
    python3 .github/readme/make_art.py --check    exit 1 if the files on disk differ from a fresh build

Standard library only. The output is deterministic, so --check can run in CI.
The art holds no version or test counts, so it never goes stale when those change.
The text and the pen strokes are positioned with textLength, so they line up in any font.
"""
import sys
from pathlib import Path
from artlib import *
from panels import PANELS

HERE = Path(__file__).resolve().parent

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
    ML = 14.0
    for ci, (t, say, desc, sample) in enumerate(cards):
        mark = len(body)
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
        grp = "".join(body[mark:]); del body[mark:]
        css += stops(f"m{ci}", ML, [(0, "opacity:0;transform:translateY(14px)"), (.4 + ci * 1.1, "opacity:0;transform:translateY(14px)"), (1.0 + ci * 1.1, "opacity:1;transform:translateY(0)"), (ML - 1.2, "opacity:1;transform:translateY(0)"), (ML - .6, "opacity:0;transform:translateY(0)"), (ML, "opacity:0;transform:translateY(14px)")]) + run(f"m{ci}", ML)
        body.append(f'<g class="m{ci}">{grp}</g>')
        y += card_h + 12
    css += REDUCE
    return svg(640, y - 2, "The three ways to use it. Check lists problems with the quoted line and a short fix. Rewrite returns the smallest edit and a Changed list. Write follows the rules while the agent writes and returns only the text.",
               "".join(body), css)

ART = PANELS + (("demo", demo), ("modes", modes))


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
