#!/usr/bin/env python3
"""kie.py — Bilder, Videos und Sprache über die kie.ai-API erzeugen.

Nur Standardbibliothek, kein pip. Alle Ausgaben auf Deutsch, Geldbeträge mit Komma.

Unterbefehle:
    preis      rechnet die Kosten eines Auftrags aus — ohne jeden API-Aufruf
    modelle    druckt die Preistabelle
    guthaben   fragt das verbleibende Guthaben ab
    erzeugen   der komplette Dreisprung: Auftrag anlegen, warten, herunterladen

Der API-Schlüssel kommt IMMER aus der Umgebungsvariable KIE_API_KEY,
niemals aus einer Datei.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import deque
from datetime import date, datetime
from pathlib import Path

# --------------------------------------------------------------------------
# Grundwerte
# --------------------------------------------------------------------------

BASIS = "https://api.kie.ai/api/v1"

# 200 Credits = 1 US-Dollar. Ein Credit sind rund 0,0043 Euro.
EUR_JE_CREDIT = 0.0043

# Zwischen zwei Statusabfragen liegen acht Sekunden.
WARTEZEIT = 8

# Rate Limit: 20 Anfragen je 10 Sekunden.
LIMIT_ANFRAGEN = 20
LIMIT_FENSTER = 10.0

# Bei diesen HTTP-Codes wird bis zu fünfmal wiederholt, mit wachsender Pause.
WIEDERHOLBAR = {429, 500, 502, 503}
VERSUCHE = 5

# --------------------------------------------------------------------------
# Die Preistabelle — die eine Quelle der Wahrheit
#
# art: "bild"        Preis je Bild, nach Auflösung
#      "video_sek"   Preis je Sekunde, nach Auflösung
#      "video_clip"  Preis je Clip, nach Variante (feste Cliplängen)
#      "ton_sek"     Preis je Sekunde Sprache
#      "ton_zeichen" Preis je 1.000 Zeichen
# --------------------------------------------------------------------------

PREISE = {
    # ---- Bild, Preis je Bild -------------------------------------------------
    "gpt-image-2-text-to-image": {
        "art": "bild",
        "staffel": {"1k": 6, "2k": 10, "4k": 16},
        "notiz": "Text zu Bild, sehr solide Allzweckwahl",
    },
    "gpt-image-2-image-to-image": {
        "art": "bild",
        "staffel": {"1k": 6, "2k": 10, "4k": 16},
        "notiz": "Bild zu Bild, braucht ein Eingangsbild",
    },
    "nano-banana-2": {
        "art": "bild",
        "staffel": {"1k": 8, "2k": 12, "4k": 18},
        "notiz": "kräftigere Bildsprache, etwas teurer",
    },
    "google/nano-banana-pro": {
        "art": "bild",
        "staffel": {"1k": 18, "2k": 18, "4k": 24},
        "notiz": "die teure Spitze, für Titelbilder",
    },
    "nano-banana-2-lite": {
        "art": "bild",
        "staffel": {"1k": 4},
        "notiz": "die billigste Variante, nur 1K",
    },
    "google/nano-banana-edit": {
        "art": "bild",
        "staffel": {"standard": 4},
        "notiz": "gezieltes Nachbessern eines vorhandenen Bildes",
    },
    "seedream-5-pro": {
        "art": "bild",
        "staffel": {"1k": 7, "2k": 14},
        "notiz": "eigener Bildlook, kein 4K",
    },
    # ---- Video, Preis je Sekunde ---------------------------------------------
    "grok-imagine/image-to-video": {
        "art": "video_sek",
        "staffel": {"480p": 2.4, "720p": 4.5, "1080p": 8},
        "notiz": "mit Abstand das günstigste Video; duration ist hier ein TEXT",
    },
    "bytedance/seedance-1.5-pro": {
        "art": "video_sek",
        "staffel": {"720p": 3.5, "1080p": 7.5},
        "notiz": "günstig und ruhig, aber OHNE Ton",
    },
    "kling-3-0": {
        "art": "video_sek",
        "staffel": {"720p": 14, "1080p": 18},
        "notiz": "starke Bewegung, gehobene Klasse",
    },
    "bytedance/seedance-2": {
        "art": "video_sek",
        "staffel": {"720p": 41, "1080p": 102},
        "notiz": "cineastisch, aber sehr teuer — nur für Schlüsselszenen",
    },
    # ---- Video, Preis je Clip ------------------------------------------------
    "veo3.1": {
        "art": "video_clip",
        "staffel": {"lite": 35, "fast": 65, "quality": 255},
        "laengen": [4, 6, 8],
        "notiz": "1080p, nur 4, 6 oder 8 Sekunden; duration ist hier eine ZAHL",
    },
    # ---- Ton -----------------------------------------------------------------
    "google/gemini-2-5-pro-tts": {
        "art": "ton_sek",
        # rund 4 Credits für 40 Sekunden Sprache
        "je_sekunde": 0.1,
        "notiz": "sehr günstig; nur EIN Text übergeben, keine dialogue_turns",
    },
    "elevenlabs-multilingual-v2": {
        "art": "ton_zeichen",
        "je_1000_zeichen": 12,
        "notiz": "nach Zeichen abgerechnet; Model-Slug beim ersten Lauf bestätigen",
    },
}

# Welcher Dateityp gehört zu welcher Preisart — für meta.json.
TYP_JE_ART = {
    "bild": "bild",
    "video_sek": "video",
    "video_clip": "video",
    "ton_sek": "audio",
    "ton_zeichen": "audio",
}


# --------------------------------------------------------------------------
# Formatierung — deutsche Zahlen, Komma statt Punkt
# --------------------------------------------------------------------------


def euro(betrag, stellen=3):
    """0.1548 -> '0,155'"""
    return f"{betrag:.{stellen}f}".replace(".", ",")


def zahl(wert):
    """36.0 -> '36', 2.4 -> '2,4'"""
    if abs(wert - round(wert)) < 1e-9:
        return str(int(round(wert)))
    return f"{wert:g}".replace(".", ",")


class Abbruch(Exception):
    """Ein Fehler, der dem Nutzer als Satz gezeigt wird — nicht als Traceback."""


# --------------------------------------------------------------------------
# Preise ausrechnen — nie schätzen
# --------------------------------------------------------------------------


def kosten(modell, aufloesung=None, anzahl=1, sekunden=None, zeichen=None, variante=None):
    """Gibt (credits, erklaerung) für genau diesen Auftrag zurück."""
    if modell not in PREISE:
        nah = [m for m in PREISE if modell.lower() in m.lower()]
        hinweis = f" Meintest du {nah[0]}?" if nah else " Siehe: kie.py modelle"
        raise Abbruch(f"Unbekanntes Modell: {modell}.{hinweis}")

    eintrag = PREISE[modell]
    art = eintrag["art"]

    if art == "bild":
        stufe = _stufe_waehlen(modell, eintrag["staffel"], aufloesung, "Auflösung")
        je = eintrag["staffel"][stufe]
        credits = je * anzahl
        return credits, f"{anzahl} × {zahl(je)} Credits ({stufe})"

    if art == "video_sek":
        if sekunden is None:
            raise Abbruch(f"{modell} rechnet je Sekunde — bitte --sekunden angeben.")
        stufe = _stufe_waehlen(modell, eintrag["staffel"], aufloesung, "Auflösung")
        je = eintrag["staffel"][stufe]
        credits = je * sekunden * anzahl
        teil = f"{zahl(sekunden)} s × {zahl(je)} Credits/s ({stufe})"
        return credits, (f"{anzahl} × {teil}" if anzahl != 1 else teil)

    if art == "video_clip":
        if sekunden is None:
            raise Abbruch(f"{modell} rechnet je Clip — bitte --sekunden angeben.")
        erlaubt = eintrag["laengen"]
        if int(sekunden) not in erlaubt or sekunden != int(sekunden):
            moegliche = ", ".join(str(x) for x in erlaubt)
            raise Abbruch(
                f"{modell} kann nur {moegliche} Sekunden — {zahl(sekunden)} s geht nicht."
            )
        stufe = _stufe_waehlen(modell, eintrag["staffel"], variante, "Variante")
        je = eintrag["staffel"][stufe]
        credits = je * anzahl
        return credits, f"{anzahl} × {zahl(je)} Credits ({stufe}, {int(sekunden)} s je Clip)"

    if art == "ton_sek":
        if sekunden is None:
            raise Abbruch(f"{modell} rechnet je Sekunde — bitte --sekunden angeben.")
        credits = eintrag["je_sekunde"] * sekunden * anzahl
        teil = f"{zahl(sekunden)} s × {zahl(eintrag['je_sekunde'])} Credits/s"
        return credits, (f"{anzahl} × {teil}" if anzahl != 1 else teil)

    if art == "ton_zeichen":
        if zeichen is None:
            raise Abbruch(f"{modell} rechnet je 1.000 Zeichen — bitte --zeichen angeben.")
        credits = eintrag["je_1000_zeichen"] * zeichen / 1000 * anzahl
        teil = f"{zeichen} Zeichen × {zahl(eintrag['je_1000_zeichen'])} Credits/1.000"
        return credits, (f"{anzahl} × {teil}" if anzahl != 1 else teil)

    raise Abbruch(f"Unbekannte Preisart {art} bei {modell}.")


def _stufe_waehlen(modell, staffel, gewuenscht, wortfeld):
    """Prüft die gewünschte Stufe; ohne Angabe die günstigste."""
    if gewuenscht is None:
        return min(staffel, key=lambda s: staffel[s])
    stufe = gewuenscht.lower()
    if stufe not in staffel:
        moegliche = ", ".join(staffel)
        raise Abbruch(f"{modell} kennt die {wortfeld} '{gewuenscht}' nicht — möglich: {moegliche}.")
    return stufe


def befehl_preis(args):
    credits, erklaerung = kosten(
        args.modell,
        aufloesung=args.aufloesung,
        anzahl=args.anzahl,
        sekunden=args.sekunden,
        zeichen=args.zeichen,
        variante=args.variante,
    )
    print(f"{args.modell}: {erklaerung}")
    print(f"= {zahl(credits)} Credits · {euro(credits * EUR_JE_CREDIT)} €")
    return 0


def befehl_modelle(_args):
    ueberschriften = {
        "bild": "Bild — Preis je Bild",
        "video_sek": "Video — Preis je Sekunde",
        "video_clip": "Video — Preis je Clip",
        "ton_sek": "Ton — Preis je Sekunde",
        "ton_zeichen": "Ton — Preis je 1.000 Zeichen",
    }
    for art, titel in ueberschriften.items():
        passend = [(m, e) for m, e in PREISE.items() if e["art"] == art]
        if not passend:
            continue
        print(f"\n{titel}")
        for modell, eintrag in passend:
            if "staffel" in eintrag:
                stufen = " · ".join(f"{s} {zahl(p)}" for s, p in eintrag["staffel"].items())
            elif "je_sekunde" in eintrag:
                stufen = f"{zahl(eintrag['je_sekunde'])} je Sekunde"
            else:
                stufen = f"{zahl(eintrag['je_1000_zeichen'])} je 1.000 Zeichen"
            print(f"  {modell:<30} {stufen}")
            print(f"  {'':<30} {eintrag['notiz']}")
    print(f"\n200 Credits = 1 US-Dollar · 1 Credit = {euro(EUR_JE_CREDIT, 4)} €")
    print("Preise ändern sich häufig — vor größeren Läufen auf kie.ai/pricing schauen.")
    return 0


# --------------------------------------------------------------------------
# Die API-Schicht
# --------------------------------------------------------------------------

_anfragezeiten = deque()


def _rate_limit_einhalten():
    """Höchstens 20 Anfragen je 10 Sekunden — clientseitig gebremst."""
    jetzt = time.monotonic()
    while _anfragezeiten and jetzt - _anfragezeiten[0] > LIMIT_FENSTER:
        _anfragezeiten.popleft()
    if len(_anfragezeiten) >= LIMIT_ANFRAGEN:
        pause = LIMIT_FENSTER - (jetzt - _anfragezeiten[0]) + 0.1
        if pause > 0:
            time.sleep(pause)
    _anfragezeiten.append(time.monotonic())


def schluessel():
    wert = os.environ.get("KIE_API_KEY", "").strip()
    if not wert:
        raise Abbruch(
            "KIE_API_KEY ist nicht gesetzt.\n"
            "  export KIE_API_KEY='dein-schluessel'   (und dauerhaft in ~/.zshrc bzw. ~/.bashrc)"
        )
    return wert


def anfrage(pfad, daten=None, params=None):
    """Ein Aufruf gegen die kie.ai-API, mit Wiederholungen und klaren Fehlern."""
    url = BASIS + pfad
    if params:
        url += "?" + urllib.parse.urlencode(params)

    rumpf = json.dumps(daten).encode("utf-8") if daten is not None else None
    kopf = {
        "Authorization": f"Bearer {schluessel()}",
        "Accept": "application/json",
    }
    if rumpf is not None:
        kopf["Content-Type"] = "application/json"

    letzter = ""
    for versuch in range(1, VERSUCHE + 1):
        _rate_limit_einhalten()
        bitte = urllib.request.Request(url, data=rumpf, headers=kopf,
                                       method="POST" if rumpf is not None else "GET")
        try:
            with urllib.request.urlopen(bitte, timeout=120) as antwort:
                inhalt = json.loads(antwort.read().decode("utf-8"))
                break
        except urllib.error.HTTPError as fehler:
            if fehler.code == 402:
                raise Abbruch("HTTP 402 — das Guthaben ist leer. Auf kie.ai aufladen.")
            if fehler.code == 401:
                raise Abbruch("HTTP 401 — der KIE_API_KEY wurde abgelehnt.")
            if fehler.code in WIEDERHOLBAR and versuch < VERSUCHE:
                pause = 2 ** versuch
                print(f"  HTTP {fehler.code} — neuer Versuch in {pause} s "
                      f"({versuch}/{VERSUCHE - 1})", file=sys.stderr)
                time.sleep(pause)
                letzter = f"HTTP {fehler.code}"
                continue
            raise Abbruch(f"HTTP {fehler.code} von {pfad}: {fehler.reason}")
        except urllib.error.URLError as fehler:
            if versuch < VERSUCHE:
                pause = 2 ** versuch
                print(f"  Netzwerkfehler — neuer Versuch in {pause} s", file=sys.stderr)
                time.sleep(pause)
                letzter = str(fehler.reason)
                continue
            raise Abbruch(f"Keine Verbindung zu kie.ai: {fehler.reason}")
    else:
        raise Abbruch(f"{VERSUCHE} Versuche gescheitert ({letzter}).")

    if inhalt.get("code") != 200:
        raise Abbruch(f"kie.ai meldet Fehler {inhalt.get('code')}: "
                      f"{inhalt.get('msg') or inhalt.get('message') or 'ohne Angabe'}")
    return inhalt.get("data") or {}


def befehl_guthaben(_args):
    daten = anfrage("/chat/credit")
    # Die Antwort ist je nach Konto mal eine blanke Zahl, mal ein Objekt.
    credits = daten if isinstance(daten, (int, float)) else daten.get("credits", daten)
    try:
        credits = float(credits)
    except (TypeError, ValueError):
        print(f"Guthaben: {credits}")
        return 0
    print(f"Guthaben: {zahl(credits)} Credits · {euro(credits * EUR_JE_CREDIT, 2)} €")
    return 0


# --------------------------------------------------------------------------
# Erzeugen: Auftrag anlegen, warten, herunterladen, protokollieren
# --------------------------------------------------------------------------


def auftrag_anlegen(modell, eingabe):
    daten = anfrage("/jobs/createTask", daten={"model": modell, "input": eingabe})
    task_id = daten.get("taskId")
    if not task_id:
        raise Abbruch("Antwort ohne taskId — der Auftrag wurde nicht angelegt.")
    return task_id


def auf_ergebnis_warten(task_id, still=False):
    """Fragt alle acht Sekunden nach, bis success oder fail."""
    gesehen = None
    while True:
        daten = anfrage("/jobs/recordInfo", params={"taskId": task_id})
        zustand = daten.get("state")
        if zustand != gesehen and not still:
            print(f"  Status: {zustand}")
            gesehen = zustand

        if zustand == "success":
            # resultJson ist ein JSON-STRING, der erst geparst werden muss.
            roh = daten.get("resultJson") or "{}"
            ergebnis = json.loads(roh) if isinstance(roh, str) else roh
            urls = ergebnis.get("resultUrls") or []
            if not urls:
                raise Abbruch("Auftrag fertig, aber ohne resultUrls.")
            # Die tatsächlich abgerechneten Credits, nicht der geschätzte Preis.
            verbraucht = daten.get("creditsConsumed")
            return urls, verbraucht

        if zustand == "fail":
            grund = daten.get("failMsg") or daten.get("failCode") or "ohne Angabe"
            raise Abbruch(f"Auftrag fehlgeschlagen: {grund}")

        if zustand not in ("waiting", "queuing", "generating"):
            raise Abbruch(f"Unerwarteter Zustand: {zustand}")

        time.sleep(WARTEZEIT)


def zielordner(projekt, wurzel=None):
    """~/Medien/JJJJ-MM-TT-projektname/"""
    sauber = re.sub(r"[^a-z0-9]+", "-", projekt.lower()).strip("-") or "projekt"
    basis = Path(wurzel).expanduser() if wurzel else Path.home() / "Medien"
    ordner = basis / f"{date.today().isoformat()}-{sauber}"
    ordner.mkdir(parents=True, exist_ok=True)
    return ordner


def herunterladen_und_protokollieren(urls, ordner, modell, prompt, typ, credits):
    """Lädt die Ergebnisse herunter UND schreibt meta.json im selben Schritt fort.

    Die Ergebnis-URLs von kie.ai verfallen nach 24 Stunden — deshalb sofort.
    Beides gehört zusammen, damit das Protokoll nicht vergessen werden kann.
    """
    meta_pfad = ordner / "meta.json"
    bestehend = []
    if meta_pfad.exists():
        try:
            bestehend = json.loads(meta_pfad.read_text(encoding="utf-8")) or []
        except json.JSONDecodeError:
            # Lieber umbenennen als überschreiben — nichts geht verloren.
            meta_pfad.rename(meta_pfad.with_suffix(".json.kaputt"))
            print("  meta.json war unlesbar und wurde als meta.json.kaputt beiseitegelegt.",
                  file=sys.stderr)
            bestehend = []

    # Credits gleichmäßig auf die einzelnen Dateien verteilen.
    je_datei = (credits / len(urls)) if credits else 0
    nummer = _naechste_nummer(ordner)
    neue = []

    for url in urls:
        endung = Path(urllib.parse.urlparse(url).path).suffix or _endung_je_typ(typ)
        name = f"{nummer:02d}{endung}"
        ziel = ordner / name
        # Nie eine vorhandene Datei überschreiben — lieber weiterzählen.
        while ziel.exists():
            nummer += 1
            name = f"{nummer:02d}{endung}"
            ziel = ordner / name
        _datei_holen(url, ziel)
        eintrag = {
            "zeit": datetime.now().replace(microsecond=0).isoformat(),
            "datei": name,
            "typ": typ,
            "modell": modell,
            "prompt": prompt,
            "credits": round(je_datei, 2),
            "eur": round(je_datei * EUR_JE_CREDIT, 4),
        }
        neue.append(eintrag)
        print(f"  {ziel}")
        nummer += 1

    # Anhängen, nicht überschreiben.
    meta_pfad.write_text(
        json.dumps(bestehend + neue, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return neue


def _naechste_nummer(ordner):
    """Zählt an den bereits vorhandenen Dateien weiter, nicht an den meta-Einträgen."""
    hoechste = 0
    for datei in ordner.iterdir():
        if datei.name == "meta.json" or not datei.is_file():
            continue
        ziffern = re.match(r"(\d+)", datei.stem)
        if ziffern:
            hoechste = max(hoechste, int(ziffern.group(1)))
    return hoechste + 1


def _endung_je_typ(typ):
    return {"bild": ".png", "video": ".mp4", "audio": ".wav"}.get(typ, ".bin")


def _datei_holen(url, ziel):
    for versuch in range(1, VERSUCHE + 1):
        try:
            with urllib.request.urlopen(url, timeout=300) as antwort, \
                    open(ziel, "wb") as datei:
                while True:
                    brocken = antwort.read(65536)
                    if not brocken:
                        break
                    datei.write(brocken)
            return
        except (urllib.error.HTTPError, urllib.error.URLError) as fehler:
            if versuch < VERSUCHE:
                time.sleep(2 ** versuch)
                continue
            raise Abbruch(
                f"Download gescheitert: {fehler}\n"
                "  Achtung: die Ergebnis-URLs verfallen nach 24 Stunden."
            )


def befehl_erzeugen(args):
    if args.modell not in PREISE:
        raise Abbruch(f"Unbekanntes Modell: {args.modell}. Siehe: kie.py modelle")
    art = PREISE[args.modell]["art"]
    typ = TYP_JE_ART[art]

    # Vorher rechnen, damit die Schätzung im Protokoll steht, falls die API
    # ausnahmsweise keine creditsConsumed liefert.
    geschaetzt, erklaerung = kosten(
        args.modell,
        aufloesung=args.aufloesung,
        anzahl=args.anzahl,
        sekunden=args.sekunden,
        zeichen=args.zeichen if args.zeichen else (len(args.prompt) if art == "ton_zeichen" else None),
        variante=args.variante,
    )

    eingabe = {"prompt": args.prompt}
    if args.aufloesung:
        eingabe["image_size" if art == "bild" else "resolution"] = args.aufloesung
    if args.sekunden is not None and art in ("video_sek", "video_clip"):
        # Bei veo3.1 eine ZAHL, bei grok-imagine ein TEXT — siehe references/modelle.md.
        eingabe["duration"] = int(args.sekunden) if args.modell == "veo3.1" else str(int(args.sekunden))
    if args.anzahl > 1 and art == "bild":
        eingabe["num_images"] = args.anzahl
    if args.extra:
        try:
            eingabe.update(json.loads(args.extra))
        except json.JSONDecodeError as fehler:
            raise Abbruch(f"--extra ist kein gültiges JSON: {fehler}")

    print(f"{args.modell}: {erklaerung} = {zahl(geschaetzt)} Credits · "
          f"{euro(geschaetzt * EUR_JE_CREDIT)} € (geschätzt)")

    task_id = auftrag_anlegen(args.modell, eingabe)
    print(f"  Auftrag {task_id} angelegt.")
    urls, verbraucht = auf_ergebnis_warten(task_id)

    credits = verbraucht if verbraucht is not None else geschaetzt
    ordner = zielordner(args.projekt, args.wurzel)
    herunterladen_und_protokollieren(urls, ordner, args.modell, args.prompt, typ, credits)

    print(f"Abgerechnet: {zahl(float(credits))} Credits · "
          f"{euro(float(credits) * EUR_JE_CREDIT)} €")
    return 0


# --------------------------------------------------------------------------
# Kommandozeile
# --------------------------------------------------------------------------


def parser_bauen():
    p = argparse.ArgumentParser(
        prog="kie.py",
        description="Bilder, Videos und Sprache über die kie.ai-API erzeugen.",
    )
    unter = p.add_subparsers(dest="befehl", required=True)

    pr = unter.add_parser("preis", help="Kosten ausrechnen, ohne API-Aufruf")
    pr.add_argument("--modell", required=True)
    pr.add_argument("--aufloesung", help="1k, 2k, 4k bzw. 480p, 720p, 1080p")
    pr.add_argument("--anzahl", type=int, default=1, help="Wie viele Ergebnisse (Standard 1)")
    pr.add_argument("--sekunden", type=float, help="Länge bei Video und Ton")
    pr.add_argument("--zeichen", type=int, help="Zeichenzahl bei zeichenbasiertem Ton")
    pr.add_argument("--variante", help="bei veo3.1: lite, fast oder quality")
    pr.set_defaults(funktion=befehl_preis)

    mo = unter.add_parser("modelle", help="Preistabelle drucken")
    mo.set_defaults(funktion=befehl_modelle)

    gu = unter.add_parser("guthaben", help="verbleibendes Guthaben abfragen")
    gu.set_defaults(funktion=befehl_guthaben)

    er = unter.add_parser("erzeugen", help="anlegen, warten, herunterladen, protokollieren")
    er.add_argument("--modell", required=True)
    er.add_argument("--prompt", required=True, help="Videomodelle verstehen NUR Englisch")
    er.add_argument("--projekt", required=True, help="Name des Zielordners unter ~/Medien/")
    er.add_argument("--aufloesung")
    er.add_argument("--anzahl", type=int, default=1)
    er.add_argument("--sekunden", type=float)
    er.add_argument("--zeichen", type=int)
    er.add_argument("--variante")
    er.add_argument("--extra", help="weitere input-Felder als JSON, z. B. '{\"image_url\": \"...\"}'")
    er.add_argument("--wurzel", help="abweichende Ablage statt ~/Medien")
    er.set_defaults(funktion=befehl_erzeugen)

    return p


def main():
    args = parser_bauen().parse_args()
    try:
        return args.funktion(args)
    except Abbruch as fehler:
        print(f"Fehler: {fehler}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nAbgebrochen.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
