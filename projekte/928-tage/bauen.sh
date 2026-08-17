#!/usr/bin/env bash
# bauen.sh — schneidet aus den fünf Clips das fertige Reel „928 Tage".
#
#   bash projekte/928-tage/bauen.sh [QUELLORDNER]
#
# Erwartet im Quellordner 01.mp4 … 05.mp4.
# Ergebnis: 928-tage-reel.mp4, 1080 × 1920, 33 Sekunden, stumm.
#
# Stumm ist Absicht: die KI-Stimme aus dem ersten Video war unbrauchbar. Die Musik
# kommt aus Instagrams eigener Bibliothek — mehr Reichweite, rechtlich sauber.
set -euo pipefail

ORDNER="${1:-$HOME/Medien/2026-08-16-928-tage}"
ARBEIT="$(mktemp -d)"
trap 'rm -rf "$ARBEIT"' EXIT

command -v ffmpeg >/dev/null || { echo "ffmpeg fehlt: apt-get install -y ffmpeg"; exit 1; }

# Bild 1 bekommt eine Sekunde mehr, damit die Ruhe vor dem Klingeln trägt;
# Bild 5 läuft voll durch, weil sie am Fenster das Bild ist, auf dem man stehenbleibt.
LAENGEN=(7 6 6 6 8)

echo "Clips kürzen …"
for i in 1 2 3 4 5; do
  quelle="$ORDNER/0$i.mp4"
  [ -f "$quelle" ] || { echo "fehlt: $quelle"; exit 1; }
  # Kein Clip wird hier beschnitten — besonders Bild 3 nicht, das Kind muss ganz
  # im Bild bleiben. Falls ein Lauf doch erfundene Schrift einblendet: wie in den
  # anderen Projekten mit crop=…,scale=1080:1920 die betroffenen Bildzeilen wegnehmen.
  BILD="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30"

  # -an wirft den von Veo mitgelieferten Ton weg.
  ffmpeg -v error -y -i "$quelle" -t "${LAENGEN[$((i-1))]}" -an \
    -vf "$BILD" \
    -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p "$ARBEIT/$i.mp4"
  echo "file '$ARBEIT/$i.mp4'" >> "$ARBEIT/liste.txt"
done

echo "Aneinanderhängen …"
ffmpeg -v error -y -f concat -safe 0 -i "$ARBEIT/liste.txt" -c copy "$ARBEIT/roh.mp4"

# Die Einblendungen als .ass. Die Werte stammen aus dem ersten Video und sind dort
# teuer gelernt: BorderStyle 1 mit kräftiger Kontur (nicht der Kasten aus BorderStyle 3),
# sonst verschwindet weiße Schrift auf hellem Grund; MarginV 380, sonst verdeckt
# Instagrams Bedienleiste die letzte Zeile.
cat > "$ARBEIT/text.ass" <<'ASS'
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Haupt,DejaVu Sans,62,&H00FFFFFF,&H00000000,&HC8000000,0,0,1,5,2,2,90,90,380,1
Style: Stark,DejaVu Sans,76,&H00FFFFFF,&H00000000,&HC8000000,1,0,1,5,2,2,90,90,380,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.80,0:00:06.50,Haupt,,0,0,0,,Morgens um sieben\Nklingelte es an der Tür.
Dialogue: 0,0:00:07.50,0:00:12.50,Stark,,0,0,0,,Zehn Beamte\Nin unserer Wohnung.
Dialogue: 0,0:00:13.50,0:00:18.50,Stark,,0,0,0,,Sie trugen mein Kind hinaus.
Dialogue: 0,0:00:19.50,0:00:24.50,Haupt,,0,0,0,,Ein Beschluss in meiner Hand.\NSeitdem: 928 Tage.
Dialogue: 0,0:00:25.50,0:00:29.50,Haupt,,0,0,0,,Kein Anruf. Kein Besuch.
Dialogue: 0,0:00:29.80,0:00:33.00,Stark,,0,0,0,,928 Tage sind genug.
ASS

echo "Text einbrennen …"
# -crf 26 statt 23: die dichte Schraffur dieses Stils frisst deutlich mehr Bitrate als
# die Aquarellflächen der anderen Videos. Erst damit bleibt die Datei unter 30 MB.
ffmpeg -v error -y -i "$ARBEIT/roh.mp4" -vf "ass=$ARBEIT/text.ass" \
  -c:v libx264 -preset slow -crf 26 -maxrate 6M -bufsize 9M -pix_fmt yuv420p \
  -movflags +faststart "$ORDNER/928-tage-reel.mp4"

echo
echo "Fertig: $ORDNER/928-tage-reel.mp4"
ffprobe -v error -show_entries format=duration,size -show_entries stream=width,height \
  -of default=noprint_wrappers=1 "$ORDNER/928-tage-reel.mp4"
