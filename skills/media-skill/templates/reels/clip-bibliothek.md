# Clip-Bibliothek

Zwölf Clips à 8 Sekunden, aus denen alle sechs Reels zusammengesetzt werden.
Mehrfach verwendete Clips werden **einmal** erzeugt — das ist der Unterschied
zwischen 336 und 532 Credits.

| Clip | Bild | Rolle | Verwendet in | Was zu sehen ist |
|---|---|---|---|---|
| `C01` | `cover-reel1-warnung.png` | Hook | Reel 1 | Akte, Warndreieck, geschwärzte Blätter |
| `C02` | `cover-reel2-sensible-daten.png` | Hook | Reel 2 | Akte, Kopie wandert aus dem Schutzkreis |
| `C03` | `cover-reel3-vertraulich.png` | Hook | Reel 3 | verschlossenes Tagebuch, roter Pfeil zerbricht den Schutzkreis |
| `C04` | `cover-reel5-beweise.png` | Hook | Reel 4, Reel 5 | Beweisumschlag, Kamera, Schutzschild |
| `C05` | `cover-reel6-hetzjagd.png` | Hook | Reel 6 | Mutter-Kind-Silhouette, Stoppschild, rote Nachrichtenfäden |
| `C06` | `kanal-motiv.png` | Hook | Reel 4 | Kanal-Motiv: Schild, Lupe, Fingerabdruck |
| `C07` | `kanal-motiv.png` | Abbinder | Reel 1, Reel 2, Reel 3, Reel 4, Reel 5, Reel 6 | Kanal-Motiv als Abbinder — **einmal erzeugt, in allen sechs Reels verwendet** |
| `B01` | `beleg-b1-sms.png` | Beleg | Reel 6 | SMS: „Klage oder Strafanzeige?" |
| `B02` | `beleg-b2-leck.png` | Beleg | Reel 1 | WhatsApp: „Irgendwo ist ein Leck passiert" |
| `B03` | `beleg-b3-0906.png` | Beleg | Reel 2, Reel 5 | **Kernbeleg** — „am 09.06 von mir Interna an eine andere Mutter weiter gab" |
| `B04` | `beleg-b4-streit-anonym.png` | Beleg | Reel 3 | WhatsApp 4. Juli 2026, Streitverlauf — Avatar abgedeckt |
| `B05` | `beleg-b5-gruppe-anonym.png` | Beleg | Reel 5 | Gruppe „Mütter Netzwerk Deutschland", viele Entfernungen — Avatar abgedeckt |

**12 Clips × 28 Credits = 336 Credits · 1,44 €**

---

## Erzeugen

Erst hochladen, dann sofort den Auftrag anlegen — die Upload-Adresse ist nicht
unbegrenzt gültig.

```bash
cd skills/media-skill

# Bild hochladen, URL merken (kostet nichts)
python3 scripts/kie.py hochladen ~/Medien/tatort-fake-mami-quellen/BILD.png --ordner images/tatort

# Clip erzeugen (28 Credits · 0,120 €)
python3 scripts/kie.py erzeugen \
  --modell bytedance/seedance-1.5-pro --aufloesung 720p --sekunden 8 \
  --prompt "PROMPT AUS DEM REEL-BLATT" \
  --projekt tatort-fake-mami \
  --extra '{"image_url": "https://…"}'
```
