# Die Prompts

Alle Prompts **englisch** — Videomodelle ignorieren deutsche und kosten trotzdem.

Modell: `veo3.1`, Variante `lite`, 1080p, 8 Sekunden, 9:16.
Preis: **35 Credits je Clip, längenunabhängig** — also 8 s erzeugen und im Schnitt kürzen.

---

## Der Stilblock

Steht wortgleich am Anfang jedes Prompts:

```
European graphic novel style, clean ink linework over muted watercolour, realistic
faces, cinematic light, subtle paper grain.
```

Und jeder Prompt endet auf:

```
No text, no captions, no lettering, no logos, no signage, no watermark.
```

## Referenzbilder statt Figurenbeschreibung

Im ersten Video (`projekte/244-tage/`) musste ein wortgleicher Figurenblock die
Gleichheit über fünf Clips tragen — drei Clips mussten trotzdem nachlaufen. Hier geht es
anders: **ein Standbild wird zuerst erzeugt und dann als Referenz an die Clips
weitergereicht.**

```bash
python3 skills/media-skill/scripts/kie.py erzeugen \
  --modell gpt-image-2-text-to-image --aufloesung 2k --projekt 1370-tage \
  --extra '{"aspect_ratio":"9:16"}' --prompt "<Stilblock> …"

python3 skills/media-skill/scripts/veo.py --projekt 1370-tage \
  --referenz "https://tempfile.aiquickdraw.com/images/…png" --prompt "<Stilblock> …"
```

Ein Bild kostet **6 Credits**, ein Videoversuch **35**. Wer den Stil erst am Bild prüft
und dann als Referenz weitergibt, spart die Fehlläufe — und die Gesichter bleiben gleich.

Zwei Fallen dabei:

- Die Bild-URL ist **24 Stunden** gültig. Danach ist die Referenz tot.
- `kie.py` gibt die URL nicht aus, sondern lädt nur herunter. Wer sie als Referenz
  braucht, muss sie sich beim Lauf notieren oder über
  `GET /jobs/recordInfo?taskId=…` → `resultJson.resultUrls` nachholen — dafür braucht
  man aber die taskId aus der Ausgabe.

**Wo keine Personen vorkommen, kommt auch keine Referenz dazu.** Das Elternbild als
Referenz an ein „leeres Zimmer" zu hängen holt die Eltern ins Bild — dieselbe Falle wie
der Teddy im ersten Video. Für Clip 2 und 3 reicht der Stilblock allein; das ist an zwei
Standbildern vorher geprüft worden.

---

## Clip 1 — Das Krankenhaus (mit Referenz)

```
<STILBLOCK> A dim hospital room at night, one warm bedside lamp. The mother with dark
brown hair and blue eyes holds her four-week-old newborn against her chest; the father
leans in beside her, his hand on the baby's blanket. She strokes the baby's head, both
parents breathe slowly, exhausted and worried. Almost still camera, the faintest slow
push-in. <NEGATIV>
```

## Clip 2 — Das Zimmer danach (ohne Referenz)

```
<STILBLOCK> A dim hospital room at night, one warm bedside lamp still on. An empty
hospital bassinet with a crumpled white sheet, a closed grey folder on the side table,
an unmade bed. In the doorway a single faceless adult silhouette stands backlit from the
corridor, then turns and walks away. Slow push-in, cold and quiet. <NEGATIV>
```

## Clip 3 — Das nie benutzte Kinderzimmer (ohne Referenz)

```
<STILBLOCK> An empty child's bedroom in grey daylight, never used: a small bed made up
perfectly and untouched, an empty toy shelf, rain running down the window, dust drifting
in the air. Completely empty of people. Very slow push-in, lonely and still. <NEGATIV>
```

## Clip 4 — Das Sorgerecht (mit Referenz)

```
<STILBLOCK> Close-up of the mother's hands holding a single blank official sheet of
paper, her fingers trembling slightly. Behind her, out of focus, a closed apartment door.
Her face is not in frame, only her hands and the paper. Soft grey daylight, shallow depth
of field, almost still camera. The paper is completely blank. <NEGATIV>
```

Das Blatt bleibt **leer**. Erfundene Aktenzeichen sehen aus wie Kauderwelsch, und ein
lesbares Dokument im Bild wäre in einem laufenden Verfahren das Letzte, was man will.

## Clip 5 — Das Kind will nach Hause (mit Referenz)

```
<STILBLOCK> A small boy of almost four with light brown hair and blue eyes stretches both
arms forward, desperate to run; a faceless adult silhouette holds him back by the wrist.
A few steps ahead of him the mother kneels with open arms, the father standing behind
her, both reaching towards the boy. An empty gap of floor between them. Backlit doorway,
warm light against cold grey, slow motion, unbearable longing. <NEGATIV>
```

Der Abstand zwischen Kind und Eltern ist das ganze Bild. Er darf nicht verschwinden —
wer daraus eine Umarmung macht, erzählt das Gegenteil dessen, was gerade wahr ist.
