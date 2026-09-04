# Mail-Betrieb

Die ganze Plattform ist ein Postfach und eine Tabelle. Damit das trägt, muss beides
sauber aufgesetzt sein — sonst wird aus „anonym" schnell „alles liegt ungeordnet in
einem Google-Postfach".

---

## 1. Das Postfach

- **Anbieter in Deutschland**, mit Auftragsverarbeitungsvertrag: mailbox.org, Posteo
  oder ein eigener Server. **Kein Gmail, kein Outlook.com.** Bei dieser Zielgruppe ist
  das kein Puritanismus, sondern Voraussetzung.
- **Getrennte Adressen** — sie machen die Sortierung und die Löschung leicht:

  | Adresse | Wofür |
  |---|---|
  | `hallo@…` | Anfragen von Suchenden und Anbietenden |
  | `termine@…` | Anmeldungen zu Veranstaltungen |
  | `mitglied@…` | Mitgliedschaft, Rechnung, Kündigung |
  | `melden@…` | wenn etwas schiefgegangen ist |

- **Autoantwort** auf allen vier, siehe Vorlage 0.
- **Zwei-Faktor-Anmeldung** aktiviert. Ein gekapertes Postfach wäre hier eine
  Katastrophe.
- **Kein Weiterleiten** in ein privates Postfach. Auch nicht kurz.

---

## 2. Vorlagen

### 0 — Autoantwort (sofort, automatisch)

> Deine Nachricht ist angekommen. Ich lese sie persönlich und melde mich innerhalb von
> drei Tagen.
>
> Falls es gerade nicht auszuhalten ist, warte bitte nicht auf mich:
> Telefonseelsorge 0800 111 0 111, rund um die Uhr, kostenlos.
> Hilfetelefon Gewalt gegen Frauen 116 016.
>
> Diese Mail ist automatisch. Antworte einfach darauf, wenn dir noch etwas einfällt.

### 1 — Erste Antwort an eine Suchende

> Hallo [Name],
>
> danke, dass du geschrieben hast. Du musst mir nichts weiter erklären.
>
> Ich schaue jetzt, wer in Region [X] unterwegs ist, und frage dort an. Das dauert
> ein paar Tage. Ich nenne dabei weder deinen Namen noch deinen Ort — nur, worum es
> geht und dass es in deiner Ecke ist.
>
> Wenn jemand ja sagt, frage ich noch einmal bei dir nach, bevor ich irgendetwas
> weitergebe. Ohne dein zweites Ja passiert nichts.
>
> [Falls Termin angefragt:] Am [Datum] ist [Veranstaltung] in Region [X].
> Der Beitrag liegt bei [X] €. Wenn das gerade nicht geht, schreib mir ein Wort —
> dann bist du eingeladen, das sieht niemand.

### 2 — Anfrage an eine Anbietende

> Hallo [Name],
>
> ich habe eine Anfrage, die zu dem passt, was du angeboten hast:
>
> Es geht um [Kategorie], in Region [X], ungefähr [Zeitraum]. Kinder sind dabei: [ja/nein].
>
> Mehr weiß ich im Moment auch nicht — und mehr sage ich absichtlich nicht.
>
> Magst du? Ein „ja" oder „geht gerade nicht" reicht mir, ohne Begründung.

### 3 — Kontaktherstellung (erst nach beidem Ja)

> Hallo ihr beiden,
>
> ihr habt beide zugestimmt, deshalb bringe ich euch jetzt zusammen.
>
> [Name A] — [Name B]. Ab hier macht ihr das unter euch aus.
>
> Zwei Bitten: Trefft euch beim ersten Mal an einem öffentlichen Ort. Und sagt mir
> hinterher kurz, ob es gepasst hat — ein Wort reicht.
>
> Was ihr euch erzählt, bleibt bei euch. Auch vor mir.

### 4 — Einladung bestätigen

> Hallo [Name],
>
> du bist dabei, alles ist geregelt. Auf der Liste stehst du wie alle anderen, es gibt
> keine getrennte Abrechnung und niemand am Tisch weiß davon.
>
> Treffpunkt: [genaue Adresse], [Uhrzeit].
>
> Wenn du doch nicht kannst, sag einfach ab. Das ist kein Problem und kostet nichts.

### 5 — Absage, wenn niemand gefunden wurde

> Hallo [Name],
>
> ich habe gefragt, aber in Region [X] hat gerade niemand Zeit. Das tut mir leid und
> es liegt nicht an dir.
>
> Ich behalte deine Anfrage noch [4 Wochen] im Blick und melde mich, sobald sich
> etwas ergibt. Wenn du das nicht möchtest, schreib ein Wort und ich lösche sie sofort.
>
> Am [Datum] ist [Stammtisch] in Region [X] — dorthin kannst du auch einfach so kommen.

---

## 3. Die Vermittlungsliste

Eine einzige verschlüsselte Tabelle, lokal auf einem Rechner (VeraCrypt-Container
oder verschlüsselte Festplatte). **Nicht in einer Cloud.**

| Spalte | Inhalt |
|---|---|
| Kürzel | fortlaufend, z. B. `A-041` — nie ein Name |
| Rolle | sucht / bietet |
| Region | eine Ziffer |
| Kategorien | Stichworte |
| Kinder | ja / nein |
| Erste Mail | Datum |
| Stand | offen / angefragt / vermittelt / erledigt / gelöscht |
| Rückmeldung | gut / okay / nicht gut |
| Löschen am | Datum |

Namen und Mailadressen bleiben **ausschließlich im Postfach**, nie in der Tabelle.
Die Tabelle allein sagt nichts über irgendjemanden aus. Falls sie je in falsche Hände
gerät, steht dort nichts Verwertbares.

---

## 4. Löschfristen

| Was | Wann weg |
|---|---|
| Anfrage, erledigt | 3 Monate nach Abschluss |
| Anfrage, ohne Vermittlung | 3 Monate nach der Absage |
| Anmeldungen zu einem Termin | 4 Wochen nach dem Termin |
| Rechnungen und Mitgliedsdaten | 10 Jahre — gesetzliche Aufbewahrungspflicht, kein Ermessen |
| Meldungen über Vorfälle | 3 Jahre, getrennt abgelegt |
| Zeile in der Vermittlungsliste | mit der Anfrage |

Einmal im Quartal ein fester Termin im Kalender: löschen. Sonst passiert es nie.

Wichtig für die Datenschutzerklärung: Rechnungsdaten müssen bleiben, alles andere
nicht. Das ehrlich schreiben — „wir löschen alles sofort" wäre gelogen.

---

## 5. Was du niemals per Mail machst

- Rechtliche Einschätzungen geben. Auch nicht „nur meine Meinung".
- Namen, Orte oder Details der einen Seite an die andere weitergeben, bevor beide
  zugestimmt haben.
- Screenshots aus Akten oder Behördenschreiben anfordern oder speichern.
- Mails weiterleiten. Immer neu schreiben, nur mit dem, was nötig ist.
- Über Dritte reden, die nicht gefragt wurden.

---

## 6. Wenn eine Mail Sorge macht

Manche Nachrichten werden schwer sein. Feste Reaktion, damit du im Moment nicht
improvisieren musst:

1. Antworten, ruhig, ohne Diagnose, ohne Rat.
2. Die Nummern nennen: Telefonseelsorge 0800 111 0 111, Hilfetelefon 116 016,
   im Notfall 112.
3. Anbieten, dass jemand mitkommt oder anruft — konkret, nicht vage.
4. Nicht selbst zur Krisenbegleitung werden. Du bist Veranstalterin, nicht Therapeutin.
   Das schützt dich und sie.

Bei akuter Gefahr für ein Kind gilt kein Versprechen von Vertraulichkeit mehr.
Das gehört so auch in die Verhaltensregeln — vorher, nicht hinterher.
