# Mittelfinger auf Reisen — Website

Statische Website zum Reiseprojekt „Mittelfinger auf Reisen“.
Kein Build, kein Framework, keine Abhängigkeiten: HTML, CSS und etwas
JavaScript. Doppelklick auf `index.html` reicht zum Anschauen.

> **Ich scheiß drauf. Ich fahr los.**
> Gegen Konventionen. Für Freiheit.

## Seiten

| Datei | Inhalt |
|---|---|
| `index.html` | Startseite: Hero, Botschaft, Kartenteaser, neueste Abenteuer, Scheiß-drauf-Momente, Mitmachen, nächster Stopp |
| `karte.html` | Reisekarte mit allen Orten als Pins, darunter dieselben Orte als Liste |
| `unterwegs.html` | Übersicht aller Reiseberichte |
| `beitrag-*.html` | einzelne Reiseberichte (drei Beispiele) |
| `warum-dieser-finger.html` | Entstehungsgeschichte und die Grundregel |
| `ueber-mich.html` | Über mich |
| `mitmachen.html` | Einsendeformular und Community-Regeln |
| `shop.html` | Merch: Aufkleber, Shirt, Aufnäher, kleiner Reisefinger |
| `kontakt.html` | Kontaktformular, E-Mail, Social Media |
| `impressum.html`, `datenschutz.html` | Pflichtseiten |
| `404.html` | Fehlerseite („Falsch abgebogen“) |

Dazu: `styles.css` (Design-System), `main.js` (Verhalten),
`orte.js` (**alle Orte**), `fonts/`, `bilder/`.

## Was du als Erstes machen solltest

1. **Orte pflegen** — `orte.js` ist die einzige Stelle dafür. Karte,
   Ortsliste und Startseiten-Teaser lesen alle daraus. Oben in der Datei
   steht, was jedes Feld bedeutet.
2. **Fotos ergänzen** — siehe `bilder/LIESMICH.md`.
3. **Impressum und Datenschutz ausfüllen** — beide sind Vorlagen mit
   `[eckigen Klammern]`. Ohne vollständiges Impressum sollte die Seite in
   Deutschland nicht online gehen.
4. **Formulare anschließen** — im HTML steht
   `data-endpoint="[PLATZHALTER-FORMULAR-ENDPOINT]"` (in `kontakt.html` und
   `mitmachen.html`). Trag dort die URL deines Formularanbieters ein, z. B.
   von Formspree. Solange der Platzhalter drinsteht, sagt das Formular
   ehrlich, dass der Versand noch nicht eingerichtet ist, statt Erfolg
   vorzutäuschen.
5. **Beispieltexte ersetzen** — die drei Reiseberichte und einige Absätze
   sind als Beispiel markiert (oranger Kasten `hinweis-demo`). Wenn deine
   eigenen Texte drinstehen, den Kasten löschen.
6. **Platzhalter suchen** — alles, was noch fehlt, ist im Text orange
   umrandet. Findbar mit:

   ```bash
   grep -rn "PLATZHALTER\|class=\"ph\"\|hinweis-demo" *.html
   ```

## Reisekarte

Die Karte nutzt [Leaflet](https://leafletjs.com/) und Kacheln von
OpenStreetMap. Beides sind fremde Server, die dabei die IP-Adresse der
Besucher sehen — deshalb lädt die Karte **erst nach einem Klick**, und die
Entscheidung wird nur lokal im Browser gemerkt. Das ist der Grund, warum das
etwas umständlicher gebaut ist als nötig: so bleibt die Seite ohne
Einwilligungsbanner sauber.

Wenn die Karte nicht lädt (kein Netz, Blocker), bleiben alle Orte als Liste
darunter lesbar. Die Liste ist kein Notbehelf, sondern die barrierefreie
Fassung derselben Daten.

## Design

| Farbe | Wofür |
|---|---|
| Asphalt-Schwarz `#14161a` | Hintergrund, Navigation, starke Flächen |
| Warmes Cremeweiß `#f4efe6` | Text und ruhige Inhaltsbereiche |
| Signalorange `#ff6a13` | Schaltflächen, Kartenpins, Akzente |
| Petrol `#0f5c58` | Natur-, Reise- und Camper-Abschnitte |
| Sand `#f2c14e` | Aufkleber, Straßenlinien, zweiter Akzent |

Überschriften in **Archivo Black** (liegt in `fonts/`, wird von diesem
Server ausgeliefert — kein Google Fonts, das erspart ein Datenschutzproblem).
Handschriftliche Akzente (`class="hand"`) nutzen die Systemschriften; wer
eine echte Handschrift will, lädt sich z. B. Caveat herunter, legt sie nach
`fonts/` und ergänzt ein `@font-face` in `styles.css`.

Alle Kontraste sind gegen WCAG AA geprüft, Tastaturbedienung und
`prefers-reduced-motion` funktionieren, Schaltflächen sind mindestens 48 px hoch.

## Veröffentlichen

Der Ordner ist eine fertige statische Seite — hochladen genügt.

- **GitHub Pages:** Das `docs/`-Verzeichnis dieses Repos gehört bereits zu
  einer anderen Seite. Für „Mittelfinger auf Reisen“ also den Inhalt dieses
  Ordners in ein eigenes Repository legen (als `docs/` oder Repo-Wurzel) und
  Pages dort aktivieren.
- **Netlify / Cloudflare Pages:** Ordner ins Dashboard ziehen, fertig.
  Kein Build-Befehl, kein Ausgabeverzeichnis.
- **Klassischer Webspace:** per FTP hochladen.

Lokal ansehen mit Live-Reload-freiem Minimalserver:

```bash
python3 -m http.server 8080
```

## Später

Vorgesehen, aber bewusst noch nicht gebaut: Community-Karte für Einsendungen,
Newsletter, Abstimmung über das nächste Ziel, Video-Tagebuch, eigene Rubrik
für Stellplätze. Die Struktur ist so angelegt, dass jedes davon eine weitere
Seite plus ein paar Zeilen in `orte.js` ist.
