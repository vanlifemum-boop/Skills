# Modelle, Preise und die Fallen

Nachschlagewerk für `media-skill`. Die Zahlen hier stehen genauso in der Preistabelle
`PREISE` in `scripts/kie.py` — wer eine ändert, ändert beide.

**Preise nie aus dieser Datei ablesen und im Kopf rechnen.** Immer rechnen lassen:

```bash
python3 scripts/kie.py preis --modell MODELL [--aufloesung 2k] [--anzahl 6] [--sekunden 8]
```

---

## Umrechnung

200 Credits = 1 US-Dollar · **1 Credit ≈ 0,0043 €**

---

## Bild — Preis je Bild

| Modell | 1K | 2K | 4K | wofür |
|---|---|---|---|---|
| `gpt-image-2-text-to-image` | 6 | 10 | 16 | Text zu Bild, solide Allzweckwahl |
| `gpt-image-2-image-to-image` | 6 | 10 | 16 | braucht ein Eingangsbild |
| `nano-banana-2` | 8 | 12 | 18 | kräftigere Bildsprache |
| `google/nano-banana-pro` | 18 | 18 | 24 | die teure Spitze, für Titelbilder |
| `nano-banana-2-lite` | 4 | — | — | die billigste Variante, nur 1K |
| `google/nano-banana-edit` | 4 (fest) | | | gezieltes Nachbessern eines Bildes |
| `seedream-5-pro` | 7 | 14 | — | eigener Look, kein 4K |

## Video — Preis je Sekunde

| Modell | 480p | 720p | 1080p | wofür |
|---|---|---|---|---|
| `grok-imagine/image-to-video` | 2,4 | 4,5 | 8 | mit Abstand das günstigste Video |
| `bytedance/seedance-1.5-pro` | — | 3,5 | 7,5 | günstig und ruhig, **ohne Ton** |
| `kling-3-0` | — | 14 | 18 | starke Bewegung, gehobene Klasse |
| `bytedance/seedance-2` | — | 41 | 102 | cineastisch, sehr teuer — nur Schlüsselszenen |

Acht Sekunden 720p kosten also: grok 36 · seedance-1.5-pro 28 · kling-3-0 112 ·
seedance-2 328 Credits. Der Abstand zwischen billigster und teuerster Wahl ist Faktor 12 —
deshalb steht die Kostenfrage im Skill ganz vorn.

## Video — Preis je Clip

| Modell | Lite | Fast | Quality | Länge |
|---|---|---|---|---|
| `veo3.1` (1080p) | 35 | 65 | 255 | **nur 4, 6 oder 8 Sekunden** |

## Ton

| Modell | Preis | wofür |
|---|---|---|
| `google/gemini-2-5-pro-tts` | ~4 Credits je 40 s (0,1 je Sekunde) | sehr günstig, gute Sprachqualität |
| `elevenlabs-multilingual-v2` | 12 Credits je 1.000 Zeichen | viele Sprachen, Stimmauswahl |

---

## Die Fallen

**Ergebnis-URLs verfallen nach 24 Stunden.**
Deshalb lädt `kie.py erzeugen` sofort herunter und schreibt im selben Schritt `meta.json`
fort. Niemals eine kie.ai-URL „für später" notieren — sie ist morgen tot.

**Das Eingangsbild heißt bei jedem Modell anders — und ein falscher Name
kostet still Geld.** Wird das Feld nicht erkannt, ignoriert das Modell das Bild
kommentarlos, erzeugt irgendetwas aus dem Prompt und rechnet voll ab. Gemessen:

| Modell | Feld | Form |
|---|---|---|
| `bytedance/seedance-1.5-pro` | `input_urls` | Liste, 0–2 Bilder |
| `bytedance/seedance-2` | `input_urls` | Liste |
| `grok-imagine/image-to-video` | `image_urls` | Liste, bis 7 Bilder |
| `gpt-image-2-image-to-image` | `image_urls` | Liste |
| `google/nano-banana-edit` | `image_urls` | Liste |

`kie.py --bild DATEI` setzt das richtige Feld selbst (Tabelle `BILDFELD` im
Skript) und lädt die Datei vorher hoch. Wer `--extra` von Hand baut, muss den
Namen bei `docs.kie.ai/market/<hersteller>/<modell>` nachsehen.

**Videomodelle verstehen nur englische Prompts.**
Deutsche Prompts werden schlicht ignoriert, das Ergebnis hat dann nichts mit dem Auftrag zu
tun — und kostet trotzdem. Vor jedem Video-Auftrag den Prompt ins Englische übersetzen. Bei
Bild und Ton ist Deutsch in Ordnung.

**`duration` hat je Modell einen anderen Typ und andere Grenzen.**
Bei `grok-imagine` ein **Text** (`"6"`, erlaubt 6–30), bei `veo3.1` und den
seedance-Modellen eine **Zahl** — `veo3.1` nur 4, 6 oder 8, `seedance-1.5-pro`
4 bis 12. Ein unerlaubter Wert bringt „Value must be within the specified range".
`kie.py` setzt Typ und Grenzen richtig; wer `--extra` benutzt, muss selbst aufpassen.

**`aspect_ratio` ist bei seedance Pflicht.** Fehlt es, antwortet die API mit
„This field is required" — ohne zu sagen, welches Feld gemeint ist.

**`google/gemini-2-5-pro-tts` schneidet mehrere `dialogue_turns` ab.**
Es kommen nur die ersten rund neun Sekunden an, der Rest fehlt kommentarlos. Deshalb: **ein**
Text übergeben, Absätze durch Leerzeilen trennen. Keine `dialogue_turns`-Liste bauen.

**Suno läuft nicht über `/jobs/createTask`.**
Musik ist ein eigener Weg, den `kie.py` bewusst nicht abdeckt:

```
POST /api/v1/generate
  {"prompt": "...", "customMode": false, "instrumental": true,
   "model": "V5", "callBackUrl": "..."}
Status: GET /api/v1/generate/record-info?taskId=...
```

**HTTP 402 heißt: Guthaben leer.** Auf kie.ai aufladen. `kie.py guthaben` zeigt den Stand.

**Ein angenommener Auftrag kostet, auch wenn er nie fertig wird.** `createTask`
reserviert die Credits sofort. Ein Auftrag mit leerem `input` wurde angenommen,
blieb auf `waiting` stehen und hielt trotzdem 14,4 Credits fest. Also nie mit
halben Aufträgen herumprobieren — Schema vorher in der Doku nachlesen.

**Upload- und Ergebnis-Host stehen hinter Cloudflare.** Ohne Browser-User-Agent
antworten sie mit **403 (Fehlercode 1010)** — der `Python-urllib`-Standardkopf
reicht nicht. `kie.py` schickt deshalb bei Upload und Download einen
Browser-Kopf mit. Bricht ein Download trotzdem ab: `kie.py holen <taskId>
--projekt NAME` lädt das Ergebnis nach, statt es neu zu erzeugen.

**Preise ändern sich häufig.** Vor größeren Läufen auf **kie.ai/pricing** nachsehen und die
Tabelle hier sowie `PREISE` in `kie.py` angleichen, wenn etwas abweicht.

**Der ElevenLabs-Model-Slug ist noch unbestätigt.**
In der Preistabelle steht `elevenlabs-multilingual-v2`. Falls kie.ai den Auftrag mit
„unbekanntes Modell" ablehnt, den echten Slug auf kie.ai nachsehen und an beiden Stellen
korrigieren.

---

## Die API in drei Zügen

Basis `https://api.kie.ai/api/v1`, Header `Authorization: Bearer $KIE_API_KEY`.
Der Schlüssel kommt **immer** aus der Umgebungsvariable, nie aus einer Datei.

1. `POST /jobs/createTask` mit `{"model": "...", "input": {...}}` → `data.taskId`.
   Ist `code != 200`, ist es fehlgeschlagen.
2. `GET /jobs/recordInfo?taskId=...` **alle acht Sekunden** abfragen. `data.state` läuft über
   `waiting` → `queuing` → `generating` → `success` oder `fail`.
3. Bei `success` steckt das Ergebnis in `data.resultJson` — **das ist ein JSON-String**, den
   man erst parsen muss. Darin `resultUrls` als Liste. Die tatsächlich abgerechneten Credits
   stehen in `data.creditsConsumed` (nicht der geschätzte Preis!).

Bei **429, 500, 502, 503** bis zu fünfmal wiederholen, mit wachsender Pause.
Rate Limit: **20 Anfragen je 10 Sekunden**.
