#!/usr/bin/env python3
"""pruefstreifen.py — Analyse und Timing als Bild, zum Nachsehen mit dem Auge.

Ohne Spracherkennung ist das Auge das Kontrollinstrument: der Streifen zeigt
übereinander Gesamtpegel, Gesangskurve, erkannte Phrasen und — sobald timing.json
existiert — die zugeordneten Textzeilen. Sitzt eine Zeilenmarke neben statt auf
einer Phrase, sieht man das sofort.

    python3 pruefstreifen.py --uebersicht          # der ganze Song auf einem Bild
    python3 pruefstreifen.py --von 0 --bis 120     # 30-Sekunden-Streifen des Bereichs
"""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HIER = Path(__file__).parent
AUSGABE = HIER / "bauplatz" / "pruefstreifen"

SCHRIFT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SCHRIFT_FETT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

GRUND = (18, 18, 22)
GITTER = (48, 48, 58)
TAKTLINIE = (70, 70, 90)
PEGEL = (90, 110, 140)
GESANG = (250, 200, 90)
SCHWELLE_FARBE = (200, 70, 70)
PHRASE = (70, 180, 140)
ZEILE = (240, 90, 150)
TEXT = (235, 235, 240)


def schrift(groesse, fett=False):
    return ImageFont.truetype(SCHRIFT_FETT if fett else SCHRIFT, groesse)


def streifen_zeichnen(analyse, timing, von, bis, breite, hoehe=430):
    """Ein Bild für den Zeitbereich [von, bis)."""
    spanne = bis - von
    px = breite / spanne
    bild = Image.new("RGB", (breite, hoehe), GRUND)
    stift = ImageDraw.Draw(bild)

    def x(t):
        return (t - von) * px

    # --- Zeitachse, Sekundenraster, Taktlinien -----------------------------
    takt = analyse["schlag_abstand"]
    erster = analyse["erster_schlag"]
    schlag_nr = int((von - erster) / takt)
    t = erster + schlag_nr * takt
    while t < bis:
        if t >= von:
            # Jeder vierte Schlag ist ein Taktanfang und wird kräftiger gezeichnet.
            ist_takt = schlag_nr % 4 == 0
            stift.line([(x(t), 26), (x(t), hoehe)], fill=TAKTLINIE if ist_takt else GITTER,
                       width=2 if ist_takt else 1)
        t += takt
        schlag_nr += 1

    schritt = 1 if spanne <= 40 else 5
    sekunde = int(von) - int(von) % schritt
    while sekunde < bis:
        if sekunde >= von:
            stift.line([(x(sekunde), 0), (x(sekunde), 20)], fill=(120, 120, 130))
            stift.text((x(sekunde) + 3, 4), f"{int(sekunde // 60)}:{int(sekunde % 60):02d}",
                       font=schrift(13), fill=TEXT)
        sekunde += schritt

    # --- Gesamtpegel und Gesangskurve --------------------------------------
    aufl = analyse["aufloesung"]
    gesamt = analyse["huelle_gesamt"]
    gesang = analyse["huelle_gesang"]

    def kurve(werte, oben, unten, farbe, skala):
        punkte = []
        for spalte in range(breite):
            t = von + spalte / px
            i = int(t / aufl)
            if 0 <= i < len(werte):
                wert = min(werte[i] / skala, 1.0)
                punkte.append((spalte, unten - wert * (unten - oben)))
        if len(punkte) > 1:
            stift.line(punkte, fill=farbe, width=1)

    stift.text((6, 34), "Pegel", font=schrift(12), fill=PEGEL)
    kurve(gesamt, 50, 170, PEGEL, 0.55)

    stift.text((6, 182), "Gesang (Mitte minus Seite, lokal normiert)", font=schrift(12), fill=GESANG)
    # Schwellenlinie bei 1,35 — der Wert aus phrasen_finden.
    schwelle_y = 320 - min(1.35 / 3.0, 1.0) * (320 - 198)
    stift.line([(0, schwelle_y), (breite, schwelle_y)], fill=SCHWELLE_FARBE, width=1)
    kurve(gesang, 198, 320, GESANG, 3.0)

    # --- Phrasen ------------------------------------------------------------
    for i, p in enumerate(analyse["phrasen"]):
        if p["ende"] < von or p["start"] > bis:
            continue
        stift.rectangle([x(p["start"]), 328, x(p["ende"]), 344], fill=PHRASE)
        if (p["ende"] - p["start"]) * px > 22:
            stift.text((x(p["start"]) + 2, 329), str(i), font=schrift(11), fill=GRUND)

    # --- Textzeilen aus timing.json -----------------------------------------
    if timing:
        etage = 0
        for eintrag in timing["zeilen"]:
            if eintrag["ende"] < von or eintrag["start"] > bis:
                continue
            xs, xe = x(eintrag["start"]), x(eintrag["ende"])
            y = 352 + (etage % 2) * 38
            stift.rectangle([xs, y, xe, y + 34], outline=ZEILE, width=2)
            stift.line([(xs, 328), (xs, y)], fill=ZEILE, width=1)
            text = f"{eintrag['nr']} {eintrag['text']}"
            if xe - xs > 40:
                stift.text((xs + 4, y + 3), text[: int((xe - xs) / 6.5)],
                           font=schrift(13), fill=TEXT)
            etage += 1

    stift.rectangle([0, 0, breite - 1, hoehe - 1], outline=(60, 60, 70))
    return bild


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--analyse", default=str(HIER / "analyse.json"))
    p.add_argument("--timing", default=str(HIER / "timing.json"))
    p.add_argument("--von", type=float, default=0.0)
    p.add_argument("--bis", type=float)
    p.add_argument("--fenster", type=float, default=30.0, help="Sekunden je Streifen")
    p.add_argument("--breite", type=int, default=1900)
    p.add_argument("--uebersicht", action="store_true", help="ganzer Song auf einem Bild")
    args = p.parse_args()

    analyse = json.loads(Path(args.analyse).read_text(encoding="utf-8"))
    timing_pfad = Path(args.timing)
    timing = json.loads(timing_pfad.read_text(encoding="utf-8")) if timing_pfad.exists() else None

    AUSGABE.mkdir(parents=True, exist_ok=True)
    dauer = analyse["dauer"]
    bis = args.bis if args.bis is not None else dauer

    if args.uebersicht:
        bild = streifen_zeichnen(analyse, timing, 0, dauer, args.breite)
        ziel = AUSGABE / "uebersicht.png"
        bild.save(ziel)
        print(ziel)
        return

    t = args.von
    while t < bis:
        ende = min(t + args.fenster, bis)
        bild = streifen_zeichnen(analyse, timing, t, ende, args.breite)
        ziel = AUSGABE / f"streifen_{int(t):04d}_{int(ende):04d}.png"
        bild.save(ziel)
        print(ziel)
        t = ende


if __name__ == "__main__":
    main()
