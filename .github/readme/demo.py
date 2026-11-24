"""The before and after, drawn as two sheets of paper on a night desk. The text is the example in the README."""
from artlib import stops, run, esc, pen, anim, PEN, MONO, SANS
from pixel import *

SCALE = 1.4
CWD = 7.2      # width of one monospace character at 12 px
FS = 12


def demo():
    L, W, H = 16.0, 600, 336
    before = ["Here's the thing: shipping fast", "isn't just about speed, it's", "about trust.", "",
              "Last month our team cut the", "checkout bug backlog from 42 to", "9 in two weeks. Not just a win", "for engineering, but a win for",
              "customers, for the business, and", "for the future.", "", "Agree? What's your biggest lesson?"]
    after = ["Shipping fast builds trust.", "", "Last month our team cut the", "checkout bug backlog from 42 to", "9 in two weeks."]
    # (line, first char, last char), struck in this order; the number marks the pattern it belongs to
    strikes = [(0, 0, 17), (1, 0, 28), (2, 0, 5), (6, 16, 30), (7, 0, 30), (8, 0, 32), (9, 0, 15), (11, 0, 34)]
    times = [1.0, 2.0, 2.4, 3.6, 4.0, 4.4, 4.8, 6.0]
    y0, step = 62, 19
    ys = [y0 + i * step for i in range(len(before))]
    cw_, ch = 276, 292
    xl, xr, top = 10, 314, 16
    css, body = [f".pen{{fill:none;stroke:{PEN};stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}}"
                 f".ink{{fill:#2a2a2a}}.ok{{fill:#1d6b3a}}"], []
    body.append(stars(W, H, 30, 91, 40))
    for x in (xl, xr):
        body.append(f'<rect x="{x}" y="{top}" width="{cw_}" height="{ch}" rx="10" fill="{PAPER2}" stroke="#e4dcc8" stroke-width="2"/>')
    body.append(f'<text class="sans" x="{xl+16}" y="{top+26}" style="font-size:12px;font-weight:700;letter-spacing:.14em;fill:#8a8068">BEFORE</text>')
    css.append(anim("aft", 7.0, .5, "fade") + run("aft", L))
    body.append(f'<g class="aft"><text class="sans" x="{xr+16}" y="{top+26}" style="font-size:12px;font-weight:700;letter-spacing:.14em;fill:#1d6b3a">AFTER</text>')
    # the numbers stay: highlight them in both sheets
    def hl(x, y, i, n): return f'<rect x="{x+16+i*CWD-1.5:.1f}" y="{y-12}" width="{n*CWD+3:.1f}" height="16" rx="2.5" fill="{MARK}" opacity=".85"/>'
    body.append("</g>")
    body.append(hl(xl, ys[5], 26, 2) + hl(xl, ys[6], 0, 1))
    for i, t in enumerate(before):
        if t:
            body.append(f'<text class="ink" x="{xl+16}" y="{ys[i]}" style="font-size:{FS}px" textLength="{len(t)*CWD:.1f}" lengthAdjust="spacingAndGlyphs">{esc(t)}</text>')
    for k, ((li, a, b), t) in enumerate(zip(strikes, times)):
        css.append(anim(f"s{k}", t, .5, "draw") + f".s{k}{{stroke-dasharray:1;stroke-dashoffset:0;animation:s{k} {L}s linear infinite}}")
        body.append(f'<path class="pen s{k}" pathLength="1" d="{pen(xl+16+a*CWD-2, xl+16+b*CWD+2, ys[li]-4, 300+k)}"/>')
    # the after sheet, line by line
    aft = []
    aft.append(hl(xr, ys[3], 26, 2) + hl(xr, ys[4], 0, 1))
    for i, t in enumerate(after):
        if t:
            aft.append(f'<text class="ink ok" x="{xr+16}" y="{ys[i]}" style="font-size:{FS}px" textLength="{len(t)*CWD:.1f}" lengthAdjust="spacingAndGlyphs">{esc(t)}</text>')
    css.append(anim("al", 7.4, .8, "fade") + run("al", L))
    body.append(f'<g class="al">{"".join(aft)}</g>')
    # the facts, kept: two coins and a check
    css.append(anim("cn", 9.0, .6, "fade") + run("cn", L))
    coin = lambda cx, cy, t: (f'<circle cx="{cx}" cy="{cy}" r="17" fill="{GOLD}" stroke="#c98a14" stroke-width="2.5"/><circle cx="{cx}" cy="{cy}" r="11" fill="none" stroke="#e6a92c" stroke-width="1.6"/>'
                               f'<text x="{cx}" y="{cy+5}" style="font-size:14px;font-weight:800;fill:#7a4a05;text-anchor:middle">{t}</text>')
    body.append(f'<g class="cn">{coin(xr+52, top+ch-50, "42")}{coin(xr+98, top+ch-50, "9")}{icon(CHECK, GREEN, 5, xr+cw_-60, top+ch-66)}</g>')
    cmd = "npx skills add nocodeanish/write-without-ai-slop"
    body.append(f'<text style="font-size:11px;fill:#8d95b3" x="{W/2}" y="{H-8}" text-anchor="middle" textLength="{len(cmd)*6.6:.0f}" lengthAdjust="spacingAndGlyphs">{cmd}</text>')
    css.append(f"@keyframes all{{0%,92%{{opacity:1}}97%,100%{{opacity:0}}}}.all{{animation:all {L}s linear infinite}}")
    return night(W, H, "A short draft on the left, marked up with a red pen: a setup before the point, a not-just-X contrast, a group of three and a bait question are struck through. On the right, the same draft after the edit, with the numbers 42 and 9 kept, shown as two gold coins and a green check.",
                 f'<g class="all">{"".join(body)}</g>', "".join(css), ".al,.aft,.cn{opacity:1}", scale=SCALE)
