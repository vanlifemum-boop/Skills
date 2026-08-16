# Die fünf Video-Prompts

Alle Prompts sind **englisch** — Videomodelle ignorieren deutsche Prompts, kosten aber
trotzdem (siehe `skills/media-skill/references/modelle.md`).

Modell: `veo3.1`, Variante `lite`, 1080p, 8 Sekunden, Seitenverhältnis 9:16.
Preis: **35 Credits je Clip, unabhängig von der Länge** — deshalb überall 8 s erzeugen
und erst im Schnitt kürzen.

---

## Der Figurenblock

Steht **wortgleich am Anfang jedes Prompts**. Das ist bei Text-zu-Video der einzige
verlässliche Hebel dafür, dass der Junge in allen fünf Clips gleich aussieht.

```
Anime style, soft cel shading, muted watercolor palette, gentle film grain.
A slender 10-year-old boy with chin-length blonde hair tied back in a small low
ponytail and large blue eyes, wearing simple everyday clothes. He carries a beige
mohair teddy bear with jointed arms and three well-worn hardcover fantasy books
with a brass compass emblem.
```

Der Steiff-Bär ist bewusst als „beiger Mohair-Teddy mit beweglichen Armen"
beschrieben, die Bücher als „abgegriffene Hardcover mit Messing-Kompass-Emblem" —
echte Marken und Buchcover gehören nicht in einen Prompt. Das Bild bleibt trotzdem
eindeutig ihres.

Jeder Prompt endet auf `No text, no captions, no subtitles, no logos, no watermark.`
Der Text kommt erst im Schnitt dazu — was das Modell selbst einblendet, ist meistens
verstümmeltes Kauderwelsch.

---

## Clip 1 — Der Moment

```
<FIGURENBLOCK> Grey rainy afternoon in a narrow apartment hallway. Seen from behind,
the boy clutches the teddy bear and the three books tightly against his chest. In the
open doorway ahead stand two adult women in long coats, dark faceless backlit
silhouettes. The boy turns his head halfway back over his shoulder. Slow static wide
shot, shallow depth of field, muted blues and greys, melancholic, rain on the window.
No text, no captions, no subtitles, no logos, no watermark.
```

## Clip 2 und 3 benutzen den Figurenblock NICHT

Das ist teuer gelernt: In Clip 2 stand zuerst der volle Figurenblock, mit dem Zusatz
„The boy is absent from this shot". Das Ergebnis zeigte den Teddy **und** die Bücher
auf dem Nachttisch — das Modell nimmt jedes Substantiv aus dem Prompt als Bildinhalt,
„absent" hin oder her. Genau das Gegenteil der Geschichte: er hat beides mitgenommen,
das Zimmer ist ohne sie leer. 35 Credits für den Fehlversuch.

Für Bilder ohne den Jungen steht deshalb nur der **Stilblock** am Anfang:

```
Anime style, soft cel shading, muted watercolor palette, gentle film grain.
```

Und was fehlen soll, wird ausdrücklich verneint — nicht bloß weggelassen.

## Clip 2 — Das leere Zimmer

```
<STILBLOCK> An empty child's bedroom in pale morning light. Completely empty of people.
No teddy bear anywhere, no stuffed animals, no books. An unmade bed with rumpled sheets,
an empty gap on the bookshelf where books are missing, a single small blue hair tie
alone on the bare nightstand, dust motes drifting in a sunbeam. Very slow push-in,
quiet, lonely, muted palette.
No text, no captions, no subtitles, no logos, no watermark.
```

## Clip 3 — Der Kalender

```
<STILBLOCK> Extreme close-up of a paper wall calendar, day after day crossed out in blue
ballpoint pen. A woman's hand enters the frame and slowly crosses out one more day, the
pen trembling slightly. Only her hand is visible, her face is never shown. No people
otherwise, no teddy bear, no books. Shallow depth of field, soft grey window light.
No text, no captions, no subtitles, no logos, no watermark.
```

## Clip 4 — Im Heim

```
<FIGURENBLOCK> A bare institutional bedroom at night: plain walls, a single narrow bed,
one warm lamp. Seen from behind, the boy sits on the wide windowsill looking out at
distant city lights; the beige teddy bear sits beside him and the three books are
stacked next to it. Cool blue night palette, very slow static shot, deeply quiet.
No text, no captions, no subtitles, no logos, no watermark.
```

## Clip 5 — Die Hoffnung

```
<FIGURENBLOCK> A door swings open and warm golden light floods a dim room. The boy runs
toward the light holding the teddy bear by one arm, hair ponytail flying. In the
foreground, seen from behind, the silhouette of a kneeling woman with open arms, her
face never visible. The moment just before the embrace. Backlit, dust glowing in the
light, slow motion, hopeful, tender.
No text, no captions, no subtitles, no logos, no watermark.
```

---

## Der Aufruf

```bash
python3 skills/media-skill/scripts/kie.py erzeugen \
  --modell veo3.1 --variante lite --aufloesung 1080p --sekunden 8 \
  --projekt 244-tage --extra '{"aspect_ratio":"9:16"}' \
  --prompt "…"
```

`--extra` ist der einzige Weg zum Seitenverhältnis: `kie.py` setzt von sich aus nur
`resolution` und `duration` — bei `veo3.1` als **Zahl**, erlaubt sind ausschließlich
4, 6 und 8.

**Reihenfolge:** erst Clip 1 allein erzeugen und ansehen. Sitzen Anime-Look und Figur,
laufen 2–5 durch. Das spart Fehlläufe à 35 Credits.
