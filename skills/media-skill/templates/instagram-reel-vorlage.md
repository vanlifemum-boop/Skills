# Instagram-Reel aus einem Standbild — die Vorlage

Wie aus einem fertigen Cover oder einem Beleg-Screenshot ein 9:16-Reel wird.
Gebaut für die Serie „Tatort Fake Mami", brauchbar für jede Reihe, die aus Standbildern
plus Text-Einblendungen besteht.

**Grundsatz: kein Auftrag ohne ausdrückliche Freigabe.** Jeder Clip kostet Geld. Erst
rechnen, dann fragen, dann erzeugen — in dieser Reihenfolge.

---

## Der Aufbau eines Reels

Drei Clips à 8 Sekunden ergeben 24 Sekunden. Das ist die Standardlänge.

| Clip | Zeit | Was drin ist | Bewegung |
|---|---|---|---|
| A — Hook | 0–8 s | das Cover mit der Schlagzeile | ganz langsamer Push-in, sonst nichts |
| B — Beleg | 8–16 s | der Screenshot, auf den es ankommt | leichter Vertikal-Drift, Tiefenparallaxe |
| C — Abbinder | 16–24 s | Kernsatz und Kanal-Logo | Zoom-out, Ruhe, Standbild am Ende |

Braucht ein Reel mehr Beleg, wird B verdoppelt: dann sind es vier Clips und 32 Sekunden.

**Die Reihenfolge ist nicht verhandelbar.** Der Hook trägt die ersten drei Sekunden, in
denen entschieden wird, ob jemand weiterschaut. Der Beleg kommt danach, nie zuerst.

---

## Modell und Kosten

| | |
|---|---|
| Modell | `bytedance/seedance-1.5-pro` |
| Auflösung | 720p |
| Länge | 8 Sekunden je Clip |
| Preis | **28 Credits · 0,120 € je Clip** |

Nie aus dem Kopf rechnen, immer rechnen lassen:

```bash
python3 scripts/kie.py preis --modell bytedance/seedance-1.5-pro --aufloesung 720p --sekunden 8
```

`seedance-1.5-pro` liefert **keinen Ton**. Das ist hier gewollt: Die Reels laufen stumm,
die Aussage tragen die Text-Einblendungen.

---

## Der Ablauf, Schritt für Schritt

```bash
cd skills/media-skill

# 1. Guthaben prüfen — kostet nichts
python3 scripts/kie.py guthaben

# 2. Falls nötig: Gesichter, Namen, Nummern abdecken — kostet nichts
python3 scripts/schwaerzen.py QUELLE.png ZIEL-anonym.png --kasten 95,98,172,180

# 3. Bild hochladen — kostet nichts, liefert die öffentliche URL
python3 scripts/kie.py hochladen ~/Medien/tatort-fake-mami-quellen/BILD.png --ordner images/tatort

# 4. Kosten ansagen, Freigabe abwarten

# 5. Clip erzeugen — DAS kostet
python3 scripts/kie.py erzeugen \
  --modell bytedance/seedance-1.5-pro --aufloesung 720p --sekunden 8 \
  --prompt "ENGLISCHER PROMPT" \
  --projekt tatort-fake-mami \
  --extra '{"image_url": "https://…"}'

# 6. Galerie mit Gesamtsumme bauen
python3 scripts/galerie.py --nooeffnen
```

Schritt 5 lädt sofort herunter und schreibt `meta.json` mit den **tatsächlich**
abgerechneten Credits fort. Ergebnis-URLs von kie.ai verfallen nach 24 Stunden — deshalb
nie „für später" notieren.

---

## Der Prompt-Baukasten

**Prompts sind auf Englisch.** Videomodelle ignorieren deutsche Prompts stillschweigend,
das Ergebnis hat dann nichts mit dem Auftrag zu tun — und kostet trotzdem.

Ein Prompt besteht aus vier Teilen, immer in dieser Reihenfolge:

```
[1 Bewegung]  [2 Stimmung]  [3 Look]  [4 Sperrklausel]
```

### 1 — Bewegung, je nach Clip-Rolle

| Rolle | Baustein |
|---|---|
| Hook | `Extremely slow push-in on the centre of the frame, barely perceptible.` |
| Beleg | `Very slow vertical drift downward with subtle depth parallax between layers.` |
| Abbinder | `Slow pull-back, the frame settles and comes to a complete rest.` |

### 2 — Stimmung, immer gleich

```
Serious, calm, documentary tone. No fast motion, no shake, no whip pans, no flicker.
```

### 3 — Look, immer gleich

```
Dark navy background, red and cyan accent glow, cinematic grade, 9:16 vertical.
```

### 4 — Die Sperrklausel, **Pflicht in jedem Prompt**

```
Do not add, alter, remove or invent any text, letters, numbers, logos or faces.
Keep all existing lettering perfectly sharp, legible and unchanged.
```

Ohne diesen Satz erfindet das Modell Buchstaben in Dokumenten und Chatblasen. Bei einem
Beleg-Clip macht das aus einem Beweis eine Fälschung — der teuerste Fehler, den diese
Reihe machen kann. Nach jedem Beleg-Clip wird deshalb Bild für Bild kontrolliert.

---

## Text-Einblendungen

Ohne Stimme tragen die Einblendungen alles. Sie entstehen im Schnittprogramm
(CapCut, InShot), nicht im Video-Modell — Modelle schreiben keinen verlässlichen Text.

- **Lesetempo:** 6–10 Wörter je Einblendung, mindestens 2,5 Sekunden Standzeit.
- **Sichere Zone:** unteres Fünftel freilassen — dort liegen Caption, Profilname und
  Buttons. Oberes Zehntel ebenfalls, wegen der Statusleiste.
- **Größe:** Schlagzeile groß genug, um bei Daumenbreite lesbar zu sein. Im Zweifel größer.
- **Farbe:** Weiß auf dunklem Grund, Rot nur für die Warnzeile, Cyan nur für den Schutz-
  gedanken. Drei Farben, mehr nicht — so bleibt die Reihe wiedererkennbar.
- **Untertitel-Automatik greift nicht**, weil kein Ton vorhanden ist. Alles muss gesetzt
  werden.

---

## Vor dem Posten — die Checkliste

Aus den Veröffentlichungsregeln der Reihe:

- [ ] Nur geschwärzte Kopien veröffentlichen; Originale getrennt und unverändert aufbewahrt.
- [ ] Keine Telefonnummern, Adressen oder Daten von Kindern im Bild — auch nicht in einem
      einzelnen Frame, auch nicht unscharf.
- [ ] Keine Beleidigungen, Diagnosen oder Spekulationen ergänzt.
- [ ] Niemand wird zur Kontaktaufnahme, Meldungswelle oder Beschimpfung aufgefordert.
- [ ] Belegte Weitergabe und unbestätigter Verdacht sprachlich klar getrennt.
- [ ] Jeder Beleg-Clip einmal ganz angesehen: kein Zeichen verändert oder hinzuerfunden.
- [ ] Kommentare mit Drohungen, privaten Daten oder Beleidigungen werden gelöscht.

### Der Schluss-Hinweis, unter jeden Beitrag

> Dieser Beitrag dient der sachlichen Warnung und dem Schutz betroffener Mütter.
> Keine Beleidigungen, Drohungen oder Kontaktaufnahme zu beteiligten Personen.
> Private Daten werden gelöscht.

---

## Die sechs Reel-Blätter

In `templates/reels/` liegt je Reel ein Blatt mit Bildzuordnung, fertigen englischen
Prompts und der Einblendungsliste mit Timecodes. Zuerst aber `clip-bibliothek.md`
lesen: Mehrere Clips kommen in mehreren Reels vor und werden **nur einmal** erzeugt.
Für die sechs Reels der Serie sind das 12 Clips statt 19 — 336 statt 532 Credits.

| Blatt | Inhalt |
|---|---|
| `clip-bibliothek.md` | **zuerst lesen** — welche Clips es gibt und wer sie benutzt |
| `reel-1.md` | WARNUNG AN BETROFFENE MÜTTER |
| `reel-2.md` | SENSIBLE DATEN WURDEN WEITERGEGEBEN |
| `reel-3.md` | VERTRAULICH HEISST VERTRAULICH |
| `reel-4.md` | PRÜFE, WEM DU DATEN GIBST |
| `reel-5.md` | BEWEISE SICHERN. DATEN SCHÜTZEN. |
| `reel-6.md` | KEINE HETZJAGD. KLARE WARNUNG. |
