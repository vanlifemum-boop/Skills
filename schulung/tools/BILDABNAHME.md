# Bildabnahme — 10.08.2026

Alle 18 Master gesichtet und gegen die Kriterien geprüft: kein lesbarer Text, keine Gesichter
oder Hände, Farbstimmung deckt sich mit dem Anker, wirkt weder anklagend noch rührselig,
keine falschen Verfahrensinhalte.

**Ergebnis: 12 freigegeben, 4 müssen neu, 2 mit Anmerkung.**

## Freigegeben

| Bild | Befund |
|---|---|
| `REF_1` | Der Anker sitzt. Patiniertes Messing, Petrol und Ocker, dunkler Grund. |
| `IMG_L1` | Sehr stark. Langer leerer Tisch, ein Stuhl, gesiegeltes Dokument, hohes Fensterlicht. |
| `IMG_L3` | Karteikarten in exakter Reihe, die letzte im Schatten. Genau der Brief. |
| `IMG_L5` | Glockenkurve aus Licht, roter Ausreißer weit außen. Der rote Akzent sitzt sparsam. |
| `IMG_L6` | Gekippter Klotzturm, drei Klötze wieder gestapelt. Etwas kalt, aber trägt den Merksatz. |
| `IMG_L10` | Kita-Fächer, Beobachtungsheft mit unleserlichen Strichen. Motiv stimmt. |
| `IMG_L11` | Dokument im Türspalt, harte Lichtkante. Eines der besten. |
| `IMG_L12` | Notizbuch, Stift, Uhr, Abendlicht. Warm und ruhig. |
| `IMG_L13` | Papierstapel mit vier farbigen Markern. |
| `IMG_END` | Kompass im Morgenlicht, ruhend. Trägt den Abschluss. |
| `IMG_PRINT` | Klemmbrett von oben, sehr aufgeräumt. Signalisiert „ausdrucken". |
| `REF_2` | Brauchbarer Zweitkandidat, nicht verwendet. |

## Müssen neu

### `IMG_L9` — liest sich als Friedhof

Sechs Wegmarken auf Erdboden im Nebel, mit Grabstein-Silhouetten. Bei einem Level über
Inobhutnahme, Pflegefamilie und Erkrankung ist das die denkbar schlechteste Assoziation.
**Neu:** glatte abstrakte Marker auf poliertem Boden **im Innenraum**, ausdrücklich
`no soil, no ground, no outdoor setting`.

### `IMG_L7` — Motiv verfehlt

Statt eines Maßstabs mit weichen, überlappenden Lichtbändern zeigt das Bild eine
Pendel-Apparatur mit Kugel. Ausgerechnet das Level, in dem das Bild den Schutzriegel tragen
soll — *Entwicklung verläuft in Spannen, nicht auf Termine* — trägt ihn nicht.
**Neu:** Maßstab in Nahaufnahme, Teilstriche als breite ineinander verlaufende Leuchtbänder.

### `IMG_L2` — falsches Konzept

Ein schwarzer **Schwärzungsbalken** statt einer leeren Unterschriftszeile. Schwärzung ist ein
anderes Thema (Akteneinsicht) und lenkt vom Merksatz ab.
**Neu:** ausdrücklich `completely blank and unmarked` für das breite helle Feld.

### `IMG_L4` — sieht aus wie ein Verhörraum

Zwei Stühle, nackte Betonwände, Lichtkegel von oben. Der Lehrtext daneben sagt ausdrücklich:
*Belastende Fragen sind Methode, nicht Angriff.* Das Bild sagt das Gegenteil und untergräbt
damit genau die Botschaft des Levels.
**Neu:** schlichter, ruhiger Beratungsraum, seitliches Tageslicht, neutrale Atmosphäre.

## Mit Anmerkung

### `IMG_L8` — Motiv richtig, Raum zu verfallen

Kinderjacke am Haken, Tür angelehnt, warmes Licht — genau der Brief. Aber der Flur blättert ab
und wirkt verlassen. In Kombination mit einer Kinderjacke kippt das Richtung
Vernachlässigungs-Bildsprache. **Neu gefasst** mit `tidy well-kept hallway, homely and safe`.

### `IMG_HERO` — anderes Objekt als der Anker

Zeigt einen kleinen runden Taschenkompass, nicht die Kompassrose aus `REF_1`. Die Farbwelt
passt, die Objektidentität nicht. Kein Fehler, aber ein Bruch in der Markenführung.
**Zusatz ergänzt:** `the same patinated brass compass rose disc as in the reference image`.

## Der systematische Befund

Die Eigenschaft **„weathered, patinated"** aus dem Referenzprompt ist von der Kompassrose auf
die **Innenräume** übergesprungen. Abblätternde Wände und Verfall finden sich in `IMG_L4`,
`IMG_L8`, `IMG_L10` und `IMG_HERO`. Beim Metallobjekt ist das gewollt — bei Räumen, in denen es
um Kinder geht, schadet es.

Gegenmittel ist ein neuer Baustein in `prompts.json`, der bei betroffenen Motiven über das Feld
`zusatz` angehängt wird:

```
well-kept intact interior, clean undamaged walls,
no peeling paint, no rubble, no decay, no abandonment
```

## Nachziehen

Die Prompts in `prompts.json` sind bereits korrigiert. Die betroffenen Motive stehen in
`state.json` als erledigt, deshalb ist **`--neu` nötig**, sonst werden sie übersprungen:

```bash
python3 kie_bilder.py motive --ref-url "<URL von REF_1 aus state.json>" --neu \
  --nur IMG_L2,IMG_L4,IMG_L7,IMG_L8,IMG_L9,IMG_HERO
python3 kie_bilder.py pack
python3 bilder_einsetzen.py
```

Sechs Bilder à 18 Credits = **108 Credits ≈ 0,47 $.**
