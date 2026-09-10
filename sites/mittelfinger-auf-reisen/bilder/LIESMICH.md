# Bilder

Hier kommen die Fotos rein. Aktuell hat die Seite noch keine Bildflächen —
sie ist so gebaut, dass sie auch ohne Fotos fertig aussieht und nicht nach
Baustelle.

## Ein Foto in einen Blogbeitrag

In der Beitragsdatei (z. B. `../blog-start-wiesbaden.html`) an die passende
Stelle im `<article class="artikel">`:

```html
<img src="bilder/dateiname.jpg"
     alt="Ausgestreckter Mittelfinger vor dem Camper in der Einfahrt"
     loading="lazy"
     style="border-radius:16px;margin:26px 0" />
```

## Ein Foto ins Kartenfenster

`../daten.js` beim Ort ein Feld `foto` ergänzen und in `karteZeichnen()` in
`../main.js` ausgeben — dort steht schon der Aufbau des Popups.

## Praktisches

- **Format:** JPEG für Fotos, quer 4:3 oder 3:2, hochkant 3:4.
- **Größe:** lange Kante etwa 1600 px, unter 300 KB. Alles darüber macht die
  Seite auf dem Handy im Funkloch unbenutzbar.
- **Dateinamen:** klein, ohne Umlaute und Leerzeichen —
  `wiesbaden-einfahrt.jpg`.
- **`alt` ist Pflicht.** Ein Satz, was zu sehen ist. Nicht „Foto", nicht leer.
- **Keine fremden Bilder** ohne Erlaubnis. Auch keine aus der Bildersuche.
