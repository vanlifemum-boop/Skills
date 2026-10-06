# BSSD – Website

Statische Website für **BSSD – Beratung & Schulungen & Sport & Dienstleistungen** (Gregor Nebel).
Komplett getrennt von der GutachtenKompass-Seite in `docs/`.

## Aufbau – jede Säule hat ihr eigenes Verzeichnis

| Pfad | Inhalt |
|---|---|
| `index.html` | Startseite: die drei Säulen, Einzel-AAT®, Zielgruppen |
| `beratung/` | **Säule 01** – Systemische Familien-, Krisen- & Mobbingberatung, B2B, Zertifikate |
| `sport/` | **Säule 02** – Personal Training (Boxen, Kickboxen, Kraft, Mobilität, funktionell), Ernährung |
| `schulungen/` | **Säule 03** – Sicherheit, Gewaltschutz, Deeskalation, Gesprächsführung |
| `anti-gewalt-training/` | Einzel-AAT® (Inhalte aus dem Flyer) |
| `ueber-mich/`, `kontakt/`, `impressum/`, `datenschutz/` | Weitere Seiten |
| `assets/` | Gemeinsames CSS, JS, Favicon |

Jede Säule hat einen eigenen Hero-Bereich und eine eigene Akzentfarbe
(Beratung Blau, Sport Glutrot, Schulungen Signalgold, AAT Justizgrau).
Über die Säulenleiste unter dem Menü wechselt man direkt zwischen den drei Säulen.

## Bearbeiten

Die Texte stehen in `_inhalt/*.html`. Kopf, Säulenleiste und Fußbereich ergänzt das Skript:

```bash
python3 bssd/_bauen.py
```

Telefon, E-Mail und Ort einmal oben in `_bauen.py` (`STAMM`) eintragen und neu bauen.
Dann werden alle gelb markierten Platzhalter ersetzt.

## Vor dem Livegang noch offen

- [ ] Telefon, E-Mail, Ort (`STAMM` in `_bauen.py`)
- [ ] Impressum: Anschrift, USt-Angabe, Markenhinweis AAT®
- [ ] Datenschutz: Hosting-Anbieter eintragen, rechtlich prüfen lassen
- [ ] Über mich: Porträtfoto, Abschluss Pädagogik/Soziale Arbeit, Sport-Lizenzen
- [ ] Optional: Schriften lokal einbinden (statt Google Fonts) und echte Fotos
