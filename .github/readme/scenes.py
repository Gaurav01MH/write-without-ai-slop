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
    L, V, XC, GY, S = 24.0, 100, 110, 262, 5
    css, sky, mid, world, front, bursts = [LEG_CSS, f'.coin{{font-weight:800;fill:#7a4a05;text-anchor:middle;font-family:{MONO}}}'], [], [], [], [], []
    W, H = 600, 336
    # --- sky: stars, a moon, a skyline of paper piles that scrolls slowly
    sky.append(stars(W, H, 34, 11, 170))
    sky.append(f'<circle cx="330" cy="92" r="20" fill="#ece6c9"/><circle cx="324" cy="86" r="4" fill="#d8d1b0"/><circle cx="337" cy="99" r="3" fill="#d8d1b0"/>')
    r = random.Random(3)
    city, x = "", 0
    while x < 360:
        bw = r.choice((40, 56, 72)); bh = r.randrange(40, 100, 10)
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
    mid.append(f'<defs><g id="tile">{tile}</g></defs><g class="gr">' + "".join(f'<use href="#tile" x="{k*120}"/>' for k in range(7)) + '</g>')
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
    world.append(f'<g transform="translate({fx:.0f} {GY})"><rect x="-3" y="-170" width="6" height="170" fill="#d9d2bd"/><circle cx="0" cy="-175" r="8" fill="{GOLD}"/>'
                 f'<g class="pen_up"><g transform="translate(3 -70)"><path d="M0,0 L74,24 L0,48 Z" fill="{GREEN}" stroke="#2c8a5a" stroke-width="3" stroke-linejoin="round"/>{icon(CHECK, "#ffffff", 5, 14, 12)}</g></g></g>')
    rc = random.Random(9)
    for k in range(18):
        dx, dy = rc.uniform(-120, 120), rc.uniform(-60, 50)
        col = rc.choice((PEN, GOLD, GREEN, "#7e8cf0", "#ffffff"))
        t0 = ft + .1 + rc.uniform(0, .25)
        css.append(stops(f"cf{k}", L, [(0, "opacity:0;transform:translate(0,0)"), (t0, "opacity:0;transform:translate(0,0)"), (t0 + .05, "opacity:1;transform:translate(0,0)"),
                                       (t0 + 1.4, f"opacity:1;transform:translate({dx:.0f}px,{dy+130:.0f}px)"), (t0 + 1.9, f"opacity:0;transform:translate({dx*1.1:.0f}px,{dy+170:.0f}px)"), (L, "opacity:0")]) + run(f"cf{k}", L))
        HIDE.append(f"cf{k}")
        world.append(f'<g transform="translate({fx:.0f} {GY-180})"><rect class="cf{k}" x="0" y="0" width="{rc.choice((6, 8))}" height="{rc.choice((6, 8))}" fill="{col}"/></g>')

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
    sb = (f'<rect x="432" y="14" width="152" height="46" rx="10" fill="#0a1020" stroke="#2a3558" stroke-width="2"/>'
          f'{sprite(BLOB, BLOB_PAL, 2, 444, 28)}'
          f'<circle cx="532" cy="37" r="12" fill="{GOLD}" stroke="#c98a14" stroke-width="2.5"/><circle cx="532" cy="37" r="7.5" fill="none" stroke="#e6a92c" stroke-width="1.6"/>')
    d1, c1 = digits("sb", L, 476, 49, (3.4, 6.4, 12.2, 17.0), 28, SLOP_L)
    d2, c2 = digits("sc", L, 550, 49, coin_t, 28, GOLD)
    css += [c1, c2]
    front.append(sb + d1 + d2)
    front.append(f'<text class="sans" x="168" y="52" style="font-size:34px;font-weight:800;fill:{CREAM}" textLength="236" lengthAdjust="spacingAndGlyphs">no-ai-slop</text>')

    css.append(stops("scene", L, [(0, "opacity:1"), (22.8, "opacity:1"), (23.7, "opacity:0"), (L, "opacity:0")]) + run("scene", L))
    body = f'<g class="scene">{"".join(sky)}{"".join(mid)}<g class="world">{"".join(world)}</g>{"".join(front)}</g>'
    return night(W, H, "no-ai-slop. A pixel-art editor in a red beret runs along ruled paper and stomps four green slop blobs with a red pen: a plain one, a second, a trio of small ones and one with a question balloon. The editor collects two coins, 42 and 9, instead of striking them, and reaches a green finish flag. A scoreboard counts four blobs struck and two coins kept.",
                 body, "".join(css), scale=1.4)


# ================================================================= zoo
def zoo():
    """17 pattern monsters. A scan flags four together and the editor clears them; a second scan flags one and the editor lets it be."""
    L, W, H = 22.0, 600, 336
    css, body = [LEG_CSS, "@keyframes mb{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}.mb{animation:mb 1s steps(1) infinite}",
                 "@keyframes shk{0%,100%{transform:translateX(0)}50%{transform:translateX(3px)}}.shk{animation:shk .12s steps(1) infinite}"], []
    body.append(stars(W, H, 40, 31, 230))
    GY = 296
    body.append(f'<rect x="0" y="{GY}" width="{W}" height="{H-GY}" fill="#10172b"/><rect x="0" y="{GY}" width="{W}" height="6" fill="#2a3558"/>')
    gx0, gy0, dx, dy, S = 138, 40, 80, 80, 5
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
        body.append(shadow(x + 17, y + 42, 21))
        inner = f'<g class="mb" style="animation-delay:-{(i*.17)%1:.2f}s">{sprite(g, pal, S)}'
        if i in A or i in B:
            col = PEN if i in A else "#f0b45a"
            t0 = scans[0][0] if i in A else scans[1][0]
            tb = beam_time(t0, 3.4, i)
            end = 5.5 if i in A else 18.8
            css.append(window(f"rd{i}", L, tb, end, fade=.12))
            inner += f'<g class="rd{i}"><g class="shk">{sprite(g, monster_pal(i, col), S)}</g></g>'
            mark = icon(EXCL, PEN, 3, 14, -26) if i in A else icon(QMARK, "#f0b45a", 3, 10, -28)
            css.append(window(f"mk{i}", L, tb, end if i in A else 15.0, fade=.12))
            inner += f'<g class="mk{i}">{mark}</g>'
        inner += "</g>"
        if i in A:
            css.append(stops(f"vs{i}", L, [(0, "opacity:1"), (5.5, "opacity:1"), (5.6, "opacity:0"), (9.8, "opacity:0"), (10.4, "opacity:1"), (L - 1.4, "opacity:1"), (L - .6, "opacity:0"), (L, "opacity:0")]) + run(f"vs{i}", L))
            p, pc = poof(f"pz{i}", L, 5.55, x + 17, y + 17, MONSTER_COLORS[i % 6], 4, 2.4)
            css.append(pc)
            body.append(f'<g transform="translate({x} {y})"><g class="vs{i}">{inner}</g></g>{p}')
        else:
            css.append(stops(f"vs{i}", L, [(0, "opacity:1"), (L - 1.4, "opacity:1"), (L - .6, "opacity:0"), (L, "opacity:0")]) + run(f"vs{i}", L))
            body.append(f'<g transform="translate({x} {y})"><g class="vs{i}">{inner}</g></g>')
    # the spared one gets a heart and a happy hop
    x7, y7 = gx0 + 1 * dx, gy0 + 1 * dy
    css.append(window("heart", L, 15.3, 19.0, fade=.15))
    css.append(stops("hop", L, [(0, "transform:translateY(0)"), (15.3, "transform:translateY(0)"), (15.55, "transform:translateY(-16px)"), (15.8, "transform:translateY(0)"), (16.1, "transform:translateY(-16px)"),
                                  (16.35, "transform:translateY(0)"), (L, "transform:translateY(0)")]) + run("hop", L))
    body.append(f'<g class="heart">{icon(HEART, PEN, 4, x7 + 6, y7 - 30)}<text class="serif" x="{x7 + 34}" y="{y7 - 14}" style="font-size:15px">stet</text></g>')
    # scan beams
    for k, (t0, d) in enumerate(scans):
        css.append(stops(f"sc{k}", L, [(0, "opacity:0;transform:translateY(0)"), (t0 - .05, "opacity:0;transform:translateY(0)"), (t0, "opacity:1;transform:translateY(0)"),
                                       (t0 + d, f"opacity:1;transform:translateY({3*dy}px)"), (t0 + d + .2, f"opacity:0;transform:translateY({3*dy}px)"), (L, "opacity:0")]) + run(f"sc{k}", L))
        body.append(f'<g transform="translate(0 {gy0-6})"><g class="sc{k}"><rect x="{gx0-24}" y="-26" width="{5*dx+100}" height="26" fill="{GREEN}" opacity=".13"/><rect x="{gx0-24}" y="-2" width="{5*dx+100}" height="4" rx="2" fill="{GREEN}"/></g></g>')
    # the editor
    css.append(stops("hj", L, [(0, "transform:translateY(0)"), (5.2, "transform:translateY(0)"), (5.5, "transform:translateY(-50px)"), (5.9, "transform:translateY(0)"), (15.2, "transform:translateY(0)"), (15.45, "transform:translateY(-18px)"),
                               (15.7, "transform:translateY(0)"), (16.0, "transform:translateY(-18px)"), (16.25, "transform:translateY(0)"), (L, "transform:translateY(0)")]) + run("hj", L))
    css.append(stops("sw", L, [(0, "transform:rotate(-12deg)"), (5.1, "transform:rotate(-12deg)"), (5.5, "transform:rotate(42deg)"), (6.2, "transform:rotate(-12deg)"), (15.0, "transform:rotate(-12deg)"),
                               (15.6, "transform:rotate(75deg)"), (L, "transform:rotate(75deg)")]) + run("sw", L))
    body.append(f'<text x="24" y="60" style="font-size:40px;font-weight:800;fill:{GOLD}">17</text>')
    body.append(shadow(78, GY + 3, 40))
    body.append(f'<g transform="translate(48 {GY})"><g class="hj">{editor(5, "sw")}</g></g>')
    css.append(stops("scene", L, [(0, "opacity:1"), (L - 1.4, "opacity:1"), (L - .6, "opacity:0"), (L, "opacity:0")]) + run("scene", L))
    return night(W, H, "Seventeen pixel monsters, one for each pattern. A scan flags four of them together, and the editor with the red pen clears them. A second scan flags just one, and the editor lowers the pen and lets it stay; the monster gets a heart and hops.",
                 f'<g class="scene">{"".join(body)}</g>', "".join(css), ".sc0,.sc1{opacity:0}", scale=1.4)


SCENES = (("hero", hero), ("zoo", zoo))
