#!/usr/bin/env bash
# bauen.sh — schneidet aus den fünf Clips und dem Voiceover das fertige Reel.
#
#   bash projekte/244-tage/bauen.sh [QUELLORDNER]
#
# Erwartet im Quellordner 01.mp4 … 05.mp4 und die Sprachdatei (06.*).
# Ergebnis: 244-tage-reel.mp4, 1080 × 1920, 33 Sekunden.
set -euo pipefail

ORDNER="${1:-$HOME/Medien/2026-08-16-244-tage}"
ARBEIT="$(mktemp -d)"
trap 'rm -rf "$ARBEIT"' EXIT

command -v ffmpeg >/dev/null || { echo "ffmpeg fehlt: apt-get install -y ffmpeg"; exit 1; }

# Clip 1 bekommt eine Sekunde mehr, damit der Blick über die Schulter sitzt;
# Clip 5 läuft voll durch, weil die Umarmung das Bild ist, auf dem man stehenbleibt.
LAENGEN=(7 6 6 6 8)

echo "Clips kürzen …"
for i in 1 2 3 4 5; do
  quelle="$ORDNER/0$i.mp4"
  [ -f "$quelle" ] || { echo "fehlt: $quelle"; exit 1; }

  BILD="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30"
  if [ "$i" = 3 ]; then
    # Im Kalenderclip steht oben eine erfundene Wochentagszeile — typisches
    # KI-Kauderwelsch. Statt 35 Credits für einen neuen Versuch auszugeben,
    # schneiden wir sie weg: 855 × 1520 mittig heraus (bleibt 9:16, keine
    # Verzerrung) und wieder auf volle Größe. Übrig bleiben die Kreuze.
    BILD="crop=720:1280:180:640,scale=1080:1920,fps=30"
  fi

  # -an wirft den von Veo mitgelieferten Ton weg — darunter kommt das Voiceover.
  ffmpeg -v error -y -i "$quelle" -t "${LAENGEN[$((i-1))]}" -an \
    -vf "$BILD" \
    -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p "$ARBEIT/$i.mp4"
  echo "file '$ARBEIT/$i.mp4'" >> "$ARBEIT/liste.txt"
done

echo "Aneinanderhängen …"
ffmpeg -v error -y -f concat -safe 0 -i "$ARBEIT/liste.txt" -c copy "$ARBEIT/roh.mp4"

# Die Einblendungen als .ass — eine eigene Datei ist übersichtlicher als ein
# drawtext-Filter mit fünf Zeitfenstern, und Umlaute gehen zuverlässig.
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
Dialogue: 0,0:00:00.80,0:00:06.50,Stark,,0,0,0,,Er durfte nur seinen Teddy mitnehmen.
Dialogue: 0,0:00:07.50,0:00:12.50,Stark,,0,0,0,,244 Tage.
Dialogue: 0,0:00:13.50,0:00:18.50,Haupt,,0,0,0,,244 Tage, in denen ich mein Kind vermisse.
Dialogue: 0,0:00:19.50,0:00:24.50,Haupt,,0,0,0,,Mein Kind wächst weiter.\NOhne mich.
Dialogue: 0,0:00:25.50,0:00:29.50,Haupt,,0,0,0,,Ich möchte einfach nur\Nwieder Mama sein.
Dialogue: 0,0:00:29.80,0:00:33.00,Stark,,0,0,0,,244 Tage sind genug.
ASS

STIMME=""
for kandidat in "$ORDNER"/06.*; do [ -f "$kandidat" ] && STIMME="$kandidat"; done

echo "Text einbrennen und Ton legen …"
if [ -n "$STIMME" ]; then
  ffmpeg -v error -y -i "$ARBEIT/roh.mp4" -i "$STIMME" \
    -vf "ass=$ARBEIT/text.ass" \
    -filter_complex "[1:a]adelay=500|500,volume=1.6,apad[a]" \
    -map 0:v -map "[a]" -shortest \
    -c:v libx264 -preset slow -crf 23 -maxrate 8M -bufsize 12M -pix_fmt yuv420p \
    -c:a aac -b:a 192k -movflags +faststart \
    "$ORDNER/244-tage-reel.mp4"
else
  echo "  (keine Sprachdatei gefunden — Reel wird stumm gebaut)"
  # -crf 23 statt 20: Instagram rechnet das Video ohnehin neu, und unter 30 MB
  # lässt es sich überall verschicken. Sichtbar ist der Unterschied nicht.
  ffmpeg -v error -y -i "$ARBEIT/roh.mp4" -vf "ass=$ARBEIT/text.ass" \
    -c:v libx264 -preset slow -crf 23 -maxrate 8M -bufsize 12M -pix_fmt yuv420p \
    -movflags +faststart "$ORDNER/244-tage-reel.mp4"
fi

echo
echo "Fertig: $ORDNER/244-tage-reel.mp4"
ffprobe -v error -show_entries format=duration,size -show_entries stream=width,height \
  -of default=noprint_wrappers=1 "$ORDNER/244-tage-reel.mp4"
