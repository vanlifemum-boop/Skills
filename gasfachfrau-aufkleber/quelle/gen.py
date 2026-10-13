import math, random, os

RED = "#F35A37"; AMBER = "#FDA634"; INK = "#1C2A31"; CREAM = "#FBF1DF"; BRICK = "#A8321F"
ANTON = "font-family:Anton;font-weight:400"
FRA_I = "font-family:Fraunces;font-style:italic;font-weight:500"
FRA_IB = "font-family:Fraunces;font-style:italic;font-weight:700"
FRA = "font-family:Fraunces;font-weight:600"
WORD = "font-family:'DejaVu Sans';font-weight:700"


def logo(x, y, h, color=INK, anchor="start"):
    """Logo lockup: flame mark + wordmark, unchanged from the original."""
    fs = h * 0.36
    tw = fs * 0.66 * 14  # approx. width of 'gasfachfrau.de' in DejaVu Sans Bold
    total = h + h * 0.22 + tw
    if anchor == "middle":
        x -= total / 2
    return (f'<image href="logo.png" x="{x}" y="{y}" width="{h}" height="{h}"/>'
            f'<text x="{x + h * 1.22}" y="{y + h * 0.63}" style="{WORD};font-size:{fs}px" fill="{color}">gasfachfrau.de</text>')


def bottle_path(x, y, w, h):
    """Propane bottle silhouette (body + foot) in box x,y,w,h, collar on top."""
    s = lambda px, py: f"{x + px * w / 40:.2f},{y + py * h / 100:.2f}"
    body = (f"M{s(2,36)} C{s(2,22)} {s(10,18)} {s(20,18)} C{s(30,18)} {s(38,22)} {s(38,36)} "
            f"L{s(38,88)} Q{s(38,94)} {s(32,94)} L{s(8,94)} Q{s(2,94)} {s(2,88)} Z")
    foot = f"M{s(6,93)} L{s(34,93)} L{s(34,100)} L{s(6,100)} Z"
    collar = (f"M{s(10,20)} L{s(10,4)} Q{s(10,0)} {s(14,0)} L{s(26,0)} Q{s(30,0)} {s(30,4)} L{s(30,20)} Z "
              f"M{s(14,4.5)} L{s(26,4.5)} L{s(26,11)} L{s(14,11)} Z")
    return body, foot, collar


def svg(w, h, inner, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">'
            f'<defs>{defs}</defs>{inner}</svg>')


# ---------------------------------------------------------------- 1 Pfanne (rund)
def d1():
    W = H = 100
    cx, cy, R = 50, 45, 30
    flames = []
    n = 30
    for i in range(n):
        a = 360 / n * i
        for r0, sc, col in ((R - 1, 1.25, RED), (R - 1, 0.8, AMBER)):
            flames.append(
                f'<path transform="rotate({a + (6 if col == AMBER else 0)} {cx} {cy}) translate({cx} {cy - r0}) scale({sc})" '
                f'd="M-1.7,0 C-1.7,-2.6 -0.2,-3.4 0,-6 C0.6,-3.4 1.7,-2.6 1.7,0 Z" fill="{col}"/>')
    inner = f'''
    <clipPath id="c"><circle cx="50" cy="50" r="50"/></clipPath>
    <g clip-path="url(#c)">
      <rect width="100" height="100" fill="{CREAM}"/>
      {''.join(flames)}
      <g transform="rotate(-24 {cx} {cy})">
        <rect x="{cx + R - 2}" y="{cy - 4}" width="45" height="8" rx="4" fill="{INK}"/>
        <rect x="{cx + R + 14}" y="{cy - 1}" width="10" height="2" rx="1" fill="{CREAM}" opacity=".35"/>
      </g>
      <circle cx="{cx}" cy="{cy}" r="{R}" fill="#2A3A42"/>
      <circle cx="{cx}" cy="{cy}" r="{R - 2.2}" fill="{INK}"/>
      <text x="{cx}" y="{cy - 6}" text-anchor="middle" style="{ANTON};font-size:10.5px;letter-spacing:.3px" fill="{CREAM}">FEUER UND</text>
      <text x="{cx}" y="{cy + 7.5}" text-anchor="middle" style="{ANTON};font-size:14.5px;letter-spacing:.3px" fill="{AMBER}">FLAMME.</text>
      <text x="{cx}" y="{cy + 15.5}" text-anchor="middle" style="{FRA_I};font-size:4.6px" fill="{CREAM}">Aber bitte</text>
      <text x="{cx}" y="{cy + 21}" text-anchor="middle" style="{FRA_IB};font-size:4.6px" fill="{CREAM}">unter der Pfanne.</text>
      {logo(50, 84.5, 7, INK, "middle")}
    </g>'''
    return W, H, svg(W, H, inner)


# ---------------------------------------------------------------- 2 Flaschen-Reihe
def d2():
    W, H = 150, 100
    bw, bh, x0, y0 = 11.2, 28, 10, 60
    n = 9; pick = 6
    gap = (130 - n * bw) / (n - 1)
    bottles = []
    for i in range(n):
        x = x0 + i * (bw + gap)
        b, f, c = bottle_path(x, y0, bw, bh)
        if i == pick:
            bottles.append(f'<path d="{c}" fill="{INK}" fill-rule="evenodd"/><path d="{f}" fill="{INK}"/><path d="{b}" fill="{RED}"/>'
                           f'<image href="logo.png" x="{x + bw / 2 - 3.2}" y="{y0 + bh * .48}" width="6.4" height="6.4" '
                           f'style="filter:brightness(0) invert(1)"/>')
        else:
            st = f'fill="none" stroke="{INK}" stroke-width=".55" stroke-linejoin="round" opacity=".55"'
            bottles.append(f'<path d="{c}" {st} fill-rule="evenodd"/><path d="{f}" {st}/><path d="{b}" {st}/>')
    px = x0 + pick * (bw + gap) + bw / 2
    inner = f'''
    <rect width="{W}" height="{H}" fill="{CREAM}"/>
    {logo(10, 8, 8)}
    <text x="10" y="35" style="{ANTON};font-size:17px" fill="{INK}">FLASCHEN</text>
    <text x="10" y="52" style="{ANTON};font-size:17px" fill="{INK}">GIBT’S GENUG.</text>
    <text x="141" y="33" text-anchor="end" style="{FRA_IB};font-size:6.4px" fill="{RED}">Wir haben</text>
    <text x="141" y="40.5" text-anchor="end" style="{FRA_IB};font-size:6.4px" fill="{RED}">die richtige.</text>
    <path d="M128,44 C129,50 {px + 6},51 {px + 1.5},{y0 - 2.5}" fill="none" stroke="{RED}" stroke-width=".8" stroke-linecap="round"/>
    <path d="M{px - 1},{y0 - 5.5} L{px + 1.3},{y0 - 2} L{px + 4.6},{y0 - 4.2}" fill="none" stroke="{RED}" stroke-width=".8" stroke-linecap="round" stroke-linejoin="round"/>
    {''.join(bottles)}
    <rect x="0" y="{y0 + bh + .6}" width="{W}" height=".5" fill="{INK}" opacity=".25"/>'''
    return W, H, svg(W, H, inner)


# ---------------------------------------------------------------- 3 Flasche (Konturschnitt)
def d3():
    W, H = 84, 140
    m = 3  # weißer Konturrand
    bx, by, bw, bh = m + 1, m, W - 2 * m - 2, H - 2 * m
    b, f, c = bottle_path(bx, by, bw, bh)
    cx = W / 2
    inner = f'''
    <g fill="#ffffff" stroke="#ffffff" stroke-width="{2 * m}" stroke-linejoin="round">
      <path d="{c}"/><path d="{f}"/><path d="{b}"/>
    </g>
    <path d="{c}" fill="#34474F"/>
    <path d="{c}" fill="{INK}" fill-rule="evenodd"/>
    <path d="{f}" fill="{INK}"/>
    <path d="{b}" fill="{RED}"/>
    <path d="M{bx + bw * .1},{by + bh * .3} C{bx + bw * .1},{by + bh * .24} {bx + bw * .2},{by + bh * .22} {bx + bw * .3},{by + bh * .215}"
          fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="1.6" stroke-linecap="round"/>
    <rect x="{bx + 6}" y="{by + bh * .31}" width="{bw - 12}" height="13" rx="2.5" fill="{CREAM}"/>
    {logo(cx, by + bh * .31 + 2.6, 7.8, INK, "middle")}
    <text x="{cx}" y="{by + bh * .31 + 23}" text-anchor="middle" style="{FRA_I};font-size:5.6px" fill="{CREAM}">Flaschen gibt’s genug.</text>
    <text x="{cx}" y="{by + bh * .31 + 41}" text-anchor="middle" style="{ANTON};font-size:16px" fill="{CREAM}">WIR HABEN</text>
    <text x="{cx}" y="{by + bh * .31 + 58}" text-anchor="middle" style="{ANTON};font-size:16px" fill="{CREAM}">DIE</text>
    <text x="{cx}" y="{by + bh * .31 + 75}" text-anchor="middle" style="{ANTON};font-size:16px" fill="{INK}">RICHTIGE.</text>'''
    return W, H, svg(W, H, inner)


# ---------------------------------------------------------------- 4 Retro-Wohnmobil-Streifen
def d4():
    W, H = 150, 100
    stripes = []
    for i, col in enumerate((BRICK, RED, AMBER)):
        y = 76 + i * 7.2
        stripes.append(
            f'<path d="M-5,{y} L{104 + i * 5},{y} C{124 + i * 5},{y} {128 + i * 4},{y - 34} {160},{y - 60}" '
            f'fill="none" stroke="{col}" stroke-width="5.4"/>')
    inner = f'''
    <rect width="{W}" height="{H}" fill="{CREAM}"/>
    {''.join(stripes)}
    {logo(10, 8, 8)}
    <text x="10" y="27" style="{FRA_I};font-size:8px" fill="{INK}">Wir sind</text>
    <text x="10" y="44" style="{ANTON};font-size:17px" fill="{INK}">FEUER UND</text>
    <text x="10" y="61" style="{ANTON};font-size:17px" fill="{RED}">FLAMME.</text>
    <text x="69" y="53.5" style="{FRA_I};font-size:6.4px" fill="{INK}">Dein Wohnmobil</text>
    <text x="69" y="61" style="{FRA_IB};font-size:6.4px" fill="{INK}">nicht.</text>'''
    return W, H, svg(W, H, inner)


# ---------------------------------------------------------------- 5 Stempel "BERUFLICH."
def d5():
    W, H = 150, 100
    random.seed(7)
    specks = "".join(
        f'<circle cx="{random.uniform(0, 110):.2f}" cy="{random.uniform(0, 40):.2f}" r="{random.choice([.12, .18, .25, .35, .5])}" fill="#000"/>'
        for _ in range(900))
    scratches = "".join(
        f'<path d="M{(x:=random.uniform(0, 110)):.1f},{(y:=random.uniform(0, 40)):.1f} l{random.uniform(4, 14):.1f},{random.uniform(-1, 1):.1f}" stroke="#000" stroke-width="{random.choice([.15, .25])}"/>'
        for _ in range(14))
    defs = f'''<mask id="grunge" maskUnits="userSpaceOnUse" x="0" y="0" width="110" height="40">
      <rect width="110" height="40" fill="#fff"/>{specks}{scratches}</mask>'''
    sx, sy = 9, 0
    inner = f'''
    <rect width="{W}" height="{H}" fill="{INK}"/>
    {logo(10, 8, 8, CREAM)}
    <text x="10" y="37" style="{FRA};font-size:10.5px" fill="{CREAM}">Wir kennen uns</text>
    <text x="10" y="50" style="{FRA};font-size:10.5px" fill="{CREAM}">mit Flaschen aus.</text>
    <g transform="translate(14 60) rotate(-6 50 15)">
      <g mask="url(#grunge)">
        <rect x="1" y="1" width="100" height="30" rx="3" fill="none" stroke="{RED}" stroke-width="1.6"/>
        <rect x="3.6" y="3.6" width="94.8" height="24.8" rx="1.8" fill="none" stroke="{RED}" stroke-width=".6"/>
        <text x="51" y="23.6" text-anchor="middle" style="{ANTON};font-size:18.5px;letter-spacing:1px" fill="{RED}">BERUFLICH.</text>
      </g>
    </g>'''
    return W, H, svg(W, H, inner, defs)


def page(w, h, body, css="fonts/fonts.css", bg="transparent"):
    return f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{css}">
<style>@page{{size:{w}mm {h}mm;margin:0}}html,body{{margin:0;padding:0;background:{bg}}}svg{{display:block}}</style>
</head><body>{body}</body></html>'''


if __name__ == "__main__":
    out = os.path.dirname(os.path.abspath(__file__))
    for i, fn in enumerate((d1, d2, d3, d4, d5), 1):
        w, h, s = fn()
        open(f"{out}/s{i}.html", "w").write(page(w, h, s))
        open(f"{out}/s{i}.size", "w").write(f"{w} {h}")
