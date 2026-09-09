#!/usr/bin/env python3
"""bilder_einsetzen.py — die Bildwelt in die HTML-Schulung einsetzen.

Liest die Vorlage mit den {{IMG_*}}-Platzhaltern und out/bilder.json und
schreibt eine eigenstaendige HTML-Datei, in der jedes Bild als Data-URI steckt.

Die Vorlage bleibt unangetastet — nur so laesst sich der Schritt wiederholen,
wenn ein Motiv nachgezogen wurde. Das Ergebnis ist die teilbare Datei.

    python3 bilder_einsetzen.py
    python3 bilder_einsetzen.py --ziel ../fertig.html

Die Platzhalter stehen an zwei Stellen in unterschiedlicher Form:

    <div class="bild"><span>{{IMG_HERO}}</span></div>   direkt im Markup
    bild:"{{IMG_L1}}"                                   als Feld der Level-Daten

Das <span> ist der Leerzustand (graue Versalien mittig). Gefuellt gehoert dort
ein <img>, fuer das das Stylesheet mit .bild img bereits alles mitbringt.
Deshalb wird nicht der Platzhalter ersetzt, sondern das ganze <span> — sonst
stuende die Data-URI als sichtbarer Text in der Seite.
"""

import argparse
import json
import re
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
VORLAGE = HIER.parent / "gutachten-schulung.html"
BILDER = HIER / "out" / "bilder.json"
ZIEL = HIER.parent / "gutachten-schulung.fertig.html"

# Der Renderer der Level-Bilder. Er setzt den Feldwert als Text in ein <span>;
# sobald dort eine Data-URI steht, muss daraus ein <img> werden.
RENDERER_ALT = 's.appendChild(el("div","bild",`<span>${l.bild}</span>`));'
RENDERER_NEU = 's.appendChild(el("div","bild",`<img src="${l.bild}" alt="">`));'


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--vorlage", type=Path, default=VORLAGE)
    p.add_argument("--bilder", type=Path, default=BILDER)
    p.add_argument("--ziel", type=Path, default=ZIEL)
    args = p.parse_args()

    for pfad in (args.vorlage, args.bilder):
        if not pfad.exists():
            sys.exit(f"fehlt: {pfad}")

    html = args.vorlage.read_text(encoding="utf-8")
    bilder = json.loads(args.bilder.read_text(encoding="utf-8"))

    offen = set(re.findall(r"\{\{(IMG_[A-Z0-9_]+)\}\}", html))
    if not offen:
        sys.exit(
            "Die Vorlage enthaelt keine {{IMG_*}}-Platzhalter mehr.\n"
            "Vermutlich zeigt --vorlage schon auf eine fertige Datei."
        )

    fehlend = sorted(offen - set(bilder))
    if fehlend:
        sys.exit(
            "Fuer diese Platzhalter fehlt ein Bild in bilder.json:\n  "
            + ", ".join(fehlend)
            + "\nNachziehen mit:  python3 kie_bilder.py motive --ref-url … --nur "
            + ",".join(fehlend)
        )

    ungenutzt = sorted(set(bilder) - offen)

    # 1) Der Renderer muss zuerst umgestellt werden — danach ist das <span>
    #    im Markup nicht mehr die einzige Fundstelle des Musters.
    if RENDERER_ALT not in html:
        sys.exit(
            "Der erwartete Renderer der Level-Bilder wurde nicht gefunden.\n"
            "Die Vorlage hat sich geaendert, das Skript muss nachgezogen werden.\n"
            f"gesucht: {RENDERER_ALT}"
        )
    html = html.replace(RENDERER_ALT, RENDERER_NEU)

    # 2) Direkt im Markup stehende Platzhalter samt umgebendem <span> ersetzen.
    def als_img(m: re.Match) -> str:
        return f'<img src="{bilder[m.group(1)]}" alt="">'

    html, n_markup = re.subn(
        r"<span>\{\{(IMG_[A-Z0-9_]+)\}\}</span>", als_img, html
    )

    # 3) Verbliebene Platzhalter sind Feldwerte der Level-Daten — dort ist der
    #    nackte Ersatz richtig, weil der Renderer die URI jetzt als src setzt.
    html, n_daten = re.subn(
        r"\{\{(IMG_[A-Z0-9_]+)\}\}", lambda m: bilder[m.group(1)], html
    )

    rest = re.findall(r"\{\{[A-Z0-9_]+\}\}", html)
    if rest:
        sys.exit(f"Es blieben Platzhalter uebrig: {sorted(set(rest))}")

    args.ziel.write_text(html, encoding="utf-8")

    groesse = args.ziel.stat().st_size / 1_048_576
    print(f"{n_markup} Bilder im Markup, {n_daten} in den Level-Daten")
    print(f"→ {args.ziel}  ({groesse:.1f} MB)")
    if ungenutzt:
        print(f"nicht verwendet: {', '.join(ungenutzt)}")
    if groesse > 50:
        print("Achtung: ueber 50 MB — Zielgroesse der Schulung ist ≤ 50 MB.")


if __name__ == "__main__":
    main()
