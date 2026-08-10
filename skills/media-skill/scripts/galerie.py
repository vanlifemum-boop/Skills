#!/usr/bin/env python3
"""galerie.py — baut aus allen meta.json unter ~/Medien eine einzelne HTML-Seite.

Nur Standardbibliothek, kein pip. Die fertige Seite braucht keinen Server:
Dateien werden über relative Pfade eingebunden, ausdrücklich NICHT als Base64
— sonst wird die Seite bei ein paar hundert Einträgen unbenutzbar.

    python3 galerie.py                 baut ~/Medien/galerie.html und öffnet sie
    python3 galerie.py --nooeffnen     baut nur
    python3 galerie.py --wurzel PFAD   andere Ablage statt ~/Medien
"""

import argparse
import html
import json
import shutil
import subprocess
import sys
from pathlib import Path

EUR_JE_CREDIT = 0.0043

TYP_LABEL = {"bild": "Bild", "video": "Video", "audio": "Ton"}


# --------------------------------------------------------------------------
# Einlesen
# --------------------------------------------------------------------------


def eintraege_sammeln(wurzel):
    """Liest alle Projektordner ein. Einträge ohne Datei werden übersprungen."""
    eintraege = []
    uebersprungen = 0

    for meta_pfad in sorted(wurzel.glob("*/meta.json")):
        projekt = meta_pfad.parent.name
        try:
            roh = json.loads(meta_pfad.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as fehler:
            print(f"  {meta_pfad} unlesbar, übersprungen ({fehler})", file=sys.stderr)
            continue
        if not isinstance(roh, list):
            print(f"  {meta_pfad} ist keine Liste, übersprungen", file=sys.stderr)
            continue

        for eintrag in roh:
            datei = meta_pfad.parent / str(eintrag.get("datei", ""))
            if not datei.is_file():
                uebersprungen += 1
                continue
            eintrag = dict(eintrag)
            eintrag["_projekt"] = projekt
            eintrag["_pfad"] = datei
            # Relativ zur Wurzel — die galerie.html liegt genau dort.
            eintrag["_relativ"] = f"{projekt}/{datei.name}"
            eintraege.append(eintrag)

    if uebersprungen:
        print(f"  {uebersprungen} Einträge ohne Datei übersprungen.")

    # Neueste zuerst.
    eintraege.sort(key=lambda e: str(e.get("zeit", "")), reverse=True)
    return eintraege


# --------------------------------------------------------------------------
# Video-Vorschaubilder — einmalig ziehen, dann zwischengespeichert
# --------------------------------------------------------------------------


def vorschaubild(datei):
    """Zieht per ffmpeg ein Vorschaubild und legt es als <datei>.thumb.jpg ab.

    Beim zweiten Aufbau ist es schon da und wird nicht neu erzeugt.
    Fehlt ffmpeg, läuft die Galerie ohne Vorschaubild weiter.
    """
    ziel = datei.with_name(datei.name + ".thumb.jpg")
    if ziel.exists():
        return ziel
    if not shutil.which("ffmpeg"):
        return None
    try:
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", str(datei),
             "-frames:v", "1", "-vf", "scale=480:-1", str(ziel)],
            check=True, capture_output=True, timeout=60,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return ziel if ziel.exists() else None
    return ziel if ziel.exists() else None


# --------------------------------------------------------------------------
# Deutsche Zahlen
# --------------------------------------------------------------------------


def de(wert, stellen=2):
    """1234.5 -> '1.234,50' — Punkt als Tausender, Komma als Dezimalzeichen."""
    return f"{wert:,.{stellen}f}".translate(str.maketrans(",.", ".,"))


def datum_kurz(zeit):
    """'2026-08-08T11:20:03' -> '08.08.2026, 11:20'"""
    text = str(zeit)
    if len(text) >= 16 and text[4] == "-":
        return f"{text[8:10]}.{text[5:7]}.{text[0:4]}, {text[11:16]}"
    return text


# --------------------------------------------------------------------------
# HTML bauen
# --------------------------------------------------------------------------

STIL = """
:root {
  --grund: #fbfbfa; --karte: #fff; --rand: #e3e2df;
  --schrift: #1c1b19; --leise: #6b6863; --akzent: #3b6ea5;
}
@media (prefers-color-scheme: dark) {
  :root {
    --grund: #17181a; --karte: #1f2124; --rand: #32353a;
    --schrift: #e8e7e4; --leise: #9b9892; --akzent: #7aa6d6;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0; padding: 2rem 1.5rem 4rem;
  background: var(--grund); color: var(--schrift);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
               "Helvetica Neue", Arial, sans-serif;
  font-size: 15px; line-height: 1.5;
}
.huelle { max-width: 1400px; margin: 0 auto; }
h1 { font-size: 1.3rem; font-weight: 600; margin: 0 0 1.25rem; }
.summe {
  display: flex; flex-wrap: wrap; gap: 2.5rem;
  background: var(--karte); border: 1px solid var(--rand); border-radius: 10px;
  padding: 1.25rem 1.5rem; margin-bottom: 1.5rem;
}
.summe div { min-width: 8rem; }
.summe .wert { font-size: 1.9rem; font-weight: 600; letter-spacing: -0.02em; }
.summe .name { color: var(--leise); font-size: 0.8rem; text-transform: uppercase;
               letter-spacing: 0.06em; }
.werkzeuge { display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center;
             margin-bottom: 1.5rem; }
button, select, input {
  font: inherit; color: inherit; background: var(--karte);
  border: 1px solid var(--rand); border-radius: 7px; padding: 0.4rem 0.8rem;
}
button { cursor: pointer; }
button.aktiv { background: var(--akzent); border-color: var(--akzent); color: #fff; }
input[type=search] { flex: 1; min-width: 12rem; }
.raster {
  display: grid; gap: 1.25rem;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
}
.kachel {
  background: var(--karte); border: 1px solid var(--rand); border-radius: 10px;
  overflow: hidden; display: flex; flex-direction: column;
}
.kachel .medium {
  width: 100%; aspect-ratio: 4/3; object-fit: cover; display: block;
  background: var(--grund);
}
.kachel audio { width: 100%; margin: 1.5rem 0.75rem 0.5rem; }
.kachel .text { padding: 0.75rem 0.9rem 0.9rem; }
.prompt {
  margin: 0 0 0.5rem; display: -webkit-box; -webkit-line-clamp: 3;
  -webkit-box-orient: vertical; overflow: hidden;
}
.zeile { color: var(--leise); font-size: 0.82rem; }
.modell { font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
          font-size: 0.78rem; word-break: break-all; }
.leer { color: var(--leise); padding: 3rem 0; text-align: center; }
"""

SKRIPT = """
const kacheln = [...document.querySelectorAll('.kachel')];
const suche = document.getElementById('suche');
const modellwahl = document.getElementById('modellwahl');
const knoepfe = [...document.querySelectorAll('[data-typ]')];
const leer = document.getElementById('leer');
let typ = 'alle';

function filtern() {
  const text = suche.value.trim().toLowerCase();
  const modell = modellwahl.value;
  let sichtbar = 0;
  for (const kachel of kacheln) {
    const passtTyp = typ === 'alle' || kachel.dataset.typ === typ;
    const passtModell = modell === 'alle' || kachel.dataset.modell === modell;
    const passtText = !text || kachel.dataset.suche.includes(text);
    const zeigen = passtTyp && passtModell && passtText;
    kachel.hidden = !zeigen;
    if (zeigen) sichtbar++;
  }
  leer.hidden = sichtbar > 0;
}

for (const knopf of knoepfe) {
  knopf.addEventListener('click', () => {
    knoepfe.forEach(k => k.classList.toggle('aktiv', k === knopf));
    typ = knopf.dataset.typ;
    filtern();
  });
}
suche.addEventListener('input', filtern);
modellwahl.addEventListener('change', filtern);
"""


def kachel_bauen(eintrag, wurzel):
    typ = str(eintrag.get("typ", "")).lower()
    quelle = html.escape(eintrag["_relativ"])
    prompt = str(eintrag.get("prompt", ""))
    modell = str(eintrag.get("modell", "unbekannt"))
    credits = float(eintrag.get("credits") or 0)
    eur = float(eintrag.get("eur") or credits * EUR_JE_CREDIT)

    if typ == "bild":
        medium = f'<img class="medium" src="{quelle}" loading="lazy" alt="">'
    elif typ == "video":
        thumb = vorschaubild(eintrag["_pfad"])
        poster = ""
        if thumb:
            poster = f' poster="{html.escape(str(thumb.relative_to(wurzel)))}"'
        medium = (f'<video class="medium" src="{quelle}"{poster} '
                  f'controls preload="none"></video>')
    else:
        medium = f'<audio src="{quelle}" controls preload="none"></audio>'

    suchtext = html.escape(f"{prompt} {modell} {eintrag['_projekt']}".lower(), quote=True)

    return f"""      <article class="kachel" data-typ="{html.escape(typ)}"
        data-modell="{html.escape(modell)}" data-suche="{suchtext}">
        {medium}
        <div class="text">
          <p class="prompt">{html.escape(prompt)}</p>
          <div class="zeile modell">{html.escape(modell)}</div>
          <div class="zeile">{de(credits)} Credits · {de(eur, 3)} €</div>
          <div class="zeile">{html.escape(eintrag['_projekt'])} · {datum_kurz(eintrag.get('zeit', ''))}</div>
        </div>
      </article>"""


def seite_bauen(eintraege, wurzel):
    anzahl = len(eintraege)
    credits_gesamt = sum(float(e.get("credits") or 0) for e in eintraege)
    eur_gesamt = sum(
        float(e.get("eur") if e.get("eur") is not None else float(e.get("credits") or 0) * EUR_JE_CREDIT)
        for e in eintraege
    )

    modelle = sorted({str(e.get("modell", "unbekannt")) for e in eintraege})
    optionen = "\n".join(
        f'          <option value="{html.escape(m)}">{html.escape(m)}</option>'
        for m in modelle
    )

    typen = {str(e.get("typ", "")).lower() for e in eintraege}
    knoepfe = ['<button data-typ="alle" class="aktiv">Alle</button>']
    for schluessel, beschriftung in TYP_LABEL.items():
        if schluessel in typen:
            knoepfe.append(f'<button data-typ="{schluessel}">{beschriftung}</button>')

    kacheln = "\n".join(kachel_bauen(e, wurzel) for e in eintraege)

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mediengalerie</title>
<style>{STIL}</style>
</head>
<body>
  <div class="huelle">
    <h1>Mediengalerie</h1>

    <section class="summe">
      <div><div class="wert">{de(anzahl, 0)}</div><div class="name">Generierungen</div></div>
      <div><div class="wert">{de(credits_gesamt, 0)}</div><div class="name">Credits gesamt</div></div>
      <div><div class="wert">{de(eur_gesamt)} €</div><div class="name">Euro gesamt</div></div>
    </section>

    <div class="werkzeuge">
      {" ".join(knoepfe)}
      <select id="modellwahl">
          <option value="alle">Alle Modelle</option>
{optionen}
      </select>
      <input type="search" id="suche" placeholder="Suche in Prompt, Modell, Projekt …">
    </div>

    <div class="raster">
{kacheln}
    </div>
    <p class="leer" id="leer" hidden>Nichts gefunden.</p>
  </div>
<script>{SKRIPT}</script>
</body>
</html>
"""


# --------------------------------------------------------------------------
# Hauptlauf
# --------------------------------------------------------------------------


def oeffnen(pfad):
    befehl = "open" if sys.platform == "darwin" else "xdg-open"
    if not shutil.which(befehl):
        print(f"  ({befehl} nicht gefunden — Seite bitte selbst öffnen)")
        return
    subprocess.run([befehl, str(pfad)], check=False)


def main():
    p = argparse.ArgumentParser(
        prog="galerie.py",
        description="Baut aus allen meta.json unter ~/Medien eine einzelne HTML-Seite.",
    )
    p.add_argument("--wurzel", default="~/Medien", help="Ablage (Standard ~/Medien)")
    p.add_argument("--nooeffnen", action="store_true", help="Seite nur bauen, nicht öffnen")
    args = p.parse_args()

    wurzel = Path(args.wurzel).expanduser()
    if not wurzel.is_dir():
        print(f"Fehler: {wurzel} gibt es nicht.", file=sys.stderr)
        return 1

    eintraege = eintraege_sammeln(wurzel)
    if not eintraege:
        print(f"Keine Einträge unter {wurzel} gefunden.", file=sys.stderr)

    ziel = wurzel / "galerie.html"
    ziel.write_text(seite_bauen(eintraege, wurzel), encoding="utf-8")

    gesamt = sum(float(e.get("credits") or 0) for e in eintraege)
    print(f"{ziel} — {len(eintraege)} Einträge, {de(gesamt, 0)} Credits gesamt.")

    if not args.nooeffnen:
        oeffnen(ziel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
