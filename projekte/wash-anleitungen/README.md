# WaSH Innovation — Anleitungen neu erzeugt

Instagram-Karussells (4:5) und A4-Blätter für drei Produkte, erzeugt über kie.ai aus den
abfotografierten Originalanleitungen. Der Text ist gestrafft und neu formuliert, das Layout
folgt den Originalblättern.

**Die eine Regel:** Die Handbrause darf in Form, Kanten, Aufhängeschlitz, schwarzem Druckknopf
und Proportionen **nicht** vom Produktfoto abweichen. Geändert wird ausschließlich die Farbe
der Kappe — blau statt grün.

## Wie die Farbtreue sichergestellt wird

Nicht über den Prompt allein. Zuerst entsteht **ein** verbindliches Masterbild:
das Original-Produktfoto, bei dem `google/nano-banana-edit` nur die Farbe tauscht
(4 Credits). Erst dieses Masterbild geht als erste Referenz in jeden weiteren Auftrag.
Prompts allein erfinden die Produktform neu — ein erster Lauf ohne Master lieferte eine
klassische runde Duschbrause statt der kantigen Kappe.

```
Original (grün) ──nano-banana-edit──► produkt-blau-master.png ──► Referenz für alle 49 Aufträge
```

Die zweite Referenz je Auftrag ist das abfotografierte Originalblatt — sie gibt den
Zeichenstil vor (feine schwarze Konturlinien, cremeweißes Papier, nummerierte Kreise).

## Umfang

| Blatt | Karussell 4:5 Strich | Karussell 4:5 Foto | A4 |
|---|---|---|---|
| Pocket Shower (8 Schritte) | 9 | 9 | 1 |
| Pocket Bath+ (3 Anwendungen + 3 Schritte) | 7 | 7 | 1 |
| Bottle Shower Mini (6 Schritte) | 7 | 7 | 1 |

49 Bilder, rund 510 Credits (≈ 2,20 €). Karussell 2K, A4 4K im Seitenverhältnis 3:4.

## Ablauf

```bash
export KIE_API_KEY='...'
python3 lauf.py voll2.json 8      # 8 Aufträge parallel
```

`lauf.py` legt die Aufträge an, pollt alle acht Sekunden, lädt sofort herunter und schreibt
`meta.json` fort. Ablage: `~/Medien/JJJJ-MM-TT-wash-anleitungen/`.

## Was beim Bauen Zeit gekostet hat

- **Umlaute gehören in den Prompt.** Wer „druecken“ schreibt, bekommt „druecken“ ins Bild
  gesetzt — das Modell setzt den Text buchstabengetreu. Bei fotorealistischen Prompts
  korrigiert es stillschweigend, bei Strichzeichnungen nicht.
- **Referenzbilder brauchen einen Upload.** kie.ai nimmt nur URLs. Der Upload läuft über
  `https://kieai.redpandaai.co/api/file-base64-upload` und antwortet ohne `User-Agent`-Header
  mit HTTP 403 (Cloudflare 1010).
- **Menschen unter der Dusche fallen in die Inhaltsfilter.** Ein Slide „Person duscht“ wurde
  abgelehnt. Die fotorealistischen Motive zeigen deshalb nur Hände und das Produkt.
- **Ergebnis-URLs verfallen nach 24 Stunden** — deshalb lädt `lauf.py` sofort herunter.
