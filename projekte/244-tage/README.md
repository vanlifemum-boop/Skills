# 244 Tage — Instagram-Reel zur Inobhutnahme

Ein 33 Sekunden langes Hochformat-Video im Anime-Stil: ein Junge wird von zwei Frauen
abgeholt und darf nur mitnehmen, was er tragen kann — seinen Teddy und drei Bücher.
Danach das leere Zimmer, der Kalender, das Heim, und am Ende die Umarmung, auf die
seine Mutter wartet.

Erzeugt über **kie.ai** mit `veo3.1` (Variante `lite`, 1080p), Sprecherstimme über
`google/gemini-2-5-pro-tts`, zusammengeschnitten mit `ffmpeg`.

| Datei | Inhalt |
|---|---|
| `prompts.md` | die fünf englischen Video-Prompts und der Figurenblock |
| `voiceover.md` | Sprechtext und TTS-Aufruf |
| `texteinblendungen.md` | Einblendungen mit Zeiten, Bildunterschrift, Hashtags |
| `veo.py` | erzeugt Veo-Clips — der Endpunkt, den `kie.py` nicht bedient |
| `bauen.sh` | schneidet aus Clips und Stimme das fertige Reel |

Die Videodateien selbst liegen unter `~/Medien/JJJJ-MM-TT-244-tage/` und gehören
**nicht** ins Repo.

---

## In einem Rutsch

```bash
export KIE_API_KEY='…'

# 1. Die fünf Clips (Prompts stehen in prompts.md)
python3 projekte/244-tage/veo.py --projekt 244-tage --prompt "<Prompt aus prompts.md>"

# 2. Die Stimme
python3 projekte/244-tage/tts.py --projekt 244-tage

# 3. Der Schnitt
bash projekte/244-tage/bauen.sh
```

## Was Geld kostet

Geplant waren fünf Clips: **175 Credits · 0,75 €**. Tatsächlich gebraucht wurden **neun**
bezahlte Clips — **315 Credits · rund 1,35 €**. Wofür die vier zusätzlichen draufgingen:

| Nachlauf | Grund |
|---|---|
| Clip 2 | zeigte Teddy und Bücher im leeren Zimmer — er hat beides mitgenommen |
| Clip 3 | dasselbe: Teddy stand im Hintergrund des Kalenderbilds |
| Clip 5 | keine Umarmung, nur ein Gegenüberstehen — der Schluss trug nicht |
| Clip 5 | die Mutter war dunkelhaarig, sie ist blond |

Zwei weitere Versuche für Clip 3 brachen serverseitig mit „Internal Error" ab; dafür
sollte nichts berechnet worden sein. Die verworfenen Fassungen liegen unter
`~/Medien/…-244-tage/verworfen/`.

`veo3.1` kostet **je Clip gleich viel, egal ob 4, 6 oder 8 Sekunden**. Also immer 8 s
erzeugen und erst im Schnitt kürzen — das gibt gratis Spielraum beim Timing.

Ein misslungener Clip kostet 35 Credits. Deshalb: **Clip 1 zuerst allein** erzeugen und
ansehen, bevor 2–5 durchlaufen.

## Der Ton fehlt noch

Die Sprecherstimme wurde erzeugt, ließ sich aber nicht herunterladen: Sprachdateien
liegen bei kie.ai auf `file.aiquickdraw.com`, und dieser Host wird von der
Netzwerk-Richtlinie dieser Umgebung abgewiesen (`CONNECT tunnel failed, 403`).
Videos gehen durch, weil sie auf `tempfile.aiquickdraw.com` liegen.

Drei Wege:

1. `file.aiquickdraw.com` in die **Netzwerk-Allowlist der Umgebung** eintragen
   (nicht in `.claude/settings.json` — die steuert das nicht), dann `tts.py` erneut laufen
   lassen. Kostet 3,2 Credits.
2. Den Text **selbst einsprechen** und die Datei als `06.m4a` in den Medienordner legen.
   `bauen.sh` findet sie von allein. Das ist die stärkste Fassung.
3. Stumm lassen und in Instagram Musik darunterlegen — so liegt das Reel gerade vor.

---

## Zwei Dinge, über die man stolpert

**`veo3.1` läuft nicht über `/jobs/createTask`.**
`skills/media-skill/scripts/kie.py` schickt alles an den Market-Endpunkt. Veo hat bei
kie.ai einen eigenen — wie Suno. Ein Aufruf mit `--modell veo3.1` scheitert dort mit
`422: The model name you specified is not supported`. Dafür gibt es `veo.py`: es spricht
`POST /api/v1/veo/generate` und `GET /api/v1/veo/record-info` an, benutzt aber Download,
Dateibenennung und `meta.json` unverändert aus `kie.py` weiter. Die Slugs heißen dort
`veo3_lite`, `veo3_fast` und `veo3` — nicht `veo3.1`.

**Der Download braucht `curl`.**
Die Ergebnisse liegen auf `tempfile.aiquickdraw.com`, nicht unter `kie.ai`. Hinter dem
Agenten-Proxy antwortet dieser Host auf Pythons `urllib` mit HTTP 403, auf `curl` aber
mit 200. `veo.py` hängt sich deshalb in `kie._datei_holen` ein und lädt mit `curl`.
Wichtig, weil die Ergebnis-URLs **nach 24 Stunden verfallen** — wer nicht sofort lädt,
hat bezahlt und nichts.

---

## Die Leitplanken — nicht wegoptimieren

- **Kein echtes Gesicht, kein Foto.** Der Anime-Stil ist genau deshalb gewählt: er
  erzählt die Geschichte, ohne das Kind zu zeigen.
- **Die beiden Frauen bleiben gesichtslose Silhouetten** im Gegenlicht — ohne
  Dienstkleidung, ohne Logo, ohne Namen. Es geht um das Erleben der Mutter, nicht um
  eine Anklage gegen bestimmte Personen.
- **Keine Markenzeichen im Prompt.** Der Steiff-Bär ist ein „beiger Mohair-Teddy mit
  beweglichen Armen", die Bücher sind „abgegriffene Hardcover mit Messing-Kompass-Emblem".
  Das Bild bleibt trotzdem eindeutig ihres.
- **KI-Inhalt kennzeichnen** — Instagrams Schalter beim Hochladen, plus der Satz in der
  Bildunterschrift.

---

## Beim nächsten Mal — „300 Tage"

Das Paket ist bewusst so gebaut, dass sich nur die Zahl ändert:

1. In `texteinblendungen.md` und `bauen.sh` die `244` ersetzen.
2. `bauen.sh` neu laufen lassen — dieselben Clips, neue Zahl, **keine neuen Credits**.
3. Nur wenn ein neues Bild dazu soll, einen weiteren Clip erzeugen (35 Credits).

Die Clips altern nicht. Was altert, ist die Zahl.
