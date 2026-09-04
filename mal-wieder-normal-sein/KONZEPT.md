# Konzept — Fassung 2 (Firma, Mail-Betrieb, nichts öffentlich)

Geändert gegenüber Fassung 1:

| Vorher | Jetzt |
|---|---|
| Öffentliche Angebots-Börse | **Ersatzlos gestrichen.** Es gibt keine Liste, in der Personen stehen. |
| Anmeldung, Profile, Datenbank | Keine. Alles läuft über E-Mail und eine handgeführte Liste. |
| Verein, Spenden, Solidartopf | Firma. Rechnung mit freiwilligem Aufschlag, plus Mitgliedschaft. |
| Matching per Software | Vermittlung von Hand — bewusst. |

---

## 1. Warum das die bessere Konstruktion ist

Kein öffentliches Verzeichnis heißt: Es gibt nichts zu durchsuchen, nichts zu
screenshotten, nichts, was in einem Verfahren gegen jemanden verwendet werden kann.
Kein Konto heißt: keine Passwörter, keine Datenlecks, keine Löschanträge.

Die Vermittlung von Hand ist keine Notlösung, sondern das Produkt. Genau dafür zahlt
die Mitgliedschaft: Ein Mensch liest, denkt nach und fragt gezielt bei jemandem an —
statt einer Trefferliste.

**Grenze:** Das funktioniert bis etwa 150 bis 200 aktiven Personen. Danach braucht es
entweder Hilfe beim Lesen der Mails oder doch ein System. Diese Grenze früh im Blick
behalten — sie kommt schneller als gedacht.

---

## 2. Was auf der Seite überhaupt sichtbar ist

Sichtbar sind ausschließlich **Zahlen und Regionen**, nie Personen:

- Das Regionen-Raster: „Region 9 — 13 Mamis, 2 Stammtische". Von Hand gepflegt,
  einmal im Monat aktualisiert, mit Datum versehen.
- Die Termine: Datum, Art, Region, „Kinder willkommen", Anzahl freier Plätze.
  Der genaue Ort steht nur in der Bestätigungsmail.
- Der Einladungs-Zähler: wie viele Einladungen offen, vergeben, noch nicht finanziert.

Alles andere ist Text: was es gibt, wie es abläuft, was es kostet, was es nicht ist.

---

## 3. Der Anfrage-Baukasten

Statt eines Formulars, das irgendwo hin abgeschickt wird, baut die Seite im Browser
einen fertigen Mailtext zusammen. Zwei Knöpfe: „Als E-Mail öffnen" oder „Text kopieren".

Das ist bewusst so gelöst:
- Es verlässt nichts den Rechner, bevor die Frau selbst sendet.
- Sie sieht Wort für Wort, was sie verschickt, und kann alles ändern.
- Es braucht keinen Server, keine Datenbank, keine Einwilligungserklärung für eine
  Übermittlung, die gar nicht stattfindet.
- Wer keine Mail schreiben will, kopiert den Text in Signal oder WhatsApp.

Hinweis im Feld für Freitext: *„Bitte keine Namen, Adressen oder Aktenzeichen."*

**Wenn später doch ein serverseitiges Formular kommt** (weil `mailto:` auf manchen
Handys hakt): Es muss auf einem eigenen Server laufen, per TLS, und die Mail direkt
in ein deutsches Postfach zustellen. Kein Formspree, kein Google Forms, kein Typeform.

---

## 4. Seitenstruktur

```
/                        Startseite (alles Wesentliche auf einer Seite)
/mitgliedschaft          Die drei Stufen, was drin ist, Widerruf, Kündigung
/einladung               Wie das Einladen funktioniert, für beide Seiten
/begleitung              Was Begleitung ist und was nicht, wo sie erlaubt ist
/termine                 Ausführliche Terminliste
/stammtisch              Starterkit für eine neue Region
/silvester               Die mehrtägige Auszeit
/anonym                  Wie wir dich schützen, in einfacher Sprache
/verhaltensregeln
/teilnahmebedingungen  /widerruf  /datenschutz  /impressum
```

Reine Textseiten, statisch. Astro oder sogar nur HTML reicht vollkommen.

---

## 5. Das Preismodell

### Rechnung pro Veranstaltung

| Zeile | Betrag | Anmerkung |
|---|---|---|
| Teilnahme | Selbstkosten | deckt Lokal, Material, Organisation |
| Trinkgeld | +0 / 5 / 10 € | freiwillig, ein Klick |
| Ich lade mit ein | +15 € | finanziert einen ganzen Platz |
| Eingeladen | 0 € | erscheint als „bereits beglichen" |

Wichtig: Auf der Teilnehmerliste, im Lokal, beim Zahlen ist **nicht erkennbar**, wer
eingeladen wurde. Es gibt keine getrennte Abrechnung am Tisch. Das ist kein Detail,
das ist der Unterschied zwischen Würde und Almosen.

### Mitgliedschaft

| Stufe | Preis | Inhalt |
|---|---|---|
| Dabei | 3 € | Termine zuerst, Rundbrief |
| Mittendrin | 7 € | zusätzlich: Vermittlung von Begleitungen, Vorrang bei Plätzen, Vorlagen |
| Ich trage mit | 15 € | zusätzlich: finanziert monatlich eine Einladung |

Monatlich kündbar, Pause jederzeit möglich, wer pausiert bleibt eingeladen.

**Nicht in der Mitgliedschaft enthalten und nie versprochen:** rechtliche Einschätzung,
Erfolg bei Terminen, garantierte Verfügbarkeit einer Begleitperson. Formulierung immer
„Wir vermitteln", nie „Du bekommst".

### Plattform dafür

Steady statt Patreon prüfen: deutsches Unternehmen, Abrechnung in Euro, deutsche
Rechnungen, deutschsprachiger Support, DSGVO deutlich einfacher. Patreon ist
US-amerikanisch — bei dieser Zielgruppe ein unnötiges Argument gegen dich.
Alternativ direkt über die eigene Firma per SEPA-Lastschrift, dann bleibt alles im Haus.

---

## 6. Was du täglich machen musst

Realistisch, damit es nicht überrollt:

- **Postfach zweimal täglich**, feste Zeiten. Nicht dauernd.
- **Autoantwort** ist Pflicht: „Deine Mail ist angekommen. Wir melden uns innerhalb
  von drei Tagen. Wenn es dringend ist: hier sind die Nummern."
- **Vermittlung** aus einer handgeführten Liste (Tabelle, verschlüsselt, lokal).
- **Löschen** was erledigt ist — siehe `MAIL-BETRIEB.md`.
- **Einmal im Monat**: Zahlen im Regionen-Raster aktualisieren, Datum ändern.

---

## 7. Ton

Unverändert: Du-Ansprache, kurze Sätze, keine Behördensprache, keine Versprechen.
Neu dazu: Beim Geld wird nie beschönigt. „Das kostet 12 €. Wenn du sie nicht hast,
schreib uns ein Wort, dann bist du eingeladen." Keine Umschreibung, kein Antrag,
kein Formular.
