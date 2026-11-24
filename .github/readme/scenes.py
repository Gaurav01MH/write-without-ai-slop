"""Animated pixel-art scenes for the README. Each function returns one SVG string.

The art tells the story with pictures: an editor with a red pen hunts slop blobs, the facts (coins) stay safe.
All motion is plain CSS keyframes, so it plays inside an <img> on GitHub. The resting state of every element is
a finished picture, so reduced motion shows a clean still. The output is deterministic.
"""
import math
import random
from artlib import esc, stops, run, svg, MONO, SANS, SERIF, REDUCE, PEN, MARK
from pixel import *


def track(name, loop, pts, up="ease-out", down="ease-in", prop="transform:translateY({v}px)"):
    """Keyframes from (second, value) pairs with a gentle ease: rising segments ease out, falling ones ease in."""
    pts = sorted(pts, key=lambda p: p[0])
    out, last = [], None
    for k, (t, v) in enumerate(pts):
        t = round(t, 3)
        if last is not None and t <= last:
            t = last + .001
        last = t
        ease = ""
        if k + 1 < len(pts):
            ease = f";animation-timing-function:{up if pts[k+1][1] < v else down if pts[k+1][1] > v else 'linear'}"
        out.append((t, prop.format(v=v) + ease))
    return stops(name, loop, out) + run(name, loop)


def shadow(cx, cy, rx):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="5" fill="#000" opacity=".3"/>'


def editor(s, pen_class="", legs_class=("la", "lb")):
    """The editor: beret, red pen, two leg frames that swap while running. Returns svg of a figure with its feet at y=0."""
    h = len(EDITOR) * s
    legs_h = len(LEGS_A) * s
    top = -(h + legs_h)
    body = sprite(EDITOR, EDITOR_PAL, s, 0, top)
    la = f'<g class="{legs_class[0]}">{sprite(LEGS_A, EDITOR_PAL, s, 0, top + h)}</g>'
    lb = f'<g class="{legs_class[1]}">{sprite(LEGS_B, EDITOR_PAL, s, 0, top + h)}</g>'
    pen = (f'<g transform="translate({10.5*s:.0f} {top + 10*s:.0f})"><g class="{pen_class}">'
           f'<g transform="rotate(-38)"><rect x="-{s}" y="-{s*.7:.1f}" width="{s*8.5:.1f}" height="{s*1.4:.1f}" rx="{s*.5:.1f}" fill="{PEN}"/>'
           f'<rect x="{s*5.2:.1f}" y="-{s*.7:.1f}" width="{s*1.5:.1f}" height="{s*1.4:.1f}" fill="{CREAM}"/>'
           f'<path d="M{s*7.5:.1f},-{s*.7:.1f} L{s*9.6:.1f},0 L{s*7.5:.1f},{s*.7:.1f} Z" fill="#1d1d26"/></g></g></g>')
    return body + la + lb + pen


LEG_CSS = ("@keyframes la{0%{opacity:1}50%,100%{opacity:0}}@keyframes lb{0%{opacity:0}50%,100%{opacity:1}}"
           ".la{animation:la .36s steps(1) infinite}.lb{animation:lb .36s steps(1) infinite}")


# ================================================================= hero
def hero():
    L, V, XC, GY, S = 24.0, 100, 224, 340, 6
    css, sky, mid, world, front, bursts = [LEG_CSS, f'.coin{{font-weight:800;fill:#7a4a05;text-anchor:middle;font-family:{MONO}}}'], [], [], [], [], []
    W, H = 1200, 440
    # --- sky: stars, a moon, a skyline of paper piles that scrolls slowly
    sky.append(stars(W, H, 60, 11, 250))
    sky.append(f'<circle cx="760" cy="96" r="30" fill="#ece6c9"/><circle cx="750" cy="88" r="6" fill="#d8d1b0"/><circle cx="772" cy="106" r="4" fill="#d8d1b0"/>')
    r = random.Random(3)
    city, x = "", 0
    while x < 360:
        bw = r.choice((40, 56, 72)); bh = r.randrange(50, 140, 10)
        city += f'<rect x="{x}" y="{GY-bh}" width="{bw-4}" height="{bh}" fill="#16213f"/>'
        for wy in range(GY - bh + 12, GY - 14, 20):
            for wx in range(x + 8, x + bw - 14, 16):
                if r.random() < .45:
                    city += f'<rect x="{wx}" y="{wy}" width="5" height="7" fill="{"#e9c96a" if r.random() < .3 else "#27386a"}"/>'
        x += bw
    css.append("@keyframes far{to{transform:translateX(-360px)}}.far{animation:far 12s linear infinite}")
    sky.append(f'<defs><g id="city">{city}</g></defs><g class="far">' + "".join(f'<use href="#city" x="{k*360}"/>' for k in range(5)) + '</g>')
    # --- ground: sheets of ruled paper that scroll at the same speed as the enemies
    tile = (f'<rect x="0" y="{GY}" width="116" height="110" fill="#efe6cf"/><rect x="0" y="{GY}" width="116" height="6" fill="#fff7e0"/>'
            + "".join(f'<rect x="0" y="{GY+yy}" width="116" height="2" fill="#a9bde8" opacity=".7"/>' for yy in (30, 52, 74, 96))
            + f'<rect x="20" y="{GY}" width="2" height="110" fill="{PEN}" opacity=".55"/>')
    css.append("@keyframes gr{to{transform:translateX(-120px)}}.gr{animation:gr 1.2s linear infinite}")
    mid.append(f'<defs><g id="tile">{tile}</g></defs><g class="gr">' + "".join(f'<use href="#tile" x="{k*120}"/>' for k in range(11)) + '</g>')
    mid.append(f'<rect x="0" y="{GY+40}" width="{W}" height="80" fill="#000" opacity=".18"/>')

    # --- the world scrolls left; every enemy reaches the editor at its own second
    css.append(stops("world", L, [(0, "transform:translateX(0)"), (L, f"transform:translateX({-V*L}px)")]) + run("world", L))
    def wx(t): return XC + V * t
    stomps, scoreboard_blobs = [], []
    n = 0
    def blob(t, s=4, extra="", pop_color=SLOP):
        nonlocal n
        n += 1
        w, h = 12 * s, 9 * s
        css.append(stops(f"sq{n}", L, [(0, "opacity:1;transform:scale(1,1)"), (t, "opacity:1;transform:scale(1,1)"), (t + .1, "opacity:1;transform:scale(1.3,.25)"),
                                       (t + .4, "opacity:0;transform:scale(1.5,.1)"), (L, "opacity:0;transform:scale(1.5,.1)")]) + run(f"sq{n}", L, "transform-box:fill-box;transform-origin:50% 100%"))
        css.append(f"@keyframes wob{n}{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-3px)}}}}")
        p, pc = poof(f"pf{n}", L, t, wx(t), GY - h / 2, pop_color)
        css.append(pc)
        world.append(f'<g transform="translate({wx(t)-w/2:.0f} {GY-h})"><g class="sq{n}">{sprite(BLOB, BLOB_PAL, s)}{extra}</g></g>')
        bursts.append(p)
        stomps.append(t)
    # enemies: a plain blob, a second blob, a trio of small ones, a bait blob with a question balloon
    for t in (3.0, 6.0):
        blob(t)
    for t in (11.0, 11.45, 11.9):
        blob(t, s=3)
    balloon = (f'<g transform="translate(6 -46)"><rect x="-2" y="-2" width="40" height="44" rx="8" fill="#ffffff"/><path d="M14,42 L22,42 L18,50 Z" fill="#ffffff"/>'
               f'{icon(QMARK, "#3b3f66", 5, 6, 4)}</g>')
    css.append(stops("balloon", L, [(0, "opacity:1"), (16.55, "opacity:1"), (16.6, "opacity:0"), (L, "opacity:0")]) + run("balloon", L))
    blob(16.6, extra=f'<g class="balloon">{balloon}</g>')
    # coins: facts stay, so the editor collects them instead of striking them
    coin_t = (8.4, 14.2)
    for k, (t, label) in enumerate(zip(coin_t, ("42", "9"))):
        css.append(stops(f"cn{k}", L, [(0, "opacity:1;transform:translateY(0) scale(1)"), (t - .1, "opacity:1;transform:translateY(-4px) scale(1)"), (t, "opacity:1;transform:translateY(-24px) scale(1.5)"),
                                       (t + .35, "opacity:0;transform:translateY(-70px) scale(1.7)"), (L, "opacity:0;transform:translateY(-70px) scale(1.7)")]) + run(f"cn{k}", L, "transform-box:fill-box;transform-origin:50% 50%"))
        css.append(f"@keyframes bob{k}{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}")
        p, pc = poof(f"cp{k}", L, t, wx(t), GY - 150, GOLD, 5, 2.8)
        css.append(pc)
        fs = 20 if len(label) == 2 else 22
        world.append(f'<g transform="translate({wx(t):.0f} {GY-150})"><g class="cn{k}"><circle r="22" fill="{GOLD}" stroke="#c98a14" stroke-width="3"/><circle r="15" fill="none" stroke="#e6a92c" stroke-width="2"/>'
                     f'<text class="coin" x="0" y="{fs*.36:.1f}" style="font-size:{fs}px">{label}</text></g></g>')
        bursts.append(p)
    world.extend(bursts)
    # --- finish flag
    ft = 20.0
    fx = wx(ft)
    css.append(stops("pen_up", L, [(0, "transform:translateY(0)"), (ft + .05, "transform:translateY(0)"), (ft + .9, "transform:translateY(-100px)"), (L, "transform:translateY(-100px)")]) + run("pen_up", L))
    css.append("@keyframes flut{0%,100%{transform:skewY(0)}50%{transform:skewY(4deg)}}")
    world.append(f'<g transform="translate({fx:.0f} {GY})"><rect x="-3" y="-200" width="6" height="200" fill="#d9d2bd"/><circle cx="0" cy="-205" r="8" fill="{GOLD}"/>'
                 f'<g class="pen_up"><g transform="translate(3 -80)"><path d="M0,0 L74,24 L0,48 Z" fill="{GREEN}" stroke="#2c8a5a" stroke-width="3" stroke-linejoin="round"/>{icon(CHECK, "#ffffff", 5, 14, 12)}</g></g></g>')
    rc = random.Random(9)
    for k in range(18):
        dx, dy = rc.uniform(-120, 120), rc.uniform(-60, 50)
        col = rc.choice((PEN, GOLD, GREEN, "#7e8cf0", "#ffffff"))
        t0 = ft + .1 + rc.uniform(0, .25)
        css.append(stops(f"cf{k}", L, [(0, "opacity:0;transform:translate(0,0)"), (t0, "opacity:0;transform:translate(0,0)"), (t0 + .05, "opacity:1;transform:translate(0,0)"),
                                       (t0 + 1.4, f"opacity:1;transform:translate({dx:.0f}px,{dy+130:.0f}px)"), (t0 + 1.9, f"opacity:0;transform:translate({dx*1.1:.0f}px,{dy+170:.0f}px)"), (L, "opacity:0")]) + run(f"cf{k}", L))
        HIDE.append(f"cf{k}")
        world.append(f'<g transform="translate({fx:.0f} {GY-210})"><rect class="cf{k}" x="0" y="0" width="{rc.choice((6, 8))}" height="{rc.choice((6, 8))}" fill="{col}"/></g>')

    # --- the editor, fixed on screen, jumping on each beat
    jump = [(0, 0)]
    def hop(t, hc=36):
        jump.extend([(t - .6, 0), (t - .3, -(hc + 62)), (t, -hc), (t + .25, -(hc + 58)), (t + .6, 0)])
    hop(3.0); hop(6.0)
    jump.extend([(7.8, 0), (8.4, -118), (9.0, 0)])
    jump.extend([(10.4, 0), (10.7, -90), (11.0, -27), (11.22, -88), (11.45, -27), (11.67, -88), (11.9, -27), (12.15, -88), (12.6, 0)])
    jump.extend([(13.6, 0), (14.2, -118), (14.8, 0)])
    hop(16.6)
    jump.extend([(19.4, 0), (20.0, -122), (20.7, 0), (L, 0)])
    jump = sorted(set(jump))
    # keep only the highest-priority duplicates: drop landing points that sit between chained hops
    clean = []
    for t, v in jump:
        if clean and abs(clean[-1][0] - t) < .05:
            continue
        clean.append((t, v))
    css.append(track("jump", L, clean))
    swing = [(0, -6)]
    for t in (3.0, 6.0, 11.0, 11.45, 11.9, 16.6):
        swing += [(t - .2, 0), (t, 38), (t + .25, 0)]
    swing = sorted(set(swing))
    css.append(stops("swing", L, [(t, f"transform:rotate({a}deg)") for t, a in swing] + [(L, "transform:rotate(0deg)")]) + run("swing", L))
    front.append(shadow(XC, GY + 4, 34))
    front.append(f'<g transform="translate({XC-24} {GY})"><g class="jump">{editor(S, "swing")}</g></g>')

    # --- scoreboard: blobs struck, coins kept
    sb = (f'<rect x="868" y="22" width="296" height="72" rx="14" fill="#0a1020" stroke="#2a3558" stroke-width="2"/>'
          f'{sprite(BLOB, BLOB_PAL, 3, 890, 42)}'
          f'<circle cx="1034" cy="58" r="17" fill="{GOLD}" stroke="#c98a14" stroke-width="3"/><circle cx="1034" cy="58" r="11" fill="none" stroke="#e6a92c" stroke-width="2"/>')
    d1, c1 = digits("sb", L, 940, 74, (3.4, 6.4, 12.2, 17.0), 40, SLOP_L)
    d2, c2 = digits("sc", L, 1070, 74, coin_t, 40, GOLD)
    css += [c1, c2]
    front.append(sb + d1 + d2)
    front.append(f'<text class="sans" x="40" y="74" style="font-size:40px;font-weight:800;fill:{CREAM}" textLength="470" lengthAdjust="spacingAndGlyphs">write-without-ai-slop</text>')

    css.append(stops("scene", L, [(0, "opacity:1"), (22.8, "opacity:1"), (23.7, "opacity:0"), (L, "opacity:0")]) + run("scene", L))
    body = f'<g class="scene">{"".join(sky)}{"".join(mid)}<g class="world">{"".join(world)}</g>{"".join(front)}</g>'
    return night(W, H, "write-without-ai-slop. A pixel-art editor in a red beret runs along ruled paper and stomps four green slop blobs with a red pen: a plain one, a second, a trio of small ones and one with a question balloon. The editor collects two coins, 42 and 9, instead of striking them, and reaches a green finish flag. A scoreboard counts four blobs struck and two coins kept.",
                 body, "".join(css))



# ================================================================= factory
def factory():
    """A sheet rides a conveyor past four stations: write, inspect, edit, send."""
    L, W, H, FY = 18.0, 1200, 340, 268
    css, body = [LEG_CSS, "@keyframes rb{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}.rb{animation:rb .9s steps(1) infinite}",
                 "@keyframes belt{to{transform:translateX(-48px)}}.belt{animation:belt .8s linear infinite}",
                 "@keyframes scr{0%,100%{transform:translate(0,0)}50%{transform:translate(-6px,5px)}}.scr{animation:scr .3s steps(1) infinite}"], []
    body.append(stars(W, H, 50, 21, 200))
    # floor and belt
    body.append(f'<rect x="0" y="{FY+54}" width="{W}" height="{H-FY-54}" fill="#10172b"/><rect x="0" y="{FY}" width="{W}" height="54" fill="#1b2442"/>')
    body.append(f'<clipPath id="belt"><rect x="20" y="{FY}" width="{W-40}" height="26"/></clipPath><g clip-path="url(#belt)"><rect x="20" y="{FY}" width="{W-40}" height="26" fill="#2a3358"/>'
                f'<g class="belt">{"".join(f"<rect x=\"{k*48}\" y=\"{FY+8}\" width=\"22\" height=\"10\" rx=\"3\" fill=\"#3b4678\"/>" for k in range(26))}</g></g>')
    body.append(f'<rect x="20" y="{FY+26}" width="{W-40}" height="6" fill="#0a1020"/>')
    xs = (190, 490, 790)
    pals = [{"M": "#4c7bd9", "L": "#a8c4ff"}, {"M": "#9a5fd0", "L": "#e0c0ff"}, {"M": "#d65a43", "L": "#ffd0c4"}]
    names = ("writer", "inspector", "editor")
    for k, (cx, pl) in enumerate(zip(xs, pals)):
        pal = {"M": pl["M"], "L": pl["L"], "W": "#ffffff", "K": "#141a30"}
        body.append(shadow(cx, FY - 2, 58))
        body.append(f'<g transform="translate({cx-48} {FY-112})"><g class="rb" style="animation-delay:-{k*.3}s">{sprite(ROBOT, pal, 8)}</g></g>')
    # writer: desk lamp feel -> arm and pen scribbling on the sheet
    cx = xs[0]
    body.append(f'<g transform="translate({cx+44} {FY-46})"><g class="scr"><path d="M0,0 L-34,16" stroke="#4c7bd9" stroke-width="9" stroke-linecap="round"/><rect x="-48" y="13" width="20" height="6" rx="2" fill="{PEN}" transform="rotate(25 -34 16)"/></g></g>')
    # inspector: a lens and a pulsing beam while the sheet is under it
    cx = xs[1]
    css.append(window("beam", L, 5.3, 7.7, fade=.2))
    css.append("@keyframes pls{0%,100%{opacity:.55}50%{opacity:.2}}")
    body.append(f'<g class="beam"><path d="M{cx-20},{FY-76} L{cx-70},{FY-4} L{cx+36},{FY-4} Z" fill="{GOLD}" opacity=".3" style="animation:pls .5s steps(1) infinite"/></g>')
    body.append(f'<circle cx="{cx-20}" cy="{FY-76}" r="24" fill="#ffffff" fill-opacity=".12" stroke="#e0c0ff" stroke-width="5"/><path d="M{cx-3},{FY-58} L{cx+13},{FY-40}" stroke="#e0c0ff" stroke-width="6" stroke-linecap="round"/>')
    # editor: a pen arm that swings down once
    cx = xs[2]
    css.append(stops("slam", L, [(0, "transform:rotate(-100deg)"), (9.3, "transform:rotate(-100deg)"), (9.65, "transform:rotate(62deg)"), (10.1, "transform:rotate(-100deg)"), (L, "transform:rotate(-100deg)")]) + run("slam", L))
    body.append(f'<g transform="translate({cx+44} {FY-46})"><g class="slam"><path d="M0,0 L-8,44" stroke="#d65a43" stroke-width="9" stroke-linecap="round"/>'
                f'<g transform="translate(-8 44)"><rect x="-5" y="-2" width="10" height="32" rx="3" fill="{PEN}"/><path d="M-5,30 L5,30 L0,40 Z" fill="#1d1d26"/></g></g></g>')
    # mailbox at the end
    mx = 1070
    MB = [".BBBBBBBBBBBB.", "BBBBBBBBBBBBBB", "BBDDDDDDDDDDBB", "BBDDDDDDDDDDBB", "BBBBBBBBBBBBBB", "BBBBBBBBBBBBBB", ".BB........BB.", ".BB........BB."]
    body.append(shadow(mx, FY - 2, 66))
    body.append(f'<g transform="translate({mx-49} {FY-56})">{sprite(MB, {"B": "#3a9a78", "D": "#0b1a16"}, 7)}</g>')
    css.append(window("ck", L, 14.1, 16.6, fade=.15))
    body.append(f'<g class="ck">{icon(CHECK, GREEN, 9, mx-31, FY-150)}</g>')
    p, pc = poof("mp", L, 14.2, mx, FY - 100, GREEN, 7, 3.4)
    body.append(p); css.append(pc)
    # the sheet, with slop riding on it
    stops_x = [(0, -70), (.6, -70), (1.1, xs[0]), (3.9, xs[0]), (5.0, xs[1]), (7.7, xs[1]), (8.8, xs[2]), (11.2, xs[2]), (12.8, mx - 40), (13.7, mx)]
    css.append(stops("sheet", L, [(t, f"transform:translateX({x}px);opacity:1") for t, x in stops_x] +
                     [(13.95, f"transform:translateX({mx}px) translateY(18px);opacity:0"), (L, f"transform:translateX({mx}px) translateY(18px);opacity:0")]) + run("sheet", L))
    sheet_in = sprite(SHEET, SHEET_PAL, 5, -25, -55)
    blobs = ""
    for k, bx in enumerate((-46, -16, 14)):
        css.append(stops(f"bl{k}", L, [(0, "opacity:0;transform:scale(0)"), (2.2 + k * .25, "opacity:0;transform:scale(0)"), (2.55 + k * .25, "opacity:1;transform:scale(1)"),
                                       (9.7, "opacity:1;transform:scale(1)"), (9.75, "opacity:0;transform:scale(1.4,.3)"), (L, "opacity:0;transform:scale(1.4,.3)")]) + run(f"bl{k}", L, "transform-box:fill-box;transform-origin:50% 100%"))
        blobs += f'<g class="bl{k}">{sprite(BLOB, BLOB_PAL, 3, bx, -80)}</g>'
    css.append(window("exc", L, 5.6, 9.6, fade=.1))
    exc = "".join(icon(EXCL, PEN, 3, bx + 15, -116) for bx in (-46, -16, 14))
    css.append(window("spk", L, 10.2, 13.2, fade=.15))
    spk = "".join(icon(STARP, GOLD, 3, bx, y) for bx, y in ((-46, -86), (26, -94), (-10, -118)))
    css.append(stops("slash", L, [(0, "stroke-dashoffset:1;opacity:0"), (9.55, "stroke-dashoffset:1;opacity:0"), (9.56, "stroke-dashoffset:1;opacity:1"), (9.8, "stroke-dashoffset:0;opacity:1"), (10.4, "stroke-dashoffset:0;opacity:0"), (L, "opacity:0")]) + run("slash", L, "stroke-dasharray:1"))
    slash = f'<path class="slash" pathLength="1" d="M-52,-86 L50,-62 M-50,-66 L52,-88" stroke="{PEN}" stroke-width="4" stroke-linecap="round" fill="none"/>'
    p2, pc2 = poof("sp", L, 9.7, 0, -70, SLOP, 7, 3.2)
    css.append(pc2)
    body.append(f'<g transform="translate(0 {FY})"><g class="sheet">{sheet_in}{blobs}<g class="exc">{exc}</g><g class="spk">{spk}</g>{slash}{p2}</g></g>')
    css.append(stops("scene", L, [(0, "opacity:1"), (16.6, "opacity:1"), (17.4, "opacity:0"), (L, "opacity:0")]) + run("scene", L))
    return night(W, H, "A conveyor belt moves a sheet of paper past three robots and a mailbox. The sheet picks up green slop blobs, a purple inspector robot spots them with a lens and a light beam, a red editor robot strikes them out with a pen, and the clean sheet drops into the mailbox with a green check.",
                 f'<g class="scene">{"".join(body)}</g>', "".join(css), ".sheet{opacity:0}.ck{opacity:1}")


# ================================================================= zoo
def zoo():
    """17 pattern monsters. A scan flags four together and the editor clears them; a second scan flags one and the editor lets it be."""
    L, W, H = 22.0, 1200, 420
    css, body = [LEG_CSS, "@keyframes mb{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}.mb{animation:mb 1s steps(1) infinite}",
                 "@keyframes shk{0%,100%{transform:translateX(0)}50%{transform:translateX(3px)}}.shk{animation:shk .12s steps(1) infinite}"], []
    body.append(stars(W, H, 70, 31, 290))
    GY = 372
    body.append(f'<rect x="0" y="{GY}" width="{W}" height="{H-GY}" fill="#10172b"/><rect x="0" y="{GY}" width="{W}" height="6" fill="#2a3558"/>')
    gx0, gy0, dx, dy, S = 340, 56, 150, 112, 7
    flagged = {0: 1.0, 1: 1.0, 2: 1.0, 6: 1.0}
    scans = [(1.0, 3.4), (11.0, 3.4)]
    A, B = {0, 1, 2, 6}, {7}
    def beam_time(t0, d, i):
        r = i // 6
        return t0 + ((r * dy + 24) / (3 * dy)) * d
    for i in range(17):
        x, y = gx0 + (i % 6) * dx, gy0 + (i // 6) * dy
        pal = monster_pal(i)
        g = monster(i, S)
        body.append(shadow(x + 24, y + 58, 30))
        inner = f'<g class="mb" style="animation-delay:-{(i*.17)%1:.2f}s">{sprite(g, pal, S)}'
        if i in A or i in B:
            col = PEN if i in A else "#f0b45a"
            t0 = scans[0][0] if i in A else scans[1][0]
            tb = beam_time(t0, 3.4, i)
            end = 5.5 if i in A else 18.8
            css.append(window(f"rd{i}", L, tb, end, fade=.12))
            inner += f'<g class="rd{i}"><g class="shk">{sprite(g, monster_pal(i, col), S)}</g></g>'
            mark = icon(EXCL, PEN, 4, 20, -34) if i in A else icon(QMARK, "#f0b45a", 4, 14, -38)
            css.append(window(f"mk{i}", L, tb, end if i in A else 15.0, fade=.12))
            inner += f'<g class="mk{i}">{mark}</g>'
        inner += "</g>"
        if i in A:
            css.append(stops(f"vs{i}", L, [(0, "opacity:1"), (5.5, "opacity:1"), (5.6, "opacity:0"), (9.8, "opacity:0"), (10.4, "opacity:1"), (L - 1.4, "opacity:1"), (L - .6, "opacity:0"), (L, "opacity:0")]) + run(f"vs{i}", L))
            p, pc = poof(f"pz{i}", L, 5.55, x + 24, y + 24, MONSTER_COLORS[i % 6], 5, 2.6)
            css.append(pc)
            body.append(f'<g transform="translate({x} {y})"><g class="vs{i}">{inner}</g></g>{p}')
        else:
            css.append(stops(f"vs{i}", L, [(0, "opacity:1"), (L - 1.4, "opacity:1"), (L - .6, "opacity:0"), (L, "opacity:0")]) + run(f"vs{i}", L))
            body.append(f'<g transform="translate({x} {y})"><g class="vs{i}">{inner}</g></g>')
    # the spared one gets a heart and a happy hop
    x7, y7 = gx0 + 1 * dx, gy0 + 1 * dy
    css.append(window("heart", L, 15.3, 19.0, fade=.15))
    css.append(stops("hop", L, [(0, "transform:translateY(0)"), (15.3, "transform:translateY(0)"), (15.55, "transform:translateY(-22px)"), (15.8, "transform:translateY(0)"), (16.1, "transform:translateY(-22px)"),
                                  (16.35, "transform:translateY(0)"), (L, "transform:translateY(0)")]) + run("hop", L))
    body.append(f'<g class="heart">{icon(HEART, PEN, 6, x7 + 10, y7 - 46)}</g>')
    # scan beams
    for k, (t0, d) in enumerate(scans):
        css.append(stops(f"sc{k}", L, [(0, "opacity:0;transform:translateY(0)"), (t0 - .05, "opacity:0;transform:translateY(0)"), (t0, "opacity:1;transform:translateY(0)"),
                                       (t0 + d, f"opacity:1;transform:translateY({3*dy}px)"), (t0 + d + .2, f"opacity:0;transform:translateY({3*dy}px)"), (L, "opacity:0")]) + run(f"sc{k}", L))
        body.append(f'<g transform="translate(0 {gy0-6})"><g class="sc{k}"><rect x="{gx0-24}" y="-26" width="{5*dx+100}" height="26" fill="{GREEN}" opacity=".13"/><rect x="{gx0-24}" y="-2" width="{5*dx+100}" height="4" rx="2" fill="{GREEN}"/></g></g>')
    # the editor
    css.append(stops("hj", L, [(0, "transform:translateY(0)"), (5.2, "transform:translateY(0)"), (5.5, "transform:translateY(-70px)"), (5.9, "transform:translateY(0)"), (15.2, "transform:translateY(0)"), (15.45, "transform:translateY(-26px)"),
                               (15.7, "transform:translateY(0)"), (16.0, "transform:translateY(-26px)"), (16.25, "transform:translateY(0)"), (L, "transform:translateY(0)")]) + run("hj", L))
    css.append(stops("sw", L, [(0, "transform:rotate(-12deg)"), (5.1, "transform:rotate(-12deg)"), (5.5, "transform:rotate(42deg)"), (6.2, "transform:rotate(-12deg)"), (15.0, "transform:rotate(-12deg)"),
                               (15.6, "transform:rotate(75deg)"), (L, "transform:rotate(75deg)")]) + run("sw", L))
    body.append(shadow(180, GY + 4, 56))
    body.append(f'<g transform="translate(144 {GY})"><g class="hj">{editor(7, "sw")}</g></g>')
    css.append(stops("scene", L, [(0, "opacity:1"), (L - 1.4, "opacity:1"), (L - .6, "opacity:0"), (L, "opacity:0")]) + run("scene", L))
    return night(W, H, "Seventeen pixel monsters, one for each pattern. A scan flags four of them together, and the editor with the red pen clears them. A second scan flags just one, and the editor lowers the pen and lets it stay; the monster gets a heart and hops.",
                 f'<g class="scene">{"".join(body)}</g>', "".join(css), ".sc0,.sc1{opacity:0}")


# ================================================================= clones
def clones():
    """Five identical posts get five different looks."""
    L, W, H, GY = 14.0, 1200, 360, 300
    css, body = [LEG_CSS, "@keyframes cb{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}.cb{animation:cb .8s steps(1) infinite}"], []
    body.append(stars(W, H, 50, 41, 220))
    body.append(f'<rect x="0" y="{GY}" width="{W}" height="{H-GY}" fill="#10172b"/><rect x="0" y="{GY}" width="{W}" height="6" fill="#2a3558"/>')
    HATS = {"cap": ["..HHHHHH..", ".HHHHHHHH.", "HHHHHHHHHH"], "top": ["..HHHHHH..", "..HHHHHH..", "HHHHHHHHHH"],
            "bean": ["...HHHH...", "..HHHHHH..", ".HHHHHHHH."], "crown": ["H.H.HH.H.H", "HHHHHHHHHH", "HHHHHHHHHH"],
            "ant": ["....HH....", "....HH....", "..HHHHHH.."]}
    FACE = [".SSSSSSSS.", ".SKSSSSKS.", ".SSSSSSSS.", "..SSSSSS.."]
    BODY = [".BBBBBBBB.", "BBBBBBBBBB", "BBBBBBBBBB", ".BBBBBBBB.", ".BB....BB.", ".KK....KK."]
    grey = {"H": "#9aa3b2", "S": "#c9ccd6", "B": "#8a93a6", "K": "#454c60"}
    looks = [("cap", "#e0524a", "#f0c9a0", "#2f8fa8", HEART, "#e0524a"), ("top", "#ffcf4a", "#e8b890", "#5fae5a", STARP, "#ffcf4a"),
             ("bean", "#9a6fd6", "#f6d3b0", "#e08a3c", BOLT, "#9a6fd6"), ("crown", "#4fc3d8", "#d9a07a", "#e07aa8", DROP, "#4fc3d8"),
             ("ant", "#f3ecdc", "#f0c9a0", "#4c7bd9", NOTE, "#f3ecdc")]
    S = 8
    xs = [200 + i * 200 for i in range(5)]
    ts = [3.4 + 1.9 * i for i in range(5)]
    for i, (cx, t) in enumerate(zip(xs, ts)):
        hat, hc, sk, bc, ic, icc = looks[i]
        body.append(shadow(cx, GY + 3, 38))
        before = sprite(HATS["cap"] + FACE + BODY, grey, S, -40, -13 * S)
        before_b = (f'<rect x="-30" y="{-13*S-62}" width="60" height="44" rx="10" fill="#ffffff"/><path d="M-6,{-13*S-18} L6,{-13*S-18} L0,{-13*S-8} Z" fill="#ffffff"/>'
                    f'{sprite(BLOB, BLOB_PAL, 4, -24, -13*S-56)}')
        after = sprite(HATS[hat] + FACE + BODY, {"H": hc, "S": sk, "B": bc, "K": "#1d1d26"}, S, -40, -13 * S)
        after_b = (f'<rect x="-30" y="{-13*S-62}" width="60" height="44" rx="10" fill="#ffffff"/><path d="M-6,{-13*S-18} L6,{-13*S-18} L0,{-13*S-8} Z" fill="#ffffff"/>'
                   f'{icon(ic, "#2b3350" if icc == "#f3ecdc" else icc, 6, -15, -13*S-54)}')
        css.append(stops(f"b{i}", L, [(0, "opacity:1;transform:scale(1)"), (t, "opacity:1;transform:scale(1)"), (t + .05, "opacity:0;transform:scale(1.25,.6)"), (L - 1.4, "opacity:0"), (L - .6, "opacity:0"), (L, "opacity:0")]) + run(f"b{i}", L, "transform-box:fill-box;transform-origin:50% 100%"))
        css.append(stops(f"a{i}", L, [(0, "opacity:0;transform:scale(.6)"), (t, "opacity:0;transform:scale(.6)"), (t + .2, "opacity:1;transform:scale(1.2,.85)"), (t + .45, "opacity:1;transform:scale(1)"), (L - 1.4, "opacity:1;transform:scale(1)"), (L - .6, "opacity:0;transform:scale(1)"), (L, "opacity:0")]) + run(f"a{i}", L, "transform-box:fill-box;transform-origin:50% 100%"))
        p, pc = poof(f"po{i}", L, t, cx, GY - 60, hc, 6, 3.0)
        css.append(pc)
        body.append(f'<g transform="translate({cx} {GY})"><g class="b{i}">{before}{before_b}</g><g class="cb" style="animation-delay:-{i*.15}s"><g class="a{i}">{after}{after_b}</g></g></g>{p}')
    # editor runs along and taps each clone
    arrive = [x - 150 for x in xs]
    pts = [(0, -110), (.2, -110)]
    for i, (ax, t) in enumerate(zip(arrive, ts)):
        pts += [(t - .9, ax), (t + .5, ax)]
    pts += [(ts[-1] + 1.8, 1280), (L, 1280)]
    css.append(track("hx", L, pts, up="linear", down="linear", prop="transform:translateX({v}px)"))
    jump = [(0, 0)]
    for t in ts:
        jump += [(t - .3, 0), (t - .1, -46), (t, -20), (t + .25, 0)]
    css.append(track("hy", L, jump + [(L, 0)]))
    swing = [(0, -8)]
    for t in ts:
        swing += [(t - .2, -8), (t, 40), (t + .3, -8)]
    css.append(stops("sw", L, [(t, f"transform:rotate({a}deg)") for t, a in sorted(set(swing))] + [(L, "transform:rotate(-8deg)")]) + run("sw", L))
    body.append(f'<g transform="translate(0 {GY})"><g class="hx"><g class="hy">{editor(6, "sw")}</g></g></g>')
    css.append(stops("scene", L, [(0, "opacity:1"), (L - 1.4, "opacity:1"), (L - .6, "opacity:0"), (L, "opacity:0")]) + run("scene", L))
    return night(W, H, "Five identical grey characters, each with the same green slop blob in its speech bubble. An editor with a red pen runs along and taps each one. Each becomes different: its own hat, its own colours and its own picture in the bubble.",
                 f'<g class="scene">{"".join(body)}</g>', "".join(css), ".b0,.b1,.b2,.b3,.b4{opacity:0}.hx{transform:translateX(1280px)}")


# ================================================================= cartridge
def cartridge():
    """Install: a skill cartridge drops into a sleepy robot, which wakes up and scares the slop away."""
    L, W, H, GY = 12.0, 1200, 300, 262
    css, body = [LEG_CSS, "@keyframes slp{0%,100%{transform:translateY(0)}50%{transform:translateY(-2px)}}.slp{animation:slp 1.2s steps(1) infinite}"], []
    body.append(stars(W, H, 50, 51, 170))
    body.append(f'<rect x="0" y="{GY}" width="{W}" height="{H-GY}" fill="#10172b"/><rect x="0" y="{GY}" width="{W}" height="6" fill="#2a3558"/>')
    cx, S = 520, 11
    rw, rh = 12 * S, 14 * S
    grey = {"M": "#7d869e", "L": "#aab2c8", "W": "#dfe3ee", "K": "#2a3050"}
    blue = {"M": "#4c7bd9", "L": "#ffd24a", "W": "#ffffff", "K": "#141a30"}
    body.append(shadow(cx, GY + 3, 70))
    css.append(stops("sleep", L, [(0, "opacity:1"), (2.7, "opacity:1"), (2.8, "opacity:0"), (L - 1.4, "opacity:0"), (L - .6, "opacity:1"), (L, "opacity:1")]) + run("sleep", L))
    css.append(stops("awake", L, [(0, "opacity:0"), (2.7, "opacity:0"), (2.8, "opacity:1"), (L - 1.4, "opacity:1"), (L - .6, "opacity:0"), (L, "opacity:0")]) + run("awake", L))
    css.append(stops("dance", L, [(0, "transform:translateY(0)"), (3.2, "transform:translateY(0)"), (3.45, "transform:translateY(-26px)"), (3.7, "transform:translateY(0)"), (3.95, "transform:translateY(-26px)"),
                                  (4.2, "transform:translateY(0)"), (L, "transform:translateY(0)")]) + run("dance", L))
    zz = icon(["XXX", "..X", ".X.", "XXX"], "#c3cae0", 5, 0, 0)
    css.append(window("zz", L, 0, 2.6, fade=.1))
    robot_group = (f'<g class="dance"><g class="sleep"><g class="slp">{sprite(ROBOT, grey, S, cx - rw / 2, GY - rh)}</g></g>'
                   f'<g class="awake">{sprite(ROBOT, blue, S, cx - rw / 2, GY - rh)}'
                   f'<g transform="translate({cx+rw/2-8} {GY-rh+60})"><g class="penhold"><g transform="rotate(-55)"><rect x="-6" y="-5" width="70" height="10" rx="4" fill="{PEN}"/><rect x="42" y="-5" width="10" height="10" fill="{CREAM}"/><path d="M64,-5 L78,0 L64,5 Z" fill="#141a30"/></g></g></g></g>'
                   f'<g class="zz" transform="translate({cx+40} {GY-rh-10})">{zz}<g transform="translate(18 -18)">{icon(["XXX", "..X", ".X.", "XXX"], "#c3cae0", 4)}</g></g></g>')
    css.append("@keyframes ph{0%,100%{transform:rotate(0)}50%{transform:rotate(-10deg)}}.penhold{animation:ph .7s steps(1) infinite}")
    body.append(robot_group)
    # eyes flash and stars when it wakes
    css.append(stops("flash", L, [(0, "opacity:0"), (2.55, "opacity:0"), (2.7, "opacity:.9"), (3.1, "opacity:0"), (L, "opacity:0")]) + run("flash", L))
    body.append(f'<g class="flash">{sprite(ROBOT, {k: "#ffffff" for k in "MLWK"}, S, cx - rw / 2, GY - rh)}</g>')
    p, pc = poof("wk", L, 2.7, cx, GY - rh - 6, GOLD, 8, 4.5)
    css.append(pc); body.append(p)
    # the cartridge drops into the top of the head
    css.append(track("cart", L, [(0, -240), (.5, -240), (1.5, -4), (1.7, -20), (1.9, -4), (2.3, 26), (2.6, 26), (2.9, 26), (3.1, 120), (L, 120)]))
    css.append(stops("cartv", L, [(0, "opacity:1"), (2.9, "opacity:1"), (3.0, "opacity:0"), (L, "opacity:0")]) + run("cartv", L))
    cart = (f'<g transform="translate({cx-42} {GY-rh-60})"><g class="cart"><g class="cartv"><rect x="0" y="0" width="84" height="62" rx="7" fill="#2b3350" stroke="#4a5586" stroke-width="3"/>'
            f'<rect x="8" y="8" width="68" height="34" rx="4" fill="{PAPER2}"/><rect x="22" y="2" width="40" height="5" rx="2" fill="#0f1628"/>'
            f'<g transform="translate(24 28) rotate(-35)"><rect x="-14" y="-3" width="30" height="6" rx="2" fill="{PEN}"/><path d="M-14,-3 L-20,0 L-14,3 Z" fill="#1d1d26"/></g>'
            f'<text x="42" y="56" style="font-size:12px;font-weight:700;fill:{CREAM};text-anchor:middle" textLength="66" lengthAdjust="spacingAndGlyphs">SKILL.md</text></g></g></g>')
    body.append(cart)
    # three slop blobs on the right run away once the robot wakes
    for k, bx in enumerate((860, 930, 1000)):
        a = 3.5 + k * .25
        css.append(stops(f"fl{k}", L, [(0, "opacity:1;transform:translateX(0)"), (a, "opacity:1;transform:translateX(0)"), (a + .15, "opacity:1;transform:translateX(0)"), (a + 1.8, "opacity:1;transform:translateX(420px)"), (a + 2.0, "opacity:0;transform:translateX(440px)"), (L, "opacity:0;transform:translateX(440px)")]) + run(f"fl{k}", L))
        css.append(f"@keyframes sh{k}{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-8px)}}}}")
        body.append(f'<g class="fl{k}"><g transform="translate({bx} {GY-36})"><g style="animation:sh{k} {.9 if a else 1}s steps(1) infinite">{sprite(BLOB, BLOB_PAL, 4)}</g></g></g>')
    ex = ""
    css.append(window("exa", L, 3.4, 4.3, fade=.08))
    for bx in (860, 930, 1000):
        ex += icon(EXCL, PEN, 4, bx + 12, GY - 80)
    body.append(f'<g class="exa">{ex}</g>')
    css.append(stops("scene", L, [(0, "opacity:1"), (L - 1.4, "opacity:1"), (L - .6, "opacity:0"), (L, "opacity:0")]) + run("scene", L))
    return night(W, H, "A grey sleepy robot gets a skill cartridge labelled SKILL.md dropped into its head. It lights up blue, grabs a red pen and hops, and the three green slop blobs nearby panic and run away.",
                 f'<g class="scene">{"".join(body)}</g>', "".join(css), ".flash,.sleep,.cartv,.fl0,.fl1,.fl2{opacity:0}.awake{opacity:1}")


SCENES = (("hero", hero), ("factory", factory), ("zoo", zoo), ("clones", clones), ("cartridge", cartridge))
