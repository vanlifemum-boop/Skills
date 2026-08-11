# Musikvideo „Der Gutachten-Troll"

Bauplan für das Musikvideo zum Song: 6:05, zwei Formate (16:9 für YouTube,
9:16 für Reels/TikTok), Songtext zeilenweise eingebrannt, Bildmaterial aus
zwölf KI-Clips, Kamerafahrten über das Poster und selbst gebauten Karteikarten.

## Was hier liegt

| Datei | Aufgabe |
|---|---|
| `liedtext.txt` → `liedtext.py` → `liedtext.json` | Songtext mit Abschnitten, Art (gesungen/gesprochen/effekt) und Silbenzahlen |
| `takt_analyse.py` → `analyse.json` | Tempo, Taktgitter, Gesangsphrasen aus dem Signal |
| `timing_bauen.py` → `timing.json` | Zeilen auf die Zeitachse legen; **die Stellschraube ist `FENSTER` oben im Skript** |
| `pruefstreifen.py` | Analyse und Timing als Bild — zur Kontrolle mit dem Auge |
| `struktur.py` | Selbstähnlichkeitsmatrix (hier unergiebig, der Song liegt auf einer Harmonieschleife) |
| `text_ass.py` → `bauplatz/text_*.ass` | Untertitel in der Optik des Posters |
| `szenen.json` → `clips_erzeugen.py` | die zwölf KI-Clips über kie.ai |
| `grafik_szenen.py` | Titel-, Akten- und Schlusskarten |
| `schnitt_bauen.py` → `schnitt.json` | Schnittliste: wann Clip, wann Einschub |
| `video_bauen.py` | Boomerangs, Teile, Endmontage |
| `vorschau.sh` | 480p-Schnellrender nur mit Text und Ton, für die Timing-Abnahme |

`material/` (Song, Poster) und `bauplatz/` (alles Gerenderte) bleiben per
`.gitignore` draußen.

## Ablauf von vorn

```bash
python3 liedtext.py
python3 takt_analyse.py          # braucht material/song.mp3
python3 timing_bauen.py
python3 text_ass.py --format 16-9 && python3 text_ass.py --format 9-16
./vorschau.sh                    # abnehmen lassen, dann erst weiter
python3 grafik_szenen.py
python3 clips_erzeugen.py --los   # kostet Credits
python3 schnitt_bauen.py
python3 video_bauen.py --format 16-9
python3 video_bauen.py --format 9-16
```

## Warum das Timing so gebaut ist

In dieser Umgebung ist keine Spracherkennung verfügbar (`huggingface.co` ist
von der Egress-Policy gesperrt), es gibt also kein Transkript mit Zeitstempeln.
Das Timing kommt deshalb aus drei Messungen am Signal — Taktgitter, Gesangs-
kurve aus Mitte-minus-Seite, Sprechpausen per `silencedetect` — plus den
Abschnittsfenstern in `timing_bauen.py`. Die erste Fassung ist damit begründet,
aber nicht gehört: **die Abnahme läuft über `vorschau.sh`**, und Korrekturen
gehören in `FENSTER`, nicht in `timing.json` (das wird überschrieben).

## Kosten

Zwölf Clips à 8 s, 720p, `bytedance/seedance-1.5-pro`: 28 Credits je Clip,
336 Credits ≈ 1,45 €. Dazu zwei Testläufe (28,4 Credits) und ein leerer
Fehlversuch, der trotzdem 14,4 Credits reserviert hat. Abgerechnet wird über
`skills/media-skill`; der Nachweis je Datei steht in `~/Medien/*/meta.json`.
