---
name: uglyfunnel
description: Baut für ein Unternehmen komplette Ugly Funnels für alle fünf Bewusstseinsstufen (Unaware bis Most Aware) – Recherche, Framework und je Stufe ein eigener Funnel mit Anzeige, Funnel-Seite, Danke-Seite und E-Mails. Funnel-Arten nach den Klassikern des Direktmarketings – Advertorial, Quiz, Listicle, Gratis-Ratgeber, VSL zum Freischalten, Webinar, Angebotsseite. Pur wie ein Advertorial, vom Kunden nur das Logo. Nutze diesen Skill bei "/uglyfunnel", "Ugly Funnel", "Funnel für alle Awareness-Stufen", "Advertorial bauen", "Funnel statt Webseite", "Landingpages für jede Bewusstseinsstufe".
---

# /uglyfunnel – Funnels für alle fünf Bewusstseinsstufen

Eine Premium-Webseite erreicht vor allem die Menschen, die schon kaufen wollen. Laut Chet Holmes sind das von 100 nur
3, dazu 7, die offen dafür sind. Die anderen 90 erreichst du mit Funnels: schlichte Seiten, die genau bei dem ansetzen,
was die Person gerade weiß und denkt. Dieser Skill baut sie komplett.

**Grundprinzip:** Funnel-Seiten sind keine Webseiten. Keine Navigation, ein Ziel, ein Angebot. Pur wie ein
Zeitungsartikel (weiß, schlichte Schrift, gelbe Markierung). Vom Kunden kommt nur das Logo rein, kein Branding.

## Ablauf

### 1. Infos klären (fehlendes kurz nachfragen)
Firma, Ort, **ein** Produkt (z. B. „Komplettbad“, nicht „Badsanierung allgemein“), Logo-Datei oder Webseite, Telefon,
Adresse, Bewertungen (Anzahl, Schnitt), echte Fotos (Projekte, Team, Problemstellen). Keine erfundenen Kundenzahlen
ohne Hinweis: Fehlt etwas, Platzhalter `[[…]]` setzen und am Ende auflisten.

### 2. Recherche → `recherche.md`
Was beschäftigt die Zielgruppe auf jeder Stufe? Quellen: Google-Suchvorschläge (`suggestqueries.google.com`), Foren,
Verbände, Studien, Statistiken. **Nur belegte Zahlen**, jede mit Quelle; jede Zahl im Original prüfen. Keine Namen von
Konkurrenten in die Funnels übernehmen. Details: `references/bewusstseinsstufen.md`.

### 3. Framework → `framework.md` (dem Nutzer zeigen, bevor gebaut wird)
Tabelle, eine Zeile je Stufe: **Gedanke** (wörtlich, wie der Kunde denkt) · **Frage im Kopf** · **Einstieg**
(Lead-Typ nach *Great Leads*) · **Funnel-Art** · **Angebot** (ein kleiner nächster Schritt) · **Herkunft** (woher die
Menschen kommen). Produkt ≠ Anbieter: Product Aware zweifelt am Produkt, nicht an der Firma.

### 4. Funnels bauen → `funnels/`
Je Funnel ein Ordner mit `anzeige.html`, `seite.html`, `danke.html`, `emails.html`, dazu `funnels/index.html` als
Übersicht. Funnel-Art je Stufe aus `references/funnel-arten.md` (Aufbau, Pflichtteile, Überschrift-Muster).
Stil und Texte nach `references/stil-und-texte.md`.

Standard-Zuordnung:

| Stufe | Funnel-Art | typisches Angebot | Herkunft |
|---|---|---|---|
| 1 Unaware | Advertorial (Zeitungsartikel) | kostenloser Check / Messung | Facebook, Instagram |
| 2 Problem Aware | Quiz | Gratis-Check mit Ergebnis | Facebook, Instagram |
| 3 Solution Aware | Listicle **und** Gratis-Ratgeber (PDF gegen E-Mail) | kostenlose Planung | Google-Suche |
| 4 Product Aware | VSL zum Freischalten **und** Webinar | Beratungs-/Planungstermin | Retargeting, E-Mail |
| 5 Most Aware | Angebotsseite (Festpreis, Telefon, Kalender) | Angebot / Termin | Startseite, Name bei Google, E-Mail |

### 5. Prüfen
`python3 scripts/pruefen.py <ordner>/funnels` macht von jeder Seite Ganzseiten-Screenshots bei 1920 und 390 px
(`funnels/_vorschau/`) und meldet JS-Fehler und seitliches Scrollen. Jeden Screenshot ansehen und gegen
`references/stil-und-texte.md` → „Prüfliste“ abhaken. Formulare durchklicken (leiten per JS auf `danke.html`).

### 6. Übergabe
Kurz: welche Funnels, welche Angebote, welche Platzhalter `[[…]]` der Nutzer noch füllen muss (Fotos, Video, Zahlen),
und dass die Formulare noch an ein echtes Ziel (CRM, E-Mail-Tool, Kalender) angebunden werden müssen – bis dahin
leiten sie nur per JS auf `danke.html`.
