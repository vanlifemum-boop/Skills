#!/usr/bin/env python3
"""Erzeugt aus tage.py je Tag ein HyperFrames-Projekt (1080x1920, 75 s).

Aufbau jeder Folge (Konzept A: "Der Gegenstand bleibt, die Zeit wechselt"):
  heute   0-24 s  Kind, warme Gegenwart, ein Gegenstand
  wandel 24-32 s  Farbe weicht, Jahreszahlen rollen zurück, der Gegenstand vervielfacht sich
  damals 32-52 s  Archiv: Akte mit Schreibmaschinentext, Reihen gleicher Gegenstände
  recht  52-67 s  Farbe kehrt zurück, das Recht als Antwort
  ende   67-75 s  letzter Satz des Kindes, Türchen schließt sich

Aufruf: python3 build.py <zielordner> [tag ...]
"""
import html, json, os, shutil, sys
from string import Template

sys.path.insert(0, os.path.dirname(__file__))
from tage import TAGE
from objekte import OBJEKTE

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
SCENES = [("heute", 0, 24), ("wandel", 24, 8), ("damals", 32, 20), ("recht", 52, 15), ("ende", 67, 8)]
TOTAL = 75

# Farben
WALL, FLOOR, INK, WOOD = "#C9A388", "#7A5644", "#2B1D17", "#A87650"
HALL_WALL, HALL_FLOOR, GREY_OBJ = "#B5B0A6", "#8D887E", "#8F8B83"
PAPER, TYPE_INK, RED, CREAM = "#E6DFCC", "#2E2A25", "#9E2B22", "#F3E6D3"

# Gegenstand: Mittelpunkt unten (Füße) und Maßstab, in allen Szenen gleich
OBJ_X, OBJ_Y = 540, 1560


def esc(s):
    return html.escape(s, quote=False)


def words(text, cls="w"):
    return " ".join(f'<span class="{cls}">{esc(w)}</span>' for w in text.split())


def chars(text):
    out = []
    for w in text.split():
        out.append('<span class="wd">' + "".join(f'<span class="c">{esc(c)}</span>' for c in w) + "</span>")
    return " ".join(out)


def read_time(text):
    return 0.5 + 0.3 * len(text.split())


# ---------------------------------------------------------------- Welten (SVG)

def snow(prefix, x0, y0, w, h, dur, seed):
    """Deterministischer Schnee im Fenster: Flocken als Kreise, Tweens mit endlicher Wiederholung."""
    import random
    r = random.Random(seed)
    flakes, js = [], []
    for i in range(26):
        fx = x0 + r.uniform(8, w - 8)
        rad = r.uniform(2.5, 5.5)
        fall = r.uniform(6.5, 10.5)
        off = r.uniform(0, fall)
        fid = f"{prefix}-fl{i}"
        flakes.append(f'<circle id="{fid}" cx="{fx:.1f}" cy="{y0 - 10}" r="{rad:.1f}" fill="#F4F1EA" opacity="0.85"/>')
        reps = int((dur + off) / fall) + 1
        js.append(
            f'tl.fromTo("#{fid}",{{y:0,x:0}},{{y:{h + 20},x:{r.uniform(-18, 18):.1f},duration:{fall:.2f},'
            f'ease:"none",repeat:{reps}}},{-off:.2f});'
        )
    return "\n".join(flakes), "\n".join(js)


def present_world(prefix, dur, seed):
    """Warme Küche am Abend: Wand, Boden, Fenster mit Schnee, Tischkante, Kerze, Lichtkegel."""
    flakes, snow_js = snow(prefix, 150, 820, 300, 330, dur, seed)
    svg = f"""
<svg class="world" viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" data-layout-ignore>
  <defs>
    <radialGradient id="{prefix}-pool" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#F6D7A8" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#F6D7A8" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="{prefix}-win"><rect x="150" y="820" width="300" height="330" rx="6"/></clipPath>
  </defs>
  <rect width="{W}" height="{H}" fill="{WALL}"/>
  <rect y="1480" width="{W}" height="{H - 1480}" fill="{FLOOR}"/>
  <rect y="1474" width="{W}" height="12" fill="#5E4235"/>
  <g>
    <rect x="150" y="820" width="300" height="330" rx="6" fill="#2F3B57"/>
    <g clip-path="url(#{prefix}-win)">{flakes}</g>
    <rect x="150" y="820" width="300" height="330" rx="6" fill="none" stroke="{INK}" stroke-width="10"/>
    <line x1="300" y1="820" x2="300" y2="1150" stroke="{INK}" stroke-width="8"/>
    <line x1="150" y1="985" x2="450" y2="985" stroke="{INK}" stroke-width="8"/>
    <rect x="130" y="1150" width="340" height="16" rx="4" fill="#E9DCC9" stroke="{INK}" stroke-width="5"/>
  </g>
  <g>
    <rect x="770" y="1130" width="330" height="26" fill="#8A5A3C" stroke="{INK}" stroke-width="5"/>
    <path d="M770 1156 H1100 V1300 Q1020 1290 950 1310 Q860 1292 770 1306 Z" fill="#E9DCC9" stroke="{INK}" stroke-width="5"/>
    <rect x="800" y="1306" width="22" height="174" fill="#7A4E33" stroke="{INK}" stroke-width="5"/>
    <rect id="{prefix}-candle" x="902" y="1040" width="34" height="90" rx="4" fill="#F1E8D8" stroke="{INK}" stroke-width="5"/>
    <line x1="919" y1="1040" x2="919" y2="1024" stroke="{INK}" stroke-width="4"/>
    <ellipse id="{prefix}-flame" cx="919" cy="1008" rx="11" ry="20" fill="#F2B54A" stroke="#C9772B" stroke-width="3"/>
  </g>
  <ellipse id="{prefix}-pool" cx="{OBJ_X}" cy="1560" rx="420" ry="120" fill="url(#{prefix}-pool)"/>
</svg>"""
    flame_js = (f'tl.fromTo("#{prefix}-flame",{{scaleY:1,transformOrigin:"50% 100%"}},'
                f'{{scaleY:1.12,duration:0.9,ease:"sine.inOut",yoyo:true,repeat:{int(dur / 0.9)}}},0);')
    return svg, snow_js + "\n" + flame_js


def hall_world(prefix, obj, rows=True, sec=0):
    """Anstaltssaal: gekachelte graue Wand, Reihen gleicher Gegenstände (ohne den Helden)."""
    tiles = []
    for y in range(0, 1480, 80):
        tiles.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#A39E94" stroke-width="2"/>')
    for x in range(0, W + 1, 80):
        tiles.append(f'<line x1="{x}" y1="0" x2="{x}" y2="1480" stroke="#A39E94" stroke-width="2"/>')
    copies = []
    if rows:
        k = 0
        # hintere Reihe, mittlere Reihe, vordere Reihe (seitlich vom Helden)
        for (scale, base_y, xs) in [
            (0.42, 1335, [90, 250, 410, 570, 730, 890, 1050]),
            (0.62, 1420, [20, 250, 830, 1060]),
            (1.0, OBJ_Y, [40, 1040]),
        ]:
            for x in xs:
                copies.append(
                    f'<g id="{prefix}-c{k}" class="{prefix}-copy" transform="translate({x},{base_y}) scale({scale})">'
                    f'<use href="#{prefix}-obj"/></g>'
                )
                k += 1
    return f"""
<svg class="world" viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" data-layout-ignore>
  <defs><g id="{prefix}-obj">{obj['svg'](GREY_OBJ, '#4A4640')}</g></defs>
  <rect width="{W}" height="{H}" fill="{HALL_WALL}"/>
  {''.join(tiles)}
  <rect y="1480" width="{W}" height="{H - 1480}" fill="{HALL_FLOOR}"/>
  <rect y="1474" width="{W}" height="12" fill="#6E6A62"/>
  <g transform="translate(965,912)">
    <circle r="46" fill="#ECE7DC" stroke="#3E3A34" stroke-width="7"/>
    {''.join(f'<line x1="0" y1="-38" x2="0" y2="-31" stroke="#3E3A34" stroke-width="4" transform="rotate({a})"/>' for a in range(0, 360, 30))}
    <line x1="0" y1="0" x2="0" y2="-24" stroke="#3E3A34" stroke-width="6" stroke-linecap="round" transform="rotate(300)"/>
    <line x1="0" y1="0" x2="0" y2="-33" stroke="#3E3A34" stroke-width="4" stroke-linecap="round" transform="rotate(60)"/>
    <g id="{prefix}-sec" transform="rotate({sec})"><line x1="0" y1="6" x2="0" y2="-36" stroke="#8E2A22" stroke-width="2.5"/></g>
    <circle r="4" fill="#3E3A34"/>
  </g>
  {''.join(copies)}
</svg>"""


def hero(prefix, obj, fill):
    """Der Gegenstand des Tages, Füße bei (OBJ_X, OBJ_Y)."""
    return f"""
<svg class="world" viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" data-layout-ignore>
  <g id="{prefix}-heroPos" transform="translate({OBJ_X},{OBJ_Y})">
    <g id="{prefix}-hero">{obj['svg'](fill, INK, cls=prefix + '-fill')}</g>
  </g>
</svg>"""


GRAIN = """<svg class="world grain" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-ignore>
<filter id="GID"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4"/>
<feColorMatrix values="0 0 0 0 0.2  0 0 0 0 0.18  0 0 0 0 0.15  0 0 0 0.55 0"/></filter>
<rect width="1080" height="1920" filter="url(#GID)"/></svg>"""


# ---------------------------------------------------------------- Szenen-Gerüst

HELPERS = """
function blurWords(sel,t,gap){tl.fromTo(sel+" .w",{opacity:0,filter:"blur(7px)"},{opacity:1,filter:"blur(0px)",duration:0.55,ease:"power2.out",stagger:gap||0.11},t);}
function greyWords(sel,t,gap){tl.fromTo(sel+" .w",{opacity:0.16},{opacity:1,duration:0.45,ease:"none",stagger:gap||0.12},t);}
function lineIn(sel,t){tl.fromTo(sel,{opacity:0,filter:"blur(9px)"},{opacity:1,filter:"blur(0px)",duration:0.7,ease:"power3.out"},t);}
function typeIn(sel,t,gap){tl.fromTo(sel+" .c",{opacity:0},{opacity:1,duration:0.01,ease:"none",stagger:gap||0.028},t);}
function stampWords(sel,t,gap){var ws=document.querySelectorAll(sel+" .w");ws.forEach(function(w,i){var at=t+i*(gap||0.38);tl.fromTo(w,{opacity:0,scale:1.35},{opacity:1,scale:1,duration:0.12,ease:"power4.out"},at);});}
function outLine(sel,t){tl.to(sel,{opacity:0,filter:"blur(7px)",duration:0.3,ease:"power2.in"},t);}
"""

SCENE_T = Template("""<template>
  <style>
    #root { position:absolute; inset:0; overflow:hidden; background:$bg; }
    #root .world { position:absolute; left:0; top:0; width:1080px; height:1920px; }
    #root .grain { opacity:0.10; mix-blend-mode:multiply; }
    #root .line { position:absolute; left:120px; top:330px; width:768px; color:$ink;
                  font-family:"Nunito",sans-serif; font-weight:800; font-size:60px; line-height:1.2; letter-spacing:-0.01em; }
    #root .line .w { display:inline-block; }
    #root .src { position:absolute; left:120px; width:768px; font-family:"Inter",sans-serif; font-weight:400;
                 font-size:28px; line-height:1.3; color:$srcInk; }
$css
  </style>
  <div id="root" data-composition-id="$id" data-width="1080" data-height="1920">
$body
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
$helpers
$js
    window.__timelines["$id"] = tl;
  </script>
</template>
""")


def scene_file(sid, body, js, css="", bg=WALL, ink=INK, src_ink="#4A372D"):
    return SCENE_T.substitute(id=sid, body=body, js=js, css=css, bg=bg, ink=ink, srcInk=src_ink, helpers=HELPERS)


def line_clip(lid, text, start, end, style="blur", cls="line", track=2, extra=""):
    inner = chars(text) if style == "type" else words(text)
    return (f'<div id="{lid}" class="clip {cls}" data-start="{start:.2f}" data-duration="{end - start + 0.35:.2f}" '
            f'data-track-index="{track}" data-hold{extra}>{inner}</div>')


def anim_in(lid, style, t):
    sel = "#" + lid
    return {"blur": f'blurWords("{sel}",{t:.2f});', "grey": f'greyWords("{sel}",{t:.2f});',
            "line": f'lineIn("{sel}",{t:.2f});', "type": f'typeIn("{sel}",{t:.2f});',
            "stamp": f'stampWords("{sel}",{t:.2f});', "none": ""}[style]


def sequence(prefix, lines, t0, t_end, styles, gap=0.45, cls="line", hold_min=None):
    """Verteilt Zeilen nacheinander; jede Zeile bekommt Lesezeit, die letzte bis t_end."""
    body, js, marks = [], [], []
    t = t0
    for i, text in enumerate(lines):
        style = styles[i % len(styles)]
        intro = {"type": len(text) * 0.028, "stamp": len(text.split()) * 0.38}.get(style, len(text.split()) * 0.11)
        hold = max(read_time(text), hold_min or 0) + intro
        end = t_end if i == len(lines) - 1 else t + hold + 0.6
        lid = f"{prefix}-l{i}"
        body.append(line_clip(lid, text, t, end, style if style != "none" else "blur", cls=cls))
        js.append(anim_in(lid, style, t))
        js.append(f'outLine("#{lid}",{end - 0.3:.2f});')
        marks.append((t, end))
        t = end + gap
    if t - gap > t_end + 0.01:
        raise ValueError(f"{prefix}: Zeilen passen nicht ({t - gap:.1f}s > {t_end}s): {lines}")
    return "\n".join(body), "\n".join(js), marks


# ---------------------------------------------------------------- die fünf Szenen

def s_heute(d, obj):
    p = "he"
    world, wjs = present_world(p, 24, d["tag"])
    lines = d["kind"]
    styles = ["none", "blur", "line", "grey", "blur", "grey"]
    body_l, js_l, marks = sequence(p, lines, 0.0, 23.6, styles)
    # Erste Zeile steht schon im ersten Bild (Vorschaubild)
    js = [wjs, js_l]
    # leiser werdender Lichtkegel bei der vorletzten Zeile, langsamer Blick auf den Gegenstand bei der letzten
    t_dim = marks[-2][0]
    js.append(f'tl.to("#{p}-pool",{{opacity:0.25,duration:3,ease:"power2.inOut"}},{t_dim:.2f});')
    js.append(f'tl.fromTo("#{p}-hero",{{scale:1}},{{scale:1.05,duration:{23.9 - marks[-1][0]:.2f},ease:"power2.inOut",transformOrigin:"50% 100%"}},{marks[-1][0]:.2f});')
    js.append(obj.get("heute_js", "")(p, marks) if callable(obj.get("heute_js")) else "")
    body = world + hero(p, obj, WOOD) + body_l
    return scene_file("heute", body, "\n".join(js))


def s_wandel(d, obj):
    p = "wa"
    world, wjs = present_world(p, 8, d["tag"] + 100)
    hall = hall_world(p, obj)
    years = d.get("jahre", ["2026", "1990", "1945", "1933", "1922"]) + [d["epoche"]]
    roll = "".join(f'<div class="yr{" last" if i == len(years) - 1 else ""}">{esc(y)}</div>' for i, y in enumerate(years))
    n = len(years) - 1
    css = f"""
    #root #wa-hallWrap {{ position:absolute; inset:0; }}
    #root #wa-yrWin {{ position:absolute; left:120px; top:330px; width:768px; height:300px; overflow:hidden; }}
    #root #wa-yrStrip .yr {{ height:300px; display:flex; align-items:center; justify-content:center;
      font-family:"League Gothic",sans-serif; font-size:280px; line-height:1; color:{INK}; }}
    #root #wa-yrStrip .yr.last {{ font-size:{d.get('epoche_size', 150)}px; letter-spacing:0.02em; }}
    #root #wa-sub {{ top:650px; text-align:center; font-family:"Inter",sans-serif; font-weight:700; font-size:40px; }}"""
    body = (world + f'<div id="wa-hallWrap">{hall}</div>' + hero(p, obj, WOOD) +
            f'<div id="wa-yr" class="clip" data-start="0.2" data-duration="7.5" data-track-index="2" '
            f'data-layout-allow-overflow><div id="wa-yrWin"><div id="wa-yrStrip">{roll}</div></div></div>' +
            line_clip("wa-sub", d["epoche_zeile"], 4.4, 7.4, cls="line", track=3))
    js = [wjs,
          'tl.fromTo("#wa-hallWrap",{opacity:0},{opacity:1,duration:2.2,ease:"power2.inOut"},0.3);',
          f'tl.fromTo(".wa-fill",{{fill:"{WOOD}"}},{{fill:"{GREY_OBJ}",duration:2.0,ease:"power2.inOut"}},0.6);',
          'tl.set(".wa-copy",{opacity:0},0);',
          f'tl.fromTo("#wa-yrStrip",{{y:0}},{{y:{-300 * n},duration:3.6,ease:"power3.inOut"}},0.4);',
          'tl.fromTo("#wa-yrStrip",{filter:"blur(0px)"},{filter:"blur(5px)",duration:1.4,ease:"power2.in",yoyo:true,repeat:1},0.8);',
          'outLine("#wa-yr .yr.last",7.3);',
          anim_in("wa-sub", "line", 4.4), 'outLine("#wa-sub",7.3);']
    # Kopien erscheinen hart nacheinander: Ordnung
    order = [11, 12, 7, 8, 9, 10, 3, 2, 4, 1, 5, 0, 6]
    for i, k in enumerate(order):
        js.append(f'tl.set("#wa-c{k}",{{opacity:1}},{2.5 + i * 0.26:.2f});')
    return scene_file("wandel", body, "\n".join(js), css=css)


def s_damals(d, obj):
    p = "da"
    hall = hall_world(p, obj)
    ticks = "".join(f'tl.set("#da-sec",{{rotation:{(i+1)*6}, svgOrigin:"0 0"}},{i+1});' for i in range(19))
    css = f"""
    #root #da-card {{ position:absolute; left:96px; top:330px; width:888px; height:550px; background:{PAPER};
      border:3px solid #9C9483; box-shadow:0 10px 0 rgba(60,55,48,0.25); }}
    #root #da-tab {{ position:absolute; left:40px; top:-44px; padding:6px 22px; background:{PAPER}; border:3px solid #9C9483;
      border-bottom:none; font-family:"IBM Plex Mono",monospace; font-size:28px; color:#5A544A; }}
    #root .akte {{ left:150px; top:395px; width:780px; color:{TYPE_INK}; font-family:"IBM Plex Mono",monospace;
      font-weight:500; font-size:44px; line-height:1.28; letter-spacing:-0.01em; }}
    #root .akte .wd {{ display:inline-block; }}
    #root .akte.stamp {{ font-family:"Inter",sans-serif; font-weight:900; font-size:54px; text-transform:uppercase; color:#6E2A22; }}
    #root .akte.stamp .w {{ display:inline-block; border:4px solid #6E2A22; padding:2px 12px; margin:6px 6px 0 0; transform:rotate(-2deg); }}
    #root #da-dim {{ position:absolute; inset:0; background:#2A2622; opacity:0; }}"""
    lines = d["damals"]
    styles = d.get("damals_stile", ["type", "stamp", "type", "grey"])
    body_l, js_l, marks = sequence(p, lines, 0.9, 19.6, styles, cls="line akte", hold_min=2.6)
    for i, s in enumerate(styles[:len(lines)]):
        if s == "stamp":
            body_l = body_l.replace(f'id="{p}-l{i}" class="clip line akte"', f'id="{p}-l{i}" class="clip line akte stamp"')
    src = f'<div id="da-src" class="src" style="top:820px;left:150px;width:620px;color:#5A544A">Quelle: {esc(d["damals_quelle"])}</div>'
    body = (hall + hero(p, obj, GREY_OBJ) + '<div id="da-dim"></div>' +
            f'<div id="da-cardWrap" class="clip" data-start="0" data-duration="20" data-track-index="1">'
            f'<div id="da-card"><div id="da-tab">AKTE</div></div>{src}</div>' + body_l + GRAIN.replace("GID", "da-grain"))
    js = [js_l, ticks,
          'tl.fromTo("#da-card",{y:-60,rotation:-3,opacity:0},{y:0,rotation:-1,opacity:1,duration:0.8,ease:"power3.out"},0.0);',
          'tl.fromTo("#da-src",{opacity:0},{opacity:1,duration:0.5},0.6);',
          'tl.to("#da-cardWrap",{opacity:0,duration:0.3,ease:"power2.in"},19.65);']
    # der Gegenstand passt nicht in die Reihe ... und wird zurechtgerückt
    ta, tb = marks[2][0] + 0.3, marks[2][1] - 1.4
    js.append(f'tl.fromTo("#da-hero",{{rotation:0,x:0}},{{rotation:7,x:26,duration:0.9,ease:"power2.out",transformOrigin:"50% 100%"}},{ta:.2f});')
    js.append(f'tl.to("#da-hero",{{rotation:0,x:0,duration:0.22,ease:"power4.in"}},{tb:.2f});')
    js.append(f'tl.to("#da-dim",{{opacity:0.28,duration:2.8,ease:"power2.inOut"}},{marks[-1][0]:.2f});')
    return scene_file("damals", body, "\n".join(js), css=css, bg=HALL_WALL, ink=TYPE_INK)


def s_recht(d, obj):
    p = "re"
    world, wjs = present_world(p, 15, d["tag"] + 200)
    hall = hall_world(p, obj, sec=114)
    css = f"""
    #root #re-hallWrap, #root #re-dim {{ position:absolute; inset:0; }}
    #root #re-dim {{ background:#2A2622; }}
    #root #re-para {{ position:absolute; left:120px; top:320px; width:768px; font-family:"Inter",sans-serif; font-weight:900;
      font-size:{d.get('para_size', 96)}px; line-height:1; letter-spacing:-0.02em; color:{RED}; }}
    #root .sub {{ top:{330 + d.get('para_size', 96) + 50}px; font-family:"Inter",sans-serif; font-weight:700; font-size:48px; line-height:1.22; }}"""
    first = d["recht_titel"]
    subs = d["recht"]
    t_para = 2.6 + max(read_time(first), 3.0) + len(first.split()) * 0.11 + 0.6 + 0.4
    b1 = line_clip("re-t", first, 2.6, t_para - 0.4)
    j1 = [anim_in("re-t", "blur", 2.6), f'outLine("#re-t",{t_para - 0.7:.2f});']
    body_s, js_s, marks = sequence(p, subs, t_para + 0.4, 14.6, ["line", "grey"], cls="line sub")
    para = (f'<div id="re-paraClip" class="clip" data-start="{t_para:.2f}" data-duration="{15 - t_para:.2f}" data-track-index="3">'
            f'<div id="re-para">{esc(d["paragraph"])}</div>'
            f'<div id="re-src" class="src" style="top:752px;width:640px">Quelle: {esc(d["recht_quelle"])}</div></div>')
    prop = obj["prop"](p) if obj.get("prop") else ""
    body = world + f'<div id="re-hallWrap">{hall}<div id="re-dim"></div></div>' + hero(p, obj, GREY_OBJ) + prop + b1 + para + body_s
    js = [wjs,
          'tl.fromTo("#re-dim",{opacity:0.28},{opacity:0,duration:1.2,ease:"power2.out"},0);',
          'tl.fromTo("#re-hallWrap",{opacity:1},{opacity:0,duration:2.2,ease:"power2.inOut"},0.4);',
          'tl.fromTo("#re-hallWrap svg",{filter:"blur(0px)"},{filter:"blur(14px)",duration:2.2,ease:"power2.in"},0.4);',
          f'tl.fromTo(".re-fill",{{fill:"{GREY_OBJ}"}},{{fill:"{WOOD}",duration:1.8,ease:"power2.inOut"}},0.5);',
          'tl.fromTo("#re-pool",{opacity:0},{opacity:1,duration:2.0,ease:"power2.inOut"},0.8);',
          "\n".join(j1),
          f'tl.fromTo("#re-para",{{opacity:0,scale:1.12,transformOrigin:"0% 50%"}},{{opacity:1,scale:1,duration:0.5,ease:"expo.out"}},{t_para:.2f});',
          f'tl.fromTo("#re-src",{{opacity:0}},{{opacity:1,duration:0.5}},{t_para + 0.6:.2f});',
          'tl.to("#re-paraClip",{opacity:0,duration:0.3,ease:"power2.in"},14.6);',
          js_s]
    if obj.get("prop_js"):
        js.append(obj["prop_js"](p))
    return scene_file("recht", body, "\n".join(js), css=css)


def s_ende(d, obj):
    p = "en"
    world, wjs = present_world(p, 8, d["tag"] + 300)
    prop = obj["prop"](p) if obj.get("prop") else ""
    css = f"""
    #root .door {{ position:absolute; top:0; width:540px; height:1920px; background:#7E2620; }}
    #root .door .inset {{ position:absolute; left:50px; right:50px; top:120px; bottom:120px; border:6px solid #5E1B16; }}
    #root .door .inset2 {{ position:absolute; left:80px; right:80px; top:150px; bottom:150px; border:3px solid #C99A6B; opacity:0.6; }}
    #root #en-doorL {{ left:0; }} #root #en-doorR {{ left:540px; }}
    #root #en-doorL {{ box-shadow: inset -6px 0 0 #5E1B16; }}
    #root #en-num {{ position:absolute; left:0; width:1080px; top:360px; text-align:center; font-family:"League Gothic",sans-serif;
      font-size:420px; line-height:1; color:{CREAM}; }}
    #root #en-name {{ position:absolute; left:120px; width:840px; top:830px; text-align:center; font-family:"Inter",sans-serif;
      font-weight:900; font-size:64px; line-height:1.1; color:{CREAM}; }}
    #root #en-rest {{ position:absolute; left:120px; width:840px; top:930px; text-align:center; font-family:"Inter",sans-serif;
      font-weight:400; font-size:38px; line-height:1.3; color:#E8C9A8; }}"""
    last = d["kind_schluss"]
    b = line_clip("en-l", last, 0.3, 3.9)
    rest = "Noch 1 Tag bis Weihnachten" if d["tag"] == 23 else ("Frohe Weihnachten" if d["tag"] == 24 else f"Noch {24 - d['tag']} Tage bis Weihnachten")
    card = (f'<div id="en-card" class="clip" data-start="4.0" data-duration="4" data-track-index="3">'
            f'<div id="en-doorL" class="door"><div class="inset"></div><div class="inset2"></div></div>'
            f'<div id="en-doorR" class="door"><div class="inset"></div><div class="inset2"></div></div>'
            f'<div id="en-num">{d["tag"]}</div><div id="en-name">Systemfehler Familie</div>'
            f'<div id="en-rest">Adventskalender 2026<br>{esc(rest)}</div></div>')
    body = world + hero(p, obj, WOOD) + prop + b + card
    js = [wjs, anim_in("en-l", "grey", 0.3), 'outLine("#en-l",3.6);',
          'tl.fromTo("#en-doorL",{x:-560},{x:0,duration:0.7,ease:"power3.inOut"},4.0);',
          'tl.fromTo("#en-doorR",{x:560},{x:0,duration:0.7,ease:"power3.inOut"},4.0);',
          'tl.fromTo("#en-num",{opacity:0,scale:1.25},{opacity:1,scale:1,duration:0.45,ease:"expo.out"},4.75);',
          'tl.fromTo("#en-name",{opacity:0,filter:"blur(8px)"},{opacity:1,filter:"blur(0px)",duration:0.5,ease:"power3.out"},5.2);',
          'tl.fromTo("#en-rest",{opacity:0},{opacity:1,duration:0.5,ease:"power2.out"},5.6);']
    if obj.get("prop_js_static"):
        js.append(obj["prop_js_static"](p))
    return scene_file("ende", body, "\n".join(js), css=css)


# ---------------------------------------------------------------- Projekt

INDEX_T = Template("""<!doctype html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Systemfehler Familie · Tag $tag</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * { margin:0; padding:0; box-sizing:border-box; }
      html, body { margin:0; width:1080px; height:1920px; overflow:hidden; background:$wall; }
      #root { width:100%; height:100%; position:relative; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="$total" data-width="1080" data-height="1920">
$hosts
      <audio id="melodie" class="clip" src="assets/melodie.mp3" data-start="0" data-duration="$total" data-track-index="5" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
""")


def build(day, dest):
    d = TAGE[day]
    obj = OBJEKTE[d["objekt"]]
    proj = os.path.join(dest, f"tag-{day:02d}")
    os.makedirs(os.path.join(proj, "compositions"), exist_ok=True)
    os.makedirs(os.path.join(proj, "assets"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "melodie.mp3"), os.path.join(proj, "assets", "melodie.mp3"))
    makers = {"heute": s_heute, "wandel": s_wandel, "damals": s_damals, "recht": s_recht, "ende": s_ende}
    hosts = []
    for sid, start, dur in SCENES:
        with open(os.path.join(proj, "compositions", f"{sid}.html"), "w") as f:
            f.write(makers[sid](d, obj))
        hosts.append(f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{start}" data-duration="{dur}" data-track-index="1" data-track-kind="graphics" '
                     f'data-width="1080" data-height="1920"></div>')
    with open(os.path.join(proj, "index.html"), "w") as f:
        f.write(INDEX_T.substitute(tag=day, total=TOTAL, hosts="\n".join(hosts), wall=WALL))
    for name in ("package.json", "hyperframes.json", "meta.json"):
        src = os.path.join(dest, "tag-01", name)
        tgt = os.path.join(proj, name)
        if os.path.exists(src) and not os.path.exists(tgt):
            txt = open(src).read().replace("tag-01", f"tag-{day:02d}")
            open(tgt, "w").write(txt)
    print("gebaut:", proj)


if __name__ == "__main__":
    dest = sys.argv[1]
    days = [int(x) for x in sys.argv[2:]] or sorted(TAGE)
    for day in days:
        build(day, dest)
