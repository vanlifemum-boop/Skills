# Was vor dem Livegang ersetzt werden muss

Diese Seite läuft, aber sie ist noch nicht fertig für die Öffentlichkeit.
Unten steht jede Stelle, an der etwas Erfundenes oder Vorläufiges steht.

**Schnellprüfung, ob noch etwas offen ist:**

```bash
grep -rn "platzhalter\|beispiel-domain-bitte-ersetzen\|noindex" docs/mwn/
```

Solange dieser Befehl etwas ausgibt, ist die Seite nicht livereif.

---

## 1 · Muss weg, bevor irgendjemand die Seite sieht

| Wo | Was | Womit ersetzen |
|---|---|---|
| `anfrage.js`, Konstante `MAIL` | `hallo@beispiel-domain-bitte-ersetzen.de` | die echte Adresse |
| `verhaltensregeln.html` | `melden@[DEINE-DOMAIN]` | die echte Meldeadresse |
| alle 13 `.html`-Dateien, im `<head>` | `<meta name="robots" content="noindex, nofollow">` | **löschen**, sobald die Seite unter ihrer eigenen Domain steht |

Die `noindex`-Zeile steht dort, weil die Vorschau vorläufig unter der Domain
eines anderen Projekts ausgeliefert wird. Unter der eigenen Domain muss sie raus,
sonst findet die Seite niemand.

---

## 2 · Impressum (`impressum.html`)

Alle rot markierten Klammern. Ohne diese Angaben darf die Seite nicht online:

- Firmenname mit Rechtsform
- Straße, Hausnummer, Postleitzahl, Ort
- vertretungsberechtigte Person
- E-Mail-Adresse (Pflicht) · Telefonnummer (keine Pflicht — eine E-Mail-Adresse
  mit Antwort binnen drei Tagen genügt; wenn keine Nummer, den Punkt streichen)
- Registergericht und Registernummer — entfällt bei einem Einzelunternehmen ohne Eintrag
- Umsatzsteuer-Identifikationsnummer **oder** Hinweis auf die Kleinunternehmer-
  regelung nach § 19 UStG
- redaktionell verantwortliche Person nach § 18 Abs. 2 MStV

## 3 · Datenschutzerklärung (`datenschutz.html`)

- Verantwortliche: Firma, Anschrift, E-Mail (Abschnitt 1)
- **Hosting-Anbieter mit Anschrift** und die Speicherdauer der Server-Protokolle
  (Abschnitt 2 und 10) — beim Anbieter erfragen, nicht schätzen
- **Postfach-Anbieter mit Anschrift** (Abschnitt 5) — dort auch den
  Auftragsverarbeitungsvertrag nach Art. 28 DSGVO abschließen
- Zahlungsdienstleister oder Bank, Steuerberatung (Abschnitt 9)
- zuständige Datenschutz-Aufsichtsbehörde mit Anschrift (Abschnitt 12)
- Datum unten

## 4 · Entwurfsseiten

`teilnahmebedingungen.html` und `widerruf.html` tragen ein rotes Band und sind
im Fuß als *Entwurf* gekennzeichnet. Sie sind **nicht geprüft**. Vor dem ersten
Euro, der fließt:

1. beide anwaltlich gegenlesen lassen,
2. die Platzhalter füllen,
3. das rote Band aus der Datei löschen (`<div class="entwurf">…</div>`),
4. das `<span class="f-entwurf">Entwurf</span>` aus dem Fuß **aller** Seiten
   entfernen — der Fuß steht in jeder Datei einzeln.

---

## 5 · Reihenfolge zum Abarbeiten

Aus `RECHT.md`, Abschnitt 10. Die Seite darf **jetzt schon** online sein,
solange sie nur informiert, zu Stammtischen einlädt und Anfragen per Mail
annimmt — also solange kein Geld fließt.

1. Domain sichern, Postfach bei einem deutschen Anbieter einrichten,
   Autoantwort aktivieren (Vorlage 0 in `MAIL-BETRIEB.md`)
2. Impressum und Datenschutz ausfüllen
3. `noindex` entfernen, Seite unter eigener Domain ausliefern
4. Steuerberaterin: Umsatzsteuer, Kleinunternehmerregelung, Behandlung des Trinkgelds
5. Betriebshaftpflicht mit Einschluss von Veranstaltungen abschließen
6. Teilnahmebedingungen und Widerrufsbelehrung prüfen lassen
7. Rechnungsvorlage bauen — Kleinbetragsregelung nach § 33 UStDV nutzen, wo möglich
8. Abrechnung einrichten, Kündigungsknopf nach § 312k BGB nicht vergessen
9. **Erst dann** die Mitgliedschaft freischalten und die Hinweiskästen
   „noch nicht freigeschaltet" aus `index.html` und `mitgliedschaft.html` löschen

---

## 6 · Beispielzahlen

Alles in `daten.js` sind Beispiele: die zehn Regionen mit ihren Mamis- und
Stammtischzahlen, die drei Termine, der Einladungs-Zähler. Vor dem Livegang
durch echte Zahlen ersetzen und `STAND` mitändern.

Im Fuß jeder Seite steht dazu ein ehrlicher Satz. Auch der muss weg, sobald
die Zahlen stimmen — er steht in jeder Datei einzeln:

> Alle Zahlen auf dieser Seite sind Beispiele. Vorschaufassung, noch nicht öffentlich.

---

## 7 · Wenn der Kopf oder der Fuß sich ändert

Es gibt bewusst kein Build-Werkzeug — dreizehn ganz normale HTML-Dateien.
Der Preis dafür: Kopf und Fuß stehen in jeder Datei einzeln. Wer sie ändert,
ändert sie überall. Für die immer gleichen Fälle reicht:

```bash
cd docs/mwn
grep -l "alter Text" *.html | xargs sed -i 's/alter Text/neuer Text/g'
```
