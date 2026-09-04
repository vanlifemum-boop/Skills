# Mal wieder normal sein

**Gemeinsam statt allein.** Stammtische, Ausflüge, Auszeiten und Begleitung zu
Terminen für Mütter, die gerade viel tragen.

Zwei Grundsätze, aus denen sich alles Weitere ergibt:

1. **Auf der Seite steht niemand.** Keine Profile, keine Börse, keine Suche nach
   Personen. Sichtbar sind nur Zahlen, Regionen und Termine. Jede Anfrage kommt als
   E-Mail an — und wird von Hand weitergefragt.
2. **Dahinter steht eine Firma, kein Verein.** Kein Spendenrecht, keine
   Gemeinnützigkeit, keine Bedürftigkeitsprüfung. Wer zahlen kann, zahlt Rechnung plus
   freiwilligen Aufschlag. Wer nicht kann, wird eingeladen — unsichtbar für alle anderen.

---

## Dateien

| Datei | Inhalt |
|---|---|
| `index.html` | Lauffähiger Prototyp der Startseite mit Anfrage-Baukasten |
| `design-tokens.css` | Farben, Typo, Raster, Motion |
| `KONZEPT.md` | Seitenstruktur, Preismodell, was sichtbar ist und was nicht |
| `MAIL-BETRIEB.md` | Postfach, Antwortvorlagen, Vermittlungsliste, Löschfristen |
| `RECHT.md` | Steuern, Mitgliedschaft, RDG-Grenze, Anonymität vs. Rechnung, Reiserecht |

Die Datenbankdateien aus der ersten Fassung sind entfallen — es gibt keine Datenbank.

---

## Stack

Bewusst minimal. Es gibt nichts zu warten, was kaputtgehen kann.

- **Astro** (oder reines HTML) — statisch, schnell, kein Login, kein Server
- **Hosting** Cloudflare Pages oder Netlify, Free-Tier reicht
- **Postfach** mailbox.org oder Posteo, mit Auftragsverarbeitungsvertrag
- **Mitgliedschaft** Steady (deutsch) statt Patreon, oder SEPA-Lastschrift direkt
- **Schriften selbst hosten** — im Prototyp noch per CDN eingebunden, das muss weg
- Keine Analytics, keine Karten, keine eingebetteten Feeds, keine Drittanbieter-Skripte

---

## Der Anfrage-Baukasten

Das Herzstück auf der Startseite. Kein Formular, das irgendwohin gesendet wird:
Die Seite baut im Browser einen fertigen Mailtext zusammen, den die Nutzerin sieht,
ändern und dann selbst abschicken oder kopieren kann.

Vorteil: Es verlässt nichts den Rechner, bevor sie sendet. Kein Server, keine
Übermittlung, keine Einwilligung für etwas, das nicht stattfindet.

`mailto:` hakt auf manchen Handys — deshalb gibt es immer auch „Text kopieren".
Falls später ein echtes Formular nötig wird: eigener Server, TLS, Zustellung direkt
in ein deutsches Postfach. Kein Formspree, kein Google Forms.

---

## Nächste Schritte

**Diese Woche**
1. Domain sichern, Postfach einrichten, Autoantwort aktivieren
2. `index.html` in Astro überführen, Textseiten anlegen
3. Impressum und Datenschutz — die einzigen Pflichtseiten für Stufe 1
4. Instagram-Aufruf starten, erste Anfragen von Hand beantworten

**Danach, in dieser Reihenfolge**
5. Steuerberaterin: Umsatzsteuer und Behandlung des Trinkgelds klären
6. Betriebshaftpflicht abschließen
7. Teilnahmebedingungen und Widerrufsbelehrung
8. Erst dann: Rechnung mit Aufschlag und Mitgliedschaft freischalten

Ohne 5 bis 8 kann die Seite online sein, solange kein Geld fließt.

---

## Feste Regeln für jede Weiterarbeit

- Keine öffentliche Liste, in der Personen vorkommen. Nie.
- Kontakt zwischen zwei Menschen erst, wenn **beide** einzeln zugestimmt haben.
- Das Wort „Spende" kommt nirgends vor — die Firma ist nicht gemeinnützig.
- Kein Text darf nach Rechtsberatung klingen. „Wir gehen mit", nie „wir helfen dir mit
  dem Jugendamt".
- Wer eingeladen wurde, ist für die anderen nicht erkennbar — nicht auf der Liste,
  nicht auf der Rechnung, nicht am Tisch.
- Jede Veranstaltung trägt sichtbar „Kinder willkommen" — ja oder nein.
- Zahlen im Regionen-Raster immer mit Datum. Veraltete Zahlen sind schlimmer als keine.
