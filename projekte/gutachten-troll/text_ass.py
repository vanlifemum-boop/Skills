#!/usr/bin/env python3
"""text_ass.py — timing.json in ASS-Untertitel setzen, in der Optik des Posters.

Farben und Schrift kommen vom Plakat: Archivo Black (aus docs/fonts), Creme
251/237/215 und das Pink 217/93/114, beide direkt aus dem Bild gemessen.
Drei Sorten Zeilen:

  gesungen    Versalien, Creme, Schlüsselwörter pink
  gesprochen  gemischte Schreibung, ruhiger, etwas kleiner
  effekt      KRAWUMM! — groß, pink, mit kurzem Aufschlag

    python3 text_ass.py --format 16-9
    python3 text_ass.py --format 9-16
"""

import argparse
import json
import re
from pathlib import Path

HIER = Path(__file__).parent
SCHRIFT_NAME = "Archivo Black"

# ASS nimmt Farben als &HAABBGGRR& — also blau zuerst.
CREME = "&H00D7EDFB&"
PINK = "&H00725DD9&"
SCHWARZ = "&H00000000&"
SCHATTEN = "&H96000000&"

FORMATE = {
    "16-9": {
        "breite": 1920, "hoehe": 1080,
        "gesungen": 66, "gesprochen": 54, "effekt": 128,
        "rand_unten": 96, "umbruch": 34,
    },
    "9-16": {
        "breite": 1080, "hoehe": 1920,
        "gesungen": 68, "gesprochen": 56, "effekt": 132,
        "rand_unten": 520, "umbruch": 22,
    },
}

# Diese Wörter tragen die Pointe — sie werden pink gesetzt.
SCHLUESSELWOERTER = [
    "gutachten-troll", "gutachten", "wahrheit", "menschen", "stempel", "akten",
    "aktenordner", "aktenberg", "aktenrand", "objektiv", "objektivität", "neutral",
    "wissenschaftlich", "zuhören", "papier", "formular", "kästchen", "randvoll",
    "krawumm", "klapp", "raschel", "gesamtbild", "zauberstab", "zauberbuch",
    "vermutung", "unbekannt", "wirklichkeit", "emotionen", "bindung",
]


def kopf(fmt):
    return f"""[Script Info]
; Erzeugt von text_ass.py — nicht von Hand ändern, sondern das Skript.
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: {fmt['breite']}
PlayResY: {fmt['hoehe']}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: gesungen,{SCHRIFT_NAME},{fmt['gesungen']},{CREME},{CREME},{SCHWARZ},{SCHATTEN},0,0,0,0,100,100,1,0,1,5,3,2,80,80,{fmt['rand_unten']},1
Style: gesprochen,{SCHRIFT_NAME},{fmt['gesprochen']},{CREME},{CREME},{SCHWARZ},{SCHATTEN},0,0,0,0,96,96,2,0,1,4,3,2,80,80,{fmt['rand_unten']},1
Style: effekt,{SCHRIFT_NAME},{fmt['effekt']},{PINK},{PINK},{SCHWARZ},{SCHATTEN},0,0,0,0,100,100,4,0,1,7,4,5,40,40,40,1
Style: zeitcode,{SCHRIFT_NAME},28,&H0000FFFF&,&H0000FFFF&,{SCHWARZ},&HC8000000&,0,0,0,0,100,100,0,0,3,3,0,7,24,24,24,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def zeit(sekunden):
    """0:00:01.23 — ASS rechnet in Hundertstel."""
    sekunden = max(sekunden, 0)
    stunden, rest = divmod(sekunden, 3600)
    minuten, sek = divmod(rest, 60)
    return f"{int(stunden)}:{int(minuten):02d}:{sek:05.2f}"


def umbrechen(text, breite):
    """Weicher Umbruch auf höchstens zwei Zeilen — mehr verdeckt zu viel Bild."""
    if len(text) <= breite:
        return text
    woerter = text.split()
    zeilen, aktuell = [], ""
    for wort in woerter:
        probe = f"{aktuell} {wort}".strip()
        if len(probe) > breite and aktuell:
            zeilen.append(aktuell)
            aktuell = wort
        else:
            aktuell = probe
    zeilen.append(aktuell)
    if len(zeilen) > 2:
        # Gleichmäßig auf zwei Zeilen umlegen, statt drei kurze zu stapeln.
        mitte = len(woerter) // 2
        zeilen = [" ".join(woerter[:mitte]), " ".join(woerter[mitte:])]
    return "\\N".join(zeilen)


def einfaerben(text):
    """Schlüsselwörter pink, der Rest bleibt creme."""
    def ersetzen(treffer):
        wort = treffer.group(0)
        if wort.lower().strip("„“\"',.!?…–-") in SCHLUESSELWOERTER:
            return f"{{\\c{PINK}}}{wort}{{\\c{CREME}}}"
        return wort

    return re.sub(r"[^\s]+", ersetzen, text)


def ereignis(eintrag, fmt):
    art = eintrag["art"]
    text = eintrag["text"]

    if art == "effekt":
        # Kurzer Aufschlag: von 130 % auf 100 % in 140 ms.
        inhalt = (f"{{\\fad(60,180)\\fscx130\\fscy130"
                  f"\\t(0,140,\\fscx100\\fscy100)}}{text.upper()}")
        return f"Dialogue: 0,{zeit(eintrag['start'])},{zeit(eintrag['ende'])},effekt,,0,0,0,,{inhalt}"

    if art == "gesprochen":
        gesetzt = umbrechen(text, fmt["umbruch"] + 4)
        inhalt = f"{{\\fad(160,200)}}{einfaerben(gesetzt)}"
        return f"Dialogue: 0,{zeit(eintrag['start'])},{zeit(eintrag['ende'])},gesprochen,,0,0,0,,{inhalt}"

    gesetzt = umbrechen(text.upper(), fmt["umbruch"])
    inhalt = f"{{\\fad(120,160)}}{einfaerben(gesetzt)}"
    return f"Dialogue: 0,{zeit(eintrag['start'])},{zeit(eintrag['ende'])},gesungen,,0,0,0,,{inhalt}"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--format", choices=sorted(FORMATE), default="16-9")
    p.add_argument("--timing", default=str(HIER / "timing.json"))
    p.add_argument("--ziel")
    p.add_argument("--zeitcode", action="store_true",
                   help="laufende Zeit oben links — nur für die Sync-Vorschau, "
                        "damit Korrekturstellen benannt werden können")
    args = p.parse_args()

    fmt = FORMATE[args.format]
    timing = json.loads(Path(args.timing).read_text(encoding="utf-8"))

    zeilen = [kopf(fmt)]
    zeilen += [ereignis(e, fmt) for e in timing["zeilen"]]

    if args.zeitcode:
        # Sekundenweise Einblendung — ffmpeg hat in dieser Umgebung kein drawtext,
        # also macht libass auch das.
        for sekunde in range(int(timing["dauer"]) + 1):
            marke = f"{sekunde // 60}:{sekunde % 60:02d}"
            zeilen.append(f"Dialogue: 1,{zeit(sekunde)},{zeit(sekunde + 1)},"
                          f"zeitcode,,0,0,0,,{marke}")

    ziel = Path(args.ziel) if args.ziel else HIER / "bauplatz" / f"text_{args.format}.ass"
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text("\n".join(zeilen) + "\n", encoding="utf-8")
    print(f"{len(timing['zeilen'])} Zeilen → {ziel}")


if __name__ == "__main__":
    main()
