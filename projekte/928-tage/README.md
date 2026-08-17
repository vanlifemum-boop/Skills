# 928 Tage — Instagram-Reel im amerikanischen Graphic-Novel-Stil

Ein 33 Sekunden langes Hochformat-Video: Morgens um sieben sitzt eine Familie am
Frühstückstisch, es klingelt. Ein Sondereinsatzkommando stürmt die Wohnung, der Vater
bekommt Handschellen, das Kind wird hinausgetragen. Der Mutter bleibt ein Beschluss in
der Hand. Seitdem 928 Tage — kein Anruf, kein Besuch.

Drittes Video der Reihe. `projekte/244-tage/` ist Anime, `projekte/1370-tage/`
europäische Graphic Novel — dieses hier ist harte amerikanische Tusche mit Schraffur.
Das ist kein Geschmack, sondern Inhalt: die ersten beiden erzählen stille Sehnsucht,
dieses erzählt einen Überfall.

| Datei | Inhalt |
|---|---|
| `prompts.md` | Stilblock, Negativblock, die fünf Prompts |
| `texteinblendungen.md` | Einblendungen mit Zeiten, Bildunterschrift, Hashtags |
| `bauen.sh` | schneidet aus den fünf Clips das Reel |

```bash
bash projekte/928-tage/bauen.sh ~/Medien/2026-08-17-928-final
```

Stumm, wie die beiden anderen — Musik kommt aus Instagrams Bibliothek.

## Zwei Dinge, die dieses Video gelehrt hat

**Der Sicherheitsfilter von Veo blockiert, was nach Kindesentführung aussieht.**
Der ursprüngliche Prompt für Bild 3 lautete „a helmeted figure carries the eight-year-old
boy out through the flat door". Antwort: `Request blocked: The input content was flagged
by safety filters as potentially dangerous`. Kein Serverfehler, sondern eine inhaltliche
Ablehnung — und sie kommt, bevor Credits fließen.

Die Lösung war nicht, die Aussage abzuschwächen, sondern die **Kamera umzustellen**: statt
eines Erwachsenen, der ein Kind wegträgt, der Blick über die Schulter der Mutter durch die
offene Wohnungstür, das Kind schon einige Stufen tiefer, zurückblickend. Dieselbe
Aussage, kein Griff eines Erwachsenen ans Kind im Bild — und deutlich stärker, weil der
Abstand zwischen beiden das eigentliche Thema ist.

Ein Zwischenversuch scheiterte anders: Mutter und Kind standen sich in der Tür gegenüber,
das las sich wie ein normaler Moment. Wer eine Szene entschärft, verliert sie. Wer sie
neu staffelt, behält sie.

**Alter und Statur gehören in den ersten Prompt, nicht in den fünften Clip.**
Die Mutter kam beim ersten Durchlauf als Frau um die fünfzig heraus („in her forties"
reicht dem Modell als Einladung, deutlich älter zu zeichnen), beim zweiten Versuch zu
schlank. Erst „a plus-size young mother in her early thirties, full-figured and
heavy-set, round full face" traf es. Das kostete fünf Clips à 35 Credits — beim nächsten
Video wird Statur und Alter am 6-Credit-Standbild geklärt, bevor irgendein Clip läuft.

**Zwei Figuren, wo eine stehen sollte.**
Bild 1 zeigte den Vater gleichzeitig sitzend am Tisch und stehend an der Tür — der Prompt
sagte „alle drei sitzen" **und** „der Vater steht auf". Das Modell malt in so einem Fall
beides. Der nächste Versuch setzte dann zwei Jungen an den Tisch. Erst eine ausdrückliche
Personenzählung hat es gelöst:

> `Exactly three people are in the scene and no one else: one mother seated, exactly one
> boy seated beside her, one father standing at the door. A single child only, no other
> children, no other adults.`

Wer eine Bewegung beschreibt („steht auf und geht zur Tür"), bekommt beide Zustände in
einem Bild. Besser den **Endzustand** beschreiben: „steht schon an der Tür, sein Stuhl ist
leer".

**Beschriftungen auf Uniformen lassen sich nicht wegverneinen.**
`no writing, no letters, no patches, no emblems, no badges, no insignia` stand am Ende
viermal im Prompt — auf den Westen stand trotzdem „Police". Bei Polizeimotiven ist das
offenbar so fest im Modell verankert, dass Negativangaben nicht greifen. Es blieb stehen,
weil englisches „Police" ohne Wappen keine bestimmte deutsche Behörde bezeichnet — genau
das war die Leitplanke, nicht das Wort an sich. Wo es stört: im Schnitt wegschneiden,
nicht neu erzeugen.

## Was gekostet wurde

| Posten | Credits |
|---|---|
| 3 Standbilder (Stilprobe, dann zwei Korrekturen an der Mutter) | 18 |
| Erster Durchlauf: 4 Clips (Bild 3 vom Filter blockiert, kostenfrei) | 140 |
| 2 Versuche für Bild 3 | 70 |
| Zweiter Durchlauf mit korrigierter Mutter: 5 Clips | 175 |
| **Summe** | **403 Cr · rund 1,73 €** |

Das teuerste der drei Videos, und der Grund steht oben: eine Figurbeschreibung, die erst
nach fünf fertigen Clips beanstandet wurde. Zum Vergleich: Video 1 kostete 315, Video 2
nur 228 Credits.

## Die Leitplanken — nicht wegoptimieren

- **Keine Behörde erkennbar.** Keine Aufschriften, Wappen, Abzeichen, Dienstgrade. Helme
  und Visiere, keine Gesichter. `no badges, no insignia` steht deshalb im Negativblock.
- **Keine Waffen, kein Blut.** `No weapons drawn, no blood` gehört in den Prompt für
  Bild 2. Ohne das kippt die Szene ins Actionhafte, und Instagram drosselt
  Gewaltdarstellungen.
- **Das Gericht wird im Video nicht benannt**, das Blatt in Bild 4 bleibt leer.
- **Der Missbrauch im Heim kommt nicht ins Video** — weder als Bild noch als Einblendung.
  In der Bildunterschrift steht ein einziger zurückhaltender Satz, dessen zweite Hälfte
  die wichtigere ist: dass sie nicht mehr dazu schreibt.
- **Kein echtes Gesicht, kein Foto.**

## Beim nächsten Mal

Die Zahl steht in `texteinblendungen.md` und in `bauen.sh`. Ändern, `bauen.sh` neu laufen
lassen — dieselben Clips, neue Zahl, keine neuen Credits.
