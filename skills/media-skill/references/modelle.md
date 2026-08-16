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

`veo3.1` hat einen **eigenen Endpunkt** und läuft nicht über `kie.py erzeugen` —
siehe die Falle weiter unten. Der Preis gilt **je Clip, unabhängig von der Länge**:
vier Sekunden kosten so viel wie acht. Also acht erzeugen und im Schnitt kürzen.

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

**Videomodelle verstehen nur englische Prompts.**
Deutsche Prompts werden schlicht ignoriert, das Ergebnis hat dann nichts mit dem Auftrag zu
tun — und kostet trotzdem. Vor jedem Video-Auftrag den Prompt ins Englische übersetzen. Bei
Bild und Ton ist Deutsch in Ordnung.

**`duration` hat je Modell einen anderen Typ.**
Bei `grok-imagine` ist es ein **Text** (`"8"`), bei `veo3.1` eine **Zahl** (`8`) — und dort
sind nur 4, 6 oder 8 erlaubt. `kie.py` setzt das richtig; wer `--extra` benutzt, muss selbst
aufpassen.

**`google/gemini-2-5-pro-tts` nimmt kein `prompt`.**
`kie.py erzeugen` schickt `prompt` und läuft damit in eine Kette von 422ern
(„speakers …", dann „speaker_id …", dann „voice_name …"). Die Eingabe muss so aussehen:

```json
{"language": "de-DE",
 "speakers": [{"speaker_id": "Speaker 1", "voice_name": "Sulafat"}],
 "dialogue_turns": [{"speaker_id": "Speaker 1", "text": "…"}]}
```

`speaker_id` muss wörtlich **„Speaker N"** heißen — ein sprechender Name wie
„Erzählerin" wird abgelehnt. Fertiger Aufrufer: `projekte/244-tage/tts.py`.

**Und genau EIN `dialogue_turn`.**
Mehrere Turns schneidet das Modell nach rund neun Sekunden kommentarlos ab, der Rest
fehlt und ist trotzdem bezahlt. Also den ganzen Text in einen einzigen Turn, Absätze
durch Leerzeilen.

**Ton und Video kommen von verschiedenen Hosts.**
Videos liegen auf `tempfile.aiquickdraw.com`, Sprachdateien auf `file.aiquickdraw.com`.
Wer nur den ersten freigeschaltet hat, bekommt beim Ton `CONNECT tunnel failed, 403`.
Beide Hosts gehören in die Netzwerk-Allowlist der Umgebung — in
`.claude/settings.json` einzutragen reicht dafür **nicht**.

**Veo 3.1 läuft nicht über `/jobs/createTask`.**
Wie Suno hat Veo bei kie.ai einen eigenen Endpunkt. `kie.py erzeugen --modell veo3.1`
scheitert deshalb mit `422: The model name you specified is not supported` — bevor
Credits fließen, immerhin. Die Slugs heißen dort anders: `veo3_lite`, `veo3_fast`,
`veo3` (Quality). Ein einsatzfertiger Aufrufer liegt in `projekte/244-tage/veo.py`;
er benutzt Download, Dateinamen und `meta.json` unverändert aus `kie.py` weiter.

```
POST /api/v1/veo/generate
  {"prompt": "...", "model": "veo3_lite", "aspect_ratio": "9:16",
   "duration": 8, "resolution": "1080p", "generationType": "TEXT_2_VIDEO"}
Status: GET /api/v1/veo/record-info?taskId=...
  successFlag 0 = läuft, 1 = fertig; die URLs stehen in response.resultUrls
```

**Der Download braucht unter Umständen `curl`.**
Die Ergebnisse liegen auf `tempfile.aiquickdraw.com`, nicht unter `kie.ai`. Hinter
einem Agenten-Proxy antwortet dieser Host auf Pythons `urllib` mit **HTTP 403**, auf
`curl` dagegen mit 200. Wer das trifft, hängt sich in `kie._datei_holen` ein und lädt
mit `curl` — so macht es `projekte/244-tage/veo.py`. Wichtig, weil die URLs nach
24 Stunden verfallen: sonst ist der Auftrag bezahlt und die Datei weg.

**Suno läuft nicht über `/jobs/createTask`.**
Musik ist ein eigener Weg, den `kie.py` bewusst nicht abdeckt:

```
POST /api/v1/generate
  {"prompt": "...", "customMode": false, "instrumental": true,
   "model": "V5", "callBackUrl": "..."}
Status: GET /api/v1/generate/record-info?taskId=...
```

**HTTP 402 heißt: Guthaben leer.** Auf kie.ai aufladen. `kie.py guthaben` zeigt den Stand.

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
