"""Animated README panels: the hero, the write flow, the pattern scan, the sameness fix and the install line.

Each function returns one SVG string. All motion is plain CSS keyframes, so it plays inside an <img> on GitHub
without scripts or web fonts. The resting state of every element is its final state, so a viewer with
reduced motion sees a finished picture. Output is deterministic.
"""
import math
from artlib import *

DESK, DESK2, LINE = "#17161d", "#23212c", "#363343"
CREAM, DIM, GREEN = "#f3ecdc", "#9a94a8", "#4fd18b"

DARK = (f"text{{font-family:{MONO};font-size:15px;fill:{CREAM};white-space:pre}}"
        f".sans{{font-family:{SANS}}}.dim{{fill:{DIM}}}.ink{{fill:{INK}}}.green{{fill:{GREEN}}}.red{{fill:{PEN}}}"
        f".lab{{font-family:{SANS};font-size:12px;font-weight:600;letter-spacing:.16em;fill:{DIM}}}"
        f".head{{font-family:{SANS};font-weight:800;fill:{CREAM}}}"
        f".serif{{font-family:{SERIF};font-style:italic;fill:{PEN}}}"
        f".pen{{fill:none;stroke:{PEN};stroke-width:2.8;stroke-linecap:round;stroke-linejoin:round}}"
        f".strike{{fill:none;stroke:{PEN};stroke-width:2;stroke-linecap:round}}"
        f".tile{{fill:{DESK2};stroke:{LINE};stroke-width:1.5}}"
        f".big{{font-family:{MONO};font-size:54px;font-weight:700}}")


def sprite():
    """A red pen. Its tip is at the origin and the body leans up and to the right."""
    return (f'<g transform="rotate(-52)"><rect x="9" y="-5" width="74" height="10" rx="4" fill="{PEN}"/>'
            f'<rect x="60" y="-5" width="9" height="10" fill="{CREAM}" opacity=".85"/>'
            f'<path d="M0,0 L11,-5 L11,5 Z" fill="{CREAM}"/><path d="M0,0 L4,-1.8 L4,1.8 Z" fill="{INK}"/></g>')


def dark_svg(w, h, label, body, css):
    bg = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="{DESK}" stroke="{LINE}" stroke-width="2"/>'
    return svg(w, h, label, bg + body, DARK + css + REDUCE)


# ---------------------------------------------------------------- hero
def hero():
    L = 24.0
    css, body = [], []
    # the sheet's text is the demo's draft, so the picture matches the example in the README
    before = ["Here's the thing: shipping fast isn't just about", "speed, it's about trust.", "",
              "Last month our team cut the checkout bug backlog", "from 42 to 9 in two weeks. Not just a win for",
              "the engineering team, but a win for customers,", "the business, and for the future.", "",
              "Agree? What's your biggest lesson?"]
    cw, y0, step, sx, sy = 9.0, 88, 28, 24, 0
    ys = [y0 + i * step for i in range(len(before))]
    # (line, first char, last char), in the order the pen works
    strikes = [(0, 0, 17), (0, 32, 48), (1, 0, 17), (4, 27, 45), (5, 0, 47), (6, 0, 29), (8, 0, 34)]
    starts = [5.0, 7.0, 7.8, 9.8, 10.6, 11.4, 13.2]
    dur = 0.7
    counter_at = [5.7, 8.5, 12.1, 13.9]

    # --- title, typed
    css.append(stops("type", L, [(0, "transform:translateX(0)"), (0.4, "transform:translateX(0)"), (2.4, "transform:translateX(780px)"), (L, "transform:translateX(780px)")]))
    css.append(".type{animation:type 24s steps(21) infinite}")
    body.append(f'<text class="head" x="48" y="130" style="font-size:54px" textLength="596" lengthAdjust="spacingAndGlyphs">write-without-ai-slop</text>')
    body.append(f'<rect class="type" x="44" y="82" width="620" height="64" fill="{DESK}"/>')
    css.append(stops("caret", L, [(0, "transform:translateX(0);opacity:1"), (0.4, "transform:translateX(0);opacity:1"),
                                    (2.4, "transform:translateX(600px);opacity:1"), (2.7, "transform:translateX(600px);opacity:0"),
                                    (24, "transform:translateX(600px);opacity:0")]))
    css.append(".caret{animation:caret 24s steps(21) infinite}")
    body.append(f'<rect class="caret" x="46" y="86" width="7" height="50" fill="{PEN}"/>')
    # --- underline and one-line promise
    css.append(anim("ul", 2.8, .9, "draw") + ".ul{stroke-dasharray:1;stroke-dashoffset:0;animation:ul 24s linear infinite}")
    body.append(f'<path class="pen ul" pathLength="1" d="{pen(46, 640, 150, 41)}"/>')
    css.append(anim("sub", 3.4, .8, "fade") + run("sub", L))
    body.append(f'<text class="sans dim sub" x="48" y="196" style="font-size:23px" textLength="470" lengthAdjust="spacingAndGlyphs">Fewer tells. Same facts. Your voice.</text>')

    # --- ticker of phrases the skill strikes, scrolling behind a strike line
    phrases = ["In today's fast-paced world", "Let's dive in", "game-changer", "I hope this helps", "it's worth noting",
               "Certainly!", "at the end of the day", "tapestry", "Not just X, but Y", "unlock"]
    est = 8.1
    x, items = 0, []
    for p in phrases:
        w = len(p) * est
        items.append((x, p, w)); x += w + 46
    total = x
    def strip(off):
        out = ""
        for ix, p, w in items:
            xx = off + ix
            out += (f'<text class="sans dim" x="{xx:.0f}" y="244" style="font-size:16px" textLength="{w:.0f}" lengthAdjust="spacingAndGlyphs">{esc(p)}</text>'
                    f'<path class="strike" d="M{xx-4:.0f},{239 + (len(p) % 3) - 1} L{xx+w+4:.0f},{238 + (len(p) % 4) - 1}"/>')
        return out
    css.append(f"@keyframes tick{{0%{{transform:translateX(0)}}100%{{transform:translateX({-total:.0f}px)}}}}.tick{{animation:tick 40s linear infinite}}")
    body.append(f'<clipPath id="band"><rect x="40" y="214" width="640" height="44"/></clipPath>')
    body.append(f'<g clip-path="url(#band)"><g class="tick">{strip(48)}{strip(48 + total)}</g></g>')
    body.append(f'<defs><linearGradient id="fadeL"><stop offset="0" stop-color="{DESK}"/><stop offset="1" stop-color="{DESK}" stop-opacity="0"/></linearGradient>'
                f'<linearGradient id="fadeR"><stop offset="0" stop-color="{DESK}" stop-opacity="0"/><stop offset="1" stop-color="{DESK}"/></linearGradient></defs>'
                f'<rect x="40" y="210" width="80" height="52" fill="url(#fadeL)"/><rect x="600" y="210" width="80" height="52" fill="url(#fadeR)"/>')

    # --- readouts
    body.append(f'<rect class="tile" x="48" y="292" width="280" height="108" rx="12"/><text class="lab" x="70" y="324">PATTERNS CAUGHT</text>')
    body.append(f'<rect class="tile" x="348" y="292" width="280" height="108" rx="12"/><text class="lab" x="370" y="324">FACTS CHANGED</text>')
    edges = [0] + counter_at + [L + 1]
    for n in range(5):
        a, b = edges[n], edges[n + 1]
        if n == 0:
            kf = stops(f"c{n}", L, [(0, "opacity:1"), (a if a else 0.01, "opacity:1"), (b, "opacity:1"), (b + .01, "opacity:0"), (L, "opacity:0")])
        else:
            kf = stops(f"c{n}", L, [(0, "opacity:0"), (a, "opacity:0"), (a + .01, "opacity:1"), (b, "opacity:1"), (b + .01, "opacity:0"), (L, "opacity:0")]) if n < 4 else \
                 stops(f"c{n}", L, [(0, "opacity:0"), (a, "opacity:0"), (a + .01, "opacity:1"), (L, "opacity:1")])
        css.append(kf + run(f"c{n}", L))
        body.append(f'<text class="big c{n}" x="70" y="384">{n}</text>')
    body.append(f'<text class="big green" x="370" y="384">0</text>')
    css.append(stops("glow", L, [(0, "opacity:.0"), (16.2, "opacity:0"), (16.8, "opacity:1"), (L, "opacity:1")]) + run("glow", L))
    body.append(f'<rect class="glow" x="348" y="292" width="280" height="108" rx="12" fill="none" stroke="{GREEN}" stroke-width="2.5"/>')

    # --- the sheet
    sh = []
    sh.append(f'<rect x="8" y="10" width="504" height="372" rx="12" fill="#000" opacity=".35"/>')
    sh.append(f'<rect x="0" y="0" width="504" height="372" rx="12" fill="{PAPER}" stroke="{EDGE}" stroke-width="2"/>')
    sh.append(f'<text class="lab" x="24" y="42" style="fill:#8a8068">DRAFT</text>')
    def hl(i, a, n): return f'<rect x="{sx + a*cw - 2:.1f}" y="{ys[i] - 16}" width="{n*cw + 4:.1f}" height="22" rx="3" fill="{MARK}" opacity=".8"/>'
    sh.append(hl(4, 5, 2) + hl(4, 11, 1))
    for i, s in enumerate(before):
        if s:
            sh.append(f'<text class="ink" x="{sx}" y="{ys[i]}" textLength="{len(s)*cw:.1f}" lengthAdjust="spacingAndGlyphs">{esc(s)}</text>')
    for k, (li, a, b) in enumerate(strikes):
        s0, e0 = starts[k], starts[k] + dur
        css.append(anim(f"s{k}", s0, dur, "draw") + f".s{k}{{stroke-dasharray:1;stroke-dashoffset:0;animation:s{k} {L}s linear infinite}}")
        sh.append(f'<path class="pen s{k}" pathLength="1" d="{pen(sx + a*cw - 3, sx + b*cw + 3, ys[li] - 6, 200 + k)}"/>')
    # circle round the numbers, then the proof-reader's "stet"
    cx, cy, rx, ry = sx + 8.5 * cw, ys[4] - 5, 7.2 * cw, 17
    ring = "M" + " L".join(f"{cx + rx*math.cos(a/12*2*math.pi - math.pi/2):.1f},{cy + ry*math.sin(a/12*2*math.pi - math.pi/2):.1f}" for a in range(13))
    css.append(anim("ring", 15.0, .9, "draw") + f".ring2{{stroke-dasharray:1;stroke-dashoffset:0;animation:ring {L}s linear infinite}}")
    sh.append(f'<path class="pen ring2" pathLength="1" style="stroke-width:2.2" d="{ring}"/>')
    css.append(anim("stet", 16.2, .7, "fade") + run("stet", L))
    sh.append(f'<text class="serif stet" x="{sx + 46*cw - 4:.0f}" y="{ys[4] - 22}" style="font-size:21px">stet</text>')
    # pen sprite path
    pts = [(0.0, (600, -60)), (4.0, (600, -60)), (4.8, (sx - 3, ys[0] - 6))]
    for (li, a, b), s0 in zip(strikes, starts):
        pts.append((s0, (sx + a*cw - 3, ys[li] - 6)))
        pts.append((s0 + dur, (sx + b*cw + 3, ys[li] - 6)))
    pts.append((14.7, (cx - rx, cy)))
    for a in range(13):
        pts.append((15.0 + a * .9 / 12, (cx + rx*math.cos(a/12*2*math.pi - math.pi/2) , cy + ry*math.sin(a/12*2*math.pi - math.pi/2))))
    pts.append((16.6, (cx, cy - ry)))
    pts.append((17.4, (620, -60)))
    pts.append((L, (620, -60)))
    # a transform keyframe cannot start at an earlier time than the last, so sort and de-duplicate
    seen, clean = set(), []
    for t, (px, py) in sorted(pts, key=lambda p: p[0]):
        t = round(t, 2)
        while t in seen: t += .01
        seen.add(t); clean.append((t, f"transform:translate({px:.1f}px,{py:.1f}px)"))
    css.append(stops("penpath", L, clean) + f".penmove{{animation:penpath {L}s linear infinite}}")
    sh.append(f'<g class="penmove" style="transform:translate(620px,-60px)">{sprite()}</g>')
    css.append(stops("sheet", L, [(0, "opacity:0;transform:translateY(24px)"), (0.8, "opacity:0;transform:translateY(24px)"), (2.0, "opacity:1;transform:translateY(0)"), (L, "opacity:1;transform:translateY(0)")]) + run("sheet", L))
    body.append(f'<g transform="translate(656 34) rotate(1.4)"><g class="sheet">{"".join(sh)}</g></g>')

    css.append(stops("reset", L, [(0, "opacity:0"), (.25, "opacity:1"), (22.3, "opacity:1"), (23.3, "opacity:0"), (L, "opacity:0")]) + run("reset", L))
    return dark_svg(1200, 440,
                    "write-without-ai-slop. A red pen strikes four patterns from a short draft: a setup before the point, a not-just-X contrast, a group of three and a bait question. The numbers 42 and 9 are circled and marked stet. The counters read: patterns caught 4, facts changed 0.",
                    f'<g class="reset">{"".join(body)}</g>', "".join(css))


# ---------------------------------------------------------------- flow
def flow():
    L = 16.0
    css, body = [], []
    xs = [150, 450, 750, 1050]
    times = [1.0, 4.2, 7.6, 11.0]   # when the sheet arrives at each stop
    hold = 2.2
    body.append('<text class="lab" x="40" y="46">WRITE MODE, END TO END</text>')
    heads = ["Write", "Check", "Fix", "Hand back"]
    caps = ["follows the rules as it writes", "runs the final check on its own draft", "the smallest edit that removes it", "only the text comes back"]
    cy = 160
    for i, x in enumerate(xs):
        body.append(f'<rect class="tile" x="{x-100}" y="{cy-70}" width="200" height="140" rx="16"/>')
        a, b = times[i] + .6, times[i] + hold + .6
        css.append(stops(f"on{i}", L, [(0, "opacity:0"), (a, "opacity:0"), (a + .3, "opacity:1"), (b, "opacity:1"), (b + .3, "opacity:0"), (L, "opacity:0")]) + run(f"on{i}", L))
        col = GREEN if i == 3 else PEN
        body.append(f'<rect class="on{i}" x="{x-100}" y="{cy-70}" width="200" height="140" rx="16" fill="none" stroke="{col}" stroke-width="3"/>')
        body.append(f'<text class="head" x="{x}" y="{cy+104}" style="font-size:22px;text-anchor:middle" textLength="{len(heads[i])*13}" lengthAdjust="spacingAndGlyphs">{heads[i]}</text>')
        body.append(f'<text class="sans dim" x="{x}" y="{cy+130}" style="font-size:14px;text-anchor:middle" textLength="{len(caps[i])*6.5:.0f}" lengthAdjust="spacingAndGlyphs">{caps[i]}</text>')
        if i < 3:
            body.append(f'<path d="M{x+112},{cy} L{xs[i+1]-114},{cy}" stroke="{LINE}" stroke-width="3" stroke-dasharray="3 9" stroke-linecap="round" fill="none"/>'
                        f'<path d="M{xs[i+1]-122},{cy-8} L{xs[i+1]-110},{cy} L{xs[i+1]-122},{cy+8}" stroke="{LINE}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    # icon 1: lines being written
    x = xs[0]
    for j, wd in enumerate((120, 96, 108)):
        css.append(stops(f"w{j}", L, [(0, "transform:scaleX(0)"), (times[0] + j * .5, "transform:scaleX(0)"), (times[0] + j * .5 + 1.0, "transform:scaleX(1)"), (L, "transform:scaleX(1)")]) + run(f"w{j}", L, "transform-box:fill-box;transform-origin:left center"))
        body.append(f'<rect class="w{j}" x="{x-60}" y="{cy-30+j*26}" width="{wd}" height="9" rx="4.5" fill="{CREAM}" opacity=".85"/>')
    # icon 2: a magnifier sweeping the lines
    x = xs[1]
    for j, wd in enumerate((120, 96, 108)):
        body.append(f'<rect x="{x-60}" y="{cy-30+j*26}" width="{wd}" height="9" rx="4.5" fill="{CREAM}" opacity=".45"/>')
    css.append(stops("mag", L, [(0, "transform:translate(-40px,-10px)"), (times[1] + .4, "transform:translate(-40px,-10px)"), (times[1] + 2.0, "transform:translate(30px,34px)"), (L, "transform:translate(30px,34px)")]) + run("mag", L))
    body.append(f'<g class="mag"><circle cx="{x}" cy="{cy-8}" r="24" fill="{DESK}" fill-opacity=".55" stroke="{CREAM}" stroke-width="4"/><path d="M{x+17},{cy+9} L{x+34},{cy+27}" stroke="{CREAM}" stroke-width="6" stroke-linecap="round"/></g>')
    # icon 3: a line struck by the pen
    x = xs[2]
    for j, wd in enumerate((120, 96, 108)):
        body.append(f'<rect x="{x-60}" y="{cy-30+j*26}" width="{wd}" height="9" rx="4.5" fill="{CREAM}" opacity=".85"/>')
    css.append(anim("fx", times[2] + .5, .9, "draw") + f".fx{{stroke-dasharray:1;stroke-dashoffset:0;animation:fx {L}s linear infinite}}")
    body.append(f'<path class="pen fx" pathLength="1" d="{pen(x-66, x+66, cy-25, 9)}"/>')
    css.append(stops("fade2", L, [(0, "opacity:.85"), (times[2] + 1.6, "opacity:.85"), (times[2] + 2.2, "opacity:.15"), (L, "opacity:.15")]) + run("fade2", L))
    # icon 4: a check
    x = xs[3]
    css.append(anim("ck", times[3] + .5, .8, "draw") + f".ck{{stroke-dasharray:1;stroke-dashoffset:0;animation:ck {L}s linear infinite}}")
    body.append(f'<path class="ck" pathLength="1" d="M{x-34},{cy+2} L{x-8},{cy+28} L{x+38},{cy-30}" fill="none" stroke="{GREEN}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    # the sheet that travels
    pos = [(0, f"transform:translate({xs[0]-170}px,0);opacity:0")]
    pos.append((0.5, f"transform:translate({xs[0]-170}px,0);opacity:0"))
    pos.append((times[0] - .2, f"transform:translate({xs[0]}px,0);opacity:1"))
    for i in range(1, 4):
        pos.append((times[i - 1] + hold + .3, f"transform:translate({xs[i-1]}px,0);opacity:1"))
        pos.append((times[i] - .2, f"transform:translate({xs[i]}px,0);opacity:1"))
    pos.append((times[3] + hold + .6, f"transform:translate({xs[3]}px,0);opacity:1"))
    pos.append((times[3] + hold + 1.2, f"transform:translate({xs[3]+60}px,0);opacity:0"))
    pos.append((L, f"transform:translate({xs[3]+60}px,0);opacity:0"))
    css.append(stops("tok", L, pos) + run("tok", L))
    body.append(f'<g class="tok"><g transform="translate(0 {cy-112}) rotate(-4)"><rect x="-21" y="-2" width="42" height="52" rx="5" fill="{PAPER}" stroke="{EDGE}" stroke-width="2"/>'
                f'<path d="M-12,12 h24 M-12,24 h24 M-12,36 h14" stroke="{INK}" stroke-width="3" stroke-linecap="round" opacity=".55"/></g></g>')
    css.append(stops("reset", L, [(0, "opacity:0"), (.3, "opacity:1"), (L - 1.2, "opacity:1"), (L - .4, "opacity:0"), (L, "opacity:0")]) + run("reset", L))
    return dark_svg(1200, 330, "Write mode from start to end: the agent writes with the rules in mind, checks its own draft, makes the smallest edit that removes any problem, and hands back only the text.",
                    f'<g class="reset">{"".join(body)}</g>', "".join(css))


# ---------------------------------------------------------------- patterns
PATTERNS = ["Not X, but Y", "Groups of three", "Setup before the point", "Fake meaning on the tail", "Puffed importance",
            "Stacked fragments", "Closer that repeats or flatters", "Piled-up hedges", "Vague sources", "Rotating synonyms",
            "False ranges", "Same shape everywhere", "Challenge-then-optimism formula", "Generic where a fact should be",
            "Chatbot leftovers", "Sameness across a batch", "Fixes that make new tells"]


def patterns():
    L = 22.0
    css, body = [], []
    cw_, ch, gx, gy, x0, y0 = 270, 40, 12, 10, 42, 104
    body.append('<text class="lab" x="42" y="46">17 PATTERNS, CHECKED IN COMBINATION</text>')
    scans = [(1.0, 4.0, {0, 1, 2, 6}, "DRAFT A", "4 together: fix them", PEN),
             (11.0, 4.0, {7}, "DRAFT B", "1 alone: stet, let it stand", GREEN)]
    flag_time = {}
    for (t0, d, idx, *_rest) in scans:
        for i in idx:
            flag_time[i] = t0 + ((i // 4) * (ch + gy) + ch / 2) / (5 * (ch + gy)) * d
    for i, name in enumerate(PATTERNS):
        x, y = x0 + (i % 4) * (cw_ + gx), y0 + (i // 4) * (ch + gy)
        body.append(f'<rect class="tile" x="{x}" y="{y}" width="{cw_}" height="{ch}" rx="10"/>')
        body.append(f'<text class="dim" x="{x+14}" y="{y+26}" style="font-size:13px">{i+1:02d}</text>')
        body.append(f'<text class="sans" x="{x+44}" y="{y+26}" style="font-size:14.5px" textLength="{len(name)*6.7:.0f}" lengthAdjust="spacingAndGlyphs">{esc(name)}</text>')
    body.append(f'<rect class="tile" x="{x0+cw_+gx}" y="{y0+4*(ch+gy)}" width="{3*cw_+2*gx}" height="{ch}" rx="10" stroke-dasharray="4 6" fill="none"/>')
    for (t0, d, idx, tag, verdict, col) in scans:
        for i in sorted(idx):
            x, y = x0 + (i % 4) * (cw_ + gx), y0 + (i // 4) * (ch + gy)
            a = flag_time[i]
            b = t0 + 7.6
            nm = f"f{i}"
            css.append(stops(nm, L, [(0, "opacity:0"), (a, "opacity:0"), (a + .25, "opacity:1"), (b, "opacity:1"), (b + .6, "opacity:0"), (L, "opacity:0")]) + run(nm, L))
            body.append(f'<g class="{nm}"><rect x="{x}" y="{y}" width="{cw_}" height="{ch}" rx="10" fill="{col}" fill-opacity=".16" stroke="{col}" stroke-width="2.5"/></g>')
        # beam
        nm = f"beam{int(t0)}"
        css.append(stops(nm, L, [(0, "opacity:0;transform:translateY(0)"), (t0 - .2, "opacity:0;transform:translateY(0)"), (t0, "opacity:1;transform:translateY(0)"),
                                 (t0 + d, "opacity:1;transform:translateY(250px)"), (t0 + d + .3, "opacity:0;transform:translateY(250px)"), (L, "opacity:0")]) + run(nm, L))
        body.append(f'<g class="{nm}"><rect x="30" y="{y0-4}" width="1140" height="4" rx="2" fill="{col}"/><rect x="30" y="{y0-34}" width="1140" height="30" fill="url(#bg{int(t0)})" /></g>')
        body.append(f'<defs><linearGradient id="bg{int(t0)}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col}" stop-opacity="0"/><stop offset="1" stop-color="{col}" stop-opacity=".28"/></linearGradient></defs>')
        # verdict
        vt = t0 + d + .6
        nm = f"v{int(t0)}"
        css.append(stops(nm, L, [(0, "opacity:0"), (t0 - .2, "opacity:0"), (t0, "opacity:1"), (vt - .1, "opacity:1"), (t0 + 7.6, "opacity:1"), (t0 + 8.2, "opacity:0"), (L, "opacity:0")]) + run(nm, L))
        css.append(stops(nm + "b", L, [(0, "opacity:0"), (vt, "opacity:0"), (vt + .5, "opacity:1"), (t0 + 7.6, "opacity:1"), (t0 + 8.2, "opacity:0"), (L, "opacity:0")]) + run(nm + "b", L))
        body.append(f'<text class="lab {nm}" x="{x0+cw_+gx+18}" y="{y0+4*(ch+gy)+26}">{tag}</text>')
        cls = "green" if col == GREEN else "red"
        body.append(f'<text class="head {cls} {nm}b" x="{x0+cw_+gx+110}" y="{y0+4*(ch+gy)+29}" style="font-size:22px" textLength="{len(verdict)*11.6:.0f}" lengthAdjust="spacingAndGlyphs">{verdict}</text>')
    css.append(stops("reset", L, [(0, "opacity:0"), (.3, "opacity:1"), (L - 1.2, "opacity:1"), (L - .4, "opacity:0"), (L, "opacity:0")]) + run("reset", L))
    return dark_svg(1200, 376, "The 17 patterns the skill checks for, in a grid. A scan flags four patterns together in one draft, and the skill fixes them. A second scan flags only one pattern in another draft, and the skill leaves it alone, which editors call stet.",
                    f'<g class="reset">{"".join(body)}</g>', "".join(css))


# ---------------------------------------------------------------- sameness
def sameness():
    L = 14.0
    css, body = [], []
    after = [("We shipped on", "a Friday."), ("Bugs: 42 down", "to 9."), ("A support ticket", "changed our plan."),
             ("The rewrite took", "three weeks."), ("Nobody owned", "checkout.")]
    bars_after = [(150, 90, 120), (110, 150, 70), (140, 100, 130), (90, 150, 110), (130, 80, 150)]
    cwid, gap, x0, y0, chh = 210, 22, 31, 116, 170
    body.append('<text class="lab" x="42" y="46">SAMENESS ACROSS A BATCH</text>')
    css.append(stops("lb1", L, [(0, "opacity:1"), (5.0, "opacity:1"), (5.6, "opacity:0"), (L - 1.2, "opacity:0"), (L - .6, "opacity:1"), (L, "opacity:1")]) + run("lb1", L))
    css.append(stops("lb2", L, [(0, "opacity:0"), (5.4, "opacity:0"), (6.0, "opacity:1"), (L - 1.2, "opacity:1"), (L - .6, "opacity:0"), (L, "opacity:0")]) + run("lb2", L))
    body.append(f'<text class="head red lb1" x="42" y="82" style="font-size:26px" textLength="560" lengthAdjust="spacingAndGlyphs">Five posts, one opening.</text>')
    body.append(f'<text class="head green lb2" x="42" y="82" style="font-size:26px" textLength="560" lengthAdjust="spacingAndGlyphs">Five posts, five openings.</text>')
    css.append(stops("b1", L, [(0, "opacity:1"), (5.0 + 0, "opacity:1"), (5.6, "opacity:0"), (L - 1.2, "opacity:0"), (L - .6, "opacity:1"), (L, "opacity:1")]) + run("b1", L))
    css.append(stops("a1", L, [(0, "opacity:0"), (5.4, "opacity:0"), (6.0, "opacity:1"), (L - 1.2, "opacity:1"), (L - .6, "opacity:0"), (L, "opacity:0")]) + run("a1", L))
    for i in range(5):
        x = x0 + i * (cwid + gap)
        # the whole card settles in one after the other
        css.append(stops(f"k{i}", L, [(0, "opacity:0;transform:translateY(18px)"), (.3 + i * .35, "opacity:0;transform:translateY(18px)"), (.9 + i * .35, "opacity:1;transform:translateY(0)"), (L - 1.2, "opacity:1;transform:translateY(0)"), (L - .6, "opacity:0;transform:translateY(0)"), (L, "opacity:0;transform:translateY(18px)")]) + run(f"k{i}", L))
        card = [f'<rect x="{x}" y="{y0}" width="{cwid}" height="{chh}" rx="12" fill="{PAPER}" stroke="{EDGE}" stroke-width="2"/>']
        # before
        b = [f'<text class="ink" x="{x+18}" y="{y0+42}" style="font-size:16px" textLength="{17*9.6:.0f}" lengthAdjust="spacingAndGlyphs">Here\'s the thing:</text>',
             f'<path class="strike" d="{pen(x+14, x+18+17*9.6+4, y0+36, 300+i)}"/>']
        for j, wd in enumerate((150, 150, 112)):
            b.append(f'<rect x="{x+18}" y="{y0+66+j*24}" width="{wd}" height="9" rx="4.5" fill="{INK}" opacity=".22"/>')
        card.append(f'<g class="b1">{"".join(b)}</g>')
        # after
        a = []
        for j, t in enumerate(after[i]):
            a.append(f'<text class="ink" x="{x+18}" y="{y0+42+j*24}" style="font-size:16px" textLength="{len(t)*9.6:.0f}" lengthAdjust="spacingAndGlyphs">{esc(t)}</text>')
        for j, wd in enumerate(bars_after[i][:2]):
            a.append(f'<rect x="{x+18}" y="{y0+98+j*24}" width="{wd}" height="9" rx="4.5" fill="{INK}" opacity=".22"/>')
        card.append(f'<g class="a1">{"".join(a)}</g>')
        body.append(f'<g class="k{i}">{"".join(card)}</g>')
    body.append(f'<text class="sans dim" x="42" y="{y0+chh+44}" style="font-size:15px" textLength="760" lengthAdjust="spacingAndGlyphs">Invented posts. When a batch opens or ends the same way, the skill varies it.</text>')
    return dark_svg(1200, 348, "Five posts that all open with the same setup line. After the skill, each post opens in its own way. The posts are invented.",
                    "".join(body), "".join(css))


# ---------------------------------------------------------------- install
def install():
    L = 14.0
    css, body = [], []
    cmd = "npx skills add nocodeanish/write-without-ai-slop"
    note = "# then ask your agent: check this draft"
    fw = 13.2
    tx = 112
    body.append(f'<rect x="40" y="36" width="1120" height="176" rx="14" fill="#0f0e14" stroke="{LINE}" stroke-width="2"/>')
    body.append('<clipPath id="term"><rect x="41" y="37" width="1118" height="174" rx="13"/></clipPath><g clip-path="url(#term)">')
    for k, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        body.append(f'<circle cx="{70+k*24}" cy="62" r="7" fill="{c}"/>')
    body.append('<text class="lab" x="560" y="67">TERMINAL</text>')
    body.append(f'<text style="font-size:22px;fill:{PEN}" x="64" y="124">$</text>')
    body.append(f'<text style="font-size:22px" x="{tx-20}" y="124" textLength="{len(cmd)*fw:.1f}" lengthAdjust="spacingAndGlyphs">{cmd}</text>')
    body.append(f'<text class="dim" style="font-size:22px" x="{tx-20}" y="172" textLength="{len(note)*fw:.1f}" lengthAdjust="spacingAndGlyphs">{note}</text>')
    w1, w2 = len(cmd) * fw, len(note) * fw
    css.append(stops("t1", L, [(0, "transform:translateX(0)"), (.8, "transform:translateX(0)"), (3.4, f"transform:translateX({w1+30:.0f}px)"), (L, f"transform:translateX({w1+30:.0f}px)")]))
    css.append(f".t1{{animation:t1 {L}s steps({len(cmd)}) infinite}}")
    css.append(stops("t2", L, [(0, "transform:translateX(0)"), (4.6, "transform:translateX(0)"), (6.6, f"transform:translateX({w2+30:.0f}px)"), (L, f"transform:translateX({w2+30:.0f}px)")]))
    css.append(f".t2{{animation:t2 {L}s steps({len(note)}) infinite}}")
    body.append(f'<rect class="t1" x="{tx-24}" y="98" width="{w1+30:.0f}" height="36" fill="#0f0e14"/>')
    body.append(f'<rect class="t2" x="{tx-24}" y="146" width="{w2+30:.0f}" height="36" fill="#0f0e14"/>')
    css.append(stops("c1", L, [(0, "transform:translateX(0);opacity:1"), (.8, "transform:translateX(0);opacity:1"), (3.4, f"transform:translateX({w1:.0f}px);opacity:1"), (3.5, f"transform:translateX({w1:.0f}px);opacity:0"), (L, f"transform:translateX({w1:.0f}px);opacity:0")]))
    css.append(f".c1{{animation:c1 {L}s steps({len(cmd)}) infinite}}")
    css.append(stops("c2", L, [(0, "transform:translateX(0);opacity:0"), (4.5, "transform:translateX(0);opacity:0"), (4.6, "transform:translateX(0);opacity:1"), (6.6, f"transform:translateX({w2:.0f}px);opacity:1"), (L, f"transform:translateX({w2:.0f}px);opacity:1")]))
    css.append(f".c2{{animation:c2 {L}s steps({len(note)}) infinite}}")
    css.append("@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:0}}.bl{animation:bl 1s steps(1) infinite}")
    body.append(f'<rect class="c1" x="{tx-20}" y="104" width="11" height="24" fill="{CREAM}"/>')
    body.append(f'<g class="bl"><rect class="c2" x="{tx-20}" y="152" width="11" height="24" fill="{CREAM}"/></g>')
    body.append('</g>')
    css.append(stops("reset", L, [(0, "opacity:0"), (.2, "opacity:1"), (L - 1.0, "opacity:1"), (L - .3, "opacity:0"), (L, "opacity:0")]) + run("reset", L))
    return dark_svg(1200, 250, "A terminal types the install command, npx skills add nocodeanish/write-without-ai-slop, then a note: then ask your agent to check this draft.",
                    f'<g class="reset">{"".join(body)}</g>', "".join(css))


PANELS = (("hero", hero), ("flow", flow), ("patterns", patterns), ("sameness", sameness), ("install", install))
