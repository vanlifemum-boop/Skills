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
python3 skills/media-skill/scripts/tts.py --projekt 244-tage
python3 skills/media-skill/scripts/tts.py --projekt 244-tage --stimme Achernar   # weichere Stimme
```

**Nicht** `kie.py erzeugen --modell google/gemini-2-5-pro-tts`: das schickt `prompt`,
und das Modell will etwas anderes. Man läuft in drei 422er nacheinander, bis klar wird,
wie die Eingabe wirklich aussehen muss:

```json
{"language": "de-DE",
 "speakers": [{"speaker_id": "Speaker 1", "voice_name": "Sulafat"}],
 "dialogue_turns": [{"speaker_id": "Speaker 1", "text": "…"}]}
```

`speaker_id` muss wörtlich **„Speaker N"** heißen — „Erzählerin" wird abgelehnt. Und es
bleibt bei **einem einzigen** Turn: mehrere schneidet das Modell nach rund neun Sekunden
kommentarlos ab und berechnet trotzdem alles.

## Der Ton fehlt im fertigen Reel noch

Die Datei wurde erzeugt, ließ sich hier aber nicht laden: Sprachdateien liegen auf
`file.aiquickdraw.com`, und dieser Host wird von der Netzwerk-Richtlinie der Umgebung
abgewiesen (`CONNECT tunnel failed, 403`) — Videos gehen durch, weil sie auf
`tempfile.aiquickdraw.com` liegen. Entweder den Host in der **Allowlist der Umgebung**
freigeben (nicht in `.claude/settings.json`, die steuert das nicht) und `tts.py` erneut
laufen lassen, oder den Text selbst einsprechen.

## Besser als jede KI-Stimme

Sprich den Text mit dem Handy selbst ein und schick die Datei. Eine echte Mutterstimme,
die an der richtigen Stelle stockt, trägt dieses Video weiter als jede saubere
Synthesestimme — und der Austausch kostet nichts, die Clips bleiben wie sie sind.
