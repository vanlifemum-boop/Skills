# Bilder

Hier kommen die Fotos rein. Solange ein Bild fehlt, zeigt die Seite einen
sichtbar gestreiften Platzhalter mit Beschreibung — bewusst so, damit man nie
im Zweifel ist, was noch fehlt.

## Ein Foto einbauen

**In der Reisekarte / Ortsliste:** in `../orte.js` beim jeweiligen Ort eintragen:

```js
foto: "bilder/lofoten-reine.jpg",
alt:  "Ausgestreckter Mittelfinger vor den Bergen von Reine, dahinter der Camper im Regen",
```

**Auf einer Seite:** den Platzhalter-Block

```html
<div class="foto"><span class="foto__label">Platzhalter: …</span></div>
```

ersetzen durch

```html
<div class="foto"><img src="bilder/dateiname.jpg" alt="Beschreibung" loading="lazy" /></div>
```

Bei Kacheln heißt die Klasse `kachel__media` statt `foto` — sonst identisch.

## Praktisches

- **Format:** JPEG für Fotos, quer 4:3 oder 5:4, hochkant 3:4.
- **Größe:** lange Kante etwa 1600 px, unter 300 KB. Alles darüber macht die
  Seite auf dem Handy im Funkloch unbenutzbar.
- **Dateinamen:** klein, ohne Umlaute und Leerzeichen — `transfagarasan-nebel.jpg`.
- **`alt` ist Pflicht.** Ein Satz, was zu sehen ist. Nicht „Foto“, nicht leer.
- **Keine fremden Bilder** ohne Erlaubnis. Auch keine aus der Bildersuche.
