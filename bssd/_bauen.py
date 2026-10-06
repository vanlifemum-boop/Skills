#!/usr/bin/env python3
"""Baut die statischen BSSD-Seiten aus den Inhalten in _inhalt/.

Jede Datei in _inhalt/ beginnt mit einem Kopfblock (Schlüssel: Wert), getrennt
durch eine Zeile '---' vom HTML-Inhalt. Kopf, Säulen-Umschalter und Fuß werden
hier einheitlich ergänzt. Aufruf:  python3 bssd/_bauen.py
"""
import pathlib

WURZEL = pathlib.Path(__file__).resolve().parent
QUELLE = WURZEL / "_inhalt"

# ---- Stammdaten: vor dem Livegang ausfüllen --------------------------------
STAMM = {
    "email": "",      # z. B. kontakt@ihre-domain.de
    "telefon": "",    # z. B. +49 151 …
    "ort": "",        # z. B. Einsatzgebiet / Stadt
}

def wert(schluessel, text):
    v = STAMM[schluessel]
    return v if v else f'<span class="platzhalter">[{text}]</span>'

NAV = [
    ("beratung/", "Beratung", "beratung"),
    ("sport/", "Sport", "sport"),
    ("schulungen/", "Schulungen", "schulungen"),
    ("anti-gewalt-training/", "Anti-Gewalt-Training", "aat"),
    ("ueber-mich/", "Über mich", "ueber"),
]
SAEULEN = [("01", "Beratung", "beratung"), ("02", "Sport", "sport"), ("03", "Schulungen", "schulungen")]

def kopf(r, aktiv):
    links = "\n".join(
        f'        <a href="{r}{h}"{" aria-current=\"page\"" if k == aktiv else ""}>{t}</a>'
        for h, t, k in NAV
    )
    return f"""  <a class="skip-link" href="#inhalt">Zum Inhalt springen</a>

  <header class="kopf">
    <div class="container kopf__inner">
      <a class="marke" href="{r}index.html" aria-label="BSSD — zur Startseite">
        <span class="marke__wort">BSSD</span>
        <span class="marke__zusatz">Beratung · Schulungen · Sport · Dienstleistungen</span>
      </a>
      <button class="burger" aria-label="Menü öffnen" aria-expanded="false" aria-controls="hauptnav">☰</button>
      <nav class="nav" id="hauptnav" aria-label="Hauptnavigation">
{links}
        <a class="knopf" href="{r}kontakt/"{" aria-current=\"page\"" if aktiv == "kontakt" else ""}>Kontakt</a>
      </nav>
    </div>
  </header>
"""

def umschalter(r, aktiv):
    if aktiv not in {k for _, _, k in SAEULEN}:
        return ""
    punkte = "\n".join(
        f'      <li><a href="{r}{k}/" data-s="{k}"{" aria-current=\"page\"" if k == aktiv else ""}><span>{n}</span>{t}</a></li>'
        for n, t, k in SAEULEN
    )
    return f"""
  <nav class="umschalter" aria-label="Die drei Säulen">
    <ul class="umschalter__liste container">
{punkte}
    </ul>
  </nav>
"""

def fuss(r):
    return f"""
  <footer class="fuss">
    <div class="container">
      <div class="fuss__raster">
        <div>
          <a class="marke" href="{r}index.html"><span class="marke__wort">BSSD</span></a>
          <p style="margin-top:16px">Beratung &amp; Schulungen &amp; Sport &amp; Dienstleistungen<br />Gregor Nebel</p>
        </div>
        <div>
          <h4>Säulen</h4>
          <ul>
            <li><a href="{r}beratung/">01 · Beratung</a></li>
            <li><a href="{r}sport/">02 · Sport</a></li>
            <li><a href="{r}schulungen/">03 · Schulungen</a></li>
            <li><a href="{r}anti-gewalt-training/">Einzel-AAT®</a></li>
          </ul>
        </div>
        <div>
          <h4>BSSD</h4>
          <ul>
            <li><a href="{r}ueber-mich/">Über mich</a></li>
            <li><a href="{r}kontakt/">Kontakt</a></li>
            <li><a href="{r}impressum/">Impressum</a></li>
            <li><a href="{r}datenschutz/">Datenschutz</a></li>
          </ul>
        </div>
        <div>
          <h4>Kontakt</h4>
          <ul>
            <li>{wert("telefon", "Telefon")}</li>
            <li>{wert("email", "E-Mail")}</li>
            <li>{wert("ort", "Ort / Einsatzgebiet")}</li>
          </ul>
        </div>
      </div>
      <div class="fuss__unten">
        <span>© <span id="jahr">2026</span> BSSD · Gregor Nebel</span>
        <span>Aggression verstehen · Verhalten ändern · Zukunft gestalten</span>
      </div>
    </div>
  </footer>
"""

def seite(meta, inhalt):
    tiefe = meta["pfad"].count("/")
    r = "../" * tiefe
    saeule = meta.get("saeule", "beratung")
    aktiv = meta.get("aktiv", "")
    inhalt = (inhalt.replace("{R}", r)
              .replace("{EMAIL}", wert("email", "E-Mail"))
              .replace("{TELEFON}", wert("telefon", "Telefon"))
              .replace("{ORT}", wert("ort", "Ort / Einsatzgebiet"))
              .replace("{EMAIL_ROH}", STAMM["email"]))
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{meta["titel"]}</title>
  <meta name="description" content="{meta["beschreibung"]}" />
  <meta name="theme-color" content="#0b1622" />
  <link rel="icon" href="{r}assets/img/favicon.svg" type="image/svg+xml" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..900&amp;family=EB+Garamond:wght@400;500&amp;family=Source+Sans+3:wght@400;600;700&amp;display=swap" />
  <link rel="stylesheet" href="{r}assets/css/bssd.css" />
</head>
<body data-saeule="{saeule}">
{kopf(r, aktiv)}{umschalter(r, aktiv)}
  <main id="inhalt">
{inhalt.rstrip()}
  </main>
{fuss(r)}
  <script src="{r}assets/js/bssd.js" defer></script>
</body>
</html>
"""

def main():
    for datei in sorted(QUELLE.glob("*.html")):
        roh = datei.read_text(encoding="utf-8")
        kopfteil, inhalt = roh.split("\n---\n", 1)
        meta = dict(z.split(": ", 1) for z in kopfteil.strip().splitlines())
        meta["pfad"] = "" if meta["pfad"] == "-" else meta["pfad"]  # "-" = Startseite
        ziel = WURZEL / meta["pfad"] / "index.html"
        ziel.parent.mkdir(parents=True, exist_ok=True)
        ziel.write_text(seite(meta, inhalt), encoding="utf-8")
        print("gebaut:", ziel.relative_to(WURZEL))

if __name__ == "__main__":
    main()
