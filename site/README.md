# Seifenglück — DIY-Naturkosmetik-Website

Eine hochwertige, statische Website im „Clean-Beauty"-Look mit 10 originalen
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
- `styles.css` — Design (Palette, Typografie, Karten, Scroll-Reveals, responsive).
- `recipes.js` — **alle Rezept-Inhalte** (hier neue Rezepte ergänzen/bearbeiten).
- `main.js` — Rendering der Rezepte, Filter, Copy-Buttons, Scroll-Effekte.

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

## Optional: Cinematic-Video-Hero
Für den echten „Scroll-Cinematic"-Video-Effekt (Higgsfield MCP) siehe die
Anleitung in `../SKILL.md`. Aktuell nutzt der Hero einen eleganten,
kostenlosen CSS-Effekt.
