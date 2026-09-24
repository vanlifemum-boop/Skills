# Skydancer System Services – Vorab-Onepager

Umsetzung der Startseite aus dem Website-Konzept (Phase „Pilot“, Tag 31–60: *Onepager als Vorab-Seite live*).
Eine einzige, eigenständige Datei: `index.html` (kein Build, keine Abhängigkeiten außer Google Fonts).

Die bestehende GutachtenKompass-Seite unter `docs/` ist davon unberührt.

## Aufbau (8 Abschnitte laut Konzept)

1. Hero mit Kernbotschaft, zwei CTAs und den drei Persona-Einstiegen („Autark reisen“, „Unterwegs arbeiten“, „Sicher unterwegs“)
2. Vertrauensleiste
3. Problem „Fünf Geräte, fünf Apps, drei Werkstätten“ plus die vier Abgrenzungspunkte
4. Fünf Bausteine mit Preisangabe
5. Command Center: Fahrzeuggrafik mit Hotspots, Paketpreis, Angebotsleiter (Command Center „Empfohlen“)
6. So arbeiten wir: vier Schritte
7. Referenz mit Auszug aus der digitalen Fahrzeugakte
8. Anfrage-Konfigurator in vier Schritten mit Paketvorschlag und unverbindlicher Preisspanne

Dazu: Sticky-CTA auf Mobilgeräten, Footer mit Werkstatt, Öffnungszeiten und Rechtlichem.

## Platzhalter (auf der Seite gestrichelt markiert)

- Zertifizierungen, Anzahl Projekte, Google-Bewertung
- Preis des Technik-Checks (offene Entscheidung im Konzept)
- Referenzprojekt: Muster, bis das erste Pilotprojekt freigegeben ist (Zitat, Fotos, Zahlen der Fahrzeugakte)
- Werkstattadresse, Öffnungszeiten, Karte
- Impressum, Datenschutz, AGB, Partnerseite (Links zeigen noch auf den Footer)
- Hero-Video: vorerst eine gezeichnete Szene zur blauen Stunde; das Video kommt nach dem Fotoshooting

## Annahmen, bitte prüfen

- **„ab“-Preise je Baustein** stehen im Konzept nur für Internet Pro (3.500–5.900 €). Die anderen Bausteine zeigen das Paket, in dem sie enthalten sind.
- **Zuordnung SmartCamper → Touring Connected** und der **Umfang von Command Center** (Kamera, SmartCamper, Internet, Security, Fahrzeugakte, 12 Monate Support) sind aus den Personas abgeleitet.
- **Paketvorschlag im Konfigurator** (`vorschlag()` im Skript):
  - Autarkie + mindestens 2 weitere Bausteine → Expedition Signature
  - Kamera + SmartCamper + Internet + Security → Command Center
  - nur Kamera und/oder Security → Vision & Security
  - nur Internet → Internet Pro als Einzelleistung
  - Internet und/oder SmartCamper ohne Kamera, Security oder Autarkie → Touring Connected
  - alles andere → „Individuelle Kombination“, Preisrahmen im Rückruf
- **Die Vertrauensleiste** nennt Marken als „Systeme, die wir integrieren“, nicht als Partner. Bitte erst nach einer echten Partnerschaft umbenennen.
- **Typografie:** Archivo (Überschriften), IBM Plex Sans (Text), IBM Plex Mono (Anzeigen und Zahlen). Das Konzept nennt Space Grotesk und Inter nur als Beispiele.

## Vor dem Launch

- **Schriften selbst hosten:** Google Fonts direkt einzubinden ist in Deutschland datenschutzrechtlich riskant, darum die Schriften wie in `docs/fonts/` lokal ablegen.
- **Formular anbinden:** Der Konfigurator sendet noch nichts. Anbindung an CRM (HubSpot/Pipedrive) und Terminbuchung (Cal.com/Calendly) mit Anzahlung.
- **Strukturierte Daten:** LocalBusiness, Service, FAQ, Review.
