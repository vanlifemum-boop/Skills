#!/usr/bin/env python3
"""folge.py — arbeitet mit einer Folge der Reihe „Recht erklärt für Eltern".

Die eine Quelle der Wahrheit ist das Folgen-JSON unter folgen/. Alles andere
wird daraus erzeugt: das Sprecherskript, die Bildprompts, der Reel-Plan und die
Aufrufe an skills/media-skill/scripts/kie.py.

Unterbefehle:
    pruefen    Struktur, Zeiten und Prompts prüfen — ohne API-Aufruf
    skript     Sprecherskript als Markdown nach skript/ schreiben
    prompts    fertige Bildprompts ausgeben (Serienstil + Szene)
    kosten     Kosten des ganzen Bildmaterials ausrechnen (ruft kie.py preis)
    erzeugen   die kie.py-Aufrufe zeigen — und mit --echt auch ausführen

Nur Standardbibliothek. Alle Ausgaben auf Deutsch.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
PROJEKT = HIER.parent
STANDARD_FOLGE = PROJEKT / "folgen" / "folge-01-inobhutnahme.json"
STILDATEI = PROJEKT / "stil" / "serienstil.txt"

# Sprechtempo für die Zeitschätzung: ruhiger Erklärton, rund 145 Wörter je Minute.
WOERTER_JE_SEKUNDE = 145 / 60

# So weit darf die Bilddeckung eines Kapitels vom Ziel abweichen, bevor gewarnt wird.
TOLERANZ = 0.15

# Text zu Video, 3,5 Credits je Sekunde in 720p, ohne Ton — den liefert die
# Sprachaufnahme separat. Modelle mit "image-to-video" im Namen brauchen ein
# Startbild und lassen sich nicht ohne --extra verwenden.
STANDARD_MODELL = "bytedance/seedance-1.5-pro"

# Wörter, die einen deutschen Prompt verraten — Videomodelle verstehen nur Englisch.
DEUTSCHE_WOERTER = {
    "der", "die", "das", "und", "mit", "eine", "einen", "einem", "nicht", "auf",
    "von", "für", "ist", "wird", "im", "am", "zum", "zur", "kind", "eltern",
}


class Abbruch(Exception):
    """Ein Fehler, der als Satz gezeigt wird — nicht als Traceback."""


def kie_pfad():
    """Findet kie.py im Repo, egal von wo folge.py aufgerufen wird."""
    for eltern in [PROJEKT, *PROJEKT.parents]:
        kandidat = eltern / "skills" / "media-skill" / "scripts" / "kie.py"
        if kandidat.exists():
            return kandidat
    raise Abbruch(
        "kie.py nicht gefunden. Erwartet unter skills/media-skill/scripts/kie.py "
        "im selben Repo."
    )


def laden(pfad):
    try:
        return json.loads(Path(pfad).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise Abbruch(f"Folgen-Datei nicht gefunden: {pfad}")
    except json.JSONDecodeError as fehler:
        raise Abbruch(f"Folgen-Datei ist kein gültiges JSON: {fehler}")


def woerter(text):
    return len(re.findall(r"\S+", text))


def sprechdauer(text):
    return woerter(text) / WOERTER_JE_SEKUNDE


def stil():
    return STILDATEI.read_text(encoding="utf-8").strip()


def voller_prompt(szene, kapitel):
    """Serienstil + Szenenanweisung — das, was an kie.ai geht."""
    return (
        f"{stil()}\n\n"
        f"Shot: {szene['visual_prompt'].strip()}.\n"
        f"This shot supports an educational explanation of: {kapitel['titel']}.\n"
        f"Do not invent legal facts through visuals."
    )


# --------------------------------------------------------------------------
# pruefen
# --------------------------------------------------------------------------


def befehl_pruefen(daten, args):
    fehler, warnungen = [], []
    gesehen = set()

    for pflicht in ("serie", "folge", "titel", "kapitel"):
        if pflicht not in daten:
            fehler.append(f"Feld fehlt: {pflicht}")
    if fehler:
        raise Abbruch("\n".join(fehler))

    ziel = daten.get("bilddeckung", 0.45)

    print(f"{daten['serie']} — Folge {daten['folge']}")
    print(f"{daten['titel']}\n")
    print(f"Zieldeckung: {ziel:.0%} der Sprechzeit mit erzeugtem Material,")
    print("der Rest über Standbilder, gehaltene Einstellungen und Einblendungen.\n")
    print(f"{'Kap':>3}  {'Wörter':>6}  {'Text':>6}  {'Bild':>6}  {'Deckung':>8}  Titel")

    text_gesamt = bild_gesamt = 0
    for kapitel in daten["kapitel"]:
        text_s = sprechdauer(kapitel["sprechertext"])
        bild_s = sum(s["sekunden"] for s in kapitel["szenen"])
        text_gesamt += text_s
        bild_gesamt += bild_s

        kapitelziel = kapitel.get("bilddeckung", ziel)
        deckung = bild_s / text_s if text_s else 0
        marke = " " if abs(deckung - kapitelziel) <= TOLERANZ else "!"

        print(
            f"{kapitel['nr']:>3}  {woerter(kapitel['sprechertext']):>6}  "
            f"{text_s:>5.0f}s  {bild_s:>5.0f}s  {deckung:>7.0%}{marke} "
            f"{kapitel['titel']}"
        )

        if marke == "!":
            richtung = "über" if deckung > kapitelziel else "unter"
            warnungen.append(
                f"Kapitel {kapitel['nr']}: {deckung:.0%} Deckung liegt {richtung} dem Ziel "
                f"von {kapitelziel:.0%} — Szenen ergänzen oder streichen."
            )

        for szene in kapitel["szenen"]:
            if szene["id"] in gesehen:
                fehler.append(f"Szenen-ID doppelt: {szene['id']}")
            gesehen.add(szene["id"])

            prompt = szene["visual_prompt"]
            treffer = DEUTSCHE_WOERTER & set(prompt.lower().split())
            if treffer:
                fehler.append(
                    f"{szene['id']}: Prompt sieht deutsch aus ({', '.join(sorted(treffer))}) — "
                    "Videomodelle ignorieren deutsche Prompts und kosten trotzdem."
                )
            if not 4 <= szene["sekunden"] <= 10:
                warnungen.append(
                    f"{szene['id']}: {szene['sekunden']}s — die meisten Modelle liefern 4–10s."
                )

    print(
        f"\nGesamt: {len(daten['kapitel'])} Kapitel, {len(gesehen)} Szenen, "
        f"{text_gesamt / 60:.1f} min Sprechertext, {bild_gesamt / 60:.1f} min erzeugtes "
        f"Material, Deckung {bild_gesamt / text_gesamt:.0%}."
    )

    for w in warnungen:
        print(f"  Hinweis: {w}")
    if fehler:
        raise Abbruch("\n".join(f"  Fehler: {f}" for f in fehler))
    print("\nKeine Fehler.")


# --------------------------------------------------------------------------
# skript
# --------------------------------------------------------------------------


def befehl_skript(daten, args):
    zeilen = [
        f"# {daten['serie']} — Folge {daten['folge']}",
        "",
        f"## {daten['titel']}",
        "",
        "> **Erzeugte Datei.** Geändert wird `folgen/"
        f"{Path(args.datei).name}`, danach `python3 scripts/folge.py skript`.",
        "",
        f"> **Prüfstand:** {daten.get('pruefstand', 'unbekannt')}",
        "",
        "Dieses Skript erklärt die allgemeine Rechtslage. Es ist keine Rechtsberatung.",
        "",
        "---",
        "",
    ]

    laufzeit = 0.0
    inhalt = ["## Inhalt", ""]
    for kapitel in daten["kapitel"]:
        marke = f"{int(laufzeit // 60):02d}:{int(laufzeit % 60):02d}"
        inhalt.append(f"- `{marke}` **{kapitel['nr']}. {kapitel['titel']}**")
        laufzeit += sprechdauer(kapitel["sprechertext"])
    zeilen += inhalt + ["", "---", ""]

    laufzeit = 0.0
    for kapitel in daten["kapitel"]:
        dauer = sprechdauer(kapitel["sprechertext"])
        marke = f"{int(laufzeit // 60):02d}:{int(laufzeit % 60):02d}"
        laufzeit += dauer

        zeilen += [
            f"## {kapitel['nr']}. {kapitel['titel']}",
            "",
            f"`{marke}` · rund {dauer:.0f} Sekunden · "
            f"{woerter(kapitel['sprechertext'])} Wörter",
            "",
            "### Sprechertext",
            "",
        ]
        for absatz in kapitel["sprechertext"].split("\n"):
            zeilen += [absatz.strip(), ""]

        if kapitel.get("einblendungen"):
            zeilen += ["### Einblendungen", ""]
            zeilen += [f"- {e}" for e in kapitel["einblendungen"]] + [""]

        if kapitel.get("belege"):
            zeilen += [
                "### Belege",
                "",
                ", ".join(kapitel["belege"]),
                "",
            ]

        zeilen += ["### Bild", "", "| Szene | Sek. | Motiv |", "|---|---|---|"]
        for szene in kapitel["szenen"]:
            motiv = szene["visual_prompt"].replace("|", "/")
            zeilen.append(f"| `{szene['id']}` | {szene['sekunden']} | {motiv} |")
        zeilen += ["", "---", ""]

    if daten.get("reels"):
        zeilen += ["## Reels aus dieser Folge", ""]
        for reel in daten["reels"]:
            aus = ", ".join(str(k) for k in reel["aus_kapitel"])
            zeilen += [
                f"### Reel {reel['nr']} — {reel['titel']}",
                "",
                f"- **Hook:** {reel['hook']}",
                f"- **Kernsatz:** {reel['kernsatz']}",
                f"- **Quelle:** Kapitel {aus} · Format 9:16",
                "",
            ]

    ziel = PROJEKT / "skript" / (Path(args.datei).stem + ".md")
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text("\n".join(zeilen).rstrip() + "\n", encoding="utf-8")
    print(f"Geschrieben: {ziel.relative_to(PROJEKT)} ({len(zeilen)} Zeilen)")
    print(f"Geschätzte Laufzeit: {laufzeit / 60:.1f} Minuten.")


# --------------------------------------------------------------------------
# prompts
# --------------------------------------------------------------------------


def befehl_prompts(daten, args):
    for kapitel in daten["kapitel"]:
        if args.kapitel is not None and kapitel["nr"] != args.kapitel:
            continue
        for szene in kapitel["szenen"]:
            print(f"--- {szene['id']} ({szene['sekunden']}s) ---")
            print(voller_prompt(szene, kapitel))
            print()


# --------------------------------------------------------------------------
# kosten
# --------------------------------------------------------------------------


def befehl_kosten(daten, args):
    sekunden = sum(s["sekunden"] for k in daten["kapitel"] for s in k["szenen"])
    anzahl = sum(len(k["szenen"]) for k in daten["kapitel"])

    befehl = [
        sys.executable, str(kie_pfad()), "preis",
        "--modell", args.modell,
        "--sekunden", str(sekunden),
    ]
    if args.aufloesung:
        befehl += ["--aufloesung", args.aufloesung]
    if args.variante:
        befehl += ["--variante", args.variante]

    print(f"{anzahl} Szenen, {sekunden} Sekunden Bildmaterial insgesamt.")
    print(f"$ {' '.join(befehl[1:])}\n")
    ergebnis = subprocess.run(befehl, text=True)
    if ergebnis.returncode != 0:
        raise Abbruch("kie.py preis ist fehlgeschlagen — siehe Meldung oben.")
    print(
        "\nDazu kommt die Sprachaufnahme. Zeichenzahl des Sprechertexts: "
        f"{sum(len(k['sprechertext']) for k in daten['kapitel'])}."
    )


# --------------------------------------------------------------------------
# erzeugen
# --------------------------------------------------------------------------


def befehl_erzeugen(daten, args):
    if "image-to-video" in args.modell and not args.extra:
        raise Abbruch(
            f"{args.modell} braucht ein Startbild. Entweder ein Text-zu-Video-Modell "
            f"wählen (Standard: {STANDARD_MODELL}) oder je Szene ein Bild erzeugen und "
            "mit --extra '{\"image_url\": \"…\"}' übergeben."
        )

    projektname = args.projekt or f"recht-folge-{daten['folge']:02d}"
    auftraege = []

    for kapitel in daten["kapitel"]:
        if args.kapitel is not None and kapitel["nr"] != args.kapitel:
            continue
        for szene in kapitel["szenen"]:
            befehl = [
                sys.executable, str(kie_pfad()), "erzeugen",
                "--modell", args.modell,
                "--sekunden", str(szene["sekunden"]),
                "--projekt", projektname,
                "--prompt", voller_prompt(szene, kapitel),
            ]
            if args.aufloesung:
                befehl += ["--aufloesung", args.aufloesung]
            if args.variante:
                befehl += ["--variante", args.variante]
            if args.extra:
                befehl += ["--extra", args.extra]
            auftraege.append((szene["id"], befehl))

    if not auftraege:
        raise Abbruch("Keine Szenen ausgewählt.")

    if not args.echt:
        print(f"Trockenlauf — {len(auftraege)} Aufrufe, nichts wird erzeugt.\n")
        for szenen_id, befehl in auftraege:
            print(f"# {szenen_id}")
            print("$ " + " ".join(f"'{t}'" if " " in t or "\n" in t else t for t in befehl[1:]))
            print()
        print("Mit --echt tatsächlich erzeugen. Vorher: folge.py kosten.")
        return

    for nummer, (szenen_id, befehl) in enumerate(auftraege, 1):
        print(f"\n[{nummer}/{len(auftraege)}] {szenen_id}")
        ergebnis = subprocess.run(befehl, text=True)
        if ergebnis.returncode != 0:
            raise Abbruch(
                f"Abbruch bei {szenen_id}. Bereits erzeugte Szenen liegen unter "
                f"~/Medien/…-{projektname}/ und sind bezahlt."
            )
    print(f"\nFertig: {len(auftraege)} Szenen.")


# --------------------------------------------------------------------------


def main():
    zerleger = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    zerleger.add_argument(
        "--datei", default=str(STANDARD_FOLGE), help="Folgen-JSON (Standard: Folge 1)"
    )
    unter = zerleger.add_subparsers(dest="befehl", required=True)

    unter.add_parser("pruefen", help="Struktur, Zeiten und Prompts prüfen")
    unter.add_parser("skript", help="Sprecherskript als Markdown schreiben")

    pr = unter.add_parser("prompts", help="fertige Bildprompts ausgeben")
    pr.add_argument("--kapitel", type=int, help="nur dieses Kapitel")

    ko = unter.add_parser("kosten", help="Kosten des Bildmaterials ausrechnen")
    ko.add_argument("--modell", default=STANDARD_MODELL)
    ko.add_argument("--aufloesung", default="720p")
    ko.add_argument("--variante")

    er = unter.add_parser("erzeugen", help="kie.py-Aufrufe zeigen oder ausführen")
    er.add_argument("--modell", default=STANDARD_MODELL)
    er.add_argument("--aufloesung", default="720p")
    er.add_argument("--variante")
    er.add_argument("--kapitel", type=int, help="nur dieses Kapitel")
    er.add_argument("--projekt", help="Ordnername unter ~/Medien/")
    er.add_argument("--extra", help="weitere input-Felder als JSON, an kie.py durchgereicht")
    er.add_argument("--echt", action="store_true", help="wirklich erzeugen — kostet Geld")

    args = zerleger.parse_args()

    try:
        daten = laden(args.datei)
        {
            "pruefen": befehl_pruefen,
            "skript": befehl_skript,
            "prompts": befehl_prompts,
            "kosten": befehl_kosten,
            "erzeugen": befehl_erzeugen,
        }[args.befehl](daten, args)
    except Abbruch as fehler:
        print(f"\n{fehler}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
