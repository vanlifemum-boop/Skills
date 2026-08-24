# Recht erklärt für Eltern

Eine Videoreihe für YouTube und Instagram, die Eltern familien- und jugendhilferechtliche
Abläufe erklärt. Folge 1 behandelt die Inobhutnahme nach § 42 SGB VIII.

Dieses Verzeichnis enthält den Inhalt der Reihe und das Werkzeug, das daraus Bildmaterial
erzeugt. Es enthält keinen Schnitt und keinen Upload — das passiert außerhalb.

---

## Die eine Quelle der Wahrheit

Alles zu einer Folge steht in **einer** Datei unter `folgen/`: Sprechertext, Einblendungen,
Paragrafenbelege, Bildprompts und der Reel-Plan.

```
folgen/folge-01-inobhutnahme.json     ← hier wird geändert
        │
        ├─ scripts/folge.py skript    → skript/folge-01-inobhutnahme.md   (Sprecherfassung)
        ├─ scripts/folge.py prompts   → fertige Prompts für kie.ai
        ├─ scripts/folge.py kosten    → Kostenvoranschlag, gerechnet nicht geschätzt
        └─ scripts/folge.py erzeugen  → ruft skills/media-skill/scripts/kie.py auf
```

Das Markdown-Skript ist **erzeugt**. Wer es direkt bearbeitet, verliert die Änderung beim
nächsten Lauf. Immer das JSON ändern, dann `skript` neu laufen lassen.

## Ablauf

```bash
cd projekte/recht-erklaert-fuer-eltern

python3 scripts/folge.py pruefen      # Struktur, Bilddeckung, englische Prompts
python3 scripts/folge.py skript       # Sprecherfassung für die juristische Prüfung
python3 scripts/folge.py kosten       # was der Bildlauf kostet
python3 scripts/folge.py erzeugen     # Trockenlauf: zeigt die Aufrufe, erzeugt nichts
python3 scripts/folge.py erzeugen --echt   # kostet Geld
```

Voraussetzung für `--echt` ist `KIE_API_KEY` in der Umgebung; alles andere läuft ohne
Netzzugang. Ergebnisse landen unter `~/Medien/JJJJ-MM-TT-recht-folge-01/`, protokolliert in
`meta.json`. Die Ergebnis-URLs von kie.ai verfallen nach 24 Stunden — `kie.py` lädt deshalb
sofort herunter.

Ein einzelnes Kapitel nachziehen: `--kapitel 8`.

## Warum kein eigener API-Client

Das Ursprungskonzept skizzierte ein eigenes `kie_client.py` mit erfundenen Endpunkten. Im
Repo liegt unter `skills/media-skill/scripts/kie.py` bereits ein Client, der die echte
kie.ai-API bedient, Preise rechnet, Ergebnisse herunterlädt und jeden Lauf protokolliert.
`folge.py` ruft ihn auf, statt ihn zu doppeln.

## Bilddeckung

Erzeugte Clips sind 4 bis 10 Sekunden lang, der Sprechertext einer Folge dauert rund
17 Minuten. Beides 1:1 zu belegen wäre teuer und sähe unruhig aus. Deshalb steht im JSON
eine **Zieldeckung**: der Anteil der Sprechzeit, der mit erzeugtem Material belegt wird.

```json
"bilddeckung": 0.45
```

Der Rest läuft über gehaltene Einstellungen, langsame Fahrten auf Standbildern und
Einblendungen. `pruefen` meldet jedes Kapitel, das um mehr als 15 Prozentpunkte abweicht.
Der Kaltstart hat eine eigene Deckung von 95 % — er läuft bewusst voll bebildert.

## Was Folge 1 kostet

Gerechnet mit `kie.py preis`, Stand der Preistabelle im Repo. 200 Credits sind ein
US-Dollar, ein Credit rund 0,0043 €.

| Posten | Menge | Modell | Credits | Euro |
|---|---|---|---|---|
| Bildmaterial | 62 Szenen · 496 s · 720p | `bytedance/seedance-1.5-pro` | 1736 | 7,47 € |
| Sprachaufnahme | 17,4 min | `google/gemini-2-5-pro-tts` | 104 | 0,45 € |
| Titelbilder Reels | 8 Bilder · 2K | `gpt-image-2-text-to-image` | 80 | 0,34 € |
| **Summe** | | | **1920** | **8,26 €** |

Alternativen: `grok-imagine/image-to-video` ist mit 4,5 Credits/s teurer **und** braucht je
Szene ein Startbild — `folge.py` bricht deshalb ab, wenn ein `image-to-video`-Modell ohne
`--extra` gewählt wird. `elevenlabs-multilingual-v2` kostet für denselben Text 0,91 € statt
0,45 €, bietet dafür Stimmauswahl. Preise ändern sich; vor einem großen Lauf `kie.py preis`
neu rechnen lassen.

## Zwei Ausspielwege

| | YouTube | Instagram Reels |
|---|---|---|
| Format | 1920 × 1080, 16:9 | 1080 × 1920, 9:16 |
| Länge | die ganze Folge, rund 17 min | ein Schwerpunkt, 30–60 s |
| Gliederung | Kapitelmarken aus dem Inhaltsverzeichnis | ein Kernsatz je Reel |
| Untertitel | ja | groß, hart eingebrannt |

Die acht Reels zu Folge 1 stehen im JSON unter `reels` und erscheinen am Ende des erzeugten
Skripts — je mit Hook, Kernsatz und Quellkapitel. Bildmaterial für die Reels wird aus den
Szenen der Quellkapitel beschnitten, nicht neu erzeugt.

---

## Vor der Veröffentlichung: juristische Prüfung

**Das Skript ist juristisch ungeprüft.** Es wurde nach Gesetzestext erstellt, nicht nach
Kommentarliteratur oder aktueller Rechtsprechung. Vor der Veröffentlichung muss eine
Fachanwältin oder ein Fachanwalt für Familienrecht gegenlesen. Diese Punkte gehören auf die
Prüfliste:

- [ ] Stimmen alle Paragrafenangaben im Feld `belege` mit der aktuellen Fassung überein?
- [ ] § 42 Abs. 1 S. 1 Nr. 2: Ist die zweistufige Prüfung (Buchst. a und b) korrekt
      wiedergegeben? Dieser Punkt trägt Kapitel 2 und Reel 2.
- [ ] Kapitel 9 und 13: Trennung von Familiengericht und Sozialgericht — ist die
      Rechtswegzuweisung für Inobhutnahmen im Zielbundesland unstreitig?
- [ ] Kapitel 13: Sind § 52 Abs. 2, § 54 Abs. 2 und § 57 FamFG als Ansatzpunkte gegen eine
      einstweilige Anordnung richtig und vollständig genug dargestellt?
- [ ] Kapitel 5: Aussage zum Umgangsrecht während der Inobhutnahme — belastbar formuliert?
- [ ] Kapitel 10: Trägt die Abgrenzung „Verfahrensfehler ≠ automatische Rückführung"?
- [ ] Kapitel 12: Hinweis auf § 201 StGB richtig eingegrenzt?
- [ ] Gibt es Länderbesonderheiten, die eine pauschale Aussage unzulässig machen?
- [ ] Ist der Hinweis „keine Rechtsberatung" an Anfang und Ende deutlich genug?

Erst wenn das erledigt ist, wird `pruefstand` im JSON umgestellt.

## Inhaltliche Leitplanken

Diese Regeln gelten für jede Folge und stehen als maschinenlesbare Fassung in
`stil/serienstil.txt`:

- Fehler werden als **mögliche** Fehler benannt, nie als Unterstellung gegen eine konkrete
  Behörde oder Person.
- Verfahrensfehler und Rechtsfolgen werden getrennt gehalten. Ein Fehler bringt kein Kind
  zurück — dieser Satz steht bewusst im Skript.
- Keine identifizierbaren Personen, keine echten Behörden, Wappen oder Logos im Bild.
- Kein lesbarer Text im generierten Bild: Modelle erfinden Schrift, und eine erfundene
  Aktennotiz sähe aus wie ein Beleg.
- Keine weinenden Kinder, kein Festhalten, kein Polizeieinsatz. Die Reihe erklärt, sie
  dramatisiert nicht.

## Geplante Folgen

| Nr. | Titel | Stand |
|---|---|---|
| 1 | Die Inobhutnahme – Ablauf und Voraussetzungen | Skript fertig, juristisch ungeprüft |
| 2 | Die ersten 24 Stunden – was passiert jetzt? | offen |
| 3 | Widerspruch der Eltern – was muss dann passieren? | offen |
| 4 | Das Familiengericht – wann muss es eingeschaltet werden? | offen |
| 5 | Akteneinsicht – welche Unterlagen gibt es? | offen |
| 6 | Dokumentation – warum jeder Zeitpunkt wichtig ist | offen |
| 7 | Fehler im Verfahren – was kann ein Fehler rechtlich bedeuten? | offen |
| 8 | Beschwerde, Dienstaufsicht oder Gericht? | offen |
| 9 | Das familienpsychologische Gutachten verstehen | offen |
| 10 | Welche Rechte hat das Kind? | offen |
| 11 | Welche Rechte haben Eltern? | offen |
| 12 | Der Weg zur Rückführung | offen |

Eine neue Folge beginnt als Kopie des Folgen-JSON. `folge.py` arbeitet mit jeder Datei:
`python3 scripts/folge.py --datei folgen/folge-02-erste-24-stunden.json pruefen`.
