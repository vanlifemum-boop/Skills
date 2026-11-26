#!/usr/bin/env python3
"""Erzeugt das PDF 'Bilderauftrag' mit allen benötigten Bildern und Beschreibungen."""
import html, sys

STIL_RAUM = ("Painterly 3D animated storybook style like a Pixar film still, soft cinematic light, rich detail, "
             "landscape 3:2 (1536x1024), no people, no text, no logos, no symbols, keep the middle and lower third "
             "open floor space so characters can be placed later.")
SEPIA = " Whole image in warm sepia tones like an old photograph, slightly faded, soft film grain."

RAEUME_HEUTE = [
    ("H1", "Kinderzimmer der Wohngruppe bei Nacht", "2, 7, 13, 19, 23, 24", "raum_H1_kinderzimmer_nacht.png",
     "Schlichtes, ordentliches Kinderzimmer einer Wohngruppe bei Nacht. Ein Einzelbett mit weißem Kopfkissen und Bettdecke "
     "steht links. Unter dem Kissen schaut ein gefaltetes Blatt Papier hervor. Durchs Fenster rechts fällt Mondlicht, draußen schneit es. "
     "Eine kleine warme Nachttischlampe brennt. An der Wand hängen ein Kinderbild und ein Adventskalender mit offenen Türchen. "
     "Stimmung: zärtlich, einsam, still.",
     "Empty simple tidy child's bedroom in a modern German children's group home at night. A single bed with white pillow and duvet on the left, "
     "a folded sheet of paper peeking out from under the pillow. Moonlight through a window on the right, snow falling outside. "
     "A small warm bedside lamp. A child's drawing and an Advent calendar with opened doors on the wall. Tender, lonely, quiet mood."),
    ("H2", "Kinderzimmer am Tag mit Schreibtisch", "3, 15, 17", "raum_H2_kinderzimmer_tag.png",
     "Dasselbe Kinderzimmer am Tag (gleiches Fenster, gleiche Farben wie H1). Vorne ein Schreibtisch mit Kinderstuhl. Darauf liegen "
     "ein Blatt mit durchgestrichenen Wünschen, Buntstifte, Schere, gelbes Bastelpapier und ein halb fertiger Papierstern. An der Wand "
     "ein Kalender mit Strichen. Graues Winterlicht von draußen, eine Schreibtischlampe.",
     "Empty child's bedroom in a modern German children's group home during a grey winter day. In front a child's desk with a small chair; "
     "on the desk a sheet of paper with crossed-out wishes, crayons, scissors, yellow craft paper and a half-finished paper star. "
     "A wall calendar with tally marks. Soft grey daylight from the window, a warm desk lamp."),
    ("H3", "Gemeinschaftsraum der Wohngruppe", "4, 9, 11, 12, 20", "raum_H3_gemeinschaftsraum.png",
     "Wohnzimmer einer Wohngruppe: großes Sofa, ein Tisch mit Stühlen, auf einem Sideboard ein Festnetztelefon. "
     "Adventsdeko mit Adventskranz, Lichterkette und Papiersternen am Fenster. An einer Pinnwand hängen Zettel mit Telefonnummern. "
     "Gemütlich, aber man merkt: Hier wohnen viele Kinder.",
     "Empty living room of a modern German children's group home in December: a large sofa, a table with several chairs, a landline phone "
     "on a sideboard, an Advent wreath with candles, fairy lights and paper stars in the window, a pinboard with notes and phone numbers. "
     "Cosy but clearly a shared home for many children, evening light."),
    ("H4", "Küche der Wohngruppe mit Plätzchen", "16", "raum_H4_kueche_wohngruppe.png",
     "Große Gemeinschaftsküche einer Wohngruppe. Auf dem Tisch ein Backblech mit Plätzchen, eines am Rand etwas dunkler. "
     "Mehrere Stühle, ein Wochenplan an der Wand. Warmes Licht.",
     "Empty large shared kitchen of a modern German children's group home, a baking tray with Christmas cookies on the table "
     "(one cookie slightly darker at the edge), several chairs, a weekly chore plan on the wall, warm light."),
    ("H5", "Küche zuhause (Erinnerung ans Backen)", "3, 16, 18", "raum_H5_kueche_zuhause.png",
     "Kleine, warme Familienküche, abends, goldenes Licht. Auf dem Holztisch liegen Mehl, Teig, Ausstechformen und eine Teigrolle. "
     "Eine offene Schublade, ein Sofa ist durch die Tür zu sehen, auf dem eine Decke herunterrutscht. Sehr geborgen, ein bisschen verträumt "
     "(soll wie eine Erinnerung wirken).",
     "Empty small warm family kitchen in the evening, golden dreamy light. On the wooden table flour, cookie dough, cookie cutters and a rolling pin; "
     "a half-open drawer; through a doorway a sofa with a blanket slipping off. Very cosy, nostalgic, like a warm memory, soft glow at the edges."),
    ("H6", "Eingang der Wohngruppe", "6, 22", "raum_H6_eingang.png",
     "Eingangsbereich einer Wohngruppe: Garderobe mit Kinderjacken und Mützen, ein Schuhregal mit vielen Kinderschuhen, eine Bank zum "
     "Schuhe anziehen, die Haustür mit Milchglas. Abend, Lampe an.",
     "Empty entrance hall of a modern German children's group home: coat rack with children's jackets and hats, a shoe rack full of children's shoes, "
     "a bench to sit on while putting on shoes, front door with frosted glass, evening, lamp on."),
    ("H7", "Fensterbank mit Blick auf verschneite Straße", "14, 22", "raum_H7_fenster.png",
     "Blick von innen aus einem Fenster mit breiter Fensterbank (Kissen darauf). Draußen eine verschneite Straße am Abend mit "
     "Straßenlaternen und Häusern, die Straße führt in die Ferne. Innen leicht dunkel, draußen bläulich.",
     "View from inside a room through a large window with a wide window seat and a cushion. Outside a snowy street in the evening with street lamps "
     "and houses, the road leading into the distance. Inside slightly dark, outside bluish winter dusk."),
    ("H8", "Garten der Wohngruppe im Schnee", "8, 9", "raum_H8_garten_schnee.png",
     "Garten hinter der Wohngruppe im Schnee: ein Schneemann, ein Schlitten, Spuren im Schnee, im Hintergrund das Haus mit "
     "beleuchteten Fenstern. Heller Wintertag.",
     "Empty garden behind a modern German children's group home covered in snow: a snowman, a sled, footprints in the snow, the house with lit windows "
     "in the background, bright winter afternoon."),
    ("H9", "Schulhof im Winter", "21", "raum_H9_schulhof.png",
     "Schulhof einer Grundschule im Winter: Schulgebäude, Bäume ohne Laub, etwas Schnee, eine Bank. Morgens.",
     "Empty primary school playground in winter: school building, bare trees, a little snow, a bench, morning light."),
    ("H10", "Formeller Konferenzraum", "5, 10, 19", "raum_H10_konferenzraum.png",
     "Sachlicher Besprechungsraum eines Amts: langer Tisch mit vielen Stühlen, Akten, Laptops, Kaffeetassen, Wasserflaschen. "
     "Neonlicht, eher kühl. Ein Stuhl steht etwas abseits.",
     "Empty formal meeting room in a German government office: a long table with many chairs, files, laptops, coffee cups, water bottles, "
     "cool fluorescent light; one chair stands slightly apart from the table."),
]

RAEUME_DAMALS = [
    ("D1", "Amtsstube 1920er–30er", "2, 4, 6, 7, 15, 19", "raum_D1_amtsstube.png",
     "Amtszimmer eines Jugendamts um 1925–1935: schwerer Holzschreibtisch mit Schreibmaschine, Stempeln, Tintenfass und Aktenstapeln. "
     "Ein Aktenschrank, eine Wanduhr, ein hoher Fenster mit Gardine. Davor ein einzelner Holzstuhl für Besucher.",
     "Empty German youth welfare office room around 1925-1935: heavy wooden desk with a typewriter, rubber stamps, an inkwell and stacks of files, "
     "a filing cabinet, a wall clock, a tall window with net curtain, a single wooden visitor chair in front of the desk." + SEPIA),
    ("D2", "Gerichtssaal 1930er", "3", "raum_D2_gerichtssaal.png",
     "Kleiner Gerichtssaal der 1930er Jahre: erhöhter Richtertisch aus dunklem Holz, Holzbänke, hohe Fenster. Streng und einschüchternd.",
     "Empty small German courtroom of the 1930s: raised dark wooden judge's bench, wooden benches, tall windows, strict and intimidating, no symbols." + SEPIA),
    ("D3", "Ärztliches Untersuchungszimmer 1930er", "5, 11", "raum_D3_untersuchung.png",
     "Untersuchungszimmer um 1935: Untersuchungsliege, alte Waage, Messlatte an der Wand, Schrank mit Instrumenten, Karteikarten. Kalt und sachlich.",
     "Empty medical examination room around 1935: examination couch, old scale, a height measuring rod on the wall, cabinet with instruments, "
     "index cards on a desk, cold and clinical, no symbols." + SEPIA),
    ("D4", "Barackenlager im Winter", "8, 9", "raum_D4_lager.png",
     "Holzbaracken im Winter, Stacheldrahtzaun, ein leerer Appellplatz mit Schnee, grauer Himmel. Ohne Symbole, ohne Schilder.",
     "Empty camp with wooden barracks in winter, barbed wire fence, an empty roll-call yard covered in snow, grey sky, no symbols, no signs." + SEPIA),
    ("D5", "Polnische Dorfstraße um 1940", "10, 11", "raum_D5_dorfstrasse.png",
     "Dorfstraße in Polen um 1940: kleine Bauernhäuser, ein Holzzaun, ein Brunnen, eine Kirche in der Ferne, Herbst. Ruhig, ländlich.",
     "Empty village street in rural Poland around 1940: small farmhouses, a wooden fence, a well, a church in the distance, autumn, quiet and rural." + SEPIA),
    ("D6", "Stube eines Kinderheims um 1940", "12, 13", "raum_D6_heimstube.png",
     "Sehr ordentliche Stube eines Kinderheims um 1940: gleiche Betten in Reihe, ein langer Tisch, ein Schrank mit Namensschildern ohne lesbaren Text. Ohne Symbole.",
     "Empty very orderly room in a children's home around 1940: identical beds in a row, a long table, a cupboard with small blank name tags, "
     "strict, no symbols, no flags." + SEPIA),
    ("D7", "Wohnstube einer Pflegefamilie 1940er", "13, 14", "raum_D7_pflegefamilie.png",
     "Bürgerliche Wohnstube der 1940er: Sofa mit Deckchen, Kachelofen, Standuhr, Bilder an der Wand, Esstisch mit Tischdecke.",
     "Empty bourgeois German living room of the 1940s: sofa with doilies, tiled stove, grandfather clock, framed pictures, dining table with tablecloth, no symbols." + SEPIA),
    ("D8", "Archiv mit Aktenregalen", "16, 23", "raum_D8_archiv.png",
     "Langer Archivgang mit hohen Regalen voller Akten und Karteikästen, eine Leiter, eine Hängelampe, Staub im Licht.",
     "Empty long archive aisle with tall shelves full of files and card index boxes, a ladder, a hanging lamp, dust in the light beams." + SEPIA),
    ("D9", "Bahnhof 1946 mit Suchzetteln", "17", "raum_D9_bahnhof.png",
     "Bahnhofshalle im Jahr 1946, teils beschädigt, eine Wand voller angehefteter Suchzettel und Fotos (ohne lesbaren Text), Koffer, Dampf.",
     "Empty partly damaged German railway station hall in 1946, a wall covered with pinned search notes and small photos (no readable text), "
     "old suitcases on the platform, steam." + SEPIA),
    ("D10", "Heimflur / Waschraum 1950er–60er", "18, 20", "raum_D10_heim1960.png",
     "Langer, kahler Flur eines Kinderheims der 1950er–60er mit Linoleum, Türen in Reihe, oder Waschraum mit Waschbecken in Reihe. Kalt, streng.",
     "Empty long bare corridor of a West German children's home in the 1950s-60s with linoleum floor and a row of doors, next to it a washroom with a row "
     "of sinks, cold and strict. Faded 1960s colour photograph look, muted and slightly washed out."),
    ("D11", "DDR-Jugendwerkhof", "21", "raum_D11_jugendwerkhof.png",
     "Hof eines geschlossenen Jugendwerkhofs der DDR: hohe Mauer, vergitterte Fenster, ein Tor. Oder eine kleine Zelle mit Pritsche. Grau, bedrückend. Ohne Symbole.",
     "Empty courtyard of a closed East German youth detention facility in the 1970s: high wall, barred windows, a heavy gate, grey and oppressive, no symbols. "
     "Faded 1970s colour photograph look, cold grey-green tones."),
    ("D12", "Anhörungssaal um 2009", "22", "raum_D12_anhoerung.png",
     "Moderner Sitzungssaal: Tische im Halbkreis, Mikrofone, Wasserflaschen, große Fenster. In Farbe.",
     "Empty modern hearing room around 2009: tables arranged in a semicircle, microphones, water bottles, large windows, neutral and serious, full colour, no logos."),
    ("D13", "Internationaler Konferenzsaal", "24", "raum_D13_konferenzsaal.png",
     "Großer internationaler Konferenzsaal, allgemein (kein echtes Gebäude): Sitzreihen, Pulte mit Mikrofonen, Kopfhörer. In Farbe.",
     "Empty large generic international conference hall (not a real recognisable building): rows of desks with microphones and headphones, "
     "a podium, soft daylight, full colour, no logos, no flags."),
]

BLATT = ("Charakterblatt wie deine bisherigen: weißer Hintergrund, 4 × 2 Posen, Beschriftung unter jeder Pose, Titel oben. "
         "Ganze Figur von Kopf bis Fuß, nichts abgeschnitten, Posen nicht überlappend, etwas Abstand zwischen den Figuren.")

FIGUREN = [
    ("F1", "Die 9 Kinder im Weihnachtslook – SITZEND", "fast alle", "Charakter_XX_Weihnachtslook_sitzend.png  (9 Blätter)",
     "Jedes der 9 Kinder in seiner bekannten Weihnachtskleidung, sitzend auf einem schlichten hellen Holzstuhl, frontal. "
     "Der Stuhl ist ganz zu sehen.",
     ["sitzend traurig", "sitzend fröhlich", "sitzend nachdenklich", "sitzend weinend", "malt am Tisch (Stift in der Hand, Blick nach unten)",
      "schreibt einen Brief", "sitzt auf dem Boden, umarmt die Knie", "sitzend hoffnungsvoll"]),
    ("F2", "Die 9 Kinder im Weihnachtslook – BESONDERE HALTUNGEN", "2, 4, 11–14, 16, 17, 20, 22, 23",
     "Charakter_XX_Weihnachtslook_Haltungen.png  (9 Blätter)",
     "Jedes der 9 Kinder in seiner Weihnachtskleidung, stehend, mit Gegenständen.",
     ["Telefonhörer am Ohr, traurig", "Telefonhörer am Ohr, tapfer lächelnd", "liest einen Brief, traurig", "hält einen gebastelten Papierstern hoch",
      "isst ein Plätzchen mit geschlossenen Augen", "von hinten (Rücken zum Betrachter)", "wartet mit Jacke und Schuhen, Zettel in der Hand",
      "liegt wach mit Kopf auf Kissen, Decke bis zum Kinn (ohne Bettgestell)"]),
    ("F3", "Die 9 Kinder im Look 1922–1945 – SITZEND & IN REIHE", "2–17",
     "Charakter_XX_1922-1945_Haltungen.png  (9 Blätter)",
     "Jedes der 9 Kinder in seiner historischen Kleidung.",
     ["sitzend traurig (Holzbank)", "sitzend ängstlich", "sitzt still mit gefalteten Händen", "steht gehorsam, Arme an der Seite, Blick gesenkt",
      "von hinten", "kniet und schrubbt den Boden", "steht mit kleinem Koffer / Bündel", "liegt mit grauer Decke, Kopf auf Kissen"]),
    ("F4", "Mama heute (zwei verschiedene Mütter)", "3, 4, 13, 20, 24", "Mama_01.png, Mama_02.png",
     "Zwei Mütter Anfang/Mitte 30, moderne Winterkleidung (Strickpulli, Jeans), Malstil wie die Kinder. Eine mit dunklen, eine mit hellen Haaren.",
     ["traurig", "weinend", "am Telefon, traurig", "am Telefon, lächelnd", "hoffnungsvoll", "breitet die Arme aus (Umarmung)",
      "sitzt am Tisch, Hände gefaltet", "von hinten am Fenster"]),
    ("F5", "Betreuerin der Wohngruppe heute", "5, 6, 10, 19", "Betreuerin_heute.png",
     "Freundliche Frau um die 40, Strickjacke, Namensschild ohne Text, Malstil wie die Kinder.",
     ["freundlich stehend", "sitzend zuhörend mit Notizblock", "erklärt (offene Hand)", "nachdenklich", "besorgt",
      "kniet auf Kinderhöhe", "telefoniert", "hält eine Akte"]),
    ("F6", "Mitarbeiter Jugendamt heute", "5, 15, 19", "Jugendamt_heute.png",
     "Mann um die 50, Hemd und Pullunder, Brille, Malstil wie die Kinder.",
     ["sitzt am Tisch mit Akte", "schreibt", "schaut auf Kalender", "ernst", "freundlich", "erklärt", "telefoniert", "steht mit Akte unter dem Arm"]),
    ("F7", "Erzieherin / Diakonisse 1920–1940er", "2–9", "Erzieherin_damals.png",
     "Strenge Frau um die 50, dunkles langes Kleid, weiße Schürze, weiße Haube, Schlüsselbund am Gürtel. Malstil wie die Kinder.",
     ["streng stehend", "zeigt mit dem Finger", "mit Liste / Klemmbrett", "Hände hinter dem Rücken", "läutet eine Handglocke",
      "schimpft", "hält Schlüsselbund hoch", "von hinten"]),
    ("F8", "Beamter und Fürsorgerin 1930er", "4, 6, 7, 15", "Beamter_damals.png, Fuersorgerin_damals.png",
     "Beamter: Mann um die 45, dunkler Anzug, Brille, Schnurrbart. Fürsorgerin: Frau um die 40, Kostüm, Hut, Handtasche. Malstil wie die Kinder.",
     ["sitzt am Schreibtisch und schreibt", "stempelt", "überreicht eine Akte", "steht ernst", "mit Aktentasche", "notiert etwas im Stehen",
      "schüttelt den Kopf", "unterschreibt"]),
    ("F9", "Mutter 1940er (polnische Bäuerin)", "10–14, 17", "Mutter_1940.png",
     "Frau um die 30, Kopftuch, Strickjacke, Schürze, einfache Kleidung. Würdevoll, keine Karikatur. Malstil wie die Kinder.",
     ["weint verzweifelt", "ruft nach jemandem", "hält ein kleines Foto", "sucht, schaut sich um", "streckt die Arme aus",
      "umarmt ins Leere", "hoffnungsvoll", "still trauernd"]),
    ("F10", "Pflegemutter 1940er", "13, 14", "Pflegemutter_1940.png",
     "Bürgerliche Frau um die 35, Kleid, Haarknoten, Malstil wie die Kinder.",
     ["freundlich", "unsicher", "Hand ausgestreckt, als läge sie auf einer Kinderschulter", "liest einen Brief", "nachdenklich", "sitzend",
      "besorgt", "erklärt"]),
    ("F11", "Kinder im Heim 1950er–60er", "18–20", "Charakter_01_02_05_08_Heimlook_1960.png  (4 Blätter)",
     "Charakter 01, 02, 05 und 08 in einheitlicher grauer Heimkleidung der 1950er–60er (Kittel / Schürze, Strickstrümpfe), kurze Haare bzw. Zöpfe.",
     ["traurig", "steht in Reihe, gerade", "schrubbt den Boden", "sitzt beim Essen", "weint", "ängstlich", "still mit gesenktem Kopf", "hoffnungsvoll"]),
    ("F12", "Jugendliche im DDR-Jugendwerkhof", "21", "Jugendliche_DDR.png  (Junge und Mädchen)",
     "Ein Junge und ein Mädchen, etwa 15 Jahre, blaue Arbeitsanzüge, kurze Haare, Malstil wie die Kinder.",
     ["ängstlich", "wütend", "steht still", "marschiert in Reihe", "sitzt auf einer Pritsche", "arbeitet", "weint", "trotzig"]),
    ("F13", "Ehemalige Heimkinder, heute alt", "22", "Ehemalige_Heimkinder.png  (Mann und Frau)",
     "Ein Mann und eine Frau um die 70, einfache Alltagskleidung, Malstil wie die Kinder.",
     ["spricht ernst ins Mikrofon", "hält ein altes Kinderfoto", "weint", "hoffnungsvoll", "sitzt", "nachdenklich", "hält sich an der Hand",
      "lächelt vorsichtig"]),
]

E = html.escape


def raum_card(r):
    nr, titel, tage, datei, de, en = r
    return f"""<section class="card"><div class="head"><span class="nr">{nr}</span><h3>{E(titel)}</h3><span class="tage">Tag {E(tage)}</span></div>
<p class="de">{E(de)}</p><div class="meta"><b>Dateiname:</b> {E(datei)} &nbsp;·&nbsp; <b>Format:</b> Querformat 3:2, 1536×1024</div>
<div class="label">Prompt zum Kopieren</div><pre>{E(en + ' ' + STIL_RAUM)}</pre></section>"""


def fig_card(f):
    nr, titel, tage, datei, de, posen = f
    lis = "".join(f"<li>{E(p)}</li>" for p in posen)
    return f"""<section class="card"><div class="head"><span class="nr">{nr}</span><h3>{E(titel)}</h3><span class="tage">Tag {E(tage)}</span></div>
<p class="de">{E(de)}</p><div class="label">Die 8 Posen</div><ol class="posen">{lis}</ol>
<div class="meta"><b>Dateiname:</b> {E(datei)}</div></section>"""


CSS = """
@page { size: A4; margin: 16mm 15mm 18mm; }
body { font-family: 'Inter', 'DejaVu Sans', sans-serif; color:#2a211c; font-size:10.5pt; line-height:1.45; }
h1 { font-size:28pt; margin:0 0 4mm; color:#8A2A22; letter-spacing:-0.02em; }
h2 { font-size:16pt; margin:9mm 0 4mm; padding-bottom:2mm; border-bottom:2px solid #8A2A22; color:#8A2A22; page-break-after:avoid; }
.sub { font-size:12pt; color:#6b5b50; margin-bottom:8mm; }
.box { background:#F6EFE6; border-left:4px solid #8A2A22; padding:4mm 5mm; margin:4mm 0; }
.box li { margin:1mm 0; }
.card { border:1px solid #E1D6C8; border-radius:3mm; padding:4mm 5mm; margin:0 0 5mm; page-break-inside:avoid; }
.head { display:flex; align-items:baseline; gap:3mm; }
.nr { background:#8A2A22; color:#fff; font-weight:700; border-radius:2mm; padding:0.5mm 2.5mm; font-size:10pt; }
h3 { margin:0; font-size:12.5pt; flex:1; }
.tage { color:#8A2A22; font-size:9.5pt; font-weight:600; white-space:nowrap; }
.de { margin:2.5mm 0; }
.meta { font-size:9pt; color:#5c4d43; margin-top:2mm; }
.label { font-size:8.5pt; text-transform:uppercase; letter-spacing:0.08em; color:#8A2A22; font-weight:700; margin-top:2.5mm; }
pre { white-space:pre-wrap; font-family:'DejaVu Sans Mono', monospace; font-size:8.3pt; background:#FBF8F4; border:1px dashed #D6C7B4;
      padding:2.5mm 3mm; margin:1.5mm 0 0; line-height:1.4; }
ol.posen { columns:2; margin:1.5mm 0 0; padding-left:6mm; }
ol.posen li { margin:0.6mm 0; break-inside:avoid; }
table { border-collapse:collapse; width:100%; font-size:9.5pt; }
td, th { border:1px solid #E1D6C8; padding:1.5mm 2mm; text-align:left; vertical-align:top; }
th { background:#F6EFE6; }
.pb { page-break-before:always; }
"""


def main(out):
    over = "".join(f"<tr><td><b>{r[0]}</b></td><td>{E(r[1])}</td><td>{E(r[2])}</td></tr>" for r in RAEUME_HEUTE + RAEUME_DAMALS)
    overf = "".join(f"<tr><td><b>{f[0]}</b></td><td>{E(f[1])}</td><td>{E(f[2])}</td></tr>" for f in FIGUREN)
    doc = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<h1>Bilderauftrag</h1>
<div class="sub">Adventskalender 2026 · Systemfehler Familie · alle Bilder für die 24 Videos</div>
<div class="box"><b>Für alle Bilder gilt</b><ul>
<li><b>Stil:</b> derselbe gemalte 3D-Bilderbuchstil wie deine Kinder-Charakterblätter und die bisherigen Räume.</li>
<li><b>Räume:</b> Querformat 3:2 (1536×1024), <b>ohne Menschen</b>, ohne Text, Logos und Symbole. Die untere Bildhälfte bleibt eher frei, damit ich die Kinder hineinstellen kann.</li>
<li><b>Damals</b> in Sepia (wie Speisesaal und Schlafsaal), <b>heute</b> in Farbe. Die Räume D10–D11 sind in verblassten Farben, D12–D13 in vollen Farben.</li>
<li><b>Figuren:</b> {E(BLATT)}</li>
<li><b>Gleiches Gesicht:</b> Bei den Kindern bitte immer dieselben 9 Gesichter wie in deinen bisherigen Blättern verwenden (Charakter 01 bis 09).</li>
<li><b>Dateinamen</b> wie angegeben. Dann kann ich jedes Bild sofort zuordnen.</li>
</ul></div>
<h2>Übersicht</h2>
<table><tr><th>Nr</th><th>Raum</th><th>Tage</th></tr>{over}</table>
<table style="margin-top:4mm"><tr><th>Nr</th><th>Figuren</th><th>Tage</th></tr>{overf}</table>
<p style="margin-top:4mm">Insgesamt: <b>23 Räume</b> und <b>Figurenblätter</b> (F1–F3 je 9 Blätter, F11 4 Blätter, die übrigen je 1–2 Blätter).</p>
<h2 class="pb">A · Räume heute (Farbe)</h2>{''.join(raum_card(r) for r in RAEUME_HEUTE)}
<h2 class="pb">B · Räume damals (Sepia bzw. verblasst)</h2>{''.join(raum_card(r) for r in RAEUME_DAMALS)}
<h2 class="pb">C · Figuren und Posen</h2>{''.join(fig_card(f) for f in FIGUREN)}
</body></html>"""
    hpath = out.replace(".pdf", ".html")
    open(hpath, "w").write(doc)
    print("ok", out)


if __name__ == "__main__":
    main(sys.argv[1])
