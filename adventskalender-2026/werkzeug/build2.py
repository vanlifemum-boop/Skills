#!/usr/bin/env python3
"""Stil 2 "Bilderbuch-Film": die Avatar-Kinder spielen die Geschichte in gemalten Räumen.

Szenen je Folge (75 s, 1080x1920):
  flur     0-16  Kind heute in der Wohngruppe, andere Kinder am Weihnachtsbaum
  zuhause 16-28  Familientisch, Geschwister sitzen, ein Stuhl bleibt leer
  wandel  28-34  dasselbe Kind wechselt die Zeit: Weihnachtspulli -> Kleidung von damals, Sepia
  damals  34-53  Anstalt: Kinder in Reihen, Schatten eines Erwachsenen, Akte und Stempel
  recht   53-68  Gesprächsraum heute, Kinderzeichnung, das Recht
  ende    68-75  letzter Satz, Türchen schließt sich

Aufruf: python3 build2.py <zielordner> [tag ...]
"""
import html, os, shutil, sys
from string import Template

sys.path.insert(0, os.path.dirname(__file__))
from build import HELPERS, read_time, words, chars, esc  # gemeinsame Textbausteine
from tage2 import TAGE

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
K = 1.875                     # Faktor Originalbild (1024 hoch) -> Bühnenbild (1920 hoch)
SCENES = [("flur", 0, 16), ("zuhause", 16, 12), ("wandel", 28, 6), ("damals", 34, 19), ("recht", 53, 15), ("ende", 68, 7)]
TOTAL = 75
EMO = ["froehlich", "traurig", "weinend", "wuetend", "ueberrascht", "nachdenklich", "aengstlich", "hoffnungsvoll"]
CREAM, RED = "#FFF6EA", "#C8352A"
USED = set()                  # Bilddateien, die ins Projekt kopiert werden


def img(kind, name):
    USED.add((kind, name))
    return f"assets/{kind}/{name}"


# ------------------------------------------------------------------ Bausteine

def kid(kid_id, char, look, poses, cx, bottom, h, clip=None, first=None, extra_style=""):
    """Ein Kind mit mehreren Posen übereinander; sichtbar ist zuerst `first` (oder die erste).
    clip: Anteil der Höhe, der sichtbar bleibt (Kind sitzt hinter einem Tisch)."""
    first = first or poses[0]
    w = h * 0.8
    vis_h = h * clip if clip else h
    layers = []
    for p in poses:
        src = img("kinder", f"k{char:02d}_{look}_{p}.png")
        op = 1 if p == first else 0
        layers.append(f'<div id="{kid_id}-{p}" class="pose" style="opacity:{op}"><img src="{src}" alt=""/></div>')
    return (f'<div id="{kid_id}" class="kidbox" style="left:{cx - w / 2:.0f}px;top:{bottom - vis_h:.0f}px;width:{w:.0f}px;'
            f'height:{vis_h:.0f}px;{extra_style}" data-layout-ignore>'
            f'<div id="{kid_id}-body" class="kidbody" style="height:{h:.0f}px">{"".join(layers)}</div></div>')


def swap(kid_id, frm, to, t):
    return (f'tl.to("#{kid_id}-{frm}",{{opacity:0,duration:0.22,ease:"power1.in"}},{t:.2f});'
            f'tl.fromTo("#{kid_id}-{to}",{{opacity:0,scale:0.965}},{{opacity:1,scale:1,duration:0.32,ease:"power2.out",transformOrigin:"50% 100%",immediateRender:false}},{t:.2f});')


def breathe(kid_id, dur, period=1.7, amt=0.012, delay=0.0):
    reps = max(1, int(dur / period))
    return (f'tl.fromTo("#{kid_id}-body",{{scaleY:1}},{{scaleY:{1 + amt},transformOrigin:"50% 100%",duration:{period / 2:.2f},'
            f'ease:"sine.inOut",yoyo:true,repeat:{reps * 2 - 1}}},{delay:.2f});')


def text_lines(prefix, lines, cls="line"):
    """lines: [(text, start, end, style)] -> HTML + JS"""
    body, js = [], []
    for i, (text, s, e, style) in enumerate(lines):
        lid = f"{prefix}-l{i}"
        inner = chars(text) if style == "type" else words(text)
        body.append(f'<div id="{lid}" class="clip {cls}" data-start="{s:.2f}" data-duration="{e - s + 0.35:.2f}" '
                    f'data-track-index="2" data-hold>{inner}</div>')
        js.append({"blur": f'blurWords("#{lid}",{s:.2f});', "grey": f'greyWords("#{lid}",{s:.2f});',
                   "line": f'lineIn("#{lid}",{s:.2f});', "type": f'typeIn("#{lid}",{s:.2f});',
                   "stamp": f'stampWords("#{lid}",{s:.2f});', "none": ""}[style])
        js.append(f'outLine("#{lid}",{e - 0.3:.2f});')
    return "\n".join(body), "\n".join(js)


def cam(tl_id, steps):
    """steps: [(t, dur, x, y, s, ease)] Kamera über dem Bühnenbild (Ursprung oben links)."""
    js = []
    for i, (t, d, x, y, s, ease) in enumerate(steps):
        if i == 0:
            js.append(f'tl.set("#{tl_id}",{{x:{x},y:{y},scale:{s},transformOrigin:"0 0"}},0);')
        else:
            js.append(f'tl.to("#{tl_id}",{{x:{x},y:{y},scale:{s},duration:{d},ease:"{ease}"}},{t:.2f});')
    return "\n".join(js)


BASE_CSS = f"""
    #root {{ position:absolute; inset:0; overflow:hidden; background:#1b1512; }}
    #root .stage {{ position:absolute; left:0; top:0; width:2880px; height:1920px; }}
    #root .stage > img.bg {{ position:absolute; left:0; top:0; width:2880px; height:1920px; }}
    #root .kidbox {{ position:absolute; overflow:hidden; }}
    #root .kidbody {{ position:absolute; left:0; right:0; top:0; }}
    #root .pose {{ position:absolute; inset:0; }}
    #root .pose img {{ position:absolute; bottom:0; left:50%; height:100%; width:auto; transform:translateX(-50%); }}
    #root .scrim {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(14,10,9,0.78) 0%, rgba(14,10,9,0.55) 30%, rgba(14,10,9,0) 48%); }}
    #root .line {{ position:absolute; left:124px; top:330px; width:800px; color:{CREAM}; font-family:"Nunito",sans-serif;
                  font-weight:900; font-size:64px; line-height:1.16; letter-spacing:-0.01em; text-shadow:0 3px 18px rgba(0,0,0,0.45); }}
    #root .line .w, #root .line .wd {{ display:inline-block; }}
    #root .src {{ position:absolute; left:124px; width:660px; font-family:"Inter",sans-serif; font-size:28px; line-height:1.3;
                 color:rgba(255,246,234,0.82); }}"""

SCENE_T = Template("""<template>
  <style>
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


def scene(sid, body, js, css=""):
    return SCENE_T.substitute(id=sid, css=BASE_CSS + css, body=body, js="\n".join(js) if isinstance(js, list) else js, helpers=HELPERS)


# ------------------------------------------------------------------ Szenen

def s_flur(d):
    p, c = "fl", d["kind_nr"]
    others = d["flur_kinder"]
    world = [f'<img class="bg" src="{img("raeume", "flur.jpg")}" alt=""/>']
    # andere Kinder klein am Baum (Weltkoordinaten des Originalbilds * K)
    spots = [(865, 574, 122), (1052, 576, 122), (948, 598, 138)]
    js = []
    for i, (ch, (x, y, h)) in enumerate(zip(others, spots)):
        kid_id = f"{p}-o{i}"
        world.append(kid(kid_id, ch, "heute", ["froehlich", "hoffnungsvoll", "ueberrascht"], x * K, y * K, h * K))
        js.append(breathe(kid_id, 16, 1.3 + i * 0.2, 0.02, i * 0.3))
        js.append(swap(kid_id, "froehlich", "hoffnungsvoll", 6.0 + i * 0.5))
        js.append(swap(kid_id, "hoffnungsvoll", "froehlich", 10.5 + i * 0.4))
    hero = kid(f"{p}-k", c, "heute", ["traurig", "nachdenklich", "weinend"], 540, 1990, 1180)
    lines = d["flur_zeilen"]
    tb, tj = text_lines(p, lines)
    body = (f'<div id="{p}-stage" class="stage">{"".join(world)}</div><div class="scrim"></div>'
            f'<div id="{p}-heroWrap" style="position:absolute;inset:0">{hero}</div>{tb}')
    js += [cam(f"{p}-stage", [(0, 0, -900, 0, 1, ""), (3.6, 3.4, -1873, -390, 1.3, "power2.inOut"),
                             (8.4, 3.0, -1100, -60, 1.06, "power2.inOut")]),
           f'tl.fromTo("#{p}-heroWrap",{{x:0}},{{x:-330,duration:3.4,ease:"power2.inOut"}},3.6);',
           f'tl.to("#{p}-heroWrap",{{x:0,duration:3.0,ease:"power2.inOut"}},8.4);',
           breathe(f"{p}-k", 16),
           swap(f"{p}-k", "traurig", "nachdenklich", 4.2),
           swap(f"{p}-k", "nachdenklich", "traurig", 9.0),
           swap(f"{p}-k", "traurig", "weinend", 13.2),
           tj]
    return scene("flur", body, js)


def s_zuhause(d):
    p, c = "zu", d["kind_nr"]
    s1, s2 = d["geschwister"]
    world = [f'<img class="bg" src="{img("raeume", "wohnzimmer.jpg")}" alt=""/>',
             kid(f"{p}-g1", s1, "heute", ["froehlich", "nachdenklich", "traurig"], 905 * K, 505 * K, 300 * K, clip=0.52),
             kid(f"{p}-g2", s2, "heute", ["froehlich", "nachdenklich", "traurig"], 1185 * K, 470 * K, 270 * K, clip=0.52),
             kid(f"{p}-ghost", c, "heute", ["hoffnungsvoll", "traurig"], 330 * K, 1010 * K, 560 * K, extra_style="opacity:0")]
    tb, tj = text_lines(p, d["zuhause_zeilen"])
    body = f'<div id="{p}-stage" class="stage">{"".join(world)}</div><div class="scrim"></div>{tb}'
    t_leer = d["zuhause_zeilen"][-1][1]
    js = [cam(f"{p}-stage", [(0, 0, -1640, -40, 1.04, ""), (3.0, 3.6, -400, 0, 1.0, "power2.inOut"),
                            (t_leer + 0.4, 5.0, -560, -380, 1.25, "power1.inOut")]),
          breathe(f"{p}-g1", 12, 1.5, 0.015), breathe(f"{p}-g2", 12, 1.8, 0.015, 0.4),
          swap(f"{p}-g1", "froehlich", "nachdenklich", 6.5), swap(f"{p}-g2", "froehlich", "traurig", 7.2),
          # Erinnerung: das Kind erscheint kurz neben seinem Stuhl ... und verblasst, wenn der Platz "leer bleibt"
          f'tl.to("#{p}-ghost",{{opacity:0.62,duration:1.4,ease:"power2.out"}},5.4);',
          swap(f"{p}-ghost", "hoffnungsvoll", "traurig", t_leer + 1.2),
          f'tl.to("#{p}-ghost",{{opacity:0,duration:2.2,ease:"power2.in"}},{t_leer + 3.2:.2f});',
          breathe(f"{p}-ghost", 12, 1.7, 0.012),
          tj]
    return scene("zuhause", body, js)


def s_wandel(d):
    p, c = "wa", d["kind_nr"]
    years = ["2026", "1990", "1945", "1933", "1922", d["epoche"]]
    roll = "".join(f'<div class="yr{" last" if i == len(years) - 1 else ""}">{esc(y)}</div>' for i, y in enumerate(years))
    css = f"""
    #root .layer {{ position:absolute; inset:0; }}
    #root .layer > img.bg {{ position:absolute; left:-900px; top:0; width:2880px; height:1920px; }}
    #root #wa-past {{ clip-path: inset(0 100% 0 0); }}
    #root #wa-band {{ position:absolute; top:0; bottom:0; width:160px; left:-160px;
       background:linear-gradient(90deg, rgba(255,240,210,0) 0%, rgba(255,240,210,0.85) 50%, rgba(255,240,210,0) 100%); }}
    #root #wa-yrWin {{ position:absolute; left:110px; top:330px; width:860px; height:300px; overflow:hidden; }}
    #root #wa-yrStrip .yr {{ height:300px; display:flex; align-items:center; justify-content:center; color:{CREAM};
      font-family:"League Gothic",sans-serif; font-size:280px; line-height:1; text-shadow:0 4px 24px rgba(0,0,0,0.5); }}
    #root #wa-yrStrip .yr.last {{ font-size:{d.get('epoche_size', 170)}px; letter-spacing:0.02em; }}"""
    now = kid(f"{p}-k1", c, "heute", ["traurig"], 540, 2350, 2100)
    old = kid(f"{p}-k2", c, "sepia", ["traurig", "aengstlich"], 540, 2350, 2100)
    body = (f'<div id="wa-now" class="layer"><img class="bg" src="{img("raeume", "wohnzimmer_weich.jpg")}" alt=""/>{now}</div>'
            f'<div id="wa-past" class="layer"><img class="bg" src="{img("raeume", "speisesaal_weich.jpg")}" alt=""/>{old}</div>'
            f'<div id="wa-band"></div><div class="scrim"></div>'
            f'<div id="wa-yr" class="clip" data-start="0.1" data-duration="5.8" data-track-index="2" data-layout-allow-overflow>'
            f'<div id="wa-yrWin" data-layout-ignore><div id="wa-yrStrip" data-layout-ignore>{roll}</div></div></div>')
    js = [f'tl.fromTo("#wa-now .kidbody, #wa-past .kidbody",{{scale:1}},{{scale:1.06,transformOrigin:"50% 30%",duration:6,ease:"none"}},0);',
          'tl.to("#wa-past",{clipPath:"inset(0 0% 0 0)",duration:1.6,ease:"power2.inOut"},1.2);',
          'tl.fromTo("#wa-band",{x:0},{x:1240,duration:1.6,ease:"power2.inOut"},1.2);',
          f'tl.fromTo("#wa-yrStrip",{{y:0}},{{y:{-300 * (len(years) - 1)},duration:3.2,ease:"power3.inOut"}},1.0);',
          'tl.fromTo("#wa-yrStrip",{filter:"blur(0px)"},{filter:"blur(5px)",duration:1.2,ease:"power2.in",yoyo:true,repeat:1},1.3);',
          swap(f"{p}-k2", "traurig", "aengstlich", 4.4),
          'tl.to("#wa-yr",{opacity:0,duration:0.3},5.55);']
    return scene("wandel", body, js, css)


def s_damals(d):
    p, c = "da", d["kind_nr"]
    world = [f'<img class="bg" src="{img("raeume", "speisesaal.jpg")}" alt=""/>']
    # Schatten eines Erwachsenen an der Rückwand
    world.append(f'<svg id="{p}-shadow" width="520" height="1110" viewBox="0 0 420 900" style="position:absolute;left:2300px;top:470px;opacity:0" data-layout-ignore>'
                 '<g fill="#1a120c"><ellipse cx="210" cy="110" rx="70" ry="85"/><rect x="185" y="185" width="50" height="40"/>'
                 '<path d="M60 900 L90 300 Q110 220 210 215 Q310 220 330 300 L360 900 Z"/>'
                 '<path d="M95 320 L20 640 L60 650 L120 390 Z"/></g></svg>')
    rows = d["damals_kinder"]   # [(char, table)]
    tables = {1: (1125, 620, [470, 975, 1462]), 2: (880, 430, [712, 1200, 1687]), 3: (825, 356, [1300, 1700])}
    used = {1: 0, 2: 0, 3: 0}
    kid_ids = []
    for ch, t in rows:
        clipY, h, xs = tables[t]
        x = xs[used[t]]; used[t] += 1
        kid_id = f"{p}-r{ch}"
        world.append(kid(kid_id, ch, "sepia", ["traurig", "aengstlich", "nachdenklich"], x, clipY, h, clip=0.5,
                            first=["traurig", "nachdenklich", "aengstlich"][ch % 3]))
        kid_ids.append(kid_id)
    hero = kid(f"{p}-k", c, "sepia", ["aengstlich", "nachdenklich", "traurig", "weinend"], 560, 2020, 1000)
    css = f"""
    #root #da-card {{ position:absolute; left:80px; top:300px; width:920px; height:470px; background:#EFE6D2;
      border:3px solid #8C7E66; box-shadow:0 14px 0 rgba(30,20,10,0.35); transform:rotate(-1deg); }}
    #root .akte {{ left:130px; top:350px; width:820px; color:#2E2A25; font-family:"IBM Plex Mono",monospace; font-weight:600;
      font-size:44px; line-height:1.28; text-shadow:none; }}
    #root .akte.stamp {{ font-family:"Inter",sans-serif; font-weight:900; font-size:56px; text-transform:uppercase; color:#7A2A20; }}
    #root .akte.stamp .w {{ border:5px solid #7A2A20; padding:2px 12px; margin:6px 8px 0 0; transform:rotate(-2deg); }}"""
    lines = d["damals_zeilen"]
    tb, tj = text_lines(p, lines, cls="line akte")
    for i, l in enumerate(lines):
        if l[3] == "stamp":
            tb = tb.replace(f'id="{p}-l{i}" class="clip line akte"', f'id="{p}-l{i}" class="clip line akte stamp"')
    src = f'<div id="{p}-src" class="src" style="top:715px;left:130px;color:#5A5040">Quelle: {esc(d["damals_quelle"])}</div>'
    body = (f'<div id="{p}-stage" class="stage">{"".join(world)}</div>'
            f'<div id="{p}-heroWrap" style="position:absolute;inset:0">{hero}</div>'
            f'<div id="{p}-cardClip" class="clip" data-start="0" data-duration="19" data-track-index="1"><div id="da-card"></div>{src}</div>{tb}')
    t_stamp = lines[1][1]
    t_q = lines[2][1]
    js = [cam(f"{p}-stage", [(0, 0, -420, -60, 1.04, ""), (0.2, 18.6, -700, -60, 1.04, "none")]),
          'tl.fromTo("#da-card",{y:-50,opacity:0},{y:0,opacity:1,duration:0.7,ease:"power3.out"},0.1);',
          'tl.fromTo("#da-src",{opacity:0},{opacity:1,duration:0.5},0.6);',
          'tl.to("#da-cardClip",{opacity:0,duration:0.3},18.6);',
          breathe(f"{p}-k", 19, 1.5, 0.014)]
    for i, k in enumerate(kid_ids):
        js.append(breathe(k, 19, 1.6 + i * 0.13, 0.012, i * 0.2))
    # Bei den Stempeln: alle Kinder nehmen dieselbe Haltung an (Gehorsam)
    for i, (k, (ch, _)) in enumerate(zip(kid_ids, rows)):
        first = ["traurig", "nachdenklich", "aengstlich"][ch % 3]
        if first != "traurig":
            js.append(swap(k, first, "traurig", t_stamp + 1.5 + i * 0.12))
    # Schatten kommt bei der Frage
    js += [f'tl.fromTo("#{p}-shadow",{{x:0,opacity:0}},{{x:-900,opacity:0.5,duration:5.5,ease:"power1.inOut"}},{t_q - 0.5:.2f});',
           swap(f"{p}-k", "aengstlich", "nachdenklich", 2.2),
           swap(f"{p}-k", "nachdenklich", "traurig", t_stamp + 0.5),
           swap(f"{p}-k", "traurig", "aengstlich", t_q + 0.8),
           swap(f"{p}-k", "aengstlich", "weinend", t_q + 4.6),
           tj]
    return scene("damals", body, js, css)


def s_recht(d):
    p, c = "re", d["kind_nr"]
    world = [f'<img class="bg" src="{img("raeume", "gespraech.jpg")}" alt=""/>']
    hero = kid(f"{p}-k", c, "heute", ["nachdenklich", "ueberrascht", "hoffnungsvoll", "froehlich"], 290, 2000, 1060)
    css = f"""
    #root #re-flash {{ position:absolute; inset:0; background:#F3E3C6; }}
    #root #re-para {{ position:absolute; left:124px; top:320px; width:860px; font-family:"Inter",sans-serif; font-weight:900;
      font-size:104px; line-height:1; letter-spacing:-0.02em; color:#FFFFFF; }}
    #root #re-para span {{ background:{RED}; padding:6px 20px; display:inline-block; }}
    #root .sub {{ top:480px; font-size:54px; }}"""
    title = d["recht_titel"]
    t1 = 1.2
    t_para = t1 + max(read_time(title), 3.0) + len(title.split()) * 0.11 + 0.9
    lines = [(title, t1, t_para - 0.45, "blur")]
    tb, tj = text_lines(p, lines)
    sb, sj = text_lines(p + "s", [(d["recht_sub"], t_para + 0.5, 14.6, "line")], cls="line sub")
    para = (f'<div id="re-paraClip" class="clip" data-start="{t_para:.2f}" data-duration="{15 - t_para:.2f}" data-track-index="3">'
            f'<div id="re-para"><span>{esc(d["paragraph"])}</span></div>'
            f'<div id="re-src" class="src" style="top:800px">Quelle: {esc(d["recht_quelle"])}</div></div>')
    body = (f'<div id="{p}-stage" class="stage">{"".join(world)}</div><div class="scrim"></div>'
            f'<div id="{p}-heroWrap" style="position:absolute;inset:0">{hero}</div>{tb}{para}{sb}<div id="re-flash"></div>')
    js = [cam(f"{p}-stage", [(0, 0, -900, -40, 1.02, ""), (0.2, 14.6, -1240, -180, 1.12, "power1.inOut")]),
          'tl.fromTo("#re-flash",{opacity:1},{opacity:0,duration:0.9,ease:"power2.out"},0);',
          f'tl.fromTo("#{p}-heroWrap",{{x:-420}},{{x:0,duration:1.4,ease:"power3.out"}},0.2);',
          f'tl.fromTo("#{p}-heroWrap",{{y:0}},{{y:-18,duration:0.35,ease:"sine.inOut",yoyo:true,repeat:3}},0.2);',
          breathe(f"{p}-k", 15),
          swap(f"{p}-k", "nachdenklich", "ueberrascht", t_para - 0.2),
          swap(f"{p}-k", "ueberrascht", "hoffnungsvoll", t_para + 1.6),
          f'tl.fromTo("#re-para span",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:0.45,ease:"expo.out"}},{t_para:.2f});',
          f'tl.fromTo("#re-src",{{opacity:0}},{{opacity:1,duration:0.5}},{t_para + 0.6:.2f});',
          'tl.to("#re-paraClip",{opacity:0,duration:0.3},14.6);',
          tj, sj]
    return scene("recht", body, js, css)


def s_ende(d):
    p, c = "en", d["kind_nr"]
    world = [f'<img class="bg" src="{img("raeume", "wohnzimmer.jpg")}" alt=""/>',
             kid(f"{p}-k", c, "heute", ["hoffnungsvoll", "froehlich"], 330 * K, 1010 * K, 560 * K)]
    tb, tj = text_lines(p, [(d["kind_schluss"], 0.2, 3.3, "grey")])
    rest = {23: "Noch 1 Tag bis Weihnachten", 24: "Frohe Weihnachten"}.get(d["tag"], f"Noch {24 - d['tag']} Tage bis Weihnachten")
    css = f"""
    #root .door {{ position:absolute; top:0; width:540px; height:1920px; background:#8A2A22; }}
    #root .door .inset {{ position:absolute; left:50px; right:50px; top:120px; bottom:120px; border:6px solid #651D17; }}
    #root .door .inset2 {{ position:absolute; left:80px; right:80px; top:150px; bottom:150px; border:3px solid #D9A86F; opacity:0.6; }}
    #root #en-doorL {{ left:0; box-shadow: inset -6px 0 0 #651D17; }} #root #en-doorR {{ left:540px; }}
    #root #en-num {{ position:absolute; left:0; width:1080px; top:360px; text-align:center; font-family:"League Gothic",sans-serif;
      font-size:420px; line-height:1; color:{CREAM}; }}
    #root #en-name {{ position:absolute; left:120px; width:840px; top:830px; text-align:center; font-family:"Inter",sans-serif;
      font-weight:900; font-size:64px; line-height:1.1; color:{CREAM}; }}
    #root #en-rest {{ position:absolute; left:120px; width:840px; top:930px; text-align:center; font-family:"Inter",sans-serif;
      font-size:38px; line-height:1.3; color:#F0D2B0; }}"""
    card = (f'<div id="en-card" class="clip" data-start="3.4" data-duration="3.6" data-track-index="3">'
            f'<div id="en-doorL" class="door"><div class="inset"></div><div class="inset2"></div></div>'
            f'<div id="en-doorR" class="door"><div class="inset"></div><div class="inset2"></div></div>'
            f'<div id="en-num">{d["tag"]}</div><div id="en-name">Systemfehler Familie</div>'
            f'<div id="en-rest">Adventskalender 2026<br>{esc(rest)}</div></div>')
    body = f'<div id="{p}-stage" class="stage">{"".join(world)}</div><div class="scrim"></div>{tb}{card}'
    js = [cam(f"{p}-stage", [(0, 0, -560, -380, 1.25, ""), (0.1, 3.3, -520, -320, 1.21, "power1.inOut")]),
          breathe(f"{p}-k", 7), swap(f"{p}-k", "hoffnungsvoll", "froehlich", 1.8), tj,
          'tl.fromTo("#en-doorL",{x:-560},{x:0,duration:0.7,ease:"power3.inOut"},3.4);',
          'tl.fromTo("#en-doorR",{x:560},{x:0,duration:0.7,ease:"power3.inOut"},3.4);',
          'tl.fromTo("#en-num",{opacity:0,scale:1.25},{opacity:1,scale:1,duration:0.45,ease:"expo.out"},4.1);',
          'tl.fromTo("#en-name",{opacity:0,filter:"blur(8px)"},{opacity:1,filter:"blur(0px)",duration:0.5,ease:"power3.out"},4.4);',
          'tl.fromTo("#en-rest",{opacity:0},{opacity:1,duration:0.5},4.6);']
    return scene("ende", body, js, css)


INDEX_T = Template("""<!doctype html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Systemfehler Familie · Tag $tag</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * { margin:0; padding:0; box-sizing:border-box; }
      html, body { margin:0; width:1080px; height:1920px; overflow:hidden; background:#1b1512; }
      #root { width:100%; height:100%; position:relative; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="$total" data-width="1080" data-height="1920">
$hosts
      <audio id="musik" class="clip" src="assets/melodie.mp3" data-start="0" data-duration="$total" data-track-index="5" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
""")


def build(day, dest):
    d = TAGE[day]
    proj = os.path.join(dest, f"tag-{day:02d}")
    os.makedirs(os.path.join(proj, "compositions"), exist_ok=True)
    for sub in ("kinder", "raeume"):
        os.makedirs(os.path.join(proj, "assets", sub), exist_ok=True)
    shutil.copy(os.path.join(HERE, "melodie.mp3"), os.path.join(proj, "assets", "melodie.mp3"))
    makers = {"flur": s_flur, "zuhause": s_zuhause, "wandel": s_wandel, "damals": s_damals, "recht": s_recht, "ende": s_ende}
    hosts = []
    USED.clear()
    for sid, start, dur in SCENES:
        with open(os.path.join(proj, "compositions", f"{sid}.html"), "w") as f:
            f.write(makers[sid](d))
        hosts.append(f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{start}" data-duration="{dur}" data-track-index="1" data-track-kind="graphics" '
                     f'data-width="1080" data-height="1920"></div>')
    for kind, name in USED:
        shutil.copy(os.path.join(ROOT, kind, name), os.path.join(proj, "assets", kind, name))
    with open(os.path.join(proj, "index.html"), "w") as f:
        f.write(INDEX_T.substitute(tag=day, total=TOTAL, hosts="\n".join(hosts)))
    for old in ("heute", "wandel_alt", "recht_alt"):
        pass
    print("gebaut:", proj, len(USED), "Bilder")


if __name__ == "__main__":
    dest = sys.argv[1]
    for day in [int(x) for x in sys.argv[2:]] or sorted(TAGE):
        build(day, dest)
