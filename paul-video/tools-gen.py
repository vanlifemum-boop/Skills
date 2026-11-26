#!/usr/bin/env python3
"""Generates the PAUL HyperFrames compositions (run once; afterwards edit the HTML directly)."""
import math, os, json

OUT = "/home/user/Skills/paul-video"
NAVY, ORANGE, RED, SKY = "#1B2452", "#F07A2E", "#E3262E", "#E8F2F6"

# ---------------------------------------------------------------- shared art
def paul_svg(p, extra_style=""):
    ribs = lambda x: "".join(
        f'<line x1="{x+6}" y1="{y}" x2="{x+38}" y2="{y}" stroke="#3B3B41" stroke-width="4" stroke-linecap="round"/>'
        for y in range(96, 300, 22))
    strap = lambda x1, y1, x2, y2: (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#141416" stroke-width="26" stroke-linecap="round"/>'
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#3A3A40" stroke-width="2" stroke-dasharray="7 7"/>')
    return f'''<svg id="{p}" class="paul" viewBox="-160 -40 720 480" overflow="visible" style="{extra_style}">
  <defs><linearGradient id="{p}-alu" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#F5F7F9"/><stop offset=".42" stop-color="#C4CBD2"/>
    <stop offset=".55" stop-color="#E1E5E9"/><stop offset="1" stop-color="#A7B0B8"/></linearGradient></defs>
  <g id="{p}-body">
    <g id="{p}-armL">{strap(66,210,-20,282)}
      <g id="{p}-foreL">{strap(-20,282,-52,380)}
        <rect x="-74" y="368" width="44" height="26" rx="6" fill="none" stroke="#D3D9DE" stroke-width="7"/></g></g>
    <g id="{p}-armR">{strap(334,210,420,282)}
      <g id="{p}-foreR">{strap(420,282,452,380)}
        <g transform="translate(452 384)"><rect x="-30" y="-18" width="60" height="42" rx="7" fill="#D7DDE2" stroke="#7F8890" stroke-width="3"/>
        <rect x="-22" y="-8" width="44" height="14" rx="4" fill="#F1F3F5" stroke="#8E979F" stroke-width="2"/>
        <circle cx="0" cy="14" r="4" fill="#7F8890"/></g></g></g>
    <rect x="54" y="72" width="46" height="250" rx="17" fill="#202024"/>{ribs(54)}
    <rect x="300" y="72" width="46" height="250" rx="17" fill="#202024"/>{ribs(300)}
    <rect x="92" y="88" width="216" height="218" rx="12" fill="url(#{p}-alu)" stroke="#8E979F" stroke-width="3"/>
    <g opacity=".35" stroke="#FFFFFF" stroke-width="2"><line x1="104" y1="104" x2="296" y2="104"/><line x1="104" y1="292" x2="296" y2="292"/></g>
    <rect id="{p}-shine" x="60" y="88" width="34" height="218" fill="#FFFFFF" opacity="0" transform="skewX(-18)"/>
    <g fill="#6B737B" stroke="#FFFFFF" stroke-width="1.5"><circle cx="122" cy="118" r="8"/><circle cx="278" cy="118" r="8"/><circle cx="122" cy="276" r="8"/><circle cx="278" cy="276" r="8"/></g>
    <circle cx="136" cy="230" r="13" fill="{ORANGE}" opacity=".35"/><circle cx="264" cy="230" r="13" fill="{ORANGE}" opacity=".35"/>
    <g id="{p}-eyes">
      <ellipse cx="164" cy="176" rx="31" ry="37" fill="#FFFFFF" stroke="{NAVY}" stroke-width="5"/>
      <ellipse cx="236" cy="176" rx="31" ry="37" fill="#FFFFFF" stroke="{NAVY}" stroke-width="5"/>
      <g id="{p}-pupils"><circle cx="167" cy="182" r="15" fill="{NAVY}"/><circle cx="239" cy="182" r="15" fill="{NAVY}"/>
        <circle cx="172" cy="176" r="5" fill="#FFFFFF"/><circle cx="244" cy="176" r="5" fill="#FFFFFF"/></g></g>
    <path id="{p}-smile" d="M172 244 Q200 270 228 244" fill="none" stroke="{NAVY}" stroke-width="7" stroke-linecap="round"/>
    <g id="{p}-talk" opacity="0"><ellipse cx="200" cy="252" rx="22" ry="17" fill="{NAVY}"/><ellipse cx="200" cy="261" rx="12" ry="6" fill="{ORANGE}"/></g>
  </g></svg>'''

def bottle_svg(bid, strap=False, w=260, strap_hidden=False):
    s = ""
    if strap:
        s = f'''<g id="{bid}-strap" opacity="{0 if strap_hidden else 1}"><rect x="34" y="250" width="232" height="30" fill="#141416"/>
      <rect x="34" y="263" width="232" height="2" fill="#3A3A40"/>
      <g transform="translate(150 265)"><rect x="-40" y="-24" width="80" height="48" rx="7" fill="#D7DDE2" stroke="#7F8890" stroke-width="3"/>
      <rect x="-30" y="-10" width="60" height="18" rx="4" fill="#F1F3F5" stroke="#8E979F" stroke-width="2"/></g></g>'''
    return f'''<svg id="{bid}" viewBox="0 0 300 540" width="{w}" overflow="visible">
  <defs><linearGradient id="{bid}-g" x1="0" x2="1"><stop offset="0" stop-color="#A9B1B8"/><stop offset=".3" stop-color="#E4E8EB"/><stop offset="1" stop-color="#9AA3AB"/></linearGradient></defs>
  <path d="M88 112 L66 30 L98 20 L122 104Z" fill="#BCC3CA" stroke="#8E979F" stroke-width="3"/>
  <path d="M212 112 L234 30 L202 20 L178 104Z" fill="#BCC3CA" stroke="#8E979F" stroke-width="3"/>
  <rect x="139" y="30" width="22" height="52" fill="#C79A3A"/><rect x="124" y="18" width="52" height="15" rx="5" fill="#A87C25"/>
  <path d="M40 210 Q40 96 150 96 Q260 96 260 210 L260 474 Q260 512 222 514 L78 514 Q40 512 40 474Z" fill="url(#{bid}-g)" stroke="#8E979F" stroke-width="3"/>
  <ellipse cx="150" cy="96" rx="50" ry="16" fill="#2FA34A"/>
  <rect x="41" y="360" width="218" height="52" fill="{RED}"/>
  <line x1="41" y1="318" x2="259" y2="318" stroke="#9AA3AB" stroke-width="3"/><line x1="41" y1="470" x2="259" y2="470" stroke="#9AA3AB" stroke-width="3"/>
  <rect x="68" y="150" width="18" height="300" rx="9" fill="#FFFFFF" opacity=".35"/>
  <circle cx="150" cy="494" r="7" fill="#596168"/>{s}
</svg>'''

def caravan_svg(cid, w=420):
    return f'''<svg id="{cid}" viewBox="0 0 440 240" width="{w}" overflow="visible">
  <line x1="355" y1="168" x2="430" y2="182" stroke="{NAVY}" stroke-width="8" stroke-linecap="round"/>
  <rect x="20" y="28" width="340" height="152" rx="42" fill="#FFFFFF" stroke="{NAVY}" stroke-width="6"/>
  <rect x="58" y="60" width="118" height="56" rx="14" fill="{NAVY}"/><rect x="222" y="60" width="52" height="104" rx="9" fill="none" stroke="{NAVY}" stroke-width="5"/>
  <rect x="22" y="134" width="336" height="14" fill="{ORANGE}"/><rect x="300" y="66" width="36" height="30" rx="6" fill="#D7DDE2" stroke="{NAVY}" stroke-width="4"/>
  <circle cx="190" cy="186" r="30" fill="{NAVY}"/><circle cx="190" cy="186" r="11" fill="#D7DDE2"/>
</svg>'''

def buckle_big(bid):
    return f'''<svg id="{bid}" viewBox="0 0 600 420" width="600" overflow="visible">
  <rect x="0" y="170" width="140" height="70" fill="#141416"/><rect x="460" y="170" width="140" height="70" fill="#141416"/>
  <rect x="0" y="203" width="140" height="3" fill="#3A3A40"/><rect x="460" y="203" width="140" height="3" fill="#3A3A40"/>
  <rect x="120" y="130" width="360" height="150" rx="18" fill="#CDD4DA" stroke="#77808A" stroke-width="5"/>
  <circle cx="170" cy="205" r="12" fill="#8E979F"/><circle cx="430" cy="205" r="12" fill="#8E979F"/>
  <g id="{bid}-eye"><rect x="270" y="262" width="60" height="60" rx="10" fill="none" stroke="#9AA3AB" stroke-width="14"/></g>
  <g id="{bid}-lever"><rect x="150" y="150" width="300" height="70" rx="14" fill="#EEF1F3" stroke="#77808A" stroke-width="5"/>
    <rect x="180" y="172" width="240" height="10" rx="5" fill="#C4CBD2"/><circle cx="160" cy="185" r="16" fill="#9AA3AB"/></g>
</svg>'''

def padlock(pid):
    return f'''<svg id="{pid}" viewBox="0 0 200 260" width="190" overflow="visible">
  <path id="{pid}-shackle" d="M50 120 L50 70 Q50 18 100 18 Q150 18 150 70 L150 120" fill="none" stroke="#C4CBD2" stroke-width="22" stroke-linecap="round"/>
  <rect x="20" y="110" width="160" height="140" rx="22" fill="{NAVY}"/><circle cx="100" cy="170" r="16" fill="{ORANGE}"/><rect x="93" y="176" width="14" height="36" rx="5" fill="{ORANGE}"/>
</svg>'''

def screw(sid, x, y):
    return f'''<svg id="{sid}" viewBox="0 0 80 200" width="70" style="position:absolute;left:{x}px;top:{y}px" overflow="visible">
  <rect x="4" y="0" width="72" height="26" rx="8" fill="#C4CBD2" stroke="#77808A" stroke-width="3"/><line x1="40" y1="4" x2="40" y2="22" stroke="#77808A" stroke-width="5"/>
  <path d="M28 26 L52 26 L50 170 L40 196 L30 170Z" fill="#B9C1C8" stroke="#77808A" stroke-width="3"/>
  <g stroke="#77808A" stroke-width="3">{"".join(f'<line x1="26" y1="{yy}" x2="54" y2="{yy+10}"/>' for yy in range(40,170,16))}</g></svg>'''

# --------------------------------------------------------------- animation helpers
def talk(p, windows):
    js = []
    for (a, b) in windows:
        js.append(f'tl.set("#{p}-talk",{{opacity:1}},{a:.2f});tl.set("#{p}-smile",{{opacity:0}},{a:.2f});')
        t, i = a, 0
        while t < b - 0.05:
            v = 0.3 + 0.7 * abs(math.sin(i * 1.9 + a * 3.1))
            js.append(f'tl.to("#{p}-talk",{{scaleY:{v:.2f},duration:0.1,ease:"none",svgOrigin:"200 252"}},{t:.2f});')
            t += 0.11; i += 1
        js.append(f'tl.set("#{p}-talk",{{opacity:0}},{b:.2f});tl.set("#{p}-smile",{{opacity:1}},{b:.2f});')
    return "\n".join(js)

def blink(p, times):
    return "\n".join(
        f'tl.to("#{p}-eyes",{{scaleY:0.08,duration:0.06,ease:"power1.in",svgOrigin:"200 176"}},{t});'
        f'tl.to("#{p}-eyes",{{scaleY:1,duration:0.09,ease:"power1.out",svgOrigin:"200 176"}},{t+0.07:.2f});' for t in times)

def bob(p, start, dur, amp=7, period=0.7):
    n = max(1, int(dur / period) - 1)
    if n % 2 == 0: n -= 1
    return f'tl.fromTo("#{p}-body",{{y:0}},{{y:-{amp},duration:{period/1:.2f},ease:"sine.inOut",repeat:{n},yoyo:true}},{start});'

def wave(p, t, side="L", n=5):
    if side == "L":
        return (f'tl.to("#{p}-armL",{{rotation:128,svgOrigin:"66 210",duration:0.35,ease:"back.out(1.6)"}},{t});'
                f'tl.fromTo("#{p}-foreL",{{rotation:-20}},{{rotation:28,svgOrigin:"-20 282",duration:0.16,ease:"sine.inOut",repeat:{n},yoyo:true}},{t+0.1:.2f});'
                f'tl.to("#{p}-armL",{{rotation:0,svgOrigin:"66 210",duration:0.4,ease:"power2.inOut"}},{t+0.25+0.16*(n+1):.2f});'
                f'tl.to("#{p}-foreL",{{rotation:0,svgOrigin:"-20 282",duration:0.4,ease:"power2.inOut"}},{t+0.3+0.16*(n+1):.2f});')
    return (f'tl.to("#{p}-armR",{{rotation:-128,svgOrigin:"334 210",duration:0.35,ease:"back.out(1.6)"}},{t});'
            f'tl.fromTo("#{p}-foreR",{{rotation:20}},{{rotation:-28,svgOrigin:"420 282",duration:0.16,ease:"sine.inOut",repeat:{n},yoyo:true}},{t+0.1:.2f});'
            f'tl.to("#{p}-armR",{{rotation:0,svgOrigin:"334 210",duration:0.4,ease:"power2.inOut"}},{t+0.25+0.16*(n+1):.2f});'
            f'tl.to("#{p}-foreR",{{rotation:0,svgOrigin:"420 282",duration:0.4,ease:"power2.inOut"}},{t+0.3+0.16*(n+1):.2f});')

def rest_arms(p):
    return (f'tl.set("#{p}-armL",{{rotation:0,svgOrigin:"66 210"}},0);tl.set("#{p}-foreL",{{rotation:0,svgOrigin:"-20 282"}},0);'
            f'tl.set("#{p}-armR",{{rotation:0,svgOrigin:"334 210"}},0);tl.set("#{p}-foreR",{{rotation:0,svgOrigin:"420 282"}},0);'
            f'tl.set("#{p}-eyes",{{scaleY:1,svgOrigin:"200 176"}},0);tl.set("#{p}-talk",{{opacity:0,scaleY:1,svgOrigin:"200 252"}},0);tl.set("#{p}-smile",{{opacity:1}},0);')

BASE_CSS = f"""
    #root {{ position:absolute; inset:0; overflow:hidden; font-family:'Montserrat',sans-serif; color:{NAVY}; }}
    .abs {{ position:absolute; }}
    .thin {{ font-weight:300; letter-spacing:-0.01em; line-height:1; }}
    .heavy {{ font-weight:800; letter-spacing:-0.02em; line-height:0.95; }}
    .center {{ left:0; right:0; text-align:center; }}
    .paul {{ position:absolute; }}
    .sticker {{ filter: drop-shadow(0 18px 30px rgba(27,36,82,.22)); }}
"""

def scene(cid, dur, css, html, js, ground="#FFFFFF"):
    return f'''<template>
  <style>{BASE_CSS}
    #root {{ background:{ground}; }}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920" data-layout-allow-overflow>
{html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
'''

def write(name, s):
    os.makedirs(f"{OUT}/compositions", exist_ok=True)
    open(f"{OUT}/compositions/{name}.html", "w").write(s)

# ================================================================ S1 HOOK (8.6s)
s1_html = f'''
    <div id="s1-hook" class="abs center" style="top:300px">
      <div class="thin" style="font-size:78px">Rappelt's bei dir</div>
      <div class="heavy" style="font-size:112px;margin-top:10px">im GAS&shy;KASTEN?</div></div>
    <div id="s1-t2" class="abs center" style="top:300px;opacity:0">
      <div class="thin" style="font-size:78px">Vollbremsung –</div>
      <div class="heavy" style="font-size:140px;color:{RED};margin-top:10px">GESCHOSS!</div></div>
    <div id="s1-t3" class="abs center" style="top:300px;opacity:0">
      <div class="thin" style="font-size:78px">Das muss</div>
      <div class="heavy" style="font-size:140px;color:{ORANGE};margin-top:10px">NICHT SEIN.</div></div>
    <div id="s1-world" class="abs" style="left:0;top:0;width:1080px;height:1920px;z-index:1">
      <div id="s1-road" class="abs" style="left:-200px;top:1090px;width:1480px;height:14px;background:repeating-linear-gradient(90deg,{NAVY} 0 90px,transparent 90px 150px);opacity:.25"></div>
      <div id="s1-box" class="abs" style="left:270px;top:590px;width:540px;height:500px;border-radius:30px;background:#D9E6EC;border:10px solid {NAVY};box-shadow:inset 0 -26px 0 #C3D3DA"></div>
      <div id="s1-door" class="abs" style="left:800px;top:590px;width:40px;height:500px;border-radius:0 30px 30px 0;background:{ORANGE}"></div>
      <div id="s1-bottle" class="abs" style="left:410px;top:612px">{bottle_svg("s1-b", strap=False, w=260)}</div>
      <div id="s1-band" class="abs" style="left:410px;top:612px;width:260px;height:468px">
        <svg viewBox="0 0 300 540" width="260" overflow="visible"><g id="s1-bandg">
        <rect x="34" y="250" width="232" height="30" fill="#141416"/><g transform="translate(150 265)"><rect x="-40" y="-24" width="80" height="48" rx="7" fill="#D7DDE2" stroke="#7F8890" stroke-width="3"/>
        <rect x="-30" y="-10" width="60" height="18" rx="4" fill="#F1F3F5" stroke="#8E979F" stroke-width="2"/></g></g></svg></div>
    </div>
    <div id="s1-k1" class="abs heavy" style="left:150px;top:640px;font-size:58px;color:{ORANGE};transform:rotate(-14deg)">KLONK!</div>
    <div id="s1-k2" class="abs heavy" style="left:700px;top:760px;font-size:50px;color:{ORANGE};transform:rotate(12deg)">KLONK!</div>
    <div id="s1-lines" class="abs" style="left:60px;top:620px;width:340px;height:420px">
      <svg viewBox="0 0 340 420" width="340" overflow="visible"><g stroke="{RED}" stroke-width="12" stroke-linecap="round">
      <line x1="330" y1="60" x2="80" y2="120"/><line x1="330" y1="200" x2="30" y2="230"/><line x1="330" y1="340" x2="90" y2="330"/></g></svg></div>
    <div id="s1-wipe" class="abs" style="left:540px;top:900px;width:120px;height:120px;margin:-60px 0 0 -60px;border-radius:50%;background:{ORANGE};opacity:0;z-index:5"></div>
    <div class="abs" style="left:0;top:1104px;width:1080px;height:820px;background:#D3E3EA;z-index:0"></div>
'''
s1_js = f'''
tl.set("#s1-wipe",{{scale:0,opacity:1}},0.01); tl.set("#s1-band",{{opacity:0}},0); tl.set("#s1-lines",{{opacity:0}},0);
tl.set("#s1-k1",{{opacity:0}},0); tl.set("#s1-k2",{{opacity:0}},0);
// rattle (frame 0 already shows the hook)
tl.fromTo("#s1-bottle",{{rotation:-3,transformOrigin:"50% 100%"}},{{rotation:3,duration:0.09,ease:"sine.inOut",repeat:21,yoyo:true}},0);
tl.fromTo("#s1-world",{{x:0}},{{x:6,duration:0.11,ease:"sine.inOut",repeat:17,yoyo:true}},0);
tl.fromTo("#s1-k1",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.18,ease:"back.out(3)"}},0.35);
tl.to("#s1-k1",{{opacity:0,duration:0.2}},1.1);
tl.fromTo("#s1-k2",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.18,ease:"back.out(3)"}},1.0);
tl.to("#s1-k2",{{opacity:0,duration:0.2}},1.8);
// brake: world lurches right then stops hard, bottle keeps going
tl.to("#s1-hook",{{opacity:0,y:-40,duration:0.3,ease:"power2.in"}},2.35);
tl.fromTo("#s1-road",{{x:0}},{{x:-300,duration:0.5,ease:"power3.out"}},2.2);
tl.to("#s1-world",{{x:70,duration:0.18,ease:"power2.out"}},2.62);
tl.to("#s1-world",{{x:0,duration:0.5,ease:"elastic.out(1,0.4)"}},2.8);
tl.to("#s1-bottle",{{x:-250,y:-40,rotation:-70,duration:0.55,ease:"power3.out"}},2.7);
tl.fromTo("#s1-lines",{{opacity:0,x:120}},{{opacity:1,x:0,duration:0.25,ease:"power2.out"}},2.85);
tl.to("#s1-lines",{{opacity:0,duration:0.3}},4.2);
tl.fromTo("#s1-t2",{{opacity:0,scale:1.4}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"}},2.95);
tl.to("#s1-bottle",{{rotation:-76,duration:1.6,ease:"none"}},3.25);
// "Das muss nicht sein!": bottle snaps back upright, strap band clamps
tl.to("#s1-t2",{{opacity:0,y:-30,duration:0.25,ease:"power2.in"}},6.05);
tl.to("#s1-bottle",{{x:0,y:0,rotation:0,duration:0.45,ease:"back.out(1.4)"}},6.2);
tl.fromTo("#s1-band",{{opacity:0,scaleX:0.1,transformOrigin:"50% 50%"}},{{opacity:1,scaleX:1,duration:0.3,ease:"back.out(2)"}},6.6);
tl.fromTo("#s1-t3",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},6.35);
// wipe from the buckle into Paul's world
tl.set("#s1-wipe",{{left:540,top:841}},7.6);
tl.fromTo("#s1-wipe",{{scale:0}},{{scale:40,duration:0.75,ease:"power2.in"}},7.75);
'''
write("s1", scene("s1", 8.6, "", s1_html, s1_js, ground=SKY))

# ================================================================ S2 HI ICH BIN PAUL (6.0s)
s2_html = f'''
    <div id="s2-blobO" class="abs" style="left:540px;top:960px;width:3000px;height:3000px;margin:-1500px 0 0 -1500px;border-radius:50%;background:{ORANGE}"></div>
    <div id="s2-blobN" class="abs" style="left:640px;top:1250px;width:760px;height:620px;border-radius:48% 52% 40% 60%;background:{NAVY}"></div>
    <div id="s2-title" class="abs center" style="top:300px">
      <div class="thin" style="font-size:80px">Hi, ich bin</div>
      <div class="heavy" style="font-size:190px;margin-top:6px">PAUL.</div></div>
    <div id="s2-road" class="abs center" style="top:300px;opacity:0">
      <div id="s2-van" style="display:inline-block">{caravan_svg("s2-car", w=400)}</div>
      <div class="thin" style="font-size:44px;margin-top:4px">Wohnwagen · Wohnmobil · Anhänger</div></div>
    <div id="s2-paulwrap" class="abs" style="left:150px;top:600px;width:780px;height:520px">{paul_svg("s2p","left:0;top:0;width:780px;height:520px")}</div>
    <div id="s2-bottle" class="abs" style="left:440px;top:740px">{bottle_svg("s2-b", strap=True, w=200, strap_hidden=True)}</div>
'''
s2_js = f'''{rest_arms("s2p")}
tl.fromTo("#s2-blobO",{{scale:1}},{{scale:0.12,x:-520,y:-720,duration:0.6,ease:"power3.inOut"}},0);
tl.fromTo("#s2-blobN",{{scale:0,rotation:-20}},{{scale:1,rotation:0,duration:0.6,ease:"back.out(1.4)"}},0.3);
tl.fromTo("#s2-paulwrap",{{y:700,scaleY:1,scaleX:1}},{{y:0,duration:0.45,ease:"back.out(1.5)"}},0.12);
tl.fromTo("#s2-paulwrap",{{scaleY:0.82,scaleX:1.12,transformOrigin:"50% 100%"}},{{scaleY:1,scaleX:1,duration:0.5,ease:"elastic.out(1,0.45)"}},0.5);
tl.fromTo("#s2-title",{{opacity:0,y:50}},{{opacity:1,y:0,duration:0.45,ease:"power3.out"}},0.35);
{wave("s2p",0.45,"L",5)}
{talk("s2p",[(0.4,1.49),(1.76,3.33),(3.56,4.92)])}
{blink("s2p",[1.6,3.9,5.5])}
// bottle slides in, Paul steps back behind it and hugs (strap band)
tl.set("#s2-bottle",{{x:900}},0);
tl.to("#s2-paulwrap",{{scale:0.62,y:-194,duration:0.5,ease:"power3.inOut",transformOrigin:"50% 50%"}},1.7);
tl.to("#s2p-armL",{{rotation:-40,svgOrigin:"66 210",duration:0.4,ease:"power2.out"}},1.8);
tl.to("#s2p-armR",{{rotation:40,svgOrigin:"334 210",duration:0.4,ease:"power2.out"}},1.8);
tl.to("#s2-bottle",{{x:0,duration:0.5,ease:"back.out(1.2)"}},1.8);
tl.fromTo("#s2-b-strap",{{opacity:0,scaleX:0.1,svgOrigin:"150 265"}},{{opacity:1,scaleX:1,duration:0.3,ease:"back.out(2)"}},2.45);
tl.fromTo("#s2-bottle",{{scaleX:1}},{{scaleX:0.96,duration:0.12,ease:"power2.out",yoyo:true,repeat:1,transformOrigin:"50% 60%"}},2.8);
tl.to("#s2p-eyes",{{scaleY:0.45,svgOrigin:"200 176",duration:0.15}},2.9);
tl.to("#s2p-eyes",{{scaleY:1,svgOrigin:"200 176",duration:0.15}},3.5);
// caravan drives in where the title was
tl.to("#s2-title",{{opacity:0,y:-40,duration:0.3,ease:"power2.in"}},3.35);
tl.set("#s2-road",{{opacity:1}},3.5);
tl.fromTo("#s2-van",{{x:-900}},{{x:0,duration:0.7,ease:"power3.out"}},3.5);
tl.fromTo("#s2-van",{{rotation:2}},{{rotation:-1,duration:0.12,yoyo:true,repeat:9,ease:"sine.inOut"}},3.5);
// whip out
tl.to("#root > div",{{x:-1200,duration:0.4,ease:"power3.in"}},5.6);
'''
write("s2", scene("s2", 6.0, "", s2_html, s2_js))

# ================================================================ S3 FEATURES (11.8s)
s3_html = f'''
    <div id="s3-a" class="abs" style="left:0;top:0;width:1080px;height:1920px">
      <div id="s3-at" class="abs center heavy" style="top:300px;font-size:116px">ALUMINIUM</div>
      <div id="s3-photo" class="abs sticker" style="left:250px;top:450px;width:580px;padding:18px 18px 64px;background:#fff;border-radius:10px;transform:rotate(-4deg)">
        <img src="assets/paul-profil-foto.png" style="width:544px;display:block;border-radius:4px"/>
        <div class="thin" style="position:absolute;left:0;right:0;bottom:16px;text-align:center;font-size:30px">So seh ich in echt aus</div></div>
      <div class="abs" style="left:110px;top:800px">
        <div id="s3-c1" class="heavy" style="font-size:56px;margin-bottom:26px"><span style="color:{ORANGE}">✓</span> leicht</div>
        <div id="s3-c2" class="heavy" style="font-size:56px;margin-bottom:26px"><span style="color:{ORANGE}">✓</span> robust</div>
        <div id="s3-c3" class="heavy" style="font-size:56px"><span style="color:{ORANGE}">✓</span> rostet nicht</div></div>
      <div id="s3-pw" class="abs" style="left:520px;top:760px;width:480px;height:320px">{paul_svg("s3p","left:0;top:0;width:480px;height:320px")}</div>
    </div>
    <div id="s3-b" class="abs" style="left:0;top:0;width:1080px;height:1920px">
      <div id="s3-bt" class="abs center heavy" style="top:300px;font-size:92px">KLAPPSCHLOSS</div>
      <div id="s3-bt2" class="abs center heavy" style="top:300px;font-size:84px;opacity:0">ABSCHLIESSBAR</div>
      <div id="s3-buckle" class="abs" style="left:240px;top:500px">{buckle_big("s3-bk")}</div>
      <div id="s3-lock" class="abs" style="left:445px;top:760px">{padlock("s3-pl")}</div>
      <div id="s3-klack" class="abs heavy" style="left:700px;top:470px;font-size:64px;color:{ORANGE};transform:rotate(10deg)">KLACK!</div>
      <div id="s3-sub1" class="abs center thin" style="top:960px;font-size:56px">Ein Handgriff – <b style="font-weight:800">zu.</b></div>
      <div id="s3-sub2" class="abs center thin" style="top:1010px;font-size:52px;opacity:0">mit <b style="font-weight:800">Vorhängeschloss</b></div>
      <img id="s3-real" class="abs sticker" src="assets/paul-gurt.png" style="left:90px;top:430px;width:250px;transform:rotate(-8deg)"/>
    </div>
    <div class="abs" style="left:-240px;top:1400px;width:620px;height:620px;border-radius:50%;background:{ORANGE}"></div>
    <div id="s3-wipe" class="abs" style="left:0;top:1920px;width:1080px;height:2000px;background:{NAVY}"></div>
'''
s3_js = f'''{rest_arms("s3p")}
// --- A: Aluminium
tl.fromTo("#s3-at",{{opacity:0,y:50}},{{opacity:1,y:0,duration:0.45,ease:"power3.out"}},0.0);
tl.fromTo("#s3-photo",{{opacity:0,y:80,rotation:-12}},{{opacity:1,y:0,rotation:-4,duration:0.55,ease:"back.out(1.5)"}},0.3);
tl.fromTo("#s3-pw",{{y:500}},{{y:0,duration:0.5,ease:"back.out(1.4)"}},0.5);
{talk("s3p",[(0.4,1.61),(1.82,2.37),(2.57,3.08),(3.59,4.55)])}
{blink("s3p",[1.2,3.3])}
tl.fromTo("#s3-c1",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.35,ease:"back.out(2)"}},1.82);
tl.fromTo("#s3-c2",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.35,ease:"back.out(2)"}},2.57);
tl.fromTo("#s3-c3",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.35,ease:"back.out(2)"}},3.59);
// flex on "robust"
tl.to("#s3p-armR",{{rotation:-95,svgOrigin:"334 210",duration:0.3,ease:"back.out(2)"}},2.5);
tl.to("#s3p-foreR",{{rotation:-110,svgOrigin:"420 282",duration:0.3,ease:"back.out(2)"}},2.58);
tl.fromTo("#s3-pw",{{scale:1}},{{scale:1.08,duration:0.15,yoyo:true,repeat:1,transformOrigin:"50% 100%"}},2.6);
// shine on "rostet nicht"
tl.fromTo("#s3p-shine",{{opacity:0.0,x:0}},{{opacity:0.7,x:240,duration:0.5,ease:"power2.inOut"}},3.6);
tl.to("#s3p-shine",{{opacity:0,duration:0.15}},4.1);
// --- B: Klappschloss
tl.set("#s3-b",{{opacity:0}},0);
tl.to("#s3-a",{{x:-1200,duration:0.4,ease:"power3.in"}},4.45);
tl.fromTo("#s3-b",{{opacity:1,x:1200}},{{x:0,duration:0.45,ease:"power3.out"}},4.6);
tl.set("#s3-bk-lever",{{rotation:-38,svgOrigin:"160 185"}},0);
tl.set("#s3-lock",{{opacity:0}},0); tl.set("#s3-klack",{{opacity:0}},0); tl.set("#s3-sub1",{{opacity:0}},0);
tl.fromTo("#s3-real",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},5.0);
tl.to("#s3-bk-lever",{{rotation:-46,svgOrigin:"160 185",duration:0.35,ease:"power2.out"}},6.2);
tl.to("#s3-bk-lever",{{rotation:0,svgOrigin:"160 185",duration:0.16,ease:"power4.in"}},6.85);
tl.fromTo("#s3-buckle",{{y:0}},{{y:10,duration:0.06,yoyo:true,repeat:1}},7.01);
tl.fromTo("#s3-klack",{{opacity:0,scale:0.3}},{{opacity:1,scale:1,duration:0.2,ease:"back.out(3)"}},7.02);
tl.to("#s3-klack",{{opacity:0,duration:0.25}},7.9);
tl.fromTo("#s3-sub1",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},7.05);
// --- C: Vorhängeschloss
tl.to("#s3-bt",{{opacity:0,y:-30,duration:0.25}},8.1);
tl.fromTo("#s3-bt2",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},8.3);
tl.to("#s3-sub1",{{opacity:0,duration:0.2}},8.1);
tl.set("#s3-pl-shackle",{{y:-46}},0);
tl.fromTo("#s3-lock",{{opacity:0,y:-500}},{{opacity:1,y:0,duration:0.45,ease:"bounce.out"}},8.5);
tl.to("#s3-pl-shackle",{{y:0,duration:0.14,ease:"power4.in"}},9.6);
tl.fromTo("#s3-lock",{{rotation:0}},{{rotation:6,duration:0.08,yoyo:true,repeat:3,transformOrigin:"50% 0%"}},9.74);
tl.fromTo("#s3-sub2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},9.0);
// wipe to navy
tl.to("#s3-wipe",{{y:-1920,duration:0.45,ease:"power3.in"}},11.35);
'''
write("s3", scene("s3", 11.8, "", s3_html, s3_js))

# ================================================================ S4 PASST + TÜV (7.8s)
rows = [("5 + 11 kg", "Gasflaschen"), ("Ø 229–300 mm", "Durchmesser"), ("max. 910 mm", "Flaschenhöhe")]
rows_html = "".join(
    f'<div id="s4-r{i}" style="display:flex;justify-content:space-between;align-items:baseline;border-top:2px solid rgba(255,255,255,.25);padding:22px 0">'
    f'<span class="thin" style="font-size:{92 if i==0 else 78}px;color:#fff">{a}</span><span class="thin" style="font-size:30px;color:#C9CFE3">{b}</span></div>'
    for i, (a, b) in enumerate(rows))
s4_html = f'''
    <div id="s4-specs" class="abs" style="left:120px;top:300px;width:840px">
      <div class="heavy" style="font-size:34px;color:{ORANGE};letter-spacing:.06em;margin-bottom:14px">PASST PAUL ZU DEINER FLASCHE?</div>
      {rows_html}</div>
    <div id="s4-b1" class="abs" style="left:260px;top:820px">{bottle_svg("s4-ba", strap=True, w=130)}</div>
    <div id="s4-b2" class="abs" style="left:560px;top:760px">{bottle_svg("s4-bb", strap=True, w=180)}</div>
    <div id="s4-stamp" class="abs" style="left:290px;top:330px;width:500px;height:500px">
      <svg viewBox="0 0 500 500" width="500"><defs><path id="s4-ring" d="M250 250 m-190 0 a190 190 0 1 1 380 0 a190 190 0 1 1 -380 0"/></defs>
        <circle cx="250" cy="250" r="236" fill="none" stroke="{ORANGE}" stroke-width="14"/>
        <circle cx="250" cy="250" r="150" fill="{ORANGE}"/>
        <text font-family="Montserrat" font-weight="800" font-size="30" fill="#fff" letter-spacing="4"><textPath href="#s4-ring">DIN EN 12195-1 · VDI 2700 · LADUNGSSICHERUNG ·</textPath></text>
        <text x="250" y="236" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="46" fill="{NAVY}">TÜV NORD</text>
        <text x="250" y="300" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="44" fill="#fff">GEPRÜFT</text></svg></div>
    <div id="s4-force" class="abs center" style="top:880px">
      <div class="heavy" style="font-size:120px;color:#fff">60 daN</div>
      <div class="thin" style="font-size:40px;color:#fff;margin-top:12px">in, entgegen &amp; quer zur Fahrtrichtung</div></div>
    <div id="s4-wipe" class="abs" style="left:540px;top:960px;width:120px;height:120px;margin:-60px 0 0 -60px;border-radius:50%;background:#FFFFFF;opacity:0"></div>
    <div class="abs" style="left:700px;top:1380px;width:620px;height:620px;border-radius:50%;background:{ORANGE}"></div>
'''
s4_js = f'''
tl.set("#s4-wipe",{{scale:0,opacity:1}},0.01);
tl.fromTo("#s4-specs > div:first-child",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.0);
tl.fromTo("#s4-r0",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},0.4);
tl.fromTo("#s4-r1",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},1.0);
tl.fromTo("#s4-r2",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},1.5);
tl.fromTo("#s4-b1",{{opacity:0,y:200}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.6)"}},0.75);
tl.fromTo("#s4-b2",{{opacity:0,y:200}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.6)"}},1.35);
// to the stamp
tl.to(["#s4-specs","#s4-b1","#s4-b2"],{{opacity:0,y:-40,duration:0.3,ease:"power2.in",stagger:0.03}},2.45);
tl.fromTo("#s4-stamp",{{opacity:0,scale:2.4,rotation:-30}},{{opacity:1,scale:1,rotation:-10,duration:0.28,ease:"power4.in"}},2.75);
tl.fromTo("#root",{{x:0}},{{x:14,duration:0.05,yoyo:true,repeat:5,ease:"none"}},3.03);
tl.fromTo("#s4-force",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.45,ease:"power3.out"}},4.95);
tl.fromTo("#s4-wipe",{{scale:0}},{{scale:40,duration:0.5,ease:"power2.in"}},7.3);
'''
write("s4", scene("s4", 7.8, "", s4_html, s4_js, ground=NAVY))

# ================================================================ S5 EHRLICH + MONTAGE (6.5s)
s5_html = f'''
    <div id="s5-wall" class="abs" style="left:200px;top:540px;width:680px;height:500px;border-radius:28px;background:#F3EEE6"></div>
    <div id="s5-wood" class="abs" style="left:200px;top:540px;width:680px;height:500px;border-radius:28px;background:repeating-linear-gradient(0deg,#C99A62 0 60px,#B88A55 60px 64px);opacity:0"></div>
    <div id="s5-metal" class="abs" style="left:200px;top:540px;width:680px;height:500px;border-radius:28px;background:linear-gradient(135deg,#D9DEE3,#AEB6BE);opacity:0"></div>
    <div id="s5-gfk" class="abs" style="left:200px;top:540px;width:680px;height:500px;border-radius:28px;background:#FFFFFF;border:6px solid #D7DDE2;opacity:0"></div>
    <div id="s5-wl" class="abs heavy" style="left:230px;top:980px;font-size:40px;color:#fff;opacity:0">HOLZ</div>
    <div id="s5-t1" class="abs center" style="top:300px">
      <div class="thin" style="font-size:78px">Ehrlich gesagt:</div>
      <div class="heavy" style="font-size:66px;margin-top:16px">Schrauben sind<br/>nicht dabei.</div></div>
    <div id="s5-t2" class="abs center" style="top:300px;opacity:0">
      <div class="thin" style="font-size:66px">Jede Wand ist anders –</div>
      <div class="heavy" style="font-size:62px;margin-top:16px">nimm die passenden.</div></div>
    <div id="s5-t3" class="abs center" style="top:300px;opacity:0">
      <div class="thin" style="font-size:72px">montiert in</div>
      <div class="heavy" style="font-size:120px;margin-top:6px;color:{ORANGE}"><span id="s5-n">1</span> Schritten</div></div>
    {screw("s5-s1",250,600)}{screw("s5-s2",500,560)}{screw("s5-s3",750,600)}
    <svg id="s5-x" class="abs" viewBox="0 0 700 300" width="700" style="left:190px;top:580px" overflow="visible">
      <line x1="40" y1="40" x2="660" y2="260" stroke="{RED}" stroke-width="22" stroke-linecap="round"/></svg>
    <div id="s5-pw" class="abs" style="left:240px;top:600px;width:600px;height:400px">{paul_svg("s5p","left:0;top:0;width:600px;height:400px")}</div>
    <div class="abs" style="left:-260px;top:1380px;width:640px;height:600px;border-radius:44% 56% 50% 50%;background:{NAVY}"></div>
    <div id="s5-dots" class="abs center" style="top:1060px;opacity:0">{"".join(f'<span id="s5-d{i}" style="display:inline-block;width:34px;height:34px;border-radius:50%;margin:0 10px;background:#D7DDE2"></span>' for i in range(1,7))}</div>
'''
s5_js = f'''{rest_arms("s5p")}
tl.fromTo("#s5-t1",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.05);
tl.fromTo("#s5-pw",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(1.6)"}},0.0);
tl.to("#s5p-pupils",{{x:-12,y:12,duration:0.3}},0.4);
tl.to("#s5p-armL",{{rotation:-35,svgOrigin:"66 210",duration:0.4,ease:"power2.out"}},0.6);
tl.to("#s5p-armR",{{rotation:35,svgOrigin:"334 210",duration:0.4,ease:"power2.out"}},0.6);
tl.fromTo("#s5-pw",{{y:0}},{{y:-18,duration:0.18,yoyo:true,repeat:1,ease:"power2.out"}},0.9);
{talk("s5p",[(0.4,2.37),(2.86,4.10),(4.69,6.43)])}
{blink("s5p",[2.0,4.4])}
// screws pop then get crossed (Paul moves aside)
tl.to("#s5-pw",{{x:0,y:170,scale:0.6,duration:0.4,ease:"power3.inOut",transformOrigin:"50% 50%"}},1.2);
tl.fromTo(["#s5-s1","#s5-s2","#s5-s3"],{{opacity:0,y:-60,rotation:-20}},{{opacity:1,y:0,rotation:0,duration:0.35,ease:"back.out(2)",stagger:0.1}},1.3);
tl.fromTo("#s5-x",{{opacity:0,scaleX:0,transformOrigin:"0% 50%"}},{{opacity:1,scaleX:1,duration:0.25,ease:"power3.out"}},1.95);
tl.to(["#s5-s1","#s5-s2","#s5-s3","#s5-x"],{{opacity:0,duration:0.25}},2.7);
// walls
tl.to("#s5-t1",{{opacity:0,y:-30,duration:0.25}},2.7);
tl.fromTo("#s5-t2",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},2.86);
tl.to("#s5-pw",{{y:0,scale:0.8,duration:0.4,ease:"power3.inOut"}},2.8);
tl.to("#s5p-pupils",{{x:0,y:0,duration:0.3}},2.8);
tl.to("#s5p-armL",{{rotation:0,svgOrigin:"66 210",duration:0.3}},2.8);
tl.to("#s5p-armR",{{rotation:0,svgOrigin:"334 210",duration:0.3}},2.8);
tl.set("#s5-wl",{{opacity:1}},2.9);
tl.fromTo("#s5-wood",{{opacity:0}},{{opacity:1,duration:0.15}},2.9);
tl.set("#s5-wl",{{textContent:"ALU / STAHL"}},3.35); tl.fromTo("#s5-metal",{{opacity:0}},{{opacity:1,duration:0.15}},3.35);
tl.set("#s5-wl",{{textContent:"GFK",color:"{NAVY}"}},3.8); tl.fromTo("#s5-gfk",{{opacity:0}},{{opacity:1,duration:0.15}},3.8);
// 6 steps
tl.to(["#s5-t2","#s5-wl"],{{opacity:0,y:-30,duration:0.25}},4.45);
tl.to("#s5-dots",{{opacity:1,duration:0.2}},4.6);
tl.fromTo("#s5-t3",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},4.6);
''' + "\n".join(
    f'tl.set("#s5-n",{{textContent:"{i}"}},{4.7+0.22*(i-1):.2f});tl.to("#s5-d{i}",{{backgroundColor:"{ORANGE}",scale:1.25,duration:0.1}},{4.7+0.22*(i-1):.2f});tl.to("#s5-d{i}",{{scale:1,duration:0.1}},{4.8+0.22*(i-1):.2f});'
    for i in range(1, 7)) + f'''
tl.fromTo("#s5-pw",{{y:0}},{{y:-40,duration:0.2,yoyo:true,repeat:1,ease:"power2.out"}},5.8);
tl.to("#root > *",{{opacity:0,duration:0.2}},6.3);
'''
write("s5", scene("s5", 6.5, "", s5_html, s5_js))

# ================================================================ S6 QR + END (8.3s)
s6_html = f'''
    <div id="s6-blobN" class="abs" style="left:-360px;top:-470px;width:820px;height:700px;border-radius:44% 56% 62% 38%;background:{NAVY}"></div>
    <div id="s6-blobO" class="abs" style="left:760px;top:1500px;width:520px;height:520px;border-radius:50%;background:{ORANGE}"></div>
    <div id="s6-title" class="abs center" style="top:300px">
      <div class="thin" style="font-size:64px">Scann mich &amp; sieh</div>
      <div class="heavy" style="font-size:96px;margin-top:8px">PAUL IN AKTION</div></div>
    <div id="s6-end" class="abs center" style="top:300px;opacity:0">
      <div class="thin" style="font-size:60px;letter-spacing:.02em">DAS IST</div>
      <div class="heavy" style="font-size:160px">PAUL.</div></div>
    <img id="s6-photo" class="abs sticker" src="assets/flasche-sticker.png" style="left:110px;top:520px;height:520px"/>
    <div id="s6-qrcard" class="abs sticker" style="left:470px;top:540px;width:420px;padding:20px;background:#fff;border-radius:22px;border:6px solid {NAVY}">
      <img src="assets/qr-paul.png" style="width:368px;display:block"/>
      <div class="thin" style="font-size:28px;text-align:center;margin-top:10px;line-height:1.15">Produktseite mit Montagevideo</div></div>
    <svg id="s6-arrow" class="abs" viewBox="0 0 120 80" width="120" style="left:620px;top:470px" overflow="visible">
      <path d="M60 0 L60 50 M30 28 L60 62 L90 28" stroke="{ORANGE}" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <div id="s6-url" class="abs center heavy" style="top:1046px;font-size:46px">gasflaschenhalter.de</div>
    <div id="s6-pw" class="abs" style="left:30px;top:905px;width:270px;height:180px">{paul_svg("s6p","left:0;top:0;width:270px;height:180px")}</div>
    <div id="s6-foot" class="abs" style="left:120px;top:1130px;width:840px;display:flex;align-items:center;gap:24px;opacity:0">
      <img src="assets/logo-vb.png" style="width:110px"/>
      <div><div class="heavy" style="font-size:30px">Gasflaschenhalterung FH 160 Aluminium</div>
      <div class="thin" style="font-size:28px;margin-top:6px">TÜV NORD geprüft · DIN EN 12195-1 / VDI 2700</div></div></div>
'''
s6_js = f'''{rest_arms("s6p")}
tl.fromTo("#s6-blobN",{{scale:0.4,rotation:-30}},{{scale:1,rotation:0,duration:0.7,ease:"back.out(1.3)"}},0);
tl.fromTo("#s6-blobO",{{scale:0}},{{scale:1,duration:0.6,ease:"back.out(1.5)"}},0.2);
tl.fromTo("#s6-title",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.45,ease:"power3.out"}},0.1);
tl.fromTo("#s6-photo",{{opacity:0,x:-200,rotation:-10}},{{opacity:1,x:0,rotation:-4,duration:0.55,ease:"back.out(1.4)"}},0.15);
tl.fromTo("#s6-qrcard",{{opacity:0,scale:0.5,rotation:8}},{{opacity:1,scale:1,rotation:0,duration:0.5,ease:"back.out(1.7)"}},0.37);
tl.fromTo("#s6-arrow",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.3,ease:"power2.out"}},0.8);
tl.to("#s6-arrow",{{y:14,duration:0.35,ease:"sine.inOut",repeat:3,yoyo:true}},1.1);
tl.fromTo("#s6-url",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.9);
tl.fromTo("#s6-pw",{{opacity:0,y:120,scale:0.6}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"back.out(1.8)"}},0.6);
tl.to("#s6p-armR",{{rotation:-75,svgOrigin:"334 210",duration:0.35,ease:"back.out(2)"}},1.0);
tl.to("#s6p-pupils",{{x:10,y:-8,duration:0.25}},1.0);
{talk("s6p",[(0.37,2.79)])}
{blink("s6p",[2.2,4.6,6.9])}
// end lockup keeps the QR on screen
tl.to(["#s6-title","#s6-arrow"],{{opacity:0,duration:0.3,ease:"power2.in"}},3.1);
tl.fromTo("#s6-end",{{opacity:0,scale:0.85}},{{opacity:1,scale:1,duration:0.5,ease:"back.out(1.6)"}},3.3);
tl.fromTo("#s6-foot",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.45,ease:"power3.out"}},3.6);
{wave("s6p",4.6,"L",5)}
'''
write("s6", scene("s6", 8.3, "", s6_html, s6_js))

# ================================================================ captions
caps = [  # absolute seconds
    (0.6, 2.27, "Rappelt's bei dir auch im Gaskasten?"),
    (2.79, 5.95, "Bei einer Vollbremsung wird eine lose Gasflasche zum Geschoss."),
    (6.39, 7.4, "Das muss nicht sein!"),
    (9.0, 10.09, "Hi, ich bin Paul!"),
    (10.36, 11.93, "Ich halte deine Gasflasche fest –"),
    (12.16, 13.6, "egal, wohin die Reise geht."),
    (15.0, 16.21, "Ich bin aus Aluminium:"),
    (16.42, 17.68, "leicht, robust –"),
    (18.19, 19.15, "und ich roste nicht."),
    (19.33, 20.6, "Mein Klappschloss?"),
    (20.82, 22.4, "Ein Handgriff, und zu!"),
    (22.87, 25.4, "Und mit Vorhängeschloss bin ich sogar abschließbar."),
    (26.8, 28.74, "Ich passe auf 5- und 11-Kilo-Flaschen."),
    (29.02, 30.82, "Und der TÜV Nord hat mich geprüft –"),
    (31.4, 33.2, "nach der Norm für Ladungssicherung."),
    (34.6, 36.57, "Ehrlich gesagt: Schrauben bring ich nicht mit –"),
    (37.06, 38.3, "denn jede Wand ist anders."),
    (38.89, 40.63, "Dafür bin ich in sechs Schritten montiert."),
    (41.07, 43.55, "Scann den Code und schau mir beim Festhalten zu!"),
]
cap_html, cap_js = [], []
for i, (a, b, t) in enumerate(caps):
    cap_html.append(f'<div id="cap{i}" class="cap clip" data-start="{a}" data-duration="{b-a:.2f}"><span>{t}</span></div>')
    cap_js.append(f'tl.fromTo("#cap{i} span",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.16,ease:"power2.out"}},{a});')
cap = f'''<template>
  <style>
    #root {{ position:absolute; inset:0; pointer-events:none; }}
    .cap {{ position:absolute; left:120px; width:660px; top:1110px; text-align:center; font-family:'Montserrat',sans-serif; }}
    .cap span {{ display:inline-block; background:{NAVY}; color:#fff; font-weight:800; font-size:40px; line-height:1.2; padding:10px 22px; border-radius:16px; box-decoration-break:clone; -webkit-box-decoration-break:clone; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
    {"".join(cap_html)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {"".join(cap_js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
'''
write("captions", cap)

# ================================================================ index
scenes = [("s1", 0, 8.6), ("s2", 8.6, 6.0), ("s3", 14.6, 11.8), ("s4", 26.4, 7.8), ("s5", 34.2, 6.5), ("s6", 40.7, 8.3)]
hosts = "\n".join(
    f'      <div id="{s}" data-composition-id="{s}" data-composition-src="compositions/{s}.html" data-start="{a}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:1"></div>'
    for s, a, d in scenes)
index = f'''<!doctype html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ margin:0; width:1080px; height:1920px; overflow:hidden; background:#FFFFFF; }}
      #root {{ position:relative; width:1080px; height:1920px; font-family:'Montserrat',sans-serif; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="49" data-width="1080" data-height="1920">
{hosts}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="49" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:5"></div>
      <audio id="voice" class="clip" src="assets/voice.mp3" data-start="0" data-duration="49" data-track-index="3" data-volume="1"></audio>
      <audio id="music" class="clip" src="assets/musik-2.mp3" data-start="0" data-duration="49" data-track-index="4" data-volume="0.16" data-fade-out="1.5"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open(f"{OUT}/index.html", "w").write(index)
print("ok")
