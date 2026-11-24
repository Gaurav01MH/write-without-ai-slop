"""The "try it" strip, the three-modes robots and the results screen. All drawn in design units, shown at 1.4 times."""
from artlib import stops, run, esc, PEN, SANS, MONO
from pixel import *
from scenes import track, shadow, LEG_CSS

SCALE = 1.4


def label(x, y, text, size=15, name=None, fill=CREAM, anchor="middle", weight=700):
    cls = f"sans {name}" if name else "sans"
    return f'<text class="{cls}" x="{x}" y="{y}" style="font-size:{size}px;font-weight:{weight};fill:{fill};text-anchor:{anchor}">{esc(text)}</text>'


# ================================================================= try it
def tryit():
    """Install, paste, see: a cartridge wakes a robot, it eats a slop-covered sheet and hands back a clean one."""
    L, W, H, FY, S = 14.0, 600, 250, 184, 8
    cx = 300
    css, body = [LEG_CSS], []
    body.append(stars(W, H, 34, 61, 130))
    body.append(f'<rect x="0" y="{FY}" width="{W}" height="{H-FY}" fill="#10172b"/><rect x="0" y="{FY}" width="{W}" height="4" fill="#2a3558"/>')
    rw, rh = 12 * S, 14 * S
    grey = {"M": "#7d869e", "L": "#aab2c8", "W": "#dfe3ee", "K": "#2a3050"}
    blue = {"M": "#4c7bd9", "L": "#ffd24a", "W": "#ffffff", "K": "#141a30"}
    body.append(shadow(cx, FY + 2, 56))
    css.append(stops("sleep", L, [(0, "opacity:1"), (2.7, "opacity:1"), (2.8, "opacity:0"), (L - 1.4, "opacity:0"), (L - .6, "opacity:1"), (L, "opacity:1")]) + run("sleep", L))
    css.append(stops("awake", L, [(0, "opacity:0"), (2.7, "opacity:0"), (2.8, "opacity:1"), (L - 1.4, "opacity:1"), (L - .6, "opacity:0"), (L, "opacity:0")]) + run("awake", L))
    css.append(track("dance", L, [(0, 0), (3.2, 0), (3.4, -20), (3.6, 0), (3.8, -20), (4.0, 0), (6.7, 0), (6.9, -8), (7.1, 0), (7.3, -8), (7.5, 0), (7.9, 0), (8.1, -26), (8.4, 0), (L, 0)]))
    css.append("@keyframes slp{0%,100%{transform:translateY(0)}50%{transform:translateY(-2px)}}.slp{animation:slp 1.2s steps(1) infinite}"
               "@keyframes ph{0%,100%{transform:rotate(0)}50%{transform:rotate(-10deg)}}.penhold{animation:ph .7s steps(1) infinite}")
    z = icon(["XXX", "..X", ".X.", "XXX"], "#c3cae0", 4)
    css.append(window("zz", L, 0, 2.6, fade=.1))
    pen_in = (f'<g transform="translate({cx+rw/2-6} {FY-rh+46})"><g class="penhold"><g transform="rotate(-55)"><rect x="-4" y="-4" width="52" height="8" rx="3" fill="{PEN}"/>'
              f'<rect x="32" y="-4" width="8" height="8" fill="{CREAM}"/><path d="M50,-4 L62,0 L50,4 Z" fill="#141a30"/></g></g></g>')
    body.append(f'<g class="dance"><g class="sleep"><g class="slp">{sprite(ROBOT, grey, S, cx - rw / 2, FY - rh)}</g></g><g class="awake">{sprite(ROBOT, blue, S, cx - rw / 2, FY - rh)}{pen_in}</g>'
                f'<g class="zz" transform="translate({cx+30} {FY-rh-6})">{z}</g></g>')
    # wake flash and burst
    css.append(stops("flash", L, [(0, "opacity:0"), (2.55, "opacity:0"), (2.7, "opacity:.9"), (3.1, "opacity:0"), (L, "opacity:0")]) + run("flash", L))
    HIDE.append("flash")
    body.append(f'<g class="flash">{sprite(ROBOT, {k: "#ffffff" for k in "MLWK"}, S, cx - rw / 2, FY - rh)}</g>')
    p, pc = poof("wk", L, 2.7, cx, FY - rh, GOLD, 6, 4.2)
    css.append(pc); body.append(p)
    # the cartridge drops into the head
    css.append(track("cart", L, [(0, -200), (.5, -200), (1.5, -2), (1.7, -16), (1.9, -2), (2.3, 20), (2.6, 20), (3.1, 90), (L, 90)]))
    css.append(stops("cartv", L, [(0, "opacity:1"), (2.9, "opacity:1"), (3.0, "opacity:0"), (L, "opacity:0")]) + run("cartv", L))
    body.append(f'<g transform="translate({cx-34} {FY-rh-50})"><g class="cart"><g class="cartv"><rect width="68" height="50" rx="6" fill="#2b3350" stroke="#4a5586" stroke-width="2.5"/>'
                f'<rect x="7" y="7" width="54" height="26" rx="3" fill="{PAPER2}"/><rect x="18" y="2" width="32" height="4" rx="2" fill="#0f1628"/>'
                f'<g transform="translate(20 22) rotate(-35)"><rect x="-12" y="-2.5" width="24" height="5" rx="2" fill="{PEN}"/><path d="M-12,-2.5 L-17,0 L-12,2.5 Z" fill="#1d1d26"/></g>'
                f'<text x="34" y="45" style="font-size:9px;font-weight:700;fill:{CREAM};text-anchor:middle" textLength="52" lengthAdjust="spacingAndGlyphs">SKILL.md</text></g></g></g>')
    # step 2: a sheet covered in slop walks in and is eaten
    sx = [(0, -60), (4.6, -60), (5.5, cx - 120), (6.0, cx - 120), (6.8, cx - 30), (7.1, cx - 8)]
    css.append(stops("sin", L, [(t, f"transform:translateX({x}px);opacity:1") for t, x in sx] + [(7.3, f"transform:translateX({cx}px) scale(.2);opacity:0"), (L, f"transform:translateX({cx}px) scale(.2);opacity:0")]) + run("sin", L, "transform-origin:0 0"))
    sheet = sprite(SHEET, SHEET_PAL, 4, -20, -44)
    blobs = "".join(sprite(BLOB, BLOB_PAL, 2, bx, -62) for bx in (-30, -8, 14))
    body.append(f'<g transform="translate(0 {FY})"><g class="sin">{sheet}{blobs}</g></g>')
    # step 3: slop flies out and bursts, a clean sheet and a check come back
    for k, (ox, oy) in enumerate(((60, -120), (110, -150), (160, -110))):
        t = 7.4 + k * .18
        css.append(stops(f"fy{k}", L, [(0, "opacity:0;transform:translate(0,0)"), (t, "opacity:0;transform:translate(0,0)"), (t + .05, "opacity:1;transform:translate(0,0)"),
                                       (t + 1.1, f"opacity:1;transform:translate({ox}px,{oy}px)"), (t + 1.15, f"opacity:0;transform:translate({ox}px,{oy}px)"), (L, "opacity:0")]) + run(f"fy{k}", L))
        HIDE.append(f"fy{k}")
        body.append(f'<g transform="translate({cx+20} {FY-70})"><g class="fy{k}">{sprite(BLOB, BLOB_PAL, 3)}</g></g>')
        p2, pc2 = poof(f"fp{k}", L, t + 1.1, cx + 20 + ox + 18, FY - 70 + oy + 13, SLOP, 5, 2.6)
        css.append(pc2); body.append(p2)
    css.append(stops("cl", L, [(0, "opacity:0;transform:translateX(0) scale(.3)"), (8.0, "opacity:0;transform:translateX(0) scale(.3)"), (8.2, "opacity:1;transform:translateX(0) scale(.6)"),
                               (9.0, "opacity:1;transform:translateX(150px) scale(1)"), (L - 1.4, "opacity:1;transform:translateX(150px) scale(1)"), (L - .6, "opacity:0;transform:translateX(150px) scale(1)"), (L, "opacity:0")]) + run("cl", L))
    HIDE.append("cl")
    body.append(f'<g transform="translate({cx+70} {FY})"><g class="cl">{sprite(SHEET, SHEET_PAL, 5, -25, -55)}</g></g>')
    css.append(window("chk", L, 9.1, L - 1.4, fade=.2))
    body.append(f'<g class="chk">{icon(CHECK, GREEN, 7, cx + 190, FY - 120)}</g>')
    # step labels
    tiles = [("install", 130, .3, 4.5), ("paste", 300, 4.6, 8.2), ("see", 470, 8.3, 12.6)]
    for k, (word, tx, a, b) in enumerate(tiles):
        css.append(window(f"tl{k}", L, a, b, fade=.15))
        body.append(f'<rect x="{tx-62}" y="{FY+16}" width="124" height="34" rx="10" fill="#1b2440" stroke="#2a3558" stroke-width="2"/>')
        body.append(f'<rect class="tl{k}" x="{tx-62}" y="{FY+16}" width="124" height="34" rx="10" fill="{GOLD}" fill-opacity=".14" stroke="{GOLD}" stroke-width="2.5"/>')
        body.append(label(tx, FY + 39, word, 17))
    css.append(stops("scene", L, [(0, "opacity:1"), (L - 1.4, "opacity:1"), (L - .6, "opacity:0"), (L, "opacity:0")]) + run("scene", L))
    return night(W, H, "Install, paste, see. A sleepy grey robot gets a skill cartridge labelled SKILL.md dropped into its head and wakes up blue with a red pen. It eats a sheet of paper covered in green slop blobs, the blobs fly out and burst, and it hands back a clean sheet with a green check.",
                 f'<g class="scene">{"".join(body)}</g>', "".join(css), ".sleep,.cartv,.sin{opacity:0}.awake,.cl{opacity:1}.cl{transform:translateX(150px)}.chk{opacity:1}.tl2{opacity:1}", scale=SCALE)


# ================================================================= robots
def robots():
    """The three ways to use it, as three robots and what each hands back."""
    L, W, H, FY, S = 15.0, 600, 250, 204, 6
    css, body = [LEG_CSS, "@keyframes rb{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}.rb{animation:rb .9s steps(1) infinite}"
                 "@keyframes scr{0%,100%{transform:translate(0,0)}50%{transform:translate(-4px,3px)}}.scr{animation:scr .3s steps(1) infinite}"], []
    body.append(stars(W, H, 34, 71, 150))
    body.append(f'<rect x="0" y="{FY}" width="{W}" height="{H-FY}" fill="#10172b"/><rect x="0" y="{FY}" width="{W}" height="4" fill="#2a3558"/>')
    cols = [("check", {"M": "#9a5fd0", "L": "#e0c0ff"}, 1.0, 5.0), ("rewrite", {"M": "#d65a43", "L": "#ffd0c4"}, 5.4, 9.8), ("write", {"M": "#4c7bd9", "L": "#a8c4ff"}, 10.2, 14.0)]
    for i, (word, pl, a, b) in enumerate(cols):
        ox = 10 + i * 196
        pal = {"M": pl["M"], "L": pl["L"], "W": "#ffffff", "K": "#141a30"}
        # the active column is lit
        css.append(window(f"on{i}", L, a, b, fade=.2))
        body.append(f'<rect class="on{i}" x="{ox-4}" y="46" width="192" height="{FY-46+46}" rx="14" fill="{GOLD}" fill-opacity=".07" stroke="{GOLD}" stroke-width="2"/>')
        body.append(shadow(ox + 36, FY + 1, 40))
        body.append(f'<g transform="translate({ox} {FY-84})"><g class="rb" style="animation-delay:-{i*.3}s">{sprite(ROBOT, pal, S)}</g></g>')
        body.append(label(ox + 92, FY + 38, word, 21))
        # the result card
        cx0, cy0, cw, chh = ox + 84, 100, 96, 104
        body.append(f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{chh}" rx="8" fill="#1b2440" stroke="#2a3558" stroke-width="2"/>')
        t0 = a + .6
        if i == 0:   # check: a lens, then findings with red dots
            css.append(stops("mg", L, [(0, "transform:translate(0,0)"), (a, "transform:translate(0,0)"), (a + 2.6, "transform:translate(0,40px)"), (L, "transform:translate(0,40px)")]) + run("mg", L))
            body.append(f'<g class="mg"><circle cx="{ox+30}" cy="{FY-62}" r="9" fill="#ffffff" fill-opacity=".12" stroke="#e0c0ff" stroke-width="3"/><path d="M{ox+37},{FY-55} L{ox+45},{FY-47}" stroke="#e0c0ff" stroke-width="4" stroke-linecap="round"/></g>')
            for k in range(3):
                css.append(window(f"fd{k}", L, t0 + k * .7, b + .4, fade=.12))
                yy = cy0 + 20 + k * 28
                body.append(f'<g class="fd{k}"><rect x="{cx0+12}" y="{yy-5}" width="10" height="10" fill="{PEN}"/><rect x="{cx0+30}" y="{yy-3}" width="{56-k*10}" height="6" rx="3" fill="{CREAM}" opacity=".7"/></g>')
        elif i == 1:   # rewrite: a struck line becomes a shorter one, plus a changed list
            body.append(f'<rect x="{cx0+10}" y="{cy0+12}" width="76" height="46" rx="3" fill="{PAPER2}"/>')
            for k in range(3):
                body.append(f'<rect x="{cx0+16}" y="{cy0+19+k*13}" width="{[64, 52, 58][k]}" height="5" rx="2.5" fill="#b9ad8f"/>')
            css.append(stops("sk", L, [(0, "stroke-dashoffset:1;opacity:0"), (t0, "stroke-dashoffset:1;opacity:0"), (t0 + .01, "stroke-dashoffset:1;opacity:1"), (t0 + .6, "stroke-dashoffset:0;opacity:1"), (L, "stroke-dashoffset:0;opacity:1")]) + run("sk", L, "stroke-dasharray:1"))
            body.append(f'<path class="sk" pathLength="1" d="M{cx0+13},{cy0+22} L{cx0+84},{cy0+21}" stroke="{PEN}" stroke-width="2.6" stroke-linecap="round" fill="none"/>')
            css.append(window("chg", L, t0 + 1.0, b + .4, fade=.12))
            body.append(f'<g class="chg">{"".join(f"<rect x=\"{cx0+14}\" y=\"{cy0+68+k*12}\" width=\"6\" height=\"6\" fill=\"{GREEN}\"/><rect x=\"{cx0+26}\" y=\"{cy0+69+k*12}\" width=\"{[56, 44][k]}\" height=\"4\" rx=\"2\" fill=\"{CREAM}\" opacity=\".6\"/>" for k in range(2))}</g>')
        else:        # write: clean lines typed out and a check
            for k in range(3):
                css.append(stops(f"ty{k}", L, [(0, "transform:scaleX(0)"), (t0 + k * .6, "transform:scaleX(0)"), (t0 + k * .6 + .9, "transform:scaleX(1)"), (L, "transform:scaleX(1)")]) + run(f"ty{k}", L, "transform-box:fill-box;transform-origin:left center"))
                body.append(f'<rect x="{cx0+10}" y="{cy0+14}" width="76" height="46" rx="3" fill="{PAPER2}"/>' if k == 0 else "")
                body.append(f'<rect class="ty{k}" x="{cx0+16}" y="{cy0+19+k*13}" width="{[64, 52, 58][k]}" height="5" rx="2.5" fill="#7a8a6a"/>')
            css.append(window("wck", L, t0 + 2.2, b + .4, fade=.15))
            body.append(f'<g class="wck">{icon(CHECK, GREEN, 5, cx0 + 30, cy0 + 66)}</g>')
        # a small arm so each robot looks busy
        if i == 2:
            body.append(f'<g transform="translate({ox+66} {FY-40})"><g class="scr"><path d="M0,0 L18,6" stroke="#4c7bd9" stroke-width="7" stroke-linecap="round"/><rect x="16" y="2" width="14" height="4" rx="2" fill="{PEN}"/></g></g>')
        if i == 1:
            css.append(track("swg", L, [(0, 0), (a + .4, 0), (a + .6, 40), (a + 1.0, 0), (L, 0)], prop="transform:rotate({v}deg)"))
            body.append(f'<g transform="translate({ox+66} {FY-46})"><g class="swg"><path d="M0,0 L14,18" stroke="#d65a43" stroke-width="7" stroke-linecap="round"/><rect x="11" y="14" width="5" height="16" rx="2" fill="{PEN}"/></g></g>')
    css.append(stops("scene", L, [(0, "opacity:1"), (L - 1.2, "opacity:1"), (L - .5, "opacity:0"), (L, "opacity:0")]) + run("scene", L))
    return night(W, H, "The three ways to use it, as three robots. Check lists each problem with a red marker. Rewrite strikes a line and shows what changed. Write types clean lines and ends with a green check.",
                 f'<g class="scene">{"".join(body)}</g>', "".join(css), ".sk{opacity:0}", scale=SCALE)


# ================================================================= results
def results():
    """The real numbers as a high-score screen: judged passes per model, and the exact checks."""
    L, W, H = 12.0, 600, 230
    css, body = [LEG_CSS], []
    body.append(stars(W, H, 34, 81, 120))
    FY = 190
    body.append(f'<rect x="0" y="{FY}" width="{W}" height="{H-FY}" fill="#10172b"/><rect x="0" y="{FY}" width="{W}" height="4" fill="#2a3558"/>')
    vals = (54, 56, 56)
    cols = ({"M": "#4c7bd9", "L": "#a8c4ff"}, {"M": "#9a5fd0", "L": "#e0c0ff"}, {"M": "#d65a43", "L": "#ffd0c4"})
    for k, (v, pl) in enumerate(zip(vals, cols)):
        bx = 28 + k * 84
        h = round(v / 57 * 80)
        t = .5 + k * .5
        css.append(stops(f"bar{k}", L, [(0, "transform:scaleY(0)"), (t, "transform:scaleY(0)"), (t + 1.0, "transform:scaleY(1)"), (L - 1.0, "transform:scaleY(1)"), (L - .4, "transform:scaleY(0)"), (L, "transform:scaleY(0)")]) + run(f"bar{k}", L, "transform-box:fill-box;transform-origin:50% 100%"))
        css.append(track(f"rr{k}", L, [(0, 0), (t, 0), (t + 1.0, -h), (t + 1.3, -h - 12), (t + 1.6, -h), (L - 1.0, -h), (L - .4, 0), (L, 0)]))
        css.append(window(f"nm{k}", L, t + 1.0, L - 1.0, fade=.15))
        body.append(f'<rect class="bar{k}" x="{bx}" y="{FY-h}" width="64" height="{h}" rx="4" fill="{pl["M"]}" fill-opacity=".35" stroke="{pl["M"]}" stroke-width="2.5"/>')
        pal = {"M": pl["M"], "L": pl["L"], "W": "#ffffff", "K": "#141a30"}
        body.append(f'<g transform="translate({bx+8} {FY-56})"><g class="rr{k}">{sprite(ROBOT, pal, 4)}</g></g>')
        body.append(f'<text class="nm{k}" x="{bx+32}" y="{FY-h-72}" style="font-size:24px;font-weight:800;fill:{GOLD};text-anchor:middle">{v}</text>')
    body.append(label(150, FY + 26, "of 57 judged", 14, fill="#9aa3c0", weight=600))
    # exact checks
    css.append(stops("big", L, [(0, "opacity:0;transform:scale(.6)"), (3.0, "opacity:0;transform:scale(.6)"), (3.4, "opacity:1;transform:scale(1.12)"), (3.7, "opacity:1;transform:scale(1)"), (L - 1.0, "opacity:1;transform:scale(1)"), (L - .4, "opacity:0"), (L, "opacity:0")]) + run("big", L, "transform-box:fill-box;transform-origin:50% 50%"))
    body.append(f'<g class="big">{icon(CHECK, GREEN, 9, 330, 60)}<text x="408" y="112" style="font-size:60px;font-weight:800;fill:{CREAM}">171</text>'
                f'<text x="520" y="112" style="font-size:24px;font-weight:700;fill:#9aa3c0">/171</text></g>')
    css.append(window("ex", L, 3.8, L - 1.0, fade=.2))
    body.append(label(330, 158, "exact checks", 20, name="ex", anchor="start"))
    for k, (cx_, cy_) in enumerate(((330, 40), (520, 36), (560, 150))):
        css.append(window(f"sp{k}", L, 3.6 + k * .3, 3.6 + k * .3 + 1.6, fade=.2))
        body.append(f'<g class="sp{k}">{icon(STARP, GOLD, 4, cx_, cy_)}</g>')
    css.append(stops("scene", L, [(0, "opacity:1"), (L - 1.0, "opacity:1"), (L - .4, "opacity:0"), (L, "opacity:0")]) + run("scene", L))
    return night(W, H, "A high-score screen with the real results. Three models were judged on 57 cases and passed 54, 56 and 56. The exact checks passed on all 171 answers.",
                 f'<g class="scene">{"".join(body)}</g>', "".join(css), ".bar0,.bar1,.bar2{transform:scaleY(1)}.rr0{transform:translateY(-76px)}.rr1,.rr2{transform:translateY(-79px)}.nm0,.nm1,.nm2,.ex,.big{opacity:1}", scale=SCALE)


STORY = (("tryit", tryit), ("robots", robots), ("results", results))
