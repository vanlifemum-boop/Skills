# Tussy Van — Cinematic Scroll Website

Dark-Premium-Onepager für die Camper-Marke **Tussy Van** mit 3D-Scroll-Effekt:
Zwei Higgsfield-generierte Szenen (Exterieur & Interieur) werden als Frame-Sequenzen
per Canvas gescrubbt — Scrollen spielt die Kamerafahrt vor und zurück.

## Starten

Kein Build nötig — statisches HTML/CSS/JS:

```bash
cd tussy-van
python3 -m http.server 8080
# → http://localhost:8080
```

## Struktur

| Pfad | Inhalt |
|---|---|
| `index.html` | Sektionen: Hero, Produkte, Story, Features, CTA, Footer (+ `SCRUB_SECTIONS`-Konfiguration) |
| `css/styles.css` | Dark-Premium-Theme (Dunkelgrün `#07100b`–`#234f38`, Rot `#c22a30`) |
| `js/scroll-cinematic.js` | Scrub-Engine: Frame-Preload, Canvas-Cover-Draw, Overlay-Fades, Reveals, Card-Tilt |
| `js/lenis.min.js` | Lenis Smooth Scroll (vendored) |
| `frames/hero/`, `frames/interior/` | je 160 JPG-Frames (ffmpeg-Kamerafahrt aus den Keyframes) |
| `assets/` | Higgsfield-Originalbilder (nano_banana) |
| `img/` | Web-optimierte Produktbilder |

## Frames neu generieren

```bash
ffmpeg -i assets/hero.png -vf "scale=7000:-2,zoompan=z='1+0.22*on/159':d=160:x='(iw-iw/zoom)*0.58':y='(ih-ih/zoom)*0.45':s=1408x792" -frames:v 160 -q:v 6 frames/hero/frame_%04d.jpg
```

Sobald Higgsfield-Video-Credits verfügbar sind (Basic-Plan+), können die
Standbild-Kamerafahrten durch echte Orbit-/Flythrough-Clips ersetzt werden:
Clip generieren, dann `ffmpeg -i clip.mp4 -vf "fps=160/6,scale=1408:-2" -q:v 6 frames/hero/frame_%04d.jpg`.
