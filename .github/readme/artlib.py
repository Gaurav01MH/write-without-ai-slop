"""Shared helpers for the README art: palette, fonts, text and pen geometry, keyframes."""
import random
from pathlib import Path

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


def stops(name, loop, points):
    """Keyframes from (second, css) pairs. Each pair is a state at that second; states ease linearly between."""
    out = ""
    for t, css in points:
        out += f"{min(100, max(0, t / loop * 100)):.3f}%{{{css}}}"
    return f"@keyframes {name}{{{out}}}"

def run(name, loop, extra=""):
    """A class rule that plays keyframes `name` forever over `loop` seconds."""
    return f".{name}{{animation:{name} {loop}s linear infinite;{extra}}}"

REDUCE = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
