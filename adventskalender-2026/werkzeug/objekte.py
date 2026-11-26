"""Gegenstände der Tage als SVG. Ursprung (0,0) = Mitte unten (Füße), nach oben negativ.
svg(fill, ink, cls) zeichnet den Gegenstand; Flächen mit Holzfarbe bekommen die Klasse cls,
damit die Szene die Farbe zwischen Gegenwart (Holz) und Vergangenheit (grau) überblenden kann."""


def _c(cls):
    return f' class="{cls}"' if cls else ""


def stuhl_svg(fill, ink, cls=None):
    c = _c(cls)
    s = f'stroke="{ink}" stroke-width="6" stroke-linejoin="round"'
    return f"""
<rect x="-150" y="-280" width="22" height="240" fill="{fill}"{c} {s}/>
<rect x="128" y="-280" width="22" height="240" fill="{fill}"{c} {s}/>
<rect x="-150" y="-280" width="22" height="240" fill="#000" opacity="0.2"/>
<rect x="128" y="-280" width="22" height="240" fill="#000" opacity="0.2"/>
<rect x="-172" y="-640" width="28" height="320" rx="6" fill="{fill}"{c} {s}/>
<rect x="144" y="-640" width="28" height="320" rx="6" fill="{fill}"{c} {s}/>
<rect x="-92" y="-570" width="22" height="240" fill="{fill}"{c} {s}/>
<rect x="-11" y="-570" width="22" height="240" fill="{fill}"{c} {s}/>
<rect x="70" y="-570" width="22" height="240" fill="{fill}"{c} {s}/>
<rect x="-184" y="-636" width="368" height="70" rx="16" fill="{fill}"{c} {s}/>
<path d="M-176 -352 L176 -352 L204 -326 L-204 -326 Z" fill="{fill}"{c} {s}/>
<path d="M-176 -352 L176 -352 L204 -326 L-204 -326 Z" fill="#fff" opacity="0.14"/>
<rect x="-212" y="-328" width="424" height="52" rx="8" fill="{fill}"{c} {s}/>
<rect x="-204" y="-280" width="32" height="280" rx="4" fill="{fill}"{c} {s}/>
<rect x="172" y="-280" width="32" height="280" rx="4" fill="{fill}"{c} {s}/>
<rect x="-176" y="-112" width="352" height="18" fill="{fill}"{c} {s}/>
"""


def stuhl_heute_js(p, marks):
    # "Ein Bein kratzt über den Boden": der Stuhl ruckt kurz
    t = marks[2][0] + 0.5
    return (f'tl.to("#{p}-hero",{{x:14,rotation:-1.5,duration:0.12,ease:"power2.out",transformOrigin:"50% 100%"}},{t:.2f});'
            f'tl.to("#{p}-hero",{{x:10,rotation:0,duration:0.5,ease:"power3.out"}},{t + 0.12:.2f});')


def zeichnung(p):
    """Ein Blatt mit einem gemalten Stern, liegt auf der Sitzfläche (Recht: 'eine Zeichnung kann helfen')."""
    return f"""
<svg class="world" viewBox="0 0 1080 1920" width="1080" height="1920" data-layout-ignore>
  <g transform="translate(540,1214)"><g id="{p}-sheet">
    <rect x="-95" y="-14" width="190" height="20" fill="#F7F2E6" stroke="#2B1D17" stroke-width="4" transform="skewX(-25)"/>
    <path d="M -10 -10 l 7 -2 l 3 -6 l 3 6 l 7 2 l -6 3 l 1 6 l -5 -3 l -5 3 l 1 -6 z" fill="#E0A63A" stroke="#2B1D17" stroke-width="2"/>
  </g></g>
</svg>"""


OBJEKTE = {
    "stuhl": {
        "svg": stuhl_svg,
        "heute_js": stuhl_heute_js,
        "prop": zeichnung,
        "prop_js": lambda p: f'tl.fromTo("#{p}-sheet",{{y:-260,rotation:-14,opacity:0}},{{y:0,rotation:0,opacity:1,duration:0.7,ease:"power3.out"}},2.0);',
    },
}
