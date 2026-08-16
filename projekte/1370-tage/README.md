# 1.370 Tage — Instagram-Reel im Graphic-Novel-Stil

Ein 33 Sekunden langes Hochformat-Video: Eltern kommen mit ihrem vier Wochen alten
Neugeborenen ins Krankenhaus, um Hilfe zu holen. Mit sieben Wochen ist das Kind weg.
Sie erkämpfen das Sorgerecht zurück — und bekommen ihr Kind trotzdem nicht.

Zweites Video der Reihe. Das erste liegt unter `projekte/244-tage/` und ist im
Anime-Stil; dieses ist bewusst das Gegenteil: europäische Graphic Novel, Tuschelinien
über Aquarell, realistische Gesichter.

| Datei | Inhalt |
|---|---|
| `prompts.md` | die fünf englischen Prompts, Stilblock und das Referenzbild-Verfahren |
| `texteinblendungen.md` | Einblendungen mit Zeiten, Bildunterschrift, Hashtags |
| `bauen.sh` | schneidet aus den fünf Clips das fertige Reel |

Erzeugt über **kie.ai**: Standbilder mit `gpt-image-2-text-to-image`, Clips mit `veo3.1`
(`lite`, 1080p) über `skills/media-skill/scripts/veo.py`, geschnitten mit `ffmpeg`.
Die Mediendateien liegen unter `~/Medien/2026-08-16-1370-tage/` und gehören **nicht**
ins Repo.

```bash
bash projekte/1370-tage/bauen.sh ~/Medien/2026-08-16-1370-tage/final
```

## Kein Ton

Das Reel ist stumm, und zwar mit Absicht. Die KI-Stimme aus dem ersten Video war
unbrauchbar. Die Musik kommt aus Instagrams eigener Bibliothek — mehr Reichweite,
rechtlich sauber, kein blockierter Download-Host.

## Was diesmal anders lief: Referenzbilder

Im ersten Video musste ein wortgleicher Figurenblock im Prompt dafür sorgen, dass die
Figur über fünf Clips gleich aussieht. Das hat nicht gereicht — drei Clips mussten
nachlaufen, und die Mutter kam am Ende mit falscher Haarfarbe heraus.

Diesmal: **erst ein Standbild für 6 Credits, dann dieses Bild als Referenz an die
Clips.** `veo.py --referenz URL` schaltet dafür auf `REFERENCE_2_VIDEO` um. Ergebnis —
Clip 1 und Clip 4 zeigen dieselbe Frau, obwohl zwischen ihnen ein Ortswechsel,
ein Tageszeitwechsel und dreieinhalb Jahre liegen.

Das Verfahren kostet fast nichts und ersetzt das Raten:

| | Preis | wofür |
|---|---|---|
| Standbild `gpt-image-2`, 2K | 6 Cr | Stil prüfen, Gesichter festlegen, Referenz liefern |
| Clip `veo3.1 lite`, 1080p | 35 Cr | der eigentliche Versuch |

Sechsmal billiger — deshalb wird jede Unsicherheit zuerst am Bild geklärt.

**Wo keine Personen vorkommen, kommt auch keine Referenz dazu.** Das Elternbild an ein
„leeres Zimmer" zu hängen holt die Eltern ins Bild. Clip 2 und 3 liefen deshalb nur mit
dem Stilblock — vorher an zwei Standbildern geprüft.

## Was gekostet wurde

| Posten | Credits |
|---|---|
| 3 Standbilder (1 Stilprobe, 2 Vorprüfungen) | 18 |
| 6 bezahlte Clips (5 verwendet, 1 verworfen) | 210 |
| **Summe** | **228 Cr · rund 0,98 €** |

Nachläufe: Clip 3 war flacher und kälter gezeichnet als die übrigen und fiel aus der
Reihe — neu mit „painted rather than sketched" und warmem Lampenlicht. Clip 4 brach
beim ersten Versuch serverseitig ab („Internal Error"), dafür sollte nichts berechnet
worden sein.

Zwei kleine Bildfehler wurden **im Schnitt** behoben statt für 35 Credits neu erzeugt:
über der Krankenhaustür in Clip 2 hing ein Schild mit erfundener Schrift — `bauen.sh`
schneidet die oberen Bildzeilen weg. Dasselbe Vorgehen wie beim Kalender im ersten Video.

## Die Leitplanken — nicht wegoptimieren

- **Die Pflegefamilie bleibt gesichtslos.** Silhouetten im Gegenlicht, keine Züge, keine
  Namen, kein Ortsbezug. Es geht um das Erleben der Eltern, nicht um einen Angriff auf
  bestimmte Menschen.
- **Keine Klinik, keine Behörde, kein Gericht benennen.** Keine Logos, keine Schilder,
  keine lesbaren Aktenzeichen. Das Blatt in Clip 4 ist **leer** — und muss es bleiben.
- **Kein echtes Kindergesicht, kein Foto.** Der gezeichnete Junge ist eine Figur, kein
  Abbild.
- **„Falsch diagnostiziert" ist ihre Schilderung** und wird als solche erzählt: über die
  geschlossene Akte im Bild, nicht über einen Vorwurf im Text.
- **KI-Inhalt kennzeichnen** — Instagrams Schalter plus der Satz in der Bildunterschrift.
  Bei realistisch gezeichneten Gesichtern wichtiger als beim Anime.

## Beim nächsten Mal

Die Zahl steht an zwei Stellen: in `texteinblendungen.md` und in `bauen.sh`. Ändern,
`bauen.sh` neu laufen lassen — dieselben Clips, neue Zahl, keine neuen Credits.
