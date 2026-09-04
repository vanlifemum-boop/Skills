# Platzhalter-Checkliste

Alles auf dieser Website, was noch keine echten Daten sind, ist im HTML mit
`data-platzhalter="..."` ausgezeichnet und wird im Browser sichtbar markiert
(hinterlegter, kursiver Text). Besucher erkennen sofort, dass es Beispielwerte
sind — die Seite behauptet nirgends, ein verbindliches Angebot zu machen.

**Alle Platzhalter finden:**

```bash
grep -rn 'data-platzhalter' masuren/*.html
```

**Beispielpreise im Rechner:** stehen gesammelt im Objekt `PREISE` ganz oben in
`kosten.js`. Dort einmal ändern genügt — der Rechner zieht alles daraus.

---

## Vor dem Livegang zwingend erledigen

| # | Was | Wo |
|---|---|---|
| 1 | Firmenname, Anschrift, Vertretung, Register, USt-ID | `impressum.html` |
| 2 | Gewerbeerlaubnis nach § 34c GewO klären (betrifft die Vermittlung beim Weiterverkauf!) | `impressum.html` |
| 3 | Hosting-Anbieter und ggf. Auftragsverarbeitung eintragen | `datenschutz.html` |
| 4 | Formulardienst benennen, sobald eingerichtet | `datenschutz.html` |
| 5 | HTTPS beim Hoster aktivieren und Weiterleitung prüfen | Hosting |
| 6 | E-Mail-Adresse eintragen (Konstante `KONTAKT_EMAIL`) | `main.js`, Zeile ~13 |
| 7 | Formular-Endpoint eintragen (`data-endpoint`) | `kontakt.html` |
| 8 | Datenschutzerklärung und Impressum juristisch prüfen lassen | — |

Solange 6 und 7 offen sind, verschickt das Formular bewusst nichts, sagt das dem
Besucher offen und bietet stattdessen eine vorausgefüllte E-Mail an. Auf
`kontakt.html` steht dazu ein sichtbarer Hinweiskasten — der kann raus, sobald
der Versand läuft.

## Inhalte, die noch fehlen

| Platzhalter | Bedeutung | Datei |
|---|---|---|
| `email`, `telefon` | Kontaktdaten (überall im Fußbereich) | alle Seiten |
| `parzelle-nr`, `groesse`, `seezugang`, `preis` | die drei Beispiel-Parzellen | `grundstuecke.html` |
| `entfernung-dorf`, `entfernung-stadt`, `winterdienst` | Entfernungen und Winterdienst | `grundstuecke.html` |
| `groesse-tiny`, `preis-tiny`, `groesse-fertig`, `preis-fertig` | Häuser | `haeuser.html` |
| `preis-brunnen`, `preis-solar`, `preis-abwasser`, `preis-strom`, `preis-zufahrt` | Autarkie- und Erschließungsmodule | `haeuser.html` |
| `notarsatz`, `uebersetzer` | geschätzte Nebenkosten | `kosten.html` |
| `grundsteuer`, `versicherung`, `wartung-klaeranlage`, `heizung`, `internet`, `winterdienst-kosten` | laufende Kosten | `kosten.html` |
| `notar-name`, `notar-ort` | der deutschsprachige Notar | `kaufablauf.html` |
| `provision`, `provision-faellig`, `provision-erfolglos`, `provision-laufzeit` | Konditionen Weiterverkauf | `wiederverkauf.html` |
| `hinweis` | Text in den Beispiel-Bannern — entfällt, sobald echte Daten drin sind | mehrere |

## Fotos

Überall, wo `<div class="bildfeld">` steht, gehört ein echtes Foto hin. Aktuell
zeigt die Seite dort gestaltete Platzhalterflächen mit dem Hinweis
„Hier kommt dein Foto" — bewusst **keine** gekauften oder fremden Bilder.

Ersetzen so:

```html
<img src="bilder/see-ufer.jpg" alt="Blick über den See auf das bewaldete Ufer"
     width="1600" height="1200" loading="lazy" />
```

Bitte an sinnvolle `alt`-Texte denken (beschreiben, was zu sehen ist) und die
Bilder vorher auf ~1600 px Breite verkleinern.

---

## Was auf der Seite belegt und **kein** Platzhalter ist

Diese Angaben sind recherchiert und sollten nur mit Quelle geändert werden:

- **2 % PCC** (`podatek od czynności cywilnoprawnych`) auf den Kaufpreis —
  das polnische Gegenstück zur Grunderwerbsteuer.
- **Grundbuchgebühren:** 200 PLN Eigentumseintragung + 100 PLN für das Anlegen
  eines Grundbuchblatts (zusammen rund 70 €).
- **Eigentumsübergang** erfolgt in Polen bereits mit der notariellen Beurkundung;
  der Grundbucheintrag wirkt deklaratorisch.
- **EU-Bürger** brauchen für normale Immobilien und Baugrundstücke keine
  Erwerbsgenehmigung — für Agrar- und Waldflächen sowie in der Grenzzone gelten
  Sonderregeln (KOWR-Vorkaufsrecht).
- **Homeschooling** (`edukacja domowa`) ist in Polen nach dem Bildungsgesetz
  erlaubt: Einschreibung an einer polnischen Schule, Genehmigung durch die
  Schulleitung, jährliche Prüfungen.
- **Keine deutsche Schule in der Region.** Die Willy-Brandt-Schule in Warschau
  (~200 km) ist die einzige Schule in Polen mit deutschem Bildungsgang. Das steht
  bewusst als Erstes auf `schule.html` — bitte nicht abschwächen.
- **Olsztyn:** rund 170.000 Einwohner, Hauptstadt der Woiwodschaft
  Ermland-Masuren, Universitätsklinik und weitere Krankenhäuser, Universität
  Ermland-Masuren, Flughafen Szymany ca. 60 km entfernt.

Rechtslage, Gebühren und Verfahren können sich ändern. Vor dem Livegang und
danach regelmäßig gegenprüfen — auf allen betroffenen Seiten steht deshalb ein
Hinweis, dass die Website keine Rechts- oder Steuerberatung ersetzt.
