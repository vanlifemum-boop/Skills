# Mittelfinger auf Reisen — Website

Statische Website: HTML, CSS, etwas JavaScript. Kein Build, keine
Abhängigkeiten, kein Framework. `index.html` im Browser öffnen genügt.

> **Ich scheiß drauf. Ich fahr los.**
> Gegen Konventionen. Für Freiheit.

## Dateien

| Datei | Rolle |
|---|---|
| `index.html` | die ganze Seite: Auftakt, Karte, Reise-Blog, Entstehungsgeschichte, Fuß |
| `blog-start-wiesbaden.html` | erster Blogbeitrag |
| `impressum.html`, `datenschutz.html` | Pflichtseiten |
| `404.html` | Fehlerseite |
| `daten.js` | **Orte und Beiträge — die einzige Pflegestelle** |
| `styles.css` | Design-System und die Orbit-Animation |
| `main.js` | Animation aufbauen, Karte, Listen |
| `bilder/` | Fotos, sobald welche da sind |

## Was du als Erstes machen solltest

1. **Impressum und Datenschutz ausfüllen.** Beide sind Vorlagen mit
   `[eckigen Klammern]`. Ohne vollständiges Impressum sollte die Seite in
   Deutschland nicht online gehen. Das ist keine Rechtsberatung — im Zweifel
   einmal prüfen lassen.
2. **Kontaktweg festlegen.** Die Seite verzichtet bewusst auf
   E-Mail-Adressen und Formulare. Gesetzlich ist trotzdem eine schnelle
   elektronische Kontaktaufnahme vorgeschrieben; welcher Weg das ist, gehört
   ins Impressum.
3. **Social-Media-Profile eintragen**, sobald sie stehen — im Fuß von
   `index.html` und in den Unterseiten (dort steht bisher nur ein Satz, kein
   Link).
4. **Orte und Beiträge ergänzen** — siehe unten.

## Orte und Beiträge pflegen

Alles steht in `daten.js`, oben in der Datei ist jedes Feld erklärt.

**Neuen Ort:** Block kopieren, Name, Land, Koordinaten und Datum eintragen.
Die Karte setzt den Finger automatisch, die Liste darunter ebenso. `start:
true` gibt es nur einmal — bei Wiesbaden.

**Neuen Beitrag:** `blog-start-wiesbaden.html` kopieren, umbenennen, Texte
ersetzen, dann in `daten.js` unter `BEITRAEGE` eintragen. Die Übersicht auf
der Startseite sortiert nach Datum, das neueste zuerst.

## Die Animation im Auftakt

Drei Ringe aus Icon-Kacheln drehen sich auf einer gekippten Ebene, der
mittlere gegenläufig. Nach außen werden die Kacheln unschärfer und blasser.
Die Mechanik stammt aus der Waitlist-Hero-Vorlage (React/Tailwind);
übernommen ist davon nur das CSS, alles andere ist eigen — die zwölf
Reise-Icons sind selbst gezeichnete Inline-SVG, keine Icon-Bibliothek und
kein CDN.

Geschraubt wird an drei Stellen:

- **`RINGE` in `main.js`** — Durchmesser, Umlaufdauer, Unschärfe, Deckkraft,
  Anzahl der Kacheln je Ring.
- **`ICONS` und `TOENE` in `main.js`** — welche Symbole und welche Farben.
- **`.orbit-plane` in `styles.css`** — `rotateX(58deg)` bestimmt, wie stark
  die Ebene gekippt ist.

Zwei Dinge sehen technisch wie Umwege aus und sind keine: Unschärfe und
Deckkraft sitzen auf den **Kacheln**, nicht auf dem Ring. Beides macht ein
Element zur Gruppe und würde die 3D-Ebene einebnen — die Kacheln lägen dann
flach auf der Scheibe, statt aufrecht zu stehen. Und `.orbit-tile` dreht mit
`rotateX(-58deg)` die Kippung der Ebene wieder heraus, damit die Icons den
Betrachter anschauen.

Bei `prefers-reduced-motion: reduce` steht alles still — die Kacheln bleiben
sichtbar und lesbar, sie bewegen sich nur nicht.

## Die Karte

Leaflet mit Kacheln von OpenStreetMap. Beides sind fremde Server, die dabei
die IP-Adresse der Besucher sehen — deshalb lädt die Karte **erst nach einem
Klick**, und die Entscheidung wird nur lokal im Browser gemerkt. Das ist der
Grund, warum das umständlicher gebaut ist als nötig: so bleibt die Seite ohne
Einwilligungsbanner sauber.

Lädt die Karte nicht (kein Netz, Blocker), bleiben die Orte als Liste
darunter lesbar. Die Liste ist kein Notbehelf, sondern die barrierefreie
Fassung derselben Daten.

Der Marker ist der Mittelfinger selbst, kein Standard-Pin — gezeichnet in
`fingerSvg()` in `main.js`, dieselbe Form wie Markenzeichen und Favicon.

## Farben und Schrift

| Farbe | Wofür |
|---|---|
| Weiß `#ffffff` | Grund der ganzen Seite |
| Tinte `#18122b` | Schrift und Fußbereich, Schwarz mit Violettstich |
| Violett `#5b21b6` → Türkis `#115e59` | Verlauf im Auftakt |
| Lila `#7c3aed` | Schaltflächen und Links |
| Türkis `#0f766e` | zweiter Akzent, kontraststark genug für kleine Schrift |
| Mint `#5eead4` | Akzent auf dunklem Grund |

Systemschriften, eng geführt und fett. Es werden keine Schriften nachgeladen —
das spart einen Datenschutz-Absatz und eine Ladezeit.

Alle Kontraste sind gegen WCAG AA gerechnet (der niedrigste Wert liegt bei
4,88 : 1). Tastaturbedienung, Skip-Link und `prefers-reduced-motion`
funktionieren, Schaltflächen sind mindestens 52 px hoch.

## Veröffentlichen

Der Workflow `.github/workflows/pages.yml` im Repo veröffentlicht genau
diesen Ordner über GitHub Pages, sobald hier etwas gepusht wird — auf `main`
und auf dem Arbeits-Branch. Die Adresse steht danach im Actions-Lauf und
unter Settings → Pages.

Alternativ: Ordner zu Netlify oder Cloudflare Pages ziehen, kein
Build-Befehl, kein Ausgabeverzeichnis. Oder klassisch per FTP hochladen.

Lokal ansehen:

```bash
python3 -m http.server 8080
```

## Noch offen

- [ ] Impressumsangaben eintragen
- [ ] Kontaktweg festlegen und ins Impressum schreiben
- [ ] Datenschutz: Hoster und Datum ergänzen
- [ ] Social-Media-Profile verlinken
- [ ] Fotos ergänzen (siehe `bilder/LIESMICH.md`)
- [ ] weitere Orte und Beiträge in `daten.js`
