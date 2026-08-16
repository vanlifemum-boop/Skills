#!/usr/bin/env bash
# bauen.sh — schneidet aus den fünf Clips das fertige Reel „1.370 Tage".
#
#   bash projekte/1370-tage/bauen.sh [QUELLORDNER]
#
# Erwartet im Quellordner 01.mp4 … 05.mp4.
# Ergebnis: 1370-tage-reel.mp4, 1080 × 1920, 33 Sekunden, stumm.
#
# Stumm ist Absicht: die KI-Stimme aus dem ersten Video war unbrauchbar. Die Musik
# kommt aus Instagrams eigener Bibliothek — mehr Reichweite, rechtlich sauber.
set -euo pipefail

ORDNER="${1:-$HOME/Medien/2026-08-16-1370-tage}"
ARBEIT="$(mktemp -d)"
trap 'rm -rf "$ARBEIT"' EXIT

command -v ffmpeg >/dev/null || { echo "ffmpeg fehlt: apt-get install -y ffmpeg"; exit 1; }

# Bild 1 bekommt eine Sekunde mehr, damit die Szene ankommt; Bild 5 läuft voll
# durch, weil das Ausgestreckt-Werden der Arme das Bild ist, auf dem man hängenbleibt.
LAENGEN=(7 6 6 6 8)

echo "Clips kürzen …"
for i in 1 2 3 4 5; do
  quelle="$ORDNER/0$i.mp4"
  [ -f "$quelle" ] || { echo "fehlt: $quelle"; exit 1; }
  BILD="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30"
  if [ "$i" = 2 ]; then
    # Über der Krankenhaustür hängt ein Schild mit erfundener Schrift — typisches
    # KI-Kauderwelsch. Statt 35 Credits für einen neuen Versuch schneiden wir die
    # oberen Bildzeilen weg: 1000 × 1778 (bleibt 9:16, keine Verzerrung).
    BILD="crop=1000:1778:40:142,scale=1080:1920,fps=30"
  fi

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
Dialogue: 0,0:00:00.80,0:00:06.50,Haupt,,0,0,0,,Wir kamen ins Krankenhaus,\Num Hilfe zu holen.
Dialogue: 0,0:00:07.50,0:00:12.50,Stark,,0,0,0,,Mit sieben Wochen\Nwar unser Kind weg.
Dialogue: 0,0:00:13.50,0:00:18.50,Stark,,0,0,0,,1.370 Tage.
Dialogue: 0,0:00:19.50,0:00:24.50,Haupt,,0,0,0,,Wir haben das Sorgerecht zurück.\NUnser Kind nicht.
Dialogue: 0,0:00:25.50,0:00:29.50,Haupt,,0,0,0,,Unser Kind will nach Hause.\NEs darf nicht.
Dialogue: 0,0:00:29.80,0:00:33.00,Stark,,0,0,0,,1.370 Tage sind genug.
ASS

echo "Text einbrennen …"
# -crf 23 statt 20: Instagram rechnet ohnehin neu, und unter 30 MB lässt sich die
# Datei überall verschicken. Sichtbar ist der Unterschied nicht.
ffmpeg -v error -y -i "$ARBEIT/roh.mp4" -vf "ass=$ARBEIT/text.ass" \
  -c:v libx264 -preset slow -crf 23 -maxrate 8M -bufsize 12M -pix_fmt yuv420p \
  -movflags +faststart "$ORDNER/1370-tage-reel.mp4"

echo
echo "Fertig: $ORDNER/1370-tage-reel.mp4"
ffprobe -v error -show_entries format=duration,size -show_entries stream=width,height \
  -of default=noprint_wrappers=1 "$ORDNER/1370-tage-reel.mp4"
