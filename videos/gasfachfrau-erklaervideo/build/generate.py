#!/usr/bin/env python3
"""Erzeugt index.html und compositions/*.html für das Gasfachfrau-Erklärvideo.

Achtung: Ein erneuter Lauf überschreibt Änderungen, die im Studio an diesen Dateien
gemacht wurden.  Aufruf:  python3 build/generate.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
OR, OR_D, OR_L, PET, INK = "#FD5B2A", "#D9441A", "#FF8B62", "#108474", "#232323"

import wave, struct, math, re

# Stimme: eine durchgehende Aufnahme (kie.ai, ElevenLabs "Will", DE)
AUDIO = "assets/voice/v3/vo.wav"
AUDIO_START = 0.30


def _envelope(path):
    w = wave.open(os.path.join(ROOT, path)); n = w.getnframes(); sr = w.getframerate()
    data = struct.unpack("<%dh" % n, w.readframes(n)); w.close()
    hop = sr // FPS; env = []
    for k in range(0, n, hop):
        ch = data[k:k + hop]; env.append(math.sqrt(sum(x * x for x in ch) / max(1, len(ch))) / 32768)
    m = max(env)
    return [round(min(1, e / m * 1.4), 2) for e in env], n / sr


ENV_ALL, AUDIO_DUR = _envelope(AUDIO)

# Szenen: id, start, dauer (an die Satzgrenzen der Aufnahme gelegt)
SCENES = [
    ("sc1", 0.0, 7.60, "s1"),
    ("sc2", 7.60, 4.95, "s2"),
    ("sc3", 12.55, 4.77, "s3"),
    ("sc4", 17.32, 7.90, "s4"),
    ("sc5", 25.22, 5.62, "s5"),
    ("sc6", 30.84, 10.89, "s6"),
    ("end", 41.73, 5.0, None),
]
TOTAL = 46.73
START = {c: st for c, st, _, _ in SCENES}
NEWDUR = {c: du for c, _, du, _ in SCENES}
CUR = {"scene": None}
# Mundbewegung: alle Szenen nutzen dieselbe Hüllkurve, versetzt um den Szenenstart
VO = {f"s{i}": AUDIO_START for i in range(1, 7)}
ENV = {f"s{i}": ENV_ALL for i in range(1, 7)}

CAPTIONS = [
    ('Tankflasche an der Autogastankstelle füllen?', 0.3, 2.78),
    ('Das ist ab jetzt offiziell erlaubt,', 3.44, 5.09),
    ('aber nur, wenn ich nach der', 5.38, 7.24),
    ('aktuellen G 607 eingebaut bin.', 7.24, 9.3),
    ('Das heißt, ich bin', 9.92, 10.89),
    ('im Flaschenkasten fest fixiert,', 10.89, 12.57),
    ('ohne Werkzeug lösbar und versiegelt.', 13.04, 14.82),
    ('Getankt wird nur über einen Füllanschluss', 15.46, 17.7),
    ('außen am Fahrzeug,', 17.7, 18.68),
    ('mit einer Sicherheitskupplung', 18.99, 20.3),
    ('in der Füllleitung,', 20.3, 21.16),
    ('und die Leitung führt nicht', 21.62, 22.82),
    ('durch den Wohnraum.', 22.82, 23.66),
    ('Dazu kommen ein Sicherheitsventil', 24.12, 26.1),
    ('und der automatische Füllstopp', 26.43, 27.93),
    ('bei achtzig Prozent.', 27.93, 28.94),
    ('Ganz wichtig:', 29.51, 30.11),
    ('Normale Gasflaschen dürfen', 30.69, 32.05),
    ('weiterhin nicht an die Tankstelle.', 32.05, 33.83),
    ('Unsicher, ob deine Anlage passt?', 34.41, 36.03),
    ('Die Gasfachfrau hilft dir gerne weiter.', 36.6, 38.49),
]


# ---------------------------------------------------------------- Gasi
SIL, SIL_D, SIL_L, ANT = "#C9CED3", "#8E959C", "#F4F6F7", "#3A3F44"
BODY_PATH = "M60 250 C60 182 122 150 200 150 C278 150 340 182 340 250 L340 662 C340 690 322 700 292 700 L108 700 C78 700 60 690 60 662 Z"


def gasi(p, look=(0, 0)):
    """Gasi, die silberne Alu-Tankflasche (Form angelehnt an Tankflaschen mit Schutzkragen), viewBox 0 0 400 760."""
    lx, ly = look
    return f"""
<svg viewBox="-60 -10 520 780" class="gasi-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="{p}-alu" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="#7F868D"/><stop offset="0.18" stop-color="#C3C8CD"/><stop offset="0.38" stop-color="#F6F8F9"/>
      <stop offset="0.6" stop-color="#D3D7DB"/><stop offset="0.85" stop-color="#A3AAB0"/><stop offset="1" stop-color="#737A81"/>
    </linearGradient>
  </defs>
  <ellipse cx="200" cy="752" rx="170" ry="16" fill="#000" opacity="0.16"/>
  <g id="{p}-body">
    <g id="{p}-armL"><path d="M62 430 Q-6 500 6 590" fill="none" stroke="{ANT}" stroke-width="26" stroke-linecap="round"/>
      <circle cx="6" cy="598" r="30" fill="#fff" stroke="{ANT}" stroke-width="6"/></g>
    <g id="{p}-armR"><path d="M338 430 Q406 500 394 590" fill="none" stroke="{ANT}" stroke-width="26" stroke-linecap="round"/>
      <circle cx="394" cy="598" r="30" fill="#fff" stroke="{ANT}" stroke-width="6"/></g>
    <path d="M78 690 L322 690 L330 744 L70 744 Z" fill="url(#{p}-alu)" stroke="{ANT}" stroke-width="6" stroke-linejoin="round"/>
    <ellipse cx="130" cy="720" rx="16" ry="9" fill="{ANT}"/><ellipse cx="200" cy="720" rx="16" ry="9" fill="{ANT}"/><ellipse cx="270" cy="720" rx="16" ry="9" fill="{ANT}"/>
    <path d="{BODY_PATH}" fill="url(#{p}-alu)" stroke="{ANT}" stroke-width="7"/>
    <path d="M60 612 L340 612 M60 640 L340 640" stroke="#8E959C" stroke-width="3"/>
    <g id="{p}-valve">
      <path d="M116 168 L124 52 L276 52 L284 168 Z" fill="url(#{p}-alu)" stroke="{ANT}" stroke-width="7" stroke-linejoin="round"/>
      <ellipse cx="200" cy="52" rx="76" ry="14" fill="#DDE1E4" stroke="{ANT}" stroke-width="6"/>
      <rect x="160" y="78" width="80" height="70" rx="10" fill="#2E3337" stroke="{ANT}" stroke-width="5"/>
      <rect x="188" y="96" width="24" height="52" rx="4" fill="#9AA1A7"/><ellipse cx="200" cy="96" rx="20" ry="8" fill="#B9BEC3"/>
    </g>
    <g id="{p}-face">
      <circle cx="118" cy="340" r="24" fill="#FF8A8A" opacity="0.28"/>
      <circle cx="282" cy="340" r="24" fill="#FF8A8A" opacity="0.28"/>
      <g id="{p}-eyes">
        <ellipse cx="150" cy="262" rx="36" ry="44" fill="#fff" stroke="{ANT}" stroke-width="6"/>
        <ellipse cx="250" cy="262" rx="36" ry="44" fill="#fff" stroke="{ANT}" stroke-width="6"/>
        <g id="{p}-pupils"><circle cx="{154+lx}" cy="{268+ly}" r="17" fill="{ANT}"/><circle cx="{254+lx}" cy="{268+ly}" r="17" fill="{ANT}"/>
          <circle cx="{160+lx}" cy="{261+ly}" r="6" fill="#fff"/><circle cx="{260+lx}" cy="{261+ly}" r="6" fill="#fff"/></g>
        <g id="{p}-lids" opacity="0">
          <ellipse cx="150" cy="262" rx="39" ry="47" fill="#D3D7DB" stroke="{ANT}" stroke-width="6"/>
          <ellipse cx="250" cy="262" rx="39" ry="47" fill="#D3D7DB" stroke="{ANT}" stroke-width="6"/>
          <path d="M114 266 Q150 282 186 266 M214 266 Q250 282 286 266" stroke="{ANT}" stroke-width="6" fill="none"/>
        </g>
      </g>
      <g id="{p}-brows">
        <path d="M118 200 Q150 184 182 198" stroke="{ANT}" stroke-width="9" fill="none" stroke-linecap="round"/>
        <path d="M218 198 Q250 184 282 200" stroke="{ANT}" stroke-width="9" fill="none" stroke-linecap="round"/>
      </g>
      <g id="{p}-mouth">
        <path d="M150 362 Q200 372 250 362 Q246 420 200 424 Q154 420 150 362 Z" fill="#3A1210" stroke="{ANT}" stroke-width="6" stroke-linejoin="round"/>
        <ellipse cx="200" cy="408" rx="26" ry="11" fill="#E8575A"/>
      </g>
    </g>
  </g>
</svg>"""


def gasi_rig_js(p, voice_off, env, blinks=(), gestures=(), look_keys=(), brows=()):
    """JS, das Mund (aus Lautstärke), Blinzeln, Arme und Blick von Gasi p animiert."""
    sc = CUR["scene"]; dur = NEWDUR[sc]; off = voice_off - START[sc]
    i0 = max(0, int(math.ceil(-off * FPS))); i1 = min(len(env), int((dur - off) * FPS))
    vals = [round(0.10 + 0.9 * e, 2) for e in env[i0:i1]]
    voice_off = round(off + i0 / FPS, 4)
    return f"""
  (function(){{
    const M = "#{p}-mouth", env = {json.dumps(vals)}, off = {voice_off};
    TLM.set(M, {{ scaleY: 0.1, svgOrigin: "200 364" }}, 0);
    for (let i = 0; i < env.length; i++) TLM.set(M, {{ scaleY: env[i] }}, off + i / 30);
    TLM.set(M, {{ scaleY: 0.1 }}, Math.min(off + env.length / 30, {dur - 0.04:.3f}));
    tl.fromTo("#{p}-body", {{ rotation: -1.2, svgOrigin: "200 740" }}, {{ rotation: 1.2, duration: 1.6, ease: "sine.inOut", yoyo: true, repeat: 7 }}, 0);
    {''.join(f'tl.set("#{p}-lids", {{opacity:1}}, {b}); tl.set("#{p}-lids", {{opacity:0}}, {b + 0.1});' for b in blinks)}
    {''.join(f'tl.to("#{p}-arm{side}", {{ rotation: {rot}, svgOrigin: "{58 if side == "L" else 342} 430", duration: {d}, ease: "back.out(1.6)" }}, {t});' for (side, rot, t, d) in gestures)}
    {''.join(f'tl.to("#{p}-pupils", {{ x: {x}, y: {y}, duration: 0.18, ease: "power2.out" }}, {t});' for (x, y, t) in look_keys)}
    {''.join(f'tl.to("#{p}-brows", {{ y: {y}, duration: 0.2, ease: "power2.out" }}, {t});' for (y, t) in brows)}
  }})();"""


# ---------------------------------------------------------------- Bausteine
PRESENTER_BG = """background: radial-gradient(ellipse 900px 1200px at 50% 40%, #1B9C8A 0%, #11796B 58%, #0A544B 100%);"""


def presenter(p, framing, start, dur, extra="", dx=0):
    """Gasi vor der Studio-Wand. framing: medium | close | top"""
    geo = {
        "medium": "width: 820px; left: 130px; top: 220px;",
        "close": "width: 1300px; left: -110px; top: -290px;",
        "top": "width: 1100px; left: -10px; top: -60px;",
    }[framing]
    return f"""
    <div id="{p}" class="clip shot" data-start="{start}" data-duration="{dur}" style="{PRESENTER_BG}">
      <div id="{p}-cam" class="cam">
        <div class="gasi" style="position:absolute; {geo} margin-left:{dx}px;">{gasi(p)}</div>
        {extra}
      </div>
    </div>"""


def label(id_, text, x, y, lx2=None, ly2=None, color=PET, size=46, anchor="left"):
    line = ""
    if lx2 is not None:
        line = f'<svg class="leader" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;overflow:visible"><line id="{id_}-ln" x1="{x}" y1="{y}" x2="{lx2}" y2="{ly2}" stroke="{color}" stroke-width="6" stroke-linecap="round"/><circle id="{id_}-dot" cx="{lx2}" cy="{ly2}" r="12" fill="{color}"/></svg>'
    tx = f"left:{x - 20}px;" if anchor == "left" else f"right:{W - x - 20}px;"
    return f"""{line}<div id="{id_}" class="tag" style="{tx} top:{y - 44}px; background:{color}; font-size:{size}px">{text}</div>"""


def scene_file(cid, dur, inner, script, style=""):
    newdur = NEWDUR.get(cid, dur); k = newdur / dur
    if abs(k - 1) > 1e-6:
        inner = re.sub(r'data-(start|duration)="([0-9.]+)"', lambda m: f'data-{m.group(1)}="{float(m.group(2)) * k:.3f}"', inner)
    script = script.replace("tl.", "tli.").replace("TLM.", "tl.")
    script = "    const tli = gsap.timeline();\n" + script + f"\n    tli.timeScale({1 / k:.5f});\n    tl.add(tli, 0);\n"
    dur = newdur
    return f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: Montserrat, sans-serif; }}
    #root .shot {{ position: absolute; inset: 0; overflow: hidden; }}
    #root .cam {{ position: absolute; inset: 0; }}
    #root .gasi-svg {{ width: 100%; height: auto; display: block; overflow: visible; }}
    #root .tag {{ position: absolute; color: #fff; font-weight: 800; padding: 14px 26px; border-radius: 18px; white-space: nowrap; letter-spacing: 0.5px; line-height: 1.1; box-shadow: 0 8px 0 rgba(0,0,0,0.18); }}
    {style}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}" data-duration="{dur}">
{inner}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{script}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


def push(sel, t, d, a=1.0, b=1.06, origin="50% 45%"):
    return f'tl.fromTo("{sel}", {{ scale: {a}, transformOrigin: "{origin}" }}, {{ scale: {b}, duration: {d}, ease: "none" }}, {t});\n'


def pop(sel, t, from_scale=0.3, d=0.45, ease="back.out(2.2)"):
    return (f'tl.fromTo("{sel}", {{ opacity: 0, scale: {from_scale} }}, '
            f'{{ opacity: 1, scale: 1, duration: {d}, ease: "{ease}" }}, {t});\n')


def draw(sel, t, d, length=2000):
    return (f'tl.fromTo("{sel}", {{ strokeDasharray: {length}, strokeDashoffset: {length} }}, '
            f'{{ strokeDashoffset: 0, duration: {d}, ease: "power2.inOut" }}, {t});\n')


# ---------------------------------------------------------------- Szene 1
def sc1():
    CUR["scene"] = "sc1"
    off = AUDIO_START
    trees = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="#4E6B34"/><circle cx="{x-r*0.4}" cy="{y-r*0.3}" r="{r*0.55}" fill="#6B8A45"/>'
        for x, y, r in [(90, 300, 60), (170, 380, 46), (950, 520, 70), (880, 640, 44), (120, 1500, 66), (980, 1300, 52), (60, 2300, 70), (960, 2500, 60), (150, 3000, 50)])
    stripesL = "".join(f'<line x1="0" y1="{y}" x2="350" y2="{y+120}" stroke="#C9A24A" stroke-width="10"/>' for y in range(-200, 3400, 60))
    stripesR = "".join(f'<line x1="730" y1="{y}" x2="1080" y2="{y-90}" stroke="#7E9450" stroke-width="10"/>' for y in range(-200, 3400, 56))
    dashes = "".join(f'<rect x="533" y="{y}" width="14" height="70" rx="4" fill="#F4F1E8"/>' for y in range(-200, 3400, 150))
    van = f"""
      <svg id="sc1-van" viewBox="0 0 260 560" style="position:absolute; left:410px; top:760px; width:260px; height:560px; overflow:visible">
        <rect x="14" y="40" width="232" height="510" rx="36" fill="#000" opacity="0.18" transform="translate(12 14)"/>
        <rect x="14" y="30" width="232" height="510" rx="36" fill="#F5F4F0" stroke="{INK}" stroke-width="6"/>
        <path d="M30 70 Q130 10 230 70 L222 130 Q130 104 38 130 Z" fill="#33424D" stroke="{INK}" stroke-width="5"/>
        <rect x="0" y="120" width="18" height="30" rx="6" fill="{INK}"/><rect x="242" y="120" width="18" height="30" rx="6" fill="{INK}"/>
        <rect x="60" y="200" width="140" height="150" rx="8" fill="#29507A" stroke="{INK}" stroke-width="5"/>
        <line x1="130" y1="200" x2="130" y2="350" stroke="#7FA6CC" stroke-width="4"/><line x1="60" y1="275" x2="200" y2="275" stroke="#7FA6CC" stroke-width="4"/>
        <rect x="90" y="390" width="80" height="80" rx="10" fill="#DADCD8" stroke="{INK}" stroke-width="5"/>
        <rect x="18" y="480" width="224" height="16" fill="{OR}"/>
      </svg>"""
    inner = f"""
    <div id="sc1-a" class="clip shot" data-start="0" data-duration="2.75" style="background:#B9944A">
      <div id="sc1-a-cam" class="cam">
        <svg id="sc1-world" viewBox="0 0 1080 3400" style="position:absolute;left:0;top:-1480px;width:1080px;height:3400px">
          <rect x="0" y="0" width="360" height="3400" fill="#D9B65A"/>{stripesL}
          <rect x="720" y="0" width="360" height="3400" fill="#93AA5C"/>{stripesR}
          <rect x="340" y="0" width="400" height="3400" fill="#7E848A"/>
          <rect x="340" y="0" width="22" height="3400" fill="#A6AAA9"/><rect x="718" y="0" width="22" height="3400" fill="#A6AAA9"/>
          {dashes}{trees}
        </svg>
        {van}
      </div>
      <div id="sc1-hook" style="position:absolute; left:110px; right:200px; top:330px; text-align:center">
        <div id="sc1-hook-1" style="display:inline-block; background:{PET}; color:#fff; font-weight:900; font-size:72px; line-height:1.08; padding:24px 34px; border-radius:26px; box-shadow:0 12px 0 rgba(0,0,0,.2)">Tankflasche an die<br>Autogas&#8209;Zapfsäule?</div>
      </div>
    </div>
    {presenter("sc1-g", "medium", 2.75, 2.85, label("sc1-ok", "✓ OFFIZIELL<br>ERLAUBT", 140, 640, color=OR, size=46), dx=90)}
"""
    s = ""
    s += 'tl.fromTo("#sc1-world", { y: 0 }, { y: 900, duration: 2.75, ease: "none" }, 0);\n'
    s += 'tl.fromTo("#sc1-van", { x: -6, rotation: -1 }, { x: 6, rotation: 1, duration: 0.7, ease: "sine.inOut", yoyo: true, repeat: 3 }, 0);\n'
    s += 'tl.fromTo("#sc1-hook-1", { scale: 0.92, opacity: 1 }, { scale: 1, duration: 0.5, ease: "back.out(2)" }, 0);\n'
    s += push("#sc1-g-cam", 2.75, 2.85, 1.0, 1.05)
    s += pop("#sc1-ok", 4.55, 0.2, 0.5, "back.out(2.6)")
    s += 'tl.fromTo("#sc1-ok", { rotation: -14 }, { rotation: -6, duration: 0.5, ease: "back.out(2.6)" }, 4.55);\n'
    s += gasi_rig_js("sc1-g", off, ENV["s1"], blinks=(3.4, 5.2),
                     gestures=[("R", -62, 4.4, 0.35), ("R", 0, 5.3, 0.3)], look_keys=[(10, -6, 4.5)], brows=[(-12, 4.4), (0, 5.3)])
    return scene_file("sc1", 5.6, inner, s)


# ---------------------------------------------------------------- Szene 2
def sc2():
    CUR["scene"] = "sc2"
    off = AUDIO_START
    pump = f"""
    <div id="sc2-a" class="clip shot" data-start="0" data-duration="1.0" style="background:#E9ECEE">
      <div id="sc2-a-cam" class="cam">
        <div style="position:absolute;left:90px;top:300px;width:900px;height:1080px;background:#fff;border:7px solid {INK};border-radius:30px"></div>
        <div style="position:absolute;left:150px;top:350px;width:780px;height:120px;background:{PET};border-radius:16px;color:#fff;font-weight:900;font-size:70px;text-align:center;line-height:120px;letter-spacing:6px">AUTOGAS · LPG</div>
        {''.join(f'<div style="position:absolute;left:170px;top:{t}px;width:520px;height:150px;background:#1E2A22;border-radius:12px;border:6px solid {INK}"></div><div id="sc2-d{i}" style="position:absolute;left:190px;top:{t+18}px;width:480px;text-align:right;font-family:JetBrains Mono, monospace;font-size:96px;color:#9CF07E;font-weight:700">0,00</div><div style="position:absolute;left:715px;top:{t+38}px;font-size:66px;font-weight:800;color:{INK}">{u}</div>' for i, (t, u) in enumerate([(540, "€"), (740, "Liter")]))}
        <div style="position:absolute;left:650px;top:980px;width:280px;height:280px;border-radius:50%;border:12px solid {PET};color:{PET};font-weight:900;font-size:46px;text-align:center;line-height:1.1;padding-top:84px">GEPRÜFT<br>LPG</div>
      </div>
    </div>"""
    sheet = f"""<div id="sc2-sheet" style="position:absolute;left:690px;top:560px;width:350px;height:500px;background:#fff;border:7px solid {INK};border-radius:16px;box-shadow:0 14px 0 rgba(0,0,0,.18);padding:34px">
        <div style="font-weight:900;font-size:84px;color:{PET};line-height:1">G 607</div>
        <div style="font-weight:800;font-size:30px;color:{INK};margin-top:14px">Einbau von Tankflaschen</div>
        {''.join(f'<div style="height:16px;background:#D6DADD;border-radius:8px;margin-top:22px;width:{w}%"></div>' for w in (92, 80, 88, 60, 84))}
      </div>"""
    inner = pump + presenter("sc2-g", "medium", 1.0, 3.2, sheet)
    s = push("#sc2-a-cam", 0, 1.0, 1.04, 1.1)
    s += 'tl.to({v:0}, { v: 1, duration: 1.0, ease: "power1.inOut", onUpdate: function(){ const v = this.targets()[0].v; const d0 = document.getElementById("sc2-d0"), d1 = document.getElementById("sc2-d1"); if (d0) d0.textContent = (v*24.37).toFixed(2).replace(".", ","); if (d1) d1.textContent = (v*31.2).toFixed(2).replace(".", ","); } }, 0);\n'
    s += push("#sc2-g-cam", 1.0, 3.2, 1.0, 1.05)
    s += 'tl.fromTo("#sc2-sheet", { y: 700, rotation: 18, opacity: 0 }, { y: 0, rotation: -6, opacity: 1, duration: 0.55, ease: "back.out(1.5)" }, 2.3);\n'
    s += gasi_rig_js("sc2-g", off, ENV["s2"], blinks=(1.6, 3.6), gestures=[("R", -38, 2.3, 0.55)],
                     look_keys=[(14, 10, 2.5), (0, 0, 3.3)], brows=[(-10, 1.1), (0, 2.0)])
    return scene_file("sc2", 4.2, inner, s)


# ---------------------------------------------------------------- Szene 3
def sc3():
    CUR["scene"] = "sc3"
    off = AUDIO_START
    wing = f"""<svg id="sc3-wing" viewBox="-110 -60 220 120" style="position:absolute;left:740px;top:844px;width:260px;height:142px;overflow:visible">
        <path d="M-20 -14 C -70 -60 -110 -40 -100 -6 C -94 20 -50 18 -20 12 Z" fill="#C7CCD1" stroke="{INK}" stroke-width="6"/>
        <path d="M20 -14 C 70 -60 110 -40 100 -6 C 94 20 50 18 20 12 Z" fill="#C7CCD1" stroke="{INK}" stroke-width="6"/>
        <circle cx="0" cy="0" r="28" fill="#A7AEB4" stroke="{INK}" stroke-width="6"/><circle cx="0" cy="0" r="9" fill="{INK}"/>
      </svg>"""
    hand = f"""<svg id="sc3-hand" viewBox="0 0 400 300" style="position:absolute;left:820px;top:794px;width:420px;height:315px;overflow:visible">
        <path d="M400 120 L170 120 Q120 120 110 150 L70 150 Q40 150 40 180 Q40 205 70 205 L200 205 L400 205 Z" fill="#fff" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
        <path d="M120 150 L120 120 Q120 80 160 80 L210 80 Q230 80 230 100 L230 120" fill="#fff" stroke="{INK}" stroke-width="7"/>
        <rect x="300" y="110" width="110" height="110" fill="{PET}" stroke="{INK}" stroke-width="7"/>
      </svg>"""
    seal = f"""<div id="sc3-seal" style="position:absolute;left:735px;top:780px;width:270px;height:270px;border-radius:50%;background:{OR};border:8px dashed #fff;outline:7px solid {INK};color:#fff;font-weight:900;font-size:40px;text-align:center;line-height:1.05;padding-top:92px;box-shadow:0 12px 0 rgba(0,0,0,.25)">VER&#8203;SIEGELT</div>"""
    box = f"""
    <div id="sc3-b" class="clip shot" data-start="1.0" data-duration="5.0" style="background:#2C3136">
      <div id="sc3-b-cam" class="cam">
        <div style="position:absolute;left:40px;top:250px;width:1000px;height:1350px;background:#3B4148;border:8px solid #1B1F23;border-radius:22px"></div>
        <div style="position:absolute;left:40px;top:1500px;width:1000px;height:100px;background:#4B525A"></div>
        <div style="position:absolute;width:640px;left:150px;top:380px">{gasi("sc3-k", look=(14, 8))}</div>
        <div id="sc3-strap" style="position:absolute;left:40px;top:880px;width:760px;height:70px;background:#15181B;border-top:6px solid #000;border-bottom:6px solid #000"></div>
        {wing}{hand}{seal}
        {label("sc3-l1", "✓ fest fixiert", 170, 400, size=50)}
        {label("sc3-l2", "Flügelschraube", 380, 1330, 830, 960, color=PET, size=48)}
      </div>
    </div>"""
    inner = presenter("sc3-g", "medium", 0, 1.0) + box
    s = push("#sc3-g-cam", 0, 1.0, 1.02, 1.06)
    s += push("#sc3-b-cam", 1.0, 5.0, 1.0, 1.07, "70% 55%")
    s += 'tl.fromTo("#sc3-strap", { scaleX: 0, transformOrigin: "100% 50%" }, { scaleX: 1, duration: 0.45, ease: "power3.out" }, 1.25);\n'
    s += pop("#sc3-wing", 1.5, 0.2, 0.4)
    s += pop("#sc3-l1", 2.35, 0.4, 0.4)
    s += 'tl.fromTo("#sc3-hand", { x: 500 }, { x: 0, duration: 0.45, ease: "power3.out" }, 3.05);\n'
    s += 'tl.to("#sc3-wing", { rotation: -200, transformOrigin: "50% 50%", duration: 0.9, ease: "power2.inOut" }, 3.45);\n'
    s += 'tl.to("#sc3-hand", { rotation: -24, transformOrigin: "20% 60%", duration: 0.9, ease: "power2.inOut" }, 3.45);\n'
    s += draw("#sc3-l2-ln", 3.5, 0.35, 600) + pop("#sc3-l2-dot", 3.5, 0, 0.3) + pop("#sc3-l2", 3.6, 0.4, 0.4)
    s += 'tl.to("#sc3-hand", { x: 520, duration: 0.35, ease: "power2.in" }, 4.55);\n'
    s += 'tl.fromTo("#sc3-seal", { opacity: 0, scale: 2.4, rotation: -30 }, { opacity: 1, scale: 1, rotation: -8, duration: 0.28, ease: "power4.in" }, 4.95);\n'
    s += 'tl.fromTo("#sc3-b-cam", { x: 0 }, { x: 14, duration: 0.05, yoyo: true, repeat: 3, ease: "none" }, 5.23);\n'
    s += gasi_rig_js("sc3-g", off, ENV["s3"], blinks=(0.6,), gestures=[("L", 40, 0.1, 0.35)])
    s += gasi_rig_js("sc3-k", off, ENV["s3"], blinks=(2.0, 4.3), look_keys=[(18, 14, 3.2), (6, -4, 5.0)], brows=[(-8, 5.0)])
    return scene_file("sc3", 6.0, inner, s)


# ---------------------------------------------------------------- Szene 4
def sc4():
    CUR["scene"] = "sc4"
    off = AUDIO_START
    side = f"""
    <div id="sc4-a" class="clip shot" data-start="0" data-duration="4.3" style="background:#E7EAEC">
      <div id="sc4-a-cam" class="cam">
        <div style="position:absolute;left:-40px;top:200px;width:1160px;height:1400px;background:#F6F7F7;border-top:8px solid #C9CED2"></div>
        <div style="position:absolute;left:-40px;top:520px;width:1160px;height:34px;background:{OR}"></div>
        <div style="position:absolute;left:-40px;top:568px;width:1160px;height:16px;background:{PET}"></div>
        <div style="position:absolute;left:-40px;top:1480px;width:1160px;height:120px;background:#9AA1A7"></div>
        <div style="position:absolute;left:300px;top:760px;width:420px;height:420px;border-radius:50%;background:#D9DDE0;border:8px solid #A9AFB4;box-shadow: inset 0 18px 30px rgba(0,0,0,.25)"></div>
        <div style="position:absolute;left:390px;top:850px;width:240px;height:240px;border-radius:50%;background:#C9A04A;border:10px solid #8E6E2A"></div>
        <div style="position:absolute;left:450px;top:910px;width:120px;height:120px;border-radius:50%;background:#5A4520;border:10px solid #E2C27A"></div>
        <svg id="sc4-noz" viewBox="0 0 700 400" style="position:absolute;left:520px;top:770px;width:700px;height:400px;overflow:visible">
          <rect x="0" y="150" width="120" height="100" rx="16" fill="#3B3F43" stroke="{INK}" stroke-width="7"/>
          <path d="M110 120 L420 120 Q470 120 480 170 L520 380 L430 380 L400 260 L110 280 Z" fill="{OR}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
          <path d="M200 280 Q260 360 360 330" fill="none" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>
          <path d="M480 160 L720 140" stroke="{INK}" stroke-width="44" stroke-linecap="round"/>
        </svg>
        {label("sc4-l1", "Füllanschluss außen", 90, 520 - 10 + 200, 420, 860, color=PET, size=50)}
      </div>
    </div>"""
    # Wohnmobil im Schnitt
    cut = f"""
    <div id="sc4-b" class="clip shot" data-start="4.3" data-duration="5.65" style="background:#DCEAF0">
      <div id="sc4-b-cam" class="cam">
        <div style="position:absolute;left:0;top:1160px;width:1080px;height:760px;background:#9BB063"></div>
        <svg viewBox="0 0 1080 1920" style="position:absolute;left:0;top:-170px;width:1080px;height:1920px;overflow:visible">
          <path d="M40 640 L860 640 Q900 640 930 700 L1030 900 L1040 1230 L40 1230 Z" fill="#FBFAF7" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>
          <path d="M880 700 L1000 920 L880 920 Z" fill="#9CC3D8" stroke="{INK}" stroke-width="7"/>
          <rect id="sc4-room" x="70" y="680" width="770" height="440" fill="#EAF2F5"/>
          <rect x="90" y="760" width="300" height="110" rx="14" fill="#C9D9E6" stroke="{INK}" stroke-width="6"/>
          <rect x="90" y="740" width="90" height="40" rx="12" fill="#fff" stroke="{INK}" stroke-width="5"/>
          <rect x="480" y="900" width="200" height="22" rx="8" fill="#B07A4A" stroke="{INK}" stroke-width="5"/>
          <rect x="570" y="922" width="22" height="160" fill="#B07A4A" stroke="{INK}" stroke-width="5"/>
          <rect x="700" y="960" width="120" height="130" rx="14" fill="#C9D9E6" stroke="{INK}" stroke-width="6"/>
          <text x="455" y="760" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="46" fill="#5C6B75">WOHNRAUM</text>
          <line x1="40" y1="1120" x2="1040" y2="1120" stroke="{INK}" stroke-width="8"/>
          <rect x="90" y="930" width="230" height="190" fill="#4B525A" stroke="{INK}" stroke-width="7"/>
          <rect x="40" y="1230" width="1000" height="20" fill="#5D646B"/>
          <circle cx="230" cy="1250" r="80" fill="#2B2F33" stroke="{INK}" stroke-width="8"/><circle cx="230" cy="1250" r="34" fill="#9AA1A7"/>
          <circle cx="840" cy="1250" r="80" fill="#2B2F33" stroke="{INK}" stroke-width="8"/><circle cx="840" cy="1250" r="34" fill="#9AA1A7"/>
          <circle cx="620" cy="1180" r="22" fill="#C9A04A" stroke="{INK}" stroke-width="6"/>
          <path id="sc4-bad" d="M620 1158 L620 860 L300 860 L240 960" fill="none" stroke="#D63A2F" stroke-width="16" stroke-dasharray="30 22" stroke-linecap="round" stroke-linejoin="round" opacity="0"/>
          <path id="sc4-good" d="M598 1180 L340 1180 Q300 1180 290 1140 L280 1100" fill="none" stroke="{PET}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
          <g id="sc4-x" opacity="0"><circle cx="455" cy="860" r="70" fill="#D63A2F" stroke="{INK}" stroke-width="7"/><path d="M425 830 L485 890 M485 830 L425 890" stroke="#fff" stroke-width="16" stroke-linecap="round"/></g>
          <g id="sc4-kup"><rect x="430" y="1155" width="80" height="50" rx="10" fill="{OR}" stroke="{INK}" stroke-width="6"/><circle cx="470" cy="1180" r="10" fill="#fff"/></g>
        </svg>
        <div style="position:absolute; width:150px; left:130px; top:765px">{gasi("sc4-m")}</div>
        {label("sc4-l2", "Sicherheitskupplung", 170, 360, 470, 985, color=OR, size=48)}
        {label("sc4-l3", "✓ unter dem Boden", 170, 460, color=PET, size=46)}
      </div>
    </div>"""
    inner = side + cut
    s = push("#sc4-a-cam", 0, 4.3, 1.0, 1.08, "45% 50%")
    s += 'tl.fromTo("#sc4-noz", { x: 640, y: -40, rotation: 8 }, { x: 0, y: 0, rotation: 0, duration: 0.7, ease: "power3.out" }, 1.0);\n'
    s += 'tl.fromTo("#sc4-noz", { scaleX: 1.06, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.25, ease: "back.out(3)" }, 1.7);\n'
    s += 'tl.fromTo("#sc4-a-cam", { y: 0 }, { y: 8, duration: 0.05, yoyo: true, repeat: 3, ease: "none" }, 1.7);\n'
    s += draw("#sc4-l1-ln", 2.35, 0.35, 700) + pop("#sc4-l1-dot", 2.35, 0, 0.3) + pop("#sc4-l1", 2.45, 0.4, 0.4)
    s += push("#sc4-b-cam", 4.3, 5.65, 1.0, 1.05, "50% 55%")
    s += draw("#sc4-good", 4.45, 0.8, 500)
    s += pop("#sc4-kup", 5.55, 0.1, 0.45)
    s += draw("#sc4-l2-ln", 5.75, 0.3, 500) + pop("#sc4-l2-dot", 5.75, 0, 0.3) + pop("#sc4-l2", 5.85, 0.4, 0.4)
    s += 'tl.set("#sc4-bad", { opacity: 1 }, 7.3);\n' + draw("#sc4-bad", 7.3, 0.7, 900)
    s += 'tl.set("#sc4-bad", { strokeDasharray: "30 22" }, 8.0);\n'
    s += 'tl.fromTo("#sc4-x", { opacity: 0, scale: 0.2, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.6)" }, 8.3);\n'
    s += 'tl.to("#sc4-bad", { opacity: 0.25, duration: 0.3 }, 8.9);\n'
    s += 'tl.to("#sc4-room", { fill: "#FBE1DC", duration: 0.3, yoyo: true, repeat: 1 }, 8.3);\n'
    s += pop("#sc4-l3", 8.5, 0.4, 0.4)
    s += 'tl.fromTo("#sc4-good", { strokeWidth: 18 }, { strokeWidth: 28, duration: 0.25, yoyo: true, repeat: 1, ease: "sine.inOut" }, 9.0);\n'
    s += gasi_rig_js("sc4-m", off, ENV["s4"], blinks=(5.0, 7.0), look_keys=[(16, 6, 4.6), (16, -14, 7.4), (0, 0, 9.0)])
    return scene_file("sc4", 9.95, inner, s)


# ---------------------------------------------------------------- Szene 5
def sc5():
    CUR["scene"] = "sc5"
    off = AUDIO_START
    ring = f"""<div id="sc5-ring" style="position:absolute;left:380px;top:-70px;width:320px;height:320px;border-radius:50%;border:14px solid {OR};"></div>
      {label("sc5-l1", "Sicherheitsventil", 150, 400, 420, 220, color=OR, size=52)}"""
    gauge_bottle = f"""
    <div id="sc5-b" class="clip shot" data-start="2.2" data-duration="2.95" style="background:#EEF1F3">
      <div id="sc5-b-cam" class="cam">
        <svg viewBox="0 0 400 760" style="position:absolute;left:200px;top:300px;width:680px;height:1292px;overflow:visible">
          <defs><clipPath id="sc5-clip"><path d="{BODY_PATH}"/></clipPath></defs>
          <path d="{BODY_PATH}" fill="#fff"/>
          <g clip-path="url(#sc5-clip)"><rect id="sc5-liq" x="0" y="150" width="400" height="600" fill="{PET}"/>
            <rect id="sc5-liq-top" x="0" y="150" width="400" height="14" fill="#3FB3A0"/></g>
          <path d="{BODY_PATH}" fill="none" stroke="#8E959C" stroke-width="16"/>
          <line x1="20" y1="260" x2="380" y2="260" stroke="{INK}" stroke-width="5" stroke-dasharray="16 12"/>
          <path d="M116 168 L124 52 L276 52 L284 168" fill="none" stroke="#8E959C" stroke-width="16" stroke-linejoin="round"/>
        </svg>
        <div id="sc5-pct" style="position:absolute;left:0;right:0;top:880px;text-align:center;font-weight:900;font-size:200px;color:#fff;-webkit-text-stroke:10px #232323;paint-order:stroke fill;">0 %</div>
        <div style="position:absolute;left:110px;top:688px;font-weight:900;font-size:56px;color:{INK}">80 %</div>
        <div id="sc5-stop" style="position:absolute;left:300px;top:380px;width:480px;height:160px;background:{OR};border:8px solid {INK};border-radius:24px;color:#fff;font-weight:900;font-size:110px;text-align:center;line-height:146px;box-shadow:0 12px 0 rgba(0,0,0,.2)">STOPP</div>
      </div>
    </div>"""
    inner = presenter("sc5-g", "top", 0, 2.2, ring) + gauge_bottle
    s = push("#sc5-g-cam", 0, 2.2, 1.0, 1.05, "50% 20%")
    s += pop("#sc5-ring", 0.55, 0.4, 0.45)
    s += 'tl.fromTo("#sc5-ring", { borderWidth: 14 }, { borderWidth: 22, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }, 1.0);\n'
    s += draw("#sc5-l1-ln", 0.8, 0.3, 600) + pop("#sc5-l1-dot", 0.8, 0, 0.3) + pop("#sc5-l1", 0.9, 0.4, 0.4)
    # Füllstand: y der Flüssigkeit von 712 (leer) bis 232 (80 %)
    s += 'tl.fromTo(["#sc5-liq", "#sc5-liq-top"], { attr: { y: 700 } }, { attr: { y: 260 }, duration: 1.85, ease: "power1.in" }, 2.35);\n'
    s += 'tl.to({v:0}, { v: 80, duration: 1.85, ease: "power1.in", onUpdate: function(){ const el = document.getElementById("sc5-pct"); if (el) el.textContent = Math.round(this.targets()[0].v) + " %"; } }, 2.35);\n'
    s += 'tl.fromTo("#sc5-stop", { opacity: 0, scale: 2.2, rotation: -16 }, { opacity: 1, scale: 1, rotation: -5, duration: 0.25, ease: "power4.in" }, 4.2);\n'
    s += 'tl.fromTo("#sc5-b-cam", { x: 0 }, { x: 12, duration: 0.05, yoyo: true, repeat: 3, ease: "none" }, 4.45);\n'
    s += gasi_rig_js("sc5-g", off, ENV["s5"], blinks=(1.5,), look_keys=[(4, -20, 0.4)], brows=[(-14, 0.4)])
    return scene_file("sc5", 5.15, inner, s)


# ---------------------------------------------------------------- Szene 6
def sc6():
    CUR["scene"] = "sc6"
    off = AUDIO_START
    field = f"""
    <div id="sc6-b" class="clip shot" data-start="1.5" data-duration="4.7" style="background:linear-gradient(#D7E6EE, #F3F6F8 70%)">
      <div id="sc6-b-cam" class="cam">
        <div style="position:absolute;left:-40px;top:600px;width:1160px;height:70px;background:{PET};border-bottom:10px solid #0B5E53"></div>
        <div style="position:absolute;left:60px;top:670px;width:40px;height:540px;background:#C9CED3;border:5px solid {INK}"></div><div style="position:absolute;left:980px;top:670px;width:40px;height:540px;background:#C9CED3;border:5px solid {INK}"></div>
        <div style="position:absolute;left:770px;top:860px;width:190px;height:350px;background:#fff;border:6px solid {INK};border-radius:14px"></div>
        <div style="position:absolute;left:790px;top:880px;width:150px;height:56px;background:{PET};border-radius:8px;color:#fff;font-weight:900;font-size:36px;text-align:center;line-height:56px">LPG</div>
        <div style="position:absolute;left:800px;top:960px;width:130px;height:70px;background:#1E2A22;border-radius:8px"></div>

        <div style="position:absolute;left:0;top:1200px;width:1080px;height:720px;background:linear-gradient(#8E959B,#71787E)"></div><div style="position:absolute;left:0;top:1200px;width:1080px;height:10px;background:#B9BEC3"></div>
        <svg id="sc6-red" viewBox="0 0 300 720" style="position:absolute;left:230px;top:400px;width:390px;height:936px;overflow:visible">
          <ellipse cx="150" cy="708" rx="140" ry="16" fill="#000" opacity="0.2"/>
          <path d="M70 40 L230 40 L238 168 L62 168 Z" fill="#56632F" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
          <ellipse cx="150" cy="40" rx="80" ry="13" fill="#6E7B45" stroke="{INK}" stroke-width="6"/>
          <rect x="92" y="78" width="40" height="52" rx="16" fill="#E6EAE3" stroke="{INK}" stroke-width="5"/><rect x="168" y="78" width="40" height="52" rx="16" fill="#E6EAE3" stroke="{INK}" stroke-width="5"/>
          <rect x="136" y="60" width="28" height="60" rx="5" fill="#9AA1A7" stroke="{INK}" stroke-width="5"/>
          <path d="M150 160 C 70 160 30 196 30 262 L30 640 Q30 680 70 680 L230 680 Q270 680 270 640 L270 262 C 270 196 230 160 150 160 Z" fill="#5B6935" stroke="{INK}" stroke-width="7"/>
          <path d="M62 250 L62 620" stroke="#7F8E52" stroke-width="18" stroke-linecap="round"/>
          <path d="M246 260 L246 620" stroke="#434E24" stroke-width="12" stroke-linecap="round"/>
          <text x="150" y="470" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="150" fill="#fff">π</text>
          <path d="M44 676 L256 676 L262 716 L38 716 Z" fill="#46512A" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
        </svg>
        <div id="sc6-ban" style="position:absolute;left:600px;top:300px;width:300px;height:300px;border-radius:50%;background:#fff;border:24px solid #D63A2F;box-shadow:0 12px 0 rgba(0,0,0,.2)">
          <svg viewBox="0 0 300 300" style="position:absolute;left:0;top:0;width:252px;height:252px">
            <path d="M70 110 L190 110 Q215 110 220 135 L235 230 L195 230 L185 170 L70 175 Z" fill="{OR}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
            <rect x="40" y="120" width="40" height="45" rx="8" fill="#3B3F43" stroke="{INK}" stroke-width="6"/>
            <line x1="40" y1="40" x2="250" y2="250" stroke="#D63A2F" stroke-width="26" stroke-linecap="round"/>
          </svg>
        </div>
      </div>
    </div>"""
    logo = f"""<div id="sc6-logo" style="position:absolute;left:40px;top:300px;display:flex;align-items:center;gap:22px;background:#fff;border:6px solid {INK};border-radius:28px;padding:18px 32px;box-shadow:0 10px 0 rgba(0,0,0,.16)">
        <img src="assets/brand/icon.png" style="width:110px;height:110px"/><div style="font-weight:900;font-size:58px;color:{INK};line-height:1">Die<br>Gasfachfrau</div></div>"""
    inner = (presenter("sc6-g", "medium", 0, 1.5) + field + presenter("sc6-c", "close", 6.2, 2.8)
             + presenter("sc6-d", "medium", 9.0, 2.4, logo))
    s = push("#sc6-g-cam", 0, 1.5, 1.0, 1.06)
    s += push("#sc6-b-cam", 1.5, 4.7, 1.0, 1.06, "50% 60%")
    s += 'tl.fromTo("#sc6-ban", { opacity: 0, scale: 2.4, rotation: -40 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.3, ease: "power4.in" }, 3.35);\n'
    s += 'tl.fromTo("#sc6-red", { x: 0 }, { x: -10, duration: 0.06, yoyo: true, repeat: 5, ease: "none" }, 3.65);\n'
    s += push("#sc6-c-cam", 6.2, 2.8, 1.0, 1.05)
    s += push("#sc6-d-cam", 9.0, 2.4, 1.0, 1.04)
    s += pop("#sc6-logo", 9.05, 0.3, 0.5)
    s += gasi_rig_js("sc6-g", off, ENV["s6"], blinks=(1.1,), gestures=[("R", -70, 0.1, 0.35)], brows=[(-14, 0.1)])
    s += gasi_rig_js("sc6-c", off, ENV["s6"], blinks=(7.0, 8.6), gestures=[("L", 30, 6.3, 0.4), ("R", -30, 6.35, 0.4)],
                     look_keys=[(-8, 4, 6.3)], brows=[(-16, 6.3)])
    s += gasi_rig_js("sc6-d", off, ENV["s6"], blinks=(10.2,), gestures=[("R", -120, 9.1, 0.35), ("R", -95, 9.5, 0.2), ("R", -125, 9.7, 0.2), ("R", -95, 9.9, 0.2), ("R", -120, 10.1, 0.2)],
                     look_keys=[(-14, -10, 9.1), (0, 0, 10.4)])
    return scene_file("sc6", 11.4, inner, s)


# ---------------------------------------------------------------- Abspann
def end():
    inner = f"""
    <div id="end-a" class="clip shot" data-start="0" data-duration="5.0" style="background:#fff">
      <div id="end-cam" class="cam">
        <img id="end-icon" src="assets/brand/icon.png" style="position:absolute;left:400px;top:320px;width:280px;height:280px"/>
        <div id="end-name" style="position:absolute;left:0;right:0;top:640px;text-align:center;font-weight:900;font-size:84px;color:{INK};letter-spacing:-2px">Die Gasfachfrau</div>
        <div id="end-sub" style="position:absolute;left:0;right:0;top:752px;text-align:center;font-weight:700;font-size:40px;color:{PET}">Tankflaschen · Einbau · Beratung</div>
        <div id="end-qrbox" style="position:absolute;left:330px;top:850px;width:420px;height:420px;background:#fff;border:8px solid {INK};border-radius:28px;padding:18px">
          <img src="assets/brand/qr-gasfachfrau.png" style="width:100%;height:100%"/></div>
        <div id="end-url" style="position:absolute;left:0;right:0;top:1300px;text-align:center;font-weight:800;font-size:58px;color:{OR}">gasfachfrau.de</div>
      </div>
    </div>"""
    s = 'tl.fromTo("#end-icon", { opacity: 0, scale: 0.5, rotation: -90 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.7, ease: "back.out(1.7)" }, 0.05);\n'
    s += 'tl.fromTo("#end-name", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 0.4);\n'
    s += 'tl.fromTo("#end-sub", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.out" }, 0.65);\n'
    s += 'tl.fromTo("#end-qrbox", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.8)" }, 0.85);\n'
    s += 'tl.fromTo("#end-url", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 1.1);\n'
    return scene_file("end", 5.0, inner, s)


# ---------------------------------------------------------------- Untertitel
def captions():
    groups, s = "", ""
    for i, (text, a, b) in enumerate(CAPTIONS):
        nxt = CAPTIONS[i + 1][1] if i + 1 < len(CAPTIONS) else None
        if nxt is not None and nxt - b < 0.5:
            b = nxt - 0.09
        b = round(b + 0.08, 2) if nxt is None or b + 0.08 < nxt - 0.1 else round(b, 2)
        groups += f'    <div id="cap{i}" class="cap"><span>{text}</span></div>\n'
        s += f'tl.set("#cap{i}", {{ opacity: 1, visibility: "visible" }}, {round(a - 0.05, 2)});\n'
        s += f'tl.set("#cap{i}", {{ opacity: 0, visibility: "hidden" }}, {b});\n'
    style = """#root .cap { position: absolute; left: 120px; right: 192px; top: 1110px; text-align: center; opacity: 0; visibility: hidden; }
    #root .cap span { display: inline-block; background: rgba(20,20,20,0.62); color: #fff; font-family: Inter, sans-serif; font-weight: 700; font-size: 42px; line-height: 1.22; padding: 10px 20px; border-radius: 12px; max-width: 768px; }"""
    return scene_file("captions", TOTAL, groups, s, style)


# ---------------------------------------------------------------- Wurzel
def index():
    hosts = ""
    for cid, st, du, _ in SCENES:
        hosts += f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{st}" data-duration="{du}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>\n'
    hosts += f'      <div id="brand" class="clip" data-start="0" data-duration="{START["end"]}" data-track-index="4" style="position:absolute; left:0; right:0; top:1700px; text-align:center; z-index:50;"><div style="display:inline-flex; align-items:center; gap:14px; background:rgba(255,255,255,0.94); border-radius:60px; padding:12px 40px 12px 16px; box-shadow:0 6px 18px rgba(0,0,0,0.2);"><img src="assets/brand/icon.png" style="width:84px; height:84px"/><span style="font-family:Montserrat, sans-serif; font-weight:800; font-size:54px; color:#232323; letter-spacing:0.3px">gasfachfrau.de</span></div></div>\n'
    hosts += f'      <audio id="vo" class="clip" src="{AUDIO}" data-start="{AUDIO_START}" data-duration="{AUDIO_DUR:.3f}" data-track-index="3" data-volume="0.8"></audio>\n'
    return f"""<!doctype html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #fff; }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: Montserrat, sans-serif; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
{hosts}    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
    files = {"sc1": sc1(), "sc2": sc2(), "sc3": sc3(), "sc4": sc4(), "sc5": sc5(), "sc6": sc6(), "end": end(), "captions": captions()}
    for k, v in files.items():
        open(os.path.join(ROOT, "compositions", f"{k}.html"), "w", encoding="utf-8").write(v)
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(index())
    print("ok:", ", ".join(files))
