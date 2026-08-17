# Die Prompts

Alle Prompts **englisch**. Modell `veo3.1`, Variante `lite`, 1080p, 8 Sekunden, 9:16 —
35 Credits je Clip, längenunabhängig.

## Der Stilblock

```
American graphic novel style, bold black ink, heavy crosshatching, hard chiaroscuro
light, desaturated limited palette with one warm accent, halftone texture.
```

Gegenentwurf zu den ersten beiden Videos: dort weiche Aquarellflächen, hier harte Tusche
und Schraffur. Das passt zur Geschichte — sie ist keine stille Sehnsucht, sie ist ein
Überfall.

## Der Negativblock — am Ende jedes Prompts

```
No text, no captions, no lettering, no writing, no logos, no badges, no insignia,
no signage, no watermark.
```

`no badges, no insignia` steht hier zusätzlich und ist kein Schmuck: Einsatzkräfte ohne
Abzeichen sind der Unterschied zwischen einer erzählten Erfahrung und der Darstellung
einer bestimmten Behörde.

## Das Referenzbild

Zuerst ein Standbild von Bild 1 mit `gpt-image-2-text-to-image` in 2K (6 Credits), dann
dieses Bild über `--referenz` an alle fünf Clips. So bleiben Mutter, Vater und Kind über
alle Bilder dieselben Menschen. Die URL steht seit diesem Projekt in der Ausgabe von
`kie.py erzeugen` und in `meta.json` — sie lebt 24 Stunden.

```bash
python3 skills/media-skill/scripts/veo.py --projekt 928-tage \
  --referenz "https://tempfile.aiquickdraw.com/images/…png" --prompt "<STILBLOCK> … <NEGATIV>"
```

---

## Clip 1 — Der Frühstückstisch

```
<STILBLOCK> A small apartment kitchen at seven in the morning, grey light. The mother,
the father and their eight-year-old son sit at the breakfast table. A doorbell rings; all
three heads turn sharply towards the flat door, the father rises from his chair and walks
out of frame. Almost still camera. <NEGATIV>
```

## Clip 2 — Der Sturm

```
<STILBLOCK> The narrow hallway of the same flat. Helmeted figures in dark tactical gear
push in through the open door, the first one behind a riot shield, their faces completely
hidden behind visors. The father stands pressed against the wall, his hands held behind
his back. Behind them the mother and the boy sit frozen at the breakfast table. Harsh
backlight from the stairwell, dust in the air. No weapons drawn, no blood. <NEGATIV>
```

`No weapons drawn, no blood` gehört in den Prompt. Ohne das kippt die Szene ins
Actionhafte — und Instagram gibt Gewaltdarstellungen weniger Reichweite.

## Clip 3 — Das Kind wird hinausgetragen

```
<STILBLOCK> A helmeted figure in dark gear carries the eight-year-old boy out through the
flat door; the boy looks back over the shoulder, arm outstretched. The mother is half
risen from the table, reaching towards him, her mouth open. Cold stairwell light behind,
warm kitchen light in front. Slow motion, devastating. <NEGATIV>
```

Das ist das Bild, wegen dem das Video existiert. Es wird im Schnitt nicht beschnitten.

## Clip 4 — Die Wohnung danach

```
<STILBLOCK> The same kitchen minutes later, silent and empty. An overturned chair, the
untouched breakfast, a spilled mug. The mother stands alone in the middle of the room
holding a single completely blank sheet of paper, staring at nothing. Grey morning light,
deep black shadows. Very slow push-in. The sheet of paper is blank. <NEGATIV>
```

Das Blatt bleibt **leer**. Erfundene Aktenzeichen sehen aus wie Kauderwelsch, und ein
lesbares Dokument im Bild wäre in einem laufenden Verfahren das Letzte, was man will.
Das Gericht wird im Video nicht benannt.

## Clip 5 — Heute

```
<STILBLOCK> The same kitchen today, two years later. The mother stands alone at the window
looking out, two dogs sitting close beside her, one leaning against her leg. The chair
where the boy sat is empty. Grey daylight, one warm lamp. Quiet, worn down, still
standing. Almost still camera. <NEGATIV>
```

Der leere Stuhl und die beiden Hunde tragen das Bild. „Still standing" ist der Ton, der
gemeint ist — nicht gebrochen, sondern übrig geblieben und weitermachend.
