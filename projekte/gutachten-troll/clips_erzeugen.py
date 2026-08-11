#!/usr/bin/env python3
"""clips_erzeugen.py — die Szenen aus szenen.json über kie.ai erzeugen.

Fährt die Liste der Reihe nach ab und ruft für jede Szene `kie.py erzeugen`.
Wiederaufnehmbar: was schon in clips/ liegt, wird übersprungen — ein Abbruch
kostet also kein zweites Mal. Vor dem ersten Auftrag steht der Kostenvoranschlag
für den ganzen Lauf, und ohne --los passiert gar nichts.

    python3 clips_erzeugen.py                 # nur rechnen
    python3 clips_erzeugen.py --los           # erzeugen
    python3 clips_erzeugen.py --los --nur stempel-schlag
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).parent
KIE = HIER / ".." / ".." / "skills" / "media-skill" / "scripts" / "kie.py"
CLIPS = HIER / "bauplatz" / "clips"
POSTER = HIER / "material" / "poster.jpg"


def preis(modell, aufloesung, sekunden, anzahl):
    ausgabe = subprocess.run(
        [sys.executable, str(KIE), "preis", "--modell", modell,
         "--aufloesung", aufloesung, "--sekunden", str(sekunden),
         "--anzahl", str(anzahl)],
        capture_output=True, text=True, check=True).stdout
    return ausgabe.strip()


def guthaben():
    ausgabe = subprocess.run([sys.executable, str(KIE), "guthaben"],
                             capture_output=True, text=True, check=True).stdout
    return ausgabe.strip()


def neueste_datei(ordner):
    dateien = [d for d in ordner.glob("*.mp4")]
    return max(dateien, key=lambda d: d.stat().st_mtime) if dateien else None


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--los", action="store_true", help="wirklich erzeugen (kostet Credits)")
    p.add_argument("--nur", help="nur diese eine Szene")
    p.add_argument("--projekt", default="gutachten-troll")
    args = p.parse_args()

    plan = json.loads((HIER / "szenen.json").read_text(encoding="utf-8"))
    szenen = plan["szenen"]
    if args.nur:
        szenen = [s for s in szenen if s["name"] == args.nur]
        if not szenen:
            raise SystemExit(f"Keine Szene namens {args.nur!r}")

    CLIPS.mkdir(parents=True, exist_ok=True)
    offen = [s for s in szenen if not (CLIPS / f"{s['name']}.mp4").exists()]

    print(f"{len(szenen)} Szenen, davon {len(offen)} offen")
    print(f"Kosten für die offenen: {preis(plan['modell'], plan['aufloesung'], plan['sekunden'], len(offen))}")
    print(guthaben())

    if not args.los:
        print("\nNichts erzeugt — mit --los starten.")
        return 0

    medien = Path.home() / "Medien"
    for i, szene in enumerate(offen, 1):
        ziel = CLIPS / f"{szene['name']}.mp4"
        print(f"\n[{i}/{len(offen)}] {szene['name']} — {szene['beschreibung']}")

        prompt = f"{szene['prompt']} {plan['stiltreue']}"
        befehl = [
            sys.executable, str(KIE), "erzeugen",
            "--modell", plan["modell"],
            "--aufloesung", plan["aufloesung"],
            "--sekunden", str(plan["sekunden"]),
            "--bild", str(POSTER),
            "--extra", json.dumps({"aspect_ratio": plan["seitenverhaeltnis"]}),
            "--prompt", prompt,
            "--projekt", args.projekt,
        ]
        lauf = subprocess.run(befehl, text=True)
        if lauf.returncode != 0:
            print(f"  ✗ {szene['name']} fehlgeschlagen — weiter mit der nächsten Szene.",
                  file=sys.stderr)
            continue

        # kie.py legt unter ~/Medien/<datum>-<projekt>/NN.mp4 ab; von dort holen
        # wir den Clip unter seinen sprechenden Namen.
        ordner = sorted(medien.glob(f"*-{args.projekt}"))
        neu = neueste_datei(ordner[-1]) if ordner else None
        if neu:
            shutil.copy2(neu, ziel)
            print(f"  → {ziel.relative_to(HIER)}")

    fertig = sorted(CLIPS.glob("*.mp4"))
    print(f"\n{len(fertig)} von {len(plan['szenen'])} Clips liegen in {CLIPS.relative_to(HIER)}")
    print(guthaben())
    return 0


if __name__ == "__main__":
    sys.exit(main())
