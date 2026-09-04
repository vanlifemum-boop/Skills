# Neues Leben Masuren — Website

Statische Website für den Verkauf von Seegrundstücken in Ermland-Masuren (Polen)
samt Tiny House, Fertighaus und Autarkie-Modulen.

Kein Build, kein Framework, kein Backend: reines HTML, CSS und JavaScript. Die
Seite lädt **keine** externen Schriften, Skripte oder Bilder — sie funktioniert
vollständig offline und setzt keine Cookies.

## Lokal ansehen

```bash
cd masuren
python3 -m http.server 8000
```

Dann http://localhost:8000 im Browser öffnen.

## Aufbau

| Datei | Inhalt |
|---|---|
| `index.html` | Startseite |
| `grundstuecke.html` | Die Grundstücke, Baurecht, Besichtigung |
| `haeuser.html` | Tiny House, Fertighaus, Autarkie-Module |
| `kosten.html` | Kostenrechner, Kaufnebenkosten, laufende Kosten |
| `kaufablauf.html` | Ablauf des Kaufs, Notar, Vollmacht |
| `leben-in-polen.html` | Anmeldung, PESEL, Versicherung, Alltag |
| `olsztyn.html` | Die Stadt 30 Autominuten entfernt |
| `schule.html` | Polnische Schule, Homeschooling, Fernunterricht |
| `wiederverkauf.html` | Weitervermittlung von Grundstück und Haus |
| `kontakt.html` | Anfrageformular |
| `impressum.html`, `datenschutz.html` | Pflichtseiten |
| `styles.css` | Design-System (Farben, Typografie, Komponenten) |
| `main.js` | Menü, Scroll-Reveals, Formular |
| `kosten.js` | Kostenrechner — **alle Beispielpreise stehen oben im Objekt `PREISE`** |

Kopf- und Fußbereich sind auf jeder Seite als HTML ausgeschrieben. Wenn du an der
Navigation etwas änderst, musst du es in allen Seiten ändern:

```bash
cd masuren
sed -i 's|alte-seite.html|neue-seite.html|g' *.html
```

## Bevor die Seite online geht

Arbeite **`PLATZHALTER.md` ab.** Dort steht, welche Angaben noch fehlen und wo sie
im Code liegen. Besonders wichtig: Impressum, Datenschutzerklärung, E-Mail-Adresse
und Formular-Endpoint.

### Formular scharf schalten

1. Bei einem Formulardienst (z. B. Formspree) ein Formular anlegen.
2. In `kontakt.html` das `data-endpoint`-Attribut auf die echte URL setzen.
3. In `main.js` die Konstante `KONTAKT_EMAIL` auf die echte Adresse setzen.
4. Den Hinweiskasten „Hinweis zum Formular" in `kontakt.html` entfernen.
5. Den Dienst in `datenschutz.html` benennen.

Solange Schritt 2 offen ist, verschickt das Formular bewusst nichts: Es sagt dem
Besucher offen, dass der Versand noch nicht eingerichtet ist, und bietet eine
vorausgefüllte E-Mail an. Es tut also nie so, als sei die Nachricht angekommen.

## Veröffentlichen

Die Seite ist ein Ordner mit statischen Dateien und läuft bei jedem Hoster.

> **Achtung:** Dieses Repository veröffentlicht über GitHub Pages bereits den
> Ordner `docs/` unter der Domain `www.gutachtenkompass.eu`. GitHub Pages kann pro
> Repository nur **eine** Quelle bedienen — dieser Ordner wird dort also nicht
> automatisch mitveröffentlicht, und `docs/` darf dafür nicht überschrieben werden.

Drei Wege, je nach Vorliebe:

**a) Eigenes Repository + GitHub Pages (kostenlos)**
Neues Repository anlegen, den Inhalt von `masuren/` hineinkopieren, unter
*Settings → Pages* die Quelle auf den Branch stellen. Für eine eigene Domain eine
Datei `CNAME` mit der Domain anlegen und beim Domain-Anbieter einen CNAME-Eintrag
auf `<benutzername>.github.io` setzen.

**b) Netlify / Vercel (kostenlos, am schnellsten)**
Ordner auf netlify.com per Drag & Drop hochladen oder das Repository verbinden.
Domain und HTTPS richtet der Dienst automatisch ein.

**c) Klassisches Webhosting**
Den Inhalt von `masuren/` per FTP ins Web-Wurzelverzeichnis laden. Darauf achten,
dass HTTPS aktiv ist und HTTP dorthin weiterleitet.

## Zugänglichkeit und Qualität

Beim Ändern bitte erhalten:

- Sprungmarke „Zum Inhalt springen" und sichtbarer Tastaturfokus
- `prefers-reduced-motion` wird respektiert (Animationen aus)
- sinnvolle Alternativtexte, sobald echte Bilder eingesetzt werden
- keine externen Requests — Schriften und Skripte bleiben lokal
- breite Tabellen stehen in `<div class="tabelle-wrap">`, damit sie einzeln
  scrollen und die Seite nicht horizontal überläuft

## Wichtiger inhaltlicher Hinweis

Die Seite trifft an mehreren Stellen Aussagen zu polnischem Recht, Steuern und
Schulwesen. Was davon belegt und was Beispielwert ist, steht am Ende von
`PLATZHALTER.md`. Bitte nichts davon „glattziehen", ohne es zu prüfen — besonders
nicht den Hinweis, dass es in der Region keine deutsche Schule gibt.
