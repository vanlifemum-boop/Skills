# Clip-Bibliothek

Zwölf Clips à 8 Sekunden, aus denen alle sechs Reels zusammengesetzt sind.
**Vier davon kosten Geld, acht nicht.**

## Was der erste Durchlauf gelehrt hat

Drei Dinge, die beim nächsten Mal Geld sparen:

1. **`fixed_lens: true` ist Pflicht.** Ohne den Schalter fährt die Kamera aus dem
   Motiv heraus; nach acht Sekunden ist die Schlagzeile halb abgeschnitten und das
   Modell lässt Objekte durchs Bild fliegen — mit erfundenen Zeichen darauf.
2. **Feine Schrift überlebt nicht.** Aus „TATORT" wird nach zwei Sekunden ein
   anderes Wort. Deshalb wird der Schriftzug hinterher aus dem Original
   zurückgeholt (`einfrieren.py`) — das kostet nichts und ist Pflicht.
3. **Zwei von fünf Cover-Clips waren trotzdem Ausschuss** (C02, C06). Ersetzt durch
   einen ffmpeg-Zoom über dasselbe Bild: ruhiger, scharf, kostenlos. Bei Motiven
   mit vielen freistehenden Objekten lohnt der KI-Weg oft gar nicht.

## Belege gehen nie durch ein Video-Modell

Ein Modell, das eine Chatnachricht umschreibt, macht aus einem Beweis eine
Fälschung. Belege bekommen einen Schwenk über das unveränderte Bild — pixelgenau
und unveränderbar.

---

## Die Clips

| Clip | Bild | Rolle | Weg | Verwendet in | Kosten |
|---|---|---|---|---|---|
| `C01` | `cover-reel1-warnung.png` | Hook | KI | Reel 1 | 28 Cr |
| `C02` | `cover-reel2-sensible-daten.png` | Hook | Zoom | Reel 2 | **0** |
| `C03` | `cover-reel3-vertraulich.png` | Hook | KI | Reel 3 | 28 Cr |
| `C04` | `cover-reel5-beweise.png` | Hook | KI | Reel 4, Reel 5 | 28 Cr |
| `C05` | `cover-reel6-hetzjagd.png` | Hook | KI | Reel 6 | 28 Cr |
| `C06` | `kanal-motiv.png` | Hook | Zoom | Reel 4 | **0** |
| `C07` | `kanal-motiv.png` | Abbinder | Zoom zurück | alle sechs | **0** |
| `B01` | `beleg-b1-sms.png` | Beleg | Schwenk | Reel 6 | **0** |
| `B02` | `beleg-b2-leck.png` | Beleg | Schwenk | Reel 1 | **0** |
| `B03` | `beleg-b3-0906.png` | Beleg | Schwenk | Reel 2, Reel 5 | **0** |
| `B04` | `beleg-b4-streit-anonym.png` | Beleg | Schwenk | Reel 3 | **0** |
| `B05` | `beleg-b5-gruppe-anonym.png` | Beleg | Schwenk | Reel 5 | **0** |

**Tatsächlich abgerechnet: 196 Credits · 0,84 €** — darin zwei Testläufe
(56 Cr) und zwei verworfene Cover-Clips (56 Cr).

---

## Die Prompts der KI-Clips

**`C01`** — `cover-reel1-warnung.png`

```
The red neon triangle pulses very faintly and a soft light shimmer drifts across the surfaces. Locked-off static camera. Every object stays exactly in place. No papers move, shift, fly or turn. No new objects enter the frame. Vertical 9:16.
```

Danach Schriftzug einfrieren: `--bereich 120,2,610,100`

**`C03`** — `cover-reel3-vertraulich.png`

```
The cyan energy sphere shimmers and its glow pulses very faintly. A soft light reflection drifts slowly across the leather cover. Locked-off static camera. Every object stays exactly in place. No papers move, shift, fly or turn. No new objects enter the frame. Vertical 9:16.
```

Danach Schriftzug einfrieren: `--bereich 290,30,442,158`

**`C04`** — `cover-reel5-beweise.png`

```
The blue shield emblem glows and pulses very faintly. Faint dust motes drift slowly in the air. Locked-off static camera. Every object stays exactly in place. No papers move, shift, fly or turn. No new objects enter the frame. Vertical 9:16.
```

Danach Schriftzug einfrieren: `--bereich 195,46,525,118`

**`C05`** — `cover-reel6-hetzjagd.png`

```
The red network threads on the right shimmer very faintly. The blue glow on the left breathes slowly. Locked-off static camera. Every object stays exactly in place. No papers move, shift, fly or turn. No new objects enter the frame. Vertical 9:16.
```

Danach Schriftzug einfrieren: `--bereich 70,56,650,128`

---

## Die drei Befehle

```bash
# Cover mit KI beleben (28 Credits) — danach IMMER den Schriftzug einfrieren
python3 scripts/kie.py hochladen ~/Medien/tatort-fake-mami-quellen/COVER.png --ordner images/tatort
python3 scripts/kie.py erzeugen \
  --modell bytedance/seedance-1.5-pro --aufloesung 720p --sekunden 8 \
  --prompt "PROMPT VON OBEN" --projekt tatort-fake-mami \
  --extra '{"input_urls": ["URL"], "aspect_ratio": "9:16", "fixed_lens": true, "generate_audio": false, "nsfw_checker": false}'
python3 scripts/einfrieren.py CLIP.mp4 COVER.png CLIP-fest.mp4 --bereich L,O,R,U

# Beleg oder Ersatz-Cover ohne KI (0 Credits)
python3 scripts/schwenk.py BILD.png ZIEL.mp4 --sekunden 8            # Schwenk
python3 scripts/schwenk.py BILD.png ZIEL.mp4 --art zoom --sekunden 8 # heranfahren
python3 scripts/schwenk.py BILD.png ZIEL.mp4 --art zoomaus           # zurückfahren

# Reel zusammensetzen (0 Credits)
python3 scripts/zusammensetzen.py reel-1.mp4 C01.mp4 B02.mp4 C07.mp4
```

---

## Prüfen, bevor ein Clip in ein Reel geht

Frames bei 0, 4 und 8 Sekunden herausziehen und ansehen. Auf jedem: Steht jeder
Buchstabe noch da, wo er hingehört? Ist etwas ins Bild gekommen, das im Original
nicht war? Bei Nein: Clip verwerfen, nicht ausbessern.
