# Systemfehler Familie – Serienkonzept

Erklärvideos zu Jugendhilfe und Kinderrechten für Instagram Reels. Hauptfiguren und
Erzähler sind Mama und Thadeo. Jede Folge stellt eine Alltagsszene dem gegenüber, was
das Verfahren vorsieht und welches Recht das Kind hat.

## Format

- 1080 × 1920 (9:16), 30 fps, 90 bis 120 Sekunden
- Ohne Stimme: Dialog in Sprechblasen, Erklärungen als Texttafeln. Viele schauen auf Instagram stumm.
  Musik kann beim Hochladen direkt in Instagram ausgewählt werden.
- Gebaut mit HyperFrames (HTML + GSAP), ohne externe KI-Dienste

## Look

- Farben wie GutachtenKompass: Schwarz/Weiß tragen, **Rot** = Systemfehler und Lücke,
  **Petrol** = Recht, **Ocker** = Wärme und Zuhause
- Schriften: Archivo Black (Überschriften), Inter (Text)
- Figuren: freigestellte Posen aus den Figurenblättern (`assets/figuren/`),
  je vier Posen: `ruhig`, `erklaert`, `denkt`, `zeigt`
- Kulissen und Gegenstände (Telefon, Stuhl, Akte, Sofa …) als CSS/SVG gezeichnet
- Alle Texte innerhalb der Instagram-Schutzzone (x 120–888, y 288–1248)

## Aufbau jeder Folge

| Teil | Dauer | Inhalt |
|---|---|---|
| Einstieg | 5 s | Kernfrage groß, Serienstempel „Systemfehler Familie · Folge NN“, Titel. Bild 0 ist das Vorschaubild. |
| Szene | 15–20 s | Alltagsmoment aus Thadeos oder Mamas Sicht, Sprechblasen. Kennzeichnung „Szenische Darstellung“. |
| Gegenseite | 12–17 s | Die andere Figur reagiert und fragt nach. |
| Nachfrage | ~14 s | Was steht im Papier? Welche Fragen bleiben offen? |
| So ist es vorgesehen | ~15 s | Ablauf in 3–4 Schritten mit Paragrafen |
| Euer Recht | ~17 s | Petrol-Karte(n) mit Erklärung und Norm, der Dialog läuft weiter |
| Die Lücke | ~11 s | Oben „In den Unterlagen“, unten „Erlebt“, roter Riss „SYSTEMFEHLER“ |
| Schlussfrage | 10 s | Frage aus dem Szenenplan, Aufruf zum Kommentieren, Hinweis „Szenische Darstellung nach Schilderung der Familie. Keine Rechtsberatung.“ |

## Wortwahl

Formulierungen aus dem Szenenplan übernehmen: „nach ihrer Schilderung“, „sinngemäß“,
„szenische Darstellung“. Keine Daten, Namen von Mitarbeitenden oder Absagen zeigen.
Die Paragrafen stammen aus dem Szenenplan und sind vor der Veröffentlichung fachlich zu prüfen.

## Folgen

| Nr. | Titel | Status |
|---|---|---|
| 01 | Nach der Sendung | offen |
| 02 | Der Stuhl im Büro | fertig (`folge-02-stuhl-im-buero/`) |
| 03 | Was ich dir sagen wollte | offen |
| 04 | Steht mein Schweigen da auch? | offen |
| 05 | Für dich allein | offen |
| 06 | Die erste Ziffer | offen |
| 07 | Die Zahnbürste | offen |
| 08 | Morgen bitte wieder | offen |
| 09 | Ich wusste nicht, dass da ein Richter ist | offen |
| 10 | Was passiert ohne Hilfeplanung? | offen |
| 11 | Warum ich oben bleibe | offen |
| M1 | Die WhatsApp | offen (braucht geschwärzte Originalausschnitte) |
| M2 | An welcher Tür? | offen |
| M3 | Für immer? | offen (mit Serienabschluss) |

## Neue Folge anlegen

1. Ordner `folge-02-stuhl-im-buero/` kopieren und umbenennen.
2. `assets/serie.css` und `assets/serie.js` bleiben gleich, die Figuren auch.
3. Szenen in `compositions/` umschreiben, Zeiten in `index.html` anpassen.
4. `npx hyperframes check --safe-zone reels`, dann
   `npx hyperframes render --quality delivery --output renders/<name>.mp4`.
