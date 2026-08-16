#!/usr/bin/env python3
"""veo.py — Veo-3.1-Clips über den eigenen kie.ai-Endpunkt erzeugen.

Warum es diese Datei gibt: `media-skill/scripts/kie.py` schickt alles an
`/jobs/createTask`. Veo 3.1 hängt dort aber nicht dran — kie.ai gibt ihm einen
eigenen Endpunkt, genau wie Suno. Ein Auftrag mit `--modell veo3.1` scheitert
deshalb mit „422: The model name you specified is not supported".

    POST /api/v1/veo/generate      {"prompt": ..., "model": "veo3_lite", ...}
    GET  /api/v1/veo/record-info?taskId=...   → successFlag 0=läuft 1=fertig

Download, Dateibenennung und meta.json kommen unverändert aus `kie.py` — hier
steht nur, was am Veo-Endpunkt anders ist.

Der API-Schlüssel kommt IMMER aus der Umgebungsvariable KIE_API_KEY.

    python3 veo.py --prompt "…" --projekt 244-tage
    python3 veo.py --prompt "…" --variante fast --sekunden 6
"""

import argparse
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# Die bewährten Bausteine aus dem media-skill weiterverwenden statt nachbauen.
SKILL = Path(__file__).resolve().parents[2] / "skills" / "media-skill" / "scripts"
sys.path.insert(0, str(SKILL))
import kie  # noqa: E402

ENDPUNKT = "https://api.kie.ai/api/v1/veo"


def _mit_curl_holen(url, ziel):
    """Die Ergebnisdateien liegen auf tempfile.aiquickdraw.com, nicht unter kie.ai.

    Hinter dem Agenten-Proxy scheitert Pythons urllib dort mit HTTP 403, curl kommt
    durch. Deshalb hängen wir uns hier in kie._datei_holen ein, statt es nachzubauen.
    """
    subprocess.run(["curl", "-sS", "--fail", "-o", str(ziel), url], check=True)


kie._datei_holen = _mit_curl_holen

# Variante → Modell-Slug am Veo-Endpunkt und Preis je Clip (längenunabhängig).
VARIANTEN = {
    "lite": ("veo3_lite", 35),
    "fast": ("veo3_fast", 65),
    "quality": ("veo3", 255),
}


def _anfrage(pfad, daten=None):
    """Ein Aufruf gegen den Veo-Endpunkt, mit denselben Wiederholungen wie kie.py."""
    schluessel = kie.schluessel()
    rumpf = json.dumps(daten).encode("utf-8") if daten is not None else None
    anfrage = urllib.request.Request(
        ENDPUNKT + pfad,
        data=rumpf,
        headers={
            "Authorization": f"Bearer {schluessel}",
            "Content-Type": "application/json",
        },
        method="POST" if daten is not None else "GET",
    )

    pause = 2
    for versuch in range(kie.VERSUCHE):
        try:
            with urllib.request.urlopen(anfrage, timeout=120) as antwort:
                return json.loads(antwort.read().decode("utf-8"))
        except urllib.error.HTTPError as fehler:
            text = fehler.read().decode("utf-8", "replace")[:400]
            if fehler.code == 402:
                raise kie.Abbruch("Guthaben leer (HTTP 402). Auf kie.ai aufladen.")
            if fehler.code in kie.WIEDERHOLBAR and versuch < kie.VERSUCHE - 1:
                time.sleep(pause)
                pause *= 2
                continue
            raise kie.Abbruch(f"kie.ai meldet Fehler {fehler.code}: {text}")
        except urllib.error.URLError as fehler:
            if versuch < kie.VERSUCHE - 1:
                time.sleep(pause)
                pause *= 2
                continue
            raise kie.Abbruch(f"Netzwerkfehler: {fehler.reason}")
    raise kie.Abbruch("Aufruf nach mehreren Versuchen aufgegeben.")


def erzeugen(prompt, variante, sekunden, aufloesung, seitenverhaeltnis, projekt):
    modell, credits = VARIANTEN[variante]
    print(f"veo3.1 ({variante}): 1 × {credits} Credits · "
          f"{kie.euro(credits * kie.EUR_JE_CREDIT)} €")

    antwort = _anfrage("/generate", {
        "prompt": prompt,
        "model": modell,
        "aspect_ratio": seitenverhaeltnis,
        "duration": int(sekunden),
        "resolution": aufloesung,
        "generationType": "TEXT_2_VIDEO",
    })
    if antwort.get("code") != 200:
        raise kie.Abbruch(f"Auftrag abgelehnt: {antwort.get('msg')}")
    auftrag = antwort["data"]["taskId"]
    print(f"  Auftrag {auftrag} läuft …")

    # successFlag: 0 = läuft, 1 = fertig, alles andere ist ein Fehlschlag.
    while True:
        time.sleep(kie.WARTEZEIT)
        stand = _anfrage(f"/record-info?taskId={auftrag}")
        daten = stand.get("data") or {}
        flagge = daten.get("successFlag")
        if flagge == 1:
            break
        if flagge not in (0, None):
            grund = daten.get("errorMessage") or stand.get("msg") or "unbekannt"
            raise kie.Abbruch(f"Erzeugung fehlgeschlagen: {grund}")

    ergebnis = daten.get("response") or {}
    urls = ergebnis.get("resultUrls") or []
    if isinstance(urls, str):
        # resultUrls kommt als JSON-Text zurück, nicht als Liste.
        urls = json.loads(urls)
    if not urls:
        raise kie.Abbruch("Auftrag fertig, aber ohne resultUrls.")

    ordner = kie.zielordner(projekt)
    kie.herunterladen_und_protokollieren(
        urls, ordner, f"veo3.1-{variante}", prompt, "video", credits
    )


def main():
    zerleger = argparse.ArgumentParser(description=__doc__)
    zerleger.add_argument("--prompt", required=True)
    zerleger.add_argument("--projekt", default="244-tage")
    zerleger.add_argument("--variante", default="lite", choices=sorted(VARIANTEN))
    zerleger.add_argument("--sekunden", type=int, default=8, choices=(4, 6, 8))
    zerleger.add_argument("--aufloesung", default="1080p")
    zerleger.add_argument("--seitenverhaeltnis", default="9:16")
    args = zerleger.parse_args()

    try:
        erzeugen(args.prompt, args.variante, args.sekunden,
                 args.aufloesung, args.seitenverhaeltnis, args.projekt)
    except kie.Abbruch as fehler:
        print(f"Fehler: {fehler}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
