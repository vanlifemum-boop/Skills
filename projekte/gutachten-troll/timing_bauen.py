#!/usr/bin/env python3
"""timing_bauen.py — Textzeilen auf die Zeitachse legen.

Zwei Zutaten: die Abschnittsfenster (Tabelle unten, von Hand korrigierbar) und die
gemessenen Gesangsphrasen aus analyse.json. Innerhalb eines Fensters werden die
Phrasen auf die Zeilenzahl gebracht — zu viele werden an den kleinsten Lücken
verschmolzen, zu wenige an der längsten Phrase nach Silbengewicht geteilt. Danach
sitzt jede Zeile auf einem gemessenen Stimmeinsatz statt auf einer Schätzung.

Korrigieren heißt: FENSTER anpassen und neu laufen lassen.

    python3 timing_bauen.py
"""

import json
from pathlib import Path

HIER = Path(__file__).parent

# Abschnittsfenster in Sekunden — die eine Stellschraube dieses Skripts.
# Hergeleitet aus dem Pegelprofil (drei laute Blöcke = drei Refrains) und den
# mit silencedetect gemessenen Sprechpausen bei 116,6 s · 204–220 s · 300–331 s.
FENSTER = [
    ("intro",            4.0,   20.4),
    ("strophe-1",       20.4,   44.5),
    ("pre-chorus-1",    44.5,   56.5),
    ("refrain-1",       56.5,   86.5),
    ("strophe-2",       86.5,  110.5),
    ("pre-chorus-2",   110.5,  119.5),
    ("refrain-2",      119.5,  150.5),
    ("bridge",         150.5,  171.5),
    ("break",          171.5,  187.5),
    ("strophe-3",      187.5,  203.5),
    ("strophe-3-bruch", 203.5, 223.0),
    ("refrain-3",      223.0,  279.5),
    ("outro",          279.5,  332.0),
]

# Text erscheint eine Spur vor dem Stimmeinsatz — sonst wirkt er hinterher.
VORLAUF = 0.18
# Kürzeste und längste Standzeit einer Zeile.
MIN_STAND, MAX_STAND = 0.9, 6.0


def verschmelzen(phrasen, hoechstens):
    """Verschmilzt an den kleinsten Lücken, bis höchstens `hoechstens` übrig sind."""
    phrasen = [dict(p) for p in phrasen]
    while len(phrasen) > hoechstens:
        luecken = [(phrasen[i + 1]["start"] - phrasen[i]["ende"], i)
                   for i in range(len(phrasen) - 1)]
        _, i = min(luecken)
        phrasen[i] = {"start": phrasen[i]["start"], "ende": phrasen[i + 1]["ende"]}
        del phrasen[i + 1]
    return phrasen


def zeilen_verteilen(phrasen, silben):
    """Ordnet jeder Zeile ein Zeitfenster zu.

    Erst werden überzählige Phrasen verschmolzen. Dann bekommt jede Phrase eine
    zusammenhängende Gruppe von Zeilen — so aufgeteilt, dass die Dauer der Phrase
    möglichst gut zum Silbenanteil ihrer Zeilen passt (kleine dynamische
    Programmierung). Innerhalb einer Phrase teilen sich mehrere Zeilen die Zeit
    nach Silben.
    """
    anzahl = len(silben)
    phrasen = verschmelzen(phrasen, anzahl)
    p_anz = len(phrasen)

    dauern = [p["ende"] - p["start"] for p in phrasen]
    dauer_summe = sum(dauern) or 1.0
    silben_summe = sum(silben) or 1.0

    # kosten[i][j]: Phrase i bekommt die Zeilen j…k — Abweichung der Anteile.
    unendlich = float("inf")
    tabelle = [[unendlich] * (anzahl + 1) for _ in range(p_anz + 1)]
    weg = [[0] * (anzahl + 1) for _ in range(p_anz + 1)]
    tabelle[0][0] = 0.0

    for i in range(1, p_anz + 1):
        anteil_zeit = dauern[i - 1] / dauer_summe
        for j in range(i, anzahl - (p_anz - i) + 1):
            for k in range(i - 1, j):
                if tabelle[i - 1][k] == unendlich:
                    continue
                anteil_silben = sum(silben[k:j]) / silben_summe
                kosten = tabelle[i - 1][k] + abs(anteil_zeit - anteil_silben)
                if kosten < tabelle[i][j]:
                    tabelle[i][j] = kosten
                    weg[i][j] = k

    # Rückwärts auflösen.
    grenzen = [anzahl]
    j = anzahl
    for i in range(p_anz, 0, -1):
        j = weg[i][j]
        grenzen.append(j)
    grenzen.reverse()

    fenster = []
    for i, phrase in enumerate(phrasen):
        von_zeile, bis_zeile = grenzen[i], grenzen[i + 1]
        gruppe = silben[von_zeile:bis_zeile]
        gesamt = sum(gruppe) or 1
        t = phrase["start"]
        spanne = phrase["ende"] - phrase["start"]
        for s in gruppe:
            ende = t + spanne * s / gesamt
            fenster.append({"start": t, "ende": ende})
            t = ende
    return fenster


def main():
    liedtext = json.loads((HIER / "liedtext.json").read_text(encoding="utf-8"))
    analyse = json.loads((HIER / "analyse.json").read_text(encoding="utf-8"))
    alle_phrasen = analyse["phrasen"]

    nach_name = {a["name"]: a for a in liedtext["abschnitte"]}
    fehlend = [n for n, _, _ in FENSTER if n not in nach_name]
    if fehlend:
        raise SystemExit(f"Fenster ohne Abschnitt im Liedtext: {fehlend}")

    zeilen_aus = []
    bericht = []

    for name, von, bis in FENSTER:
        abschnitt = nach_name[name]
        zeilen = abschnitt["zeilen"]
        drin = [p for p in alle_phrasen if p["start"] >= von and p["start"] < bis]
        if not drin:
            # Kein Gesang gemessen: gleichmäßig über das Fenster verteilen.
            schritt = (bis - von) / len(zeilen)
            drin = [{"start": von + i * schritt, "ende": von + (i + 1) * schritt}
                    for i in range(len(zeilen))]

        roh = len(drin)
        silben = [z["silben"] for z in zeilen]
        passend = zeilen_verteilen(drin, silben)
        bericht.append((name, von, bis, roh, len(zeilen)))

        for zeile, phrase in zip(zeilen, passend):
            start = max(phrase["start"] - VORLAUF, 0.0)
            zeilen_aus.append({
                "nr": zeile["nr"],
                "abschnitt": name,
                "art": zeile["art"],
                "text": zeile["text"],
                "silben": zeile["silben"],
                "start": round(start, 3),
                "ende": round(phrase["ende"], 3),
            })

    # Standzeiten glätten: bis zum nächsten Einsatz stehen lassen, aber gedeckelt.
    for i, eintrag in enumerate(zeilen_aus):
        naechster = zeilen_aus[i + 1]["start"] if i + 1 < len(zeilen_aus) else analyse["dauer"]
        ende = min(max(eintrag["ende"], eintrag["start"] + MIN_STAND),
                   eintrag["start"] + MAX_STAND, naechster - 0.04)
        eintrag["ende"] = round(max(ende, eintrag["start"] + 0.4), 3)

    ziel = HIER / "timing.json"
    ziel.write_text(json.dumps(
        {"quelle": "timing_bauen.py", "dauer": analyse["dauer"], "zeilen": zeilen_aus},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(f"{len(zeilen_aus)} Zeilen → {ziel.name}\n")
    print(f"{'Abschnitt':<17}{'Fenster':<18}{'Phrasen':>8}{'Zeilen':>8}  Anpassung")
    for name, von, bis, roh, zeilen in bericht:
        art = "passt" if roh == zeilen else (f"{roh - zeilen} verschmolzen" if roh > zeilen
                                             else f"{zeilen - roh} geteilt")
        print(f"{name:<17}{von:6.1f}–{bis:<11.1f}{roh:>8}{zeilen:>8}  {art}")


if __name__ == "__main__":
    main()
