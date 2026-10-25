# Seifenglück — DIY-Naturkosmetik-Website

Eine hochwertige, statische Website im Design **„Botanical Noir"** (dunkles
Nachtgrün, leuchtendes Blattgrün, Messing-Akzent) mit 10 originalen
DIY-Naturkosmetik-Rezepten, viralen Social-Media-Texten, Bild-Prompts und
Platz für Affiliate-Links & Werbung.

## Lokal ansehen
```bash
cd site
python3 -m http.server 8000
# dann im Browser: http://localhost:8000
```

## Dateien
- `index.html` — Struktur: Nav, Hero, „Warum DIY", Rezepte, Werbeplätze, Newsletter, Footer.
- `styles.css` — Design: Farb-Tokens (`--bg`, `--leaf`, `--brass` …), Typografie
  (Fraunces + Inter), Editorial-Reihen, Scroll-Reveals, responsive.
- `recipes.js` — **alle Rezept-Inhalte** (hier neue Rezepte ergänzen/bearbeiten).
- `main.js` — Rendering der Rezepte, Filter, Copy-Buttons, Scroll-Fortschritt,
  Parallax und gestaffelte Reveals.

## Neues Rezept hinzufügen
In `recipes.js` einen neuen Eintrag im `window.RECIPES`-Array ergänzen
(gleiche Felder wie bei den bestehenden). Die Seite rendert es automatisch.

## Affiliate-Links & Werbung
- **Affiliate:** In `recipes.js` bei jedem Rezept `affiliate.href` von `"#"`
  auf deinen echten Link ändern (z. B. Amazon PartnerNet). Die Buttons sind
  bereits mit `rel="sponsored nofollow"` ausgezeichnet.
- **Werbeplätze:** In `index.html` die `.ad__slot`-Boxen durch deinen
  Werbe-Code ersetzen (z. B. Google AdSense).
- **Pflicht in DE:** Der Transparenz-/Affiliate-Hinweis steht im Footer.
  Impressum & Datenschutz noch verlinken (Platzhalter im Footer).

## Rechtlicher Hinweis
Alle Rezepte, Texte und Bild-Prompts wurden eigenständig verfasst und basieren
auf gängigen, frei nutzbaren DIY-Grundrezepturen — es wurden keine geschützten
Inhalte Dritter übernommen.

## Design anpassen
Alle Farben stehen als CSS-Variablen ganz oben in `styles.css` unter `:root`.
Eine Farbe dort ändern färbt die ganze Seite um.

Hinweis: Die Reveal-Animationen sind an die Klasse `.js` gekoppelt (wird per
Inline-Skript im `<head>` gesetzt). Ohne JavaScript bleibt die Seite voll lesbar.

## Optional: Cinematic-Video-Hero
Für den echten „Scroll-Cinematic"-Video-Effekt (Higgsfield MCP) siehe die
Anleitung in `../SKILL.md`. Aktuell nutzt der Hero einen eleganten,
kostenlosen CSS-Effekt.
