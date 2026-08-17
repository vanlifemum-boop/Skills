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

**Schrift im Bild: mal Kauderwelsch, mal erstaunlich sauber.**
Auf dem Beschluss in Bild 4 steht `OLG FRANKFURT` gestochen lesbar, weil es ausdrücklich
im Prompt stand. Verlassen kann man sich darauf nicht — aber ausprobieren lohnt, wenn ein
Wort im Bild etwas erzählt.

**Requisiten wandern zur falschen Person.**
In Bild 1 hielt der Vater plötzlich das Schutzschild in der Hand, das im Prompt der
Polizei gehörte. Ab Sekunde 4, davor sauber. Statt 35 Credits für einen neuen Versuch
endet der Clip jetzt nach 3,5 Sekunden. Bei einem Fehler, der erst spät im Clip auftaucht,
ist der Schnitt immer die erste Antwort, nicht die Neuerzeugung.

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
| Korrekturen an Bild 1 und 3 (Vater doppelt, zwei Jungen, Huckepack) | 210 |
| Dritter Durchlauf nach der genauen Ablauf-Schilderung: 5 Clips | 175 |
| **Summe** | **rund 780 Cr · gut 3 €** |

Mehr als Video 1 und 2 zusammen (315 und 228 Credits). Und fast alles davon war
vermeidbar — die Gründe stehen unten. Der wichtigste: **der genaue Ablauf lag erst nach
zwei kompletten Durchläufen auf dem Tisch.** Wer die Szenenfolge Satz für Satz vorher
aufschreibt, spart mehr Credits als jede Prompt-Feinheit.

Und eine Warnung zur Buchhaltung: `veo.py` rechnet mit 35 Credits je Clip, weil der
Veo-Endpunkt die tatsächlich abgerechneten Credits **nicht** zurückmeldet. Real war es
mehr. Wer den Stand wissen will, fragt `kie.py guthaben` — Schätzungen aus dem Skript
laufen sonst weit auseinander.

## Die Leitplanken — nicht wegoptimieren

- **Keine Behörde erkennbar.** Keine Aufschriften, Wappen, Abzeichen, Dienstgrade. Helme
  und Visiere, keine Gesichter. `no badges, no insignia` steht deshalb im Negativblock.
- **Keine Waffen, kein Blut.** `No weapons drawn, no blood` gehört in den Prompt für
  Bild 2. Ohne das kippt die Szene ins Actionhafte, und Instagram drosselt
  Gewaltdarstellungen.
- **Das Gericht darf benannt werden** — auf ihren ausdrücklichen Wunsch steht
  `OLG FRANKFURT` auf dem Beschluss in Bild 4. Ursprünglich war ein leeres Blatt geplant,
  weil erfundene Aktenzeichen wie Kauderwelsch aussehen und ein lesbares Dokument in
  einem laufenden Verfahren riskant sein kann. Sie hat das abgewogen und entschieden;
  es ist ihre Geschichte und ihr Verfahren.
- **Der Missbrauch im Heim kommt nicht ins Video** — weder als Bild noch als Einblendung.
  In der Bildunterschrift steht ein einziger zurückhaltender Satz, dessen zweite Hälfte
  die wichtigere ist: dass sie nicht mehr dazu schreibt.
- **Kein echtes Gesicht, kein Foto.**

## Beim nächsten Mal

Die Zahl steht in `texteinblendungen.md` und in `bauen.sh`. Ändern, `bauen.sh` neu laufen
lassen — dieselben Clips, neue Zahl, keine neuen Credits.
