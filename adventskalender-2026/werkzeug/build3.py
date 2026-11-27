#!/usr/bin/env python3
"""Stil 3 – Bilderbuch-Film für alle 24 Tage, vollständig aus Daten (folgen.py).

Jede Folge, 75 s, 1080x1920:
  a       0-17   heute, Raum A: das Kind, 3 Zeilen (die erste steht schon im ersten Bild)
  b      17-29   heute, Raum B (oft Erinnerung / Zuhause), 2 Zeilen
  wandel 29-35   Großaufnahme: das Kind wechselt die Zeit, Jahreszahlen rollen
  damals 35-54   historischer Raum, Figuren in Sepia, Akte mit 3 Zeilen + Quelle
  recht  54-68   heute, das Recht als Antwort
  ende   68-75   letzter Satz, Türchen schließt sich

Aufruf: python3 build3.py <zielordner> [tag ...]
"""
import html, os, shutil, sys
from string import Template
from PIL import Image, ImageOps, ImageEnhance

sys.path.insert(0, os.path.dirname(__file__))
from folgen import FOLGEN

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(ROOT, ".ton-cache")
CREAM, RED = "#FFF6EA", "#C8352A"
SCENES = [("a", 0, 17), ("b", 17, 12), ("wandel", 29, 6), ("damals", 35, 19), ("recht", 54, 14), ("ende", 68, 7)]
TOTAL = 75
USED = {}      # Projektpfad -> Quellpfad


def E(s):
    return html.escape(s, quote=False)


def words(t):
    return " ".join(f'<span class="w">{E(w)}</span>' for w in t.split())


def chars(t):
    return " ".join('<span class="wd">' + "".join(f'<span class="c">{E(c)}</span>' for c in w) + "</span>" for w in t.split())


def read_time(t):
    return 0.5 + 0.3 * len(t.split())


# ------------------------------------------------------------------ Medien

def tone(img, kind):
    a = img.getchannel("A")
    rgb = img.convert("RGB")
    if kind == "sepia":
        g = ImageEnhance.Contrast(ImageOps.grayscale(rgb)).enhance(0.92)
        out = ImageOps.colorize(g, (52, 36, 24), (246, 226, 196), mid=(160, 124, 88))
    else:  # faded: verblasste 60er-Jahre-Farbe
        out = ImageEnhance.Color(rgb).enhance(0.45)
        out = Image.blend(out, Image.new("RGB", out.size, (214, 196, 160)), 0.12)
    out = out.convert("RGBA"); out.putalpha(a)
    return out


def figure_src(ref):
    """'k01_heute_traurig' oder 'k01_damals_still~sepia' -> (Projektpfad, Breite/Höhe)."""
    name, _, kind = ref.partition("~")
    src = os.path.join(ROOT, "kinder", name + ".webp")
    if not os.path.exists(src):
        raise FileNotFoundError(ref)
    if kind:
        os.makedirs(CACHE, exist_ok=True)
        cached = os.path.join(CACHE, f"{name}~{kind}.webp")
        if not os.path.exists(cached):
            tone(Image.open(src).convert("RGBA"), kind).save(cached, "WEBP", quality=88, method=5)
        src = cached
    rel = f"assets/fig/{os.path.basename(src).replace('~', '_')}"
    USED[rel] = src
    w, h = Image.open(src).size
    return rel, w / h


def room_src(name):
    rel = f"assets/raum/{name}.jpg"
    USED[rel] = os.path.join(ROOT, "raeume", name + ".jpg")
    return rel


# ------------------------------------------------------------------ Bausteine

SLOTS = {   # x-Mitte, Fußlinie, Höhe (Bildschirmkoordinaten)
    "hero": (540, 1990, 1150), "hero-l": (390, 1990, 1120), "hero-r": (690, 1990, 1120),
    "mid-l": (250, 1760, 780), "mid-r": (830, 1760, 780),
    "back-l": (230, 1500, 480), "back-c": (540, 1470, 430), "back-r": (850, 1500, 480),
    "close": (540, 2420, 2150),
}


def figure(fid, base, poses, slot, ghost=False, maxw=980):
    """base: 'k01_heute' / 'mama01' / 'k03_damals' ...; poses: Liste von Pose-Namen (mit optionalem ~ton)."""
    x, bottom, h = SLOTS[slot] if isinstance(slot, str) else slot
    layers, ratios = [], []
    for i, p in enumerate(poses):
        pose, _, kind = p.partition("~")
        rel, r = figure_src(f"{base}_{pose}" + (f"~{kind}" if kind else ""))
        ratios.append(r)
        layers.append((pose, rel, r))
    html_layers = []
    for i, (pose, rel, r) in enumerate(layers):
        ph = min(h, maxw / r)               # breite Posen (Bett) passen sich an
        pw = ph * r
        html_layers.append(
            f'<div id="{fid}-{i}" class="pose" style="opacity:{1 if i == 0 else 0};left:{x - pw / 2:.0f}px;top:{bottom - ph:.0f}px;'
            f'width:{pw:.0f}px;height:{ph:.0f}px"><img src="{rel}" alt=""/></div>')
    op = 0.6 if ghost else 1
    return (f'<div id="{fid}" class="fig" style="opacity:{op}" data-layout-ignore>'
            f'<div id="{fid}-b" class="figb" style="transform-origin:{x}px {bottom}px">{"".join(html_layers)}</div></div>')


def swap_js(fid, i, j, t):
    return (f'tl.to("#{fid}-{i}",{{opacity:0,duration:0.25,ease:"power1.in"}},{t:.2f});'
            f'tl.fromTo("#{fid}-{j}",{{opacity:0,scale:0.97}},{{opacity:1,scale:1,duration:0.35,ease:"power2.out",'
            f'transformOrigin:"50% 100%",immediateRender:false}},{t:.2f});')


def breathe_js(fid, dur, period=1.7, amt=0.012, delay=0.0):
    reps = max(1, int(dur / period))
    return (f'tl.fromTo("#{fid}-b",{{scaleY:1}},{{scaleY:{1 + amt},duration:{period / 2:.2f},ease:"sine.inOut",'
            f'yoyo:true,repeat:{reps * 2 - 1}}},{delay:.2f});')


def pose_plan(fid, n, marks, dur, start_at=None):
    """Wechselt die Pose bei den Zeilenanfängen (oder gleichmäßig verteilt)."""
    if n < 2:
        return ""
    if start_at:
        ts = start_at
    elif len(marks) >= n:
        ts = [marks[i][0] + 0.4 for i in range(1, n)]
    else:
        ts = [dur * k / n for k in range(1, n)]
    return "".join(swap_js(fid, k, k + 1, t) for k, t in enumerate(ts[:n - 1]))


def layout_lines(lines, t0, t1, styles, gap=0.4):
    """Verteilt die Zeilen im Fenster [t0, t1] nach Lesezeit."""
    need = []
    for i, t in enumerate(lines):
        st = styles[i % len(styles)]
        intro = len(t) * 0.022 if st == "type" else len(t.split()) * 0.06
        need.append(read_time(t) + intro + 0.15)
    total = sum(need) + gap * (len(lines) - 1)
    if total > t1 - t0 + 0.01:
        raise ValueError(f"Zeilen zu lang ({total:.1f}s > {t1 - t0:.1f}s): {lines}")
    extra = (t1 - t0 - total) / len(lines)
    out, t = [], t0
    for i, txt in enumerate(lines):
        e = t + need[i] + extra
        out.append((txt, t, e, styles[i % len(styles)]))
        t = e + gap
    return out


def text_block(prefix, specs, cls="line"):
    body, js = [], []
    for i, (txt, s, e, st) in enumerate(specs):
        lid = f"{prefix}-l{i}"
        stamp = txt.startswith("!")
        if stamp:
            txt, st = txt[1:], "stamp"
        inner = chars(txt) if st == "type" else words(txt)
        c = cls + (" stamp" if stamp else "")
        body.append(f'<div id="{lid}" class="clip {c}" data-start="{s:.2f}" data-duration="{e - s + 0.35:.2f}" '
                    f'data-track-index="2" data-hold>{inner}</div>')
        js.append({"blur": f'blurWords("#{lid}",{s:.2f});', "grey": f'greyWords("#{lid}",{s:.2f});',
                   "line": f'lineIn("#{lid}",{s:.2f});', "type": f'typeIn("#{lid}",{s:.2f});',
                   "stamp": f'stampWords("#{lid}",{s:.2f});', "none": ""}[st])
        js.append(f'outLine("#{lid}",{e - 0.3:.2f});')
    return "\n".join(body), "\n".join(js), [(s, e) for _, s, e, _ in specs]


def stage(sid, room, cam, weich=False):
    """Bühnenbild 2880x1920 mit Kamerafahrt cam=(x0, x1, s0, s1, ease) über die Szenendauer."""
    rel = room_src(room + ("_weich" if weich else ""))
    return (f'<div id="{sid}-stage" class="stage"><img class="bg" src="{rel}" alt=""/></div>', cam)


def cam_js(sid, cam, dur):
    x0, x1, s0, s1, ease = cam
    return (f'tl.set("#{sid}-stage",{{x:{x0},y:{-(s0 - 1) * 960:.0f},scale:{s0},transformOrigin:"0 0"}},0);'
            f'tl.to("#{sid}-stage",{{x:{x1},y:{-(s1 - 1) * 960:.0f},scale:{s1},duration:{dur - 0.1:.2f},ease:"{ease}"}},0.05);')


HELPERS = """
function blurWords(sel,t,gap){tl.fromTo(sel+" .w",{opacity:0,filter:"blur(7px)"},{opacity:1,filter:"blur(0px)",duration:0.55,ease:"power2.out",stagger:gap||0.1},t);}
function greyWords(sel,t,gap){tl.fromTo(sel+" .w",{opacity:0.16},{opacity:1,duration:0.45,ease:"none",stagger:gap||0.1},t);}
function lineIn(sel,t){tl.fromTo(sel,{opacity:0,filter:"blur(9px)"},{opacity:1,filter:"blur(0px)",duration:0.7,ease:"power3.out"},t);}
function typeIn(sel,t,gap){tl.fromTo(sel+" .c",{opacity:0},{opacity:1,duration:0.01,ease:"none",stagger:gap||0.022},t);}
function stampWords(sel,t,gap){var ws=document.querySelectorAll(sel+" .w");ws.forEach(function(w,i){tl.fromTo(w,{opacity:0,scale:1.4},{opacity:1,scale:1,duration:0.12,ease:"power4.out"},t+i*(gap||0.38));});}
function outLine(sel,t){tl.to(sel,{opacity:0,filter:"blur(7px)",duration:0.3,ease:"power2.in"},t);}
"""

BASE_CSS = f"""
    #root {{ position:absolute; inset:0; overflow:hidden; background:#1b1512; }}
    #root .stage {{ position:absolute; left:0; top:0; width:2880px; height:1920px; }}
    #root .stage img.bg {{ position:absolute; left:0; top:0; width:2880px; height:1920px; }}
    #root .fig, #root .figb {{ position:absolute; inset:0; }}
    #root .pose {{ position:absolute; }}
    #root .pose img {{ width:100%; height:100%; display:block; }}
    #root .scrim {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(14,10,9,0.8) 0%, rgba(14,10,9,0.58) 30%, rgba(14,10,9,0) 50%); }}
    #root .line {{ position:absolute; left:124px; top:330px; width:756px; color:{CREAM}; font-family:"Nunito",sans-serif;
                  font-weight:900; font-size:62px; line-height:1.16; letter-spacing:-0.01em; text-shadow:0 3px 18px rgba(0,0,0,0.45); }}
    #root .line .w, #root .line .wd {{ display:inline-block; }}
    #root .src {{ position:absolute; left:124px; width:640px; font-family:"Inter",sans-serif; font-size:28px; line-height:1.3; color:rgba(255,246,234,0.85); }}
    #root .flash {{ position:absolute; inset:0; background:#fff; opacity:0; }}"""

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
    return SCENE_T.substitute(id=sid, css=BASE_CSS + css, body=body, helpers=HELPERS,
                              js="\n".join(x for x in js if x))


def figures_block(sid, figs, dur, marks):
    """figs: [{base, poses, slot, ghost?, at?, enter?, fade_in?, fade_out?}] -> HTML, JS"""
    body, js = [], []
    for i, f in enumerate(figs):
        fid = f"{sid}-f{i}"
        body.append(figure(fid, f["base"], f["poses"], f["slot"], f.get("ghost", False)))
        js.append(breathe_js(fid, dur, 1.5 + 0.17 * i, 0.012 if f["slot"].startswith(("hero", "close")) else 0.016, 0.25 * i))
        js.append(pose_plan(fid, len(f["poses"]), marks if f.get("follow", True) else [], dur, f.get("at")))
        if f.get("enter"):
            dx = -520 if f["enter"] == "left" else 520
            js.append(f'tl.fromTo("#{fid}",{{x:{dx}}},{{x:0,duration:1.3,ease:"power3.out"}},{f.get("enter_t", 0.2)});')
        if f.get("fade_in") is not None:
            op = 0.6 if f.get("ghost") else 1
            js.append(f'tl.fromTo("#{fid}",{{opacity:0}},{{opacity:{op},duration:1.3,ease:"power2.out"}},{f["fade_in"]});')
        if f.get("fade_out") is not None:
            js.append(f'tl.to("#{fid}",{{opacity:0,duration:1.8,ease:"power2.in"}},{f["fade_out"]});')
        if f.get("shrink") is not None:
            js.append(f'tl.to("#{fid}-b",{{scale:0.62,duration:4.5,ease:"power1.inOut"}},{f["shrink"]});')
    return "\n".join(body), js


# ------------------------------------------------------------------ Szenen

def s_heute(sid, d, key, dur, lines_window):
    sh = d[key]
    st, cam = stage(sid, sh["raum"], sh.get("cam", (-420, -1080, 1.0, 1.06, "power1.inOut")))
    styles = ["none", "blur", "grey"] if key == "a" else ["blur", "grey"]
    specs = layout_lines(sh["zeilen"], *lines_window, styles)
    tb, tj, marks = text_block(sid, specs)
    fb, fj = figures_block(sid, sh["figuren"], dur, marks)
    body = st + fb + '<div class="scrim"></div>' + tb + ('<div id="%s-flash" class="flash"></div>' % sid if sh.get("blitz") else "")
    js = [cam_js(sid, cam, dur)] + fj + [tj]
    if sh.get("blitz"):
        js.append(f'tl.fromTo("#{sid}-flash",{{opacity:0.95}},{{opacity:0,duration:0.7,ease:"power2.out",immediateRender:false}},{sh["blitz"]});')
    return scene(sid, body, js)


def s_wandel(d):
    sid = "wandel"
    w = d["wandel"]
    target = w["ziel"]                       # z. B. 'k01_damals' + Pose
    years = w.get("jahre") or (["2026", "1990", "1945", "1933"] if not d["epoche"][:4].isdigit() or int(d["epoche"][:4]) < 1990 else ["2026", "2016"])
    years = years + [d["epoche"]]
    roll = "".join(f'<div class="yr{" last" if i == len(years) - 1 else ""}">{E(y)}</div>' for i, y in enumerate(years))
    css = f"""
    #root .layer {{ position:absolute; inset:0; }}
    #root .layer .stage {{ left:-900px; }}
    #root #wandel-past {{ clip-path: inset(0 100% 0 0); }}
    #root #wandel-band {{ position:absolute; top:0; bottom:0; width:160px; left:-160px;
       background:linear-gradient(90deg, rgba(255,240,210,0) 0%, rgba(255,240,210,0.85) 50%, rgba(255,240,210,0) 100%); }}
    #root #wandel-yrWin {{ position:absolute; left:124px; top:330px; width:756px; height:300px; overflow:hidden; }}
    #root #wandel-yrStrip .yr {{ height:300px; display:flex; align-items:center; justify-content:center; color:{CREAM};
      font-family:"League Gothic",sans-serif; font-size:280px; line-height:1; text-shadow:0 4px 24px rgba(0,0,0,0.5); }}
    #root #wandel-yrStrip .yr.last {{ font-size:{w.get('size', 150 if len(d['epoche']) > 6 else 250)}px; letter-spacing:0.02em; }}"""
    now = figure("wandel-n", d["kind_heute"], ["traurig"], "close")
    old = figure("wandel-o", target[0], [target[1]], "close")
    body = (f'<div id="wandel-now" class="layer"><div class="stage"><img class="bg" src="{room_src(d["a"]["raum"] + "_weich") if os.path.exists(os.path.join(ROOT, "raeume", d["a"]["raum"] + "_weich.jpg")) else room_src(d["a"]["raum"])}" alt=""/></div>{now}</div>'
            f'<div id="wandel-past" class="layer"><div class="stage"><img class="bg" src="{room_src(d["damals"]["raum"] + "_weich")}" alt=""/></div>{old}</div>'
            f'<div id="wandel-band"></div><div class="scrim"></div>'
            f'<div id="wandel-yr" class="clip" data-start="0.1" data-duration="5.8" data-track-index="2" data-layout-allow-overflow>'
            f'<div id="wandel-yrWin" data-layout-ignore><div id="wandel-yrStrip" data-layout-ignore>{roll}</div></div></div>')
    n = len(years) - 1
    js = ['tl.fromTo("#wandel-n-b, #wandel-o-b",{scale:1},{scale:1.06,transformOrigin:"50% 40%",duration:6,ease:"none"},0);',
          'tl.to("#wandel-past",{clipPath:"inset(0 0% 0 0)",duration:1.6,ease:"power2.inOut"},1.2);',
          'tl.fromTo("#wandel-band",{x:0},{x:1240,duration:1.6,ease:"power2.inOut"},1.2);',
          f'tl.fromTo("#wandel-yrStrip",{{y:0}},{{y:{-300 * n},duration:3.0,ease:"power3.inOut"}},1.0);',
          'tl.fromTo("#wandel-yrStrip",{filter:"blur(0px)"},{filter:"blur(5px)",duration:1.1,ease:"power2.in",yoyo:true,repeat:1},1.3);',
          'tl.to("#wandel-yr",{opacity:0,duration:0.3},5.55);']
    return scene("wandel", body, js, css)


def s_damals(d):
    sid = "damals"
    dm = d["damals"]
    st, cam = stage(sid, dm["raum"], dm.get("cam", (-1250, -650, 1.04, 1.0, "none")))
    css = """
    #root #damals-card { position:absolute; left:80px; top:300px; width:920px; height:580px; background:#EFE6D2;
      border:3px solid #8C7E66; box-shadow:0 14px 0 rgba(30,20,10,0.35); transform:rotate(-1deg); }
    #root .akte { left:130px; top:350px; width:760px; color:#2E2A25; font-family:"IBM Plex Mono",monospace; font-weight:600;
      font-size:42px; line-height:1.28; text-shadow:none; }
    #root .akte.stamp { font-family:"Inter",sans-serif; font-weight:900; font-size:72px; text-transform:uppercase; color:#7A2A20; top:420px; }
    #root .akte.stamp .w { border:6px solid #7A2A20; padding:4px 16px; margin:6px 8px 0 0; transform:rotate(-3deg); }"""
    specs = layout_lines(dm["zeilen"], 0.8, 18.6, ["type", "line", "type"])
    tb, tj, marks = text_block(sid, specs, cls="line akte")
    fb, fj = figures_block(sid, dm["figuren"], 19, marks)
    src = f'<div id="damals-src" class="src" style="top:770px;left:130px;width:760px;color:#5A5040">Quelle: {E(dm["quelle"])}</div>'
    body = (st + fb + f'<div id="damals-cardClip" class="clip" data-start="0" data-duration="19" data-track-index="1">'
            f'<div id="damals-card"></div>{src}</div>' + tb)
    js = [cam_js(sid, cam, 19),
          'tl.fromTo("#damals-card",{y:-50,opacity:0},{y:0,opacity:1,duration:0.7,ease:"power3.out"},0.1);',
          'tl.fromTo("#damals-src",{opacity:0},{opacity:1,duration:0.5},0.6);',
          'tl.to("#damals-cardClip",{opacity:0,duration:0.3},18.6);'] + fj + [tj]
    return scene(sid, body, js, css)


def s_recht(d):
    sid = "recht"
    r = d["recht"]
    st, cam = stage(sid, r.get("raum", "gespraech"), r.get("cam", (-900, -1240, 1.02, 1.1, "power1.inOut")))
    psize = r.get("size", 104 if len(r["paragraph"]) <= 14 else 70)
    css = f"""
    #root #recht-flash {{ position:absolute; inset:0; background:#F3E3C6; }}
    #root #recht-para {{ position:absolute; left:124px; top:320px; width:756px; font-family:"Inter",sans-serif; font-weight:900;
      font-size:{psize}px; line-height:1; letter-spacing:-0.02em; color:#fff; }}
    #root #recht-para span {{ background:{RED}; padding:6px 20px; display:inline-block; }}
    #root .sub {{ top:{340 + psize + 40}px; font-size:52px; }}"""
    title = r["titel"]
    t1 = 1.2
    t_para = t1 + read_time(title) + len(title.split()) * 0.1 + 1.0
    if t_para > 8.2:
        raise ValueError("Titel zu lang: " + title)
    tb, tj, _ = text_block(sid, [(title, t1, t_para - 0.45, "blur")])
    sb, sj, _ = text_block(sid + "s", [(r["sub"], t_para + 0.5, 13.6, "line")], cls="line sub")
    para = (f'<div id="recht-paraClip" class="clip" data-start="{t_para:.2f}" data-duration="{14 - t_para:.2f}" data-track-index="3">'
            f'<div id="recht-para"><span>{E(r["paragraph"])}</span></div>'
            f'<div id="recht-src" class="src" style="top:850px">Quelle: {E(r["quelle"])}</div></div>')
    figs = r.get("figuren") or [{"base": d["kind_heute"], "poses": ["nachdenklich", "ueberrascht", "hoffnungsvoll"],
                                 "slot": "hero-l", "enter": "left", "at": [t_para - 0.2, t_para + 1.6]}]
    fb, fj = figures_block(sid, figs, 14, [])
    body = st + fb + '<div class="scrim"></div>' + tb + para + sb + '<div id="recht-flash"></div>'
    js = [cam_js(sid, cam, 14),
          'tl.fromTo("#recht-flash",{opacity:1},{opacity:0,duration:0.9,ease:"power2.out"},0);',
          f'tl.fromTo("#recht-para span",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:0.45,ease:"expo.out"}},{t_para:.2f});',
          f'tl.fromTo("#recht-src",{{opacity:0}},{{opacity:1,duration:0.5}},{t_para + 0.6:.2f});',
          'tl.to("#recht-paraClip",{opacity:0,duration:0.3},13.6);'] + fj + [tj, sj]
    return scene(sid, body, js, css)


def s_ende(d):
    sid = "ende"
    st, cam = stage(sid, d["a"]["raum"], (-700, -760, 1.12, 1.16, "power1.inOut"))
    last = d["schluss"]
    t_end = min(0.2 + read_time(last) + len(last.split()) * 0.1 + 0.4, 3.9)
    tb, tj, _ = text_block(sid, [(last, 0.2, t_end, "grey")])
    t_door = t_end + 0.05
    rest = {23: "Noch 1 Tag bis Weihnachten", 24: "Frohe Weihnachten"}.get(d["tag"], f"Noch {24 - d['tag']} Tage bis Weihnachten")
    css = f"""
    #root .door {{ position:absolute; top:0; width:540px; height:1920px; background:#8A2A22; }}
    #root .door .inset {{ position:absolute; left:50px; right:50px; top:120px; bottom:120px; border:6px solid #651D17; }}
    #root .door .inset2 {{ position:absolute; left:80px; right:80px; top:150px; bottom:150px; border:3px solid #D9A86F; opacity:0.6; }}
    #root #ende-doorL {{ left:0; box-shadow: inset -6px 0 0 #651D17; }} #root #ende-doorR {{ left:540px; }}
    #root #ende-num {{ position:absolute; left:0; width:1080px; top:360px; text-align:center; font-family:"League Gothic",sans-serif;
      font-size:420px; line-height:1; color:{CREAM}; }}
    #root #ende-name {{ position:absolute; left:120px; width:840px; top:830px; text-align:center; font-family:"Inter",sans-serif;
      font-weight:900; font-size:64px; line-height:1.1; color:{CREAM}; }}
    #root #ende-rest {{ position:absolute; left:120px; width:840px; top:930px; text-align:center; font-family:"Inter",sans-serif;
      font-size:38px; line-height:1.3; color:#F0D2B0; }}"""
    card = (f'<div id="ende-card" class="clip" data-start="{t_door:.2f}" data-duration="{7 - t_door:.2f}" data-track-index="3">'
            f'<div id="ende-doorL" class="door"><div class="inset"></div><div class="inset2"></div></div>'
            f'<div id="ende-doorR" class="door"><div class="inset"></div><div class="inset2"></div></div>'
            f'<div id="ende-num">{d["tag"]}</div><div id="ende-name">Systemfehler Familie</div>'
            f'<div id="ende-rest">Adventskalender 2026<br>{E(rest)}</div></div>')
    figs = [{"base": d["kind_heute"], "poses": d.get("ende_posen", ["hoffnungsvoll", "froehlich"]), "slot": "hero", "at": [1.8]}]
    fb, fj = figures_block(sid, figs, 7, [])
    body = st + fb + '<div class="scrim"></div>' + tb + card
    js = [cam_js(sid, (-700, -760, 1.12, 1.16, "power1.inOut"), 7)] + fj + [tj,
          f'tl.fromTo("#ende-doorL",{{x:-560}},{{x:0,duration:0.7,ease:"power3.inOut"}},{t_door:.2f});',
          f'tl.fromTo("#ende-doorR",{{x:560}},{{x:0,duration:0.7,ease:"power3.inOut"}},{t_door:.2f});',
          f'tl.fromTo("#ende-num",{{opacity:0,scale:1.25}},{{opacity:1,scale:1,duration:0.45,ease:"expo.out"}},{t_door + 0.7:.2f});',
          f'tl.fromTo("#ende-name",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:0.5,ease:"power3.out"}},{t_door + 1.0:.2f});',
          f'tl.fromTo("#ende-rest",{{opacity:0}},{{opacity:1,duration:0.5}},{t_door + 0.8:.2f});']
    return scene(sid, body, js, css)


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
    d = FOLGEN[day]
    proj = os.path.join(dest, f"tag-{day:02d}")
    if os.path.isdir(os.path.join(proj, "compositions")):
        for f in os.listdir(os.path.join(proj, "compositions")):
            os.remove(os.path.join(proj, "compositions", f))
    os.makedirs(os.path.join(proj, "compositions"), exist_ok=True)
    USED.clear()
    makers = {"a": lambda: s_heute("a", d, "a", 17, (0.0, 16.6)), "b": lambda: s_heute("b", d, "b", 12, (0.3, 11.7)),
              "wandel": lambda: s_wandel(d), "damals": lambda: s_damals(d), "recht": lambda: s_recht(d), "ende": lambda: s_ende(d)}
    hosts = []
    for sid, start, dur in SCENES:
        with open(os.path.join(proj, "compositions", f"{sid}.html"), "w") as f:
            f.write(makers[sid]())
        hosts.append(f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{start}" data-duration="{dur}" data-track-index="1" data-track-kind="graphics" '
                     f'data-width="1080" data-height="1920"></div>')
    shutil.rmtree(os.path.join(proj, "assets"), ignore_errors=True)
    for rel, src in USED.items():
        os.makedirs(os.path.dirname(os.path.join(proj, rel)), exist_ok=True)
        shutil.copy(src, os.path.join(proj, rel))
    shutil.copy(os.path.join(HERE, "melodie.mp3"), os.path.join(proj, "assets", "melodie.mp3"))
    with open(os.path.join(proj, "index.html"), "w") as f:
        f.write(INDEX_T.substitute(tag=day, total=TOTAL, hosts="\n".join(hosts)))
    tpl = os.path.join(HERE, "projekt-vorlage")
    for name in os.listdir(tpl):
        tgt = os.path.join(proj, name)
        if not os.path.exists(tgt):
            open(tgt, "w").write(open(os.path.join(tpl, name)).read().replace("TAGNAME", f"tag-{day:02d}"))
    print(f"Tag {day:2d} gebaut ({len(USED)} Bilder)")


if __name__ == "__main__":
    dest = sys.argv[1]
    for day in [int(x) for x in sys.argv[2:]] or sorted(FOLGEN):
        try:
            build(day, dest)
        except Exception as e:
            print(f"Tag {day:2d} FEHLER: {type(e).__name__}: {e}")
