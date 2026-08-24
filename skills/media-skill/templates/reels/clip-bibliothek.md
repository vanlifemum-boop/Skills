# Clip-Bibliothek

Zwölf Clips à 8 Sekunden, aus denen alle sechs Reels zusammengesetzt werden.
**Nur die sieben Cover-Clips kosten Geld.** Die fünf Beleg-Clips entstehen ohne KI.

## Warum Belege nicht durch ein Video-Modell gehen

Der erste Testlauf hat gezeigt, was passiert: Das Modell ließ Blätter durchs Bild
fliegen und schrieb Fantasiezeichen darauf, und aus dem Schriftzug „TATORT" wurde
nach zwei Sekunden ein anderes Wort. Bei einem Cover ist das ärgerlich. Bei einem
Beleg-Screenshot macht es aus einem Beweis eine Fälschung.

Deshalb gilt: **Belege gehen nie durch ein Video-Modell.** Sie bekommen einen
Schwenk über das unveränderte Bild — pixelgenau, unveränderbar, kostenlos.

```bash
python3 scripts/schwenk.py BELEG.png ZIEL.mp4 --sekunden 8
```

---

## Die Clips

| Clip | Bild | Rolle | Verwendet in | Weg | Kosten |
|---|---|---|---|---|---|
| `C01` | `cover-reel1-warnung.png` | Hook | Reel 1 | KI | 28 Cr |
| `C02` | `cover-reel2-sensible-daten.png` | Hook | Reel 2 | KI | 28 Cr |
| `C03` | `cover-reel3-vertraulich.png` | Hook | Reel 3 | KI | 28 Cr |
| `C04` | `cover-reel5-beweise.png` | Hook | Reel 4, Reel 5 | KI | 28 Cr |
| `C05` | `cover-reel6-hetzjagd.png` | Hook | Reel 6 | KI | 28 Cr |
| `C06` | `kanal-motiv.png` | Hook | Reel 4 | KI | 28 Cr |
| `C07` | `kanal-motiv.png` | Abbinder | alle sechs Reels | KI | 28 Cr |
| `B01` | `beleg-b1-sms.png` | Beleg | Reel 6 | Schwenk | **0** |
| `B02` | `beleg-b2-leck.png` | Beleg | Reel 1 | Schwenk | **0** |
| `B03` | `beleg-b3-0906.png` | Beleg — **Kernbeleg** | Reel 2, Reel 5 | Schwenk | **0** |
| `B04` | `beleg-b4-streit-anonym.png` | Beleg | Reel 3 | Schwenk | **0** |
| `B05` | `beleg-b5-gruppe-anonym.png` | Beleg | Reel 5 | Schwenk | **0** |

**7 Cover-Clips × 28 Credits = 196 Credits · 0,84 €**

---

## Cover-Clips erzeugen

Zwei Einstellungen entscheiden über brauchbar oder Ausschuss:

- **`fixed_lens: true`** — ohne das fährt die Kamera aus dem Motiv heraus und
  die Schlagzeile ist am Ende halb abgeschnitten.
- **Prompt kurz halten.** Lange Verbotslisten helfen nicht; eine davon wurde sogar
  vom Inhaltsfilter abgelehnt. Das Modell soll nur Mikro-Bewegung machen:
  Neon-Puls, Lichtschimmer. Die Kamerafahrt kommt hinterher aus ffmpeg.

```bash
# 1. Bild hochladen (kostet nichts)
python3 scripts/kie.py hochladen ~/Medien/tatort-fake-mami-quellen/COVER.png --ordner images/tatort

# 2. Clip erzeugen (28 Credits · 0,120 €)
python3 scripts/kie.py erzeugen \
  --modell bytedance/seedance-1.5-pro --aufloesung 720p --sekunden 8 \
  --prompt "Locked-off static camera. Every object stays exactly in place. Only the red neon triangle pulses very faintly and a soft light shimmer drifts across the surfaces. No papers move, shift, fly or turn. No new objects enter the frame. Vertical 9:16." \
  --projekt tatort-fake-mami \
  --extra '{"input_urls": ["URL"], "aspect_ratio": "9:16", "fixed_lens": true, "generate_audio": false, "nsfw_checker": false}'

# 3. Feine Schrift aus dem Original zurückholen (kostet nichts)
python3 scripts/einfrieren.py CLIP.mp4 COVER.png CLIP-fest.mp4 --bereich 130,10,600,92
```

Schritt 3 ist Pflicht bei jedem Cover mit dem Schriftzug oben. Ohne ihn zerfällt
„TATORT" ab Sekunde zwei.

---

## Prüfen, bevor ein Clip in ein Reel geht

```bash
# Frames herausziehen und ansehen
ffmpeg -ss 0.1 -i CLIP.mp4 -frames:v 1 f1.png
ffmpeg -ss 4   -i CLIP.mp4 -frames:v 1 f2.png
ffmpeg -ss 7.9 -i CLIP.mp4 -frames:v 1 f3.png
```

Auf jedem Frame: Steht jeder Buchstabe noch da, wo er hingehört? Ist etwas ins Bild
gekommen, das im Original nicht war? Bei Nein: Clip verwerfen, nicht ausbessern.
