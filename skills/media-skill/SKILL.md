---
name: media-skill
description: >
  Erzeugt Bilder, Videos und Sprachaufnahmen über die kie.ai-API — mit ausgerechnetem
  Kostenvoranschlag vor jedem Lauf, sofortigem Download nach ~/Medien/ und einer lokalen
  Mediengalerie. Nutzen bei: "Bild erzeugen", "Bild generieren", "Video erzeugen",
  "Voiceover", "Sprachaufnahme", "kie.ai", "GPT Image", "nano banana", "seedream",
  "veo", "seedance", "kling", "Mediengalerie", "was hab ich bisher verbraucht".
---

# /media-skill — Bilder, Videos und Sprache über kie.ai

## Voraussetzung

`KIE_API_KEY` muss als Umgebungsvariable gesetzt sein:

```bash
export KIE_API_KEY='...'      # dauerhaft in ~/.zshrc bzw. ~/.bashrc
```

Der Schlüssel kommt **immer** aus der Umgebung — nie aus einer Datei, nie in einer Ausgabe,
nie in einen Commit. Fehlt er, sag das und hör auf; rate nicht herum.

## Freigegebene Domains

Läuft Claude Code in einer Sandbox oder hinter einer Netzwerk-Allowlist, müssen diese Hosts
erreichbar sein — sonst scheitert jeder Aufruf, bevor er anfängt:

| Domain       | wofür                                        |
|--------------|----------------------------------------------|
| `api.kie.ai` | alle API-Aufrufe (`/jobs/createTask`, Status, Guthaben) |
| `kie.ai`     | Preisliste und Modell-Slugs nachsehen        |
| `*.kie.ai`   | weitere Subdomains derselben Plattform       |

Im Projekt sind sie in `.claude/settings.json` eingetragen — unter `permissions.allow` als
`WebFetch(domain:…)` und unter `sandbox.network.allowedDomains`. Für die Umgebung von
Claude Code on the web gehören dieselben drei Einträge zusätzlich in die Netzwerk-Allowlist
der Umgebung; `.claude/settings.json` konfiguriert diese nicht mit.

Die **Ergebnis-URLs** liefert kie.ai auf eigenen CDN-Hosts aus, die nicht immer unter
`kie.ai` liegen. Bricht der Download mit einem Netzwerkfehler ab, obwohl der Auftrag
fertig ist: den Host aus der Fehlermeldung ablesen und ebenfalls freigeben.

---

## Alles hängt an einer Frage: Hat der Nutzer ein Modell genannt?

### Fall A — kein Modell genannt

1. **Erst überlegen**, was der Auftrag wirklich braucht: Bild oder Video oder Ton? Welche
   Auflösung reicht? Wie viele Stücke? Wie lang?
2. **Höchstens DREI Kandidaten** als kompakte Tabelle zeigen. Die Kosten gelten **für genau
   diesen Auftrag** — sechs Bilder heißt mal sechs, nicht der Stückpreis. Je ein Halbsatz
   dafür und dagegen, mehr nicht.
3. **Eine klare Empfehlung aussprechen.** Nicht die Wahl zurückgeben, nicht „kommt drauf an".
4. **Anhalten und auf ein Ja warten.** Nichts erzeugen, bevor bestätigt ist.

```
| Modell                    | 6 Bilder à 2K | dafür                  | dagegen              |
|---------------------------|---------------|------------------------|----------------------|
| nano-banana-2-lite        |  24 Cr · 0,103 € | mit Abstand billigst | nur 1K               |
| gpt-image-2-text-to-image |  60 Cr · 0,258 € | verlässliche Qualität | nichts Auffälliges   |
| google/nano-banana-pro    | 108 Cr · 0,464 € | schönste Ergebnisse  | vierfacher Preis     |

Empfehlung: gpt-image-2-text-to-image in 2K — 60 Credits, 0,258 €. Loslegen?
```

### Fall B — Modell genannt

Keine Beratung. Keine Alternativen. Keine Belehrung. **Eine Zeile:**

```
GPT Image 2, 2K, ein Bild: 10 Credits · 0,043 €. Loslegen?
```

Nur wenn das gewünschte Modell den Auftrag **technisch nicht erfüllen kann**, ein Halbsatz
Hinweis — etwa „seedream kann kein 4K, 2K ist das Maximum". Sonst nichts.

### Nachbesserung innerhalb eines schon bestätigten Auftrags

Gar nicht mehr fragen. Nur die Kosten nennen und machen.

```
Nachlauf mit geändertem Prompt: 10 Credits · 0,043 €.
```

---

## Preise ausrechnen, nie schätzen

Der Preisrechner arbeitet **ohne API-Aufruf** und ist die einzige zulässige Quelle für Zahlen
gegenüber dem Nutzer:

```bash
python3 scripts/kie.py preis --modell gpt-image-2-text-to-image --aufloesung 2k --anzahl 6
python3 scripts/kie.py preis --modell veo3.1 --variante quality --sekunden 8
python3 scripts/kie.py preis --modell elevenlabs-multilingual-v2 --zeichen 2500
```

Nie eine Zahl aus dem Kopf oder aus `references/modelle.md` abschreiben — immer rechnen lassen.

---

## Der Ablauf

| Schritt | Befehl |
|---|---|
| Guthaben prüfen | `python3 scripts/kie.py guthaben` |
| Bild hochladen | `python3 scripts/kie.py hochladen BILD.png` |
| Preistabelle ansehen | `python3 scripts/kie.py modelle` |
| Kosten ausrechnen | `python3 scripts/kie.py preis --modell M …` |
| Erzeugen + laden + protokollieren | `python3 scripts/kie.py erzeugen --modell M --prompt "…" --projekt name` |
| Galerie bauen | `python3 scripts/galerie.py` |

`erzeugen` macht den kompletten Dreisprung selbst: Auftrag anlegen → alle acht Sekunden nach dem
Status fragen → Ergebnisse **sofort** herunterladen. Sofort, weil die Ergebnis-URLs von kie.ai
**nach 24 Stunden verfallen**.

**Ablage:** `~/Medien/JJJJ-MM-TT-projektname/`

**Protokoll:** Im selben Schritt wie der Download wird `meta.json` im Zielordner
fortgeschrieben — **angehängt, nie überschrieben** — mit Zeitstempel, Dateiname, Typ, Modell,
Prompt, den **tatsächlich abgerechneten** Credits (`creditsConsumed`, nicht der Schätzung) und
dem Euro-Betrag. Das gehört bewusst in den Download-Schritt, damit es nicht vergessen werden
kann.

### Beispiele

```bash
# Ein Bild
python3 scripts/kie.py erzeugen \
  --modell gpt-image-2-text-to-image --aufloesung 2k \
  --prompt "Ein Keramikbecher auf hellem Leinen, weiches Seitenlicht" \
  --projekt produktfotos

# Ein Video — Prompt auf ENGLISCH, sonst wird er ignoriert
python3 scripts/kie.py erzeugen \
  --modell grok-imagine/image-to-video --aufloesung 720p --sekunden 8 \
  --prompt "Slow push-in on the mug, warm morning light" \
  --projekt werbeclip --extra '{"image_url": "https://…"}'

# Sprache — EIN Text, Absätze durch Leerzeilen
python3 scripts/kie.py erzeugen \
  --modell google/gemini-2-5-pro-tts --sekunden 40 \
  --prompt "Handgemacht. Und das schmeckt man." --projekt werbeclip
```

---

## Reels aus Standbildern

Soll aus fertigen Bildern eine Reihe kurzer Hochformat-Videos werden, steht der ganze
Ablauf in `templates/instagram-reel-vorlage.md`: Aufbau eines Reels, Prompt-Baukasten auf
Englisch, Einblendungs-Regeln und die Checkliste vor dem Posten. Die ausgefüllten Blätter
der Serie „Tatort Fake Mami" liegen daneben in `templates/reels/`.

Zwei Werkzeuge gehören dazu, beide **kostenlos**:

```bash
python3 scripts/schwaerzen.py QUELLE.png ZIEL-anonym.png --kasten 95,98,172,180
python3 scripts/kie.py hochladen BILD.png --ordner images/projekt
python3 scripts/schwenk.py BILD.png ZIEL.mp4 --sekunden 8
python3 scripts/einfrieren.py CLIP.mp4 ORIGINAL.png ZIEL.mp4 --bereich 120,2,610,100
python3 scripts/zusammensetzen.py reel.mp4 clip1.mp4 clip2.mp4 clip3.mp4
```

Nur `hochladen` spricht mit kie.ai — alles andere läuft lokal und **kostet nichts**:

- `schwaerzen.py` deckt Gesichter, Namen und Nummern ab und lässt die Quelldatei
  unverändert; das Original bleibt Beweismittel.
- `hochladen` liefert die öffentliche URL, die Image-to-Video für `input_urls` braucht.
  Der Upload-Host ist ein anderer als die API und verlangt eine Browser-Kennung —
  das erledigt `kie.py` selbst.
- `schwenk.py` macht aus einem Standbild einen ruhigen 9:16-Clip. **Für Belege der
  einzige vertretbare Weg:** ein Video-Modell kann Zeichen umschreiben und macht aus
  einem Beweis eine Fälschung, ein Schwenk kann das nicht.
- `einfrieren.py` holt Bildbereiche aus dem Original als feste Ebene in den Clip zurück.
  Feine Schrift überlebt kein Video-Modell — nach zwei Sekunden steht dort ein anderes
  Wort. Der Kasten muss großzügig sein, sonst lugt die Modellfassung darunter hervor.
- `zusammensetzen.py` hängt die Clips zum fertigen Reel aneinander.

`schwenk.py`, `einfrieren.py` und `zusammensetzen.py` brauchen ffmpeg. Fehlt es im
System, genügt `pip install imageio-ffmpeg` — die Skripte finden das mitgelieferte
Binary von allein.

## Die Galerie

```bash
python3 scripts/galerie.py                  # baut ~/Medien/galerie.html und öffnet sie
python3 scripts/galerie.py --nooeffnen      # nur bauen
```

Liest alle `meta.json` ein und baut eine einzelne HTML-Datei ohne Server: Raster mit Vorschau,
Filter nach Typ, Auswahlliste der Modelle, Suchfeld über Prompt, Modell und Projekt — und ganz
oben die **Gesamtsumme** aus Anzahl, Credits und Euro. Neueste zuerst. Video-Vorschaubilder
zieht sie einmalig per ffmpeg und legt sie als `<datei>.thumb.jpg` daneben, damit der zweite
Aufbau schnell ist.

---

## Bevor du irgendetwas erzeugst

Lies `references/modelle.md`. Dort stehen die vollständigen Preistabellen und die Fallen, die
Geld kosten, wenn man sie nicht kennt — vor allem:

- Ergebnis-URLs verfallen nach **24 Stunden**.
- Videomodelle verstehen **nur englische Prompts**; deutsche werden ignoriert und kosten
  trotzdem.
- `duration` ist bei `grok-imagine` ein **Text**, bei `veo3.1` eine **Zahl** (nur 4, 6 oder 8).
- `google/gemini-2-5-pro-tts` schneidet mehrere `dialogue_turns` ab — **ein** Text, Absätze
  durch Leerzeilen.
- **Suno** für Musik läuft über einen ganz anderen Endpunkt, nicht über `/jobs/createTask`.
- **HTTP 402** heißt: Guthaben leer.
- Preise ändern sich häufig — vor größeren Läufen auf `kie.ai/pricing` schauen.
