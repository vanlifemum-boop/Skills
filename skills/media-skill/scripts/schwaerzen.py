#!/usr/bin/env python3
"""schwaerzen.py — Bildbereiche vor einer Veröffentlichung abdecken.

Legt undurchsichtige Kästen über Gesichter, Namen, Profilbilder oder Nummern und
schreibt das Ergebnis IMMER in eine neue Datei. Die Quelldatei wird nie verändert —
sie bleibt als unverfälschtes Beweismittel erhalten.

Braucht Pillow:   pip install Pillow

Beispiele:
    # Kasten in Pixeln: links,oben,rechts,unten
    python3 scripts/schwaerzen.py chat.png chat-anonym.png --kasten 95,98,172,180

    # Mehrere Kästen, gemischt Pixel und Prozent der Bildkante
    python3 scripts/schwaerzen.py chat.png chat-anonym.png \
        --kasten 95,98,172,180 --kasten 40%,2%,95%,6%

    # Nachsehen, wo ein Kasten landet, ohne zu speichern
    python3 scripts/schwaerzen.py chat.png --pruefen --kasten 95,98,172,180
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("Fehler: Pillow fehlt. Installieren mit:  pip install Pillow")


def _kante(wert, gesamt):
    """'120' sind Pixel, '30%' sind Prozent der Bildkante."""
    wert = wert.strip()
    if wert.endswith("%"):
        return round(float(wert[:-1].replace(",", ".")) / 100 * gesamt)
    return round(float(wert.replace(",", ".")))


def kasten_lesen(text, breite, hoehe):
    """'links,oben,rechts,unten' zu vier Pixelwerten."""
    teile = text.split(",")
    if len(teile) != 4:
        raise ValueError(f"Kasten braucht vier Werte, bekommen: {text!r}")
    links, oben, rechts, unten = (
        _kante(teile[0], breite), _kante(teile[1], hoehe),
        _kante(teile[2], breite), _kante(teile[3], hoehe),
    )
    if rechts <= links or unten <= oben:
        raise ValueError(f"Kasten ist leer oder verdreht: {text!r}")
    return links, oben, rechts, unten


def schwaerzen(quelle, ziel, kaesten, farbe="#000000", pruefen=False):
    bild = Image.open(quelle).convert("RGB")
    stift = ImageDraw.Draw(bild)

    for text in kaesten:
        links, oben, rechts, unten = kasten_lesen(text, *bild.size)
        if pruefen:
            # Nur umranden, damit man die Lage kontrollieren kann.
            stift.rectangle([links, oben, rechts, unten], outline="#ff0000", width=4)
        else:
            stift.rectangle([links, oben, rechts, unten], fill=farbe)
        print(f"  Kasten {links},{oben} bis {rechts},{unten}"
              f"  ({rechts - links}×{unten - oben} Pixel)")

    ziel = Path(ziel)
    ziel.parent.mkdir(parents=True, exist_ok=True)
    bild.save(ziel)
    print(f"Geschrieben: {ziel}")
    print(f"Original unverändert: {quelle}")
    return ziel


def main():
    zerleger = argparse.ArgumentParser(
        description="Bildbereiche mit undurchsichtigen Kästen abdecken.")
    zerleger.add_argument("quelle", help="Eingangsbild — wird nicht verändert")
    zerleger.add_argument("ziel", nargs="?", help="Ausgabedatei")
    zerleger.add_argument("--kasten", action="append", required=True, metavar="L,O,R,U",
                          help="links,oben,rechts,unten — Pixel oder Prozent ('30%%')")
    zerleger.add_argument("--farbe", default="#000000", help="Füllfarbe, Vorgabe Schwarz")
    zerleger.add_argument("--pruefen", action="store_true",
                          help="Kästen nur rot umranden, Vorschau nach <ziel>")
    args = zerleger.parse_args()

    quelle = Path(args.quelle)
    if not quelle.is_file():
        sys.exit(f"Fehler: {quelle} gibt es nicht.")

    ziel = args.ziel
    if ziel is None:
        zusatz = "-vorschau" if args.pruefen else "-anonym"
        ziel = quelle.with_name(quelle.stem + zusatz + quelle.suffix)
    if Path(ziel).resolve() == quelle.resolve():
        sys.exit("Fehler: Ziel darf nicht die Quelldatei sein.")

    try:
        schwaerzen(quelle, ziel, args.kasten, args.farbe, args.pruefen)
    except ValueError as fehler:
        sys.exit(f"Fehler: {fehler}")


if __name__ == "__main__":
    main()
