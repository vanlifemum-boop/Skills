#!/usr/bin/env python3
"""schnitt_bauen.py — aus Abschnitten und Szenen die Schnittliste bauen.

Zwölf KI-Clips à 8 Sekunden müssen sechs Minuten tragen. Stumpf geloopt wird das
zäh, deshalb wechselt jeder Abschnitt zwischen dem Clip (als Boomerang, also
vorwärts und rückwärts) und einem Einschub: einer Kamerafahrt über einen
Posterausschnitt oder einer Karteikarte. Der Wechsel hält das Bild in Bewegung,
ohne einen einzigen weiteren Credit zu kosten.

    python3 schnitt_bauen.py
"""

import json
from pathlib import Path

from timing_bauen import FENSTER

HIER = Path(__file__).parent

VORSPANN = 4.0          # Titelkarte, bevor der erste Text kommt
CLIP_BLOCK = 14.0       # so lange läuft ein Clip am Stück
EINSCHUB_BLOCK = 6.0    # so lange ein Einschub
MIN_BLOCK = 2.5         # kürzere Reste werden angehängt statt eigenständig

# Ausschnitte des Posters (x, y, Breite, Höhe als Anteile der Kantenlänge),
# am Kontaktbogen geprüft: jeder Ausschnitt zeigt genau ein Motiv.
# Bewusst großzügig geschnitten: das Poster hat nur 1254 px Kantenlänge, ein enger
# Ausschnitt müsste für 1080p sechsfach hochgerechnet werden und wird matschig.
AUSSCHNITTE = {
    "gesicht":      (0.28, 0.17, 0.46, 0.36),
    "stempelhand":  (0.22, 0.38, 0.34, 0.30),
    "ergebnis":     (0.28, 0.60, 0.48, 0.24),
    "ordner":       (0.00, 0.24, 0.26, 0.42),
    "tasse":        (0.02, 0.60, 0.28, 0.26),
    "minitroll":    (0.72, 0.34, 0.28, 0.28),
    "schild":       (0.70, 0.20, 0.30, 0.22),
    "schreibtisch": (0.18, 0.52, 0.64, 0.40),
}

# Welche Einschübe zu welchem Abschnitt passen — inhaltlich, nicht zufällig.
EINSCHUEBE = {
    "intro":           [("poster", "schreibtisch"), ("poster", "gesicht")],
    "strophe-1":       [("poster", "tasse"), ("poster", "ordner"), ("poster", "gesicht")],
    "pre-chorus-1":    [("grafik", "akte-mutter"), ("grafik", "akte-vater"),
                        ("grafik", "akte-kind"), ("grafik", "akte-wahrheit")],
    "refrain-1":       [("poster", "ergebnis"), ("poster", "stempelhand"),
                        ("poster", "ordner")],
    "strophe-2":       [("poster", "gesicht"), ("poster", "schreibtisch")],
    "pre-chorus-2":    [("poster", "gesicht"), ("poster", "ergebnis")],
    "refrain-2":       [("poster", "stempelhand"), ("poster", "ordner"),
                        ("poster", "ergebnis")],
    "bridge":          [("poster", "schild"), ("poster", "gesicht")],
    "break":           [("poster", "stempelhand"), ("poster", "ergebnis")],
    "strophe-3":       [("poster", "minitroll"), ("poster", "schreibtisch")],
    "strophe-3-bruch": [("poster", "gesicht"), ("poster", "minitroll")],
    "refrain-3":       [("grafik", "akte-wahrheit"), ("poster", "ergebnis"),
                        ("poster", "schreibtisch"), ("poster", "gesicht")],
    "outro":           [("poster", "tasse"), ("poster", "ergebnis"),
                        ("poster", "schreibtisch")],
}


def bloecke(von, bis, clip, einschuebe):
    """Wechselt zwischen Clip und Einschub, bis das Fenster voll ist."""
    teile = []
    t = von
    nummer = 0
    while bis - t > 0.01:
        ist_clip = (nummer % 2 == 0) and clip is not None
        laenge = CLIP_BLOCK if ist_clip else EINSCHUB_BLOCK
        ende = min(t + laenge, bis)

        # Reste, die zu kurz für einen eigenen Block wären, an den vorigen hängen.
        if bis - ende < MIN_BLOCK:
            ende = bis

        if ist_clip:
            teile.append({"von": round(t, 3), "bis": round(ende, 3),
                          "typ": "clip", "quelle": clip})
        else:
            typ, quelle = einschuebe[(nummer // 2) % len(einschuebe)]
            teile.append({"von": round(t, 3), "bis": round(ende, 3),
                          "typ": typ, "quelle": quelle})
        t = ende
        nummer += 1
    return teile


def main():
    szenen = json.loads((HIER / "szenen.json").read_text(encoding="utf-8"))
    analyse = json.loads((HIER / "analyse.json").read_text(encoding="utf-8"))
    dauer = analyse["dauer"]

    clip_je_abschnitt = {s["abschnitt"]: s["name"] for s in szenen["szenen"]}

    teile = [{"von": 0.0, "bis": VORSPANN, "typ": "grafik", "quelle": "titel"}]

    for name, von, bis in FENSTER:
        von = max(von, teile[-1]["bis"])
        if bis <= von:
            continue
        teile += bloecke(von, bis, clip_je_abschnitt.get(name),
                         EINSCHUEBE.get(name, [("poster", "schreibtisch")]))

    # Der Rest bis zum Songende ist der Abspann.
    if dauer - teile[-1]["bis"] > 0.5:
        teile.append({"von": teile[-1]["bis"], "bis": round(dauer, 3),
                      "typ": "grafik", "quelle": "schluss"})

    plan = {"dauer": round(dauer, 3), "ausschnitte": AUSSCHNITTE, "teile": teile}
    ziel = HIER / "schnitt.json"
    ziel.write_text(json.dumps(plan, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(f"{len(teile)} Teile → {ziel.name}")
    art = {}
    for teil in teile:
        art[teil["typ"]] = art.get(teil["typ"], 0) + teil["bis"] - teil["von"]
    for typ, sekunden in sorted(art.items()):
        print(f"  {typ:<8} {sekunden:6.1f} s  ({sekunden / dauer * 100:4.1f} %)")

    luecken = [(a["bis"], b["von"]) for a, b in zip(teile, teile[1:]) if abs(a["bis"] - b["von"]) > 0.01]
    print("Lücken:", luecken or "keine")


if __name__ == "__main__":
    main()
