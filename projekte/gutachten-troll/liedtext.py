#!/usr/bin/env python3
"""liedtext.py — liedtext.txt in liedtext.json übersetzen.

Zählt je Zeile die Silben (deutsche Faustregel: Vokalgruppen, Diphthonge als eine).
Die Silbenzahl ist das Gewicht, mit dem die Zeilen später auf die Gesangsphrasen
verteilt werden — eine lange Zeile bekommt mehr Zeit als eine kurze.

    python3 liedtext.py            # schreibt liedtext.json neben diese Datei
"""

import json
import re
from pathlib import Path

HIER = Path(__file__).parent
QUELLE = HIER / "liedtext.txt"
ZIEL = HIER / "liedtext.json"

# Diphthonge zuerst ersetzen, sonst zählt „au" als zwei Silben.
DIPHTHONGE = ("eau", "äu", "au", "ei", "ai", "eu", "ie", "oi", "ui")
VOKALE = "aeiouäöüy"


def silben(zeile):
    """Grobe Silbenzahl einer deutschen Zeile — Vokalgruppen zählen."""
    wort_silben = 0
    for wort in re.findall(r"[a-zA-ZäöüÄÖÜß']+", zeile.lower()):
        for diph in DIPHTHONGE:
            wort = wort.replace(diph, "•")
        gruppen = re.findall(r"[" + VOKALE + "•]+", wort)
        anzahl = len(gruppen)
        # Ein stummes End-e zählt nicht als eigene Silbe, außer das Wort wäre sonst leer.
        if anzahl > 1 and wort.endswith("e") and not wort.endswith(("ee", "ie")):
            anzahl -= 1
        wort_silben += max(anzahl, 1)
    return max(wort_silben, 1)


def einlesen():
    abschnitte = []
    aktuell = None
    for roh in QUELLE.read_text(encoding="utf-8").splitlines():
        zeile = roh.strip()
        if not zeile or zeile.startswith("#"):
            continue
        if zeile.startswith("=="):
            name, _, art = zeile[2:].partition("|")
            aktuell = {"name": name.strip(), "art": art.strip() or "gesungen", "zeilen": []}
            abschnitte.append(aktuell)
            continue
        if aktuell is None:
            raise SystemExit(f"Textzeile vor dem ersten Abschnittskopf: {zeile!r}")
        effekt = zeile.startswith("*")
        text = zeile[1:].strip() if effekt else zeile
        aktuell["zeilen"].append({"text": text, "effekt": effekt, "silben": silben(text)})
    return abschnitte


def main():
    abschnitte = einlesen()
    nummer = 0
    for abschnitt in abschnitte:
        for zeile in abschnitt["zeilen"]:
            zeile["nr"] = nummer
            zeile["abschnitt"] = abschnitt["name"]
            zeile["art"] = "effekt" if zeile["effekt"] else abschnitt["art"]
            nummer += 1

    daten = {
        "titel": "Der Gutachten-Troll",
        "zeilen_gesamt": nummer,
        "abschnitte": abschnitte,
    }
    ZIEL.write_text(json.dumps(daten, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"{nummer} Zeilen in {len(abschnitte)} Abschnitten → {ZIEL.name}")
    for abschnitt in abschnitte:
        summe = sum(z["silben"] for z in abschnitt["zeilen"])
        print(f"  {abschnitt['name']:<16} {abschnitt['art']:<11} "
              f"{len(abschnitt['zeilen']):>2} Zeilen, {summe:>3} Silben")


if __name__ == "__main__":
    main()
