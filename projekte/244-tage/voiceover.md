# Voiceover

Modell: `google/gemini-2-5-pro-tts`, ca. 32 Sekunden → **3,2 Credits · 0,014 €**.
Bei Sprache ist Deutsch als Prompt in Ordnung — anders als bei Video.

## Der Sprechtext

> Vor 244 Tagen holten zwei Frauen mein Kind.
> Er durfte mitnehmen, was er tragen konnte: seinen Teddy und drei Bücher.
>
> Seitdem zähle ich.
> 244 Tage, in denen ein Platz in meinem Leben leer geblieben ist.
> Mein Kind wächst weiter — und ich verpasse Momente, die ich niemals zurückbekomme.
>
> Ich will keine Tage mehr zählen.
> Ich will einfach nur wieder Mama sein.
> 244 Tage sind genug.

## Der Aufruf

```bash
python3 skills/media-skill/scripts/kie.py erzeugen \
  --modell google/gemini-2-5-pro-tts --sekunden 32 --projekt 244-tage \
  --prompt "Vor 244 Tagen holten zwei Frauen mein Kind. Er durfte mitnehmen, was er tragen konnte: seinen Teddy und drei Bücher.

Seitdem zähle ich. 244 Tage, in denen ein Platz in meinem Leben leer geblieben ist. Mein Kind wächst weiter — und ich verpasse Momente, die ich niemals zurückbekomme.

Ich will keine Tage mehr zählen. Ich will einfach nur wieder Mama sein. 244 Tage sind genug."
```

**Die Falle:** ein einziger Text, Absätze durch Leerzeilen. Wer eine
`dialogue_turns`-Liste baut, bekommt kommentarlos nur die ersten rund neun Sekunden
zurück — bezahlt aber alles (`skills/media-skill/references/modelle.md`).

## Besser als jede KI-Stimme

Sprich den Text mit dem Handy selbst ein und schick die Datei. Eine echte Mutterstimme,
die an der richtigen Stelle stockt, trägt dieses Video weiter als jede saubere
Synthesestimme — und der Austausch kostet nichts, die Clips bleiben wie sie sind.
